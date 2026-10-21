"""2.82t: THE URGENT FIXES - the Ledger stays in hand in the gutter, the Dark Auction survives a night slept through, the Hollow
stays standing, Wilfrey's locket answers a click, followers back after two minutes (and by themselves), the summoning items
earned once, the satchel and the Prime Cooler, the Apophiss weakness, the Lucky map pieces and the Skiff parts.

THE LEDGER       dropped in the gutter (the den, the Lounge, a heist), it bounces straight back to whoever threw it - as the
                 kit's own weapons do.
THE DARK AUCTION its doors open at dusk (12000) on a sale night, not in the one-hour window at 17000 a bed always skipped (a
                 world that sleeps at nightfall never saw one); slept through after the doors open, the first lot is called
                 at daybreak instead of waiting for a midnight that never comes.
THE HOLLOW       mob griefing stays off while the Hollow King (either form) is alive in the Hollow Throne, not only while a
                 player is in it: a crew that died or left mid-fight came back to a Wither that had been wrecking the castle.
WILFREY          (p2/wilfrey.py) the locket is a click, not a one-second "use" that's eaten and handed back; sneak + use: his
                 menu - Call him / Call him over, Send him home, his wardrobe. His fall: 2 minutes, not 30.
FOLLOWERS        every overworld follower's faint is 2 minutes (was 5; the vault keeps its 45 seconds); and when it's over
                 the follower comes back by themselves, wherever you are outside the gutter - unless switched off on their
                 wardrobe page ("Back after a faint").
SUMMONING ITEMS  Dennis's horn and Pistachio's cloche are handed out once, at the fiftieth trade; lost, they take fifty
                 trades more. Fishy's bowl: only from Fishy himself, a button on his Cabinet page (phase145).
THE SATCHEL      every Vacuum Satchel is its own bag again (its contents ride in the item; the old per-player store moves into
                 the first one used); a filter of up to five items (use it with the item in your other hand: added, or
                 taken off again); and a satchel's or cooler's barrel broken while it's out puts everything back.
THE PRIME COOLER right-click switches its gathering on and off, as the satchel does; sneak + right-click sets it down.
APOPHISS         fire is his bane, in both forms: a Cecil or KillerWatt with the Fire Gem (or Wraithfire) takes 8 more from
                 him with every blow.
THE LUCKY MAP    pieces and the VORN SKIFF parts: each find is one you don't carry yet, while there's one you lack (the
                 last piece no longer takes a dozen duplicates). On a heist, what you carried walking in still counts.
KITS             every kit carries a plain Infinity bow and its arrow, for monsters out of reach (the Ranged kit has its own).
THE SALVE        Goldtooth's Salamander Salve keeps your followers out of the fire too.
BIG RIGS         a follower's host left without its model (Apophiss, Tullius, Fishy, Dennis, Pistachio, Omega) is cleared after 3 s,
                 so a heist calls them back instead of counting an invisible host.
HIGH GROUND      the fighting rooms have wall ledges five blocks up (ladders at their ends), the vault's guardian hall a gallery
                 six up down both long walls - somewhere to jump from with a mace.
GUTTER TRADERS   the Lounge's Goldtooth, Recruiter and Tailor take today's coins, Medallions and Insignias again: they kept
                 the trades (and the item stamp) of the version that first summoned them; now they are refreshed when the list changes.
THE REGALIA      the Wings of the Damned stand in for the Ribcage: wings + the other three pieces still wake the full set.
ONE CREW         in the gutter (den, lounge, heists) players can't hurt each other.
HEIST WINS       now and then a Lucky Map piece turns up in your haul: 6% at Tier I, 2% more each tier, 14% at Tier V.
THE SPIRE        solo, a Spire or Bell Tower drawn in place of a crew-only room left its exit door ten blocks above the
                 next passage, over open void: the layout now climbs with it, as it always did for a room drawn the usual way.
"""
import json
import os
import re

from items import T, ITEMS
from nbt import snbt

GOLD = '#ffcf40'
WMENU = 2360                       # Wilfrey's menu (bm.menu) and its buttons 2361..2364
AR_CODE = 2370                     # "Back after a faint" on each wardrobe page: 2370 + the follower's index
# (wardrobe key: cooldown score, the follower's host type and tag, the function that calls them - as you, at you)
AR = {'cecil': ('bm.cpcd', 'wolf', 'bm.cecilpet', 'p46/pet/try_summon'),
      'emma': ('bm.emcd', 'cat', 'bm.emmapet', 'p57/try_summon'),
      'celi': ('bm.cecd', 'wolf', 'bm.celipet', 'p66/try_summon'),
      'zib': ('bm.zbcd', 'wolf', 'bm.zibpet', 'p72/zb/try_summon'),
      'kw': ('bm.kxcd', 'wolf', 'bm.kxpet', 'p79/pet/try'),
      'leo': ('bm.lecd', 'wolf', 'bm.leopet', 'p96/try_summon'),
      'demo': ('bm.dmcd', 'wolf', 'bm.dmpet', 'p97/try_summon'),
      'apo': ('bm.apcd', 'wolf', 'bm.appet', 'p131/try_summon'),
      'tul': ('bm.tucd', 'wolf', 'bm.tupet', 'p132/try_summon'),
      'frog': ('bm.fgcd', 'wolf', 'bm.frogpet', 'p136/fg/try'),
      'don': ('bm.dncd', 'wolf', 'bm.donado', 'p136/dn/try'),
      'wil': ('bm.wlcd', 'wolf', 'bm.wilfrey', 'p2/wil/try_summon'),
      'fishy': ('bm.fycd', 'wolf', 'bm.fypet', 'p145/try_summon'),
      'dennis': ('bm.dwcd', 'wolf', 'bm.dwpet', 'p163/dw/try_summon'),
      'pistachio': ('bm.picd', 'wolf', 'bm.pipet', 'p163/pi/try_summon'),
      'omega': ('bm.omcd', 'wolf', 'bm.ompet', 'p170/try_summon'),
      'ashur': ('bm.ascd', 'wolf', 'bm.aspet', 'p185/try_summon'),
      'chef': ('bm.kkcd', 'wolf', 'bm.kkpet', 'p186/try_summon'),
      'neighbor': ('bm.nbcd', 'wolf', 'bm.nbpet', 'p187/try_summon'),
      'ava': ('bm.avcd', 'wolf', 'bm.avpet', 'p189/try_summon'), 'pearlq': ('bm.pqcd', 'wolf', 'bm.pqpet', 'p190/try_summon'),
      'bloo': ('bm.bocd', 'wolf', 'bm.bopet', 'p191/try_summon'),
      'stalker': ('bm.svcd', 'wolf', 'bm.svpet', 'p193/try_summon'),
      'lantern': ('bm.lncd', 'wolf', 'bm.lnpet', 'p194/try_summon')}
AR_IDX = {w: i for i, w in enumerate(AR)}
PET_CD = 120                       # a faint outside the vault: 2 minutes (was 5, Wilfrey's 30)
FILTER_MAX = 5

# the summoning items' lore: "5 minutes" after a faint is 2 now (re-synced on the next item version)
for _iid, _d in ITEMS.items():
    _lore = _d.get('comps', {}).get('minecraft:lore')
    if not _lore: continue
    _s = json.dumps(_lore)
    if '5 minutes' in _s and any(w in _s for w in ('faint', 'falls', 'fall,', 'come back', 'return')):
        _d['comps']['minecraft:lore'] = json.loads(_s.replace('5 minutes', '2 minutes'))
# the Vacuum Satchel and the Prime Cooler: what the new controls are
from items import ITEMS as _I
def _relore(iid, lines):
    _I[iid]['comps']['minecraft:lore'] = [T(t, c) if isinstance(t, str) else t for t, c in lines]
_relore('vacuum_satchel', [("A smuggler's bag with a hungry little engine.", 'gray'), ('Right-click: switch it ON or OFF.', 'blue'),
                           ('ON: pulls dropped items within 6 blocks', 'blue'), ('straight into itself (27 slots).', 'blue'),
                           ('Right-click with an item in your other hand:', 'blue'), (f'only that kind is taken (up to {FILTER_MAX} kinds;', 'blue'),
                           ('again with the same item takes it off).', 'gray'),
                           ('Sneak + right-click: it unfolds into a barrel', 'blue'), ('in front of you. Walk away and it folds back up.', 'gray'),
                           ('Every satchel is its own bag.', 'dark_gray')])
_relore('prime_cooler', [('Keeps Prime cuts cold: Prime Beef, Porkchop,', 'blue'), ('Mutton, Chicken and Rabbit.', 'blue'),
                         ('Nothing else goes in - not even plain meat.', 'gray'), ('Right-click: switch its gathering ON or OFF', 'blue'),
                         ('(ON: Prime cuts within 6 blocks fly into it).', 'blue'),
                         ('Sneak + right-click: it unfolds into a barrel (27 slots).', 'blue'), ('Sneak or walk away to pack it up.', 'gray'),
                         ("From Chef Fromage's kitchen.", 'gray')])


def generate(G):
    import phase28 as P28
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    F = G.FUNCS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    objs = ['bm.arof', 'bm.dwlost', 'bm.pilost'] + [f'bm.lf{k}' for k in range(1, 10)] + [f'bm.sp{k}' for k in range(1, 7)]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== THE LEDGER: never dropped in the gutter
    F['loop/fast'].append(f'execute in bm:gutter as @e[type=minecraft:item,distance=0..] if items entity @s contents {holds("fixers_ledger")} run function bm:p173/ledger/bounce')
    fn('p173/ledger/bounce', ['execute on origin run tag @s[type=minecraft:player] add bm.lthr', 'execute unless entity @a[tag=bm.lthr] run return 0',
                              'tp @s @a[tag=bm.lthr,limit=1]', 'data modify entity @s PickupDelay set value 0s',
                              'data modify entity @s Owner set from entity @a[tag=bm.lthr,limit=1] UUID',
                              'execute as @a[tag=bm.lthr] run ' + say('Keep the Ledger on you down here - the Fixer insists.', GOLD),
                              'tag @a[tag=bm.lthr] remove bm.lthr'])

    # ================================================================== THE DARK AUCTION: a night slept through still has its sale
    sch = F['p30/schedule']
    n = 0
    for i, l in enumerate(sch):
        if 'run function bm:p30/doors' in l and 'matches 17000..17999' in l:
            sch[i] = l.replace('matches 17000..17999', 'matches 12000..23999'); n += 1
        elif l == 'execute if score #state bm.auc matches 1 if score #tod bm.bm matches ..16999 run function bm:p30/start':
            sch[i] = 'execute if score #state bm.auc matches 1 if score #tod bm.bm matches ..11999 run function bm:p30/start'; n += 1
    assert n == 2, n
    d = F['p30/doors']
    d[:] = [l.replace('First lot at midnight.', 'First lot at midnight - or at daybreak, if the town sleeps through.') for l in d]

    # ================================================================== THE HOLLOW: no griefing while the King lives
    s_ = F['loop/second']
    k = s_.index('execute as @a at @s if dimension bm:hollow_throne run scoreboard players set #inh bm.p2 1')
    s_.insert(k + 1, 'execute in bm:hollow_throne if entity @e[tag=bm.boss_hollow,distance=0..] run scoreboard players set #inh bm.p2 1')
    s_.insert(k + 2, 'execute if score #inh bm.p2 matches 1 if score #mgoff bm.p2 matches 1 run gamerule mob_griefing false')

    # ================================================================== WILFREY'S MENU (sneak + use the locket)
    sel = '@e[type=minecraft:wolf,tag=bm.fsel,limit=1,sort=nearest]'
    mark = ['tag @s add bm.giver', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
            'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if function bm:p20/frog/is_givers run tag @s add bm.fsel']
    unmark = ['tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @s remove bm.giver']
    WC = '#f4f4f4'
    intro = [T('Wilfrey, the Kind Lord', WC, bold=True), T(' - the Keep\'s old master, freed. He follows and fights for you; '
                                                         'right-click him holding a weapon or armour to equip it.', 'gray')]
    dlg = lambda out: P28.multi([T("Wilfrey's Locket", WC, bold=True)], [P28.body(intro, 300)],
                                ([P28.btn(T('Call him over', WC, bold=True), WMENU + 1, width=150), P28.btn(T('Send him home', 'gray'), WMENU + 2, width=150)] if out else
                                 [P28.btn(T('Call Wilfrey', WC, bold=True), WMENU + 4, width=150)]) +
                                [P28.btn(T('Wardrobe', WC, bold=True), WMENU + 3, width=150, tooltip=T('His shield - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn('p173/wil/menu', [f'scoreboard players set @s bm.menu {WMENU}'] + mark +
       ['execute if entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p173/wil/menu_out',
        'execute unless entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p173/wil/menu_in'] + unmark)
    fn('p173/wil/menu_out', [f'dialog show @s {snbt(dlg(True))}'])
    fn('p173/wil/menu_in', [f'dialog show @s {snbt(dlg(False))}'])
    F['p28/act'].append(f'execute if score #act bm.pay matches {WMENU + 1}..{WMENU + 4} run return run function bm:p173/wil/act')
    fn('p173/wil/act', [f'execute unless score @s bm.menu matches {WMENU} run return run function bm:p28/stale',
                        f'execute if score #act bm.pay matches {WMENU + 3} run return run function bm:p119/plain/wil'] + mark +
       [f'execute if score #act bm.pay matches {WMENU + 1} if entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p2/wil/recall',
        f'execute if score #act bm.pay matches {WMENU + 2} if entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p2/wil/dismiss',
        f'execute if score #act bm.pay matches {WMENU + 4} unless entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p2/wil/try_summon',
        f'execute if score #act bm.pay matches {WMENU + 4} if entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p2/wil/recall'] + unmark)

    # ================================================================== FOLLOWERS: a 2-minute faint, and back by themselves
    cds = {v[0] for v in AR.values()}
    nset = 0
    for name, L in F.items():
        for i, l in enumerate(L):
            for cd in cds:
                if re.search(rf'scoreboard players set \S+ {re.escape(cd)} 300$', l):
                    L[i] = l[:-3] + str(PET_CD); nset += 1
                    for j, m in enumerate(L):            # (the line that says how long, beside it)
                        if '5 minutes' in m: L[j] = m.replace('5 minutes', '2 minutes')
                        if 'In 5 minutes' in m: L[j] = m.replace('In 5 minutes', 'In 2 minutes')
    assert nset >= 14, nset
    # (the vault's 45 seconds: a faint "just now" was 300 down to 290 - with 120 it's 120 down to 110)
    cdl = F['p101/cd']
    cdl[:] = [l.replace(' matches 290.. ', f' matches {PET_CD - 10}.. ') for l in cdl]
    assert all(f' matches {PET_CD - 10}.. ' in l for l in cdl), cdl
    # waiting: a faint outside the gutter marks the player; when the rest is over (and they haven't switched it off), the call
    second = []
    for w, (cd, typ, tag, call) in AR.items():
        i = AR_IDX[w]
        assert call in F, call
        second += [f'execute as @a[tag=!bm.arw{i}] at @s unless dimension bm:gutter if score @s {cd} matches {PET_CD - 10}.. run tag @s add bm.arw{i}',
                   f'execute as @a[tag=bm.arw{i}] unless score @s {cd} matches 1.. at @s run function bm:p173/ar/back_{i}']
        fn(f'p173/ar/back_{i}', [f'tag @s remove bm.arw{i}', 'execute if dimension bm:gutter run return 0',
                                 'execute unless score @s bm.arof matches 0.. run scoreboard players set @s bm.arof 0',
                                 f'scoreboard players operation #q bm.rng = @s bm.arof', f'scoreboard players set #bit bm.rng {2 ** i}',
                                 'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                                 'execute if score #q bm.rng matches 1 run return 0',
                                 'scoreboard players operation #me bm.pid = @s bm.pid',
                                 f'execute as @e[type=minecraft:{typ},tag={tag}] if score @s bm.pid = #me bm.pid run return 0',
                                 f'function bm:{call}'])
        # (the Frog and Donado come back owed a free return at their hut: no need, they're back)
    F['loop/second'] += second
    import phase99 as P99
    F['p28/act'].append(f'execute if score #act bm.pay matches {AR_CODE}..{AR_CODE + len(AR) - 1} run return run function bm:p173/ar/act')
    fn('p173/ar/act', [f'execute if score #act bm.pay matches {AR_CODE + i} run return run function bm:p173/ar/t_{i}' for w, i in AR_IDX.items()])
    for w, i in AR_IDX.items():
        fn(f'p173/ar/t_{i}', [f'execute unless score @s bm.menu matches {P99.BASE[w]} run return run function bm:p28/stale',
                              'execute unless score @s bm.arof matches 0.. run scoreboard players set @s bm.arof 0',
                              'scoreboard players operation #q bm.rng = @s bm.arof', f'scoreboard players set #bit bm.rng {2 ** i}',
                              'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                              f'execute if score #q bm.rng matches 0 run scoreboard players add @s bm.arof {2 ** i}',
                              f'execute if score #q bm.rng matches 1 run scoreboard players remove @s bm.arof {2 ** i}',
                              'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.2', f'function bm:p99/menu/{w}'])

    # ================================================================== DENNIS AND PISTACHIO: the summoning item, earned
    import phase163 as P163
    for k, art in (('dw', 'dw'), ('ps', 'pi')):
        click = F[f'p162/{k}/npc/click']
        line = f'execute if entity @s[tag=bm.{art}met] run function bm:p163/{art}/reissue'
        assert line in click, (k, click)
        click.remove(line)
        F[f'p162/{k}/traded'].append(f'execute if entity @s[tag=bm.{art}met] run function bm:p173/lost/{art}')
        iid = P163.F_[art]['item']
        has = [f'execute if items entity @s container.* {holds(iid)} run scoreboard players set #has bm.rng 1',
               f'execute if items entity @s weapon.offhand {holds(iid)} run scoreboard players set #has bm.rng 1',
               f'execute if items entity @s enderchest.* {holds(iid)} run scoreboard players set #has bm.rng 1',
               'scoreboard players operation #me bm.pid = @s bm.pid',
               f'execute as @e[type=minecraft:wolf,tag=bm.{art}pet] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1']
        who = {'dw': 'Dennis', 'pi': 'Pistachio'}[art]
        thing = ITEMS[iid]['name']
        fn(f'p173/lost/{art}', ['scoreboard players set #has bm.rng 0'] + has +
           [f'execute if score #has bm.rng matches 1 run return run scoreboard players set @s bm.{art}lost 0',
            f'scoreboard players add @s bm.{art}lost 1',
            f'execute if score @s bm.{art}lost matches 50.. run return run function bm:p173/lost/{art}_give',
            f'scoreboard players set #n bm.rng 50', f'scoreboard players operation #n bm.rng -= @s bm.{art}lost',
            title('@s', 'actionbar', [T(f'No {thing}? ', 'gray'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white'},
                                      T(f' more trades and {who} trusts you with another.', 'gray')])])
        fn(f'p173/lost/{art}_give', [f'scoreboard players set @s bm.{art}lost 0', f'function bm:p163/{art}/reissue'])

    # ================================================================== THE PRIME COOLER: on / off
    cool = holds('prime_cooler')
    uc = F['p148/use/cooler']
    k = next(i for i, l in enumerate(uc) if l == 'execute if score #hand bm.rng matches 0 run return 0')
    uc[k + 1:] = ['execute if predicate bm:p20/sneaking if score #hand bm.rng matches 1 run return run function bm:p33/box/open {path:"SelectedItem",slot:"weapon.mainhand",name:"Prime Cooler",kind:"cool"}',
                  'execute if predicate bm:p20/sneaking run return run function bm:p33/box/open {path:"equipment.offhand",slot:"weapon.offhand",name:"Prime Cooler",kind:"cool"}',
                  'execute if score #hand bm.rng matches 1 if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_coff:1b}] run return run function bm:p173/cool/on {slot:"weapon.mainhand"}',
                  'execute if score #hand bm.rng matches 2 if items entity @s weapon.offhand *[minecraft:custom_data~{bm_coff:1b}] run return run function bm:p173/cool/on {slot:"weapon.offhand"}',
                  'execute if score #hand bm.rng matches 1 run return run function bm:p173/cool/off {slot:"weapon.mainhand"}',
                  'function bm:p173/cool/off {slot:"weapon.offhand"}']
    G.wjson('bm/item_modifier/p173/cool_off.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_coff:1b}'},
                                                     {'function': 'minecraft:set_components', 'components': {'minecraft:enchantment_glint_override': False}}])
    G.wjson('bm/item_modifier/p173/cool_on.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_coff:0b}'},
                                                    {'function': 'minecraft:set_components', 'components': {'minecraft:enchantment_glint_override': True}}])
    fn('p173/cool/on', ['$item modify entity @s $(slot) bm:p173/cool_on', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.6 1.6',
                        say('Prime Cooler: ON - Prime cuts nearby fly into it.', '#8ad8ff')])
    fn('p173/cool/off', ['$item modify entity @s $(slot) bm:p173/cool_off', 'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.6 1.6',
                         say('Prime Cooler: OFF.', 'gray')])
    lf = F['loop/fast']
    k = next(i for i, l in enumerate(lf) if l.endswith('run function bm:p148/cool/pull'))
    lf[k] = lf[k].replace(f'if items entity @s container.* {cool} ', 'if function bm:p173/cool/any_on ', 1)
    assert 'p173/cool/any_on' in lf[k], lf[k]
    pull = F['p148/cool/pull']
    pull[:] = [re.sub(r' if items entity @s container\.(\d+) (\S+) run', lambda m: f' if items entity @s container.{m.group(1)} {m.group(2)} unless items entity @s '
                      f'container.{m.group(1)} *[minecraft:custom_data~{{bm_coff:1b}}] run', l) for l in pull]
    assert sum('bm_coff' in l for l in pull) == 36, pull
    fn('p173/cool/any_on', [f'execute if items entity @s container.* {cool} unless items entity @s container.* *[minecraft:custom_data~{{bm_coff:1b}}] run return 1'] +
       [f'execute if items entity @s container.{n} {cool} unless items entity @s container.{n} *[minecraft:custom_data~{{bm_coff:1b}}] run return 1' for n in range(36)] + ['return 0'])

    # ================================================================== THE VACUUM SATCHEL: its own bag, a filter
    # (phase44's per-player store overrode phase33's own-bag satchel: phase33's functions come back, the store moves into the bag)
    import phase33 as P33
    for name in ('p33/vac/use', 'p33/vac/pull', 'p33/vac/read', 'p33/vac/write'):
        F[name] = list(P33.SATCHEL[name])
    use = F['p33/vac/use']
    k = next(i for i, l in enumerate(use) if l == 'execute if score #hand bm.rng matches 0 run return 0')
    use[k + 1:k + 1] = ['function bm:p173/vac/migrate', 'data modify storage bm:tmp vfid set value ""',
                        'execute if score #hand bm.rng matches 1 run data modify storage bm:tmp vfid set from entity @s equipment.offhand.id',
                        'execute if score #hand bm.rng matches 2 run data modify storage bm:tmp vfid set from entity @s SelectedItem.id',
                        'execute unless predicate bm:p20/sneaking if score #hand bm.rng matches 1 if items entity @s weapon.offhand * unless items entity @s weapon.offhand *[minecraft:custom_data~{bm:"vacuum_satchel"}] run return run function bm:p173/vac/flt {hand:"weapon.mainhand",path:"SelectedItem"}',
                        'execute unless predicate bm:p20/sneaking if score #hand bm.rng matches 2 if items entity @s weapon.mainhand * unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"vacuum_satchel"}] run return run function bm:p173/vac/flt {hand:"weapon.offhand",path:"equipment.offhand"}']
    # the old store (bm:vac v<pid>) moves into the satchel in your hand, once - if that one's empty
    fn('p173/vac/migrate', ['execute unless score @s bm.pid matches 1.. run return 0', 'data modify storage bm:tmp vm set value {}',
                            'execute store result storage bm:tmp vm.pid int 1 run scoreboard players get @s bm.pid',
                            'execute if score #hand bm.rng matches 1 run data modify storage bm:tmp vm.slot set value "weapon.mainhand"',
                            'execute if score #hand bm.rng matches 1 run data modify storage bm:tmp vm.path set value "SelectedItem"',
                            'execute if score #hand bm.rng matches 2 run data modify storage bm:tmp vm.slot set value "weapon.offhand"',
                            'execute if score #hand bm.rng matches 2 run data modify storage bm:tmp vm.path set value "equipment.offhand"',
                            'function bm:p173/vac/migrate_m with storage bm:tmp vm'])
    fn('p173/vac/migrate_m', ['$execute unless data storage bm:vac v$(pid)[0] run return 0',
                              '$execute if data entity @s $(path).components."minecraft:container"[0] run return 0',
                              '$data modify storage bm:tmp vm.c set from storage bm:vac v$(pid)', '$data remove storage bm:vac v$(pid)',
                              'function bm:p173/vac/migrate_w with storage bm:tmp vm',
                              say('Your satchel\'s old contents are in this bag now - every satchel is its own bag.', '#c8a050')])
    fn('p173/vac/migrate_w', ['$item modify entity @s $(slot) {function:"minecraft:set_components",components:{"minecraft:container":$(c)}}'])
    # the filter: right-click with an item in the other hand - added (up to five), or taken off again
    fn('p173/vac/flt', ['$data modify storage bm:tmp vf set value {hand:"$(hand)"}',
                        'data modify storage bm:tmp vf.id set from storage bm:tmp vfid',
                        'data modify storage bm:tmp vf.list set value []',
                        '$data modify storage bm:tmp vf.list set from entity @s $(path).components."minecraft:custom_data".bm_flt',
                        'function bm:p173/vac/flt_m with storage bm:tmp vf'])
    fn('p173/vac/flt_m', ['$execute if data storage bm:tmp vf.list[{id:"$(id)"}] run return run function bm:p173/vac/flt_off with storage bm:tmp vf',
                          f'execute if data storage bm:tmp vf.list[{FILTER_MAX - 1}] run return run ' + say(f'The satchel\'s filter is full ({FILTER_MAX} kinds). Use it with one of them to take it off.', '#c8a050'),
                          '$data modify storage bm:tmp vf.list append value {id:"$(id)"}', 'function bm:p173/vac/flt_set with storage bm:tmp vf',
                          'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.4',
                          '$' + title('@s', 'actionbar', [T('Vacuum Satchel: now takes ', '#c8a050'), T('$(id)', 'white'), T(' (only what its filter lists).', '#c8a050')])])
    fn('p173/vac/flt_off', ['$data remove storage bm:tmp vf.list[{id:"$(id)"}]', 'function bm:p173/vac/flt_set with storage bm:tmp vf',
                            'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 1.0',
                            'execute unless data storage bm:tmp vf.list[0] run return run ' + say('Vacuum Satchel: filter cleared - it takes anything again.', '#c8a050'),
                            '$' + title('@s', 'actionbar', [T('Vacuum Satchel: ', '#c8a050'), T('$(id)', 'white'), T(' off its filter.', '#c8a050')])])
    fn('p173/vac/flt_set', ['data modify storage bm:tmp vf.w set value {}', 'data modify storage bm:tmp vf.w.l set from storage bm:tmp vf.list',
                            'function bm:p173/vac/flt_w with storage bm:tmp vf.w'])
    fn('p173/vac/flt_w', ['$execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"vacuum_satchel"}] run item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:{bm_flt:$(l)}}',
                                           '$execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"vacuum_satchel"}] run item modify entity @s weapon.offhand {function:"minecraft:set_custom_data",tag:{bm_flt:$(l)}}'])
    # the pick-up: with a filter, only what it lists
    pl = F['p33/vac/pull']
    k = next(i for i, l in enumerate(pl) if l.startswith('function bm:p33/vac/read with storage bm:tmp vac'))
    pl.insert(k + 1, 'function bm:p173/vac/flt_read with storage bm:tmp vac')
    k = next(i for i, l in enumerate(pl) if 'run function bm:p33/vac/take' in l)
    pl[k] = pl[k].replace(' at @s run function bm:p33/vac/take', ' if function bm:p173/vac/ok at @s run function bm:p33/vac/take')
    fn('p173/vac/flt_read', ['data modify storage bm:tmp vac.f set value []',
                             '$data modify storage bm:tmp vac.f set from entity @s Inventory[{Slot:$(n)b}].components."minecraft:custom_data".bm_flt'])
    fn('p173/vac/ok', ['execute unless data storage bm:tmp vac.f[0] run return 1', 'data modify storage bm:tmp vfo set value {}',
                       'data modify storage bm:tmp vfo.id set from entity @s Item.id', 'return run function bm:p173/vac/ok_m with storage bm:tmp vfo'])
    fn('p173/vac/ok_m', ['$execute if data storage bm:tmp vac.f[{id:"$(id)"}] run return 1', 'return 0'])
    # (phase44's own barrel from before 2.82t still closes into the old store - and that moves into the bag at the next use;
    #  its opening is gone)
    for f_ in ('p44/vac/open', 'p44/vac/try', 'p44/vac/c2i', 'p44/vac/migrate', 'p44/vac/spill', 'p44/vac/spill1', 'p44/vac/close_mine',
               'p44/vac/check', 'p44/vac/close', 'p44/vac/close_m', 'p44/vac/i2c', 'p148/broke/vac'):
        F.pop(f_)
    for lp in ('tick', 'loop/second'):
        n_ = len(F[lp]); F[lp][:] = [l for l in F[lp] if 'tag=bm.vacm]' not in l]; assert len(F[lp]) == n_ - 1, lp

    # ================================================================== BOX BARRELS BROKEN WHILE OUT: everything goes back in
    F['loop/fast'].append('execute as @e[type=minecraft:marker,tag=bm.bxm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p173/box/broke')
    fn('p173/box/broke', ['scoreboard players operation #own bm.pid = @s bm.pid', 'scoreboard players set #on bm.rng 0',
                          'execute as @a if score @s bm.pid = #own bm.pid run scoreboard players set #on bm.rng 1',
                          'execute if score #on bm.rng matches 0 run return 0',
                          'data modify storage bm:tmp bxk set value []', 'scoreboard players set #bs bm.rng 0',
                          'execute as @e[type=minecraft:item,distance=..1.6] if function bm:p173/box/fresh run function bm:p173/box/grab',
                          'setblock ~ ~ ~ minecraft:barrel[facing=up]', 'data modify block ~ ~ ~ Items set from storage bm:tmp bxk',
                          'function bm:p33/box/close'])
    fn('p173/box/fresh', ['execute store result score #age bm.rng run data get entity @s Age', 'execute if score #age bm.rng matches ..30 run return 1', 'return 0'])
    fn('p173/box/grab', ['execute if items entity @s contents minecraft:barrel unless items entity @s contents *[minecraft:custom_data] run return run kill @s',
                         'execute if score #bs bm.rng matches 27.. run return 0',
                         'data modify storage bm:tmp bxe set from entity @s Item', 'execute store result storage bm:tmp bxe.Slot byte 1 run scoreboard players get #bs bm.rng',
                         'data modify storage bm:tmp bxk append from storage bm:tmp bxe', 'scoreboard players add #bs bm.rng 1', 'kill @s'])

    # ================================================================== APOPHISS: fire is his bane
    F['tick'].append('execute as @e[type=minecraft:husk,tag=bm.apboss] if data entity @s {HurtTime:10s} at @s run function bm:p173/apo/hurt')
    fn('p173/apo/hurt', ['scoreboard players set #fire bm.rng 0',
                         'execute on attacker if entity @s[tag=bm.cecilpet,scores={bm.cpel=1}] run scoreboard players set #fire bm.rng 1',
                         'execute on attacker if entity @s[tag=bm.cecilpet,scores={bm.cpel=11}] run scoreboard players set #fire bm.rng 1',
                         'execute on attacker if entity @s[tag=bm.kxpet,scores={bm.kxel=1}] run scoreboard players set #fire bm.rng 1',
                         'execute on attacker if entity @s[tag=bm.kxpet,scores={bm.kxel=11}] run scoreboard players set #fire bm.rng 1',
                         'execute if score #fire bm.rng matches 0 run return 0',
                         'execute store result score #h bm.rng run data get entity @s Health',
                         'execute if score #h bm.rng matches ..9 run return 0',
                         'scoreboard players remove #h bm.rng 8', 'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng',
                         'execute at @s run particle minecraft:flame ~ ~2 ~ 0.8 1.2 0.8 0.05 30',
                         'execute at @s run playsound minecraft:entity.blaze.hurt hostile @a[distance=..32] ~ ~ ~ 0.8 0.6'])

    # ================================================================== THE LUCKY MAP PIECES AND THE SKIFF PARTS: what you carry, every second
    import phase35 as P35
    # (in the gutter your things wait at the coat check: what you carried walking in still counts - the scores hold there)
    F['loop/second'].append('execute as @a at @s unless dimension bm:gutter run function bm:p173/carry')
    fn('p173/carry', [f'execute store success score @s bm.lf{k} if items entity @s container.* {holds(f"lucky_fragment_{k}")}' for k in range(1, 10)] +
       [f'execute store success score @s bm.sp{k} if items entity @s container.* {holds(p)}' for k, (p, _n, _s) in enumerate(P35.PARTS, 1)])
    G.P173_CARRY = {**{f'lucky_fragment_{k}': f'bm.lf{k}' for k in range(1, 10)}, **{p: f'bm.sp{k}' for k, (p, _n, _s) in enumerate(P35.PARTS, 1)}}

    # ================================================================== A HEIST WIN: now and then, a Lucky Map piece in the haul (more, higher up)
    G.wjson('bm/loot_table/p173/win_frag.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry(f'lucky_fragment_{k}') for k in range(1, 10)]}]})
    HA, HB = '-200 64 -197', '-198 64 -197'                  # (the haul barrels - phase101, as the Skiff part)
    hl = F['p70/haul']
    kp = hl.index('function bm:p74/haul_pack')
    hl[kp:kp] = ['execute store result score #r bm.rng run random value 1..100',
                 'scoreboard players operation #fc bm.rng = #gt bm.rng', 'scoreboard players operation #fc bm.rng *= #2 bm.rng',
                 'scoreboard players add #fc bm.rng 4',                                  # I 6%, II 8%, III 10%, IV 12%, V 14%
                 'execute if score #r bm.rng <= #fc bm.rng run function bm:p173/win_frag']
    fn('p173/win_frag', [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:p173/win_frag',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:p173/win_frag',
                         tellraw('@s', PREFIX + [T('Lucky! ', '#e8c547', bold=True), T('A ', 'gray'), T('Lucky Map Fragment', '#e8c547', bold=True),
                                                 T(' turned up in your haul.', 'gray')])])
    fn('admin/frag_haul', ['function bm:p173/win_frag'])

    # ================================================================== EVERY KIT A BACKUP BOW (2.82t): nobody soft-locked by a monster out of reach
    # (a plain bow with Infinity and its one arrow - the Ranged kit's Fairy Bow stays the one that hurts)
    import phase72 as P72
    bow = [f'give @s {P72.kit_arg("minecraft:bow", extra={"minecraft:enchantments": {"minecraft:infinity": 1}})} 1',
           f'give @s {P72.kit_arg("minecraft:arrow")} 1']
    nk = 0
    for k in list(F):
        m = re.fullmatch(r'p80/kit/give_([124])_\d+', k)
        if not m: continue
        L = F[k]; i = L.index('function bm:p80/kit/extras')
        L[i:i] = bow; nk += 1
    assert nk >= 12, nk

    # ================================================================== ONE CREW (2.82t): in the gutter - den, lounge, heists - nobody hurts a crewmate
    # (everyone there shares a team with friendly fire off; out again, a party member is back on their party's team)
    F['load'][-1:-1] = ['team add bm.gvcrew', 'team modify bm.gvcrew friendlyFire false', 'team modify bm.gvcrew seeFriendlyInvisibles true']
    F['loop/second'].append('execute as @a[team=!bm.gvcrew] at @s if dimension bm:gutter run team join bm.gvcrew @s')
    F['loop/second'].append('execute as @a[team=bm.gvcrew] at @s unless dimension bm:gutter run function bm:p173/crew_out')
    fn('p173/crew_out', ['team leave @s', 'execute if score @s bm.pty matches 1.. run function bm:p67/join_team'])

    # ================================================================== THE SALAMANDER SALVE ON YOUR FOLLOWERS TOO (2.82t)
    import phase98 as P98
    pets = sorted({(v[3], v[4]) for v in P98.CALLED if v[3] and v[4]} | {('wolf', v[3]) for v in P98.HIRED})
    F['loop/second'] += [f'execute as @e[type=minecraft:{h},tag={t}] if function bm:p173/salve_owner run effect give @s minecraft:fire_resistance 3 0 true'
                         for h, t in pets]
    fn('p173/salve_owner', ['execute on owner if entity @s[tag=bm.gvfire] run return 1', 'return 0'])

    # ================================================================== A BIG RIG'S HOST LEFT WITHOUT ITS MODEL (2.82t)
    # (Apophiss and the others built the same way: if the model fades - a faint the rig decided on - while the host lives on, that
    #  invisible host still counted as him, so a heist's crew never called him back. Three seconds bare, and the host goes too)
    import phase95 as FX
    F['load'][-1:-1] = ['scoreboard objectives add bm.orph dummy']
    G.OBJECTIVES += ['bm.orph']
    nor = 0
    for k in ('apo', 'tul', 'fishy', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern'):
        if k not in FX.FOLK: continue
        host, tag, head = FX.FOLK[k][:3]
        anyhead = re.sub(r',tag=!bm\.\w+fade', '', head)
        F['loop/second'].append(f'execute as @e[type={host},tag={tag}] at @s run function bm:p173/orph/{k}')
        fn(f'p173/orph/{k}', ['scoreboard players operation #me bm.pid = @s bm.pid',
                              f'execute if function bm:p173/orph/{k}_has run return run scoreboard players set @s bm.orph 0',
                              'scoreboard players add @s bm.orph 1', 'execute if score @s bm.orph matches 3.. run function bm:p173/orph/drop'])
        fn(f'p173/orph/{k}_has', [f'execute as @e[{anyhead},distance=..16] if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
        nor += 1
    assert nor >= 4, nor
    fn('p173/orph/drop', ['execute on passengers run kill @s', 'data remove entity @s Owner', 'tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== HIGH GROUND FOR THE MACE (2.82t): ledges in the fighting rooms, a gallery round the boss
    # (built when the room is set up, only into air: the Counting House, the Arcane Study and the Champion's Pit get four short
    #  wall ledges five blocks up, each with a ladder; the vault's guardian hall gets a two-wide gallery round all four walls)
    import phase70_rooms as RM
    rel = RM.rel
    LEDGE, RAIL = 'minecraft:polished_blackstone_bricks', 'minecraft:gilded_blackstone'
    perch = []
    for z, zin, face in ((1, 2, 'south'), (23, 22, 'north')):
        for x0, x1, lad in ((5, 10, 11), (14, 19, 13)):      # (ladders in the middle gap: the Study's shelves and the Pit's banners line the rest)
            perch += [f'fill {rel(x0, 8, z)} {rel(x1, 8, z)} {LEDGE} replace minecraft:air',
                      f'fill {rel(x0, 8, zin)} {rel(x1, 8, zin)} {RAIL} replace minecraft:air',
                      f'fill {rel(lad, 4, z)} {rel(lad, 8, z)} minecraft:ladder[facing={face}] replace minecraft:air']
    fn('p173/perch', perch)
    # (2.83: a ring round all four walls - the two long strips stopped three blocks short of each end, and the short walls had none.
    #  The ladders go in first, so the ledge leaves each one its gap at the top.)
    gallery = []
    for z, face in ((1, 'south'), (23, 'north')):
        gallery += [f'fill {rel(3, 4, z)} {rel(3, 9, z)} minecraft:ladder[facing={face}] replace minecraft:air',
                    f'fill {rel(21, 4, z)} {rel(21, 9, z)} minecraft:ladder[facing={face}] replace minecraft:air']
    for a, b in (((1, 1), (23, 1)), ((1, 23), (23, 23)), ((1, 1), (1, 23)), ((23, 1), (23, 23))):
        gallery.append(f'fill {rel(a[0], 9, a[1])} {rel(b[0], 9, b[1])} {LEDGE} replace minecraft:air')
    for a, b in (((2, 2), (22, 2)), ((2, 22), (22, 22)), ((2, 2), (2, 22)), ((22, 2), (22, 22))):
        gallery.append(f'fill {rel(a[0], 9, a[1])} {rel(b[0], 9, b[1])} {RAIL} replace minecraft:air')
    fn('p173/perch_vault', gallery)
    for k in ('p70/r/guards/init', 'p76/r/ambush/init', 'p76/r/pit/init'):
        F[k].append('function bm:p173/perch')
    F['p70/r/vault/init'].append('function bm:p173/perch_vault')

    # ================================================================== THE GUTTER'S TRADERS KEEP UP (2.82t)
    # (a trade's cost matches the coin's custom_data exactly, version stamp and all; the market's traders are refreshed when
    #  their list changes (phase17), but the Lounge's Goldtooth, Recruiter and Tailor were summoned once and kept the stamp of
    #  the version that made them - so after an update no coin, Medallion or Insignia would buy anything. Each is now
    #  refreshed from its own summon whenever that list changes.)
    import zlib
    def recipes(line):
        i = line.find('Recipes:[')
        if i < 0: return None
        j = i + len('Recipes:'); depth = 0
        for k in range(j, len(line)):
            depth += line[k] == '['; depth -= line[k] == ']'
            if depth == 0: return line[j:k + 1]
    nfix = 0
    for f, L in list(F.items()):
        for l in L:
            if 'summon minecraft:villager' not in l or 'bm.lgprop' not in l: continue
            m = re.search(r'Tags:\[([^\]]*)\]', l); rec = recipes(l)
            if not m or not rec: continue
            tags = [t.strip('" ') for t in m.group(1).split(',')]
            key = next((t for t in tags if t not in ('bm.npc', 'bm.lgprop', 'bm.gvprop', 'bm.plated', 'bm.seen')), None)
            if not key: continue
            ver = zlib.crc32(rec.encode()) % 1000000000
            k = key.replace('bm.', '')
            fn(f'p173/npcfix/{k}', [f'data modify entity @s Offers.Recipes set value {rec}', f'scoreboard players set @s bm.ofv {ver}'])
            F['loop/second'].append(f'execute in bm:gutter as @e[type=minecraft:villager,tag={key},tag=bm.lgprop,distance=0..] unless score @s bm.ofv matches {ver} run function bm:p173/npcfix/{k}')
            nfix += 1
    assert nfix >= 3, nfix

    # ================================================================== THE WINGS OF THE DAMNED COUNT TOWARD THE REGALIA (2.82t)
    # (both take the chest: with the wings on in place of the Ribcage, the rest of the Regalia still wakes as a full set)
    cq = '*[minecraft:custom_data~{bm_set:"conqueror"}]'
    F['p2/sets/has/conqueror'].insert(0, f'execute if items entity @s armor.chest *[minecraft:custom_data~{{bm:"hollow_wings"}}] '
                                         f'if items entity @s armor.legs {cq} if items entity @s armor.feet {cq} '
                                         f'if items entity @s armor.head *[minecraft:custom_data~{{bm_set:"conqueror"}}] run return 1')
    F['p2/sets/has/conqueror'].insert(1, f'execute if items entity @s armor.chest *[minecraft:custom_data~{{bm:"hollow_wings"}}] '
                                         f'if items entity @s armor.legs {cq} if items entity @s armor.feet {cq} '
                                         f'if items entity @s armor.head *[minecraft:custom_data~{{bm:"apo_unbound_crown"}}] run return 1')

    # ================================================================== A ROOM THAT CLIMBS LIFTS THE LAYOUT WITH IT (2.82t)
    # (the solo stand-in for a crew-only event room drew a Spire without lifting the cursor: the next room sat ten blocks under
    # its exit. Every layout function that places a climbing room must also lift the cursor to its exit.)
    import phase75 as P75
    for f, body in F.items():
        for k, dy in P75.ROOM_DY.items():
            if any(l.endswith(f'function bm:p75/pc/{k}') for l in body):
                assert any(l.endswith(f'tp @s ~ ~{dy} ~') for l in body), f'{f} lays a {k} room but never lifts the cursor {dy} to its exit'

    # ================================================================== the admin's own (for tests)
    fn('admin/ar_off', ['scoreboard players set @s bm.arof 0', say('Every follower comes back after a faint again.', GOLD)])


def finalize(G):
    """After the 26.3 migration: in every loot table, a pool of map pieces (or Skiff parts) takes one you don't carry while there's one."""
    import mig263 as M
    root = G.path('data', 'bm', 'loot_table')
    carry = G.P173_CARRY
    # (a mob's drop asks its killer too; a chest's or a command's has only 'this' - asking more is a load-time warning)
    WHO = {True: ('this', 'attacking_player'), False: ('this',)}
    has = lambda sc: {'type': 'minecraft:any_of', 'terms': [{'type': 'minecraft:entity_scores', 'entity': who, 'scores': {sc: {'min': 1}}}
                                                            for who in WHO[ent]]}
    n_t = n_p = 0
    for dp, _dn, fs in os.walk(root):
        if dp.endswith(os.sep + 'items'): continue
        for f in fs:
            if not f.endswith('.json'): continue
            p = os.path.join(dp, f)
            with open(p) as h: lt = json.load(h)
            hit = False
            ent = lt.get('type', 'minecraft:entity') == 'minecraft:entity'
            for pool in lt.get('pools', []):
                ents = pool.get('entries', [])
                which = [next((i for i in carry if f'bm:\\"{i}\\"' in json.dumps(e)), None) for e in ents]
                if len(ents) < 2 or not all(which): continue
                orig = json.loads(json.dumps(ents))
                for e, iid in zip(ents, which):           # one you don't carry...
                    e['condition'] = M.conds(([e['condition']] if 'condition' in e else []) + [{'type': 'minecraft:inverted', 'term': has(carry[iid])}])
                every = {'type': 'minecraft:all_of', 'terms': [has(carry[iid]) for iid in which]}
                for e in orig:                            # ...or, carrying the whole set, an even draw as before
                    e['condition'] = M.conds(([e['condition']] if 'condition' in e else []) + [every])
                pool['entries'] = ents + orig
                hit = True; n_p += 1
            if hit:
                n_t += 1
                with open(p, 'w') as h: json.dump(lt, h, indent=1, ensure_ascii=False)
    assert n_t >= 6, n_t
    return n_t, n_p
