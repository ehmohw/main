"""2.81: THE BLACK MARKET, REBUILT - every market already in a world becomes the new town (market3.py), once.

WHEN   a market whose bm.mkt marker doesn't carry the town tag (market3.TOWN_TAG; every market built before 2.81,
       and since 2.81a the 2.81 towns too, for their counters) is rebuilt the first time a
       player comes within 200 blocks - unless a Dark Auction is running (it waits for the night to end).
HOW    the market's box (76 x 32 x 98, turned like the market) is force-loaded; once loaded:
       - anyone inside is moved up to the Lookout, by the vault door; anything lying on the floor goes there too;
       - the market's own entities are removed: its traders and their models, the crowd, cushions, neon signs, ledgers,
         Fishy's hall, Dennis's and Pistachio's rooms, the slot machines' reels, the Bounty Board... (every tag the
         market's spawns and installs give - and only those; players' followers, pets and dropped things stay);
       - the new town is placed over the old, with the market's own turn (its marker comes with it, carrying the town tag);
       - the chunks are let go. Every install then runs again on the new marker: gates, back-room ledgers, the Dark
         Auction, the Gilded Gutter, Fishy's Cabinet, Dennis's and Pistachio's rooms, the slot machines, the board, the
         lectern, the lift button. The traders come back from the new template's markers.
       The ladder shaft (beyond the end of the dig-in tunnel) is outside the box: it stays as it is.
       Nothing anyone owns is kept in the market itself: standing, Rat Bank balances, escrow, bounties signed, daily
       limits all live on the players.
       Every per-market install and patch now waits for the town tag, so nothing is placed in an old market before it's
       rebuilt.
ADMIN  /function bm:admin/market_rebuild - the nearest market (within 200 blocks) is rebuilt again."""
import re

import market3
import mgeo
import rot
from items import T


def _cw(x, z, n):
    for _ in range(n % 4): x, z = -z, x
    return x, z


def generate(G):
    fn, tellraw, PREFIX = G.fn, G.tellraw, G.PREFIX
    SX, SY, SZ, W, BF = market3.SX, market3.SY, market3.SZ, market3.W, market3.BF
    rel = mgeo.rel
    TT = market3.TOWN_TAG
    corners_t = [(0, 0), (SX - 1, 0), (0, SZ - 1), (SX - 1, SZ - 1)]
    loaded = ' '.join(f'if loaded {rel((x + 0.5, W, z + 0.5))}' for x, z in corners_t)
    look = rel((38.5, BF + 1, 78.5))
    second = [f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!{TT}] at @s rotated as @s if entity @a[distance=..200] run function bm:p168/tick',
              # (2.83: once its chunks are held it finishes even if the player who came near has gone - else they stayed force-loaded for good)
              f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!{TT},tag=bm.rbfl] at @s rotated as @s unless entity @a[distance=..200] run function bm:p168/tick']
    fn('p168/tick', ['execute if score #state bm.auc matches 1.. run return 0',
                     'execute unless entity @s[tag=bm.rbfl] run function bm:p168/hold',
                     'execute if entity @s[tag=bm.rbfl] run function bm:p168/corners',
                     f'execute {loaded} run function bm:p168/go'])
    turns = [f'execute if entity @s[y_rotation={r}] run return run function bm:p168/%s_{n}' for r, n in rot.TURNS]
    # (2.83: and each corner the tick waits for, itself - for a market turned 180 the box missed one, which never loaded, so the
    #  rebuild never ran and the rest stayed force-loaded)
    corner_at = [f'execute positioned {rel((x + 0.5, W, z + 0.5))} run forceload %s ~ ~' for x, z in corners_t]
    G.P168_CORNERS = corner_at
    # (re-asserted every second while held: a rebuild held by an older version lacks some of these, and waited for good)
    fn('p168/corners', [c % 'add' for c in corner_at] + [t % 'fl' for t in turns])
    fn('p168/hold', ['tag @s add bm.rbfl'] + [c % 'add' for c in corner_at] + [t % 'fl' for t in turns])
    fn('p168/go', [t % 'go' for t in turns])
    ROTN = {0: 'none', 1: 'clockwise_90', 2: '180', 3: 'counterclockwise_90'}
    G.P168_GO = {}
    for n in range(4):
        # the template corner that lands at the world's lowest x and z, and the box's world size from it
        w = [(_cw(x, z, n), (x, z)) for x, z in corners_t]
        mx, mz = min(p[0][0] for p in w), min(p[0][1] for p in w)
        cx, cz = next(t for (wx, wz), t in w if wx == mx and wz == mz)
        dx, dz = (SX - 1, SZ - 1) if n % 2 == 0 else (SZ - 1, SX - 1)
        minc = rel((cx + 0.5, 0.5, cz + 0.5))
        box = f'dx={dx},dy={SY - 1},dz={dz}'
        org = rel((0.5, 0.5, 0.5))
        # (/place template checks the UNturned box from the template's origin is loaded, whatever the turn - load that too)
        fn(f'p168/fl_{n}', [f'execute positioned {minc} run forceload add ~ ~ ~{dx} ~{dz}', f'execute positioned {org} run forceload add ~ ~ ~{SX - 1} ~{SZ - 1}'])
        G.P168_GO[n] = (minc, box, dx, dz)
        fn(f'p168/go_{n}', [])          # (filled in by finalize, once every phase has added its spawns)
    fn('admin/market_rebuild', [f'execute as @e[type=minecraft:marker,tag=bm.mkt,distance=..200,sort=nearest,limit=1] run tag @s remove {TT}',
                                tellraw('@s', PREFIX + [T('The nearest Black Market is rebuilt as soon as its chunks load.', 'gold')])])
    # (2.82: a trader is never invisible - the Fence is a wandering trader, and one carried over from an older market could keep the
    #  invisibility it drank one night for good. 2.82b: except the ones built invisible - the hosts under a model (Cecil, the
    #  Armory, the Chef, Zorp...): cleared, they showed as a plain villager on top of the model. finalize() lists them, from
    #  their own summons; theirs is put back, everyone else's cleared)
    second.append('function bm:p168/invis')
    second.append('execute as @e[type=minecraft:wandering_trader,tag=bm.npc,nbt=!{NoAI:1b}] run data merge entity @s {NoAI:1b}')
    G.FUNCS['loop/second'][0:0] = second
    G.P168_LOOK = look


def finalize(G):
    """After every phase: the tags the market's entities carry, the rebuild itself, and every install waiting for the town tag."""
    F = G.FUNCS
    # (the traders built invisible: a villager or wandering trader summoned with the invisibility effect - its own tag)
    inv_tags = set()
    for _f, L in F.items():
        for l in L:
            if not isinstance(l, str) or 'minecraft:invisibility' not in l: continue
            for m in re.finditer(r'summon minecraft:(villager|wandering_trader) [^{]*\{(.*)', l):
                t = re.search(r'Tags:\[([^\]]*)\]', m.group(2))
                if t:
                    tags = [x.strip().strip('"') for x in t.group(1).split(',')]
                    inv_tags |= {x for x in tags if x.startswith(('bm.npc_', 'bm.frat_')) or x == 'bm.pearl'}
    assert {'bm.npc_wizard', 'bm.npc_chef', 'bm.npc_armory'} <= inv_tags, sorted(inv_tags)
    F['p168/invis'] = ['effect clear @e[type=#bm:p56_traders,tag=bm.npc,predicate=bm:p126/invis' + ''.join(f',tag=!{t}' for t in sorted(inv_tags)) +
                       '] minecraft:invisibility'] + \
                      [f'effect give @e[type=#bm:p56_traders,tag={t},predicate=!bm:p126/invis] minecraft:invisibility infinite 0 true' for t in sorted(inv_tags)]
    TT = market3.TOWN_TAG
    summon = re.compile(r'summon minecraft:([a-z_]+) [^{]*(\{.*\})')
    tagre = re.compile(r'Tags:\[([^\]]*)\]')
    addre = re.compile(r'\btag @[a-z](?:\[[^\]]*\])? add ([a-z0-9_.]+)')
    callre = re.compile(r'function bm:([a-z0-9_/]+)')

    def tags_in(lines):
        out = set()
        for l in lines:
            for m in summon.finditer(l):
                t = tagre.search(m.group(2))
                if t: out |= {x.strip().strip('"') for x in t.group(1).split(',') if x.strip()}
            out |= set(addre.findall(l))
        return out

    def reach(roots):
        seen, todo = set(), [r for r in roots if r in F]
        while todo:
            f = todo.pop()
            if f in seen: continue
            seen.add(f)
            for l in F[f]:
                for c in callre.findall(l):
                    if c in F and c not in seen: todo.append(c)
        return seen
    roots = ['npc/spawn', 'p28/install', 'p35/patch', 'p41/patch', 'p34/patch', 'p51/market', 'p52/market', 'p145/hall/install', 'p162/install',
             'p73/dock', 'p74/lift_build'] + [f for f in F if f.startswith(('p162/dw/npc/', 'p162/ps/npc/', 'p145/npc/', 'p45/cecil/', 'npc/'))]
    mk = reach(roots)
    market_tags = tags_in(l for f in mk for l in F[f])
    for B in (market3.build(),):
        for e in B.ents: market_tags |= set(e['nbt']['Tags'])
    import market2
    for e in market2.build().ents: market_tags |= set(e['nbt']['Tags'])
    other = tags_in(l for f, L in F.items() if f not in mk for l in L)
    transient = {t for t in market_tags if t.endswith('new') or t in ('bm.n18', 'bm.new', 'bm.mkt', 'bm.m281', TT, 'bm.mshaft', 'bm.msdone', 'bm.ms74', 'bm.msnew')}
    shared = (market_tags & other) - transient
    keep_shared = {'bm.npc', 'bm.npc_spawn', 'bm.e18', 'bm.p162prop', 'bm.cabprop'}      # the market's own families (other spawns of them are never in a market)
    kill = sorted((market_tags - transient - shared) | (shared & keep_shared))
    G.P168_KILL, G.P168_SHARED = kill, sorted(shared - keep_shared)
    look = G.P168_LOOK
    for n, (minc, box, dx, dz) in G.P168_GO.items():
        org = mgeo.rel((0.5, 0.5, 0.5)); SX, SZ = market3.SX, market3.SZ
        F[f'p168/go_{n}'] = [
            f'execute positioned {org} unless loaded ~{SX - 1} ~ ~{SZ - 1} run return 0', f'execute positioned {org} unless loaded ~{SX - 1} ~ ~ run return 0',
            f'execute positioned {org} unless loaded ~ ~ ~{SZ - 1} run return 0',
            f'execute positioned {minc} run tag @a[{box},gamemode=!spectator] add bm.rbmove',
            f'execute positioned {minc} run tag @e[type=minecraft:item,{box}] add bm.rbmove',
            f'execute positioned {minc} run tag @e[type=minecraft:experience_orb,{box}] add bm.rbmove',
            f'execute positioned {look} rotated ~180 0 run tp @e[tag=bm.rbmove] ~ ~ ~ ~ ~'] + \
            [f'execute positioned {minc} run kill @e[type=!minecraft:player,tag={t},tag=!bm.mkt,{box}]' for t in kill] + [
            'scoreboard players set #rbok bm.rng 0',
            f'execute positioned {org} store success score #rbok bm.rng run place template bm:black_market ~ ~ ~ {["none", "clockwise_90", "180", "counterclockwise_90"][n]}',
            'execute if score #rbok bm.rng matches 0 run tag @s remove bm.rbfl',
            'execute if score #rbok bm.rng matches 0 run return run tag @e[tag=bm.rbmove] remove bm.rbmove',
            f'execute positioned {minc} run forceload remove ~ ~ ~{dx} ~{dz}', f'execute positioned {org} run forceload remove ~ ~ ~{SX - 1} ~{SZ - 1}'] + \
            [c % 'remove' for c in G.P168_CORNERS] + [
            'tag @e[tag=bm.rbmove] remove bm.rbmove',
            G.tellraw('@a[distance=..120]', G.PREFIX + [T('The Black Market has been rebuilt: ', 'gold'), T('streets, houses, the Lookout - the same traders, gates and rooms.', 'gray')]),
            'kill @s']
    # every per-market install and patch waits for the new town (nothing is placed in an old market before it's rebuilt)
    pats = [('@e[type=minecraft:marker,tag=bm.mkt,tag=!', f'@e[type=minecraft:marker,tag=bm.mkt,tag={TT},tag=!'),
            ('@e[type=minecraft:marker,tag=bm.mkt] at @s rotated as @s', f'@e[type=minecraft:marker,tag=bm.mkt,tag={TT}] at @s rotated as @s'),
            ('@e[type=minecraft:marker,tag=bm.mkt] at @s run', f'@e[type=minecraft:marker,tag=bm.mkt,tag={TT}] at @s run')]
    n_gated = 0
    for name in ['loop/second', 'loop/fast', 'tick'] + [f for f in F if f.endswith('install_check')]:
        L = F[name]
        for i, l in enumerate(L):
            if 'function bm:p168/tick' in l: continue
            for a, b in pats:
                if a in l and f'tag=!{TT}' not in l:
                    L[i] = l = l.replace(a, b); n_gated += 1
    G.P168_GATED = n_gated
    return len(kill), n_gated
