"""Phase 251 (2.99a): NO WAY IN BUT THE DOOR - the Undercrown and the Vorn Armada throw out anyone who hasn't earned them, and
send back anyone who got ahead of the trials.

ADMISSION   the Undercrown: the Sovereign's Summons (bm.usum) and through the Maw while it stood open - a Summons-holder within 6
            of the open gate is admitted (and only the admitted open it from inside: p237/gate/tick's "coming out" rule
            was bm.uin, which its own cave by the seam is in - the Maw opened there without the tokens). The Armada: beamed aboard by the Hive-Star Coordinates (p241/beam/tick, its last
            tick). Admission is a score, bm.lku / bm.lka = the dungeon's run (#urun / #arun) when it was given: a rebuild
            (the fall, a re-place) voids every one, online or not. Out of the box 5 s (bm.lkgu / bm.lkga; the uaq pattern): dropped; carried
            out (p237/out, p241/out): dropped. A player the update finds already inside who meets the criterion (Summons; the
            Coordinates or bm.acoord) is admitted once, the first time it sees them (bm.lkv).
ENTRY       anyone (survival/adventure) without it, inside: carried out by the dungeon's own out, told why. The Undercrown's
            "inside" is its own blocks - every reachable cell's envelope and the solid rock the boxes can take in round it -
            never the approach cave or the Nether's own rock and caves round its shell (its box is 70% the Nether's). A tunnel
            dug in from outside (in Survival: mining fatigue 34 round its zone markers takes in 98% of its rock) is caught
            once it reaches boxed rock (70% of the shell) and at the latest a block short of any room. (Inside, every reachable
            cell is within 34 of a zone marker: an admitted player is always bm.uin, in Adventure, and can't dig out.) The
            Armada's inside is its whole box (bm.ain, Adventure: hive-fleet or void).
NO SKIPPING at build time p2/verify's own walk (Grid.bfs) runs once per stage k (gates 1..k open, the bridges they bring, every
            hidden/secret door and the Hoard/Vault open): each cell is labelled with the first stage that reaches it. Each
            stage's cells (with the drops off their ledges) are dilated (1 sideways, 1 down, 3 up: a player's hitbox and
            jump) into an envelope, and on up through the open air to the ceiling (a wind charge, an elytra in its hall); a
            voxel's label is the earliest envelope over it. The voxels of label s are covered by
            boxes that hold only labels >= s (and blocks nobody stands in): never a cell of an earlier stage, nor its margin.
            At run time a stage is reached when the controller's progress (bm.pz, cached: #lkpu / #lkpa) is >= s - and a
            guarded trial's (phase245) only once its knights fell (its pz<n>_open). Once a second, every box of a stage not
            yet reached is checked: an admitted player in one is sent BACK to where they last stood on the ground outside
            every such box (bm.lkx/y/z: recorded each second after the check), or the entrance if there's none. Pearls,
            chorus fruit, elytra, riptide, mounts, recalls, tokens - however they got there. Thrown ender pearls in either
            dungeon are drunk by the floor (p2/util/pearl_zap: the pearl comes back).
(Nothing runs until the dungeon is placed - #uver / #aver at its version: before that its box is the plain Nether, the void.)
THE PASS    an operator's tag, bm.lkpass: admitted, never sent back (the older bot tests set their stages by teleport)."""
import re
from items import T
import phase237 as P237
import phase241 as P241

PFX = 'p251'
GRACE = 5                                   # seconds out of the box before admission is dropped
DIL = dict(side=1, down=1, up=3)            # a stage's envelope round its standing cells
APPROACH_SIDE = 2                           # (the Undercrown's approach cave: its envelope, wider)
ZONES = {}

# per dungeon: its runtime module, dimension, verify's outside, the admission score, its run counter, its version, the progress cache
DG = {'under': dict(mod=P237, dim='minecraft:the_nether', outside='solid', adm='bm.lku', run='#urun', ver='#uver', pz='#lkpu', st='#lkst_u', name='The Undercrown'),
      'armada': dict(mod=P241, dim='minecraft:the_end', outside='void', adm='bm.lka', run='#arun', ver='#aver', pz='#lkpa', st='#lkst_a', name='The Vorn Armada')}


# ================================================================== the stage zones (build time)
def zones(key):
    """{'n': stages, 'cells': {stage: standing cells}, 'boxes': {stage: [(x0, y0, z0, x1, y1, z1) local, inclusive]},
    'entry': [boxes] (the Undercrown only), 'L': the voxel labels} - computed once"""
    if key in ZONES: return ZONES[key]
    import numpy as np
    from p2.verify import Grid, door_cells
    from p2.config import OPEN_LIGHT, GATE_H
    c = DG[key]
    B = c['mod'].build()
    UM = B.meta.get('under') or B.meta.get('armada')
    SX, SY, SZ = B.size
    G = _memo(Grid)(B, c['outside'], 0, jumps=bool(B.meta.get('parkour')))
    gates = B.meta['gates']
    N = max(g[4] for g in gates)
    plane = lambda g: [((g[0] + dw, g[1] + dy, g[2]) if g[3] == 'x' else (g[0], g[1] + dy, g[2] + dw)) for dw in (-1, 0, 1) for dy in range(GATE_H)]
    # every side door open, at every stage: the hidden rooms, the secret doors, the Hoard / the Hive Vault
    side = {}
    for h in UM['hidden'].values():
        for q in door_cells(*h['door'][:6]): side[q] = 'minecraft:air'
    for k_ in ('hoard', 'vault'):
        if UM.get(k_):
            for q in door_cells(*UM[k_][:6]): side[q] = 'minecraft:air'
    for (x, y, z, _k) in B.meta['sdoors']: side[(x, y, z)] = side[(x, y + 1, z)] = 'minecraft:air'
    starts = [tuple(B.meta['entrance'])]
    stage = {}
    for k in range(N + 1):
        G.override = dict(side)
        for g in gates:
            if g[4] <= k:
                for q in plane(g): G.override[q] = OPEN_LIGHT
        for (n, x1, y1, z1, x2, y2, z2, blk) in UM['bridges']:
            if n <= k:
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        for z in range(z1, z2 + 1): G.override[(x, y, z)] = 'minecraft:' + blk
        for q in G.bfs(starts):
            stage.setdefault(q, k)
    # the drops: off each ledge (and a long step past it), the column a player falls down
    occ = {}
    for (x, y, z), k in stage.items():
        pts = [(x, y, z)]
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for r in (1, 2):
                nx, nz = x + dx * r, z + dz * r
                if not (G.free(nx, y, nz) and G.free(nx, y + 1, nz)): break
                fy = y
                while fy >= 0 and G.free(nx, fy, nz) and not G.stand(nx, fy, nz):
                    pts.append((nx, fy, nz)); fy -= 1
                pts.append((nx, fy, nz))
        for p in pts:
            if occ.get(p, 99) > k: occ[p] = k
    # the labels: the earliest envelope over each voxel (127: nobody's; -1: the Undercrown's approach cave)
    L = np.full((SX, SY, SZ), 127, dtype=np.int16)
    def envelope(pts, sd):
        a = np.zeros((SX + 2 * sd, SY + DIL['down'] + DIL['up'], SZ + 2 * sd), dtype=bool)
        for (x, y, z) in pts:
            if -sd <= x < SX + sd and -DIL['up'] <= y < SY + DIL['down'] and -sd <= z < SZ + sd: a[x + sd, y + DIL['up'], z + sd] = True
        o = np.zeros((SX, SY, SZ), dtype=bool)
        for dx in range(-sd, sd + 1):
            for dz in range(-sd, sd + 1):
                for dy in range(-DIL['down'], DIL['up'] + 1):       # (a voxel dy above a point is in its envelope)
                    o |= a[sd - dx:sd - dx + SX, DIL['up'] - dy:DIL['up'] - dy + SY, sd - dz:sd - dz + SZ]
        return o
    for k in range(N, -1, -1):
        L[envelope([p for p, v in occ.items() if v == k], DIL['side'])] = k
    from p2.verify import passable
    solid = np.zeros((SX, SY, SZ), dtype=bool)
    ks = np.array([q for q, v in B.b.items() if not passable(v)], dtype=np.int32)
    solid[ks[:, 0], ks[:, 1], ks[:, 2]] = True
    setm = np.zeros((SX, SY, SZ), dtype=bool)
    ks = np.array(list(B.b.keys()), dtype=np.int32)
    setm[ks[:, 0], ks[:, 1], ks[:, 2]] = True
    if key == 'under': L[envelope(B.outside, APPROACH_SIDE)] = -1
    # (the open air over a stage's floor is that stage's, up to its ceiling: a wind charge, an elytra, a jump boost in its hall)
    free = ~solid & (setm if c['outside'] == 'solid' else True)
    env = (L >= 0) & (L <= N)                 # (what must be boxed: the envelopes - the air over them may be)
    for y in range(1, SY):
        L[:, y, :] = np.where(free[:, y, :], np.minimum(L[:, y, :], L[:, y - 1, :]), L[:, y, :])
    wild = L == 127
    if key == 'under':
        # (out in the Nether's own rock, or open by it: nobody's - and never boxed. Its own rock, and its air deep inside: anyone's)
        near = ~setm
        for _ in range(2):
            n_ = near.copy()
            n_[1:] |= near[:-1]; n_[:-1] |= near[1:]; n_[:, 1:] |= near[:, :-1]; n_[:, :-1] |= near[:, 1:]; n_[:, :, 1:] |= near[:, :, :-1]; n_[:, :, :-1] |= near[:, :, 1:]
            near = n_
        wild = (L == 127) & setm & (solid | ~near)
        L[~setm & (L != -1)] = 126
    live = (L >= 0) & (L <= N)
    boxes = {s: cover((L == s) & env, ((L >= s) & live) | wild) for s in range(1, N + 1)}
    entry = cover(live & env, live | wild) if key == 'under' else []
    cells = {}
    for q, k in stage.items(): cells.setdefault(k, []).append(q)
    ZONES[key] = dict(n=N, cells=cells, boxes=boxes, entry=entry, L=L, env=env, size=(SX, SY, SZ), setm=setm if key == 'under' else None)
    return ZONES[key]


def _memo(Grid):
    """verify's Grid, remembering free/stand of every cell no stage changes (eighteen walks over the same blocks)"""
    class Memo(Grid):
        def free(self, x, y, z):
            q = (x, y, z)
            if q in self.override: return Grid.free(self, x, y, z)
            m = self.__dict__.setdefault('_f', {})
            if q not in m: m[q] = Grid.free(self, x, y, z)
            return m[q]

        def stand(self, x, y, z):
            o = self.override
            if (x, y, z) in o or (x, y + 1, z) in o or (x, y - 1, z) in o: return Grid.stand(self, x, y, z)
            m = self.__dict__.setdefault('_s', {})
            q = (x, y, z)
            if q not in m: m[q] = Grid.stand(self, x, y, z)
            return m[q]
    return Memo


def cover(M, allowed):
    """axis-aligned boxes (inclusive, local) covering every voxel of M, each inside allowed: greedy, grown from the first
    voxel not yet covered, a step a side at a time while the face it would take is all allowed"""
    import numpy as np
    left = M.copy()
    X, Y, Z = M.shape
    out = []
    flat = np.flatnonzero(left)
    i = 0
    while i < len(flat):
        x, y, z = np.unravel_index(flat[i], M.shape)
        if not left[x, y, z]: i += 1; continue
        b = [x, y, z, x, y, z]
        grew = True
        while grew:
            grew = False
            for ax in (0, 2, 1):
                for hi in (True, False):
                    lo_, hi_ = b[ax], b[ax + 3]
                    nv = hi_ + 1 if hi else lo_ - 1
                    if not (0 <= nv < M.shape[ax]): continue
                    sl = [slice(b[0], b[3] + 1), slice(b[1], b[4] + 1), slice(b[2], b[5] + 1)]
                    sl[ax] = slice(nv, nv + 1)
                    if allowed[tuple(sl)].all():
                        if hi: b[ax + 3] = nv
                        else: b[ax] = nv
                        grew = True
        left[b[0]:b[3] + 1, b[1]:b[4] + 1, b[2]:b[5] + 1] = False
        out.append(tuple(int(v) for v in b))
        i += 1
    return out


def selftest(key):
    """no box holds a voxel labelled with an earlier stage (or the approach), nor any earlier stage's standing cell; every
    voxel of each stage is covered. Returns (errors, report lines)"""
    import numpy as np
    Z_ = zones(key)
    L, errs, rep = Z_['L'], [], []
    earlier = {}
    for k, cs in Z_['cells'].items():
        for q in cs: earlier[q] = k
    for s, bs in Z_['boxes'].items():
        cov = np.zeros(L.shape, dtype=bool)
        for (x0, y0, z0, x1, y1, z1) in bs:
            sub = L[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1]
            if (sub < s).any() or (sub == 126).any(): errs.append(f'{key}: a stage-{s} box {(x0, y0, z0, x1, y1, z1)} holds an earlier voxel')
            cov[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1] = True
        bad = [q for q, k in earlier.items() if k < s and any(x0 - 1 <= q[0] <= x1 + 1 and y0 - 3 <= q[1] <= y1 + 1 and z0 - 1 <= q[2] <= z1 + 1
                                                              for (x0, y0, z0, x1, y1, z1) in bs)]
        if bad: errs.append(f'{key}: stage {s}: {len(bad)} earlier standing cells within a box or its margin, e.g. {bad[:3]}')
        miss = int(((L == s) & Z_['env'] & ~cov).sum())
        if miss: errs.append(f'{key}: stage {s}: {miss} voxels uncovered')
        rep.append(f'stage {s:2d}: {len(Z_["cells"].get(s, [])):5d} new cells, {int((L == s).sum()):6d} voxels ({int(((L == s) & Z_["env"]).sum()):6d} by its floors, all boxed), {len(bs):3d} boxes')
    for (x0, y0, z0, x1, y1, z1) in Z_['entry']:
        sub = L[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1]
        if (sub == -1).any() or (sub == 126).any() or not Z_['setm'][x0:x1 + 1, y0:y1 + 1, z0:z1 + 1].all():
            errs.append(f'{key}: an entry box {(x0, y0, z0, x1, y1, z1)} reaches the approach or the Nether\'s own rock')
    if Z_['entry']:
        cov = np.zeros(L.shape, dtype=bool)
        for (x0, y0, z0, x1, y1, z1) in Z_['entry']: cov[x0:x1 + 1, y0:y1 + 1, z0:z1 + 1] = True
        miss = int((((L >= 0) & (L <= Z_['n'])) & Z_['env'] & ~cov).sum())
        if miss: errs.append(f'{key}: {miss} inside voxels out of every entry box')
        rep.append(f'entry: {len(Z_["entry"])} boxes over {int(cov.sum())} voxels (the approach cave and the Nether round it left out)')
    return errs, rep


# ================================================================== generate
def generate(G):
    """-> (boxes checked a second at most: the Undercrown's, the Armada's)"""
    fn, title, tellraw = G.fn, G.title, G.tellraw
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    P = G.PREFIX
    objs = ['bm.lku', 'bm.lka', 'bm.lkgu', 'bm.lkga', 'bm.lkv', 'bm.lkd', 'bm.lkx', 'bm.lky', 'bm.lkz']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.FUNCS['admin/uninstall'][0:0] = ['tag @a remove bm.lk_under', 'tag @a remove bm.lk_armada', 'tag @a remove bm.lkpass']
    G.fn('admin/lockout/pass', ['tag @s add bm.lkpass', G.title('@s', 'actionbar', T('Lockout pass: you may go anywhere in the Undercrown and the Armada (admin/lockout/unpass to drop it).', 'yellow'))])
    G.fn('admin/lockout/unpass', ['tag @s remove bm.lkpass'])
    sec, first, counts = [], ['scoreboard players set @s bm.lkv 1'], []
    for i, (key, c) in enumerate(DG.items(), 1):
        M, dim, adm, run, pz, st, nm = c['mod'], c['dim'], c['adm'], c['run'], c['pz'], c['st'], c['name']
        p_ = M.__name__.replace('phase', 'p')
        Z_ = zones(key)
        B = M.build()
        d, N = B.d, Z_['n']
        F, tg, gr = f'{PFX}/{key}', f'bm.lk_{key}', f'bm.lkg{key[0]}'
        guard = sorted(__import__('p2.config', fromlist=['D']).D[d].get('guard', {}))
        box = lambda b: f'x={M.OX + b[0]},y={M.OY + b[1]},z={M.OZ + b[2]},dx={b[3] - b[0]},dy={b[4] - b[1]},dz={b[5] - b[2]}'
        who = 'gamemode=!creative,gamemode=!spectator'
        # ---- admission (a score: the run it was given in), and the grace out of the box
        fn(f'{F}/admit', [f'scoreboard players operation @s {adm} = {run} bm.p2', f'tag @s add {tg}', f'scoreboard players set @s {gr} {GRACE}'])
        fn(f'{F}/drop', [f'scoreboard players reset @s {adm}', f'tag @s remove {tg}', 'execute if score @s bm.lkd matches %d run scoreboard players reset @s bm.lky' % i])
        sec += [f'tag @a[tag={tg}] remove {tg}', f'execute as @a if score @s {adm} = {run} bm.p2 run tag @s add {tg}', f'tag @a[tag=bm.lkpass] add {tg}',
                f'scoreboard players remove @a[tag={tg},scores={{{gr}=1..}}] {gr} 1', f'execute in {dim} run scoreboard players set @a[{M.BOX},tag={tg}] {gr} {GRACE}',
                f'execute as @a[tag={tg}] unless score @s {gr} matches 1.. run function bm:{F}/drop']
        G.FUNCS[f'{p_}/out'].append(f'function bm:{F}/drop')                 # (carried out: at once)
        # ---- the stage reached: the controller's progress (kept as it's solved, re-read while it's loaded); a guarded trial
        #      only once its knights fell (phase245 runs pz<n>_open then)
        for n in sorted(B.meta['puzzles']):
            G.FUNCS[f'p2/{d}/pz{n}_solve'].append(f'scoreboard players set {pz} bm.p2 {n}')
        G.FUNCS[f'p2/{d}/reset'].append(f'scoreboard players set {pz} bm.p2 0')
        sec += [f'execute in {dim} as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},{M.BOX},limit=1] store result score {pz} bm.p2 run scoreboard players get @s bm.pz',
                f'scoreboard players operation {st} bm.p2 = {pz} bm.p2']
        for g in guard:
            sec.append(f'execute if score {pz} bm.p2 matches {g} unless score #lkg{g}{key[0]} bm.p2 matches 1 run scoreboard players set {st} bm.p2 {g - 1}')
            G.FUNCS[f'p2/{d}/pz{g}_open'].append(f'scoreboard players set #lkg{g}{key[0]} bm.p2 1')
            G.FUNCS[f'p2/{d}/pz{g}_reset'].append(f'scoreboard players set #lkg{g}{key[0]} bm.p2 0')
        # (a rebuild: no progress, no knights felled - and every admission was the last run's)
        bt = G.FUNCS[f'{p_}/build/try']
        bt.insert(len(bt) - 1, f'function bm:{F}/rebuilt')
        fn(f'{F}/rebuilt', [f'scoreboard players set {pz} bm.p2 0', f'scoreboard players set {st} bm.p2 0'] + [f'scoreboard players set #lkg{g}{key[0]} bm.p2 0' for g in guard])
        # ---- who gets in
        if key == 'under':        # through the open Maw, with the Summons
            # (and the Maw opens from the inside only for those it admitted: bm.uin is anyone near a zone marker - its own cave too)
            gt = G.FUNCS['p237/gate/tick']
            k_ = next(j for j, l in enumerate(gt) if 'tag=bm.uin]' in l)
            gt[k_] = gt[k_].replace('tag=bm.uin]', f'tag={tg}]')
            sec.append(f'execute in {dim} as @e[type=minecraft:marker,tag=bm.ugate,tag=bm.open,{M.BOX}] at @s as @a[distance=..6,tag=bm.usum,tag=!{tg},{who}] run function bm:{F}/admit')
            first.append(f'execute if entity @s[tag=bm.usum] if dimension {dim} if entity @s[{M.BOX}] run function bm:{F}/admit')
        else:                     # the tractor beam's last tick, on the Dock
            bm_ = G.FUNCS['p241/beam/tick']
            beam = next(int(re.search(r'bm\.abeam matches (\d+) run execute in ', l).group(1)) for l in bm_ if ' run tp @s ' in l)
            bm_.append(f'execute if score @s bm.abeam matches {beam} run function bm:{F}/admit')
            first += [f'execute if dimension {dim} if entity @s[{M.BOX}] if items entity @s container.* {M.holds("hive_coords")} run function bm:{F}/admit',
                      f'execute if dimension {dim} if entity @s[{M.BOX},tag=bm.acoord] run function bm:{F}/admit']
        G.FUNCS[f'admin/{key}/go'].append(f'function bm:{F}/admit')
        # ---- once a second, while anyone who plays is in its box
        placed = f'if score {c["ver"]} bm.p2 matches {getattr(M, c["ver"][1:].upper())}'      # (before it's placed, its box is the plain Nether / the void)
        sec.append(f'execute {placed} in {dim} if entity @a[{M.BOX},{who}] run function bm:{F}/sec')
        body = ['tag @a[tag=bm.lkhit] remove bm.lkhit']
        if key == 'under':        # (its inside: its own blocks - not the approach cave, not the Nether's rock round it)
            fn(f'{F}/entry', [f'execute as @a[{box(b)},tag=!{tg},tag=!bm.lkhit,{who}] at @s run function bm:{F}/eject' for b in Z_['entry']])
            body.append(f'execute if entity @a[{M.BOX},tag=!{tg},{who}] run function bm:{F}/entry')
        else:                     # (its inside: all of its box)
            body.append(f'execute as @a[{M.BOX},tag=!{tg},{who}] at @s run function bm:{F}/eject')
        nb = len(Z_['entry'])
        for s in range(1, N + 1):
            bs = Z_['boxes'][s]
            if not bs: continue
            nb += len(bs)
            fn(f'{F}/z{s}', [f'execute as @a[{box(b)},tag={tg},tag=!bm.lkhit,tag=!bm.lkpass,{who}] at @s run function bm:{F}/back' for b in bs])
            body.append(f'execute if score {st} bm.p2 matches ..{s - 1} run function bm:{F}/z{s}')
        body.append(f'execute as @a[{M.BOX},tag={tg},tag=!bm.lkhit,gamemode=!spectator,nbt={{OnGround:1b}}] run function bm:{F}/mark')
        fn(f'{F}/sec', body)
        counts.append(nb)
        fn(f'{F}/mark', [f'scoreboard players set @s bm.lkd {i}', 'execute store result score @s bm.lkx run data get entity @s Pos[0]',
                         'execute store result score @s bm.lky run data get entity @s Pos[1]', 'execute store result score @s bm.lkz run data get entity @s Pos[2]'])
        # ---- out (no admission), and back (ahead of the trials)
        how = "the Sovereign's Summons, and through the Maw while it stands open." if key == 'under' else 'the Hive-Star Coordinates, and its tractor beam.'
        fn(f'{F}/eject', ['tag @s add bm.lkhit', 'ride @s dismount', f'function bm:{p_}/out',
                          title('@s', 'actionbar', [T(nm, 'dark_red', bold=True), T(' does not know you. You are carried out.', 'gray', italic=True)]),
                          tellraw('@s', P + [T(nm + ': ', 'dark_red', bold=True), T('there is no way in but its own - ', 'gray'), T(how, 'white')])])
        ex, ey, ez = (M.OX + B.meta['entrance'][0], M.OY + B.meta['entrance'][1], M.OZ + B.meta['entrance'][2])
        # (where they last stood - once: caught again before they stand anywhere new, it's the entrance)
        fn(f'{F}/back', ['tag @s add bm.lkhit', 'ride @s dismount', 'effect give @s minecraft:slow_falling 2 0 true',
                         f'execute store success score #lk bm.rng if score @s bm.lkd matches {i} if score @s bm.lky matches -64..',
                         f'execute if score #lk bm.rng matches 1 run function bm:{F}/to_last', f'execute if score #lk bm.rng matches 0 run function bm:{F}/to_start',
                         'scoreboard players reset @s bm.lky',
                         'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 20', 'execute at @s run playsound minecraft:block.respawn_anchor.deplete player @s ~ ~ ~ 0.6 1.4',
                         title('@s', 'actionbar', [T(nm, 'dark_red', bold=True), T(' will not be skipped: its trials come in their order. Back you go.', 'gray', italic=True)])])
        fn(f'{F}/to_last', ['execute store result storage bm:tmp lk.x int 1 run scoreboard players get @s bm.lkx', 'execute store result storage bm:tmp lk.y int 1 run scoreboard players get @s bm.lky',
                            'execute store result storage bm:tmp lk.z int 1 run scoreboard players get @s bm.lkz', f'function bm:{F}/to with storage bm:tmp lk'])
        fn(f'{F}/to', [f'$execute in {dim} run tp @s $(x).5 $(y) $(z).5'])
        fn(f'{F}/to_start', [f'execute in {dim} run tp @s {ex + 0.5} {ey} {ez + 0.5}'])
        # ---- thrown pearls: the floor drinks them (the pearl comes back)
        near = f' at @s if entity @e[type=minecraft:marker,tag=bm.zone_d,tag=bm.d_{d},distance=..40]' if key == 'under' else ''
        fast.append(f'execute {placed} in {dim} as @e[type=minecraft:ender_pearl,{M.BOX}]{near} at @s run function bm:p2/util/pearl_zap')
    fn(f'{PFX}/first', first)
    second.append(f'function bm:{PFX}/sec')
    fn(f'{PFX}/sec', ['execute as @a unless score @s bm.lkv matches 1 at @s run function bm:p251/first'] + sec)
    return tuple(counts)



def sample(key, s):
    """a standing cell first reached at stage s, 2+ inside one of its boxes (stage 0: an entry box) - world coordinates (t322)"""
    Z_, M = zones(key), DG[key]['mod']
    bs = Z_['entry'] if s == 0 else Z_['boxes'][s]
    G_ = M.build().b
    for q in sorted(Z_['cells'].get(s, [])):
        if s == 0 and not bs: return (M.OX + q[0], M.OY + q[1], M.OZ + q[2])
        if 'air' not in G_.get((q[0], q[1] + 2, q[2]), 'air'): continue
        if any(b[0] + 2 <= q[0] <= b[3] - 2 and b[1] <= q[1] <= b[4] - 3 and b[2] + 2 <= q[2] <= b[5] - 2 for b in bs):
            return (M.OX + q[0], M.OY + q[1], M.OZ + q[2])


if __name__ == '__main__':
    import sys
    for key in sys.argv[1:] or list(DG):
        e, rep = selftest(key)
        print(f'{key}: {zones(key)["n"]} stages, {len(e)} errors')
        for r in rep + e: print('   ', r)
        print('    sample cells (world):', {s: sample(key, s) for s in (0, 2, 3, zones(key)['n'] - 1, zones(key)['n'])})

