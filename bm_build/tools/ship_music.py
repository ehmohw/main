"""3.00: synthesises the music aboard the Overworld's two alien ships (phase250 plays them, as it does the market's theme):

  THE MOTHERSHIP  "Tractor Beam Bossa" (vendor/ship_mothership.ogg) - the Donadians' saucer (phase25, bm:mothership): a
                  little alien lounge - a bubbling synth bass on a bossa line, a drum machine's clave and shaker, a slow
                  wobbling pad, FM-bell arpeggios, bloops, and a gliding THEREMIN with the tune. Playful, a bit mysterious.
                  A minor (dorian), 120 BPM, 36 bars = 72 s.
  THE DREADNOUGHT "Hive Iron March" (vendor/ship_dreadnought.ogg) - the Vorn's red warship (phase32, bm:red_mothership): heavy
                  and military - a galloping low-string ostinato, war drums and a marching snare, struck hull plates, a sub
                  drone, horns and trombones with the theme, trumpets over the chorale. D minor, 96 BPM, 32 bars = 80 s.

  Each has an INVASION-NIGHT variant on the same tune and length (vendor/ship_mothership_inv.ogg, ship_dreadnought_inv.ogg):
  "Red Alert" aboard the mothership (a two-tone alarm, a kick on every beat, sixteenth-note hats and arpeggios, a nervous gated
  pad, laser zaps, a theremin with its nerves showing), "Battle Stations" aboard the Dreadnought (a klaxon, the snare doubled to
  sixteenths, the ostinato driven in sixteenths, timpani, trumpet stabs).

All synthesised with tools/market_music.py's own instruments and its circular Track (notes and reverb running past the end wrap
to the start, so each loops without a seam), mastered as the market's theme is: -15 LUFS integrated, sample peak under -1 dBFS
after the Vorbis encode. Deterministic; run it to rebuild (needs numpy, scipy and ffmpeg - never needed to build the packs):
    python3 tools/ship_music.py [mothership] [dreadnought] [inv] [preview DIR]     (no names: all four)"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import market_music as mm
from market_music import (SR, m, hz, tt, noise, lp, hp, bp, adsr, additive, formant, _pitch, Track, at_beat, play, glide,
                          rhodes, synbass, kick909, clap, hat, siren, zap, blip, stab, glide_line, bowed, timp, boom, crash,
                          tom, trumpet, ride)

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


def horn(x, dur, amp=1.0, bright=0.5, **_):
    """horns and trombones: additive brass, a dark formant, a swell into long notes, the lip's blat on the attack"""
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    fr = _pitch(n, f, 0.25, 0, 0.1 if dur > 0.6 else 0, 0.3, 5.0)
    s = additive(fr, lambda k, fk: k ** -0.8 * formant(fk, 650 + 700 * bright, 0.7, 1.5) / (1 + (fk / (1600 + 2600 * bright)) ** 4), n) / 5
    swell = 1 + 0.25 * np.clip(t / max(dur, 0.3), 0, 1)
    return amp * s * swell * (1 + 0.5 * np.exp(-t * 20)) * adsr(n, 0.04, 0.1, 0.85, 0.08)


def snare(amp=1.0, tight=1.0):
    t = tt(0.3); n = len(t)
    s = bp(noise(n), 1500, 9000) * np.exp(-t * 22 * tight) + 0.6 * np.sin(2 * np.pi * 200 * t) * np.exp(-t * 35)
    s += 0.5 * hp(noise(n), 4000) * np.exp(-t * 12 * tight)                                # (the wires)
    return amp * s * 0.7


def plate(amp=1.0, f=180.0):
    """a struck hull plate: a few inharmonic partials ringing, the strike's clank"""
    t = tt(1.4); n = len(t)
    s = np.zeros(n)
    for r, a, d in ((1, 1, 3), (2.32, .7, 4), (3.87, .5, 5), (5.21, .35, 7), (7.13, .25, 9)):
        s += a * np.sin(2 * np.pi * f * r * t + mm.G.uniform(0, 6)) * np.exp(-t * d)
    s += 0.6 * bp(noise(n), 1500, 6000) * np.exp(-t * 60)
    return amp * s / 2.5 * adsr(n, 0.001, 0, 1, 0.2)


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


# ====================================================================== THE DREADNOUGHT: "Hive Iron March"
DN_BPM, DN_BARS = 96, 32
DN_INTRO = [[(0, 'D2', 'm')], [(0, 'D2', 'm')], [(0, 'Bb1', 'M')], [(0, 'A1', 'M')]]
DN_A = [[(0, 'D2', 'm')], [(0, 'D2', 'm')], [(0, 'Bb1', 'M')], [(0, 'Bb1', 'M')], [(0, 'G1', 'm')], [(0, 'G1', 'm')], [(0, 'A1', 'M')], [(0, 'A1', 'M')]]
DN_A2 = [[(0, 'D2', 'm')], [(0, 'C2', 'M')], [(0, 'Bb1', 'M')], [(0, 'A1', 'M')], [(0, 'G1', 'm')], [(0, 'Eb2', 'M')], [(0, 'A1', 'M')], [(0, 'A1', '7')]]
DN_B = [[(0, 'Bb1', 'M')], [(0, 'F1', 'M')], [(0, 'G1', 'm')], [(0, 'D2', 'm')], [(0, 'Eb2', 'M')], [(0, 'Bb1', 'M')], [(0, 'A1', 'M')], [(0, 'A1', '7')]]
DN_CODA = [[(0, 'D2', 'm')], [(0, 'Eb2', 'M')], [(0, 'D2', 'm')], [(0, 'A1', '7')]]
DN_CHART = DN_INTRO + DN_A + DN_A2 + DN_B + DN_CODA
DN_SEC = ['intro'] * 4 + ['A1'] * 8 + ['A2'] * 8 + ['B'] * 8 + ['coda'] * 4
assert len(DN_CHART) == DN_BARS == len(DN_SEC)
DN_THEME = [(0, 'D4', 1.5), (1.5, 'D4', .5), (2, 'F4', 1), (3, 'A4', 1),
            (4, 'D5', 2.5), (6.5, 'C5', .5), (7, 'A4', 1),
            (8, 'Bb4', 1.5), (9.5, 'A4', .5), (10, 'G4', 1), (11, 'F4', 1),
            (12, 'D4', 3), (15, 'F4', 1),
            (16, 'G4', 1.5), (17.5, 'G4', .5), (18, 'Bb4', 1), (19, 'D5', 1),
            (20, 'G5', 2), (22, 'F5', 1), (23, 'Eb5', 1),
            (24, 'C#5', 1.5), (25.5, 'D5', .5), (26, 'E5', 1), (27, 'C#5', 1),
            (28, 'A4', 4)]
DN_THEME2 = [n for n in DN_THEME if not 12 <= n[0] < 16] + [(12, 'C#4', 3), (15, 'E4', 1)]
DN_CHORALE = [(0, 'F5', 2), (2, 'D5', 1), (3, 'Bb4', 1), (4, 'C5', 2), (6, 'A4', 1), (7, 'F4', 1),
              (8, 'G4', 1), (9, 'Bb4', 1), (10, 'D5', 1), (11, 'G5', 1), (12, 'F5', 3), (15, 'E5', 1),
              (16, 'Eb5', 2), (18, 'G5', 1), (19, 'Bb5', 1), (20, 'F5', 2), (22, 'D5', 2),
              (24, 'E5', 1.5), (25.5, 'C#5', .5), (26, 'E5', 1), (27, 'G5', 1), (28, 'A5', 3), (31, 'C#5', 1)]


def dreadnought(tr, inv=False):
    C = DN_CHART
    for bar in range(DN_BARS):
        sec = DN_SEC[bar]
        r, kind = ch(bar, C)
        while r > m('F2'): r -= 12
        lvl = {'intro': 0.85, 'A1': 0.95, 'A2': 1.0, 'B': 0.95, 'coda': 1.1}[sec]
        # the ostinato: low strings galloping (an eighth and two sixteenths); on an invasion night straight sixteenths
        if inv: steps = [(i / 4, 0.22) for i in range(16)]
        else: steps = [(b + o, d) for b in range(4) for o, d in ((0, 0.45), (0.5, 0.22), (0.75, 0.22))]
        for i, (b, d) in enumerate(steps):
            x = r + (12 if (inv and i % 8 == 6) else 0)
            acc = 1.0 if b % 1 == 0 else 0.75
            tr.add(bowed(x + 12, d * tr.beat, 0.2 * acc * lvl, 0.55, voices=2, attack=0.01), tr.at(bar, 0) + b * tr.beat, -0.25, 1, 0.25)
        tr.add(sub(r, 4 * tr.beat + 0.2, 0.14), tr.at(bar, 0), 0, 1, 0.05)
        # the war drums: a boom on one and three, the timpani, the hull plates on four; the marching snare
        for b in (0, 2): tr.add(boom(0.5 * lvl), tr.at(bar, b), 0, 1, 0.12)
        if bar % 2 == 0: tr.add(timp(r + 12 if r + 12 <= m('A2') else r, 1.6, 0.4 * lvl), tr.at(bar, 0), 0.1, 1, 0.3)
        tr.add(plate(0.4 * lvl, 160 if bar % 2 else 190), tr.at(bar, 3), 0.45, 1, 0.45)
        if sec != 'intro' or bar >= 2:
            pat = ([i / 4 for i in range(16)] if inv else [0, 1, 1.75, 2, 2.5, 3, 3.25, 3.5])
            for b in pat:
                a = 0.4 if b in (1, 3) else (0.24 if b % 1 == 0 else 0.16)
                tr.add(snare(a * lvl, 1.2), tr.at(bar, 0) + b * tr.beat, 0.15, 1, 0.3)
        if bar % 4 == 3:                                                                 # (a buzz roll into each four bars)
            for j in range(12): tr.add(snare(0.1 + 0.022 * j, 1.6), tr.at(bar, 2) + j * tr.beat / 6, 0.15, 1, 0.3)
        if bar in (4, 12, 20, 28): tr.add(crash(0.14), tr.at(bar, 0), -0.3, 1, 0.4)
        # the brass's chords (low, held) from the theme on
        if sec != 'intro':
            vs = voicing(r, kind, 'D3', 'A3')
            tr.add(stab(vs, 4 * tr.beat, 0.12 if sec != 'B' else 0.16), tr.at(bar, 0), 0.3, 1, 0.4)
    # the theme: horns, trombones an octave down; the second time trumpets above; the chorale with the strings high
    play(tr, 4, DN_THEME, horn, 0.15, 0.62, 0.35)
    play(tr, 4, DN_THEME, horn, -0.15, 0.42, 0.35, k=-12, bright=0.3)
    play(tr, 12, DN_THEME2, horn, 0.15, 0.62, 0.35)
    play(tr, 12, DN_THEME2, horn, -0.15, 0.42, 0.35, k=-12, bright=0.3)
    play(tr, 12, DN_THEME2, trumpet, 0.25, 0.32, 0.35, k=12, muted=False, scoop=0.2)
    play(tr, 20, DN_CHORALE, trumpet, 0.2, 0.5, 0.35, muted=False, scoop=0.15)
    play(tr, 20, DN_CHORALE, horn, -0.2, 0.45, 0.35, k=-12)
    for bar in range(20, 28):
        r, kind = ch(bar, C)
        for v in voicing(r + 24, kind, 'D5', 'A5'):
            tr.add(bowed(v, 4 * tr.beat + 0.2, 0.05, 0.7, trem=(12 if inv else 0), voices=3, attack=0.3), tr.at(bar, 0), 0.4, 1, 0.5)
    for bar, hits in ((28, (0, 1.5)), (29, (0, 1.5)), (30, (0, 1.5, 2.5)), (31, (0,))):
        r, kind = ch(bar, C)
        for b in hits:
            for v in voicing(r + 12, kind, 'D4', 'A4'):
                tr.add(horn(v, 0.45 * tr.beat, 0.4), tr.at(bar, b), 0.1, 1, 0.35)
                tr.add(horn(v - 12, 0.45 * tr.beat, 0.3, bright=0.3), tr.at(bar, b), -0.1, 1, 0.35)
    if inv:
        for bar in (0, 2, 18, 26):                                                       # (the klaxon)
            tr.add(siren(4 * tr.beat, 0.14, 'D5', 'Ab5', 1.6), tr.at(bar, 0), -0.35, 1, 0.45)
        for bar in range(4, DN_BARS):
            if bar % 2: continue
            r, kind = ch(bar, C)
            tr.add(stab(voicing(r + 12, kind, 'A3', 'F4'), 0.35 * tr.beat, 0.2), tr.at(bar, 3.5), 0.2, 1, 0.3)
        for bar in range(4, DN_BARS, 4):
            tr.add(timp('D2', 1.2, 0.35, roll=2 * tr.beat), tr.at(bar + 3, 2), 0, 1, 0.3)


SHIPS = {'mothership': (mothership, MS_BPM, MS_BARS, 3001), 'dreadnought': (dreadnought, DN_BPM, DN_BARS, 3002)}


def build(name, inv=False):
    part, bpm, bars, seed = SHIPS[name]
    mm.G = np.random.default_rng(seed + 10 * inv)
    tr = Track(bars=bars, beat=60.0 / bpm, swing=0.5)
    part(tr, inv)
    return tr.render(room=1.9 if name == 'mothership' else 2.3)


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
