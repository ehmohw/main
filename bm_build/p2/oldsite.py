"""3.0: a final dungeon that moved (the Undercrown and the Armada, out to 2.5k-5k from 0,0): in a world that had it built at its old
spot, that copy is taken down once, before the first build at the new one - whoever is in it carried out, what it made cleared,
its blocks back to the dimension's own (netherrack in the Nether, the void's air in the End). A world that never had it: nothing.

3.0e: a dungeon can have moved more than once (the Armada: 2.99's site, then 3.0's, now high in the End's sky). Each old site has
its own function and flag (name / flag), and its own test of whether this world ever built there (built: execute conditions, any
one true = it did); keep (the new box) is asserted clear of the old one's every fill. biome: put the old box's biome back too.
SITES records each one (name -> dim, box selector) for the passes that guard a teardown (phase248's backpacks)."""

SITES = {}


def quarters(x0, z0, sx, sz, m=8):
    """a forceload takes at most 256 chunks: a box and its margin in four"""
    mx, mz = x0 + sx // 2, z0 + sz // 2
    return [f'{a} {b} {c} {e}' for a, c in ((x0 - m, mx), (mx + 1, x0 + sx + m)) for b, e in ((z0 - m, mz), (mz + 1, z0 + sz + m))]


def _overlap(a0, asz, b0, bsz):
    return all(a0[i] < b0[i] + bsz[i] and b0[i] < a0[i] + asz[i] for i in range(3))


def generate(G, key, dim, old, size, block, clear, out_fn, ver, name=None, flag=None, built=None, keep=None, biome=None):
    """{name} (default {key}/oldsite): called first by the build's try; returns 1 while the old copy still stands (the try waits),
    0 once it's gone. clear: entity selectors (no box) for what the dungeon made; ver: its built-version score (unset or 0 - it was
    never built here), unless built (a list of execute conditions) says otherwise."""
    (ox, oy, oz), (sx, sy, sz) = old, size
    name = name or f'{key}/oldsite'
    flag = flag or f'#{key}_old'
    built = built or [f'score {ver} bm.p2 matches 1..']
    if keep:
        assert not _overlap(old, size, *keep), f'{name}: the old box {old} {size} overlaps the new one {keep}'
    box = f'x={ox},y={oy},z={oz},dx={sx - 1},dy={sy - 1},dz={sz - 1}'
    SITES[name] = (dim, box)
    fl = quarters(ox, oz, sx, sz)
    fills = [f'execute in {dim} run fill {ox + x} {oy + y} {oz + z} {ox + min(sx, x + 32) - 1} {oy + min(sy, y + 32) - 1} {oz + min(sz, z + 32) - 1} {block}'
             for x in range(0, sx, 32) for y in range(0, sy, 32) for z in range(0, sz, 32)]
    bio = []
    if biome:
        import phase255 as NS
        bio = NS.fills(dim, old, size, biome)
        if keep:      # (fillbiome works in 4-block quarts, padded a quart round: never reach the new box's own padded quarts)
            P, q = NS.PAD, NS._q
            pad = lambda o, z: ((q(o[0] - P), q(o[1] - P), q(o[2] - P)), tuple(q(o[i] + z[i] - 1 + P) + 4 - q(o[i] - P) for i in range(3)))
            assert not _overlap(*pad(old, size), *pad(*keep)), f'{name}: its biome fill would reach the new box'
    G.fn(name, [f'execute if score {flag} bm.p2 matches 1 run return 0',
                'scoreboard players set #olb bm.p2 0', *[f'execute if {c} run scoreboard players set #olb bm.p2 1' for c in built],
                f'execute unless score #olb bm.p2 matches 1 run return run scoreboard players set {flag} bm.p2 1',
                *[f'execute in {dim} run forceload add {q}' for q in fl],
                f'execute in {dim} store success score #olok bm.p2 if loaded {ox} {oy} {oz} if loaded {ox + sx - 1} {oy} {oz + sz - 1} if loaded {ox} {oy} {oz + sz - 1} if loaded {ox + sx - 1} {oy} {oz}',
                'execute unless score #olok bm.p2 matches 1 run return 1',
                f'scoreboard players add {flag}w bm.p2 1', f'execute unless score {flag}w bm.p2 matches 4.. run return 1',
                f'execute in {dim} as @a[{box}] at @s run function bm:{out_fn}',
                *[f'execute in {dim} run kill @e[{s},{box}]' for s in clear], *fills, *bio,
                *[f'execute in {dim} run forceload remove {q}' for q in fl],
                f'scoreboard players set {flag} bm.p2 1', 'return 0'])
    return box
