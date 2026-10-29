"""3.0: a final dungeon that moved (the Undercrown and the Armada, out to 2.5k-5k from 0,0): in a world that had it built at its old
spot, that copy is taken down once, before the first build at the new one - whoever is in it carried out, what it made cleared,
its blocks back to the dimension's own (netherrack in the Nether, the void's air in the End). A world that never had it: nothing."""


def quarters(x0, z0, sx, sz, m=8):
    """a forceload takes at most 256 chunks: a box and its margin in four"""
    mx, mz = x0 + sx // 2, z0 + sz // 2
    return [f'{a} {b} {c} {e}' for a, c in ((x0 - m, mx), (mx + 1, x0 + sx + m)) for b, e in ((z0 - m, mz), (mz + 1, z0 + sz + m))]


def generate(G, key, dim, old, size, block, clear, out_fn, ver):
    """{key}/oldsite: called first by the build's try; returns 1 while the old copy still stands (the try waits), 0 once it's gone.
    clear: entity selectors (no box) for what the dungeon made; ver: its built-version score (unset - it was never built here)."""
    (ox, oy, oz), (sx, sy, sz) = old, size
    box = f'x={ox},y={oy},z={oz},dx={sx - 1},dy={sy - 1},dz={sz - 1}'
    fl = quarters(ox, oz, sx, sz)
    flag = f'#{key}_old'
    fills = [f'execute in {dim} run fill {ox + x} {oy + y} {oz + z} {ox + min(sx, x + 32) - 1} {oy + min(sy, y + 32) - 1} {oz + min(sz, z + 32) - 1} {block}'
             for x in range(0, sx, 32) for y in range(0, sy, 32) for z in range(0, sz, 32)]
    G.fn(f'{key}/oldsite', [f'execute if score {flag} bm.p2 matches 1 run return 0',
                            f'execute unless score {ver} bm.p2 matches 1.. run return run scoreboard players set {flag} bm.p2 1',
                            *[f'execute in {dim} run forceload add {q}' for q in fl],
                            f'execute in {dim} store success score #olok bm.p2 if loaded {ox} {oy} {oz} if loaded {ox + sx - 1} {oy} {oz + sz - 1} if loaded {ox} {oy} {oz + sz - 1} if loaded {ox + sx - 1} {oy} {oz}',
                            'execute unless score #olok bm.p2 matches 1 run return 1',
                            f'scoreboard players add {flag}w bm.p2 1', f'execute unless score {flag}w bm.p2 matches 4.. run return 1',
                            f'execute in {dim} as @a[{box}] at @s run function bm:{out_fn}',
                            *[f'execute in {dim} run kill @e[{s},{box}]' for s in clear], *fills,
                            *[f'execute in {dim} run forceload remove {q}' for q in fl],
                            f'scoreboard players set {flag} bm.p2 1', 'return 0'])
