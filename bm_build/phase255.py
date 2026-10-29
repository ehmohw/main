"""3.0a: NOTHING RISES IN THE DEEP - no mob spawns in the Undercrown (phase237) or the Vorn Armada (phase241) but their own: the
combat rooms' foes (trials, waves, guards, spawners, knights, bosses and theirs) and, in the Undercrown only, the Dread Mires
(phase246's p246/uc/*, the Sovereign's own).

THE BIOME    bm:undercrown / bm:armada spawn nothing (natural_mob_spawns overridden empty, no patrols, no raids, no world-gen
             creatures) - and now it is really there: fillbiome is bounded by the max_block_modifications gamerule (32768 blocks,
             counted on the quart-snapped corners) and the builds' 56- and 60-wide columns (~350k blocks each) failed every time,
             leaving the plain Nether / End biome over both boxes. fills() cuts each box into 16 x 16 columns and pads it a quart
             (4 blocks) all round, so the game's biome blur reads the dungeon's biome right up to the box's faces. Worlds placed
             before 3.0a get theirs once (bio/*: the box force-loaded a few seconds, filled, checked at its eight corners, released).
THE SWEEP    once a second, while anyone is in a placed dungeon's box: a monster in it (#bm:p255_wild) that is none of the dungeon's
             own (an allow-list of tags, ALLOW_*; the boxes' rebuild CLEAR lists are folded in) and not someone's (invisible custom-
             mob hosts, persistent mobs - a name tag, a pet, anything the pack made to stay -, an owner, a leash, a player riding it,
             a follower's bm.pid, a dungeon slime's named split) is taken: dropped into the void and killed - nothing drops. In the
             Armada a wild Dread Mire melts away too (the planted, tame ones are their owners').
FIRST SIGHT  mobs/init (every monster the pack rolls: elite / champion / lucky, Blood Moon, invasions, Dread variants, the Mire's
             own roll) starts by taking a bare monster (no tags, no name: a natural spawn) first seen in a placed box - before any of
             those can turn it into something else or call minions.
THE OTHERS   the Mire's natural roll never rises in the Armada; the Stalkers (p181/stk/at), the Vorn invasions' saucers, slimes and
             phantoms (and their troopers, in the Undercrown - the Armada's own reinforcements and Vexis's pods are troopers too),
             and the Arachno-Lantern (p82/summon) never come up inside either box (bm:p255/in_box, a location predicate)."""
import allies
import phase237 as P237
import phase241 as P241

PFX = 'p255'
BIOV = 1                                    # bump to re-fill both boxes' biome in every world (bio/*)
PAD = 4                                     # (one quart round the box: the biome blur samples the neighbouring quarts)
TILE = 16                                   # (a 16 x 16 column: 13 x 121 x 13 blocks after the snap - well under 32768)
LIMIT = 32768                               # (vanilla max_block_modifications; the pack never raises it)

# monsters a box can get by nature (the biome lists, a fortress's, the Nether's and the End's) or by wandering in
WILD = ['zombie', 'husk', 'drowned', 'zombie_villager', 'skeleton', 'stray', 'bogged', 'parched', 'wither_skeleton', 'creeper', 'spider',
        'cave_spider', 'enderman', 'endermite', 'witch', 'slime', 'magma_cube', 'sulfur_cube', 'ghast', 'blaze', 'piglin', 'piglin_brute',
        'zombified_piglin', 'hoglin', 'zoglin', 'strider', 'phantom', 'pillager', 'vindicator', 'evoker', 'illusioner', 'ravager', 'vex',
        'breeze', 'creaking', 'guardian', 'silverfish', 'shulker', 'bat', 'zombie_horse', 'skeleton_horse', 'camel_husk', 'zombie_nautilus']
SPLITS = ['slime', 'magma_cube', 'sulfur_cube']      # (a named slime's children keep its name, never its tags)
# the pack's own, in either box: the player's side (followers ride wolves and cats - not WILD - but hirelings, escorts, a
# necromancer's revenants, the hypnotised), NPCs, bosses
ALLOW_ANY = ['bm.dgmob', 'bm.boss', 'bm.boss_part', 'bm.khost', 'bm.npc', 'bm.hypno', 'bm.revenant', 'bm.mtame'] + allies.ALLIES
# the Undercrown: its trials' and waves' Dread (bm.udread), its echo knights, the Sovereign's knights and eyes, its Mires
ALLOW_U = ['bm.udread', 'bm.ueknight', 'bm.usov', 'bm.svk', 'bm.sveye', 'bm.svm', 'bm.dbecho', 'bm.mire', 'bm.muc']
# the Armada: its Vorn (dressed bm.avorn -> bm.vorn), guards, reinforcements, Vexis and its drones / pods / clones
ALLOW_A = ['bm.avorn', 'bm.aguard', 'bm.vorn', 'bm.vtroop', 'bm.vstay', 'bm.avx', 'bm.vxk', 'bm.vxcl']

DG = {'under': dict(mod=P237, dim='minecraft:the_nether', ver='#uver', VER=P237.UVER, col='#ucol', bio='#ubio', biome='bm:undercrown', allow=ALLOW_U),
      'armada': dict(mod=P241, dim='minecraft:the_end', ver='#aver', VER=P241.AVER, col='#acol', bio='#abio', biome='bm:armada', allow=ALLOW_A)}

# the biome's spawn settings (both dungeons): every one the game reads where it spawns
NO_SPAWNS = {'minecraft:gameplay/natural_mob_spawns': {'argument': {'spawn_costs': {}, 'spawns_by_category': {}}, 'modifier': 'override'},
             'minecraft:gameplay/can_pillager_patrol_spawn': False, 'minecraft:gameplay/can_start_raid': False,
             'minecraft:gameplay/nether_portal_spawns_piglin': False, 'minecraft:gameplay/creature_world_gen_spawn_probability': 0.0}


def _q(v):
    return v // 4 * 4


def fills(dim, origin, size, biome, done=None):
    """fillbiome lines over a box (and PAD round it), each within the block limit; then `done` (holder, value) is set"""
    (ox, oy, oz), (sx, sy, sz) = origin, size
    x0, y0, z0, x1, y1, z1 = ox - PAD, oy - PAD, oz - PAD, ox + sx - 1 + PAD, oy + sy - 1 + PAD, oz + sz - 1 + PAD
    out = []
    for bx in range(x0, x1 + 1, TILE):
        for bz in range(z0, z1 + 1, TILE):
            ex, ez = min(x1, bx + TILE - 1), min(z1, bz + TILE - 1)
            vol = (_q(ex) - _q(bx) + 1) * (_q(y1) - _q(y0) + 1) * (_q(ez) - _q(bz) + 1)
            assert vol <= LIMIT, f'fillbiome {bx} {y0} {bz} .. {ex} {y1} {ez}: {vol} blocks > {LIMIT}'
            out.append(f'execute in {dim} run fillbiome {bx} {y0} {bz} {ex} {y1} {ez} {biome}')
    if done: out.append(f'scoreboard players set {done[0]} bm.p2 {done[1]}')
    return out


def box_of(M):
    return (M.OX, M.OY, M.OZ), (M.SX, M.SY, M.SZ)


def quarters(M):
    """the build's own forceload: the box and an 8-block margin, in four quarters (at most 256 chunks a command)"""
    mx, mz = M.OX + M.SX // 2, M.OZ + M.SZ // 2
    return [f'{a} {b} {c} {d}' for a, c in ((M.OX - 8, mx), (mx + 1, M.OX + M.SX + 8)) for b, d in ((M.OZ - 8, mz), (mz + 1, M.OZ + M.SZ + 8))]


def selector(key):
    """the sweep's: a monster in the box that is none of the dungeon's own (before the per-mob checks in p255/cull)"""
    c = DG[key]
    M = c['mod']
    tags = list(dict.fromkeys(ALLOW_ANY + c['allow'] + [t[4:] for s in M.CLEAR for t in s.split(',') if t.startswith('tag=') and not t.startswith('tag=!')]))
    if key == 'armada': tags = [t for t in tags if t != 'bm.mire']          # (no Mire is the Armada's own)
    return f'@e[type=#bm:{PFX}_wild,{M.BOX},' + ','.join(f'tag=!{t}' for t in tags) + ',predicate=!bm:p44/invis]'


def generate(G):
    """-> (functions patched to keep out of the boxes, mobs/init functions guarded)"""
    fn, wjson = G.fn, G.wjson
    second = G.FUNCS['loop/second']
    import json as _json
    # ---- the biomes: nothing spawns (phase237 / phase241 wrote them with NO_SPAWNS - checked as written)
    for key, c in DG.items():
        b = _json.load(open(G.path('data', 'bm', 'worldgen', 'biome', c['biome'].split(':')[1] + '.json')))
        a = b.get('attributes', {})
        ns = a.get('minecraft:gameplay/natural_mob_spawns', {})
        assert ns.get('modifier') == 'override' and ns.get('argument') == {'spawn_costs': {}, 'spawns_by_category': {}}, f'{c["biome"]}: it spawns: {ns}'
        for k, v in NO_SPAWNS.items():
            assert a.get(k) == v, f'{c["biome"]}: {k} is {a.get(k)!r}, not {v!r}'
        bt = G.FUNCS[f'{c["mod"].__name__.replace("phase", "p")}/build/try']
        n = sum(1 for l in bt if ' fillbiome ' in l)
        assert n == len(fills(c['dim'], *box_of(c['mod']), c['biome'])), f'{key}: build/try has {n} fillbiome lines, not fills()\'s'
        assert f'scoreboard players set {c["bio"]} bm.p2 {BIOV}' in bt, f'{key}: build/try never marks its biome filled'
    wjson(f'bm/tags/entity_type/{PFX}_wild.json', {'values': [f'minecraft:{t}' for t in WILD]})
    wjson(f'bm/tags/entity_type/{PFX}_splits.json', {'values': [f'minecraft:{t}' for t in SPLITS]})
    loc = {}
    for key, c in DG.items():
        M = c['mod']
        loc[key] = {'condition': 'minecraft:location_check', 'predicate': {'dimension': c['dim'], 'position': {
            'x': {'min': float(M.OX), 'max': float(M.OX + M.SX)}, 'y': {'min': float(M.OY), 'max': float(M.OY + M.SY)},
            'z': {'min': float(M.OZ), 'max': float(M.OZ + M.SZ)}}}}
        wjson(f'bm/predicate/{PFX}/in_{key}.json', loc[key])
    wjson(f'bm/predicate/{PFX}/in_box.json', {'condition': 'minecraft:any_of', 'terms': list(loc.values())})
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #ubgu bm.p2 0', 'scoreboard players set #abgu bm.p2 0', 'scoreboard players set #ubw bm.p2 0',
                              'scoreboard players set #abw bm.p2 0']

    # ---- the biome, once, in a world placed before it took (the box force-loaded, filled, checked at its corners, released)
    for key, c in DG.items():
        M, dim, k = c['mod'], c['dim'], key[0]
        fl = quarters(M)
        (ox, oy, oz), (sx, sy, sz) = box_of(M)
        corners = [(x, y, z) for x in (ox, ox + sx - 1) for y in (oy, oy + sy - 1) for z in (oz, oz + sz - 1)]
        second.append(f'execute if score {c["ver"]} bm.p2 matches {c["VER"]} unless score {c["bio"]} bm.p2 matches {BIOV} '
                      f'unless score {c["col"]} bm.p2 matches 1.. unless score #{k}bgu bm.p2 matches 20.. run function bm:{PFX}/bio/{key}')
        fn(f'{PFX}/bio/{key}', [*[f'execute in {dim} run forceload add {q}' for q in fl],
                                f'execute in {dim} store success score #{k}bl bm.rng if loaded {ox} {oy} {oz} if loaded {ox + sx - 1} {oy} {oz + sz - 1} '
                                f'if loaded {ox} {oy} {oz + sz - 1} if loaded {ox + sx - 1} {oy} {oz}',
                                f'execute unless score #{k}bl bm.rng matches 1 run scoreboard players add #{k}bgu bm.p2 1',
                                f'execute unless score #{k}bl bm.rng matches 1 if score #{k}bgu bm.p2 matches 20.. run function bm:{PFX}/bio/{key}_off',
                                f'execute unless score #{k}bl bm.rng matches 1 run return 0',
                                f'scoreboard players add #{k}bw bm.p2 1', f'execute unless score #{k}bw bm.p2 matches 3.. run return 0',
                                *fills(dim, (ox, oy, oz), (sx, sy, sz), c['biome']),
                                f'execute in {dim} store success score #{k}bl bm.rng ' + ' '.join(f'if biome {x} {y} {z} {c["biome"]}' for (x, y, z) in corners),
                                f'execute if score #{k}bl bm.rng matches 1 run scoreboard players set {c["bio"]} bm.p2 {BIOV}',
                                f'execute unless score #{k}bl bm.rng matches 1 run scoreboard players add #{k}bgu bm.p2 5',
                                f'function bm:{PFX}/bio/{key}_off'])
        fn(f'{PFX}/bio/{key}_off', [f'scoreboard players set #{k}bw bm.p2 0', *[f'execute in {dim} run forceload remove {q}' for q in fl]])

    # ---- the sweep (once a second, while anyone is in a placed box)
    sweep = []
    for key, c in DG.items():
        M = c['mod']
        sweep.append(f'execute if score {c["ver"]} bm.p2 matches {c["VER"]} in {c["dim"]} if entity @a[{M.BOX}] run function bm:{PFX}/{key}')
        body = [f'execute as {selector(key)} at @s run function bm:{PFX}/cull']
        if key == 'armada':
            body.append(f'execute as @e[type=minecraft:husk,tag=bm.mire,tag=!bm.mtame,{M.BOX}] at @s run function bm:p246/melt')
        fn(f'{PFX}/{key}', body)
    second[0:0] = sweep                     # (ahead of the mob rolls: a natural spawn is gone before it's rolled)
    fn(f'{PFX}/cull', ['execute if data entity @s {PersistenceRequired:1b} run return 0',
                       'execute on owner run return 0', 'execute on leasher run return 0',
                       'execute on passengers if entity @s[type=minecraft:player] run return 0',
                       'execute if score @s bm.pid matches -2147483648.. run return 0',
                       f'execute if entity @s[type=#bm:{PFX}_splits,tag=!bm.tiered] if data entity @s CustomName run return 0',
                       f'function bm:{PFX}/gone'])
    fn(f'{PFX}/gone', ['tp @s ~ -400 ~', 'kill @s'])

    # ---- first sight: a bare monster (a natural spawn) in a placed box, before anything rolls it
    import phase27 as P27
    kinds = sorted(set(G.ARMORED) | set(G.UNARMORED) | set(P27.LUCKY_ONLY))
    n_init = 0
    for t in kinds:
        L = G.FUNCS.get(f'mobs/init/{t}')
        if not L: continue
        L[0:0] = [f'execute if predicate bm:{PFX}/in_{key} if score {c["ver"]} bm.p2 matches {c["VER"]} unless data entity @s Tags '
                  f'unless data entity @s CustomName run return run function bm:{PFX}/gone' for key, c in DG.items()]
        n_init += 1
    assert n_init >= 30, n_init

    # ---- the pack's other risers: never inside a box (the Undercrown's own Mires come from p246/uc/*, never the roll)
    patched = 0
    keep_out = {'p246/roll': 'in_armada', 'p181/stk/at': 'in_box', 'p82/summon': 'in_box', 'p32/spawn/saucer': 'in_box',
                'p32/spawn/bigslime': 'in_box', 'p32/spawn/bphantom': 'in_box', 'p32/spawn/trooper': 'in_under'}
    for f_, p in keep_out.items():
        L = G.FUNCS[f_]
        L.insert(0, f'execute if predicate bm:{PFX}/{p} run return 0')
        patched += 1
    return patched, n_init
