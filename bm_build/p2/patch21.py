"""2.1 in-world repairs for dungeons that generated before the fixes. Jigsaw structures are placed with a random
rotation, so every position is taken relative to a marker that was built with yaw 0 (it turns with the structure):
local ^left ^up ^forward offsets at that yaw equal the template offsets for any rotation. Block states that carry a
direction (the stair patch) come in four pre-rotated variants, picked by reading a reference stair's facing.

- Frost Spire F1: the 4th Frost-Eye (target) sat 2 blocks outside the tower wall -> moved into the inner wall face.
- Frost Spire F3->roof stair: one step sat under the roof floor (head bump, top unreachable) -> rebuilt 1 block north.
- All dungeons: vault key_item is re-synced to the current key definition (keys are re-stamped every item version,
  and a vault only opens for an exact component match); victor's vaults become ominous vaults."""
from nbt import snbt
from p2.kit import stack_nbt

DIRS = ['north', 'east', 'south', 'west']        # clockwise


def rot_off(dx, dz, r):
    for _ in range(r): dx, dz = -dz, dx          # StructureTemplate CLOCKWISE_90: (x, z) -> (-z, x)
    return dx, dz


def rot_state(state, r):
    if '[' not in state or r == 0: return state
    name, props = state[:-1].split('[', 1)
    out = []
    kv = dict(p.split('=') for p in props.split(','))
    new = {}
    for k, v in kv.items():
        if k == 'facing' and v in DIRS: v = DIRS[(DIRS.index(v) + r) % 4]
        if k == 'axis' and v in ('x', 'z') and r % 2: v = 'z' if v == 'x' else 'x'
        if k in DIRS: k = DIRS[(DIRS.index(k) + r) % 4]
        new[k] = v
    return name + '[' + ','.join(f'{k}={v}' for k, v in new.items()) + ']'


def dg_pos(B):
    for x, y, z, tags in B.meta['markers']:
        if 'bm.dg' in tags: return int(x), int(y), int(z)


def old_frost_stair_cells(Bnew):
    """Cells that differ between the pre-2.1 stair (z0=28) and the current one (z0=27): stair blocks and air only."""
    import inspect, types
    import p2.dungeons.frost as M
    src = inspect.getsource(M).replace('stair(30, 3, z0=27)', 'stair(30, 3)')
    mod = types.ModuleType('p2.dungeons.frost_old')
    mod.__dict__.update({'__name__': 'p2.dungeons.frost_old', '__package__': 'p2.dungeons'})
    exec(compile(src, 'frost_old', 'exec'), mod.__dict__)
    O = mod.build()
    cells = []
    for k in sorted(set(O.b) | set(Bnew.b)):
        o, n = O.b.get(k), Bnew.b.get(k)
        if o != n and n is not None and 29 <= k[0] <= 31 and 34 <= k[1] <= 42 and 19 <= k[2] <= 28:
            cells.append((k, n))
    return cells


def generate(G, builds):
    fn = G.fn
    second = []
    # ---------------- Frost-Eye
    fn('p2/frost/fix_eye', ['setblock ~ ~ ~ minecraft:deepslate_tiles', 'setblock ^-2 ^ ^ minecraft:target[power=0]', 'tp @s ^-2 ^ ^',
                            'tag @s remove bm.hit'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz1,tag=bm.d_frost] at @s rotated ~ 0 positioned ^13 ^7 ^-8 '
                  'as @e[type=minecraft:marker,tag=bm.pet_target,tag=bm.pz1,tag=bm.d_frost,distance=..0.5] at @s rotated ~ 0 '
                  'run function bm:p2/frost/fix_eye')
    # ---------------- Frost F3 -> roof stair
    F = builds['frost']
    gx, gy, gz = dg_pos(F)
    cells = old_frost_stair_cells(F)
    ref = (30 - gx, 34 - gy, 28 - gz)       # old bottom step (facing north); in the new layout this cell is air
    for r in range(4):
        lines = []
        for (x, y, z), st in cells:
            dx, dz = rot_off(x - gx, z - gz, r)
            lines.append(f'setblock ~{dx} ~{y - gy} ~{dz} {rot_state(st, r)}')
        lines.append('playsound minecraft:block.deepslate_tiles.place block @a[distance=..48] ~ ~ ~ 1 0.7')
        fn(f'p2/frost/stairfix{r}', lines)
        rx, rz = rot_off(ref[0], ref[2], r)
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_frost] at @s if entity @a[distance=..40] '
                      f'if block ~{rx} ~{ref[1]} ~{rz} minecraft:deepslate_tile_stairs[facing={DIRS[r]}] run function bm:p2/frost/stairfix{r}')
    # ---------------- vaults: current key, victor's vault ominous
    from items import ITEM_VERSION
    for d, B in builds.items():
        gx, gy, gz = dg_pos(B)
        for i, (x, y, z, key_iid, loot, facing) in enumerate(B.meta['vaults']):
            done = f'bm.vk{i}_{ITEM_VERSION}'          # once per vault per item version
            lines = []
            if key_iid.startswith('bkey_'):
                cfg = snbt({'config': {'key_item': stack_nbt(key_iid), 'loot_table': loot}})
                for f in DIRS:
                    lines.append(f'execute if block ~ ~ ~ minecraft:vault[facing={f},ominous=false] run '
                                 f'setblock ~ ~ ~ minecraft:vault[facing={f},ominous=true,vault_state=inactive]{cfg}')
            lines += [f'data modify block ~ ~ ~ config.key_item set value {snbt(stack_nbt(key_iid))}', f'tag @s add {done}']
            fn(f'p2/{d}/vaultfix{i}', lines)
            second.append(f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},tag=!{done}] at @s rotated ~ 0 '
                          f'positioned ^{x - gx} ^{y - gy} ^{z - gz} if entity @a[distance=..24] if block ~ ~ ~ minecraft:vault '
                          f'run function bm:p2/{d}/vaultfix{i}')
    return dict(second=second)
