"""EMMA - her theme: Democratus's hook and climb in D MAJOR, peaceful. Piano, wind chimes, a soft pad. 72 BPM,
36 bars = 120 s loop. No drums.

  0-3   wind chimes, the piano's slow arpeggios
  4-11  THE HOOK  piano melody over the arpeggios
 12-19  THE CLIMB piano, the pad warming
 20-27  THE HOOK  an octave up, sparser, the chimes answering
 28-35  THE HOOK  softly home to D, into the chimes again
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track, T, env, lp, hp, bp, R, SR
from sovereign_music import render, _guarded, seeded
from armada_music import M, apad
from killerwatt5 import HOOK, CLIMB, TR

BPM, BARS = 72, 36
MAJ = {5: 6, 10: 11, 0: 1}
def major(notes):
    out = []
    for x, d in notes:
        if x is None: out.append((None, d)); continue
        m = M(x); pc = m % 12
        out.append((m + (MAJ[pc] - pc if pc in MAJ else 0), d))
    return out

HOOKM = major(HOOK); HOOKM[-1] = (M('D5'), HOOKM[-1][1])
CLIMBM = major(CLIMB); CLIMBM[-1] = (M('A5'), CLIMBM[-1][1])
P_HOOK = [('D', 'M'), ('D', 'M'), ('B', 'm'), ('A', 'M'), ('D', 'M'), ('G', 'M'), ('B', 'm'), ('A', 'M')]
P_CLIMB = [('G', 'M'), ('G', 'M'), ('B', 'm'), ('A', 'M'), ('D', 'M'), ('B', 'm'), ('G', 'M'), ('A', 'M')]
P_HOME = P_HOOK[:7] + [('D', 'M')]
PENTA = [M(n) for n in ('D6', 'E6', 'F#6', 'A6', 'B6', 'D7', 'E7', 'F#7')]


def chord(r, q, octv=3):
    b = M(r + str(octv)); return [b, b + (4 if q == 'M' else 3), b + 7]


def piano(m, dur, amp=1.0, vel=0.7):
    """a piano note: slightly stretched partials, each decaying at its own rate, two strings a hair apart, a soft hammer"""
    dur = max(dur, 0.3) + 1.5
    t = T(dur); n = len(t); f = 440 * 2 ** ((m - 69) / 12)
    B = 0.0004; s = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 9000: break
        a = (vel ** (0.5 * k)) / k ** 0.9
        dec = 0.7 + 0.5 * k + f / 600
        s += a * np.exp(-t * dec) * (np.sin(2 * np.pi * fk * t) + 0.6 * np.sin(2 * np.pi * fk * 1.0012 * t + 0.4))
    s += 0.6 * np.exp(-t * 0.35 - (f / 2000)) * np.sin(2 * np.pi * f * t)      # the long singing tail of the fundamental
    s += 0.05 * bp(R.noise(n), 1500, 5000) * np.exp(-t * 60)                    # the hammer
    return amp * s * env(n, 0.002, 0, 1, 0.4) / 3


def windchime(m, amp=1.0, seed=0):
    rng = np.random.default_rng(seed)
    dur = 4.0; t = T(dur); f = 440 * 2 ** ((m - 69) / 12)
    s = sum(np.sin(2 * np.pi * f * r * t + rng.uniform(0, 6)) * np.exp(-t * d) * g
            for r, d, g in ((1, 0.9, 1), (2.76, 2.0, 0.35), (5.4, 4.0, 0.12), (8.93, 6, 0.05)))
    return amp * s * (1 + 0.15 * np.sin(2 * np.pi * rng.uniform(4, 7) * t)) * env(len(t), 0.001, 0, 1, 0.3)


def chimes(tr, bar0, bars, density=0.6, amp=0.05, seed=0):
    """the wind moving through them: little clusters, irregular"""
    rng = np.random.default_rng(seed)
    t = tr.at(bar0); end = tr.at(bar0 + bars)
    while t < end:
        if rng.random() < density:
            for j in range(rng.integers(1, 4)):
                tr.add(windchime(PENTA[rng.integers(len(PENTA))], amp * rng.uniform(0.5, 1), int(rng.integers(1 << 30))),
                       t + j * rng.uniform(0.08, 0.25), rng.uniform(-0.7, 0.7), 1, 0.7)
        t += rng.uniform(0.6, 1.8)


def accomp(tr, bar, r, q, amp=1.0):
    """the left hand and a slow rolling arpeggio, in the triplet lilt"""
    c = chord(r, q); bt = tr.beat
    tr.add(piano(c[0] - 12, bt * 4, 0.12 * amp, 0.5), tr.at(bar), -0.2, 1, 0.5)
    arp = [c[0], c[2], c[1] + 12, c[2], c[0] + 12, c[2]]
    for i, x in enumerate(arp):
        tr.add(piano(x, bt * 1.5, 0.07 * amp, 0.4), tr.at(bar, i * 2 * TR), (-0.25, 0.1)[i % 2], 1, 0.55)
    tr.add(apad([c[0] + 12, c[1] + 12, c[2] + 12], bt * 4 * 1.05, 0.03 * amp, 900, 1.5, 1.5, wave='tri' if False else 'saw'), tr.at(bar), 0, 1, 0.8)


def melody(tr, t0, notes, k=0, amp=0.16, pan=0.1):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(piano(x + k, d * tr.beat, amp, 0.75), t, pan, 1, 0.5)
        t += d * tr.beat


from armada_music import smooth, osc
from guitar import _ks


def flute(notes, beat, amp=0.1):
    """a soft flute: a pure tone with a little octave, breath, a gentle late vibrato"""
    total = sum(d for _, d in notes) * beat; n = int((total + 0.5) * SR)
    tgt = np.zeros(n); gate = np.zeros(n); on = np.zeros(n); t = 0.0
    first = next((x for x, _ in notes if x is not None), 74); tgt[:] = first
    for x, d in notes:
        i0, i1 = int(t * SR), int((t + d * beat) * SR)
        if x is not None:
            tgt[i0:] = x; gate[i0:int((t + d * beat * 0.95) * SR)] = 1; on[i0:i1] = np.arange(i1 - i0) / SR
        t += d * beat
    tt = np.arange(n) / SR
    fr = 440 * 2 ** ((smooth(tgt, 0.04) - 69) / 12) * (1 + 0.006 * np.clip((on - 0.3) / 0.4, 0, 1) * np.sin(2 * np.pi * 5 * tt))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph) + 0.12 * bp(R.noise(n), 1500, 6000)
    return amp * s * smooth(gate, 0.06)


def harp(m, amp=1.0, seed=0):
    f = 440 * 2 ** ((m - 69) / 12)
    s = _ks(f, 3.0, 0.9995, 0.25, seed)
    return amp * lp(s, 4000) * env(len(s), 0.002, 0, 1, 0.5)


def gliss(tr, t0, r, q, amp=0.05):
    c = chord(r, q, 4); notes = [c[0], c[1], c[2], c[0] + 12, c[1] + 12, c[2] + 12, c[0] + 24]
    for i, x in enumerate(notes): tr.add(harp(x, amp, i), t0 + i * 0.07, (-0.5 + 0.15 * i), 1, 0.6)


def strings(tr, bar, r, q, amp=0.04):
    c = chord(r, q, 3)
    tr.add(apad([c[0], c[2], c[1] + 12], tr.beat * 4 * 1.1, amp, 1400, 1.2, 1.5, voices=5, det=0.006, depth=0.15), tr.at(bar), -0.1, 1, 0.75)


def compose():
    tr = Track('emma', BPM, BARS)
    assert round(tr.seconds) == 120
    for b in range(4): accomp(tr, b, *(('D', 'M'), ('G', 'M'), ('D', 'M'), ('A', 'M'))[b], 0.8)
    chimes(tr, 0, 4, 0.6, 0.02, 1)
    secs = [(4, P_HOOK, 'hook'), (12, P_CLIMB, 'climb'), (20, P_HOOK, 'high'), (28, P_HOME, 'home')]
    for base, prog, kind in secs:
        for b in range(8): accomp(tr, base + b, *prog[b], 0.9 if kind == 'high' else 1.0)
        t0 = tr.at(base)
        gliss(tr, t0, *prog[0])
        if kind in ('climb', 'high'):
            for b in range(8): strings(tr, base + b, *prog[b])
        if kind == 'climb': tr.add(flute([(None if x is None else x, d) for x, d in CLIMBM], tr.beat, 0.05), t0, 0.3, 1, 0.65)
        if kind == 'high': tr.add(flute([(None if x is None else x - 12, d) for x, d in HOOKM], tr.beat, 0.06), t0, -0.3, 1, 0.65)
        if kind == 'home':
            for b in range(4): strings(tr, base + 4 + b, *prog[4 + b], 0.03)
        if kind == 'hook': melody(tr, t0, HOOKM)
        if kind == 'climb': melody(tr, t0, CLIMBM)
        if kind == 'high': melody(tr, t0, HOOKM, 12, 0.11, 0.25)
        if kind == 'home': melody(tr, t0, HOOKM, 0, 0.13)
        chimes(tr, base, 8, 0.2 if kind != 'high' else 0.35, 0.014, base)
    chimes(tr, 34, 2, 0.6, 0.02, 99)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'emma_theme.ogg'
    _guarded(render(seeded(5, compose), 3.2, 0.2), out, 6)
