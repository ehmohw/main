"""2.78: POLISH - fringe cases fixed, old rough edges smoothed.

THE KEY OF NEW BEGINNINGS (the Fence, 3 Tokens) - what a fresh start resets, and what it never takes away:
- YOUR CONQUEST RECORD goes back to zero: every dungeon can be won again, in order, and each first victory pays again
  (its Emblem, its lore, the next Sealed Map; Wilfrey's Keep a Hollow Gate). The Dark Auction's "next boss key" follows
  the record, and so do the altars and the Hollow Gate's pass for the climb.
- WHAT YOU EARNED STAYS EARNED: a new record "best ever" (bm.conqb) remembers how far you have ever got. Beaten the
  Hollow King once and you keep - through any number of fresh starts - his Warpstone (it never goes cold; you never get a
  second one), Wilfrey (his locket and his grave), the Serpent's Den (the seal reads for you, Apophiss rises for you),
  your followers in the Hollow, its gates opening as you walk up, and the Hollow Gate's way through.
- THE HOLLOW sleeps for a veteran: its trials wake only for a CHALLENGER - someone at the fifth conquest, ready for the
  King (a veteran climbing again wakes them then, and fights the King again for the record) - or someone who has never
  beaten him. A veteran mid-climb visiting the Throne doesn't wake it for the friends already there.
- NOT MID-FIGHT: the key refuses while a dungeon boss (or Apophiss) is awake near you - finish the fight first.
- THE DIALOG says all of that before you press Yes.
- From before: a record already reset leaves no trace of how far it went - the best-ever record is rebuilt from the
  Hollow King's advancement, a Warpstone or Wilfrey's locket carried (on you or in your ender chest).

EVERY FOLLOWER IN A FRAME: Zib's Donadian Medal, KillerWatt's Spark and Pearlman's card hung in an item frame bring
them out to live by it, as every other follower's item does.
"""
from items import T
import phase68 as _P68

_n = max(v[0] for v in _P68.KINDS.values()) + 1
_P68.KINDS['zib'] = (_n, 'donadian_medal', 'wolf', 'bm.zibpet', 'p72/zb/summon', 'p72/zb/dismiss', 'bm.zbsel', 'Zib', '#3ad8c8')
_P68.KINDS['kw'] = (_n + 1, 'kw_spark', 'wolf', 'bm.kxpet', 'p79/pet/summon', 'p79/pet/home', 'bm.kxsel2', 'KillerWatt', '#74d462')
_P68.KINDS['pearl'] = (_n + 2, 'pearl_card', 'cat', 'bm.pmpet', 'p128/pm/summon', 'p128/pm/dismiss', 'bm.pmsel2', 'Pearlman', '#5ac8ff')
_P68.HE.update({'zib', 'kw', 'pearl'})


def generate(G):
    import phase28 as P28
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'

    def sub(name, old, new, count=1):
        """replace a whole line (exactly `count` of them) in function `name`"""
        L = G.FUNCS[name]
        idx = [i for i, l in enumerate(L) if l == old]
        assert len(idx) == count, (name, old, len(idx))
        for i in idx: L[i] = new

    def subs(name, old, new):
        """replace a fragment inside every line of `name` that has it (at least one)"""
        L = G.FUNCS[name]
        n = 0
        for i, l in enumerate(L):
            if old in l: L[i] = l.replace(old, new); n += 1
        assert n, (name, old)

    # ================================================================== the best-ever conquest record
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.conqb dummy']
    G.OBJECTIVES += ['bm.conqb']
    S = G.FUNCS['loop/second']
    hs_old = 'execute in bm:hollow_throne store success score #hsafe bm.p2 unless entity @a[distance=0..,gamemode=!spectator,scores={bm.conq=..5}]'
    k = S.index(hs_old)
    S[k:k + 1] = ['scoreboard players add @a bm.conqb 0',
                  'execute as @a[tag=!bm.cqbm] run function bm:p137/cqb_mig',
                  'execute as @a if score @s bm.conq > @s bm.conqb run scoreboard players operation @s bm.conqb = @s bm.conq',
                  # (a challenger wakes the Hollow: at the fifth conquest, or never yet past the King)
                  'tag @a remove bm.hch', 'tag @a[scores={bm.conq=5}] add bm.hch', 'tag @a[scores={bm.conq=..4,bm.conqb=..5}] add bm.hch',
                  'execute in bm:hollow_throne store success score #hsafe bm.p2 unless entity @a[distance=0..,gamemode=!spectator,tag=bm.hch]']
    warp = holds('hollow_warpstone')
    locket = holds('wilfrey_locket')
    fn('p137/cqb_mig', ['tag @s add bm.cqbm',
                        'execute if entity @s[advancements={bm:story/boss_hollow=true}] run scoreboard players set @s[scores={bm.conqb=..5}] bm.conqb 6',
                        f'execute if items entity @s container.* {warp} run scoreboard players set @s[scores={{bm.conqb=..5}}] bm.conqb 6',
                        f'execute if items entity @s enderchest.* {warp} run scoreboard players set @s[scores={{bm.conqb=..5}}] bm.conqb 6',
                        f'execute if items entity @s container.* {locket} run scoreboard players set @s[scores={{bm.conqb=..5}}] bm.conqb 6',
                        f'execute if items entity @s enderchest.* {locket} run scoreboard players set @s[scores={{bm.conqb=..5}}] bm.conqb 6',
                        # (and anyone already holding the Warpstone keeps it from being given twice)
                        f'execute if score @s bm.conqb matches 6.. run tag @s add bm.got_warp'])

    # the Warpstone is granted once, ever (a fresh start no longer takes the "given" mark away)
    sub('loop/second', 'execute as @a[scores={bm.conq=6..},tag=!bm.got_warp] run function bm:p2/hollow/warp_grant',
        'execute as @a[scores={bm.conqb=6..},tag=!bm.got_warp] run function bm:p2/hollow/warp_grant')
    # Wilfrey counts toward the three-follower limit too, and won't come when it's full
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:wolf,tag=bm.wilfrey] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p2/wil/try_summon'].insert(0, 'execute if function bm:p58/full run return 0')
    # the Shard of the Hollow Throne was retired in 2.48 (an old one, used, re-forms as a Hollow Gate): the admin give list
    # no longer hands it out alongside the Hollow Gate, the maps and the Warpstone
    G.FUNCS['admin/give/p2map'] = [l for l in G.FUNCS['admin/give/p2map'] if 'bm:"hollow_summons"' not in l]
    assert len(G.FUNCS['admin/give/p2map']) == 7, G.FUNCS['admin/give/p2map']
    # the Hollow's trials: a challenger within reach
    sub('p2/hollow/dg', 'execute unless entity @a[distance=..100,scores={bm.conq=..5}] run return run function bm:p2/hollow/amb',
        'execute unless entity @a[distance=..100,tag=bm.hch] run return run function bm:p2/hollow/amb')
    # what beating the Hollow King earned: the Warpstone, Wilfrey, followers in the Hollow, its gates, the Gate's way through, the den
    subs('p2/hollow/warp', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    subs('p2/wil/locket', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    subs('p2/wil/grave', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    # (p74/fol_ok: 2.78 lets followers into the Hollow for anyone - no conquest to check there any more)
    sub('p61/pass', 'execute unless score @s bm.conq matches 5.. run return run function bm:p61/bounce',
        'execute unless score @s bm.conq matches 5.. unless score @s bm.conqb matches 6.. run return run function bm:p61/bounce')
    subs('loop/second', 'if entity @a[distance=..7,scores={bm.conq=6..},gamemode=!spectator] run function bm:p131/gate',
         'if entity @a[distance=..7,scores={bm.conqb=6..},gamemode=!spectator] run function bm:p131/gate')
    subs('p131/seal/sec', 'scores={bm.conq=6..}', 'scores={bm.conqb=6..}')
    subs('p131/seal/sec', 'scores={bm.conq=..5}', 'scores={bm.conqb=..5}')
    subs('p131/lair/worthy', 'scores={bm.conq=6..}', 'scores={bm.conqb=6..}')

    # (the admin's "set your conquest record" sets the best-ever record too - a clean newcomer or veteran to test with)
    for n in range(7):
        f = G.FUNCS.get(f'admin/p2/conquest_{n}')
        if f: f[0:0] = [f'scoreboard players set @s bm.conqb {n}', 'tag @s add bm.cqbm'] + (['tag @s remove bm.got_warp'] if n < 6 else [])

    # ================================================================== the key itself: say what it does, and not mid-fight
    from p2.config import D, ORDER
    first = D[ORDER[0]]
    dlg = P28.multi([T('Key of New Beginnings', '#e8e8ff', bold=True)],
                    [P28.body([T('Reset your conquest record to zero? ', 'white'),
                               T(f'The road starts again at {first["title"]}: every dungeon can be won again, in order, and each first victory pays again '
                                 '(its Emblem, its lore, the next map).', 'gray')]),
                     P28.body([T('You keep everything you own - and what you have earned stays earned: ', 'gray'),
                               T("the Hollow King's Warpstone, Wilfrey, the Serpent's Den and your followers' welcome in the Hollow.", '#c8c4d8')], 300)],
                    [P28.btn(T('Yes - start over', 'gold'), 7101, width=200), P28.btn(T('No', 'gray'), 7102, width=200)], columns=2)
    G.FUNCS['p34/renew/use'] = ['execute unless score @s bm.conq matches 1.. run return run ' +
                                say('Your conquest record is already clear - the key would change nothing. (Keep it for later.)', '#e8e8ff'),
                                'execute if function bm:p137/renew_fight run return run ' +
                                say('Not now - the key won\'t turn while a boss is awake nearby. Finish the fight first.', '#e8e8ff'),
                                f'scoreboard players set @s bm.menu {P28.MENU["renew"]}', f'dialog show @s {P28.inline(dlg)}']
    fn('p137/renew_fight', ['execute if entity @e[type=minecraft:marker,tag=bm.arena,distance=..96,scores={bm.bs=1..2}] run return 1',
                            'execute if entity @e[type=minecraft:husk,tag=bm.apboss,distance=..96] run return 1', 'return 0'])
    act = G.FUNCS['p34/renew/act']
    act.remove('tag @s remove bm.got_warp')
    k = next(i for i, l in enumerate(act) if l.startswith('clear @s ') and 'renewal_key' in l)     # (before the key is used up)
    act[k:k] = ['execute if function bm:p137/renew_fight run return run ' + say('Not now - finish the fight first.', '#e8e8ff')]
    act.append(tellraw('@s', PREFIX + [T('A new beginning: ', '#e8e8ff', bold=True), T('your conquest record is clear. ', 'gray'),
                                       T(f'Start again at {first["title"]} - the Fence sells every Sealed Map, and your old ones still lead the way. ', 'gray'),
                                       T('What you earned stays yours.', '#c8c4d8')]))

    # ================================================================== THE RECRUITER: raid contracts only for followers you've met
    # (2.78) His trades were the same for everyone - every follower's contract on sale from the start, spoiling the ones you
    # haven't found yet. He is a dialog shop now (like the Tailor - it knows who you are): a follower's contract is on his
    # books once you have met them out in the world (held their item - bm:met/<kind>, a hidden advancement); the vault's
    # hirelings and the vault gems as before. A contract for someone you haven't met won't sign (it keeps) - for contracts
    # bought before. Nothing is free: no starter contract (Cecil's too comes once you have his Summoning Gem).
    import phase72 as P72, phase98 as P98, phase103 as P103, phase77 as P77, phase60 as P60, phase70_rooms as RM
    from nbt import snbt
    from items import ITEMS
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    GOLD, REC = '#ffcf40', '#9ad0ff'
    MET = {'cecil': ['cecil_gem'], 'emma': ['emma_ribbon'], 'celi': ['celi_charm'], 'zib': ['donadian_medal'], 'killerwatt': ['kw_spark'],
           'leo': ['leo_crest'], 'demo': ['demo_seal'], 'escort': [f'skiff_escort_{c}' for c in P72.ART.ESCORT_COLS], 'apo': ['apo_oath'],
           'tul': ['tul_coin'], 'frog': ['frog_signet'], 'donado': ['donado_tag'], 'fishy': ['fy_bowl'], 'dennis': ['dw_horn'], 'pistachio': ['pi_cloche'], 'omega': ['om_monocle'], 'ashur': ['ashur_cinder'], 'chef': ['chef_ladle'], 'neighbor': ['neighbor_baton'], 'ava': ['av_locket'], 'pearlq': ['pq_pearls'], 'bloo': ['bo_claw']}
    FOL = [(k, nm, col) for (k, nm, col, *_r) in P98.CALLED] + [(k, nm, col) for (k, nm, col, *_r) in P98.HIRED]
    assert {k for k, *_r in FOL} == set(MET), sorted({k for k, *_r in FOL} ^ set(MET))
    for k, toks in MET.items():
        crit = {}
        for t in toks:
            assert t in ITEMS, t
            crit[t] = {'trigger': 'minecraft:inventory_changed',
                       'conditions': {'items': [{'items': ITEMS[t]['base'], 'predicates': {'minecraft:custom_data': snbt({'bm': t})}}]}}
        G.wjson(f'bm/advancement/met/{k}.json', {'criteria': crit, 'requirements': [list(crit)]})
    met = lambda k: f'entity @s[advancements={{bm:met/{k}=true}}]'
    CALLED_K = {c[0] for c in P98.CALLED}
    signed_fn = lambda k: f'bm:p98/signed/{k}' if k in CALLED_K else f'bm:p98/filed/{k}'

    # ---- (2.82b) the den's Raid Crew page: a follower you haven't met isn't on it - their name gave them away before you'd found
    #      them. (One with a contract signed already - from before - stays.)
    for i, (k, nm, col) in enumerate(FOL):
        L = G.FUNCS[f'p103/crew/row_{i}']
        assert L[0].startswith(f'scoreboard players set #ad{i} '), L[0]
        L.insert(1, f'execute unless {met(k)} unless function {signed_fn(k)} run return 0')

    # ---- a contract for someone you haven't met won't sign (it keeps)
    SIGN = {k: f'p89/sign/{k}' for k in ('cecil', 'emma', 'celi', 'zib', 'escort', 'killerwatt')}
    SIGN.update({'leo': 'p96/sign', 'demo': 'p97/sign', 'apo': 'p131/sign', 'tul': 'p132/sign', 'frog': 'p89/call/frog', 'donado': 'p89/call/donado',
                 'fishy': 'p145/sign', 'dennis': 'p163/dw/sign', 'pistachio': 'p163/pi/sign', 'omega': 'p170/sign', 'ashur': 'p185/sign', 'chef': 'p186/sign', 'neighbor': 'p187/sign', 'ava': 'p189/sign', 'pearlq': 'p190/sign', 'bloo': 'p191/sign'})
    assert set(SIGN) == set(MET)
    for k, nm, col in FOL:
        L = G.FUNCS[SIGN[k]]
        j = next(i for i, l in enumerate(L) if l.startswith('scoreboard players set @s bm.gvhc'))
        L.insert(j + 1, f'execute unless {met(k)} run return run function bm:p137/unmet {{n:"{nm}"}}')
    fn('p137/unmet', ['$' + tellraw('@s', GP + [T('A contract for ', 'gray'), T('$(n)', 'white'), T("? You haven't met them yet - find them out in the world first. ", 'gray'),
                                                T('(The contract keeps.)', 'dark_gray')]),
                      'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 1'])

    # ---- his stock, from his old trades (phase103, phase131/132): prices in coins (Medallions 16, Trophies 128)
    worth = {'gutter_coin': 1, 'gutter_medallion': 16, 'gutter_trophy': 128}
    sid = lambda st: st.get('components', {}).get('minecraft:custom_data', {}).get('bm', '')
    coins = lambda o: sum(int(o[b]['count']) * worth[sid(o[b])] for b in ('buy', 'buyB') if b in o)
    stock = {sid(o['sell']): o for o in P103.RECRUITER_OFFERS}
    fols = [(k, nm, col, coins(stock[f'fcontract_{k}'])) for k, nm, col in FOL]
    hires = [(i, hk, hnm, hcol, coins(stock[f'contract_{hk}'])) for i, (hk, hnm, rat, hcol, *_r) in P77.HIRE.items()]
    gems = [(g, P60.GEMS[g][0], P60.GEMS[g][1], stock[f'gem_{g}']) for g in P60.GEMS if f'gem_{g}' in stock]
    assert len(fols) <= 38 and len(hires) == 5 and len(gems) == 9 and len(stock) == len(fols) + 14, (len(fols), len(hires), len(gems), len(stock))   # (2.86: the followers' contracts grow; 8001-8039 hold 38)
    def give_cmd(st):
        comps = ','.join(c if c.startswith('!') else f'{c}={snbt(v)}' for c, v in st.get('components', {}).items())
        return f'give @s {st["id"]}[{comps}] {int(st["count"])}'

    RC = 8000                     # (his block: 8000 his page, 8001+ follower contracts, 8040 the hirelings' page, 8041+ theirs, 8050 the gems', 8051+)
    wal = [T('You have ', 'gray'), T('$(w)', GOLD, bold=True), T(' coins to spend', 'gray'), T(' (Gutter Bank and pockets; Medallions count 16, Trophies 128).', 'dark_gray')]
    btn = lambda lab, code: P28.btn(lab, code, width=180)
    back = btn([T('« The Recruiter', 'gray')], RC)
    def page(name, head, bodies, rows):
        d = P28.multi(head, bodies, [], columns=2, exit_label='Close')
        d['actions'] = '@@RAW:acts@@'
        fn(f'p137/rc/{name}', ['function bm:p98/init', 'function bm:p103/wallet', f'scoreboard players set @s bm.menu {RC}',
                               'data modify storage bm:ui rc.w set from storage bm:ui tl.w', 'data modify storage bm:ui rc.acts set value []'] + rows +
           [f'function bm:p137/rc/{name}_dlg with storage bm:ui rc'])
        fn(f'p137/rc/{name}_dlg', [f'$dialog show @s {P28.inline(d)}'])
    st = lambda txt, col: T(txt, col, bold=True)
    rows = ['scoreboard players set #rcp bm.rng 0', 'scoreboard players set #n bm.rng 0']
    for i, (k, nm, col, pr) in enumerate(fols):
        code = RC + 1 + i
        rows += ['scoreboard players set #st bm.rng 0',
                 f'execute if {met(k)} run scoreboard players add #n bm.rng 1', f'execute if {met(k)} run scoreboard players set #st bm.rng 1',
                 f'execute if score #st bm.rng matches 1 if items entity @s container.* {holds(f"fcontract_{k}")} run scoreboard players set #st bm.rng 2',
                 f'execute if function {signed_fn(k)} run scoreboard players set #st bm.rng 3',
                 f'execute if score #st bm.rng matches 1 run data modify storage bm:ui rc.acts append value {snbt(btn([T(nm, col, bold=True), T("  "), T(f"{pr} coins", GOLD)], code))}',
                 f'execute if score #st bm.rng matches 2 run data modify storage bm:ui rc.acts append value {snbt(btn([T(nm, col, bold=True), T("  "), st("IN YOUR PACK", "#ffe08a")], code))}',
                 f'execute if score #st bm.rng matches 3 run data modify storage bm:ui rc.acts append value '
                 f'{snbt(btn([T(nm, col, bold=True), T("  "), st("SIGNED" if k in CALLED_K else "FILED", "#7aff7a")], code))}']
    rows += ['execute store result storage bm:ui rc.n int 1 run scoreboard players get #n bm.rng',
             'data modify storage bm:ui rc.r_note set value ""',
             'execute if score #n bm.rng matches 0 run data modify storage bm:ui rc.r_note set value ' +
             snbt(T('No names on his books yet - meet a follower out in the world, then come back.', '#ffb070')),
             f'data modify storage bm:ui rc.acts append value {snbt(btn([T("Hirelings", "#e8c070", bold=True), T(" ›", "gray")], RC + 40))}',
             f'data modify storage bm:ui rc.acts append value {snbt(btn([T("Vault gems", "#e8b8ff", bold=True), T(" ›", "gray")], RC + 50))}']
    page('main', [T('THE RECRUITER', REC, bold=True), T('  ·  raid contracts', 'gray')],
         [P28.body([T('A Raid Contract signs a follower on for the vault - use it once and they come on every heist. ', 'gray'),
                    T("He only deals in names you know: the followers you've met out in the world.", '#c8c4d8')], 360),
          P28.body([T("Followers you've met: ", 'gray'), T('$(n)', 'white', bold=True), T(f' of {len(fols)}.  ', 'gray'), '@@RAW:r_note@@'], 360),
          P28.body(wal, 360)], rows)
    rows = ['scoreboard players set #rcp bm.rng 1']
    for i, hk, hnm, hcol, pr in hires:
        code = RC + 40 + i
        rows += ['scoreboard players set #st bm.rng 1',
                 f'execute if items entity @s container.* {holds(f"contract_{hk}")} run scoreboard players set #st bm.rng 2',
                 f'execute if function bm:p98/filed/h{i} run scoreboard players set #st bm.rng 3',
                 f'execute if score #st bm.rng matches 1 run data modify storage bm:ui rc.acts append value {snbt(btn([T(hnm, hcol, bold=True), T("  "), T(f"{pr} coins", GOLD)], code))}',
                 f'execute if score #st bm.rng matches 2 run data modify storage bm:ui rc.acts append value {snbt(btn([T(hnm, hcol, bold=True), T("  "), st("IN YOUR PACK", "#ffe08a")], code))}',
                 f'execute if score #st bm.rng matches 3 run data modify storage bm:ui rc.acts append value {snbt(btn([T(hnm, hcol, bold=True), T("  "), st("FILED", "#7aff7a")], code))}']
    rows += [f'data modify storage bm:ui rc.acts append value {snbt(back)}']
    page('hires', [T('HIRELINGS', '#e8c070', bold=True), T('  ·  the Recruiter', 'gray')],
         [P28.body([T("The vault's own hands for hire - use a contract once and it's filed in your Fixer's Ledger (Raid Crew). One at a time on a heist; "
                      "they never leave the vault.", 'gray')], 360), P28.body(wal, 360)], rows)
    rows = ['scoreboard players set #rcp bm.rng 2'] + \
           [f'data modify storage bm:ui rc.acts append value {snbt(btn([T(gn, gcol, bold=True), T("  "), T(f"{coins(o)} coins", GOLD)], RC + 51 + j))}'
            for j, (g, gn, gcol, o) in enumerate(gems)] + [f'data modify storage bm:ui rc.acts append value {snbt(back)}']
    page('gems', [T('VAULT GEMS', '#e8b8ff', bold=True), T('  ·  the Recruiter', 'gray')],
         [P28.body([T("Pearlman's nine, the vault's own: hand one to Cecil or KillerWatt in here. They stay in the vault.", 'gray')], 360), P28.body(wal, 360)], rows)
    fn('p137/rc/reopen', ['execute if score #rcp bm.rng matches 1 run return run function bm:p137/rc/hires',
                          'execute if score #rcp bm.rng matches 2 run return run function bm:p137/rc/gems', 'function bm:p137/rc/main'])
    fn('p137/rc/note', ['$' + tellraw('@s', GP + [T('$(t)', 'gray')]), 'function bm:p137/rc/reopen'])
    fn('p137/rc/poor', ['$' + tellraw('@s', GP + [T("That's $(n) coins - you have ", 'red'), {'score': {'name': '#tw', 'objective': 'bm.rng'}, 'color': 'white'},
                                                  T(' (bank and pockets).', 'red')]), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1', 'function bm:p137/rc/reopen'])
    def buy(pr, item_line, msg):
        return ['function bm:p103/wallet', f'execute if score #tw bm.rng matches ..{pr - 1} run return run function bm:p137/rc/poor {{n:{pr}}}',
                f'scoreboard players set #need bm.rng {pr}', 'function bm:p103/spend', item_line,
                'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1', tellraw('@s', GP + msg), 'function bm:p137/rc/reopen']
    for i, (k, nm, col, pr) in enumerate(fols):
        fn(f'p137/rc/f{i}', ['scoreboard players set #rcp bm.rng 0',
                             f'execute unless {met(k)} run return run function bm:p137/rc/note {{t:"He only deals in names you know."}}',
                             f'execute if function {signed_fn(k)} run return run function bm:p137/rc/note {{t:"{nm} is signed on already."}}',
                             f'execute if items entity @s container.* {holds(f"fcontract_{k}")} run return run function bm:p137/rc/note '
                             f'{{t:"You have that contract - use it to sign {nm} on."}}'] +
           buy(pr, give_cmd(stock[f'fcontract_{k}']['sell']), [T('The Recruiter hands you ', 'gray'), T(f'Raid Contract: {nm}', col, bold=True),
                                                                 T('. Use it once to sign them on.', 'gray')]))
    for i, hk, hnm, hcol, pr in hires:
        fn(f'p137/rc/h{i}', ['scoreboard players set #rcp bm.rng 1',
                             f'execute if function bm:p98/filed/h{i} run return run function bm:p137/rc/note {{t:"{hnm} is filed in your Ledger already."}}',
                             f'execute if items entity @s container.* {holds(f"contract_{hk}")} run return run function bm:p137/rc/note '
                             f'{{t:"You have that contract - use it to file {hnm} in your Ledger."}}'] +
           buy(pr, give_cmd(stock[f'contract_{hk}']['sell']), [T('The Recruiter hands you ', 'gray'), T(f"{hnm}'s contract", hcol, bold=True), T('.', 'gray')]))
    for j, (g, gn, gcol, o) in enumerate(gems):
        fn(f'p137/rc/g{j}', ['scoreboard players set #rcp bm.rng 2'] +
           buy(coins(o), give_cmd(o['sell']), [T('The Recruiter hands you a ', 'gray'), T(gn, gcol, bold=True), T(' - the vault\'s own.', 'gray')]))
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {RC}..{RC + 99} run return run function bm:p137/rc/act')
    fn('p137/rc/act', [f'execute unless score @s bm.menu matches {RC} run return run function bm:p28/stale',
                       f'execute if score #act bm.pay matches {RC} run return run function bm:p137/rc/main',
                       f'execute if score #act bm.pay matches {RC + 40} run return run function bm:p137/rc/hires',
                       f'execute if score #act bm.pay matches {RC + 50} run return run function bm:p137/rc/gems'] +
       [f'execute if score #act bm.pay matches {RC + 1 + i} run return run function bm:p137/rc/f{i}' for i in range(len(fols))] +
       [f'execute if score #act bm.pay matches {RC + 40 + i} run return run function bm:p137/rc/h{i}' for i, *_r in hires] +
       [f'execute if score #act bm.pay matches {RC + 51 + j} run return run function bm:p137/rc/g{j}' for j in range(len(gems))])

    # ---- at his counter (in the den and the Lounge): a click on him opens his book; his old trades are gone
    at = RM.rel(*P103.RECRUITER_AT)
    box = lambda tag: f'summon minecraft:interaction {at} {{Tags:["{tag}","bm.rechit"],width:1.0f,height:2.1f,response:1b}}'
    bare = snbt(dict(P103.RECRUITER_NPC, Offers={'Recipes': []}))
    for f_, prop, tag in (('p70/r/lobby/init', 'bm.gvprop', 'bm.gvprop'), ('p121/props', 'bm.gvprop', 'bm.lgprop')):
        L = G.FUNCS[f_]
        k = [i for i, l in enumerate(L) if l.startswith(f'summon minecraft:villager {at} ') and 'bm.gvrec' in l]
        assert len(k) == 1, (f_, len(k))
        L[k[0]] = f'summon minecraft:villager {at} ' + bare.replace(f'"{prop}"', f'"{tag}"')
        L.append(box(tag))
    # (dens and Lounges built before: put him right where he stands)
    G.FUNCS['loop/second'] += ['execute in bm:gutter as @e[type=minecraft:villager,tag=bm.gvrec,distance=0..] at @s run function bm:p137/rc_fix']
    fn('p137/rc_fix', ['execute if data entity @s Offers.Recipes[0] run data modify entity @s Offers.Recipes set value []',
                       'execute if entity @s[tag=bm.gvprop] unless entity @e[type=minecraft:interaction,tag=bm.rechit,distance=..1] run '
                       'summon minecraft:interaction ~ ~ ~ {Tags:["bm.gvprop","bm.rechit"],width:1.0f,height:2.1f,response:1b}',
                       'execute if entity @s[tag=bm.lgprop] unless entity @e[type=minecraft:interaction,tag=bm.rechit,distance=..1] run '
                       'summon minecraft:interaction ~ ~ ~ {Tags:["bm.lgprop","bm.rechit"],width:1.0f,height:2.1f,response:1b}'])
    G.FUNCS['loop/fast'] += ['execute as @e[type=minecraft:interaction,tag=bm.rechit] if data entity @s interaction run function bm:p137/rc_click',
                             'execute as @e[type=minecraft:interaction,tag=bm.rechit] if data entity @s attack run data remove entity @s attack']
    fn('p137/rc_click', ['execute on target at @s run function bm:p137/rc/main', 'data remove entity @s interaction'])
