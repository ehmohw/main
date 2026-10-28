"""2.80b: CECIL'S DOLLS WAIT UNTIL YOU'VE MET THEM.

Cecil sold every follower's doll from the start - KillerWatt's, Apophiss's, Wilfrey's - spoiling followers a player hadn't
found yet. His shop is the trading screen, and a trader has one list for everyone, so the list now follows whoever is at
his counter: the first player within 6 blocks has it until they step away (8 blocks), then the next nearest. A doll for a
follower they have met (held its item - bm:met/<kind>, as the Recruiter uses) is on sale as before; one they haven't is a
sealed "doll still under wraps" in the same place, out of stock. No trade moves, so nothing can be bought by mistake while
the list changes; with no one at the counter every doll is wrapped. Pearlman (his Calling Card) and Wilfrey (his locket)
get their own met/ marks for this."""
from nbt import snbt, B
from items import ITEMS, T

DOLL_KIND = {'doll_cecil': 'cecil', 'doll_celi': 'celi', 'doll_leo': 'leo', 'doll_demo': 'demo', 'doll_kw': 'killerwatt',
             'doll_apo': 'apo', 'doll_tul': 'tul', 'doll_zib': 'zib', 'doll_pearl': 'pearl', 'doll_don': 'donado',
             'doll_wil': 'wil', 'doll_frog': 'frog', 'doll_fishy': 'fishy',
             'doll_dennis': 'dennis', 'doll_pistachio': 'pistachio', 'doll_omega': 'omega', 'doll_ashur': 'ashur', 'doll_chef': 'chef', 'doll_neighbor': 'neighbor', 'doll_ava': 'ava', 'doll_pearlq': 'pearlq', 'doll_bloo': 'bloo', 'doll_stalker': 'stalker', 'doll_lantern': 'lantern', 'doll_bender': 'bender', 'doll_bones': 'bones', 'doll_capshun': 'capshun', 'doll_kettle': 'kettle', 'doll_rufus': 'rufus', 'doll_henry': 'henry', 'doll_nia': 'nia', 'doll_gem': 'gem', 'doll_batty': 'batty', 'doll_eggbert': 'eggbert', 'doll_count': 'count', 'doll_pxcecil': 'pxcecil', 'doll_pxleo': 'pxleo', 'doll_pxemma': 'pxemma', 'doll_sky': 'sky'}
NEW_MET = {'pearl': 'pearl_card', 'wil': 'wilfrey_locket'}


def _span(s, i):
    """the {...} that opens at s[i]: its end (quotes and nesting respected)"""
    d, q, k = 0, False, i
    while k < len(s):
        c = s[k]
        if q:
            if c == '\\': k += 1
            elif c == '"': q = False
        elif c == '"': q = True
        elif c in '{[': d += 1
        elif c in '}]':
            d -= 1
            if d == 0: return k + 1
        k += 1
    raise ValueError('unbalanced')


def _recipes(blob):
    """the top-level recipes of an Offers.Recipes list: [(start, end)]"""
    out, k = [], blob.index('[') + 1
    while True:
        k = blob.find('{', k)
        if k < 0: break
        e = _span(blob, k); out.append((k, e)); k = e
    return out


def generate(G):
    fn = G.fn
    for k, iid in NEW_MET.items():
        assert iid in ITEMS, iid
        crit = {iid: {'trigger': 'minecraft:inventory_changed',
                      'conditions': {'items': [{'items': ITEMS[iid]['base'], 'predicates': {'minecraft:custom_data': snbt({'bm': iid})}}]}}}
        G.wjson(f'bm/advancement/met/{k}.json', {'criteria': crit, 'requirements': [list(crit)]})
    wrapped = snbt({'id': 'minecraft:paper', 'count': 1, 'components': {
        'minecraft:item_model': 'minecraft:barrier',
        'minecraft:item_name': T('A doll still under wraps', 'gray', italic=True),
        'minecraft:lore': [T("Cecil won't say whose it is.", 'dark_gray'), T("Meet them out in the world, and it's yours to buy.", 'dark_gray')],
        'minecraft:custom_data': {'bm_wrapped': B(1)}}})
    # ---- the doll trades' places in each of his lists (his own, and the Lucky Night's)
    lists = {}
    for f, cond in (('p17/npc/wizard', 'unless score #lnight bm.bm matches 1'), ('p52/npc/wizard_lucky', 'if score #lnight bm.bm matches 1')):
        line = next(l for l in G.FUNCS[f] if l.startswith('data modify entity @s Offers.Recipes set value '))
        blob = line[len('data modify entity @s Offers.Recipes set value '):]
        found = {}
        for n, (a, e) in enumerate(_recipes(blob)):
            r = blob[a:e]
            for d in DOLL_KIND:
                if f'bm:"{d}"' in r:
                    s0 = r.index('sell:') + len('sell:'); sell = r[s0:_span(r, s0)]
                    found[d] = (n, sell)
        assert set(found) == set(DOLL_KIND), (f, sorted(set(DOLL_KIND) ^ set(found)))
        lists[cond] = found
    # ---- who is at the counter: the one already there while within 8 blocks, else the nearest within 6
    CH = 30
    NCH = (len(DOLL_KIND) + CH - 1) // CH
    MASK = lambda c: 'bm.dmask' if c == 0 else f'bm.dmask{c}'
    fn('p158/tick', [
        'scoreboard players operation #wdp bm.rng = @s bm.dpid',
        'tag @a remove bm.dcust',
        'execute if score #wdp bm.rng matches 1.. as @a[gamemode=!spectator,distance=..8] if score @s bm.pid = #wdp bm.rng run tag @s add bm.dcust',
        'execute unless entity @a[tag=bm.dcust] as @a[gamemode=!spectator,distance=..6,sort=nearest,limit=1] run tag @s add bm.dcust',
        'execute as @a[tag=bm.dcust] unless score @s bm.pid matches 1.. run function bm:p21/pid',
        'scoreboard players set @s bm.dpid 0',
        'execute as @a[tag=bm.dcust] run scoreboard players operation #wdp bm.rng = @s bm.pid',
        'execute if entity @a[tag=bm.dcust] run scoreboard players operation @s bm.dpid = #wdp bm.rng',
        ] +
       # (2.95d: a bit a doll, thirty to a mask - a score holds 31 bits, and the 32nd follower's would overflow it)
       [f'scoreboard players set #dm{c} bm.rng 0' for c in range(NCH)] +
       [f'execute as @a[tag=bm.dcust,advancements={{bm:met/{k}=true}}] run scoreboard players add #dm{i // CH} bm.rng {1 << (i % CH)}'
        for i, k in enumerate(DOLL_KIND.values())] +
       ['tag @a remove bm.dcust',
        # (unchanged customer, unchanged list: nothing to do)
        'execute ' + ' '.join(f'if score @s {MASK(c)} = #dm{c} bm.rng' for c in range(NCH)) + ' if score @s bm.dofv = @s bm.ofv run return 0'] +
       [f'scoreboard players operation @s {MASK(c)} = #dm{c} bm.rng' for c in range(NCH)] + ['scoreboard players operation @s bm.dofv = @s bm.ofv'] +
       [f'execute {cond} run function bm:p158/apply_{j}' for j, cond in enumerate(lists)])
    for j, (cond, found) in enumerate(lists.items()):
        body = [f'scoreboard players operation #dr{c} bm.rng = #dm{c} bm.rng' for c in range(NCH)]
        # (bit by bit, highest first: #dr >= 2^i means the bit is set; take it off and go on)
        for i, d in reversed(list(enumerate(DOLL_KIND))):
            n, sell = found[d]
            c, b = i // CH, 1 << (i % CH)
            body += [f'execute if score #dr{c} bm.rng matches {b}.. run data modify entity @s Offers.Recipes[{n}].sell set value {sell}',
                     f'execute if score #dr{c} bm.rng matches {b}.. run data modify entity @s Offers.Recipes[{n}].maxUses set value 2147483647',
                     f'execute if score #dr{c} bm.rng matches ..{b - 1} run data modify entity @s Offers.Recipes[{n}].sell set value {wrapped}',
                     f'execute if score #dr{c} bm.rng matches ..{b - 1} run data modify entity @s Offers.Recipes[{n}].maxUses set value 0',
                     f'execute if score #dr{c} bm.rng matches {b}.. run scoreboard players remove #dr{c} bm.rng {b}']
        fn(f'p158/apply_{j}', body)
    G.FUNCS['load'] += [f'scoreboard objectives add {MASK(c)} dummy' for c in range(1, NCH)]
    G.FUNCS['load'] += ['scoreboard objectives add bm.dpid dummy', 'scoreboard objectives add bm.dmask dummy', 'scoreboard objectives add bm.dofv dummy']
    ln = G.FUNCS['loop/second']
    k = max(i for i, l in enumerate(ln) if 'tag=bm.npc_wizard]' in l and 'bm.ofv' in l)
    # (a fresh list - his own or the night's - is wrapped up again the same second: dofv no longer matches)
    # (through a function of its own: never gated with the market chores - a wrapped doll must never show unwrapped)
    ln.insert(k + 1, 'function bm:p158/all')
    fn('p158/all', ['execute as @e[tag=bm.npc_wizard] at @s run function bm:p158/tick'])
