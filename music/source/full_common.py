"""Shared tools for the full-length themes (democratus_full, killerwatt_full, emma_full).

- note lines in a compact text form, with triplets ('t' = a third of a beat, '2t' = two thirds)
- chords by name ('Dm', 'Bb', 'A7', 'C#o7', 'Gsus4', 'F#m', 'BbM7'), transposable
- a diatonic harmonizer that follows the chord under each note (so a third above over an A major chord uses C#, not C)
- a checker that lists every held melody note that isn't in the chord under it, for review before rendering
- a render that sets loudness from the loud passages, not the average (so quiet sections don't push the rest into the
  limiter)
"""
import numpy as np
from gv_music import SR, R, lp
from sovereign_music import _guarded

TR = 1 / 3
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
QUAL = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10), 'M7': (0, 4, 7, 11), 'o': (0, 3, 6),
        'o7': (0, 3, 6, 9), 'sus4': (0, 5, 7), 'sus2': (0, 2, 7), 'add9': (0, 4, 7, 14), 'm6': (0, 3, 7, 9), '5': (0, 7)}


def midi(x):
    """'C#4' or a midi number -> midi number (int or float)"""
    if x is None or isinstance(x, (int, float, np.integer, np.floating)): return x
    n, acc, octv = x[0], x[1:-1], int(x[-1])
    return 12 * (octv + 1) + PC[n] + acc.count('#') - acc.count('b')


def L(s):
    """'D5:1 F5:t A5:2t r:2 ...' -> [(midi or None, beats)]"""
    out = []
    for tok in s.split():
        n, d = tok.split(':')
        d = {'t': TR, '2t': 2 * TR, 'h': 0.5, 'q': 0.25}.get(d) or float(d)
        out.append((None if n == 'r' else midi(n), d))
    return out


def beats(x): return sum(d for _, d in x)


def bars(x, n, bb=4):
    assert abs(beats(x) - n * bb) < 1e-6, (n * bb, beats(x))
    return x


def shift(notes, k): return [(None if x is None else midi(x) + k, d) for x, d in notes]


def stretch(notes, f): return [(x, d * f) for x, d in notes]


def head(notes, nbeats):
    """the first nbeats of a line (the last note cut to fit)"""
    out, t = [], 0.0
    for x, d in notes:
        if t >= nbeats - 1e-6: break
        out.append((x, min(d, nbeats - t))); t += d
    return out


def tail(notes, nbeats):
    """the line from beat nbeats on"""
    out, t = [], 0.0
    for x, d in notes:
        if t >= nbeats - 1e-6: out.append((x, d))
        elif t + d > nbeats + 1e-6: out.append((x, t + d - nbeats))
        t += d
    return out


def chord(name):
    """'C#o7' -> (root pc, intervals); a slash chord ('Dm/A') gives its upper chord - see bass_pc for the bass"""
    name = name.split('/')[0]
    r = name[0]; i = 1
    while i < len(name) and name[i] in '#b': i += 1
    root = (PC[r] + name[1:i].count('#') - name[1:i].count('b')) % 12
    q = name[i:]
    return root, QUAL[q]


def bass_pc(name, k=0):
    """the bass note's pitch class: the slash note if there is one, else the root"""
    if '/' in name:
        b = name.split('/')[1]
        return (PC[b[0]] + b[1:].count('#') - b[1:].count('b') + k) % 12
    return (chord(name)[0] + k) % 12


def bass_note(name, octave=2, k=0):
    """the bass note as midi, in the octave that starts at C of `octave`"""
    return 12 * (octave + 1) + bass_pc(name, k)


def tones(name, octave=3, k=0):
    """the chord's notes from its root at the given octave"""
    root, iv = chord(name)
    base = 12 * (octave + 1) + root + k
    return [base + x for x in iv]


def pcs(name, k=0):
    root, iv = chord(name)
    return {(root + x + k) % 12 for x in iv} | {bass_pc(name, k)}


def scale_under(name, key_pcs, k=0):
    """the key's scale, with any chord tone that isn't in it replacing its nearest neighbour (C# for C under A major)"""
    sc = sorted({(p + k) % 12 for p in key_pcs})
    for p in pcs(name, k):
        if p in sc: continue
        near = min(sc, key=lambda s: min((s - p) % 12, (p - s) % 12))
        sc = sorted((set(sc) - {near}) | {p})
    return sc


def chord_at(prog, t_beats, bb=4):
    return prog[int(t_beats // bb) % len(prog)]


def harmonize(notes, steps, prog, key_pcs, k=0, start=0.0, bb=4):
    """move every note `steps` degrees along the scale of the chord under it (steps=2: a third above, -5: a sixth below)"""
    out, t = [], start
    for x, d in notes:
        if x is None: out.append((None, d)); t += d; continue
        sc = scale_under(chord_at(prog, t, bb), key_pcs, k)
        x = int(round(x)); pc = x % 12
        idx = min(range(len(sc)), key=lambda i: min((sc[i] - pc) % 12, (pc - sc[i]) % 12))
        base = x - pc + sc[idx]                                   # the scale note this one is (or is nearest to)
        if base - x > 6: base -= 12
        if x - base > 6: base += 12
        octv, j = divmod(idx + steps, len(sc))
        y = base + 12 * octv + (sc[j] - sc[idx])
        out.append((y, d)); t += d
    return out


def check(label, notes, prog, k=0, start=0.0, bb=4, held=0.99, ok_ext=()):
    """print every note at least `held` beats long that isn't a chord tone (or an allowed extension, in semitones above
    the root) - a list to look over, not an error"""
    t = start; bad = []
    for x, d in notes:
        if x is not None and d >= held:
            name = chord_at(prog, t, bb); root, iv = chord(name)
            rel = (int(round(x)) - root - k) % 12
            if rel not in {i % 12 for i in iv} and rel not in ok_ext and (int(round(x)) - k) % 12 != bass_pc(name):
                bad.append(f'bar {int(t // bb) + 1} beat {t % bb + 1:.2f}: {nm(x)} over {name}{"+" + str(k) if k else ""}')
        t += d
    print(f'[{label}] ' + ('ok' if not bad else f'{len(bad)} held non-chord tones:\n   ' + '\n   '.join(bad)))
    return bad


def nm(x):
    x = int(round(x)); return ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B'][x % 12] + str(x // 12 - 1)


def line(tr, t0, notes, fn, pan=0.0, wet=0.4, gain=1.0):
    """each note through an instrument function fn(midi, seconds)"""
    t = t0
    for x, d in notes:
        if x is not None: tr.add(fn(x, d * tr.beat), t, pan, gain, wet)
        t += d * tr.beat


def render_loud(tr, room=2.4, level=0.27, pct=80, bright=5000):
    """circular reverb as sovereign_music.render, but the loudness set from the loud passages (the pct-th percentile of
    half-second RMS) rather than the whole-track average, then the same tanh rounding"""
    from scipy.signal import fftconvolve
    n = tr.n
    ir_t = np.arange(int(room * SR)) / SR
    irs = [lp(R.noise(len(ir_t)) * np.exp(-ir_t * 6.9 / room), bright) * 0.12 for _ in range(2)]

    def circ(x, ir):
        y = fftconvolve(np.concatenate([x, x[:len(ir)]]), ir)[:n + len(ir)]
        out = y[:n].copy(); out[:len(ir)] += y[n:n + len(ir)]
        return out
    st = np.stack([tr.L + circ(tr.wetL, irs[0]), tr.R + circ(tr.wetR, irs[1])])
    w = int(0.5 * SR); mono = (st[0] ** 2 + st[1] ** 2) / 2
    blocks = np.sqrt(mono[: n // w * w].reshape(-1, w).mean(1))
    ref = np.percentile(blocks, pct)
    return (np.tanh(st * (level / ref)) * 0.92).astype(np.float32)


def save(tr, out, room=2.4, level=0.27, pct=80):
    _guarded(render_loud(tr, room, level, pct), out, 6)


def section_levels(tr, marks):
    """loudness (dB, relative) of each section, to see the shape of the piece: marks = [(name, start_bar, n_bars)]"""
    st = tr.L + tr.R
    for name, b0, nb in marks:
        a, b = int(tr.at(b0) * SR), int(tr.at(b0 + nb) * SR)
        r = np.sqrt((st[a:b] ** 2).mean()) + 1e-12
        print(f'   {name:<12} bars {b0:>3}-{b0 + nb - 1:<3} {20 * np.log10(r):6.1f} dB')
