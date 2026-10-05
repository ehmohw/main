"""Phase 2: boss dungeons. Only imported by `gen_dp.py --phase2` (and gen_rp.py --phase2), so the regular
Phase 1.6 build is untouched. Importing registers the Phase 2 items."""
import p2.p2items  # noqa: F401  (registers items)
from p2 import config, logic, bosses, data
from p2.config import D, ORDER
from p2.dungeons import brood

BUILDERS = {'brood': brood.build}
for _name in ('frost', 'tide', 'hex', 'keep', 'hollow', 'lucky'):
    try:
        _m = __import__(f'p2.dungeons.{_name}', fromlist=['build'])
        BUILDERS[_name] = _m.build
    except ModuleNotFoundError:
        pass
BUILT = {}
OBJ = ['bm.conq', 'bm.pz', 'bm.done', 'bm.code', 'bm.klen', 'bm.step', 'bm.pt', 'bm.gs', 'bm.gt', 'bm.seen', 'bm.bs', 'bm.bt',
       'bm.ba', 'bm.at', 'bm.at2', 'bm.acd', 'bm.p2', 'bm.rx', 'bm.ry', 'bm.rz', 'bm.ret', 'bm.wv', 'bm.wt', 'bm.rd', 'bm.wpc', 'bm.wlcd', 'bm.wlg']


def extend_offers(O, offer):
    from p2.p2items import KEYS
    O['fence'] += [offer(price, (f'key_{d}', 1)) for d, (_, _, _, price) in KEYS.items()]
    O['fence'].append(offer(('token', 3), ('sealed_map_brood', 1)))
    # 2.13: every Sealed Map is for sale (a victory still gives the next one free; the conquest order still decides your record)
    O['fence'] += [offer(('token', n), (f'sealed_map_{d}', 1)) for d, n in (('frost', 4), ('tide', 5), ('hex', 6), ('keep', 8))]
    O['lucky'] += [offer(('lucky_trophy', 1), ('fortuna', 1)), offer(('lucky_trophy', 1), ('trophy', 3))]


def builds():
    if not BUILT:
        from p2.kit import arena_probes, shrine
        for d, f in BUILDERS.items():
            BUILT[d] = f()
            shrine(BUILT[d])                  # 2.2 altar shrines (the Hollow Throne builds its own)
            arena_probes(BUILT[d])
    return BUILT


def generate(G):
    B = builds()
    for d, Bd in B.items():
        Bd.export(G.path('data', 'bm', 'structure', f'p2_{d}.nbt'))
    from p2.dungeons import grave
    grave.build().export(G.path('data', 'bm', 'structure', 'p2_wilfrey_grave.nbt'))

    def offers():
        O = G.npc_offers()
        G.P.extend_offers(O, G.offer)
        extend_offers(O, G.offer)
        G.R.extend_offers(O, G.offer)          # Phase 1.7 trades (same order as gen_npcs)
        G.R20.extend_offers(O, G.offer)
        G.R21.extend_offers(O, G.offer)
        G.R33.extend_offers(O, G.offer)
        G.R34.extend_offers(O, G.offer)
        G.R35.extend_offers(O, G.offer)
        G.R36.extend_offers(O, G.offer)
        return O
    from p2 import patch21, trophies, wilfrey
    parts = [logic.generate(G, B), bosses.generate(G, B), data.generate(G, B, offers), patch21.generate(G, B), trophies.generate(G), wilfrey.generate(G)]
    tick = [l for p in parts for l in p.get('tick', [])]
    fast = [l for p in parts for l in p.get('fast', [])] + parts[0]['zone']
    second = [l for p in parts for l in p.get('second', [])]
    load = [l for p in parts for l in p.get('load', [])]

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')        # altars read the sneak counter, so run before it resets
    f[k:k] = fast
    # adventure zones: dungeon players (and anyone in the Hollow Throne) must not be dropped back to survival
    for i, line in enumerate(f):
        if line.endswith('run function bm:zone/exit'):
            f[i] = line.replace(' run function bm:zone/exit',
                                ' unless entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..36] unless dimension bm:hollow_throne run function bm:zone/exit')
    s = G.FUNCS['loop/second']
    s[-1:-1] = ['execute as @a unless score @s bm.conq = @s bm.conq run scoreboard players set @s bm.conq 0',
                'scoreboard players remove @a[scores={bm.acd=1..}] bm.acd 1'] + second
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJ] + [
        'scoreboard players set #3 bm.p2 3', 'scoreboard players set #10 bm.p2 10'] + load
    G.OBJECTIVES += OBJ


def post_admin(G):
    fn, tellraw, T = G.fn, G.tellraw, G.T
    B = builds()
    help_ = [tellraw('@s', [T('— Phase 2 (TEST) —', 'gold')]),
             tellraw('@s', [T('/function bm:admin/p2/place_<dungeon>', 'yellow'), T('  ' + ', '.join(d for d in B if d != 'hollow'), 'gray')]),
             tellraw('@s', [T('/function bm:admin/p2/conquest_<0-6>', 'yellow'), T('  set your conquest record', 'gray')]),
             tellraw('@s', [T('/function bm:admin/p2/reset', 'yellow'), T('  reset the nearest dungeon (re-locks every trial)', 'gray')]),
             tellraw('@s', [T('/function bm:admin/p2/hollow', 'yellow'), T('  go to the Hollow Throne', 'gray')]),
             tellraw('@s', [T('/function bm:admin/p2/shard', 'yellow'), T('  give yourself a Shard of the Hollow Throne (+5 conquests)', 'gray')]),
             tellraw('@s', [T('/locate structure bm:p2_<dungeon>', 'yellow'), T('  find one', 'gray')])]
    G.FUNCS['admin/help'][-1:-1] = help_
    for d in B:
        if d == 'hollow': continue
        fn(f'admin/p2/place_{d}', [f'place template bm:p2_{d} ~ ~ ~',
                                   tellraw('@s', G.PREFIX + [T(f'{D[d]["title"]} placed with its corner at your feet. Natural mob spawning is NOT disabled for admin-placed copies.', 'gray')])])
    for n in range(7):
        fn(f'admin/p2/conquest_{n}', [f'scoreboard players set @s bm.conq {n}', tellraw('@s', G.PREFIX + [T(f'Conquest record set to {n}.', 'gray')])])
    fn('admin/p2/reset', [f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},distance=..160,sort=nearest,limit=1] at @s run function bm:p2/{d}/reset' for d in B] +
       [tellraw('@s', G.PREFIX + [T('Nearest dungeon reset.', 'gray')])])
    fn('admin/p2/shard', ['scoreboard players set @s[scores={bm.conq=..4}] bm.conq 5', 'execute unless score @s bm.conq matches 0.. run scoreboard players set @s bm.conq 5',
                          'loot give @s loot bm:items/hollow_summons'])
    fn('admin/p2/hollow', [f'execute unless score #hver bm.p2 matches {data.HOLLOW_VER} run return run ' + tellraw('@s', G.PREFIX + [T('The Hollow Throne is still being built; try again in a few seconds.', 'gray')]),
                           'function bm:p2/hollow/enter'])
    G.FUNCS['admin/uninstall'][0:0] = [f'bossbar remove bm:boss_{d}' for d in B]
