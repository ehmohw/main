"""APOPHISS - battle theme for the climax of Story One. The pipe organ leads. No snake music: no exotic scales, no snake-charmer
reeds - a heavy, hard-fought orchestral battle in G minor, 132 BPM, 66 bars = 120 s loop.

Instruments: pipe organ (lead, harmony, chords and pedal), French horns, trombones, timpani, military snare, a string section in driving
straight sixteenths (spiccato - deliberately unlike Democratus's triplet gallop), choir, cymbals.

  0 THE CALL    timpani, the strings start, the trumpets' call and its answer
  1 THEME       the trumpet theme
  2 THEME II    trumpets in harmony, horns under, the choir
  3 THE STAND   the horns' broad counter-theme, trumpet stabs over it
  4 THE COST    pulled back: low strings, timpani, one trumpet alone with the theme
  5 RALLY       the build: snare rolls, the call passed between trumpets, rising
  6 HIGHER      the theme a step up (A minor), everything
  7 THE STAND   the counter-theme a step up, the trumpets soaring
  8 ALL         the theme home in G minor, full
  9 THE CALL    4 bars: the call hammered, a timpani roll - round again
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track, riser, tom, T, bp, R, env
from boss_music import crash, mel, bars_of
from sovereign_music import boom, render, _guarded, seeded
from armada_music import M, esnare, sub808, addc
from divine_music import horns, bones, choir
from killerwatt_music import violin_line
from armada_music import horn


RANKS = ((0.5, 0.55), (1, 1.0), (2, 0.7), (3, 0.35), (4, 0.4), (6, 0.12), (8, 0.15))   # 16', 8', 4', 2 2/3', 2', 1 1/3', 1'


def organ(notes, d, amp=1.0, ranks=RANKS, chiff=0.25):
    """a pipe organ: stacked ranks of pipes (each a slightly detuned pair), a breathy chiff as each pipe speaks, wind
    pressure flutter, a short release"""
    if not isinstance(notes, (list, tuple)): notes = [notes]
    dur = d + 0.15; t = T(dur); n = len(t); s = np.zeros(n)
    for x in notes:
        f = hz(M(x) if isinstance(x, str) else x)
        for r, g in ranks:
            fr = f * r
            if fr > 8000: continue
            for det in (-0.0009, 0.0011):
                s += g * np.sin(2 * np.pi * fr * (1 + det) * t + R.r() * 6.28)
    s /= len(notes) * len(ranks)
    s *= 1 + 0.01 * np.sin(2 * np.pi * 5.5 * t)
    s += chiff * bp(R.noise(n), 1200, 5000) * np.exp(-t * 30) / max(1, len(notes))
    return amp * 1.8 * s * env(n, 0.03, 0, 1, 0.12)


def trumpet(x, d, amp=1.0):
    """(the lead voice is now the organ, full registration)"""
    return organ([x], d * 1.02, amp)

BPM, BARS = 132, 66

THEME = mel('G4:1 D5:1.5 C5:.5 Bb4:.5 A4:.5 Bb4:1 G4:1 D5:2 Eb5:1.5 D5:.5 C5:1 Bb4:1 A4:3 D4:1 '
            'G4:1 D5:1.5 C5:.5 Bb4:.5 C5:.5 D5:1 G5:1 F5:1 Eb5:1 D5:1 C5:1 Bb4:1 A4:1 G4:2 F#4:2')
STAND = mel('Bb4:2 C5:2 D5:3 Bb4:1 C5:2 D5:2 Eb5:4 F5:2 Eb5:2 D5:2 C5:2 Bb4:2 C5:2 D5:4')
CALL = mel('G4:.5 G4:.5 D5:1 G5:2')                       # 1 bar
ANSWER = mel('F5:.5 Eb5:.5 D5:1 A4:2')
assert bars_of(THEME) == 8 and bars_of(STAND) == 8 and bars_of(CALL) == 1
P_THEME = [('G', 'm'), ('G', 'm'), ('Eb', 'M'), ('D', 'M'), ('G', 'm'), ('C', 'm'), ('C', 'm'), ('D', 'M')]
P_STAND = [('Eb', 'M'), ('G', 'm'), ('C', 'm'), ('C', 'm'), ('Bb', 'M'), ('G', 'm'), ('Eb', 'M'), ('D', 'M')]
P_CALL = [('G', 'm'), ('G', 'm'), ('Eb', 'M'), ('D', 'M')] * 2


def chord(r, q, k=0, octv=2):
    b = M(r + str(octv)) + k
    return [b, b + (4 if q == 'M' else 3), b + 7]


def hz(m): return 440.0 * 2 ** ((m - 69) / 12)


def shift(notes, k): return [(x if x is None else M(x) + k, d) for x, d in notes]


def line(tr, t0, notes, fn, pan, wet):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(fn(x, d * tr.beat), t, pan, 1, wet)
        t += d * tr.beat


def timp(m, amp=1.0, roll=False):
    return tom(hz(m), amp, 3.5 if not roll else 9.0, 0.6)


def strings(tr, bar, r, q, k, amp=0.07, pat='drive'):
    """the string section in sixteenths: root-root-fifth-root, octave leaps on the strong beats"""
    c = chord(r, q, k, 2)
    if pat == 'drive':
        fig = [c[0], c[0], c[2], c[0], c[0] + 12, c[0], c[2], c[0]] * 2
    else:                                                     # 'low': cellos, eighths
        fig = [c[0] - 12, c[0] - 12, c[2] - 12, c[0] - 12] * 2
    u = 4 / len(fig)
    s = violin_line([(x, u) for x in fig], tr.beat, amp, port=0.003, vib=5, depth=0.003, drive=1.3, legato=0.6)
    addc(tr, s, tr.at(bar), -0.3, 1, 0.4)
    addc(tr, s * 0.8, tr.at(bar) + 0.012, 0.3, 1, 0.4)


def drums(tr, bar, style, amp=1.0, root=None):
    t = tr.at(bar); bt = tr.beat
    if style in ('march', 'battle'):
        hits = (0, 1.5, 2.5) if style == 'march' else (0, 0.75, 1.5, 2.5, 3.25)
        for x in hits: tr.add(timp(root if x in (0, 2.5) else root - 5, 0.34 * amp), t + x * bt, 0, 1, 0.35)
        tr.add(boom(0.3 * amp, 65, 26, 1.6), t, 0, 1, 0.3)
        if style == 'battle': tr.add(boom(0.2 * amp, 65, 26, 1.2), t + 2.5 * bt, 0, 1, 0.3)
        tr.add(esnare(0.55 * amp, 140), t + 2 * bt, 0.05, 1, 0.55)
        tr.add(tom(55, 0.22 * amp, 5, 0.4), t + 3.5 * bt, -0.3, 1, 0.35)
    elif style == 'low':
        tr.add(timp(root, 0.32 * amp), t, 0, 1, 0.4); tr.add(timp(root, 0.2 * amp), t + 2.5 * bt, 0, 1, 0.4)
    elif style == 'roll':
        for i in range(16): tr.add(timp(root, (0.08 + 0.02 * i) * amp, True), t + i * 0.25 * bt, 0, 1, 0.35)
        tr.add(boom(0.35 * amp, 60, 24, 2.0), t + 3.75 * bt, 0, 1, 0.3)


def brass_bed(tr, bar, r, q, k, amp=1.0, hold=2):
    c = chord(r, q, k, 3)
    tr.add(organ([c[0], c[1], c[2], c[0] + 12], tr.beat * 4 * hold * 0.97, 0.09 * amp, ((1, 1.0), (2, 0.6), (4, 0.3)), 0.1), tr.at(bar), 0.15, 1, 0.55)
    tr.add(organ([c[0] - 12], tr.beat * 4 * hold * 0.97, 0.1 * amp, ((0.5, 1.0), (1, 0.6), (2, 0.25)), 0.05), tr.at(bar), 0, 1, 0.4)
    tr.add(sub808(c[0] - 12, tr.beat * 4 * 0.98, 0.16 * amp), tr.at(bar), 0, 1, 0.05)


def trp(tr, t0, notes, k=0, amp=0.17, pan=0.1, harm=False):
    line(tr, t0, shift(notes, k), lambda x, d: trumpet(x, d * 0.95, amp), pan, 0.4)
    if harm:                                                  # a second trumpet a diatonic third below
        h = []
        for x, d in notes:
            if x is None: h.append((None, d)); continue
            m = M(x); pc = (m - M('G4')) % 12
            h.append((m - (4 if pc in (0, 2, 7, 11) else 3) + k, d))
        line(tr, t0, h, lambda x, d: trumpet(x, d * 0.95, amp * 0.75), -pan, 0.45)


def stabs(tr, bar, r, q, k, amp=0.12, beats=(0, 1.5, 3)):
    c = chord(r, q, k, 4)
    for b in beats:
        for x in (c[0], c[1], c[2]): tr.add(trumpet(x, tr.beat * 0.35, amp / 2), tr.at(bar, b), 0.25, 1, 0.35)


def compose():
    tr = Track('apophiss', BPM, BARS)
    assert round(tr.seconds) == 120
    bl = tr.beat * 4
    plan = [('call', P_CALL, 0), ('theme', P_THEME, 0), ('theme2', P_THEME, 0), ('stand', P_STAND, 0), ('cost', P_THEME, 0),
            ('rally', P_CALL, 0), ('stand', P_STAND, 0), ('all', P_THEME, 0)]
    for s, (kind, prog, k) in enumerate(plan):
        base = s * 8; t0 = tr.at(base)
        tr.add(crash(0.4 if kind != 'cost' else 0.2, 3.0), t0, 0.3, 1, 0.6)
        for b in range(8):
            bar = base + b; r, q = prog[b]; root = chord(r, q, k, 2)[0]
            if kind == 'cost':
                drums(tr, bar, 'low', 0.9, root); strings(tr, bar, r, q, k, 0.08, 'low')
                if b % 2 == 0: tr.add(choir([x + 12 for x in chord(r, q, k, 3)], bl * 2, 0.06, 0.8, 'u'), tr.at(bar), 0, 1, 0.8)
                continue
            style = 'battle' if kind in ('theme2', 'stand', 'all') else 'march'
            if kind == 'rally' and b in (3, 7): style = 'roll'
            drums(tr, bar, style, 1.0, root)
            strings(tr, bar, r, q, k, 0.075)
            if b % 2 == 0: brass_bed(tr, bar, r, q, k)
            if kind in ('theme2', 'all') and b % 2 == 0:
                tr.add(choir([x + 12 for x in chord(r, q, k, 3)], bl * 2, 0.07, 0.4, 'u'), tr.at(bar), 0, 1, 0.7)
            if kind in ('all', 'stand') or b % 4 == 0: tr.add(crash(0.14), tr.at(bar), (-0.3, 0.3)[b % 2], 1, 0.5)
        if kind == 'call':
            for b in (0, 2, 4, 6):
                trp(tr, tr.at(base + b), CALL, 0, 0.18, 0.15)
                trp(tr, tr.at(base + b + 1), ANSWER, -12, 0.12, -0.2) if b < 6 else None
                if b == 6: line(tr, tr.at(base + 7), shift(ANSWER, -12), lambda x, d: horns([x], d, 0.15), -0.2, 0.5)
        if kind == 'theme':
            trp(tr, t0, THEME, 0, 0.17)
            line(tr, t0, shift(THEME, -12), lambda x, d: bones([x], d, 0.12), -0.2, 0.45)
        if kind == 'theme2':
            trp(tr, t0, THEME, k, 0.18, harm=True)
            line(tr, t0, shift(THEME, k - 12), lambda x, d: horns([x], d, 0.12), -0.15, 0.5)
        if kind == 'stand':
            line(tr, t0, shift(STAND, k - 12), lambda x, d: horns([x, x - 12], d, 0.17), -0.1, 0.5)
            line(tr, t0, shift(STAND, k), lambda x, d: choir([x], d, 0.05, 0.15, 'a'), 0, 0.7)
            for b in range(8):
                r, q = P_STAND[b]; stabs(tr, base + b, r, q, k, 0.14 if k else 0.12)
            if s > 3: trp(tr, t0, STAND, 12, 0.13, 0.2)            # the second time, trumpets soaring an octave up
        if kind == 'cost':
            line(tr, tr.at(base + 2), shift(THEME[:9], 0), lambda x, d: trumpet(x, d * 0.95, 0.13), 0.25, 0.75)
        if kind == 'rally':
            for i, b in enumerate(range(8)):
                trp(tr, tr.at(base + b), CALL, chord(*P_CALL[b], 0, 4)[0] - M('G4') - (12 if b < 4 else 0), 0.16, (-0.3, 0.3)[i % 2])
            tr.add(riser(bl * 4, 0.12), tr.at(base + 4), 0, 1, 0.4)
        if kind == 'all':
            trp(tr, t0, THEME, 0, 0.19, harm=True)
            trp(tr, t0, THEME, 12, 0.1, 0.3)
            line(tr, t0, shift(THEME, -12), lambda x, d: horns([x, x - 12], d, 0.15), -0.15, 0.5)
    base = 64                                                  # THE CALL, hammered - 2 bars
    for b in range(2):
        r, q = P_CALL[b + 2]; root = chord(r, q, 0, 2)[0]
        drums(tr, base + b, 'roll' if b == 1 else 'battle', 1.1, root)
        strings(tr, base + b, r, q, 0, 0.08); brass_bed(tr, base + b, r, q, 0, 1.1, 1)
        stabs(tr, base + b, r, q, 0, 0.14, (0, 1.5, 3) if b == 0 else (0,))
    tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
    trp(tr, tr.at(base), CALL, -4, 0.19, harm=True)
    trp(tr, tr.at(base + 1), CALL, -5, 0.19, harm=True)
    tr.add(riser(bl * 2, 0.12), tr.at(base), 0, 1, 0.4)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'apophiss_battle.ogg'
    _guarded(render(seeded(83, compose), 2.6, 0.27), out, 6)
