"""Read blocks straight out of a world's region files (anvil, 1.18+ chunk format) - for auditing how structures really sit in
generated terrain (tools/preview/placecheck.py).

    W = World('/root/bm_srv/world', 'overworld')      # or 'the_nether' / 'the_end'
    W.block(x, y, z) -> 'minecraft:stone' (properties dropped), or None where the chunk isn't generated
"""
import os, struct, zlib, gzip, io, math

# ---------------------------------------------------------------------------------------------------- a minimal NBT reader
def _nbt(buf):
    f = io.BytesIO(buf)
    def rd(n): return f.read(n)
    def payload(t):
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
            return [payload(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = rd(1)[0]
                if tt == 0: return d
                nl = struct.unpack('>H', rd(2))[0]; k = rd(nl).decode('utf-8', 'replace')
                d[k] = payload(tt)
        if t == 11: n = struct.unpack('>i', rd(4))[0]; return list(struct.unpack(f'>{n}i', rd(4 * n)))
        if t == 12: n = struct.unpack('>i', rd(4))[0]; return list(struct.unpack(f'>{n}q', rd(8 * n)))
        raise ValueError(t)
    t = rd(1)[0]; nl = struct.unpack('>H', rd(2))[0]; rd(nl)
    return payload(t)


def _name(p):
    # (26.x writes mixed lists with each entry wrapped as {'': value})
    while isinstance(p, dict): p = p['Name'] if 'Name' in p else p.get('', 'minecraft:air')
    return p


class World:
    def __init__(self, root, dim='overworld'):
        sub = {'overworld': 'region', 'the_nether': 'DIM-1/region', 'the_end': 'DIM1/region'}[dim]
        cand = [os.path.join(root, sub), os.path.join(root, 'dimensions', 'minecraft', dim, 'region')]
        self.dir = next((c for c in cand if os.path.isdir(c)), cand[0])
        self.chunks = {}

    def _chunk(self, cx, cz):
        key = (cx, cz)
        if key in self.chunks: return self.chunks[key]
        rx, rz = cx >> 5, cz >> 5
        path = os.path.join(self.dir, f'r.{rx}.{rz}.mca')
        sections = None
        if os.path.exists(path):
            with open(path, 'rb') as f:
                idx = 4 * ((cx & 31) + (cz & 31) * 32)
                f.seek(idx); loc = struct.unpack('>I', f.read(4))[0]
                off, cnt = loc >> 8, loc & 0xff
                if off:
                    f.seek(off * 4096); ln, comp = struct.unpack('>IB', f.read(5)); data = f.read(ln - 1)
                    raw = zlib.decompress(data) if comp == 2 else gzip.decompress(data) if comp == 1 else data
                    nbt = _nbt(raw)
                    if nbt.get('Status', 'minecraft:full').split(':')[-1] in ('full',):
                        sections = {}
                        for s in nbt.get('sections', []):
                            bs = s.get('block_states')
                            if not bs: continue
                            pal = [_name(p).split('[')[0] for p in bs['palette']]
                            sections[s['Y']] = (pal, bs.get('data'))
        self.chunks[key] = sections
        return sections

    def block(self, x, y, z):
        sec = self._chunk(x >> 4, z >> 4)
        if sec is None: return None
        s = sec.get(y >> 4)
        if s is None: return 'minecraft:air'
        pal, data = s
        if len(pal) == 1 or not data: return pal[0]
        bits = max(4, math.ceil(math.log2(len(pal))))
        per = 64 // bits
        i = ((y & 15) << 8) | ((z & 15) << 4) | (x & 15)
        word = data[i // per] & 0xFFFFFFFFFFFFFFFF
        v = (word >> ((i % per) * bits)) & ((1 << bits) - 1)
        return pal[v] if v < len(pal) else 'minecraft:air'
