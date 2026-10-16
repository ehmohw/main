"""2.65: FOLLOWER COSMETICS, and prices back up a little.

EMMA'S WARDROBE (Madame Velour): RIBBONS (Gold, Midnight, Mint, Snow, Crimson) re-tie the bow in her hair; DRESSES (the
  Sundress, the Midnight Gown, Sakura, the Royal Gown) re-dye her dress - her scarf still shows her buff's colour, so you
  can always tell what she's doing. Use one while she's out to dress her (it's kept - wear them as you like); sneak + use
  for her own pink ribbon or blue dress again.
CELI'S OUTFITS: Aurora, Rosehip, Midnight - her starry tunic and skirt in new colours.
ZIB'S UNIFORMS: the Crimson Guard and the Forest Ranger.
HIDDEN (only rare foes and secrets in the vault): Emma's PHANTOM RIBBON and STARLIGHT GOWN, Celi's FROSTFIRE outfit, Zib's
  GOLDEN ACE uniform.
PRICES: 2.63 halved everything and it was too cheap - now 70% of the old prices (the Scrap Bin follows). Unchanged: a
  Diamond is 2 Tokens at the Fence, the Fixer's Ledger 3 Tokens, Pearlman's gems a Medallion."""
import colorsys, json, os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int

PINK = '#ff8ad0'
RIBBONS = {1: ('Gold', '#e8b830'), 2: ('Midnight', '#3a3a9a'), 3: ('Mint', '#5ad8a8'), 4: ('Snow', '#f0f2fa'), 5: ('Crimson', '#d02a3a'), 6: ('Phantom', '#7a3adf')}
DRESSES = {1: ('Sundress', '#f0c040', '#d8a020'), 2: ('Midnight Gown', '#2c2c66', '#1e1e48'), 3: ('Sakura', '#f4a8c8', '#e088b0'),
           4: ('Royal Gown', '#f4efe2', '#d8c890'), 5: ('Starlight Gown', '#3c1c74', '#28105a'), 6: ('Gilded Gown', '#ffcf40', '#e0a820'),
           7: ('Diamond Gown', '#5ee8e0', '#34c8c4'), 8: ('Netherite Gown', '#5c5056', '#3c3338')}   # (6: 2.79a; 7, 8: 2.80c)
CELI = {1: ('Aurora', '#5ad8a8', '#3ab088'), 2: ('Rosehip', '#e07a98', '#c05878'), 3: ('Midnight', '#3a3a80', '#2a2a64'), 4: ('Frostfire', '#ff9a4a', '#e07428'),
        5: ('Gilded', '#ffcf40', '#e0a820'), 6: ('Diamond', '#5ee8e0', '#34c8c4'), 7: ('Netherite', '#5c5056', '#3c3338')}   # (5: 2.79a; 6, 7: 2.80c)
ZIB = {1: ('Crimson Guard', '#8a1a2a'), 2: ('Forest Ranger', '#2a5a30'), 3: ('Golden Ace', '#c8962a'), 4: ('Diamond Ace', '#34c8c4'), 5: ('Netherite Ace', '#5c5056')}
HIDDEN = {'cos_ribbon_6', 'cos_dress_5', 'cos_celi_4', 'cos_zib_3', 'cos_dress_6', 'cos_celi_5',
          'cos_dress_7', 'cos_dress_8', 'cos_celi_6', 'cos_celi_7', 'cos_zib_4', 'cos_zib_5'}   # (2.79a: the gilded ones only at the Tailor; 2.80c: diamond, netherite)
DYE = {'Gold': 'yellow', 'Midnight': 'blue', 'Mint': 'lime', 'Snow': 'white', 'Crimson': 'red', 'Phantom': 'purple', 'Sundress': 'yellow',
       'Midnight Gown': 'blue', 'Sakura': 'pink', 'Royal Gown': 'white', 'Starlight Gown': 'purple', 'Aurora': 'lime', 'Rosehip': 'pink',
       'Frostfire': 'orange', 'Crimson Guard': 'red', 'Forest Ranger': 'green', 'Golden Ace': 'yellow', 'Gilded Gown': 'yellow', 'Gilded': 'yellow',
       'Diamond Gown': 'light_blue', 'Netherite Gown': 'black', 'Diamond': 'light_blue', 'Netherite': 'black', 'Diamond Ace': 'light_blue', 'Netherite Ace': 'black'}


def _cos(iid, title, col, who, what, use):
    hidden = iid in HIDDEN
    item(iid, TOTEM, title, col, [what, (f'Use while {who} is with you: {use}.', 'blue'), ('Kept: change back and forth as you like.', 'gray'),
                                  ('Sneak + use: back to how she was.' if who != 'Zib' else 'Sneak + use: back to his navy.', 'gray')] +
         ([('Hidden: only rare foes and secrets carry it.', 'dark_gray')] if hidden else []),
         model=f'minecraft:{DYE[title.split(": ")[-1]]}_dye', glint=hidden or None, stack=1, cat='cosmetic', comps=hold('none'))


for _k, (_n, _c) in RIBBONS.items():
    _cos(f'cos_ribbon_{_k}', f"Emma's Ribbon: {_n}", _c, 'Emma', f'A {_n.lower()} ribbon for Emma\'s hair.', 'she ties it in her hair')
    HOLD[f'cos_ribbon_{_k}'] = f'bm:p78/use/ribbon{_k}'
for _k, (_n, _c, _c2) in DRESSES.items():
    _cos(f'cos_dress_{_k}', f"Emma's Dress: {_n}", _c, 'Emma', f'{_n} - her size exactly.', 'she wears it')
    HOLD[f'cos_dress_{_k}'] = f'bm:p78/use/dress{_k}'
for _k, (_n, _c, _c2) in CELI.items():
    _cos(f'cos_celi_{_k}', f"Celi's Outfit: {_n}", _c, 'Celi', f'Her starry tunic, in {_n.lower()}.', 'she changes (with a sigh)')
    HOLD[f'cos_celi_{_k}'] = f'bm:p78/use/celi{_k}'
for _k, (_n, _c) in ZIB.items():
    _cos(f'cos_zib_{_k}', f"Zib's Uniform: {_n}", _c, 'Zib', f'A trooper\'s tunic: the {_n}.', 'he changes into it')
    HOLD[f'cos_zib_{_k}'] = f'bm:p78/use/zib{_k}'


def _parts_with(models, prefix, keys):
    return sorted(n[len(prefix):] for n, (tex, _e) in models.items() if n.startswith(prefix) and any(k in tex for k in keys))


def extend_offers(O, offer):
    O['outfitter'] += [offer(('medallion', 2), (f'cos_ribbon_{k}', 1)) for k in RIBBONS if f'cos_ribbon_{k}' not in HIDDEN] + \
                      [offer(('medallion', 4), (f'cos_dress_{k}', 1)) for k in DRESSES if f'cos_dress_{k}' not in HIDDEN] + \
                      [offer(('medallion', 3), (f'cos_celi_{k}', 1)) for k in CELI if f'cos_celi_{k}' not in HIDDEN] + \
                      [offer(('medallion', 3), (f'cos_zib_{k}', 1)) for k in ZIB if f'cos_zib_{k}' not in HIDDEN]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    import phase57_art as EA, phase66_art as CA, phase72_art as ZA
    objs = ['bm.cosr', 'bm.cosd', 'bm.cosc', 'bm.cosz']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    model = lambda tag, m: f'execute as @e[type=minecraft:item_display,{tag}] run data modify entity @s item.components."minecraft:item_model" set value "bm:{m}"'

    # ================================================================== EMMA: her outfit now reads her wardrobe too
    OUT = EA.outfit_parts()
    MODES = (1, 2, 3, 4, 5)
    old = G.FUNCS['p57/outfit']
    G.FUNCS['p57/outfit'] = ['scoreboard players set #emd bm.rng 0', 'scoreboard players set #emr bm.rng 0',
                             'execute store result score #cp bm.rng run scoreboard players get @e[type=minecraft:item_display,tag=bm.emsel,limit=1] bm.pid',
                             'execute as @a if score @s bm.pid = #cp bm.rng run function bm:p78/emma_read'] + \
        ['execute if score #emd bm.rng matches 0 ' + l[len('execute '):] for l in old] + \
        [model(f'tag=bm.emsel,tag=bm.ep_{p}', f'em_{p}_d{d}_m{m}').replace('execute as', f'execute if score #emd bm.rng matches {d} if score #emo bm.rng matches {m} as')
         for d in DRESSES for m in MODES for p in OUT] + \
        [model('tag=bm.emsel,tag=bm.ep_head', 'em_head' if r == 0 else f'em_head_r{r}').replace('execute as', f'execute if score #emr bm.rng matches {r} as') for r in [0] + list(RIBBONS)]
    fn('p78/emma_read', ['scoreboard players operation #emd bm.rng = @s bm.cosd', 'scoreboard players operation #emr bm.rng = @s bm.cosr'])
    # (as the player: dress your Emma now, if she's out and not ethereal)
    fn('p78/emma_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid unless score @s bm.eme matches 1.. at @s run function bm:p78/emma_dress',
                        'execute if score #has bm.rng matches 0 run return run ' + say('Emma isn\'t with you - she\'ll wear it next time.', PINK)])
    fn('p78/emma_dress', ['scoreboard players set #has bm.rng 1',
                          'execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel',
                          'scoreboard players operation #emo bm.rng = @s bm.emm', 'function bm:p57/outfit', 'tag @e[tag=bm.emsel] remove bm.emsel',
                          'particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.7 0.4 0 24', 'playsound minecraft:entity.allay.item_given neutral @a[distance=..16] ~ ~ ~ 1 1.4'])
    for k, (nm, c) in RIBBONS.items():
        fn(f'p78/use/ribbon{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                  'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.cosr 0',
                                  f'execute unless predicate bm:p20/sneaking run scoreboard players set @s bm.cosr {k}', 'function bm:p78/emma_now',
                                  'execute if predicate bm:p20/sneaking run ' + say('"My pink ribbon! I missed it."', PINK),
                                  'execute unless predicate bm:p20/sneaking run ' + say(f'"{nm}? For me? I love it!"', PINK)])
    for k, (nm, c, c2) in DRESSES.items():
        fn(f'p78/use/dress{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                 'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.cosd 0',
                                 f'execute unless predicate bm:p20/sneaking run scoreboard players set @s bm.cosd {k}', 'function bm:p78/emma_now',
                                 'execute if predicate bm:p20/sneaking run ' + say('"Back in my sea-blue. Comfy!"', PINK),
                                 'execute unless predicate bm:p20/sneaking run ' + say(f'"The {nm}! How do I look? (Don\'t answer that.)"', PINK)])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvhc dummy']

    # ================================================================== CELI: her outfit swaps as she appears
    CM = CA.models()
    CELI_KEYS = ('ce_tunic', 'ce_skirt')
    CPARTS = _parts_with(CM, 'ce_', CELI_KEYS)
    G.FUNCS['p66/grow'] += ['function bm:p78/celi_dress']
    fn('p78/celi_dress', ['scoreboard players set #cd bm.rng 0',
                          'execute store result score #cp bm.rng run scoreboard players get @e[type=minecraft:item_display,tag=bm.cesel,limit=1] bm.pid',
                          'execute as @a if score @s bm.pid = #cp bm.rng run scoreboard players operation #cd bm.rng = @s bm.cosc'] +
       [model(f'tag=bm.cesel,tag=bm.cp6_{p}', f'ce_{p}' if k == 0 else f'ce_{p}_o{k}').replace('execute as', f'execute if score #cd bm.rng matches {k} as')
        for k in [0] + list(CELI) for p in CPARTS])
    fn('p78/celi_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        'execute as @e[type=minecraft:wolf,tag=bm.celipet] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
                        'execute as @e[type=minecraft:item_display,tag=bm.cep] if score @s bm.pid = #me bm.pid run tag @s add bm.cesel',
                        'execute if score #has bm.rng matches 1 run function bm:p78/celi_dress', 'tag @e[tag=bm.cesel] remove bm.cesel',
                        'execute if score #has bm.rng matches 0 run return run ' + say('Celi isn\'t with you - she\'ll wear it next time.', '#9ad8ff')])
    for k, (nm, c, c2) in CELI.items():
        fn(f'p78/use/celi{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.cosc 0',
                                f'execute unless predicate bm:p20/sneaking run scoreboard players set @s bm.cosc {k}', 'function bm:p78/celi_now',
                                'execute unless predicate bm:p20/sneaking run ' + say(f'"{nm}. Fine. It IS nice. Don\'t tell anyone."', '#9ad8ff'),
                                'execute if predicate bm:p20/sneaking run ' + say('"Finally, my real clothes."', '#9ad8ff')])

    # ================================================================== ZIB: a uniform for every occasion
    rig = ZA.zib_rig()
    ZPARTS = [n for n in rig.parts if any(f.get('texture') == '#s' for e in rig.shifted(n) for f in e['faces'].values())]
    G.FUNCS['p72/zb/rig'] += ['function bm:p78/zib_dress']
    fn('p78/zib_dress', ['scoreboard players set #zd bm.rng 0', 'scoreboard players operation #cp bm.rng = @s bm.pid',
                         'execute as @a if score @s bm.pid = #cp bm.rng run scoreboard players operation #zd bm.rng = @s bm.cosz'] +
       [f'execute if score #zd bm.rng matches {k} on passengers if entity @s[tag=bm.zbr_{n}] run data modify entity @s item.components."minecraft:item_model" set value "bm:zbr_{n}{"" if k == 0 else f"_u{k}"}"'
        for k in [0] + list(ZIB) for n in ZPARTS])
    fn('p78/zib_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                       'execute as @e[type=minecraft:wolf,tag=bm.zibpet] if score @s bm.pid = #me bm.pid at @s run function bm:p78/zib_now2',
                       'execute if score #has bm.rng matches 0 run return run ' + say('Zib isn\'t with you - he\'ll wear it next time.', '#3ad8c8')])
    fn('p78/zib_now2', ['scoreboard players set #has bm.rng 1', 'function bm:p78/zib_dress', 'execute at @s run particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.4 0.3 0.02 12'])
    for k, (nm, c) in ZIB.items():
        fn(f'p78/use/zib{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                               'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.cosz 0',
                               f'execute unless predicate bm:p20/sneaking run scoreboard players set @s bm.cosz {k}', 'function bm:p78/zib_now',
                               'execute unless predicate bm:p20/sneaking run ' + say(f'"The {nm}! Trooper Zib, reporting in style!"', '#3ad8c8')])

    # ================================================================== hidden ones: into the vault's rare tables
    hidden = ['cos_ribbon_6', 'cos_dress_5', 'cos_celi_4', 'cos_zib_3']
    for tb, w in (('shiny', 2), ('ratking', 0), ('secret', 1), ('champion', 1)):
        pth = G.path('data', 'bm', 'loot_table', 'p76', f'{tb}.json')
        if not os.path.exists(pth): continue
        lt = json.load(open(pth))
        if tb == 'ratking':
            lt['pools'].append({'rolls': 1, 'entries': [dict(G.loot_entry(i), weight=1) for i in hidden]})
        else:
            lt['pools'][0]['entries'] += [dict(G.loot_entry(i), weight=w) for i in hidden]
        G.wjson(f'bm/loot_table/p76/{tb}.json', lt)
    fn('admin/cosmetics', [give(f'cos_ribbon_{k}') for k in RIBBONS] + [give(f'cos_dress_{k}') for k in DRESSES] + [give(f'cos_celi_{k}') for k in CELI] +
       [give(f'cos_zib_{k}') for k in ZIB])


def _tint(im, dst, band=None):
    """re-dye an image: each pixel's brightness against the image's own average, carried onto the new colour"""
    from PIL import Image
    px = [im.getpixel((x, y)) for y in range(im.size[1]) for x in range(im.size[0])]
    sel = [p for p in px if p[3] and (band is None or band[0] <= colorsys.rgb_to_hls(*(v / 255 for v in p[:3]))[0] <= band[1])]
    avg = (sum(sum(p[:3]) / 3 for p in sel) / len(sel)) if sel else 128
    tc = tuple(int(dst[i:i + 2], 16) for i in (1, 3, 5))
    out = Image.new('RGBA', im.size)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            p = im.getpixel((x, y))
            h = colorsys.rgb_to_hls(*(v / 255 for v in p[:3]))[0]
            if p[3] and (band is None or band[0] <= h <= band[1]):
                k = (sum(p[:3]) / 3) / avg
                out.putpixel((x, y), tuple(int(max(0, min(255, c * k))) for c in tc) + (p[3],))
            else:
                out.putpixel((x, y), p)
    return out


BLUES = (0.47, 0.72)


def textures():
    import phase57_art as EA, phase66_art as CA, phase72_art as ZA
    E, C, Z = EA.textures(), CA.textures(), ZA.textures()
    out = {}
    for k, (nm, c) in RIBBONS.items():
        out[f'em2_pink_r{k}'] = _tint(E['em2_pink'], c)
        dk = '#' + ''.join(f'{max(0, int(int(c[i:i + 2], 16) * 0.72)):02x}' for i in (1, 3, 5))
        out[f'em2_pinkdark_r{k}'] = _tint(E['em2_pinkdark'], dk)
    import gild                                  # (2.79a: the gilded ones in polished gold - gild.py)
    for d, (nm, c, c2) in DRESSES.items():
        out[f'em2_blue_d{d}'] = gild.dress('emma', d, E['em2_blue']) if gild.is_gilded('emma', d) else _tint(E['em2_blue'], c, BLUES)
        out[f'em2_chest_d{d}'] = gild.dress('emma', d, E['em2_chest']) if gild.is_gilded('emma', d) else _tint(E['em2_chest'], c, BLUES)
        out[f'em2_skirt_d{d}'] = gild.dress('emma', d, E['em2_skirt']) if gild.is_gilded('emma', d) else _tint(E['em2_skirt'], c2, BLUES)
    for k, (nm, c, c2) in CELI.items():
        out[f'ce_tunic_o{k}'] = gild.dress('celi', k, C['ce_tunic']) if gild.is_gilded('celi', k) else _tint(C['ce_tunic'], c, BLUES)
        out[f'ce_skirt_o{k}'] = gild.dress('celi', k, C['ce_skirt']) if gild.is_gilded('celi', k) else _tint(C['ce_skirt'], c2, BLUES)
    for k, (nm, c) in ZIB.items():
        out[f'adon_trooper_u{k}'] = gild.dress('zib', k, Z['adon_trooper']) if gild.is_gilded('zib', k) else _tint(Z['adon_trooper'], c, (0.5, 0.75))
    return out


def rp(R):
    import sys
    import phase57_art as EA, phase66_art as CA, phase72_art as ZA
    R.TEXTURE_MODS.append(sys.modules[__name__])
    EM = EA.models()
    # Emma: her head with each ribbon; her dress parts with each dress, for every buff (the scarf keeps the buff's colour)
    tex, els = EM['em_head']
    for k in RIBBONS:
        R.HATS[f'em_head_r{k}'] = ({a: (f'{v}_r{k}' if a in ('em2_pink', 'em2_pinkdark') else v) for a, v in tex.items()}, els)
    DRESS_KEYS = ('em2_blue', 'em2_chest', 'em2_skirt')
    SCARF = ('em2_scarf', 'em2_scarf2')
    for p in EA.outfit_parts():
        tex, els = EM[f'em_{p}']
        for d in DRESSES:
            for m in (1, 2, 3, 4, 5):
                R.HATS[f'em_{p}_d{d}_m{m}'] = ({a: (f'{v}_d{d}' if a in DRESS_KEYS else (f'{v}_m{m}' if a in SCARF and m != 4 else v)) for a, v in tex.items()}, els)
    # Celi
    CM = CA.models()
    for p in _parts_with(CM, 'ce_', ('ce_tunic', 'ce_skirt')):
        tex, els = CM[f'ce_{p}']
        for k in CELI:
            R.HATS[f'ce_{p}_o{k}'] = ({a: (f'{v}_o{k}' if a in ('ce_tunic', 'ce_skirt') else v) for a, v in tex.items()}, els)
    # Zib (his rig's models are written straight out, like phase72's)
    def post(R2):
        rig = ZA.zib_rig()
        for n in rig.parts:
            els = rig.shifted(n)
            used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
            if 's' not in used: continue
            for k in ZIB:
                t = {a: (f'{ZA.ZB_TEX[a]}_u{k}' if a == 's' else ZA.ZB_TEX[a]) for a in used}; t['particle'] = ZA.ZB_TEX['f']
                R2.wj(f'assets/bm/models/item/zbr_{n}_u{k}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
                R2.wj(f'assets/bm/items/zbr_{n}_u{k}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/zbr_{n}_u{k}'}})
    R.POST.append(post)
