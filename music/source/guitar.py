"""the electric guitar: Karplus-Strong strings, a high-gain amp, a 4x12 cabinet"""
import numpy as np
from gv_music import SR, T, env, lp, hp, bp
from armada_music import osc, smooth, M


def _ks(f, dur, damp=0.996, bright=0.5, seed=0):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    buf = lp(buf, 2000 + 6000 * bright) if p > 64 else buf
    out = np.zeros(n); i = 0
    while i < n:
        k = min(p, n - i)
        out[i:i + k] = buf[:k]
        nb = damp * 0.5 * (buf + np.roll(buf, -1))
        buf = nb; i += k
    return out


def cab(x):
    """a 4x12: no lows below 80, a mid push, a fall-off over 5k"""
    y = hp(x, 85)
    y = y + 0.6 * bp(y, 500, 1100, 1) + 0.4 * bp(y, 2000, 3200, 1)
    return lp(lp(y, 5200), 6500)


def amp(x, gain=14.0):
    x = hp(x, 120)
    y = np.tanh(gain * x + 0.2)
    y = y - np.mean(y)
    return np.tanh(2.0 * lp(y, 7000))


def power(root, dur, muted=False, vol=1.0, seed=0):
    """a power chord (root, fifth, octave) through the amp; palm-muted = short, dark, chunky"""
    f = 440 * 2 ** ((M(root) - 69) / 12)
    d = min(dur, 0.18) if muted else dur
    s = sum(_ks(f * r, d + 0.05, 0.99 if muted else 0.9985, 0.3 if muted else 0.7, seed + i) for i, r in enumerate((1, 1.4983, 2)))
    if muted: s = lp(s, 900)
    y = cab(amp(s * 0.8, 18 if muted else 14))
    n = len(y)
    return vol * y * env(n, 0.002, 0, 1, 0.02 if muted else 0.08)


def lead_line(notes, beat, vol=0.3, k=0, port=0.03, vib=5.6, depth=0.012, legato=0.97):
    """the lead guitar: a sustaining, singing, overdriven line with slides and a wide late vibrato"""
    total = sum(d for _, d in notes) * beat
    n = int((total + 0.3) * SR)
    tgt = np.zeros(n); gate = np.zeros(n); onset = np.zeros(n); pick = np.zeros(n)
    first = next((M(x) for x, _ in notes if x is not None), 62); tgt[:] = first + k
    t = 0.0
    for x, d in notes:
        i0, i1 = int(t * SR), int((t + d * beat) * SR)
        if x is not None:
            tgt[i0:] = M(x) + k
            gate[i0:int((t + d * beat * legato) * SR)] = 1.0
            onset[i0:i1] = np.arange(i1 - i0) / SR
            a = min(i0 + int(0.01 * SR), n); pick[i0:a] = 1
        t += d * beat
    midi = smooth(tgt, port)
    tt = np.arange(n) / SR
    vb = depth * np.clip((onset - 0.25) / 0.3, 0, 1) * np.sin(2 * np.pi * vib * tt)
    fr = 440.0 * 2 ** ((midi - 69) / 12) * (1 + vb)
    s = osc(fr) * 0.6 + osc(fr * 0.5, 'pulse', 0.3) * 0.3 + osc(fr * 1.002) * 0.3
    s = s * (0.6 + 0.4 * np.exp(-onset * 3)) + pick * np.random.uniform(-1, 1, n) * 0.5
    y = cab(amp(s * 0.5, 20))
    return vol * y * smooth(gate, 0.008)
