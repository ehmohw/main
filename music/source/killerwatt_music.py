"""KILLERWATT - the Dread Eldritch's final battle (killerwatt_battle.ogg, a 120 s loop).

Built on the Vexis engine (gv_music, armada_music, sovereign_music) with two new voices:

  THE ELECTRIC VIOLIN  Democratus's instrument. A bowed sawtooth through a violin body, the bow's rasp in it, sliding
                       between notes, a vibrato that only blooms on held notes, then driven hard: a classical voice pushed
                       through distortion.
  THE WATERPHONE       bowed steel rods over a bowl of water: inharmonic partials whose pitch wavers as the water moves,
                       groaning in and out. The Dread.
  THE THEREMIN         from the Armada: the voice he speaks through, never touching anything.

DEMOCRATUS'S THEME (D minor; written for his scenes): D-F-A rising, the sixth (Bb) leaning on the fifth, a fall home to D.
KILLERWATT plays it corrupted: the fifth sharpened to a tritone (G#), the fall landing on the flat second (Eb) instead of D,
and the last bar reaching for the tonic and never getting there.

D minor, 160 BPM, 80 bars of 1.5 s = 120 s, ten sections of eight bars:
  0 ARC         war drums, the chugging bass, arcs of lightning, the theremin climbing in
  1 THE THEME   the violin with the corrupted theme over the march
  2 HIS THEME   the theme an octave up, the theremin doubling it a fifth wrong
  3 THE DREAD   half time; the waterphone groaning, the theremin alone, the bass pulsing (no let-up in the drums' threat)
  4 DESPERATE   the violin in frantic sixteenth runs, the double kick
  5 HOSTS       violin and theremin answering each other, the waterphone underneath
  6 SLAM        half time hits on every downbeat, the waterphone shrieking, lightning
  7 RISING      the theme a semitone up (Eb minor), everything
  8 FRENZY      the theme at double speed, twice
  9 THE BRINK   the stabs hammered, a roll and a riser - and round again

    python3 tools/killerwatt_music.py [out.ogg]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, T, env, lp, hp, bp, riser, tom
from boss_music import crash, mel, tp, bars_of
from sovereign_music import boom, suck, render, _guarded, seeded
from armada_music import M, osc, vlp, smooth, mono, stab, ther, addc, ekick, esnare, mhat, zap, sub808, ply

BPM, BARS, SEC = 160, 80, 8

# ---------------------------------------------------------------------- the themes
DEM = mel('D5:1.5 F5:0.5 A5:2 Bb5:3 A5:1 G5:1 F5:1 E5:1 C#5:1 D5:4')                       # Democratus, as he was (4 bars)
KW = mel('D5:1.5 F5:0.5 G#5:2 Bb5:3 G#5:1 G5:1 F5:1 E5:1 Eb5:1 D5:1.5 F5:0.5 G#5:2 '          # his theme, corrupted (8 bars)
         'C6:1.5 Bb5:0.5 G#5:1 G5:1 F5:1.5 E5:0.5 Eb5:1 D5:1 C#5:2 Eb5:2 C#5:2 Eb5:2')
RUN = mel('D5:.25 F5:.25 G#5:.25 A5:.25 Bb5:.25 A5:.25 G#5:.25 F5:.25 ' * 2 +                 # the desperate runs (8 bars)
          'Eb5:.25 G5:.25 Bb5:.25 C6:.25 Db6:.25 C6:.25 Bb5:.25 G5:.25 ' * 2 +
          'D5:.25 F5:.25 G#5:.25 A5:.25 Bb5:.25 C6:.25 Db6:.25 D6:.25 Eb6:2 ' +
          'D6:.25 C6:.25 Bb5:.25 G#5:.25 G5:.25 F5:.25 Eb5:.25 D5:.25 C#5:2 ' +
          'D5:.25 F5:.25 G#5:.25 A5:.25 Bb5:.25 A5:.25 G#5:.25 F5:.25 ' * 2 +
          'Bb5:.25 C6:.25 Db6:.25 D6:.25 Eb6:.25 F6:.25 G6:.25 G#6:.25 A6:4 ' +
          'G#6:.5 G6:.5 F6:.5 Eb6:.5 D6:.5 C#6:.5 Eb6:1 D6:2')
CALL = mel('D6:1.5 G#5:.5 Eb6:2 D6:4 r:8')                                                 # the violin's call (4 bars)
ANSWER = mel('r:8 G#5:2 A5:1 Bb5:1 Eb5:4')                                                  # the theremin's answer (4 bars)
WAIL = mel('D5:4 Eb5:4 G#5:6 A5:2 Bb5:4 A5:4 G#5:4 Eb5:4')                                 # the theremin over the dread (8 bars)
CLIMB = mel('D4:8 F4:8 G#4:8 A4:8')                                                         # the theremin climbing in (8 bars)
for _x, _b in ((DEM, 4), (KW, 8), (RUN, 8), (CALL, 4), (ANSWER, 4), (WAIL, 8), (CLIMB, 8)):
    assert bars_of(_x) == _b, (_b, bars_of(_x))

# one chord a bar: (root, minor? ) - the harmony under the theme
PROG = ['D2', 'D2', 'Bb1', 'G#1', 'G1', 'Eb2', 'D2', 'C#2']
PLAN = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]   # the key: section 7 a semitone up


# ---------------------------------------------------------------------- the new voices
def violin_line(notes, beat, amp=0.3, k=0, port=0.035, vib=6.4, depth=0.011, drive=3.2, legato=0.98):
    """THE ELECTRIC VIOLIN: one bowed voice over a whole line - sliding into each note, the vibrato blooming as it holds, the
    bow's rasp in the tone, a violin body's resonances, and then driven: a classical voice pushed through distortion"""
    total = sum(d for _, d in notes) * beat
    n = int((total + 0.3) * SR)
    tgt = np.zeros(n); gate = np.zeros(n); onset = np.zeros(n); accent = np.zeros(n)
    first = next((M(x) for x, _ in notes if x is not None), 62)
    tgt[:] = first + k
    t = 0.0
    for x, d in notes:
        i0, i1 = int(t * SR), int((t + d * beat) * SR)
        if x is not None:
            tgt[i0:] = M(x) + k
            i2 = int((t + d * beat * legato) * SR)
            gate[i0:i2] = 1.0
            onset[i0:i1] = np.arange(i1 - i0) / SR
            a = min(i0 + int(0.04 * SR), n); accent[i0:a] = np.linspace(1, 0, a - i0)
        t += d * beat
    midi = smooth(tgt, port)
    tt = np.arange(n) / SR
    vb = depth * np.clip((onset - 0.12) / 0.3, 0, 1) * np.sin(2 * np.pi * vib * tt)
    fr = 440.0 * 2 ** ((midi - 69) / 12) * (1 + vb)
    s = osc(fr) * 0.7 + osc(fr * 1.003) * 0.3
    bow = bp(R.noise(n), 2500, 7000) * (0.18 + 0.5 * accent)                    # the rasp, harsh on every new stroke
    s = s + bow
    body = (bp(s, 260, 340, 1) * 1.2 + bp(s, 430, 560, 1) * 1.0 + bp(s, 900, 1300, 1) * 0.7 +
            bp(s, 2600, 3600, 1) * 0.9 + bp(s, 4500, 6000, 1) * 0.4)
    y = np.tanh(body * drive) / np.tanh(drive)                                   # the pickup into an overdriven amp
    y = lp(y, 7000) + 0.25 * bp(y, 1800, 2600)
    g = smooth(gate, 0.012)
    return amp * y * g


def violin(tr, t0, notes, amp=0.3, pan=0.0, wet=0.35, **k):
    s = violin_line(notes, tr.beat, amp, **k)
    addc(tr, s, t0, pan, 1, wet)
    e = lp(s, 3000)                                                              # a slap-back delay, wide
    addc(tr, e, t0 + tr.beat * 0.5, -0.6 if pan >= 0 else 0.6, 0.22, min(0.9, wet + 0.25))


_ROD = (1.0, 2.37, 3.81, 5.43, 7.12)


def waterphone(f, dur, amp=1.0, bend=1.4, scrape=0.25, seed=0):
    """THE WATERPHONE: a steel rod bowed over a bowl of water - inharmonic partials, the pitch wavering and sliding as the
    water slops around inside, swelling in and groaning out, with the scrape of the bow"""
    rng = np.random.default_rng(900 + seed)
    t = T(dur); n = len(t)
    f0 = fq(f)
    slosh = smooth(rng.uniform(-1, 1, n // 800 + 2).repeat(800)[:n], 0.25)                # the water moving
    glide = bend * (np.sin(2 * np.pi * rng.uniform(0.15, 0.35) * t + rng.uniform(0, 6)) * 0.6 + slosh * 0.8)
    s = np.zeros(n)
    for i, r in enumerate(_ROD):
        fr = f0 * r * 2 ** (glide * (1 + 0.15 * i) / 12)
        ph = np.cumsum(fr) / SR
        s += np.sin(2 * np.pi * ph + 0.6 * np.sin(2 * np.pi * ph * 1.01)) * (0.8 ** i)
    s /= 2.5
    s += scrape * bp(rng.uniform(-1, 1, n), f0 * 2, f0 * 9) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    swell = np.clip(t / (dur * 0.35), 0, 1) ** 1.5 * np.clip((dur - t) / (dur * 0.5), 0, 1)
    return amp * s * swell


def shriek(dur, amp=1.0, f0='Eb6', seed=0):
    """the waterphone struck hard and bowed fast: a metal scream bending upward"""
    w = waterphone(f0, dur, amp, bend=3.0, scrape=0.6, seed=seed)
    t = T(dur)
    return w * np.exp(-t * 1.4) * 2.2


def arc(amp=1.0, dur=0.9, seed=0):
    """a lightning arc: a crackle of noise in bursts over a falling zap"""
    rng = np.random.default_rng(700 + seed)
    t = T(dur); n = len(t)
    burst = (rng.random(n) > 0.92).astype(float)
    burst = smooth(burst, 0.002)
    cr = hp(rng.uniform(-1, 1, n), 3000) * burst * 3
    return amp * (cr * np.exp(-t * 4) + zap(0.6, 4000, 150, dur)) * env(n, 0.001, 0, 1, 0.05)


def chug(f, dur, amp=1.0):
    """the bass ostinato's note: a driven saw, palm-muted"""
    return mono(f, dur, amp, 'saw', 220, 1400, 22, 2.0, 0.008, 0.6, 0.002, 0.06, 0.3, 0.02, drive=3.5)


# ---------------------------------------------------------------------- the grid
def at(tr, bar, beat=0.0):
    return tr.at(bar, beat)


def root(b, k):
    return M(PROG[b % 8]) + k


def drums(tr, bar, style, amp=1.0):
    t = at(tr, bar); bt = tr.beat
    if style == 'war':                                               # double kick in sixteenths, the backbeat
        for i in range(16): tr.add(ekick(0.36 * amp * (1.3 if i % 4 == 0 else 0.8), 12, 150, 46), t + i * 0.25 * bt, 0, 1, 0.05)
        for x in (1, 3): tr.add(esnare(0.55 * amp), t + x * bt, 0.05, 1, 0.3)
        for i in range(8): tr.add(mhat(0.09 * amp, i % 4 == 3), t + i * 0.5 * bt, 0.35, 1, 0.12)
    elif style == 'march':                                           # driving, but with room for the theme
        for x in (0, 0.75, 1.5, 2, 2.75, 3.5): tr.add(ekick(0.55 * amp), t + x * bt, 0, 1, 0.08)
        for x in (1, 3): tr.add(esnare(0.5 * amp), t + x * bt, 0.05, 1, 0.32)
        for i in range(16): tr.add(mhat(0.06 * amp * (1.5 if i % 4 == 2 else 0.8)), t + i * 0.25 * bt, 0.3, 1, 0.12)
    elif style == 'half':                                            # half time, heavy, a pulse still underneath
        tr.add(ekick(0.7 * amp, 5), t, 0, 1, 0.1); tr.add(ekick(0.4 * amp), t + 1.5 * bt, 0, 1, 0.1)
        tr.add(esnare(0.6 * amp, 160), t + 2 * bt, 0.05, 1, 0.5)
        for i in range(8): tr.add(mhat(0.08 * amp, False), t + i * 0.5 * bt, 0.35, 1, 0.12)
        for i in range(4): tr.add(tom(70, 0.12 * amp, 9, 0.2), t + (i + 0.5) * bt, -0.3, 1, 0.2)


def bassline(tr, bar, k, amp=0.16, pat='16'):
    r = root(bar, k); t = at(tr, bar)
    steps = {'16': [1] * 16, 'gallop': [1, 0, 1, 1] * 4, 'eight': [1, 0] * 8}[pat]
    for i, on in enumerate(steps):
        if on: tr.add(chug(r + 12, tr.beat * 0.22, amp * (1.25 if i % 4 == 0 else 0.85)), t + i * 0.25 * tr.beat, -0.15, 1, 0.08)
    tr.add(sub808(r, tr.barlen * 0.98, amp * 1.4), t, 0, 1, 0.05)


def power(tr, bar, k, amp=0.1, beats=(0,)):
    r = root(bar, k)
    for b in beats:
        tr.add(stab([r + 12, r + 19, r + 24], tr.beat * 0.6, amp, 5000, 500, 9.0), at(tr, bar, b), 0.2, 1, 0.3)


def compose():
    tr = Track('killerwatt', BPM, BARS)
    tr.barlen = tr.beat * 4
    assert round(tr.seconds) == 120
    for s in range(10):
        base = s * SEC; k = PLAN[s]
        for b in range(SEC):
            bar = base + b
            if s in (3, 6):
                drums(tr, bar, 'half')
                bassline(tr, bar, k, 0.14, 'eight')
            else:
                drums(tr, bar, 'war' if s in (0, 4, 7, 8, 9) else 'march')
                bassline(tr, bar, k, 0.16, '16' if s in (4, 8, 9) else 'gallop')
            if b == 0: tr.add(crash(0.42, 3.0), at(tr, bar), 0.3, 1, 0.5)
            if s in (1, 2, 7) and b % 2 == 0: power(tr, bar, k, 0.09, (0,))
            if s == 9: power(tr, bar, k, 0.12, (0, 0.75, 1.5, 2.5, 3))
        bt0 = at(tr, base)

        if s == 0:                                                   # ARC
            ther(tr, bt0, CLIMB, 0.24, -0.2, 0.5, port=0.25)
            for b in (0, 3, 5, 7): tr.add(arc(0.22, 0.9, b), at(tr, base + b, 2.5), (-0.6, 0.6)[b % 2], 1, 0.4)
            tr.add(waterphone('D3', tr.barlen * 4, 0.16, seed=1), at(tr, base + 4), 0.4, 1, 0.6)
        if s == 1:                                                   # THE THEME
            violin(tr, bt0, KW, 0.3, -0.1)
        if s == 2:                                                   # HIS THEME, an octave up, the theremin wrong under it
            violin(tr, bt0, KW, 0.3, -0.1, k=12)
            ther(tr, bt0, tp(KW, 7), 0.17, 0.35, 0.5, port=0.05, echo_=False)
            for b in (2, 6): tr.add(arc(0.18, 0.8, b + 10), at(tr, base + b, 3), 0.5, 1, 0.4)
        if s == 3:                                                   # THE DREAD
            for b, f in ((0, 'D3'), (2, 'G#2'), (4, 'Eb3'), (6, 'C#3')):
                tr.add(waterphone(f, tr.barlen * 3, 0.24, seed=b), at(tr, base + b), (-0.5, 0.5)[b // 2 % 2], 1, 0.55)
            ther(tr, bt0, WAIL, 0.27, 0.15, 0.5, port=0.12)
            tr.add(suck(tr.barlen, 0.22), at(tr, base + 7), 0.2, 1, 0.4)
        if s == 4:                                                   # DESPERATE
            violin(tr, bt0, RUN, 0.27, 0.1, port=0.012, drive=4.0)
            for b in (1, 5): tr.add(arc(0.2, 0.9, b + 20), at(tr, base + b, 1), -0.5, 1, 0.4)
        if s == 5:                                                   # HOSTS: call and answer
            for b in (0, 4):
                violin(tr, at(tr, base + b), CALL, 0.3, -0.25)
                ther(tr, at(tr, base + b), ANSWER, 0.27, 0.3, 0.5, port=0.08)
            tr.add(waterphone('G#2', tr.barlen * 8, 0.13, seed=5), bt0, 0, 1, 0.6)
        if s == 6:                                                   # SLAM
            for b in range(SEC):
                tr.add(boom(0.3, 80, 30, 1.6), at(tr, base + b), 0, 1, 0.2)
                if b % 2 == 1: tr.add(shriek(tr.barlen * 1.2, 0.16, ('Eb6', 'D6', 'G#5', 'C#6')[b // 2], b), at(tr, base + b, 0.5), (-0.5, 0.5)[b // 2 % 2], 1, 0.5)
                if b % 2 == 0: tr.add(arc(0.2, 0.9, b + 30), at(tr, base + b, 2), 0.4, 1, 0.4)
            violin(tr, bt0, mel('D6:8 Eb6:8 G#5:8 C#6:8'), 0.22, -0.1, drive=4.5)
        if s == 7:                                                   # RISING: Eb minor
            violin(tr, bt0, KW, 0.3, -0.1, k=13)
            ther(tr, bt0, tp(KW, 1), 0.2, 0.3, 0.45, port=0.05, echo_=False)
            tr.add(waterphone('Eb3', tr.barlen * 8, 0.12, seed=7), bt0, 0.4, 1, 0.6)
        if s == 8:                                                   # FRENZY: the theme at double speed, twice
            fast = [(x, d / 2) for x, d in KW]
            for kk in (0, 4):
                violin(tr, at(tr, base + kk), fast, 0.29, -0.1, k=12, port=0.015, drive=4.2)
                ther(tr, at(tr, base + kk), tp(fast, 0), 0.18, 0.3, 0.4, port=0.03, echo_=False)
        if s == 9:                                                   # THE BRINK
            violin(tr, bt0, mel('D6:2 Eb6:2 D6:2 C#6:2 D6:1 Eb6:1 D6:1 C#6:1 D6:1 Eb6:1 D6:1 C#6:1 G#5:4 A5:4 Eb6:4 D6:4'), 0.28, -0.1, drive=4.5)
            for b in range(4, 8):
                for i in range(8): tr.add(tom(150 - 12 * i, 0.22, 8, 0.2), at(tr, base + b, i * 0.5), -0.4 + 0.1 * i, 1, 0.25)
            tr.add(riser(tr.barlen * 4, 0.12), at(tr, base + 4), 0, 1, 0.4)
            tr.add(waterphone('D4', tr.barlen * 4, 0.14, bend=2.5, seed=9), at(tr, base + 4), -0.3, 1, 0.5)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'killerwatt_battle.ogg'
    tr = seeded(41, compose)
    _guarded(render(tr, 2.2, 0.27), out, 6)
