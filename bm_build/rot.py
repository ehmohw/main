"""Block-state rotation for runtime patches of rotated structures (2.20).

A market's bm.mkt marker carries the structure's turn: y_rotation 0 = as built (template +x east, +z south), 90 = turned
clockwise once (template +x -> south), 180, -90. Template states are rotated the same way the game rotates a placed
structure, so a patch can setblock the exact state the template would have placed."""

DIRS = ['north', 'east', 'south', 'west']                 # clockwise
TURNS = [('-45..45', 0), ('45..135', 1), ('135..180', 2), ('-180..-135', 2), ('-135..-45', 3)]   # y_rotation range -> clockwise quarter turns


def _cw(d, n):
    return DIRS[(DIRS.index(d) + n) % 4] if d in DIRS else d


def rotate(state, n):
    """'minecraft:x[a=b,...]' turned n quarter turns clockwise."""
    n %= 4
    if n == 0 or '[' not in state:
        return state
    name, props = state[:-1].split('[', 1)
    kv = dict(p.split('=', 1) for p in props.split(','))
    out = {}
    for k, v in kv.items():
        if k in DIRS:                                     # fences, walls, bars, panes, vines: connection per side
            out[_cw(k, n)] = v
        elif k == 'facing' or k == 'horizontal_facing':
            out[k] = _cw(v, n)
        elif k == 'axis' and v in ('x', 'z') and n % 2:
            out[k] = 'z' if v == 'x' else 'x'
        elif k == 'rotation':                             # signs, banners, skulls: 16 steps, 4 per quarter turn
            out[k] = str((int(v) + 4 * n) % 16)
        else:
            out[k] = v
    return name + '[' + ','.join(f'{k}={out[k]}' for k in kv if k not in DIRS) + \
        (',' if any(k in DIRS for k in kv) and any(k not in DIRS for k in kv) else '') + \
        ','.join(f'{k}={out[k]}' for k in DIRS if k in out) + ']'


def strip_waterlog(state):
    """The same state with waterlogged=false (for a block that must hold no water)."""
    if 'waterlogged=' in state:
        return state.replace('waterlogged=true', 'waterlogged=false')
    return state


if __name__ == '__main__':
    assert rotate('minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]', 1) == \
        'minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]'
    assert rotate('minecraft:iron_bars[east=true,north=false,south=false,waterlogged=false,west=true]', 1).endswith('north=true,east=false,south=true,west=false]')
    assert rotate('minecraft:iron_chain[axis=x,waterlogged=false]', 3) == 'minecraft:iron_chain[axis=z,waterlogged=false]'
    assert rotate('minecraft:oak_sign[rotation=12]', 2) == 'minecraft:oak_sign[rotation=4]'
    print('rot ok')
