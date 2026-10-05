"""Tiny typed NBT toolkit: SNBT strings for commands + binary NBT for structure files."""
import gzip, io, json, re, struct


class Byte(int): pass
class Short(int): pass
class Int(int): pass
class Long(int): pass
class Float(float): pass
class Double(float): pass
class IntArray(list): pass


def B(v): return Byte(int(v))
def F(v): return Float(v)
def D(v): return Double(v)
def L(v): return Long(v)


_BARE = re.compile(r'^[A-Za-z0-9_\-.+]+$')


def _key(k):
    return k if _BARE.match(k) and not k[0].isdigit() and k not in ('true', 'false') else json.dumps(k)


def snbt(v):
    """Python -> SNBT text."""
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, Byte): return f'{int(v)}b'
    if isinstance(v, Short): return f'{int(v)}s'
    if isinstance(v, Long): return f'{int(v)}L'
    if isinstance(v, Float): return f'{_num(v)}f'
    if isinstance(v, Double): return f'{_num(v)}d'
    if isinstance(v, IntArray): return '[I;' + ','.join(str(int(x)) for x in v) + ']'
    if isinstance(v, int): return str(v)
    if isinstance(v, float): return _num(v)
    if isinstance(v, str): return json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        return '{' + ','.join(f'{_key(k)}:{snbt(x)}' for k, x in v.items()) + '}'
    if isinstance(v, (list, tuple)):
        return '[' + ','.join(snbt(x) for x in v) + ']'
    raise TypeError(type(v))


def _num(f):
    s = repr(float(f))
    return s[:-2] if s.endswith('.0') else s


def to_json(v):
    """Python -> plain JSON-able (strips type wrappers)."""
    if isinstance(v, bool): return v
    if isinstance(v, int): return int(v)
    if isinstance(v, float): return float(v)
    if isinstance(v, dict): return {k: to_json(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [to_json(x) for x in v]
    return v


# ---------- binary NBT ----------
TAG = dict(end=0, byte=1, short=2, int=3, long=4, float=5, double=6, bytes=7, string=8, list=9, compound=10, ints=11)


def _tag_of(v):
    if isinstance(v, bool) or isinstance(v, Byte): return 1
    if isinstance(v, Short): return 2
    if isinstance(v, Long): return 4
    if isinstance(v, IntArray): return 11
    if isinstance(v, int): return 3
    if isinstance(v, Float): return 5
    if isinstance(v, float): return 6
    if isinstance(v, str): return 8
    if isinstance(v, (list, tuple)): return 9
    if isinstance(v, dict): return 10
    raise TypeError(type(v))


def _wstr(b, s):
    e = s.encode('utf-8')
    b.write(struct.pack('>H', len(e))); b.write(e)


def _wpay(b, t, v):
    if t == 1: b.write(struct.pack('>b', int(v)))
    elif t == 2: b.write(struct.pack('>h', int(v)))
    elif t == 3: b.write(struct.pack('>i', int(v)))
    elif t == 4: b.write(struct.pack('>q', int(v)))
    elif t == 5: b.write(struct.pack('>f', float(v)))
    elif t == 6: b.write(struct.pack('>d', float(v)))
    elif t == 8: _wstr(b, v)
    elif t == 11:
        b.write(struct.pack('>i', len(v)))
        for x in v: b.write(struct.pack('>i', int(x)))
    elif t == 9:
        if not v:
            b.write(struct.pack('>bi', 0, 0)); return
        et = _tag_of(v[0])
        b.write(struct.pack('>bi', et, len(v)))
        for x in v:
            if _tag_of(x) != et:
                raise TypeError('mixed list')
            _wpay(b, et, x)
    elif t == 10:
        for k, x in v.items():
            tt = _tag_of(x)
            b.write(struct.pack('>b', tt)); _wstr(b, k); _wpay(b, tt, x)
        b.write(b'\x00')


def write_nbt_gz(path, root):
    b = io.BytesIO()
    b.write(b'\x0a'); _wstr(b, ''); _wpay(b, 10, root)
    with open(path, 'wb') as f:                          # 2.15: fixed gzip timestamp - identical builds give identical files
        f.write(gzip.compress(b.getvalue(), mtime=0))


def read_nbt_gz(path):
    data = gzip.open(path).read()
    p = [0]

    def rd(fmt):
        n = struct.calcsize(fmt); r = struct.unpack(fmt, data[p[0]:p[0] + n]); p[0] += n
        return r[0]

    def rs():
        n = rd('>H'); s = data[p[0]:p[0] + n].decode(); p[0] += n; return s

    def pay(t):
        if t == 1: return rd('>b')
        if t == 2: return rd('>h')
        if t == 3: return rd('>i')
        if t == 4: return rd('>q')
        if t == 5: return rd('>f')
        if t == 6: return rd('>d')
        if t == 8: return rs()
        if t == 11: return [rd('>i') for _ in range(rd('>i'))]
        if t == 9:
            et = rd('>b'); n = rd('>i'); return [pay(et) for _ in range(n)]
        if t == 10:
            out = {}
            while True:
                tt = rd('>b')
                if tt == 0: return out
                k = rs(); out[k] = pay(tt)
        raise ValueError(t)
    assert rd('>b') == 10; rs()
    return pay(10)
