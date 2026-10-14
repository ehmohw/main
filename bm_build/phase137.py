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
"""
from items import T


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
    # the Hollow's trials: a challenger within reach
    sub('p2/hollow/dg', 'execute unless entity @a[distance=..100,scores={bm.conq=..5}] run return run function bm:p2/hollow/amb',
        'execute unless entity @a[distance=..100,tag=bm.hch] run return run function bm:p2/hollow/amb')
    # what beating the Hollow King earned: the Warpstone, Wilfrey, followers in the Hollow, its gates, the Gate's way through, the den
    subs('p2/hollow/warp', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    subs('p2/wil/locket', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    subs('p2/wil/grave', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
    subs('p74/fol_ok', 'unless score @s bm.conq matches 6..', 'unless score @s bm.conqb matches 6..')
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
