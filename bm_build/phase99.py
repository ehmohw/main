"""2.67: FOLLOWER WARDROBES - every outfit is yours for good, and every follower has a menu to change into them.

A COSMETIC, USED ONCE, IS UNLOCKED FOR GOOD (and used up): it goes into that follower's wardrobe. Then SNEAK + USE the
  follower's own item - any time, in the Overworld, whether they're out or not - for their menu: send them home, or
  change into any outfit they own, or back to their own clothes. Locked outfits show where to get them.
  (Emma: sneak + use while she's out still opens her buff menu - its WARDROBE button opens hers.)
NEW AT GOLDTOOTH (the raid shop): LEO'S TABARDS (Crimson Crusader, Royal Purple, Greenwood; hidden: Golden Champion),
  DEMOCRATUS' CLOAKS (Crimson Reaper, Ashen Shroud, Royal Violet; hidden: Gilded Storm), CECIL'S ROBES (Crimson, Midnight,
  Bone; hidden: Gilded) and KILLERWATT'S COLOURS (Midnight, Bone, Neon; hidden: Golden Thunder). Cecil's robe and
  KillerWatt's colours are their own look - with a gem in them, the gem's element shows instead.
"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, Int
import phase28 as P28
import phase78 as P78
import phase89 as P89
import phase79_art as KA

GOLD = '#ffcf40'
# who: (name, colour, item word, {k: (cosmetic name, (dark, mid, light))}); 4 is hidden in each
NEW = {'leo': ('Leo', '#5ab8e0', 'Tabard', {1: ('Crimson Crusader', ('#2a0408', '#9a1e2a', '#e0606a')), 2: ('Royal Purple', ('#140626', '#4a2280', '#a07ae0')),
                                            3: ('Greenwood', ('#0a2010', '#2a6a34', '#7ac080')), 4: ('Golden Champion', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Champion', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Champion', ('#141014', '#4a4046', '#9a8c94'))}),
       'demo': ('Democratus', '#7ad06a', 'Cloak', {1: ('Crimson Reaper', ('#22040a', '#8a1a24', '#e05a64')), 2: ('Ashen Shroud', ('#141416', '#55555c', '#b4b4bc')),
                                                   3: ('Royal Violet', ('#160626', '#562886', '#b48ae6')), 4: ('Gilded Storm', ('#3a2806', '#b8902a', '#ffe8a0')), 5: ('Diamond Storm', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Storm', ('#141014', '#4a4046', '#9a8c94'))}),
       'cecil': ('Cecil', '#b48cff', 'Robe', {1: ('Crimson', ('#2a060c', '#7a1a2a', '#c8506a')), 2: ('Midnight', ('#06081a', '#1e2450', '#5a64a0')),
                                              3: ('Bone', ('#5a5448', '#b8b0a0', '#f4efe4')), 4: ('Gilded', ('#3a2806', '#b08a2a', '#ffe8a0')), 5: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),
       'kw': ('KillerWatt', '#ffe040', 'Colours', {int(k[1:]): (nm, pal[0]) for k, (nm, pal) in KA.COS_PAL.items()}),
       # 2.78: the rest of the followers (their art is recoloured in phase138)
       'apo': ('Apophiss', '#3ad06a', 'Scales', {1: ('Obsidian Coil', ('#07070c', '#2a2a38', '#7a7a92')), 2: ('Blood Wyrm', ('#200406', '#7a1418', '#e0584e')),
                                                3: ('Frost Serpent', ('#0a2232', '#3a8ab4', '#c8ecff')), 4: ('Gilded Coil', ('#3a2806', '#b8902a', '#ffe8a0')), 5: ('Diamond Coil', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Coil', ('#141014', '#4a4046', '#9a8c94'))}),
       'tul': ('Tullius', '#7ad8ff', 'Coat', {1: ("Admiral's Blue", ('#060c24', '#1e3a8a', '#6a8ae0')), 2: ('Corsair Crimson', ('#22040a', '#8a1a24', '#e05a64')),
                                            3: ('Bleached Bone', ('#5a5448', '#b8b0a0', '#f4efe4')), 4: ('Gilded Captain', ('#3a2806', '#b08a2a', '#ffe8a0')), 5: ('Diamond Captain', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Captain', ('#141014', '#4a4046', '#9a8c94'))}),
       'frog': ('the Frog with Mustache', '#6ac850', 'Skin', {1: ('Bluejay', ('#1a2a6a', '#3a7ae0', '#8ac8ff')), 2: ('Ember Toad', ('#4a0e04', '#d0501a', '#ffa060')),
                                                             3: ('Old Bog', ('#2a1a0a', '#7a5430', '#c09a6a')), 4: ('Golden Prince', ('#3a2806', '#e0b02a', '#fff0a0')), 5: ('Diamond Prince', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Prince', ('#141014', '#4a4046', '#9a8c94'))}),
       'don': ('Donado', '#e8d29a', 'Coat', {1: ('Chocolate', ('#1a0e06', '#5a3418', '#a07048')), 2: ('Midnight', ('#08080c', '#2a2a34', '#7a7a8a')),
                                           3: ('Snowdrift', ('#8a8a90', '#dcdce0', '#ffffff')), 4: ('Starlit', ('#0a0626', '#4a2a9a', '#b49aff')),
                                           5: ('Gilded', ('#3a2806', '#e0b030', '#fff0a0')),
                                           6: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 7: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),        # (5: 2.79a - his gilded coat; 6, 7: 2.80c)
       'pearl': ('Pearlman', '#5ac8ff', 'Bow Tie', {1: ('Ruby', ('#3a0408', '#c0202a', '#ff7a80')), 2: ('Emerald', ('#04260e', '#1a9a44', '#7aff9a')),
                                                    3: ('Amethyst', ('#1a0630', '#7a3ac0', '#d0a0ff')), 4: ('Gilded', ('#3a2806', '#e0b030', '#fff0a0')), 5: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),
       'fishy': ('Fishy', '#ffa040', 'Top Hat', {1: ('Midnight Silk', ('#06081c', '#1e2a6a', '#6a7ad0')), 2: ('Crimson Opera', ('#22040a', '#8a1a24', '#e05a64')),
                                                  3: ('Emerald Ascot', ('#04200e', '#1a7a3a', '#6ad08a')), 4: ('Gilded Topper', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Topper', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Topper', ('#141014', '#4a4046', '#9a8c94'))}),
       'wil': ('Wilfrey', '#f4f4f4', 'Heraldry', {1: ('Crimson Cross', ('#3a0408', '#b02020', '#ff7070')), 2: ('Azure Chevron', ('#06103a', '#2a4ab0', '#8aa8ff')),
                                                  3: ('Verdant Bend', ('#06260a', '#2a8a30', '#90e090')), 4: ('Gilded Sun', ('#3a2806', '#e0b030', '#fff0a0')), 5: ('Diamond Sun', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Sun', ('#141014', '#4a4046', '#9a8c94'))})}
HIDDEN = 4
RECOLOUR = {'leo': ('le_tunic', 'le_skirt', 'le_cape'), 'demo': ('dm_hood', 'dm_hood_dk', 'dm_cape'), 'cecil': ('cec_robe', 'cec_robe_dark')}
# (2.79b: with Leo's Golden Champion his helm and armour turn diamond - polished cyan beside the gold tabard - head included)
ARMOUR = {'leo': ('le_steel', 'le_steel_dk', 'le_mail')}
DYE = {'Crimson Crusader': 'red', 'Royal Purple': 'purple', 'Greenwood': 'green', 'Golden Champion': 'yellow', 'Crimson Reaper': 'red', 'Ashen Shroud': 'gray',
       'Royal Violet': 'purple', 'Gilded Storm': 'yellow', 'Crimson': 'red', 'Midnight': 'blue', 'Bone': 'white', 'Gilded': 'yellow', 'Neon': 'magenta',
       'Golden Thunder': 'yellow', 'Obsidian Coil': 'black', 'Blood Wyrm': 'red', 'Frost Serpent': 'light_blue', 'Gilded Coil': 'yellow',
       "Admiral's Blue": 'blue', 'Corsair Crimson': 'red', 'Bleached Bone': 'white', 'Gilded Captain': 'yellow', 'Bluejay': 'light_blue',
       'Ember Toad': 'orange', 'Old Bog': 'brown', 'Golden Prince': 'yellow', 'Chocolate': 'brown', 'Midnight': 'blue', 'Snowdrift': 'white', 'Starlit': 'purple',
       'Ruby': 'red', 'Emerald': 'lime', 'Amethyst': 'purple', 'Gilded': 'yellow', 'Crimson Cross': 'red', 'Azure Chevron': 'blue', 'Verdant Bend': 'green',
       'Gilded Sun': 'yellow', 'Midnight Silk': 'blue', 'Crimson Opera': 'red', 'Emerald Ascot': 'green', 'Gilded Topper': 'yellow',
       'Diamond Champion': 'light_blue', 'Diamond Storm': 'light_blue', 'Diamond': 'light_blue', 'Diamond Coil': 'light_blue', 'Diamond Captain': 'light_blue', 'Diamond Prince': 'light_blue', 'Diamond Topper': 'light_blue', 'Diamond Sun': 'light_blue', 'Diamond Thunder': 'light_blue',
       'Netherite Champion': 'black', 'Netherite Storm': 'black', 'Netherite': 'black', 'Netherite Coil': 'black', 'Netherite Captain': 'black', 'Netherite Prince': 'black', 'Netherite Topper': 'black', 'Netherite Sun': 'black', 'Netherite Thunder': 'black'}
WORD = {'apo': 'his scales', 'tul': 'his coat', 'frog': 'his skin', 'don': 'his coat', 'pearl': 'his bow tie and hat band', 'wil': 'the shield he bears',
        'fishy': 'his top hat'}
for _w, (_who, _col, _word, _set) in NEW.items():
    for _k, (_n, _pal) in _set.items():
        _iid = f'cos_{_w}_{_k}'
        _short = {'frog': 'The Frog'}.get(_w, _who)
        _menu = {'wil': 'Sneak + use his locket while he rests: his wardrobe.', 'pearl': 'Sneak + use his card: his menu - Wardrobe.'}.get(
            _w, 'Sneak + use his own item: his menu - Wardrobe.' if _w in WORD else 'Sneak + use his own item: his menu - change any time.')
        item(_iid, TOTEM, f"{_short}'s {_word}: {_n}", _pal[1] if _pal[1] != '#55555c' else '#9a9aa2',
             [f'{_n} - for {_who} alone.' if _w not in WORD else f'{_n} - {WORD[_w]}, for {_who} alone.',
              ('Use: it\'s his for good - in his wardrobe.', 'blue'), (_menu, 'gray')] +
             ([('Hidden: rare - a Gutter Trophy at Goldtooth.', 'dark_gray')] if _k == HIDDEN else []) +
             ([('With a gem in him, the gem\'s element shows instead.', 'dark_gray')] if _w in ('cecil', 'kw') else []),
             model=f'minecraft:{DYE[_n]}_dye', glint=_k == HIDDEN or None, stack=1, cat='cosmetic', comps=hold('none'))
        HOLD[_iid] = f'bm:p99/use/{_w}{_k}'
# (the old wardrobe items say so too)
for _iid in [i for i in ITEMS if i.startswith(('cos_ribbon_', 'cos_dress_', 'cos_celi_', 'cos_zib_', 'cos_outfit_'))]:
    _L = ITEMS[_iid]['comps']['minecraft:lore']
    _L[:] = [l for l in _L if not (isinstance(l, dict) and l.get('text', '').startswith(('Kept:', 'Sneak + use', 'Use while', 'Use one while')))]
    _L.insert(1, T('Use: unlocked for good - in the wardrobe.', 'blue'))
    _L.insert(2, T('Sneak + use the follower\'s item: the menu.', 'gray'))
BASE = {'emma': 9800, 'celi': 9840, 'zib': 9860, 'cecil': 9880, 'kw': 9900, 'leo': 9920, 'demo': 9940,
        'apo': 9000, 'tul': 9020, 'frog': 9040, 'don': 9060, 'pearl': 9080, 'wil': 9100,         # (2.78: the rest - their own blocks of 20)
        'fishy': 9120}                                                                             # (2.79)
TOP = {'emma': 9839, 'celi': 9859, 'zib': 9879, 'cecil': 9899, 'kw': 9919, 'leo': 9939, 'demo': 9959}   # each follower's last code
TOP.update({w: b + 19 for w, b in BASE.items() if w not in TOP})
COS = {'leo': 'bm.cosl', 'demo': 'bm.cosm', 'cecil': 'bm.cosce', 'kw': 'bm.cosk', 'apo': 'bm.cosap', 'tul': 'bm.costu', 'frog': 'bm.cosfg', 'don': 'bm.cosdn',
       'pearl': 'bm.cospm', 'wil': 'bm.coswl', 'fishy': 'bm.cosfy'}
NAMES = {'emma': ('Emma', '#ff7ad0', 'her'), 'celi': ('Celi', '#9ad8ff', 'her'), 'zib': ('Zib', '#3ad8c8', 'him'), 'cecil': ('Cecil', '#b48cff', 'him'),
         'kw': ('KillerWatt', '#ffe040', 'him'), 'leo': ('Leo', '#5ab8e0', 'him'), 'demo': ('Democratus', '#7ad06a', 'him'),
         'apo': ('Apophiss', '#3ad06a', 'him'), 'tul': ('Tullius', '#7ad8ff', 'him'), 'frog': ('the Frog with Mustache', '#6ac850', 'him'),
         'don': ('Donado', '#e8d29a', 'him'), 'pearl': ('Pearlman', '#5ac8ff', 'him'), 'wil': ('Wilfrey', '#f4f4f4', 'him'), 'fishy': ('Fishy', '#ffa040', 'him')}
HOME = {'emma': 'p98/home/emma', 'celi': 'p98/home/celi', 'zib': 'p98/home/zib', 'cecil': 'p98/home/cecil', 'kw': 'p98/home/killerwatt',
        'leo': 'p98/home/leo', 'demo': 'p98/home/demo', 'apo': 'p98/home/apo', 'tul': 'p98/home/tul', 'frog': 'p138/home/frog', 'don': 'p138/home/don',
        'pearl': 'p138/home/pearl', 'wil': 'p138/home/wil', 'fishy': 'p145/home'}
P28.MENU.update({f'wd_{w}': b for w, b in BASE.items()})


def _recolour(ims, stops):
    """recolour a set of cloth textures together: luminance (over the whole set's range) through dark - mid - light"""
    from gen_rp import hexc
    s = [hexc(c)[:3] for c in stops]
    lum = lambda p: (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255
    vals = [lum(im.getpixel((x, y))) for im in ims.values() for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0]
    lo, hi = min(vals), max(vals)
    out = {}
    for name, im in ims.items():
        o = im.copy()
        for y in range(im.height):
            for x in range(im.width):
                p = im.getpixel((x, y))
                L = (lum(p) - lo) / max(1e-6, hi - lo)
                L = 0.15 + 0.75 * L
                c = tuple(int(s[0][i] + (s[1][i] - s[0][i]) * L / 0.5) for i in range(3)) if L < 0.5 else \
                    tuple(int(s[1][i] + (s[2][i] - s[1][i]) * (L - 0.5) / 0.5) for i in range(3))
                o.putpixel((x, y), c + (p[3],))
        out[name] = o
    return out


def textures():
    import phase96_art as LA, phase97_art as DA, phase45
    base = {'leo': LA.textures(), 'demo': DA.textures(), 'cecil': phase45.textures()}
    out = {}
    import gild
    for w, keys in RECOLOUR.items():
        for k, (_n, pal) in NEW[w][3].items():
            ims = {n: gild.dress(w, k, base[w][n]) for n in keys} if gild.is_gilded(w, k) else _recolour({n: base[w][n] for n in keys}, pal)   # (2.79a: polished gold)
            for name, im in ims.items():
                out[f'{name}_c{k}'] = im
            if gild.is_gilded(w, k):
                for n in ARMOUR.get(w, ()):
                    im = gild.metal(base[w][n], ramp=gild.steel(w, k), sheen=0 if n == 'le_mail' else 11, soften=n != 'le_mail')
                    if n.endswith('_dk'):                # (the dark steel stays darker: its trim and shadowed plates)
                        from PIL import Image
                        im = Image.merge('RGBA', [*[c.point(lambda v: int(v * 0.68)) for c in im.split()[:3]], im.split()[3]])
                    out[f'{n}_c{k}'] = im
    return out


def rp(R):
    import sys
    import phase97_art as DA
    R.TEXTURE_MODS.append(sys.modules[__name__])
    sel_items = {}                                   # a model whose part keeps its custom_model_data: the outfit picked by it
    import gild
    def worn(w, k):                                  # (the textures a look recolours: its cloth - and, the gilded look, Leo's steel)
        return RECOLOUR[w] + (ARMOUR.get(w, ()) if gild.is_gilded(w, k) else ())
    def swap(tex, w, k):
        return {a: (f'{v}_c{k}' if any(v == f'bm:block/{t}' for t in worn(w, k)) else v) for a, v in tex.items()}
    for w, prefix in (('leo', 'le_'), ('demo', 'dm_')):
        for name in [n for n in list(R.HATS) if n.startswith(prefix) and '_x' not in n and not n.startswith(prefix + 'head') and not n[len(prefix):].startswith('scythe')]:
            tex, els = R.HATS[name]
            ks = [k for k in NEW[w][3] if any(v == f'bm:block/{t}' for v in tex.values() for t in worn(w, k))]
            if not ks:
                continue
            sel_items[name] = []
            for k in ks:
                R.HATS[f'{name}_c{k}'] = (swap(tex, w, k), els)
                sel_items[name].append((f'c{k}', f'{name}_c{k}'))
        assert not any(v == f'bm:block/{t}' for v in R.HATS[f'{prefix}head'][0].values() for t in RECOLOUR[w]) or w == 'demo', w
    # Democratus' hood: a head model per cloak (his face and glowing eyes picked on it as on the plain one)
    heads = {}
    tex, els = R.HATS['dm_head']
    for k in NEW['demo'][3]:
        R.HATS[f'dm_head_c{k}'] = (swap(tex, 'demo', k), els)
        heads[f'dm_head_c{k}'] = []
        for e in DA.DEMO_EXPR:
            R.HATS[f'dm_head_c{k}_x{e}'] = (dict(swap(tex, 'demo', k), dm_face=f'bm:block/dm_face_{e}', dm_glow=f'bm:block/dm_glow_{e}'), els)
            heads[f'dm_head_c{k}'].append((e, f'dm_head_c{k}_x{e}'))
    # Cecil's own robe (worn when no gem is in him)
    for nm in ('head', 'arm', 'body', 'larm'):
        tex, els = R.HATS[f'cec2_{nm}']
        for k in NEW['cecil'][3]:
            R.HATS[f'cec2_{nm}_c{k}'] = (swap(tex, 'cecil', k), els)
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for name, cases in sel_items.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': c, 'model': mdl(m)} for c, m in cases], 'fallback': mdl(name)}})
        for name, cases in heads.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl(name)}})
        # (2.79b) Leo's head in his gilded look: his helm in diamond, every face of his on it (his face picks itself as on the plain head)
        import json, os
        for k in [k for k in NEW['leo'][3] if gild.is_gilded('leo', k)]:
            idef = json.load(open(R2.p('assets', 'bm', 'items', 'le_head.json')))['model']
            for m in ['le_head'] + [c['model']['model'].split('/')[-1] for c in idef.get('cases', [])]:
                src = json.load(open(R2.p('assets', 'bm', 'models', 'item', m + '.json')))
                src['textures'] = {a: (f'{v}_c{k}' if any(v == f'bm:block/{t}' for t in ARMOUR['leo']) else v) for a, v in src['textures'].items()}
                R2.wj(f'assets/bm/models/item/{m.replace("le_head", f"le_head_c{k}", 1)}.json', src)
            idef = json.loads(json.dumps(idef).replace('bm:item/le_head', f'bm:item/le_head_c{k}'))
            R2.wj(f'assets/bm/items/le_head_c{k}.json', {'model': idef})
    R.POST.append(post)


def groups():
    """(follower, group, current-look score, unlocked bits, {k: (name, colour)}, item, menu offset, apply (as you)) - also the Tailor's (phase103)"""
    return [('emma', 'ribbon', 'bm.cosr', 'bm.wur', {k: (n, c) for k, (n, c) in P78.RIBBONS.items()}, 'cos_ribbon_{}', 2, 'p78/emma_now'),
              ('emma', 'dress', 'bm.cosd', 'bm.wud', {k: (n, c) for k, (n, c, _c2) in P78.DRESSES.items()}, 'cos_dress_{}', 12, 'p78/emma_now'),
              ('emma', 'outfit', 'bm.coso', 'bm.wuo', dict(P89.OUTFITS), 'cos_outfit_{}', 22, 'p78/emma_now'),
              ('celi', 'celi', 'bm.cosc', 'bm.wuc', {k: (n, c) for k, (n, c, _c2) in P78.CELI.items()}, 'cos_celi_{}', 2, 'p78/celi_now'),
              ('zib', 'zib', 'bm.cosz', 'bm.wuz', dict(P78.ZIB), 'cos_zib_{}', 2, 'p78/zib_now')] + \
             [(w, w, COS[w], f'bm.wu{w}',
               {k: (n, pal[1]) for k, (n, pal) in NEW[w][3].items()}, f'cos_{w}_{{}}', 2, f'p99/{w}_now') for w in NEW]


def generate(G):
    import gild
    import phase57 as P57
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = PREFIX
    PINK = P78.PINK
    # groups: (follower, group, current-look score, unlocked bits, {k: (name, colour)}, item, menu offset, apply (as you))
    GROUPS = groups()
    objs = sorted({g[2] for g in GROUPS} | {g[3] for g in GROUPS})
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += [o for o in objs if o not in G.OBJECTIVES]
    def bit(obj, k):
        return [f'scoreboard players operation #q bm.rng = @s {obj}', f'scoreboard players set #bit bm.rng {2 ** k}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']

    # ================================================================== unlocking: a cosmetic used once is in the wardrobe for good
    for who, g, cur, un, ks, iid, off, apply in GROUPS:
        for k in ks:
            fn(f'p99/unlock/{g}{k}', [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0'] + bit(un, k) +
               ['execute if score #q bm.rng matches 1 run return 0', f'scoreboard players add @s {un} {2 ** k}',
                f'clear @s *[minecraft:custom_data~{{bm:"{iid.format(k)}"}}] 1', 'playsound minecraft:item.armor.equip_leather player @s ~ ~ ~ 1 1.2',
                tellraw('@s', P + [T(ks[k][0], ks[k][1], bold=True), T(f' is in {NAMES[who][0]}\'s wardrobe for good. ', 'gray'),
                                   T(f'(Sneak + use {NAMES[who][2]} item to change any time.)', 'dark_gray')])])
    old_use = {'ribbon': 'p78/use/ribbon{}', 'dress': 'p78/use/dress{}', 'outfit': 'p89/use/outfit{}', 'celi': 'p78/use/celi{}', 'zib': 'p78/use/zib{}'}
    for who, g, cur, un, ks, iid, off, apply in GROUPS:
        for k in ks:
            if g in old_use:
                L = G.FUNCS[old_use[g].format(k)]
                j = next(n for n, l in enumerate(L) if l.startswith('scoreboard players set @s bm.gvhc'))
                L.insert(j + 1, f'function bm:p99/unlock/{g}{k}')
            else:
                fn(f'p99/use/{g}{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                       'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'function bm:p99/unlock/{g}{k}',
                                       f'scoreboard players set @s {cur} {k}', f'function bm:{apply}'])

    # ================================================================== putting it on (as you)
    # Leo and Democratus: every part but the head picks its outfit by custom_model_data; Democratus' hood by its model
    for w, sel, part, head in (('leo', 'bm.lesel', 'bm.lep', 'bm.lp_head'), ('demo', 'bm.dmsel', 'bm.dmp', 'bm.dp_head')):
        cur = next(g[2] for g in GROUPS if g[0] == w)
        fn(f'p99/{w}_dress', ['scoreboard players set #wc bm.rng 0',
                              f'execute store result score #wp bm.rng run scoreboard players get @e[type=minecraft:item_display,tag={sel},limit=1] bm.pid',
                              f'execute as @a if score @s bm.pid = #wp bm.rng run scoreboard players operation #wc bm.rng = @s {cur}',
                              f'execute if score #wc bm.rng matches 0 as @e[type=minecraft:item_display,tag={sel}{",tag=!" + head if head else ""}] run data remove entity @s item.components."minecraft:custom_model_data"'] +
           [f'execute if score #wc bm.rng matches {k} as @e[type=minecraft:item_display,tag={sel}{",tag=!" + head if head else ""}] run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["c{k}"]}}'
            for k in NEW[w][3]] +
           ([f'execute if score #wc bm.rng matches 0 run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:dm_head"'] +
            [f'execute if score #wc bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:dm_head_c{k}"'
             for k in NEW[w][3]] if w == 'demo' else
            # (Leo's head: his face stays his own - but in the gilded look his helm is diamond)
            [f'data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:le_head"'] +
            [f'execute if score #wc bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:le_head_c{k}"'
             for k in NEW['leo'][3] if gild.is_gilded('leo', k)]))
        G.FUNCS[f'p{96 if w == "leo" else 97}/grow'].append(f'function bm:p99/{w}_dress')
        excl = ',tag=!bm.dmencp,tag=!bm.dmbp,tag=!bm.dmfade' if w == 'demo' else ',tag=!bm.lefade,tag=!bm.leencp'
        fn(f'p99/{w}_now', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as @e[type=minecraft:item_display,tag={part}{excl}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                            f'execute unless entity @e[tag={sel}] run return run ' + say(f'{NAMES[w][0]} isn\'t with you - he\'ll wear it next time.', NAMES[w][1]),
                            f'function bm:p99/{w}_dress', f'execute at @e[type=minecraft:item_display,tag={sel},limit=1] run particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.02 14',
                            f'tag @e[tag={sel}] remove {sel}'])
    # Cecil: his own robe (no gem in him)
    cur_c = next(g[2] for g in GROUPS if g[0] == 'cecil')
    G.FUNCS['p46/pet/dress'] += ['scoreboard players set #wc bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wc bm.rng = @s {cur_c}'] + \
        [f'execute if score #el bm.rng matches 0 if score #wc bm.rng matches {k} as @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_{nm}] if score @s bm.pid = #me bm.pid '
         f'run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_{nm}_c{k}"' for k in NEW['cecil'][3] for nm in ('head', 'arm', 'body', 'larm')]
    fn('p99/cecil_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute unless score @s bm.cpel matches 0.. run scoreboard players set @s bm.cpel 0',
                         'scoreboard players operation #el bm.rng = @s bm.cpel', 'function bm:p46/pet/dress',
                         'execute if score @s bm.cpel matches 1.. run ' + say('With a gem in him Cecil wears its colours - he\'ll wear his robe when it\'s out.', '#b48cff')])
    # KillerWatt: his own colours (no gem in him) - #kcos beside #kel, wherever his parts are dressed
    cur_k = next(g[2] for g in GROUPS if g[0] == 'kw')
    SUFS = [('armr', '_flex'), ('arml', '_flex')]
    for f_, parts in (('p79/pet/dress_rig', [(p, '') for p in KA.PARTS]), ('p79/flex', SUFS), ('p79/unflex', [('armr', ''), ('arml', '')])):
        L = G.FUNCS[f_]
        L += [f'execute if score #kel bm.rng matches 0 if score #kcos bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] '
              f'item.components."minecraft:item_model" set value "bm:kw_{p}{s}_c{k}"' for k in NEW['kw'][3] for p, s in parts]
    G.FUNCS['p79/pet/dress_rig'].insert(0, f'scoreboard players set #kcos bm.rng 0')
    G.FUNCS['p79/pet/dress_rig'].insert(1, f'execute on owner run scoreboard players operation #kcos bm.rng = @s {cur_k}')
    G.FUNCS['p79/pet/tick'][0:0] = ['scoreboard players set #kcos bm.rng 0', f'execute on owner run scoreboard players operation #kcos bm.rng = @s {cur_k}']
    G.FUNCS['p79/boss/tick'].insert(0, 'scoreboard players set #kcos bm.rng 0')
    G.FUNCS['p79/orphan'].insert(0, 'scoreboard players set #kcos bm.rng 0')
    fn('p99/kw_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid at @s run function bm:p99/kw_now2',
                      'execute if score #has bm.rng matches 0 run return run ' + say('KillerWatt isn\'t with you - he\'ll wear it next time.', '#ffe040'),
                      'execute if score @s bm.kxel matches 1.. run ' + say('With a gem in him KillerWatt shows its element - his colours come back when it\'s out.', '#ffe040')])
    fn('p99/kw_now2', ['scoreboard players set #has bm.rng 1', 'function bm:p79/pet/redress', 'particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 30'])

    # ================================================================== the menus (sneak + use the follower's item)
    for who in BASE:
        b = BASE[who]
        nm, col, pron = NAMES[who]
        mine = [g for g in GROUPS if g[0] == who]
        page = [f'scoreboard players set @s bm.menu {b}', 'data remove storage bm:ui wd']
        st = lambda key, txt, c: f'data modify storage bm:ui wd.r_{key} set value {snbt(T(txt, c, bold=True))}'
        btns = [P28.btn([T(f'Send {pron} home', 'gray')], b, width=150)]
        for _w, g, cur, un, ks, iid, off, apply in mine:
            page += [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0', f'execute unless score @s {cur} matches 0.. run scoreboard players set @s {cur} 0']
            for k in ks:              # (one already worn - from before the wardrobe - counts as owned)
                page += [f'execute if score @s {cur} matches {k} run function bm:p99/own/{g}{k}']
                fn(f'p99/own/{g}{k}', bit(un, k) + [f'execute if score #q bm.rng matches 0 run scoreboard players add @s {un} {2 ** k}'])
            orig = {'ribbon': 'Pink ribbon', 'dress': 'Her own dress', 'outfit': None}.get(g, 'Own clothes' if who not in ('cecil', 'kw') else 'Own colours')
            orig = {'apo': 'His own scales', 'tul': 'His old coat', 'frog': 'His own skin', 'don': 'His own coat', 'pearl': 'The blue bow tie',
                    'wil': 'No shield', 'fishy': 'His old black topper'}.get(g, orig)
            if orig:
                page += [st(f'{g}0', 'owned', 'gray'), f'execute if score @s {cur} matches 0 run {st(f"{g}0", "wearing", GOLD)}']
                if g == 'dress':
                    page += [f'execute unless score @s bm.coso matches 0 run {st(f"{g}0", "owned", "gray")}']
                btns.append(P28.btn([T(orig, 'white', bold=True), T('  '), f'@@RAW:r_{g}0@@'], b + off, width=150))
            for k, (cn, cc) in ks.items():
                page += [st(f'{g}{k}', 'locked', 'dark_gray')] + bit(un, k) + [f'execute if score #q bm.rng matches 1 run {st(f"{g}{k}", "owned", "gray")}',
                                                                               f'execute if score @s {cur} matches {k} run {st(f"{g}{k}", "wearing", GOLD)}']
                if g == 'dress':
                    page += [f'execute if score @s {cur} matches {k} unless score @s bm.coso matches 0 run {st(f"{g}{k}", "owned", "gray")}']
                btns.append(P28.btn([T(cn, cc, bold=True), T('  '), f'@@RAW:r_{g}{k}@@'], b + off + k, width=150))
        # 2.78: the aura row - locked until you have it (a rare heist find, or dear at the Tailor), then on / off
        import phase138 as P138
        an, ac = P138.AURA[who][0], P138.AURA[who][1]
        page += [st('aura', 'locked', 'dark_gray'), f'execute if entity @s[tag=bm.auown_{who}] run {st("aura", "off", "gray")}',
                 f'execute if entity @s[tag=bm.au_{who}] run {st("aura", "on", GOLD)}']
        used = {b} | {b + off + k for _w, g, cur, un, ks, iid, off, apply in mine for k in [0] + list(ks)}
        assert TOP[who] not in used, (who, TOP[who])
        btns.append(P28.btn([T(an, ac, bold=True), T('  '), '@@RAW:r_aura@@'], TOP[who], width=150,
                            tooltip=T(f'{an}: a rare aura around {nm} - a heist find, or the Tailor\'s dearest stock. On or off here.', 'gray')))
        page.append(f'function bm:p99/dlg/{who} with storage bm:ui wd')
        fn(f'p99/menu/{who}', page)
        dlg = P28.multi([T(f"{nm}", col, bold=True), T('  ·  wardrobe', 'gray')],
                        [P28.body([T('Every outfit you\'ve used is ' + pron + 's for good. Pick one any time - ', 'gray'),
                                   T('locked', 'dark_gray', bold=True), T(' ones are sold by Goldtooth in the vault (the hidden ones for a Gutter Trophy).', 'gray')] +
                                  ([T(' With a gem in him, the gem\'s element shows instead.', 'dark_gray')] if who in ('cecil', 'kw') else []), 330)],
                        btns, columns=3 if who == 'emma' else 2, exit_label='Close')
        fn(f'p99/dlg/{who}', [f'$dialog show @s {P28.inline(dlg)}'])
        # the clicks
        lines = [f'execute unless score @s bm.menu matches {b} run return run function bm:p28/stale',
                 'scoreboard players operation #me bm.pid = @s bm.pid',
                 f'execute if score #act bm.pay matches {b} run return run function bm:{HOME[who]}',
                 f'execute if score #act bm.pay matches {TOP[who]} run return run function bm:p138/au/t_{who}']
        for _w, g, cur, un, ks, iid, off, apply in mine:
            if g != 'outfit':
                fn(f'p99/pick/{g}0', [f'scoreboard players set @s {cur} 0'] + (['scoreboard players set @s bm.coso 0'] if g == 'dress' else []) +
                   [f'function bm:{apply}', f'function bm:p99/menu/{who}'])
                lines.append(f'execute if score #act bm.pay matches {b + off} run return run function bm:p99/pick/{g}0')
            for k, (cn, cc) in ks.items():
                fn(f'p99/pick/{g}{k}', bit(un, k) + [f'execute if score #q bm.rng matches 0 run return run ' +
                                                     say(f'{cn} is locked - Goldtooth sells it in the vault' + (' (hidden: a Gutter Trophy).' if iid.format(k) in P78.HIDDEN or (who in NEW and k == HIDDEN) else '.'), cc)] +
                   [f'scoreboard players set @s {cur} {k}'] + (['scoreboard players set @s bm.coso 0'] if g == 'dress' else []) +
                   [f'function bm:{apply}', f'function bm:p99/menu/{who}'])
                lines.append(f'execute if score #act bm.pay matches {b + off + k} run return run function bm:p99/pick/{g}{k}')
        fn(f'p99/act/{who}', lines)
    # (2.78: each follower's own block, routed exactly - the new ones sit at 9000-9119, away from the old run)
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {b}..{TOP[w]} run return run function bm:p99/act/{w}' for w, b in BASE.items()]
    # sneak + use: the menu (KillerWatt: not while riding him - that's his Thunder Leap)
    sneak = lambda who: f'execute if predicate bm:p20/sneaking run return run function bm:p99/menu/{who}'
    for f_, who in (('p46/pet/use', 'cecil'), ('p66/use', 'celi'), ('p72/zb/use', 'zib'), ('p96/use', 'leo')):
        L = G.FUNCS[f_]
        j = next(n for n, l in enumerate(L) if l == 'scoreboard players operation #me bm.pid = @s bm.pid')
        L.insert(j + 1, sneak(who))
    L = G.FUNCS['p79/spark']
    j = next(n for n, l in enumerate(L) if 'p79/pet/rleap' in l)
    L.insert(j + 1, sneak('kw'))
    L = G.FUNCS['p57/use']                     # Emma: out - her buff menu (its Wardrobe button); not out - her wardrobe
    j = next(n for n, l in enumerate(L) if 'unless entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking' in l)
    L[j] = 'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking run function bm:p99/menu/emma'
    G.FUNCS['p57/act'].insert(2, 'execute if score #act bm.pay matches 7306 run return run function bm:p99/menu/emma')

    # ================================================================== Goldtooth sells the new ones (Gutter Medallions; the hidden ones a Gutter Trophy)
    import phase70 as P70
    from gen_dp import offer
    prev = P70.goldtooth
    def g99():
        d = prev()
        for w in NEW:
            for k in NEW[w][3]:
                d['Offers']['Recipes'].append(offer(gild.price(f'cos_{w}_{k}', ('gutter_trophy', 1) if k == HIDDEN else ('gutter_medallion', 4)), (f'cos_{w}_{k}', 1)))
        return d
    P70.goldtooth = g99
    L = G.FUNCS['p70/r/lobby/init']
    L[:] = [l.replace(snbt(prev()), snbt(g99())) if 'bm.gvgt' in l and 'summon minecraft:villager' in l else l for l in L]
    assert any(snbt(g99()) in l for l in L), "Goldtooth's summon wasn't found to add the wardrobe"
    fn('admin/wardrobe_all', [f'scoreboard players set @s {g[3]} {sum(2 ** k for k in g[4])}' for g in GROUPS] +
       [tellraw('@s', P + [T('Every follower outfit unlocked.', 'gray')])])
    fn('admin/wardrobe_items', [give(f'cos_{w}_{k}') for w in NEW for k in NEW[w][3]])
