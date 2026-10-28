"""2.92: QUEEN AVA'S HONOURS - the follower upgrades, moved from Vesper's Ledger to the Underwater Kingdom.

Bring QUEEN AVA (your follower) to the TIDE FONT in the throne room, with the followers you want honoured beside you, and
right-click the Font: after the royal family's own business, Ava opens her HONOURS - a page for each follower with you
(up to three: Ava herself can be honoured too).
  THE ROYAL BLESSING   the first time a follower stands before Ava at the Font, she blesses them: Vitality I, free.
  (2.94) ONE HONOUR, THREE RANKS - each raises all three below together, to II, IV and then V (the same height as before):
                       I: 8 Royal Pearls and a tribute · II: 16 + 1 Dread Token and a rarer one · III: 28 + 3, their signature
                       treasure and any one Elemental Gem (Water, Rock or Fire). The old per-honour ranks below are what it sets.
  VITALITY I-V         +20% health a level (V: twice their health)
  BULWARK I-V          +3 armour and +1 toughness a level
  MIGHT I-V            +15% damage a level - their own blows and every special attack they make (the build pass below
                       scales the pack's own follower damage commands by the attacker's Might)
  PRICE                level 1: 6 Royal Pearls · 2: 10 + 1 Dread Token · 3: 16 + 2 · 4: 24 + 3 · 5: 32 + 5 and the honour's
                       own ELEMENTAL GEM - the gems are pieces of the kingdom's broken heart: Vitality V the Water Gem,
                       Bulwark V the Rock Gem, Might V the Fire Gem (Dread Tokens from your pockets first, then the Rat Bank)
  THE TIDE'S HASTE     (on Ava's first page; every follower you call) Swift Return I-II: a faint rests 80 s, then 45 s,
                       not 2 minutes. I: 12 Royal Pearls + 3 Dread Tokens; II: 24 + 5 and the Air Gem.
THE HEART COMES HOME   carry the ETHEREAL GEM (the nine gems made whole - the kingdom's lost heart) to the Font with the royal
                       family (Emma, Queen Ava, Queen Pearl): the Font takes its light for a moment, and gives it back.
                       Once each: the BLESSING OF THE HEART (+2 hearts, for good), the kingdom's dome is WARDED (a breach
                       never shatters it again), 2 Heartstones and 24 Royal Pearls.
THE SERPENT'S RESTRAINT  carry the Ethereal Gem to the Font with APOPHISS: the gem he killed a queen for, an arm's length
                       away. He doesn't take it. Once each: Apophiss gains a rank of every honour (gems not needed), and you
                       2 Heartstones and 16 Royal Pearls.
Each follower's honours are yours and theirs for good: they carry them everywhere you call them - at home, on a heist, in
every form (Wraithfire and the gem forms stack on top). Ava only walks with you in hard mode, so the honours are hard mode's.
Vesper's Ward and Vigor are retired: every Dread Token spent on them is handed back the next time you're online. (His
Swift Return stays with him.)"""
from items import T, ITEMS
from nbt import snbt, Int
import re

AVA_C, PEARL_C, GOLD = '#6ad8e8', '#d8f4ff', '#ffd66a'
MENU = 4100                                 # (its block: 4100-4199)
STATS = [('v', 'Vitality', '#ff8a9a', '+20% health a level'), ('b', 'Bulwark', '#9ad0ff', '+3 armour, +1 toughness a level'),
         ('m', 'Might', '#ffb05a', '+15% damage a level - special attacks too')]
UNIT = {'v': 1, 'b': 10, 'm': 100}          # a follower's honours in one score: v + 10 b + 100 m + 1000 (blessed)
PEARLS = [6, 10, 16, 24, 32]
DREAD = [0, 1, 2, 3, 5]
# (2.94) ONE HONOUR, THREE RANKS - each rank raises all three at once (to II, IV, then V: the same height as before), far less
# grind: (pearls, Dread Tokens, which of the follower's tributes, an Elemental Gem?)
RANKS = [(2, 8, 0, 0, False), (4, 16, 1, 2, False), (5, 28, 3, 4, True)]   # (to level, pearls, Dread Tokens, tribute index, gem)
GEMS_ANY = ('water', 'rock', 'fire')
GEM = {'v': ('water', 'Water Gem'), 'b': ('rock', 'Rock Gem'), 'm': ('fire', 'Fire Gem')}
HASTE = [(80, 12, 3, None), (45, 24, 5, ('air', 'Air Gem'))]     # Swift Return: (faint seconds, pearls, Dread Tokens, gem)
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
WARD = [3, 4, 5]                            # (Vesper's retired Ward and Vigor: Dread Tokens a level - handed back, see the refund)
# 2.93: each follower's TRIBUTE - what Ava asks for each rank, on top of the pearls: things that are that follower's own
# (rank 1 common, 2 uncommon, 3 a find, 4 a rare one, 5 their signature treasure - and the honour's Elemental Gem).
# 'minecraft:...' is a plain vanilla item (never one of the pack's look-alikes); '#...' an item tag; anything else the pack's.
TRIB = {
    'emma': [('minecraft:pink_petals', 16), ('minecraft:prismarine_crystals', 8), ('minecraft:nautilus_shell', 2), ('minecraft:heart_of_the_sea', 1), ('tide_scale', 8)],
    'celi': [('minecraft:snowball', 32), ('minecraft:packed_ice', 16), ('minecraft:blue_ice', 8), ('minecraft:goat_horn', 1), ('heartstone', 2)],
    'zib': [('minecraft:glowstone_dust', 16), ('xenite_green', 4), ('xenite_cyan', 4), ('xenite_red', 2), ('gravitic_core', 1)],
    'cecil': [('minecraft:lapis_lazuli', 16), ('minecraft:amethyst_shard', 16), ('minecraft:experience_bottle', 8), ('minecraft:ender_eye', 4), ('heartstone', 2)],
    'kw': [('minecraft:redstone', 32), ('minecraft:copper_ingot', 16), ('minecraft:lightning_rod', 4), ('blood_crystal', 8), ('heartstone', 2)],
    'leo': [('minecraft:iron_ingot', 16), ('minecraft:prismarine_shard', 16), ('minecraft:nautilus_shell', 2), ('tide_scale', 6), ('minecraft:heart_of_the_sea', 1)],
    'demo': [('minecraft:wheat', 32), ('minecraft:phantom_membrane', 4), ('minecraft:lightning_rod', 4), ('blood_crystal', 8), ('heartstone', 2)],
    'apo': [('minecraft:bone', 32), ('minecraft:wither_rose', 4), ('dread_essence', 4), ('minecraft:wither_skeleton_skull', 1), ('heartstone', 2)],
    'tul': [('minecraft:ice', 16), ('minecraft:gunpowder', 16), ('minecraft:ghast_tear', 2), ('tide_scale', 6), ('minecraft:heart_of_the_sea', 1)],
    'frog': [('minecraft:slime_ball', 16), ('minecraft:lily_pad', 16), ('minecraft:verdant_froglight', 4), ('minecraft:pearlescent_froglight', 2), ('heartstone', 2)],
    'don': [('minecraft:gold_ingot', 8), ('xenite_green', 4), ('xenite_violet', 2), ('xenite_red', 2), ('gravitic_core', 1)],
    'wil': [('minecraft:bone', 32), ('minecraft:soul_sand', 16), ('minecraft:wither_rose', 2), ('minecraft:wither_skeleton_skull', 1), ('heartstone', 2)],
    'fishy': [('minecraft:tropical_fish', 8), ('minecraft:sea_pickle', 8), ('minecraft:prismarine_crystals', 8), ('minecraft:nautilus_shell', 2), ('heartstone', 2)],
    'dennis': [('minecraft:raw_iron', 16), ('minecraft:gold_ingot', 16), ('minecraft:diamond', 4), ('minecraft:netherite_scrap', 2), ('heartstone', 2)],
    'pistachio': [('minecraft:rotten_flesh', 32), ('minecraft:string', 16), ('minecraft:phantom_membrane', 4), ('minecraft:ghast_tear', 2), ('dread_essence', 6)],
    'omega': [('minecraft:bone_block', 8), ('minecraft:soul_sand', 16), ('minecraft:wither_rose', 4), ('minecraft:wither_skeleton_skull', 1), ('dread_essence', 6)],
    'ashur': [('minecraft:blaze_powder', 16), ('minecraft:magma_cream', 8), ('minecraft:blaze_rod', 8), ('ember_scale', 6), ('heartstone', 2)],
    'chef': [('minecraft:cooked_beef', 16), ('minecraft:cake', 2), ('minecraft:golden_carrot', 16), ('minecraft:golden_apple', 2), ('heartstone', 2)],
    'neighbor': [('minecraft:note_block', 8), ('minecraft:amethyst_shard', 16), ('minecraft:jukebox', 1), ('#minecraft:creeper_drop_music_discs', 1), ('heartstone', 2)],
    'ava': [('minecraft:prismarine_shard', 16), ('minecraft:sea_lantern', 8), ('minecraft:nautilus_shell', 2), ('minecraft:heart_of_the_sea', 1), ('tide_scale', 8)],
    'pearlq': [('minecraft:prismarine_crystals', 16), ('minecraft:gold_ingot', 16), ('minecraft:nautilus_shell', 2), ('minecraft:heart_of_the_sea', 1), ('tide_scale', 8)],
    'bloo': [('minecraft:sweet_berries', 32), ('minecraft:rabbit_hide', 8), ('minecraft:rabbit_foot', 2), ('blood_crystal', 8), ('heartstone', 2)],
    'stalker': [('minecraft:spider_eye', 16), ('minecraft:fermented_spider_eye', 8), ('minecraft:echo_shard', 2), ('minecraft:sculk_catalyst', 1), ('dread_essence', 8)],
    'lantern': [('minecraft:pumpkin', 16), ('minecraft:jack_o_lantern', 8), ('minecraft:blaze_rod', 4), ('blood_crystal', 8), ('ember_scale', 6)],
    'bender': [('minecraft:bone', 16), ('minecraft:cooked_beef', 16), ('token', 8), ('heartstone', 1), ('fallen_star', 2)],
    'bones': [('minecraft:cod', 16), ('minecraft:salmon', 16), ('minecraft:tropical_fish', 8), ('minecraft:nautilus_shell', 2), ('tide_scale', 8)],
    'gem': [('minecraft:amethyst_shard', 32), ('minecraft:emerald', 16), ('minecraft:prismarine_crystals', 16), ('minecraft:echo_shard', 2), ('heartstone', 2)],
    'batty': [('minecraft:spider_eye', 16), ('minecraft:phantom_membrane', 8), ('minecraft:glow_berries', 16), ('token', 4), ('heartstone', 2)],
    'eggbert': [('minecraft:egg', 16), ('minecraft:slime_ball', 16), ('minecraft:ink_sac', 16), ('minecraft:turtle_egg', 2), ('heartstone', 2)],
    'count': [('minecraft:gold_ingot', 16), ('minecraft:slime_ball', 32), ('minecraft:black_wool', 8), ('token', 6), ('heartstone', 2)],
    'dragon': [('minecraft:paper', 32), ('minecraft:red_dye', 16), ('minecraft:green_dye', 16), ('minecraft:blaze_powder', 8), ('heartstone', 2)],
    'eraser': [('minecraft:paper', 32), ('minecraft:pink_wool', 16), ('minecraft:slime_ball', 16), ('minecraft:book', 4), ('heartstone', 2)],
    'cursor': [('minecraft:redstone', 32), ('minecraft:repeater', 8), ('minecraft:comparator', 4), ('minecraft:observer', 4), ('heartstone', 2)],
    'inkblot': [('minecraft:ink_sac', 32), ('minecraft:glow_ink_sac', 16), ('minecraft:feather', 16), ('minecraft:writable_book', 2), ('heartstone', 2)],
    'speech': [('minecraft:paper', 32), ('minecraft:book', 16), ('minecraft:writable_book', 4), ('minecraft:goat_horn', 1), ('heartstone', 2)],
    'lightbringer': [('minecraft:gold_ingot', 32), ('minecraft:glowstone_dust', 32), ('minecraft:golden_apple', 4), ('minecraft:totem_of_undying', 1), ('heartstone', 4)],
    'dryad': [('minecraft:red_mushroom', 32), ('minecraft:brown_mushroom', 32), ('minecraft:pale_moss_block', 16), ('minecraft:glow_berries', 16), ('heartstone', 2)],
    'henry': [('minecraft:cod', 32), ('minecraft:salmon', 32), ('minecraft:string', 32), ('minecraft:feather', 16), ('heartstone', 2)],
    'nia': [('minecraft:salmon', 32), ('minecraft:tropical_fish', 16), ('minecraft:string', 32), ('minecraft:white_wool', 16), ('heartstone', 2)],
    'rufus': [('token', 8), ('minecraft:gold_ingot', 16), ('minecraft:arrow', 64), ('minecraft:crossbow', 2), ('heartstone', 2)],
    'kettle': [('minecraft:paper', 32), ('minecraft:slime_ball', 16), ('minecraft:string', 16), ('minecraft:feather', 16), ('heartstone', 2)],
    'capshun': [('minecraft:paper', 32), ('minecraft:ink_sac', 16), ('minecraft:book', 8), ('minecraft:writable_book', 2), ('heartstone', 2)],
    'pxcecil': [('minecraft:amethyst_shard', 32), ('minecraft:ender_pearl', 8), ('minecraft:experience_bottle', 8), ('minecraft:echo_shard', 2), ('heartstone', 2)],
    'pxleo': [('minecraft:iron_sword', 4), ('minecraft:shield', 2), ('minecraft:emerald', 16), ('minecraft:diamond_sword', 1), ('heartstone', 2)],
    'pxemma': [('minecraft:fire_charge', 16), ('minecraft:red_mushroom', 16), ('minecraft:gold_block', 2), ('minecraft:totem_of_undying', 1), ('heartstone', 2)],
    'sky': [('minecraft:sunflower', 16), ('minecraft:glow_berries', 16), ('minecraft:daylight_detector', 4), ('fallen_star', 2), ('heartstone', 2)],
}


def trib_pred(iid):
    """the item predicate a tribute is counted and taken by (vanilla: a plain one, never the pack's look-alikes)"""
    return holds(iid) if not iid.startswith(('minecraft:', '#')) else f'{iid}[!minecraft:custom_data]'


def trib_name(iid, n):
    if iid.startswith('#'): return f'{n} music disc' + ('s' if n > 1 else '')
    if iid.startswith('minecraft:'): return f'{n} ' + iid[10:].replace('_', ' ')
    return f'{n} ' + str(ITEMS[iid]['name'])


def generate(G):
    import phase28 as P28
    import phase173 as P173
    from phase125 import WHO
    fn, title, tellraw, give, P = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second = G.FUNCS['loop/second']
    FOL = [w for w in P173.AR if w in WHO]
    IDX = {w: i + 1 for i, w in enumerate(FOL)}
    obj = lambda w: f'bm.hn_{w}'
    objs = [obj(w) for w in FOL] + ['bm.hnsel', 'bm.hns0', 'bm.hns1', 'bm.hns2', 'bm.hnap', 'bm.kua', 'bm.fret', 'bm.fward', 'bm.fvig']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (10, 100, 1000)]
    G.OBJECTIVES += objs

    # ---------------------------------------------------------------- at the Font, with Ava: her honours
    G.FUNCS['p199/font/ask'].append('execute if score #r_ava bm.rng matches 1 run function bm:p201/open')
    # (2.94) walk up to the Font with Ava and she says what it's for (once a minute at most)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.khint dummy']; G.OBJECTIVES.append('bm.khint')
    G.FUNCS['loop/second'][-1:-1] = ['scoreboard players remove @a[scores={bm.khint=1..}] bm.khint 1',
                                     'execute as @e[type=minecraft:interaction,tag=bm.kfont] at @s as @a[distance=..6,gamemode=!spectator] unless score @s bm.khint matches 1.. at @s run function bm:p201/hint']
    fn('p201/hint', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #av bm.rng 0',
                     'execute as @e[type=minecraft:wolf,tag=bm.avpet,distance=..12] if score @s bm.pid = #me bm.pid run scoreboard players set #av bm.rng 1',
                     'execute if score #av bm.rng matches 0 run return 0', 'scoreboard players set @s bm.khint 60',
                     G.title('@s', 'actionbar', [T('Queen Ava: ', AVA_C, bold=True), T('"Right-click the Font - and I will honour those who stand with you."', '#bfe8ff')])])
    fn('p201/open', ['scoreboard players set #ns bm.rng 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                     'scoreboard players set @s bm.hns0 0', 'scoreboard players set @s bm.hns1 0', 'scoreboard players set @s bm.hns2 0',
                     'data modify storage bm:ui hn set value {r_l0:{text:"—",color:"dark_gray"},r_l1:{text:"—",color:"dark_gray"},r_l2:{text:"—",color:"dark_gray"}}',
                     'execute unless score @s bm.fret matches 0.. run scoreboard players set @s bm.fret 0',
                     'execute store result storage bm:ui hn.sr int 1 run scoreboard players get @s bm.fret'] +
       [f'execute if score @s bm.fret matches {L} run data modify storage bm:ui hn.src set value "{t}"' for L, t in
        ((0, f'{HASTE[0][1]} Royal Pearls + {HASTE[0][2]} Dread Tokens'), (1, f'{HASTE[1][1]} Royal Pearls + {HASTE[1][2]} Dread Tokens + an Air Gem'), (2, 'at its height'))] +
       [f'execute if score #ns bm.rng matches ..2 as @e[type=minecraft:{P173.AR[w][1]},tag={P173.AR[w][2]},distance=..24] '
        f'if score @s bm.pid = #me bm.pid at @s run function bm:p201/slot/{w}' for w in FOL] +
       [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p201/list_dlg with storage bm:ui hn',
        'playsound minecraft:block.conduit.activate player @s ~ ~ ~ 0.8 1.4'])
    for w in FOL:
        nm, _pr, col = WHO[w][0], WHO[w][1], WHO[w][2]
        label = snbt([T(nm, col, bold=True), T('  ·  her honours', 'gray')])
        fn(f'p201/slot/{w}', ['scoreboard players add #ns bm.rng 1'] +
           [f'execute if score #ns bm.rng matches {k + 1} as @a if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.hns{k} {IDX[w]}' for k in range(3)] +
           [f'execute if score #ns bm.rng matches {k + 1} run data modify storage bm:ui hn.r_l{k} set value {label}' for k in range(3)] +
           [f'execute as @a if score @s bm.pid = #me bm.pid at @s run function bm:p201/bless/{w}'])
        fn(f'p201/bless/{w}', [f'execute unless score @s {obj(w)} matches 0.. run scoreboard players set @s {obj(w)} 0',
                               f'execute if score @s {obj(w)} matches 1000.. run return 0',
                               f'scoreboard players add @s {obj(w)} 1000',
                               f'scoreboard players operation #hv bm.rng = @s {obj(w)}', 'scoreboard players operation #hv bm.rng %= #10 bm.rng',
                               f'execute if score #hv bm.rng matches 0 run scoreboard players add @s {obj(w)} 1',
                               tellraw('@s', P + [T('THE ROYAL BLESSING: ', AVA_C, bold=True), T(nm, col, bold=True),
                                                  T(' kneels before Queen Ava - Vitality I, for good.', 'gray')]),
                               'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2'])
    B_ = lambda lbl, code, w=200, tip=None: P28.btn(lbl, code, tooltip=tip, width=w)
    lst = P28.multi([T("QUEEN AVA'S HONOURS", AVA_C, bold=True), T('  ·  the Tide Font', 'gray')],
                    [P28.body([T('"Those who stand by my family will be honoured by it. Who comes before me?"', '#bfe8ff', italic=True)], 320),
                     P28.body([T('Each follower with you can be honoured: Vitality, Bulwark and Might, five ranks each - for good, '
                                 'everywhere you call them, heists too.', 'gray')], 320),
                     P28.body([T("The Tide's Haste ", '#9af0d8', bold=True), T('$(sr)/2', 'white'),
                               T('   every follower you call: a faint rests 80 s, then 45 s', 'dark_gray')], 320)],
                    [B_('@@RAW:r_l0@@', MENU + 1), B_('@@RAW:r_l1@@', MENU + 2), B_('@@RAW:r_l2@@', MENU + 3),
                     B_([T("The Tide's Haste +1", '#9af0d8'), T('  ($(src))', 'gray')], MENU + 5)], columns=1)
    fn('p201/list_dlg', [f'$dialog show @s {P28.inline(lst)}'])

    # ---------------------------------------------------------------- a follower's page: three honours, five ranks
    pips = {L: '●' * L + '○' * (5 - L) for L in range(6)}
    def price_txt(w, k, L):
        if L >= 5: return 'at its height'
        t = f'{PEARLS[L]} Royal Pearls' + (f' + {DREAD[L]} Dread Token{"s" if DREAD[L] > 1 else ""}' if DREAD[L] else '')
        return t + ' + ' + trib_name(*TRIB[w][L]) + (f' + a {GEM[k][1]}' if L == 4 else '')
    def rank_txt(w, r):
        if r >= 3: return 'at its height'
        _to, pp, dd, ti, gem = RANKS[r]
        return (f'{pp} Royal Pearls' + (f' + {dd} Dread Token{"s" if dd > 1 else ""}' if dd else '') + ' + ' + trib_name(*TRIB[w][ti]) +
                (' + any Elemental Gem (Water, Rock or Fire)' if gem else ''))
    page = P28.multi([T("QUEEN AVA'S HONOURS", AVA_C, bold=True), T('  ·  ', 'gray'), '@@RAW:r_nm@@'],
                     [P28.body([T('Honour ', AVA_C, bold=True), T('$(hp)', 'white'), T('   Vitality, Bulwark and Might together', 'dark_gray')], 320)] +
                     [P28.body([T(s_nm + ' ', s_col, bold=True), T(f'$({k}p)', 'white'), T(f'   {desc}', 'dark_gray')], 320) for k, s_nm, s_col, desc in STATS] +
                     [P28.body([T('You have ', 'gray'), T('$(rp)', PEARL_C, bold=True), T(' Royal Pearls and ', 'gray'), T('$(dt)', '#b0102a', bold=True),
                                T(' Dread Tokens.', 'gray')], 320)],
                     [B_([T('Honour +1', AVA_C, bold=True), T('  ($(hc))', 'gray')], MENU + 11, w=260,
                         tip=T('One Honour, three ranks: each raises Vitality, Bulwark and Might together (II, IV, then V).', 'gray'))] +
                     [B_(T('« Her honours', 'gray'), MENU + 9, w=260)], columns=1)
    fn('p201/page_dlg', [f'$dialog show @s {P28.inline(page)}'])
    fn('p201/page', [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p177/wallet',
                     f'execute store result storage bm:ui hn.rp int 1 run clear @s {holds("royal_pearl")} 0'] +
       [f'execute if score @s bm.hnsel matches {IDX[w]} run function bm:p201/pg/{w}' for w in FOL] +
       ['data modify storage bm:ui hn.dt set from storage bm:ui vs.dt', 'function bm:p201/page_dlg with storage bm:ui hn'])
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        lines = [f'data modify storage bm:ui hn.r_nm set value {snbt(T(nm, col, bold=True))}',
                 f'execute unless score @s {obj(w)} matches 0.. run scoreboard players set @s {obj(w)} 0']
        for k, *_r in STATS:
            lines += [f'scoreboard players operation #hl bm.rng = @s {obj(w)}', f'scoreboard players operation #hl bm.rng /= #{UNIT[k]} bm.rng' if UNIT[k] > 1 else 'scoreboard players add #hl bm.rng 0',
                      'scoreboard players operation #hl bm.rng %= #10 bm.rng']
            lines += [f'execute if score #hl bm.rng matches {L} run data modify storage bm:ui hn.{k}p set value "{pips[L]}"' for L in range(6)]
            lines += [f'execute if score #hl bm.rng matches {L} run data modify storage bm:ui hn.{k}c set value "{price_txt(w, k, L)}"' for L in range(6)]
        lines += ['scoreboard players set #hr bm.rng 9'] + [l for k, *_r in STATS for l in (
            f'scoreboard players operation #hl bm.rng = @s {obj(w)}', f'scoreboard players operation #hl bm.rng /= #{UNIT[k]} bm.rng' if UNIT[k] > 1 else 'scoreboard players add #hl bm.rng 0',
            'scoreboard players operation #hl bm.rng %= #10 bm.rng', 'scoreboard players operation #hr bm.rng < #hl bm.rng')]
        # (the rank: the lowest of the three - 0, I at II, II at IV, III at V)
        lines += ['scoreboard players set #rk bm.rng 0', 'execute if score #hr bm.rng matches 2.. run scoreboard players set #rk bm.rng 1',
                  'execute if score #hr bm.rng matches 4.. run scoreboard players set #rk bm.rng 2', 'execute if score #hr bm.rng matches 5.. run scoreboard players set #rk bm.rng 3']
        lines += [f'execute if score #rk bm.rng matches {r} run data modify storage bm:ui hn.hp set value "{"●" * r + "○" * (3 - r)}"' for r in range(4)]
        lines += [f'execute if score #rk bm.rng matches {r} run data modify storage bm:ui hn.hc set value "{rank_txt(w, r)}"' for r in range(4)]
        fn(f'p201/pg/{w}', lines)

    # ---------------------------------------------------------------- buying a rank (2.94: one Honour - all three raised together)
    fn('p201/buy', [f'execute if score @s bm.hnsel matches {IDX[w]} run function bm:p201/b/{w}' for w in FOL] + ['function bm:p201/page'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #1000 bm.rng 1000']
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        o = obj(w)
        # (#hv, #hb, #hm: the three now; the rank from the lowest)
        lines = [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0',
                 f'scoreboard players operation #hv bm.rng = @s {o}', 'scoreboard players operation #hv bm.rng %= #10 bm.rng',
                 f'scoreboard players operation #hb bm.rng = @s {o}', 'scoreboard players operation #hb bm.rng /= #10 bm.rng', 'scoreboard players operation #hb bm.rng %= #10 bm.rng',
                 f'scoreboard players operation #hm bm.rng = @s {o}', 'scoreboard players operation #hm bm.rng /= #100 bm.rng', 'scoreboard players operation #hm bm.rng %= #10 bm.rng',
                 'scoreboard players operation #hr bm.rng = #hv bm.rng', 'scoreboard players operation #hr bm.rng < #hb bm.rng', 'scoreboard players operation #hr bm.rng < #hm bm.rng',
                 'execute if score #hr bm.rng matches 5.. run return run ' + say(f'{nm}\'s Honour is at its height.', AVA_C),
                 f'execute if score #hr bm.rng matches 4 run return run function bm:p201/pay/{w}3',
                 f'execute if score #hr bm.rng matches 2..3 run return run function bm:p201/pay/{w}2',
                 f'function bm:p201/pay/{w}1']
        fn(f'p201/b/{w}', lines)
        for r, (to, pp, dd, ti, gem) in enumerate(RANKS, 1):
            it, tn = TRIB[w][ti]
            pay = [f'execute store result score #c bm.rng run clear @s {holds("royal_pearl")} 0',
                   f'execute unless score #c bm.rng matches {pp}.. run return run ' + say(f'That rank takes {pp} Royal Pearls.', 'red'),
                   f'execute store result score #c bm.rng run clear @s {trib_pred(it)} 0',
                   f'execute unless score #c bm.rng matches {tn}.. run return run ' + say(f'For {nm}, Queen Ava asks {trib_name(it, tn)} as well.', 'red')]
            if gem:
                pay += ['scoreboard players set #gm bm.rng 0'] + \
                       [f'execute if score #gm bm.rng matches 0 if items entity @s container.* {holds("gem_" + g)} run scoreboard players set #gm bm.rng {i + 1}' for i, g in enumerate(GEMS_ANY)] + \
                       ['execute if score #gm bm.rng matches 0 run return run ' + say("The last rank takes an Elemental Gem - Water, Rock or Fire: a piece of the kingdom's heart.", 'red')]
            if dd:
                pay += [f'scoreboard players set #need bm.pay {dd}', 'execute unless function bm:p177/pay run return run function bm:p177/poor']
            if gem:
                pay += [f'execute if score #gm bm.rng matches {i + 1} run clear @s {holds("gem_" + g)} 1' for i, g in enumerate(GEMS_ANY)]
            # (each of the three up to the rank's level - never down; the blessing's thousand kept)
            pay += [f'clear @s {holds("royal_pearl")} {pp}', f'clear @s {trib_pred(it)} {tn}',
                    f'execute if score #hv bm.rng matches ..{to - 1} run scoreboard players set #hv bm.rng {to}',
                    f'execute if score #hb bm.rng matches ..{to - 1} run scoreboard players set #hb bm.rng {to}',
                    f'execute if score #hm bm.rng matches ..{to - 1} run scoreboard players set #hm bm.rng {to}',
                    f'scoreboard players operation #hk bm.rng = @s {o}', 'scoreboard players operation #hk bm.rng /= #1000 bm.rng', 'scoreboard players operation #hk bm.rng *= #1000 bm.rng',
                    'scoreboard players operation #hb bm.rng *= #10 bm.rng', 'scoreboard players operation #hm bm.rng *= #100 bm.rng',
                    'scoreboard players operation #hk bm.rng += #hv bm.rng', 'scoreboard players operation #hk bm.rng += #hb bm.rng', 'scoreboard players operation #hk bm.rng += #hm bm.rng',
                    f'scoreboard players operation @s {o} = #hk bm.rng', f'function bm:p205/check/{w}',
                    'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 1.2', 'particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.03 20',
                    tellraw('@s', P + [T(f'Honour {"I II III".split()[r - 1]}', AVA_C, bold=True), T(' for ', 'gray'), T(nm, col, bold=True),
                                       T(f' - Vitality, Bulwark and Might {"I II III IV V".split()[to - 1]}. Queen Ava touches the Font, and it is done.', 'gray')])]
            fn(f'p201/pay/{w}{r}', pay)

    # ---------------------------------------------------------------- the Tide's Haste (Swift Return, from Vesper's old Ledger)
    fn('p201/haste', ['execute unless score @s bm.fret matches 0.. run scoreboard players set @s bm.fret 0',
                      'execute if score @s bm.fret matches 2.. run return run ' + say("The Tide's Haste is at its height.", AVA_C),
                      'execute if score @s bm.fret matches 1 run return run function bm:p201/haste2', 'function bm:p201/haste1'])
    for L, (secs, pp, dd, gem) in enumerate(HASTE, 1):
        pay = [f'execute store result score #c bm.rng run clear @s {holds("royal_pearl")} 0',
               f'execute unless score #c bm.rng matches {pp}.. run return run ' + say(f'That takes {pp} Royal Pearls.', 'red')]
        if gem: pay += [f'execute unless items entity @s container.* {holds("gem_" + gem[0])} run return run ' + say(f'The last rank takes an {gem[1]}.', 'red')]
        pay += [f'scoreboard players set #need bm.pay {dd}', 'execute unless function bm:p177/pay run return run function bm:p177/poor']
        if gem: pay += [f'clear @s {holds("gem_" + gem[0])} 1']
        fn(f'p201/haste{L}', pay + [f'clear @s {holds("royal_pearl")} {pp}', f'scoreboard players set @s bm.fret {L}',
                                    'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 1.4',
                                    tellraw('@s', P + [T(f"The Tide's Haste {'I' * L}", '#9af0d8', bold=True), T(f': a faint now rests {secs} seconds, for every follower you call.', 'gray')]),
                                    'function bm:p201/open'])

    # the Tide's Haste at work: after a faint (2 minutes), the rest is cut short (2.93: from Vesper's old Ledger, its rule too)
    for w, (cd, *_r) in P173.AR.items():
        second += [f'execute as @a[scores={{bm.fret=1,{cd}=81..}}] run scoreboard players set @s {cd} 80',
                   f'execute as @a[scores={{bm.fret=2,{cd}=46..}}] run scoreboard players set @s {cd} 45']

    # ---------------------------------------------------------------- the Ethereal Gem comes home
    eth = f'items entity @s container.* {holds("ethereal_gem")}'
    G.FUNCS['p199/font/ask'][-1:-1] = [f'execute if {eth} if score #rq bm.rng matches 3 unless entity @s[tag=bm.keth_r] run function bm:p201/eth/royal']
    G.FUNCS['p199/font/ask'][1:1] = [f'execute if {eth} if score #r_apo bm.rng matches 1 unless entity @s[tag=bm.keth_a] run function bm:p201/eth/apo']   # (before 'nobody royal here')
    core = '@e[type=minecraft:marker,tag=bm.kingdom,distance=..70,sort=nearest,limit=1]'
    line = lambda who, col, txt: tellraw('@a[distance=..24]', [T(who + ': ', col, bold=True), T(txt, 'white')])
    ETH = '#e8c8ff'
    burst = ['particle minecraft:end_rod ~ ~2 ~ 1.5 1.5 1.5 0.1 120', 'particle minecraft:dust{color:[0.9,0.7,1.0],scale:2.0} ~ ~2 ~ 2 2 2 0 120'] + \
            [f'particle minecraft:dust{{color:[{r},{g},{b}],scale:1.6}} ~ ~2.5 ~ 1.2 1.2 1.2 0 30' for r, g, b in
             ((1.0, 0.45, 0.12), (0.2, 0.55, 1.0), (0.65, 0.3, 0.9), (0.2, 0.62, 0.45), (1.0, 0.9, 0.2), (0.65, 0.55, 0.45), (0.88, 0.96, 1.0), (0.35, 0.85, 0.3), (0.65, 0.92, 1.0))] + \
            ['playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1 1.4', 'playsound minecraft:block.amethyst_block.resonate player @a[distance=..32] ~ ~ ~ 1 0.6']
    fn('p201/eth/royal', ['tag @s add bm.keth_r'] + burst +
       [title('@a[distance=..32]', 'title', T('The Heart Comes Home', ETH, bold=True)),
        title('@a[distance=..32]', 'subtitle', T('the kingdom\'s lost heart, in the hands of its family', AVA_C)),
        line('Queen Ava', '#6ad8e8', 'The ethereal gem. Whole. I died for the pieces of it - and you simply... put it back together.'),
        line('Queen Pearl', '#5ae0d8', 'It is not ours to keep. Not any more. We kept it to ourselves once, and it broke the world.'),
        line('Emma', '#ff8ad8', 'Then let it bless the one who carries it. Go on - hold it up to the Font!'),
        tellraw('@a[distance=..24]', [T('*The Font drinks the gem\'s light, the whole castle glows... and the light comes back into your hands, changed.*', ETH, italic=True)]),
        f'execute as {core} run tag @s add bm.keth', give('heartstone', 2), give('royal_pearl', 24),
        tellraw('@s', [T('  + ', 'gray'), T('the Blessing of the Heart', ETH, bold=True), T(' (+2 hearts, for good), the dome WARDED (no breach can shatter it), 2 Heartstones, 24 Royal Pearls', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1'])
    second.append('execute as @a[tag=bm.keth_r] run attribute @s minecraft:max_health modifier add bm:heart_home 4 add_value')
    lost = G.FUNCS['p199/breach/lost']
    k = next(i for i, l in enumerate(lost) if 'p199/dome/shatter' in l)
    lost[k] = lost[k].replace('execute if score', 'execute unless entity @s[tag=bm.keth] if score')
    apo_up = []
    for k2, s_nm, _c, _d in STATS:
        apo_up += ['scoreboard players operation #hl bm.rng = @s bm.hn_apo', f'scoreboard players operation #hl bm.rng /= #{UNIT[k2]} bm.rng' if UNIT[k2] > 1 else 'scoreboard players add #hl bm.rng 0',
                   'scoreboard players operation #hl bm.rng %= #10 bm.rng', f'execute if score #hl bm.rng matches ..4 run scoreboard players add @s bm.hn_apo {UNIT[k2]}']
    fn('p201/eth/apo', ['tag @s add bm.keth_a', 'execute unless score @s bm.hn_apo matches 0.. run scoreboard players set @s bm.hn_apo 0'] + burst[:2] +
       ['particle minecraft:soul_fire_flame ~ ~2 ~ 1.2 1.2 1.2 0.05 80', 'playsound minecraft:entity.wither.ambient hostile @a[distance=..24] ~ ~ ~ 0.6 0.6',
        title('@a[distance=..32]', 'title', T("The Serpent's Restraint", '#3aff9a', bold=True)),
        title('@a[distance=..32]', 'subtitle', T('the gem he once killed for, an arm\'s length away', ETH)),
        line('Apophiss', '#3aff9a', '...That. I burned a palace for that. I ended a queen for the heart of it.'),
        line('Apophiss', '#3aff9a', 'It sings. Even now it sings to me, and I could take it from you before you blinked.'),
        tellraw('@a[distance=..24]', [T('*The serpent\'s claws close an inch from the gem... and open. He lowers his head to the Font instead.*', '#3aff9a', italic=True)]),
        line('Apophiss', '#3aff9a', 'Keep it. Keep it from me. That is the only gift I have for this place.'),
        ] + apo_up +
       [give('heartstone', 2), give('royal_pearl', 16),
        tellraw('@s', [T('  + ', 'gray'), T('Apophiss', '#3aff9a', bold=True), T(' gains a rank of every honour (Vitality, Bulwark, Might), 2 Heartstones, 16 Royal Pearls', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.8'])

    # ---------------------------------------------------------------- the router
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU}..{MENU + 99} run return run function bm:p201/act')
    fn('p201/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    'execute unless entity @e[type=minecraft:interaction,tag=bm.kfont,distance=..8] run return run function bm:p28/stale'] +
       [f'execute if score #act bm.pay matches {MENU + 1 + k} unless score @s bm.hns{k} matches 1.. run return run function bm:p201/open' for k in range(3)] +
       [f'execute if score #act bm.pay matches {MENU + 1 + k} run scoreboard players operation @s bm.hnsel = @s bm.hns{k}' for k in range(3)] +
       [f'execute if score #act bm.pay matches {MENU + 1}..{MENU + 3} run return run function bm:p201/page',
        f'execute if score #act bm.pay matches {MENU + 9} run return run function bm:p201/open',
        f'execute if score #act bm.pay matches {MENU + 5} run return run function bm:p201/haste'] +
       [f'execute if score #act bm.pay matches {MENU + 11} run return run function bm:p201/buy'])

    # ---------------------------------------------------------------- the honours, worn by every follower you call (each second; re-applied on change)
    for w in FOL:
        typ, tag = P173.AR[w][1], P173.AR[w][2]
        second.append(f'execute as @e[type=minecraft:{typ},tag={tag}] at @s run function bm:p201/ap/{w}')
        fn(f'p201/ap/{w}', ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            'scoreboard players set #hv bm.rng 0',
                            f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #hv bm.rng = @s {obj(w)}',
                            'execute if score @s bm.hnap = #hv bm.rng run return 0',
                            'scoreboard players operation @s bm.hnap = #hv bm.rng', 'function bm:p201/apply'])
    ap = ['attribute @s minecraft:max_health modifier remove bm:royal_vitality', 'attribute @s minecraft:armor modifier remove bm:royal_bulwark',
          'attribute @s minecraft:armor_toughness modifier remove bm:royal_bulwark', 'attribute @s minecraft:attack_damage modifier remove bm:royal_might',
          # (Vesper's retired wards)
          'attribute @s minecraft:armor modifier remove bm:dread_ward', 'attribute @s minecraft:armor_toughness modifier remove bm:dread_ward',
          'attribute @s minecraft:max_health modifier remove bm:dread_vigor',
          'scoreboard players operation #hl bm.rng = #hv bm.rng', 'scoreboard players operation #hl bm.rng %= #10 bm.rng']
    ap += [f'execute if score #hl bm.rng matches {L} run attribute @s minecraft:max_health modifier add bm:royal_vitality {0.2 * L:.1f} add_multiplied_base' for L in range(1, 6)]
    ap += ['scoreboard players operation #hl bm.rng = #hv bm.rng', 'scoreboard players operation #hl bm.rng /= #10 bm.rng', 'scoreboard players operation #hl bm.rng %= #10 bm.rng']
    ap += [f'execute if score #hl bm.rng matches {L} run attribute @s minecraft:armor modifier add bm:royal_bulwark {3 * L} add_value' for L in range(1, 6)]
    ap += [f'execute if score #hl bm.rng matches {L} run attribute @s minecraft:armor_toughness modifier add bm:royal_bulwark {L} add_value' for L in range(1, 6)]
    ap += ['scoreboard players operation #hl bm.rng = #hv bm.rng', 'scoreboard players operation #hl bm.rng /= #100 bm.rng', 'scoreboard players operation #hl bm.rng %= #10 bm.rng',
           'scoreboard players operation @s bm.kua = #hl bm.rng']
    ap += [f'execute if score #hl bm.rng matches {L} run attribute @s minecraft:attack_damage modifier add bm:royal_might {0.15 * L:.2f} add_multiplied_base' for L in range(1, 6)]
    ap += ['data modify entity @s Health set value 1024.0f', 'execute if score #hv bm.rng matches 1.. run particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.02 6']
    fn('p201/apply', ap)

    # ---------------------------------------------------------------- Vesper's Ward and Vigor, retired: every token back
    refund = {L: sum(WARD[:L]) for L in (1, 2, 3)}
    second += ['execute as @a[scores={bm.fward=1..}] run function bm:p201/refund_w', 'execute as @a[scores={bm.fvig=1..}] run function bm:p201/refund_v']
    for k, o, nm in (('w', 'bm.fward', 'Ward'), ('v', 'bm.fvig', 'Vigor')):
        fn(f'p201/refund_{k}', [f'execute if score @s {o} matches {L} run function bm:p177/refund {{n:{refund[L]}}}' for L in (1, 2, 3)] +
           [tellraw('@s', P + [T(f'Vesper\'s {nm} is retired', '#c8a0a0', bold=True), T(' - his Dread Tokens are back in your pockets. Follower honours are ', 'gray'),
                               T("Queen Ava's", AVA_C, bold=True), T(' now: bring her to the Tide Font in the Underwater Kingdom.', 'gray')]),
            f'scoreboard players set @s {o} 0'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('Queen Ava\'s Honours', AVA_C), T('  at the Tide Font with Ava: Vitality, Bulwark, Might I-V per follower', 'gray')]))


# ================================================================================================ the build pass: Might
# A follower's special attacks are the pack's own `damage` commands, naming the follower as the attacker - a tag the follower
# wears only while it strikes (bm.cpme, bm.emme, bm.kxme...). Each one is sent through a little function that reads the
# attacker's Might (bm.kua, set by p201/apply) and deals 115% / 130% / ... of the damage. Bosses' own *me tags never carry
# bm.kua, so their blows are unchanged.
STATIC = re.compile(r'damage @s (\d+(?:\.\d+)?) ([a-z_:]+) by (@e\[[^\]]*tag=bm\.[a-z0-9]+me2?[,\]][^\]]*\]?)$')
MACRO = re.compile(r'^\$damage @s \$\(d\) ([a-z_:]+) by (@e\[[^\]]*tag=bm\.[a-z0-9]+me2?[,\]][^\]]*\]?)$')
BOSS = ('bm.vwkme', 'bm.sphme', 'bm.salme', 'bm.hhme', 'bm.trtme', 'bm.gvbme', 'bm.dbme', 'bm.eskme')


def finalize(G):
    import hashlib
    made, n = {}, 0
    def key(*a): return hashlib.md5('|'.join(a).encode()).hexdigest()[:10]
    lvl = lambda sel: ['scoreboard players set #fl bm.rng 0', f'execute store result score #fl bm.rng run scoreboard players get {sel} bm.kua']
    for name in list(G.FUNCS):
        if name.startswith('p201/'): continue
        lines = G.FUNCS[name]
        for i, l in enumerate(lines):
            m = MACRO.match(l)
            if m:
                typ, sel = m.groups()
                if any(b + ',' in sel or b + ']' in sel for b in BOSS): continue
                h = key('m', typ, sel)
                if h not in made:
                    made[h] = True
                    G.FUNCS[f'p201/fm/{h}'] = ['$data modify storage bm:fd d set value $(d)', 'execute store result score #fd bm.rng run data get storage bm:fd d 100'] + lvl(sel) + \
                        ['scoreboard players operation #fm bm.rng = #fl bm.rng', 'scoreboard players operation #fm bm.rng *= #15 bm.rng',
                         'scoreboard players add #fm bm.rng 100', 'scoreboard players operation #fd bm.rng *= #fm bm.rng', 'scoreboard players operation #fd bm.rng /= #100 bm.rng',
                         'execute store result storage bm:fd x float 0.01 run scoreboard players get #fd bm.rng', f'function bm:p201/fm/{h}_d with storage bm:fd']
                    G.FUNCS[f'p201/fm/{h}_d'] = [f'$damage @s $(x) {typ} by {sel}']
                lines[i] = f'$function bm:p201/fm/{h} {{d:$(d)}}'; n += 1
                continue
            m = STATIC.search(l)
            if not m or l.startswith('$'): continue
            amt, typ, sel = m.groups()
            if any(b + ',' in sel or b + ']' in sel for b in BOSS): continue
            h = key('s', amt, typ, sel)
            if h not in made:
                made[h] = True
                a = float(amt)
                G.FUNCS[f'p201/fs/{h}'] = lvl(sel) + [f'execute if score #fl bm.rng matches {L} run return run damage @s {a * (1 + 0.15 * L):g} {typ} by {sel}' for L in range(1, 6)] + \
                    [f'damage @s {amt} {typ} by {sel}']
            lines[i] = l[:m.start()] + f'function bm:p201/fs/{h}'; n += 1
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #15 bm.rng 15', 'scoreboard players set #100 bm.rng 100']
    return n, len(made)
