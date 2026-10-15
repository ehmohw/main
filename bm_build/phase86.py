"""2.67: THE GUTTER ECONOMY - fewer coins, bigger pieces, three kinds of haul, and the Scrap Box.

FEWER COINS: everything that pays into a heist's pot pays about a third of what it did (guards, captains, the
  guardian, secrets, events, party rooms); the haul's own coins are halved too.
BIGGER PIECES: GUTTER MEDALLIONS (16 coins) and GUTTER TROPHIES (8 medallions - 128 coins). Goldtooth changes them
  either way; the Gutter Bank takes them as coins. Goldtooth's dearest goods are priced in medallions now (nothing costs
  more than a stack of coins any more), and a Black Market Token costs 2 medallions (32 coins) - at the bank as well.
THREE KINDS OF HAUL: pick yours at the den's haul lectern (it's yours until you change it):
  THE PLAIN HAUL       vanilla goods - iron, gold, diamonds, emeralds, redstone, XP bottles, enchanted books, golden apples
                       (and at the top tiers ancient debris and netherite scrap), plus a full load of building supplies.
  THE BLACK MARKET HAUL (the default)  the heist gear you know, the Fence's curios (sell them to the Scrap Box), and the
                       Fixer's prize: Tokens (1 at Tier I, up to 5 at Tier V) and Medallions (from Tier III, 2 at most);
                       a BM Trophy, very rarely, at Tier V. Only this haul pays Tokens or Medallions.
  THE GUTTER HAUL      Gutter Coins, the tier's spoils, Captain's Insignia, Gutter Medallions from Tier III, and heist
                       supplies (healing draughts, smoke bombs, lockpicks, key fragments).
THE SCRAP BOX: in the den and in the Locker Hall. Drop in what you don't need - heist gear, curios, spare vault
  trophies, Bond Sigils, banners, the Phantom Regalia... - and it pays Gutter Coins (it keeps anything it doesn't buy).
"""
import math
from items import item, T, TOTEM, ITEMS
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75

GOLD = '#ffcf40'
GUT = '#e0a040'
item('gutter_medallion', TOTEM, 'Gutter Medallion', GUT, ['Sixteen Gutter Coins, struck into one.', ('Goldtooth changes it back - or takes', 'blue'),
                                                         ('eight for a Gutter Trophy.', 'blue'), ('The Gutter Bank counts it as 16 coins.', 'dark_gray')],
     model='bm:gutter_medallion', stack=64, cat='currency')
item('gutter_trophy', TOTEM, 'Gutter Trophy', '#ffd870', ['Eight Gutter Medallions in a little gold cup.', ('128 coins, for the dearest goods.', 'blue'),
                                                         ('The Gutter Bank counts it as 128 coins.', 'dark_gray')],
     model='bm:gutter_trophy', stack=64, cat='currency', glint=True)
CURIOS = [('stolen_watch', 'Stolen Pocket Watch', '#d8c070', 'Still ticking. Somebody misses it.', 4),
          ('forged_seal', 'Forged Seal', '#d05050', 'Good enough to fool a clerk.', 7),
          ('smugglers_ledger', "Smuggler's Ledger", '#a07850', 'Names, dates, debts - worth something to someone.', 12)]
for _iid, _nm, _col, _lore, _v in CURIOS:
    item(_iid, TOTEM, _nm, _col, [_lore, ('A Fence\'s curio. The Scrap Box', 'blue'), (f'pays {_v} Gutter Coins for it.', 'blue')], model=f'bm:{_iid}', stack=16, cat='misc')
P72.KEEP += ['gutter_medallion', 'gutter_trophy']

# (the Black Market haul's prize is phase75's capped table, PRIZE_TOK / PRIZE_MED / PRIZE_TRO - an older, richer copy that
#  sat here overrode the caps and is gone)

THEMES = {1: ('THE PLAIN HAUL', '#9ad0ff', 'vanilla goods and building supplies'),
          2: ('THE BLACK MARKET HAUL', '#c070ff', 'heist gear, curios - and Tokens and Medallions'),
          3: ('THE GUTTER HAUL', GUT, 'coins, spoils, insignia and heist supplies')}
CODE = 8410
POT_PCT = 35                        # what the pot keeps of everything paid into it (2.67)


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase28 as P28
    import phase70 as P70
    import phase80 as P80
    import phase81 as P81
    import phase76 as P76
    import phase77 as P77
    rel = RM.rel
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    second = []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvth dummy', f'scoreboard players set #k{POT_PCT} bm.rng {POT_PCT}', 'scoreboard players set #k100 bm.rng 100']
    G.OBJECTIVES += ['bm.gvth']

    # ================================================================== FEWER COINS: the pot keeps a third of what's paid in (rounded by chance)
    pa = G.FUNCS['p75/pot_add']
    pa[1:1] = [f'scoreboard players operation #c bm.rng *= #k{POT_PCT} bm.rng', 'execute store result score #rr bm.rng run random value 0..99',
               'scoreboard players operation #c bm.rng += #rr bm.rng', 'scoreboard players operation #c bm.rng /= #k100 bm.rng']
    for key in ('guard', 'captain', 'boss'):
        f_ = G.FUNCS[f'p75/kill_{key}']
        G.FUNCS[f'p75/kill_{key}'] = [('execute if score #c bm.rng matches 1.. run ' + l) if l.startswith('title @s actionbar') else l for l in f_]
    for f_, a, b in [('p76/flawless', 'Flawless! 5 coins into the pot.', 'Flawless! Coins into the pot.'),
                     ('p75/trophy_again', 'You have this trophy already - 4 coins into the pot.', 'You have this trophy already - coins into the pot.'),
                     ('p76/r/rave/drop', 'Nice moves! +2 coins', 'Nice moves!'), ('p85/says/right', 'Right! +1 coin', 'Right!')]:
        G.FUNCS[f_] = [l.replace(a, b) for l in G.FUNCS[f_]]

    # ================================================================== BIGGER PIECES: Goldtooth changes money, and prices his dearest goods in medallions
    from gen_dp import offer
    orig = P70.goldtooth
    coin_id = ITEMS['gutter_coin']['comps']['minecraft:custom_data']['bm']
    def is_coin(st):
        return st is not None and st.get('components', {}).get('minecraft:custom_data', {}).get('bm') == coin_id
    def g86():
        d = orig()
        rec = d['Offers']['Recipes']
        for r in rec:
            n = int(r['buy']['count']) if is_coin(r['buy']) else 0
            if n and is_coin(r.get('buyB')):
                n += int(r['buyB']['count']); r.pop('buyB')
            if n > 32:
                r['buy'] = offer(('gutter_medallion', math.ceil(n / 16)), ('minecraft:stone', 1))['buy']
        rec[0:0] = [offer(('gutter_coin', 16), ('gutter_medallion', 1)), offer(('gutter_medallion', 1), ('gutter_coin', 16)),
                    offer(('gutter_medallion', 8), ('gutter_trophy', 1)), offer(('gutter_trophy', 1), ('gutter_medallion', 8))]
        return d
    P70.goldtooth = g86
    G.FUNCS['p70/r/lobby/init'] = [l.replace(snbt(orig()), snbt(g86())) if 'bm.gvgt' in l and 'summon minecraft:villager' in l else l for l in G.FUNCS['p70/r/lobby/init']]
    assert any(snbt(g86()) in l for l in G.FUNCS['p70/r/lobby/init']), "Goldtooth's summon wasn't found to reprice"

    # ================================================================== THREE KINDS OF HAUL
    def ent(i, w, c=None, fns=()):
        if i in ITEMS:
            e = dict(G.loot_entry(i, G.uni(*c) if isinstance(c, tuple) else c), weight=w)
            return e
        e = {'type': 'minecraft:item', 'name': i if ':' in i else 'minecraft:' + i, 'weight': w, 'functions': list(fns)}
        if c: e['functions'].append({'function': 'minecraft:set_count', 'count': G.uni(*c) if isinstance(c, tuple) else c})
        return e
    book = lambda w, lv: {'type': 'minecraft:item', 'name': 'minecraft:book', 'weight': w, 'functions': [{'function': 'minecraft:enchant_with_levels', 'levels': lv}]}
    PLAIN = {
        1: [ent('iron_ingot', 30, (3, 6)), ent('coal', 20, (8, 16)), ent('copper_ingot', 14, (6, 12)), ent('gold_ingot', 12, (2, 4)), ent('redstone', 10, (6, 12)),
            ent('lapis_lazuli', 8, (4, 8)), ent('emerald', 6, (1, 3)), ent('experience_bottle', 6, (2, 4)), ent('arrow', 6, (8, 16)), book(3, 10)],
        2: [ent('iron_ingot', 24, (4, 8)), ent('gold_ingot', 14, (3, 6)), ent('diamond', 8, (1, 1)), ent('redstone', 10, (8, 16)), ent('lapis_lazuli', 8, (6, 10)),
            ent('emerald', 8, (2, 4)), ent('experience_bottle', 8, (3, 6)), ent('ender_pearl', 5, (1, 2)), ent('obsidian', 5, (2, 4)), book(4, 15), ent('name_tag', 2)],
        3: [ent('diamond', 12, (1, 2)), ent('iron_block', 6, (1, 1)), ent('gold_block', 6, (1, 1)), ent('emerald', 10, (3, 6)), ent('experience_bottle', 10, (4, 8)),
            ent('ender_pearl', 6, (2, 3)), book(6, 20), ent('golden_apple', 3), ent('blaze_rod', 5, (2, 4)), ent('obsidian', 4, (4, 8)), ent('quartz', 5, (8, 16))],
        4: [ent('diamond', 14, (2, 3)), ent('emerald_block', 5, (1, 1)), ent('iron_block', 6, (1, 2)), ent('gold_block', 6, (1, 2)), ent('experience_bottle', 10, (6, 10)),
            book(8, 25), ent('golden_apple', 5), ent('ender_pearl', 6, (2, 4)), ent('blaze_rod', 5, (3, 6)), ent('netherite_scrap', 1)],
        5: [ent('diamond', 14, (2, 4)), ent('diamond_block', 2), ent('emerald_block', 6, (1, 2)), ent('experience_bottle', 10, (8, 14)), book(8, 30),
            ent('golden_apple', 6, (1, 2)), ent('ancient_debris', 2), ent('netherite_scrap', 3), ent('ender_pearl', 5, (3, 5)), ent('enchanted_golden_apple', 1)]}
    spoil = {t: P80.MATS[t - 1][0] for t in range(1, 6)}
    ins_ = P80.MATS[5][0]
    GUTTER = {t: [ent('gutter_coin', 40, (1 + t, 3 + 2 * t)), ent(spoil[t], 26, (2, 3 + t // 2)), ent('clockwork_fragment', 8), ent('healing_draught', 8, (1, 2)),
                  ent('smoke_bomb', 8, (2, 3)), ent('skeleton_lockpick', 5)] + ([ent(ins_, 3 + t)] if t >= 2 else []) +
              ([ent('gutter_medallion', 2 * t - 2)] if t >= 3 else []) + [ent('treasure_map_scrap', 3)] for t in range(1, 6)}
    for t in range(1, 6):
        wjson(f'bm/loot_table/gv/v{t}.json', {'pools': [{'rolls': 1, 'entries': PLAIN[t]}]})
        wjson(f'bm/loot_table/gv/g{t}.json', {'pools': [{'rolls': 1, 'entries': GUTTER[t]}]})
    haul = G.FUNCS['p70/haul']
    haul[0:0] = ['scoreboard players operation #th bm.rng = @s bm.gvth', 'execute unless score #th bm.rng matches 1..3 run scoreboard players set #th bm.rng 2']
    def themed(lines, ref, cond):
        out = []
        for l in lines:
            if f'{ref}/t' not in l: out.append(l); continue
            assert l.startswith('execute '), l
            out += [l.replace('execute ', f'execute if score {cond} matches 2 ', 1),
                    l.replace('execute ', f'execute if score {cond} matches 1 ', 1).replace(f'{ref}/t', f'{ref}/v'),
                    l.replace('execute ', f'execute if score {cond} matches 3 ', 1).replace(f'{ref}/t', f'{ref}/g')]
        return out
    G.FUNCS['p70/haul_roll'] = themed(G.FUNCS['p70/haul_roll'], 'bm:gv', '#th bm.rng')
    cp = G.FUNCS['p70/r/cache/pay']
    G.FUNCS['p70/r/cache/pay'] = ['scoreboard players operation #th bm.rng = @s bm.gvth', 'execute unless score #th bm.rng matches 1..3 run scoreboard players set #th bm.rng 2'] + \
        themed(cp, 'bm:gv', '#th bm.rng')
    G.FUNCS['p75/prize'][0:0] = ['execute unless score #th bm.rng matches 2 run return 0']
    k = next(i for i, l in enumerate(haul) if 'Your haul: ' in l)
    haul[k + 1:k + 1] = [f'execute if score #th bm.rng matches {n} run ' + tellraw('@s', P + [T(nm, col, bold=True), T(' - ' + what + '.', 'gray')]) for n, (nm, col, what) in THEMES.items()]
    # (the den's haul lectern: pick yours)
    G.FUNCS['p70/r/lobby/init'] += [f'setblock {rel(20, 4, 2)} minecraft:lectern[facing=south]',
                                    f'summon minecraft:interaction {rel(20, 4, 2)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvthsel'], 'width': F(1.05), 'height': F(1.2), 'response': B(1)}),
                                    f'summon minecraft:text_display {rel(20, 5.6, 2)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(0x70000000),
                                                                                              'text': [T('YOUR HAUL\n', GOLD, bold=True), T('plain, Black Market or gutter', 'gray')],
                                                                                              'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                                 'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})]
    G.FUNCS['loop/fast'][-1:-1] = ['execute as @e[type=minecraft:interaction,tag=bm.gvthsel] if data entity @s interaction run function bm:p86/theme/click',
                                   'execute as @e[type=minecraft:interaction,tag=bm.gvthsel] if data entity @s attack run data remove entity @s attack']
    fn('p86/theme/click', ['execute on target run function bm:p86/theme/menu', 'data remove entity @s interaction'])
    dlg = P28.multi([T('YOUR HAUL', GOLD, bold=True), T('  ·  what the Fixer packs for you', 'gray')],
                    [P28.body([T('Pick the kind of haul you want when a heist is won. It stays yours until you change it.', 'gray')], 320),
                     P28.body([T('Only the Black Market haul pays Tokens and Medallions.', 'dark_gray')], 320)],
                    [P28.btn([T(nm, col, bold=True), T('\n' + what, 'gray')], CODE + n, width=300) for n, (nm, col, what) in THEMES.items()],
                    columns=1)
    fn('p86/theme/menu', [f'scoreboard players set @s bm.menu {CODE}', f'dialog show @s {snbt(dlg)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {CODE + 1}..{CODE + 3} run return run function bm:p86/theme/pick')
    fn('p86/theme/pick', [f'execute unless score @s bm.menu matches {CODE} run return run function bm:p28/stale',
                          'scoreboard players operation @s bm.gvth = #act bm.pay', f'scoreboard players remove @s bm.gvth {CODE}'] +
       [f'execute if score @s bm.gvth matches {n} run ' + tellraw('@s', P + [T('Your haul from now on: ', 'gray'), T(nm, col, bold=True), T(' - ' + what + '.', 'gray')])
        for n, (nm, col, what) in THEMES.items()] + ['playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1'])

    # ================================================================== THE SCRAP BOX
    SCRAP = {'smoke_bomb': 1, 'skeleton_lockpick': 2, 'clockwork_fragment': 2, 'heisters_shiv': 4, 'thiefs_cowl': 5, 'smugglers_boots': 5, 'vault_breaker': 6,
             'cipher_monocle': 8, 'frog_monocle': 6, 'gilded_staff_topper': 8, 'golden_spear': 8, 'coinslinger': 8, 'gutter_cutlass': 10, 'treasurers_scepter': 16,
             'vault_hound_whistle': 16, 'healing_draught': 1, 'second_wind': 6, 'treasure_map_scrap': 3, 'golden_compass': 4, 'lucky_purse': 5, 'master_key': 12,
             'lost_lantern': 8, 'rats_foot': 8, 'gutter_laurel': 10, 'fixers_card': 6, 'gilded_boots': 6, 'gilded_leggings': 8, 'gilded_chestplate': 10,
             'gilded_helmet': 6}
    SCRAP.update({iid: v for iid, _n, _c, _l, v in CURIOS})
    SCRAP.update({iid: 8 for iid, *_r in P76.PHANTOM})
    SCRAP.update({f'raid_banner_{t}': 2 * t for t in range(1, 6)})
    SCRAP.update({iid: max(4, c // 6) for n, iid, nm, col, what, c, i in P81.SIGILS})
    MV = {'copper': 3, 'iron': 5, 'gold': 8, 'emerald': 10, 'diamond': 14, 'netherite': 20}
    SCRAP.update({f'trophy_{k}_{mk}': MV[mk] for k in P81.TK for mk, *_r in P81.METALS})
    SCRAP.update({f'contract_{v[0]}': max(4, v[7] // 4) for v in P77.HIRE.values()})
    SCRAP = {k: v for k, v in SCRAP.items() if k in ITEMS}
    coin = dict(G.stack('gutter_coin', 1)); coin.pop('count', None)
    G.FUNCS['load'][-1:-1] = [f'data modify storage bm:gsc t set value {snbt({k: Int(v) for k, v in SCRAP.items()})}',
                              f'data modify storage bm:scrap money.gutter_coin set value {snbt(coin)}']
    S = 'storage bm:gsc'
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvscrap] at @s if block ~ ~ ~ minecraft:barrel if data block ~ ~ ~ Items[0] run function bm:p86/gs/box')
    fn('p86/gs/box', [f'data modify {S} src set from block ~ ~ ~ Items', f'data modify {S} keep set value []', 'scoreboard players set #tot bm.rng 0',
                      'function bm:p86/gs/scan', 'execute if score #tot bm.rng matches ..0 run return 0',
                      f'data modify block ~ ~ ~ Items set from {S} keep',
                      'data modify storage bm:scrap pay set value [{c:"gutter_coin",n:0}]', 'execute store result storage bm:scrap pay[0].n int 1 run scoreboard players get #tot bm.rng',
                      'function bm:p51/payall', 'playsound minecraft:block.grindstone.use block @a[distance=..10] ~ ~ ~ 0.8 1.1',
                      'particle minecraft:wax_off ~ ~0.7 ~ 0.3 0.2 0.3 0 8',
                      'execute as @a[distance=..6] run ' + title('@s', 'actionbar', [T('Scrapped for ', GUT), {'score': {'name': '#tot', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                                    T(' Gutter Coins', GUT)])])
    fn('p86/gs/scan', [f'execute unless data {S} src[0] run return 0', f'data modify {S} it set from {S} src[0]', f'data remove {S} src[0]',
                       f'data remove {S} k', 'scoreboard players set #v bm.rng 0',
                       f'execute unless data {S} it.components."minecraft:custom_data".bm_kit if data {S} it.components."minecraft:custom_data".bm run data modify {S} k.id set from {S} it.components."minecraft:custom_data".bm',
                       f'execute if data {S} k.id run function bm:p86/gs/look with {S} k',
                       f'execute if score #v bm.rng matches ..0 run data modify {S} keep append from {S} it',
                       f'execute if score #v bm.rng matches 1.. store result score #n bm.rng run data get {S} it.count',
                       'execute if score #v bm.rng matches 1.. run scoreboard players operation #v bm.rng *= #n bm.rng',
                       'execute if score #v bm.rng matches 1.. run scoreboard players operation #tot bm.rng += #v bm.rng', 'function bm:p86/gs/scan'])
    fn('p86/gs/look', [f'$execute store result score #v bm.rng run data get {S} t."$(id)"'])
    box_label = snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(0x70000000),
                      'text': [T('SCRAP BOX\n', GUT, bold=True), T('spare raid goods for coins', 'gray')],
                      'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})
    G.FUNCS['p70/r/lobby/init'] += [f'setblock {rel(2, 4, 9)} minecraft:barrel[facing=up]', f'summon minecraft:marker {rel(2, 4, 9)} {{Tags:["bm.gvprop","bm.gvscrap"]}}',
                                    f'summon minecraft:text_display {rel(2, 5.6, 9)} {box_label}']
    hb = G.FUNCS['p84/hall/build']
    hb[-1:-1] = ['setblock -253 64 -242 minecraft:barrel[facing=up]', 'kill @e[type=minecraft:marker,tag=bm.gvscrap,x=-253,y=64,z=-242,distance=..1]',
                 'summon minecraft:marker -252.5 64 -241.5 {Tags:["bm.gvscrap"]}',
                 'summon minecraft:text_display -252.5 65.6 -241.5 ' + box_label.replace('"bm.gvprop"', '"bm.lkt"')]
    fn('admin/gutter_money', [G.give('gutter_medallion', 16), G.give('gutter_trophy', 2)])     # (2.79c: no curios - no haul has had them since 2.68)

    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    g = R.grid
    R.ICONS['gutter_medallion'] = g(['................', '.....oooooo.....', '...ooYYYYYYoo...', '..oYYyyyyyyYYo..', '..oYykyyyykyYo..', '.oYyykkyykkyyYo.',
                                     '.oYyykwkkwkyyYo.', '.oYyykkkkkkyyYo.', '.oYyyykppkyyyYo.', '.oYyyyykkyyyyYo.', '..oYyyyyyyyyYo..', '..oYYyyyyyyYYo..',
                                     '...ooYYYYYYoo...', '.....oooooo.....', '................', '................'],
                                    dict(o='#6a3c0c', Y='#f0b850', y='#c8862a', k='#4a2a08', w='#fff0c0', p='#ff9ab0'))
    R.ICONS['gutter_trophy'] = g(['................', '..oooooooooooo..', '.oYYYYYYYYYYYYo.', 'oYoYwYYYYYYYYoYo', 'oYoYwYYYYYYYyoYo', 'oYoYYYYYYYYYyoYo',
                                  '.oYoYYYYYYYyoYo.', '..oooYYYYYyooo..', '....oYYYYYyo....', '.....oYYYyo.....', '......oYyo......', '......oYyo......',
                                  '....ooYYYyoo....', '...okkkkkkkko...', '...oooooooooo...', '................'],
                                 dict(o='#7a5410', Y='#ffd870', y='#d0a030', w='#fffbe0', k='#5a3a20'))
    R.ICONS['stolen_watch'] = g(['.......cc.......', '......c..c......', '......oYYo......', '....ooYYYYoo....', '...oYwwwwwwYo...', '..oYwwwwkwwwYo..',
                                 '..oYwwwwkwwwYo..', '..oYwwwwkkkwYo..', '..oYwwwwwwwwYo..', '..oYwwwwwwwwYo..', '...oYwwwwwwYo...', '....ooYYYYoo....',
                                 '......oooo......', '................', '................', '................'],
                                dict(c='#c0a050', o='#6a5010', Y='#e0c060', w='#f8f4e8', k='#202020'))
    R.ICONS['forged_seal'] = g(['................', '.....rrrrrr.....', '...rrRRRRRRrr...', '..rRRRRRRRRRRr..', '..rRRddddddRRr..', '.rRRdRRRRRRdRRr.',
                                '.rRRdRwRRwRdRRr.', '.rRRdRRwwRRdRRr.', '.rRRdRRRRRRdRRr.', '..rRRddddddRRr..', '..rRRRRRRRRRRr..', '...rrRRRRRRrr...',
                                '.....rrrrrr.....', '................', '................', '................'],
                               dict(r='#6a1010', R='#d04040', d='#902020', w='#ff9a9a'))
    R.ICONS['smugglers_ledger'] = g(['................', '...bbbbbbbbbb...', '...bBBBBBBBBpb..', '...bBBBBBBBBpb..', '...bBGGGGGGBpb..', '...bBBBBBBBBpb..',
                                     '...bBGGGGBBBpb..', '...bBBBBBBBBpb..', '...bBBBBBBBBpb..', '...bBBBBBBBBpb..', '...bBBBBBBBBpb..', '...bBBBBBBBBpb..',
                                     '...bbbbbbbbbbb..', '................', '................', '................'],
                                    dict(b='#3a2410', B='#8a5a30', G='#e0c060', p='#e8e0c8'))
