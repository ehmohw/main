"""Read a box of blocks straight out of the test server's region files (Anvil format), after `save-all flush`.

usage (module): from scan import scan; blocks = scan(x1, y1, z1, x2, y2, z2, dim='overworld')
usage (cli):    python3 tools/scan.py x1 y1 z1 x2 y2 z2 [substring filter]
Returns {(x, y, z): 'minecraft:block[props]'} in absolute coordinates; air is left out unless keep_air=True.
dim: 'overworld', 'the_nether', 'the_end', or a namespaced custom dimension such as 'bm:hollow_throne'.
"""
import io, os, struct, sys, zlib, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SRV = os.environ.get('BM_SRV', '/tmp/claude-0/-home-user-main/5487f497-06f9-53d0-b240-d8be6367a14d/scratchpad/srv')


def read_nbt(f):
    def rd(n): return f.read(n)
    def tag(t):
        if t == 1: return struct.unpack('>b', rd(1))[0]
        if t == 2: return struct.unpack('>h', rd(2))[0]
        if t == 3: return struct.unpack('>i', rd(4))[0]
        if t == 4: return struct.unpack('>q', rd(8))[0]
        if t == 5: return struct.unpack('>f', rd(4))[0]
        if t == 6: return struct.unpack('>d', rd(8))[0]
        if t == 7: n = struct.unpack('>i', rd(4))[0]; return rd(n)
        if t == 8: n = struct.unpack('>H', rd(2))[0]; return rd(n).decode('utf-8', 'replace')
        if t == 9:
            et = rd(1)[0]; n = struct.unpack('>i', rd(4))[0]
            return [tag(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                et = rd(1)[0]
                if et == 0: return d
                k = tag(8); d[k] = tag(et)
        if t == 11: n = struct.unpack('>i', rd(4))[0]; return list(struct.unpack(f'>{n}i', rd(4 * n)))
        if t == 12: n = struct.unpack('>i', rd(4))[0]; return list(struct.unpack(f'>{n}q', rd(8 * n)))
        raise ValueError(t)
    t = rd(1)[0]; tag(8)
    return tag(t)


def _state(p):
    if isinstance(p, str): return p
    if '' in p: return p['']                    # 26.x heterogeneous list: a bare name wrapped as {"": name}
    props = p.get('Properties', p.get('properties'))
    return p.get('Name', p.get('id')) + ('[' + ','.join(f'{k}={v}' for k, v in sorted(props.items())) + ']' if props else '')


def region_dir(dim):
    w = os.path.join(SRV, 'world')
    if dim in ('overworld', 'minecraft:overworld'):
        for c in (os.path.join(w, 'dimensions', 'minecraft', 'overworld', 'region'), os.path.join(w, 'region')):
            if os.path.isdir(c): return c
    if dim in ('the_nether', 'minecraft:the_nether'):
        for c in (os.path.join(w, 'dimensions', 'minecraft', 'the_nether', 'region'), os.path.join(w, 'DIM-1', 'region')):
            if os.path.isdir(c): return c
    if dim in ('the_end', 'minecraft:the_end'):
        for c in (os.path.join(w, 'dimensions', 'minecraft', 'the_end', 'region'), os.path.join(w, 'DIM1', 'region')):
            if os.path.isdir(c): return c
    ns, name = dim.split(':') if ':' in dim else ('minecraft', dim)
    return os.path.join(w, 'dimensions', ns, name, 'region')


def chunk(dim, cx, cz, _cache={}):
    rx, rz = cx >> 5, cz >> 5
    path = os.path.join(region_dir(dim), f'r.{rx}.{rz}.mca')
    if not os.path.exists(path): return None
    key = (path, os.path.getmtime(path))
    if key not in _cache: _cache[key] = open(path, 'rb').read()
    data = _cache[key]
    i = 4 * ((cx & 31) + (cz & 31) * 32)
    off = (data[i] << 16 | data[i + 1] << 8 | data[i + 2]) * 4096
    if off == 0: return None
    ln = struct.unpack('>i', data[off:off + 4])[0]
    comp = data[off + 4]
    raw = data[off + 5:off + 4 + ln]
    raw = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
    return read_nbt(io.BytesIO(raw))


def section_states(sec):
    bs = sec.get('block_states')
    if not bs: return None
    pal = [_state(p) for p in bs['palette']]
    if len(pal) == 1 or 'data' not in bs: return [pal[0]] * 4096
    bits = max(4, (len(pal) - 1).bit_length())
    per = 64 // bits
    mask = (1 << bits) - 1
    out = []
    for v in bs['data']:
        v &= (1 << 64) - 1
        for k in range(per):
            out.append(pal[(v >> (k * bits)) & mask])
            if len(out) == 4096: return out
    return out


def scan(x1, y1, z1, x2, y2, z2, dim='overworld', keep_air=False, save=True):
    if save:
        from rcon import Rcon
        Rcon().cmd('save-all flush')
    x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
    out = {}
    for cx in range(x1 >> 4, (x2 >> 4) + 1):
        for cz in range(z1 >> 4, (z2 >> 4) + 1):
            c = chunk(dim, cx, cz)
            if not c: continue
            for sec in c.get('sections', []):
                sy = sec['Y']
                if sy * 16 + 15 < y1 or sy * 16 > y2: continue
                st = section_states(sec)
                if st is None: continue
                for i, s in enumerate(st):
                    if not keep_air and s in ('minecraft:air', 'minecraft:cave_air', 'minecraft:void_air'): continue
                    lx, lz, ly = i & 15, (i >> 4) & 15, i >> 8
                    x, y, z = cx * 16 + lx, sy * 16 + ly, cz * 16 + lz
                    if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2: out[(x, y, z)] = s
    return out


if __name__ == '__main__':
    a = list(map(int, sys.argv[1:7]))
    flt = sys.argv[7] if len(sys.argv) > 7 else None
    for p, s in sorted(scan(*a).items()):
        if not flt or flt in s: print(p, s)
