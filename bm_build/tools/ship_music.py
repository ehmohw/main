"""3.00: synthesises the music aboard the Overworld's two alien ships (phase250 plays them, as it does the market's theme):

  THE MOTHERSHIP  "Tractor Beam Bossa" (vendor/ship_mothership.ogg) - the Donadians' saucer (phase25, bm:mothership): a
                  little alien lounge - a bubbling synth bass on a bossa line, a drum machine's clave and shaker, a slow
                  wobbling pad, FM-bell arpeggios, bloops, and a gliding THEREMIN with the tune. Playful, a bit mysterious.
                  A minor (dorian), 120 BPM, 36 bars = 72 s.
  THE DREADNOUGHT "The Deep Hive" (vendor/ship_dreadnought.ogg) - the Vorn's red warship (phase32, bm:red_mothership): vast,
                  slow and alien, in the Armada's family (tools/armada_music.py: D with its flat second, THE CALL D-A-Eb, a
                  formant hive choir with a ring in it, struck hull plates) but its own - a sub drone and an engine pulse, a
                  machine hum breathing, a hive choir on chords moving by minor thirds over a D that never leaves, detuned
                  glass, a chittering in the dark, bulkheads struck far off, servos; the hook (all of it octatonic - the
                  half-whole scale - its held notes bending flat) in one wordless gliding voice, ring-modulated bells striking
                  each note. D, 72 BPM, 24 bars = 80 s.

  Each has an INVASION-NIGHT variant on the same tune and length (vendor/ship_mothership_inv.ogg, ship_dreadnought_inv.ogg):
  "Red Alert" aboard the mothership (a two-tone alarm, a kick on every beat, sixteenth-note hats and arpeggios, a nervous gated
  pad, laser zaps, a theremin with its nerves showing), "Battle Stations" aboard the Dreadnought (the same ship woken: a synth
  pulse driven in sixteenths, the hull beaten, metal ticks, the choir's breath pulsing, ring-modulated alarm stabs, the hive's
  tritone alarm).

All synthesised (the mothership with tools/market_music.py's instruments, the Dreadnought mostly with its own below) on
market_music's circular Track (notes and reverb running past the end wrap to the start, so each loops without a seam; the
Dreadnought's never-ending layers are tuned to whole cycles of the loop or cross-faded round it - bed(), LoopTrack), mastered
as the market's theme is: -15 LUFS integrated, sample peak under -1 dBFS after the Vorbis encode. Deterministic; run it to rebuild (needs
numpy, scipy and ffmpeg - never needed to build the packs):
    python3 tools/ship_music.py [mothership] [dreadnought] [inv] [preview DIR]     (no names: all four)"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import market_music as mm
from market_music import (SR, m, hz, tt, noise, lp, hp, bp, adsr, additive, Track, at_beat, play, glide, rhodes, synbass,
                          kick909, clap, hat, siren, zap, stab, tom, crash)

KINDS = {'m': (0, 3, 7), 'M': (0, 4, 7), 'm7': (0, 3, 7, 10), 'M7': (0, 4, 7, 11), '7': (0, 4, 7, 10), '9': (0, 4, 7, 10, 14),
         'm9': (0, 3, 7, 10, 14), 'hd': (0, 3, 6, 10), '13': (0, 4, 10, 14, 21), '7#9': (0, 4, 10, 15)}


def ch(bar, chart, beat=0.0):
    c = chart[bar % len(chart)]
    cur = c[0]
    for e in c:
        if e[0] <= beat: cur = e
    return m(cur[1]), cur[2]


def voicing(r, kind, lo='E3', hi='C4'):
    vs = [r + v for v in KINDS[kind][1:]] + [r + 12]
    while min(vs) < m(lo): vs = [v + 12 for v in vs]
    while min(vs) > m(hi): vs = [v - 12 for v in vs]
    return vs


# ====================================================================== the ships' own instruments
def fmbell(x, dur=1.2, amp=1.0):
    f = hz(x); t = tt(max(dur, 0.9)); n = len(t)
    idx = 2.2 * np.exp(-t * 6) + 0.3
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * 3.5 * t)) * np.exp(-t * 3.2)
    return amp * s * adsr(n, 0.001, 0, 1, 0.1)


def pad(notes, dur, amp=1.0, cut=1400, wob=0.25, gate=0.0):
    """a slow pad: detuned sawtooths, a filter breathing open and shut (wob Hz); gate > 0: chopped into that many pulses a second"""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for x in notes:
        for c in (-11, 0, 11):
            s += additive(np.full(n, hz(x) * 2 ** (c / 1200)), lambda k, fk: (1.0 / k) / (1 + (fk / 5000) ** 2), n)
    s /= 3 * max(1, len(notes)) ** 0.7
    lo, hi = lp(s, cut * 0.4), lp(s, cut * 1.6)
    w = 0.5 + 0.5 * np.sin(2 * np.pi * wob * t)
    s = lo + (hi - lo) * w
    if gate: s *= 0.35 + 0.65 * (np.sin(np.pi * gate * t) ** 2)
    return amp * s * adsr(n, 0.4, 0.2, 0.9, 0.4)


def bloop(amp=1.0, f0=300, f1=1300, dur=0.22):
    t = tt(dur); f = f0 * (f1 / f0) ** np.clip(t / (dur * 0.7), 0, 1)
    f = f * (1 + 0.04 * np.sin(2 * np.pi * 28 * t))
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * adsr(len(t), 0.004, 0.05, 0.8, 0.06)


def shaker(amp=1.0):
    t = tt(0.09)
    return amp * bp(noise(len(t)), 5000, 12000) * np.clip(t / 0.02, 0, 1) * np.exp(-t * 40)


def clave(amp=1.0):
    t = tt(0.12)
    return amp * (np.sin(2 * np.pi * 2500 * t) * np.exp(-t * 45) + 0.3 * np.sin(2 * np.pi * 5100 * t) * np.exp(-t * 80))


def riser(dur, amp=1.0):
    """the tractor beam's hum climbing (a sine sweeping up, a breath of noise behind it)"""
    t = tt(dur); n = len(t)
    f = 200 * 8 ** (t / dur)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6 + bp(noise(n), 1500, 7000) * 0.5
    return amp * s * (t / dur) ** 2 * adsr(n, 0.01, 0, 1, 0.05)


def sub(x, dur, amp=1.0):
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    return amp * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)) * adsr(n, 0.3, 0.1, 1, 0.3)


# ====================================================================== THE MOTHERSHIP: "Tractor Beam Bossa"
MS_BPM, MS_BARS = 120, 36
MS_INTRO = [[(0, 'A1', 'm9')], [(0, 'A1', 'm9')], [(0, 'F1', 'M7')], [(0, 'E1', '7#9')]]
MS_A = [[(0, 'A1', 'm7')], [(0, 'D2', '9')], [(0, 'A1', 'm7')], [(0, 'D2', '9')], [(0, 'F1', 'M7')], [(0, 'E1', '7')], [(0, 'A1', 'm7')], [(0, 'E1', '7')]]
MS_B = [[(0, 'D2', 'm9')], [(0, 'G1', '13')], [(0, 'C2', 'M7')], [(0, 'F1', 'M7')], [(0, 'B1', 'hd')], [(0, 'E1', '7')], [(0, 'A1', 'm7')], [(0, 'E1', '7')]]
MS_CHART = MS_INTRO + MS_A + MS_A + MS_B + MS_A
MS_SEC = ['intro'] * 4 + ['A1'] * 8 + ['A2'] * 8 + ['B'] * 8 + ['A3'] * 8
assert len(MS_CHART) == MS_BARS == len(MS_SEC)
MS_TUNE = [(0, 'E5', 1.5), (1.5, 'A5', .5), (2, 'G5', 1), (3, 'E5', 1),
           (4, 'F#5', 1.5), (5.5, 'E5', .5), (6, 'D5', 1), (7, 'C5', .5), (7.5, 'D5', .5),
           (8, 'E5', 1), (9, 'C5', 1), (10, 'A4', 1.5), (11.5, 'B4', .5),
           (12, 'C5', 1), (13, 'D5', 1), (14, 'F#5', 2),
           (16, 'A5', 1.5), (17.5, 'G5', .5), (18, 'E5', 1), (19, 'C5', 1),
           (20, 'B4', 1), (21, 'G#4', 1), (22, 'D5', 1.5), (23.5, 'C5', .5),
           (24, 'B4', 1), (25, 'A4', 2.5), (27.5, 'E5', .5),
           (28, 'G#5', 1), (29, 'B5', 1), (30, 'E6', 1.5), (31.5, 'D6', .5)]
MS_TUNE_END = [n for n in MS_TUNE if n[0] < 28] + [(28, 'E5', 1.5), (29.5, 'G#4', .5), (30, 'A4', 2)]
MS_BRIDGE = [(0, 'F5', 1), (1, 'A5', 1), (2, 'C6', 1.5), (3.5, 'E6', .5),
             (4, 'D6', 1.5), (5.5, 'B5', .5), (6, 'G5', 1), (7, 'E5', 1),
             (8, 'E5', 1), (9, 'G5', 1), (10, 'B5', 1.5), (11.5, 'C6', .5),
             (12, 'A5', 3), (15, 'G5', 1),
             (16, 'F5', 1), (17, 'D5', 1), (18, 'A5', 1.5), (19.5, 'G5', .5),
             (20, 'G#5', 1.5), (21.5, 'F5', .5), (22, 'E5', 1), (23, 'D5', 1),
             (24, 'C5', 1), (25, 'E5', 1), (26, 'A5', 2),
             (28, 'B5', .5), (28.5, 'C6', .5), (29, 'B5', .5), (29.5, 'G#5', .5), (30, 'E5', 2)]
MS_COUNTER = [(0, 'A4', 3), (4, 'B4', 3), (8, 'G4', 3), (12, 'C5', 3.5), (16, 'D5', 3), (20, 'B4', 3), (24, 'E4', 3), (28, 'G#4', 3.5)]


def mothership(tr, inv=False):
    C = MS_CHART
    for bar in range(MS_BARS):
        sec = MS_SEC[bar]
        r, kind = ch(bar, C)
        while r > m('E2'): r -= 12
        fifth = r + 7
        # the bass: a bossa line (dotted quarter, eighth, dotted quarter, eighth); on an invasion night driving eighths
        line = ([(i / 2, r + (0 if i % 4 != 3 else (12 if i % 8 == 3 else 7)), 0.4) for i in range(8)] if inv else
                [(0, r, 1.3), (1.5, fifth, 0.45), (2, fifth, 1.3), (3.5, r, 0.45)])
        for b, x, d in line:
            tr.add(synbass(x, d * tr.beat, 0.24, bright=0.2, cut=900 + 300 * inv, res=0.5), tr.at(bar, b), -0.05, 1, 0.08)
        # the drum machine
        lvl = {'intro': 0.8, 'A1': 0.9, 'A2': 1.0, 'B': 0.9, 'A3': 1.05}[sec]
        kicks = range(4) if inv else ((0, 2) if sec != 'intro' else (0,))
        for b in kicks: tr.add(kick909(0.34 * lvl), tr.at(bar, b), 0, 1, 0.05)
        claves = (0, 1.5, 3) if bar % 2 == 0 else (1, 2)
        for b in claves: tr.add(clave(0.2 * lvl), tr.at(bar, b), -0.4, 1, 0.3)
        for i in range(16 if inv else 8):
            tr.add(shaker(0.14 * lvl * (1.25 if i % 2 else 0.8)), tr.at(bar, 0) + i * tr.beat * (0.25 if inv else 0.5), 0.45, 1, 0.2)
        if inv:
            for b in (1, 3): tr.add(clap(0.3 * lvl), tr.at(bar, b), 0.1, 1, 0.3)
            for i in range(16): tr.add(hat(0.12 * (1.3 if i % 2 else 0.8)), tr.at(bar, 0) + i * tr.beat / 4, 0.3, 1, 0.1)
        elif sec != 'intro':
            for b in (0.5, 1.5, 2.5, 3.5): tr.add(hat(0.14 * lvl), tr.at(bar, b), 0.3, 1, 0.12)
        if bar in (3, 11, 19, 27, 35):
            for j in range(4): tr.add(tom(('G3', 'E3', 'C3', 'A2')[j], 0.25), tr.at(bar, 3) + j * tr.beat / 4, -0.3 + 0.2 * j, 1, 0.3)
        if bar in (4, 20, 28): tr.add(crash(0.1), tr.at(bar, 0), -0.3, 1, 0.4)
        # the pad, a whole bar, breathing; the Rhodes on the bossa's comp
        tr.add(pad(voicing(r + 12, kind, 'C4', 'A4'), 4 * tr.beat + 0.3, 0.16, 1500 + 500 * (sec == 'B'), wob=0.25, gate=(8 if inv else 0)), tr.at(bar, 0), 0.0, 1, 0.5)
        if sec != 'intro':
            for b, d in ((0, 1.2), (1.5, 0.4), (3, 0.9)) if bar % 2 == 0 else ((0.5, 0.4), (2, 1.2), (3.5, 0.4)):
                tr.add(rhodes(voicing(r, kind), d * tr.beat, 0.22), tr.at(bar, b), -0.4, 1, 0.35)
        # the bubbles: an FM-bell arpeggio (in the intro and the bridge; every bar on an invasion night)
        if sec in ('intro', 'B') or inv:
            tones = [r + 36 + v for v in KINDS[kind]] + [r + 48]
            step = 0.25 if (inv or sec == 'B') else 0.5
            for i in range(int(4 / step)):
                j = i % (2 * len(tones) - 2); j = j if j < len(tones) else 2 * len(tones) - 2 - j
                tr.add(fmbell(tones[j], 0.5, 0.07 if inv else 0.09), tr.at(bar, 0) + i * step * tr.beat, 0.55 * (-1) ** i, 1, 0.45)
    # bloops at the phrases' ends; the tractor beam climbing back to the top
    for bar in (3, 7, 11, 15, 19, 23, 27, 31):
        tr.add(bloop(0.09, *(300, 1300) if bar % 8 == 3 else (1400, 350)), tr.at(bar, 3.5), 0.6 * (-1) ** bar, 1, 0.45)
    tr.add(riser(4 * tr.beat, 0.16), tr.at(35, 0), 0, 1, 0.5)
    # the theremin
    vib = 0.55 if inv else 0.4
    glide(tr, 4, MS_TUNE, 0.1, 0.62, 0.4, vib=vib, rate=6.8 if inv else 6.0, wobble=0.1, glide=0.07)
    glide(tr, 12, MS_TUNE, 0.1, 0.62, 0.4, vib=vib, rate=6.8 if inv else 6.0, wobble=0.1, glide=0.07)
    play(tr, 12, [(b, x, d) for b, x, d in MS_COUNTER], fmbell, -0.4, 0.09, 0.5)
    play(tr, 20, MS_BRIDGE, fmbell, 0.3, 0.3, 0.45)
    glide(tr, 20, MS_COUNTER, -0.2, 0.36, 0.45, k=0, vib=vib, wobble=0.2, glide=0.12)
    glide(tr, 28, MS_TUNE_END, 0.1, 0.64, 0.4, vib=vib, rate=6.8 if inv else 6.0, wobble=0.1, glide=0.07)
    play(tr, 28, MS_TUNE_END, fmbell, 0.4, 0.07, 0.5, k=12)
    if inv:
        for bar in (2, 18, 26):
            tr.add(siren(8 * tr.beat, 0.16, 'E5', 'A#5', 3.0), tr.at(bar, 0), 0.3, 1, 0.4)
        for bar in range(4, MS_BARS, 2):
            tr.add(zap(0.06, f0=mm.G.uniform(2500, 4000)), tr.at(bar, 3.5), mm.G.uniform(-.6, .6), 1, 0.4)
        for bar in (28, 30, 32, 34):                                                     # (red-alert stabs on the last chorus)
            r, kind = ch(bar, C)
            for b in (0, 1.5): tr.add(stab(voicing(r + 12, kind, 'G3', 'E4'), 0.4 * tr.beat, 0.22), tr.at(bar, b), -0.2, 1, 0.35)


# ====================================================================== THE DREADNOUGHT: "The Deep Hive"
# The Vorn's own family (tools/armada_music.py: D with its flat second, THE CALL D-A-Eb, a formant hive choir with a ring in
# it, struck hull plates) - but not the Armada's synth fleet: no arpeggiator, no theremin, no beat. Vast, slow and wrong: the
# whole tune is octatonic (D Eb F F# G# A B C - the half-whole scale, nothing in it a sailor could sing), the chords move by
# minor thirds over a D that never leaves, and the notes bend off their pitch as they hold.
DN_BPM, DN_BARS = 72, 24                    # (a bar: 3 1/3 s; 24 bars = 80 s)
DN_KINDS = {'m': (0, 3, 7), 'M': (0, 4, 7), 'phr': (0, 1, 7)}
DN_OCT = (0, 1, 3, 4, 6, 7, 9, 10)          # (the half-whole scale's steps)
DN_PH1 = [('D2', 'm'), ('D2', 'm'), ('Ab1', 'm'), ('B1', 'm')]
DN_PH2 = [('D2', 'm'), ('F1', 'm'), ('Ab1', 'm'), ('D2', 'phr')]
DN_CHART = ([('D2', 'm'), ('D2', 'm'), ('Ab1', 'm'), ('D2', 'phr')] + DN_PH1 + DN_PH2 +
            [(r, k) for r, k in ((m(x) - 3, k) for x, k in DN_PH1 + DN_PH2)] + [('D2', 'm'), ('D2', 'm'), ('Ab1', 'm'), ('D2', 'phr')])
DN_SEC = ['intro'] * 4 + ['A'] * 8 + ['B'] * 8 + ['outro'] * 4
assert len(DN_CHART) == DN_BARS == len(DN_SEC)
# the hook: THE CALL (D A Eb) bending flat, falling down the scale; then again, sliding down the last semitone into D
DN_HOOK = [(0, 'D5', 2), (2, 'A5', 1), (3, 'Eb6', 3, -60), (6, 'C6', 1), (7, 'B5', 1),
           (8, 'G#5', 3), (11, 'A5', 1), (12, 'F#5', 2), (14, 'F5', 2, -45),
           (16, 'D5', 2), (18, 'A5', 1), (19, 'Eb6', 2), (21, 'D6', 1), (22, 'C6', 2),
           (24, 'B5', 1.5), (25.5, 'G#5', .5), (26, 'A5', 2), (28, 'Eb5', 4, -100)]
DN_HOOK_END = [n for n in DN_HOOK if n[0] < 12] + [(12, 'Eb5', 4, -100)]
DN_CALL = [(0, 'D4', 3), (3, 'A4', 1), (4, 'Eb5', 4, -40)]


def dn_chord(bar):
    r, kind = DN_CHART[bar % DN_BARS]
    return m(r), kind


def mf(x):
    return 440.0 * 2 ** ((x - 69) / 12)


def near(x, c):
    """pitch class x in the octave nearest c"""
    return x + 12 * int(round((c - x) / 12))


def lock(f, n):
    """a frequency nudged to a whole number of cycles in n samples - a tone that runs round the loop and meets itself"""
    return max(1, round(f * n / SR)) * SR / n


def onepole(x, sec, x0=None):
    from scipy.signal import lfilter
    k = np.exp(-1 / max(1.0, sec * SR))
    return lfilter([1 - k], [1, -k], x, zi=[(x[0] if x0 is None else x0) * k])[0]


def bed(tr, fn, xf=4.0, pan=0.0, gain=1.0, wet=0.3, coherent=True):
    """a layer the whole loop long: rendered a little past the end and its overrun cross-faded into its start"""
    n, k = tr.n, int(xf * SR)
    s = fn(n + k, n)
    w = np.linspace(0, 1, k)
    if not coherent: w = np.sin(w * np.pi / 2) ** 2
    out = s[:n].copy()
    out[:k] = s[:k] * (np.sqrt(w) if not coherent else w) + s[n:n + k] * (np.sqrt(1 - w) if not coherent else 1 - w)
    tr.add(out, 0.0, pan, gain, wet)


def _harm(ph, fmax, k_max=24, tilt=1.0):
    s = np.zeros_like(ph); k = 1
    while k <= k_max and k * fmax < SR * 0.45:
        s += np.sin(2 * np.pi * k * ph + 0.37 * k) / k ** tilt; k += 1
    return s


DN_VOW = {'a': (730, 1090, 2440), 'o': (570, 840, 2410), 'u': (330, 800, 2240), 'i': (300, 2200, 2950), 'e': (530, 1840, 2480)}


def _vowel(s, v, gains=(1.0, 0.55, 0.25)):
    return sum(bp(s, f * 0.88, f * 1.12) * g for f, g in zip(DN_VOW[v], gains))


def singer(line, amp=1.0, vowels=('u', 'o'), morph=0.09, port=0.11, vib=3.1, depth=0.18, ring=0.35, voices=3, legato=0.97):
    """THE HIVE'S VOICE: one wordless throat (three, a hair apart) carrying a whole line - gliding note to note, every held note
    bending off its pitch (line: (start s, midi, length s, bend cents)), a slow wide vibrato, a vowel turning over, and the
    hive's ring under it (a copy ring-modulated a fifth and a hair up); -> (signal, start s)"""
    t0 = line[0][0]; end = max(a + d for a, _x, d, _b in line)
    n = int((end - t0 + 0.9) * SR); t = np.arange(n) / SR
    tgt = np.full(n, float(line[0][1])); gate = np.zeros(n); onset = np.zeros(n)
    for a, x, d, bend in line:
        i0 = int((a - t0) * SR); i1 = min(n, int((a + d - t0) * SR))
        seg = np.arange(i1 - i0) / SR
        tgt[i0:] = x + bend / 100.0
        tgt[i0:i1] = x + bend / 100.0 * np.clip((seg - 0.4 * d) / (0.55 * d), 0, 1) ** 1.6
        gate[i0:i0 + int(d * legato * SR)] = 1
        onset[i0:i1] = seg
    semis = onepole(tgt, port) + depth * np.clip(onset / 0.7, 0, 1) * np.sin(2 * np.pi * vib * t + 0.4)
    f = mf(semis); fmax = f.max()
    src = np.zeros(n)
    for v in range(voices):
        c = (v - (voices - 1) / 2) * 7.0
        ph = np.cumsum(f * 2 ** (c / 1200) * (1 + 0.002 * np.sin(2 * np.pi * (0.23 + 0.11 * v) * t))) / SR
        src += _harm(ph + 0.21 * v, fmax)
    w = 0.5 + 0.5 * np.sin(2 * np.pi * morph * t - np.pi / 2)
    y = _vowel(src, vowels[0]) * (1 - w) + _vowel(src, vowels[1]) * w
    if ring:
        ph = np.cumsum(f) / SR
        y = y + ring * bp(y * np.sin(2 * np.pi * 1.503 * ph), 250, 5000)
    g = onepole(onepole(gate, 0.06), 0.04)
    y = y * g
    y *= 0.3 / (np.sqrt((y[g > 0.5] ** 2).mean()) + 1e-9)
    return amp * y, t0


def choir(notes, dur, amp=1.0, vowel='u', to='o', attack=1.2, release=1.5, voices=4, ring=0.25, gate=0.0, rate=0.0):
    """the hive choir on a chord: many throats on one breath, drifting, the vowel opening as it holds (a ring inside it);
    gate/rate: the breath pulsed (the hive's chatter, on an invasion night)"""
    t = tt(dur); n = len(t)
    src = np.zeros(n)
    for x in notes:
        f = mf(m(x))
        for v in range(voices):
            dv = 0.006 * (v - (voices - 1) / 2) / max(1, (voices - 1) / 2)
            ph = np.cumsum(np.full(n, f * (1 + dv)) * (1 + 0.005 * np.sin(2 * np.pi * (4.1 + 0.33 * v) * t + mm.G.uniform(0, 6)))) / SR
            src += _harm(ph + mm.G.uniform(0, 1), f * 1.02, 18)
    src /= len(notes) * voices
    w = np.clip(t / max(dur * 0.8, 0.1), 0, 1); w = w * w * (3 - 2 * w)
    y = _vowel(src, vowel) * (1 - w) + _vowel(src, to) * w
    if ring: y = y + ring * bp(y * np.sin(2 * np.pi * mf(m(notes[0])) * 1.503 * t), 250, 5000)
    if gate: y = y * (1 - gate * (0.5 - 0.5 * np.cos(2 * np.pi * rate * t)))
    return amp * 6.0 * y * adsr(n, attack, 0, 1, release)


def glass(notes, dur, amp=1.0, attack=1.6, release=1.8, shimmer=0.19):
    """a glassy pad: each note three sines a few cents apart, beating, with stretched (not quite harmonic) partials over them"""
    t = tt(dur); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = mf(m(x))
        for c in (-17, 0, 13):
            fd = f * 2 ** (c / 1200)
            for r, a in ((1, 1), (2.0, 0.3), (3.02, 0.14), (4.23, 0.08), (5.47, 0.04)):
                if fd * r < 15000: s += a * np.sin(2 * np.pi * fd * r * t + mm.G.uniform(0, 6.3))
    s /= 3 * len(notes) ** 0.8
    s *= 1 + 0.2 * np.sin(2 * np.pi * shimmer * t + mm.G.uniform(0, 6.3))
    return amp * s * adsr(n, attack, 0, 1, release)


def ringbell(x, dur=3.0, amp=1.0, bend=0.0, bright=1.0):
    """the hive bell: FM at an irrational ratio (root two) with a ring-modulated clang in its strike - metal no one tuned"""
    f = mf(m(x) if not isinstance(x, float) else x); t = tt(dur); n = len(t)
    fr = f * 2 ** (bend / 1200 * np.clip(t / dur, 0, 1) ** 1.5)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    idx = bright * (2.6 * np.exp(-t * 5) + 0.5 * np.exp(-t * 0.9))
    s = np.sin(ph + idx * np.sin(ph * 1.4142))
    s += 0.4 * np.sin(ph) * np.sin(ph * 2.756) * np.exp(-t * 4)
    s += 0.18 * np.sin(ph * 2.0 + 1) * np.exp(-t * 2.2)
    return amp * s * np.exp(-t * 1.3) * adsr(n, 0.002, 0, 1, 0.2)


def chit(x, amp=1.0, dur=0.075):
    """one click of the hive's chittering: a tiny FM chirp, fluttering like a wing-case"""
    f = mf(m(x)); t = tt(dur)
    fr = f * (1 + 0.08 * np.exp(-t * 60))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    s = np.sin(ph + 1.6 * np.sin(ph * 1.5)) * (0.55 + 0.45 * np.sin(2 * np.pi * 85 * t))
    return amp * s * np.exp(-t * 38) * adsr(len(t), 0.001, 0, 1, 0.01)


def throb(amp=1.0, f0=95.0, f1=37.0, dec=2.2):
    """the engines' pulse: an enormous soft sine, sagging in pitch, felt more than heard"""
    t = tt(2.2); n = len(t)
    fr = f1 + (f0 - f1) * np.exp(-t * 18)
    s = np.tanh(1.5 * np.sin(2 * np.pi * np.cumsum(fr) / SR)) / np.tanh(1.5)
    s += 0.3 * lp(noise(n), 180) * np.exp(-t * 20)
    return amp * s * np.exp(-t * dec) * adsr(n, 0.004, 0, 1, 0.3)


DN_PLATE = ((1.0, 1.0, 1.4), (1.594, 0.8, 1.8), (2.136, 0.7, 2.4), (2.296, 0.55, 2.6), (2.653, 0.45, 3.2), (2.918, 0.35, 3.6),
            (3.156, 0.3, 4.2), (3.501, 0.25, 4.8), (4.06, 0.18, 5.8))


def hullhit(f=90.0, amp=1.0, ring=1.0, thump=1.0, dark=2500):
    """a bulkhead struck somewhere far off in the ship: a steel plate's inharmonic modes over a thud"""
    t = tt(0.6 + 2.6 * ring); n = len(t)
    s = np.zeros(n)
    for r, a, d in DN_PLATE:
        fk = f * r * (1 + 0.01 * mm.G.standard_normal())
        s += a * np.sin(2 * np.pi * fk * t * (1 - 0.004 * np.exp(-t * 6)) + mm.G.uniform(0, 6.3)) * np.exp(-t * d / ring)
    s += thump * lp(noise(n), 240) * np.exp(-t * 12) * 2.0
    s += 0.4 * bp(noise(n), 1200, 5000) * np.exp(-t * 50)
    return amp * lp(s, dark) * adsr(n, 0.001, 0, 1, 0.2) / 2.4


def servo(dur, amp=1.0, f0=160.0, f1=360.0):
    """a great servo moving somewhere: a nasal pulse gliding up and settling"""
    t = tt(dur); n = len(t)
    u = np.clip(t / dur, 0, 1); fr = f0 * (f1 / f0) ** (u * u * (3 - 2 * u))
    ph = np.cumsum(fr) / SR
    s = np.sign(np.sin(2 * np.pi * ph)) * 0.6 + np.sin(2 * np.pi * 2.01 * ph) * 0.4
    s = bp(s, 500, 2600)
    return amp * s * np.sin(np.pi * u) ** 2 * 0.5


def hiss(dur, amp=1.0, f0=900, f1=4500):
    """hydraulics venting: a band of noise sweeping up and dying"""
    t = tt(dur); n = len(t)
    lo, hi = bp(noise(n), f0, f0 * 3), bp(noise(n), f1 * 0.5, f1 * 1.6)
    w = np.clip(t / dur, 0, 1)
    return amp * (lo * (1 - w) + hi * w) * np.sin(np.pi * w) ** 2


def ralarm(dur, amp=1.0, lo='D5', hi='G#5', rate=1.2):
    """the hive's alarm: two tones a tritone apart whooping in turn, ring-modulated into a clang no siren makes"""
    t = tt(dur); n = len(t)
    up = (np.floor(t * rate * 2) % 2).astype(float)
    semis = onepole(m(lo) + (m(hi) - m(lo)) * up, 0.02)
    ph = np.cumsum(mf(semis)) / SR
    c = np.sin(2 * np.pi * ph) + 0.35 * np.sin(6 * np.pi * ph)
    s = 0.45 * c + 0.8 * c * np.sin(2 * np.pi * 1.414 * ph + 0.5)
    wh = np.sin(np.pi * ((t * rate * 2) % 1.0)) ** 0.6                                   # (each tone whooped)
    return amp * lp(s, 5000) * wh * adsr(n, 0.01, 0, 1, 0.08) * 0.5


def rstab(notes, dur, amp=1.0, mod=1.414):
    """an alarm stab: a chord ring-modulated against itself at an irrational ratio, struck and dying"""
    t = tt(dur); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = mf(m(x))
        ph = f * t
        s += _harm(ph, f, 10) * (0.5 + np.sin(2 * np.pi * mod * ph))
    s /= len(notes)
    e = np.exp(-t * 7)
    s = lp(s, 700) + (lp(s, 5000) - lp(s, 700)) * np.exp(-t * 14)
    s = np.tanh(2.5 * s / (np.abs(s).max() + 1e-9))                                     # (its spikes rounded off)
    return amp * s * e * adsr(n, 0.004, 0, 1, 0.05)


def mtick(amp=1.0):
    """a metal tick: clashing high partials, gone at once"""
    t = tt(0.06); n = len(t)
    s = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate((3311, 4870, 5933, 7417, 8862)))
    s = hp(s + 0.6 * noise(n), 4500)
    return amp * s * np.exp(-t * 70) * 0.3


def dn_line(tr, bar0, tune, k=0):
    out = []
    for nt in tune:
        b, bt = at_beat(bar0, nt[0])
        out.append((tr.at(b, bt), m(nt[1]) + k, nt[2] * tr.beat, nt[3] if len(nt) > 3 else 0.0))
    return out


def dn_sing(tr, bar0, tune, pan=0.0, gain=1.0, wet=0.5, k=0, **kw):
    s, t0 = singer(dn_line(tr, bar0, tune, k), **kw)
    tr.add(s, t0, pan, gain, wet)
    e = lp(s, 2200)                                                                      # (the hold answering, far down the hull)
    for i in (1, 2): tr.add(e, t0 + tr.beat * 1.5 * i, -pan + (0.5 if i % 2 else -0.5), gain * 0.28 ** i, 0.85)


def dn_bells(tr, bar0, tune, pan=0.0, gain=1.0, wet=0.5, k=0, bright=1.0):
    for nt in tune:
        b, bt = at_beat(bar0, nt[0])
        d = max(2.5, nt[2] * tr.beat + 1.2)
        s = ringbell(m(nt[1]) + k, d, 1.0, nt[3] if len(nt) > 3 else 0.0, bright)
        t0 = tr.at(b, bt)
        tr.add(s, t0, pan, gain, wet)
        tr.add(lp(s, 3000), t0 + tr.beat * 0.75, -pan, gain * 0.3, 0.8)


def dreadnought(tr, inv=False):
    n = tr.n
    # ---- the beds, the whole loop long: the sub drone on D (and its fifth, coming and going), the machine hum (D's overtones
    # each breathing on its own slow cycle, a filter no one is turning), a mains-like buzz beating against itself, the air
    def drone(N, n):
        t = np.arange(N) / SR
        f2, f1, fa = lock(mf(m('D2')), n), lock(mf(m('D1')), n), lock(mf(m('A1')), n)
        s = 0.8 * np.sin(2 * np.pi * f2 * t) + 0.55 * np.sin(2 * np.pi * f1 * t)
        s += 0.3 * np.sin(2 * np.pi * fa * t) * (0.5 + 0.5 * np.sin(2 * np.pi * lock(0.0375, n) * t))
        return s * (0.78 + 0.22 * np.sin(2 * np.pi * lock(0.05, n) * t))
    bed(tr, drone, gain=0.11 if not inv else 0.09, wet=0.05)
    def hum(N, n):
        t = np.arange(N) / SR
        f = lock(mf(m('D2')), n)
        s = np.zeros(N)
        for k in range(1, 14):
            rk = lock(0.025 + 0.0125 * ((k * 7) % 5), n)
            s += (1.0 / k) * (0.5 + 0.5 * np.sin(2 * np.pi * rk * t + k * 1.7)) ** 2 * np.sin(2 * np.pi * k * f * t + k)
        fb = lock(mf(m('D3')), n)
        s += 0.12 * (np.sin(2 * np.pi * fb * t) + np.sin(2 * np.pi * (fb + lock(0.3, n)) * t)) * np.sign(np.sin(2 * np.pi * fb * 3 * t)) * 0.5
        return s
    bed(tr, hum, gain=0.045, wet=0.25, pan=-0.1)
    def air(N, n):
        t = np.arange(N) / SR
        return bp(noise(N), 2600, 7500) * (0.4 + 0.6 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t)) ** 2)
    bed(tr, air, gain=0.04 if not inv else 0.05, wet=0.6, pan=0.3, coherent=False)

    for bar in range(DN_BARS):
        sec = DN_SEC[bar]
        r, kind = dn_chord(bar)
        tones = [r + v for v in DN_KINDS[kind]]
        lvl = {'intro': 0.8, 'A': 1.0, 'B': 1.05, 'outro': 0.85}[sec]
        # the bass: the chord's root, held, under the drone
        tr.add(sub(r, 4 * tr.beat + 0.6, 0.15 * lvl), tr.at(bar, 0), 0, 1, 0.05)
        # the engines' pulse: once a bar, and once more off the beat (a heart with something wrong in it)
        tr.add(throb(0.36 * lvl), tr.at(bar, 0), 0, 1, 0.12)
        if sec != 'intro' or bar >= 2: tr.add(throb(0.2 * lvl, dec=3.0), tr.at(bar, 2.5), 0, 1, 0.15)
        # the hive choir on the chord, the vowel opening as it holds; glass above it
        v = sorted(set(near(x, m('A3')) for x in tones))
        vow = {'intro': ('u', 'u'), 'A': ('u', 'o'), 'B': ('o', 'a'), 'outro': ('u', 'o')}[sec]
        tr.add(choir(v, 4 * tr.beat + 1.4, 0.2 * lvl, vow[0], vow[1], gate=0.55 if inv else 0, rate=4 / tr.beat if inv else 0),
               tr.at(bar, 0) - 0.4, -0.25, 1, 0.55)
        if sec != 'intro' or bar >= 2:
            gl = sorted(set(near(x, m('F5')) for x in tones))
            tr.add(glass(gl, 4 * tr.beat + 1.6, 0.2 * lvl), tr.at(bar, 0) - 0.5, 0.35, 1, 0.65)
        # the hive chittering: bursts of tiny chirps running up and down the scale, somewhere in the dark
        if sec != 'intro' or bar >= 2 or inv:
            g = np.random.default_rng(700 + bar)
            bursts = (4 if inv else 2) + (1 if sec == 'B' else 0)
            for _ in range(bursts):
                b0 = g.integers(0, 14) / 4.0
                ln = int(g.integers(3, 7)); st = int(g.integers(0, 8)); dirn = 1 if g.random() < 0.6 else -1
                pan = g.uniform(-0.8, 0.8)
                for j in range(ln):
                    s_ = (st + dirn * j) % 16
                    x = r + 36 + DN_OCT[s_ % 8] + 12 * (s_ // 8)
                    while x > m('D7'): x -= 12
                    while x < m('A5'): x += 12
                    tr.add(chit(x, 0.32 * (0.7 + 0.3 * g.random())), tr.at(bar, 0) + (b0 + j / 8) * tr.beat, pan, 1, 0.55)
        # the ship itself: bulkheads struck far off, a servo, the hydraulics
        g = np.random.default_rng(900 + bar)
        if bar % 2 == 1 or sec == 'intro':
            tr.add(hullhit(g.uniform(70, 130), 0.38, 1.2, 0.6, 1800), tr.at(bar, 0) + g.uniform(0.5, 3.5) * tr.beat, g.uniform(-0.7, 0.7), 1, 0.85)
        if bar % 4 == 3: tr.add(hullhit(58, 0.45, 1.6, 1.0, 1400), tr.at(bar, 3.5), -0.2, 1, 0.8)
        if bar in (5, 13, 21): tr.add(servo(2.4, 0.5), tr.at(bar, 1.5), 0.6, 1, 0.7)
        if bar in (7, 15, 23): tr.add(hiss(2.0, 0.45), tr.at(bar, 1), -0.6, 1, 0.7)
        if bar in (2, 10, 18): tr.add(servo(3.0, 0.4, 120, 90), tr.at(bar, 0.5), -0.5, 1, 0.75)

    # ---- the tunes: THE CALL in the choir to begin; the hook (the hive's voice, the bells striking each note); in the middle
    # the bells take it a minor third down and the voice sings it an octave under them; the end, and the slide home into D
    dn_sing(tr, 0, DN_CALL, -0.3, 0.55, 0.6, vowels=('u', 'o'), ring=0.4)
    dn_sing(tr, 4, DN_HOOK, 0.1, 0.65, 0.45, vowels=('u', 'o'))
    dn_bells(tr, 4, DN_HOOK, 0.3, 0.28, 0.5)
    dn_bells(tr, 12, DN_HOOK, 0.25, 0.36, 0.5, k=-3, bright=1.2)
    dn_sing(tr, 12, DN_HOOK, -0.15, 0.5, 0.5, k=-15, vowels=('o', 'a'), ring=0.45)
    dn_sing(tr, 20, DN_HOOK_END, 0.1, 0.48, 0.55, vowels=('u', 'o'))
    dn_bells(tr, 20, DN_HOOK_END, -0.3, 0.22, 0.6, k=-12)

    if inv:
        # ---- BATTLE STATIONS: the same ship, woken - the pulse driven in sixteenths, the hull beaten, ticks, the alarm
        pat = (0, 0, 12, 0, 1, 0, 0, 12, 0, 0, 13, 0, 0, 1, 12, 0)
        for bar in range(DN_BARS):
            sec = DN_SEC[bar]
            r, kind = dn_chord(bar)
            while r > m('F2'): r -= 12
            lvl = {'intro': 0.85, 'A': 1.0, 'B': 1.05, 'outro': 0.9}[sec]
            for i, o in enumerate(pat):
                acc = 1.0 if i % 4 == 0 else 0.7
                tr.add(synbass(r + o, 0.2 * tr.beat, 0.22 * acc * lvl, bright=0.3, cut=650 + 250 * (i % 4 == 0), res=0.6),
                       tr.at(bar, 0) + i * tr.beat / 4, -0.05, 1, 0.08)
            for b in (0, 1.5, 2, 3.5) if sec != 'intro' else (0, 2):
                tr.add(hullhit(64 if b % 2 == 0 else 82, 0.42 * lvl, 0.5, 1.6, 2200), tr.at(bar, b), 0.05, 1, 0.35)
            for i in range(8 if sec != 'B' else 16):
                st = 8 if sec != 'B' else 16
                tr.add(mtick(0.5 * (1.3 if i % 2 else 0.8)), tr.at(bar, 0) + i * 4 / st * tr.beat, 0.4, 1, 0.3)
            if sec != 'intro' and bar % 2 == 1:
                hi = sorted(set(near(x, m('E4')) for x in [r + v for v in DN_KINDS[kind]] + [r + 1]))
                for b in (1.5, 3.5): tr.add(rstab(hi, 0.9, 0.85 * lvl), tr.at(bar, b), 0.25, 1, 0.4)
        for bar in (0, 12, 20):
            tr.add(ralarm(8 * tr.beat, 0.6), tr.at(bar, 0), -0.35, 1, 0.5)


SHIPS = {'mothership': (mothership, MS_BPM, MS_BARS, 3001), 'dreadnought': (dreadnought, DN_BPM, DN_BARS, 3002)}


class LoopTrack(Track):
    """market_music's Track, its final rumble filter (a high-pass at 36 Hz) run round the loop too: Track.render starts that
    filter from silence, harmless under the mothership's quiet start but a click under a drone that never stops"""
    def render(self, room=1.7):
        hp0 = mm.hp
        def hp_circ(x, fc, order=2):
            k = 2 * SR
            return hp0(np.concatenate([x[..., -k:], x], axis=-1), fc, order)[..., k:]
        mm.hp = hp_circ
        try: return Track.render(self, room)
        finally: mm.hp = hp0


def build(name, inv=False):
    part, bpm, bars, seed = SHIPS[name]
    mm.G = np.random.default_rng(seed + 10 * inv)
    tr = (Track if name == 'mothership' else LoopTrack)(bars=bars, beat=60.0 / bpm, swing=0.5)
    part(tr, inv)
    return tr.render(room=1.9 if name == 'mothership' else 3.4)


def stem(name, inv=False):
    return f'ship_{name}' + ('_inv' if inv else '')


if __name__ == '__main__':
    args = sys.argv[1:]
    d = args[args.index('preview') + 1] if 'preview' in args else None
    names = [a for a in args if a in SHIPS] or list(SHIPS)
    invs = [True] if 'inv' in args and 'base' not in args else ([False] if 'base' in args else [False, True])
    for name in names:
        for inv in invs:
            out = os.path.join(mm.VENDOR, stem(name, inv) + '.ogg')
            y, L, pk = mm.master(build(name, inv), out)
            mm.seam_check(y)
            if d: mm.preview(y, os.path.join(d, stem(name, inv) + '.mp3'))
