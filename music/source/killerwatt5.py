"""KILLERWATT - take five: its own music, not Vexis's. No sequencer, no arpeggiator, no straight sixteenths.
A TRIPLET engine (everything swings in threes - a gallop that charges rather than runs), an electric string section
(violins in a spiccato ostinato under the lead violin), tribal toms, distorted power chords, the theremin and waterphone.

150 BPM, D minor, 75 bars = 120 s:
  0 WAR CRY    toms and the ostinato, power chords on the one
  1 THE HOOK   the violin's hook
  2 BOTH       the hook, the theremin a third above
  3 THE CLIMB  the B theme: climbing through F major and back - fighting for everyone
  4 THE DREAD  half time: the waterphone, the theremin alone, the toms like a heartbeat
  5 THE SURGE  ostinato and toms building, the violin climbing in triplets
  6 HIGHER     the hook a whole step up (E minor)
  7 THE CLIMB  B theme, up a step
  8 EVERYTHING the hook back home, everyone
  9 BRINK      3 bars of hits, roll and riser - round again
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track, riser, tom
from boss_music import crash
from sovereign_music import boom, suck, render, _guarded, seeded
from armada_music import M, stab, ther, ekick, esnare, mhat, sub808
from divine_music import choir, bones
from killerwatt_music import violin, waterphone, shriek, arc, chug

BPM, BARS = 150, 75
TR = 1 / 3

def L(s):
    """'D5:1 F5:t ...' with t = a triplet eighth"""
    out = []
    for tok in s.split():
        n, d = tok.split(':')
        d = {'t': TR, '2t': 2 * TR}.get(d, None) or float(d)
        out.append((None if n == 'r' else n, d))
    return out

def beats(x): return sum(d for _, d in x)

# THE HOOK (8 bars): a triplet-pickup charge into long notes - D, up to A, the sixth (Bb) pushing, falling, then the climb
HOOK = L('r:2t D5:t A5:2 G5:t F5:t E5:t  F5:1 D5:2t E5:t F5:1 G5:1  A5:2t Bb5:t A5:3  r:2t A5:t D6:2 C6:t Bb5:t A5:t  '
         'G5:1 F5:2t G5:t A5:1 E5:1  C#5:4  r:2t D5:t A5:2 Bb5:2t C6:t  D6:2 C6:t Bb5:t A5:t A5:1')
# THE CLIMB (8 bars): F major lifting, the line reaching higher each bar - not giving up
CLIMB = L('G5:2t A5:t Bb5:1 D6:2  C6:2t Bb5:t A5:1 G5:2  Bb5:2t C6:t D6:1 F6:2  E6:3 C#6:1  '
          'D6:2t E6:t F6:1 A6:2  G6:2t F6:t E6:1 D6:2  Bb5:2t C6:t D6:1 E6:2  C#6:4')
SURGE = L(' '.join(['D5:t F5:t A5:t'] * 4 + ['D5:t G5:t Bb5:t'] * 4 + ['F5:t A5:t C6:t'] * 4 + ['E5:t A5:t C#6:t'] * 4 +
                   ['A5:t D6:t F6:t'] * 4 + ['Bb5:t D6:t G6:t'] * 4 + ['C6:t F6:t A6:t'] * 4 + ['C#6:t E6:t A6:t'] * 2) + ' A6:2')
WAIL = L('A4:4 Bb4:4 A4:2 G4:2 F4:4 E4:4 F4:2 G4:2 A4:8')
for _x, _b in ((HOOK, 32), (CLIMB, 32), (SURGE, 32), (WAIL, 32)):
    assert abs(beats(_x) - _b) < 1e-6, (_b, beats(_x))

P_HOOK = ['D', 'D', 'Bb', 'A', 'D', 'G', 'Bb', 'A']
P_CLIMB = ['G', 'G', 'Bb', 'A', 'D', 'Bb', 'G', 'A']
MAJ = {'Bb', 'A'}


def triad(r, k, octv=2):
    b = M(r + str(octv)) + k
    return [b, b + (4 if r in MAJ else 3), b + 7]


def drums(tr, bar, style):
    t = tr.at(bar, 0); bt = tr.beat
    if style == 'charge':                                       # the triplet gallop
        for b in range(4):
            tr.add(ekick(0.6, 6, 140, 46), t + b * bt, 0, 1, 0.08)
            tr.add(ekick(0.35), t + (b + 2 * TR) * bt, 0, 1, 0.08)
            for i in range(3): tr.add(mhat(0.06 * (1.5 if i == 0 else 0.8), i == 2), t + (b + i * TR) * bt, 0.35, 1, 0.12)
        for b in (1, 3): tr.add(esnare(0.55, 170), t + b * bt, 0.05, 1, 0.35)
        for i, f in enumerate((120, 100, 80)): tr.add(tom(f, 0.18, 8, 0.25), t + (3 + i * TR) * bt, -0.3 + 0.3 * i, 1, 0.25)
    elif style == 'tribal':                                     # toms carrying it
        for b in range(4):
            tr.add(tom(70, 0.32, 6, 0.35), t + b * bt, -0.25, 1, 0.3)
            tr.add(tom(95, 0.2, 8, 0.25), t + (b + 2 * TR) * bt, 0.25, 1, 0.3)
        tr.add(ekick(0.6, 6), t, 0, 1, 0.1); tr.add(esnare(0.5, 170), t + 2 * bt, 0.05, 1, 0.45)
    elif style == 'heart':
        tr.add(boom(0.3, 75, 28, 1.4), t, 0, 1, 0.3); tr.add(boom(0.2, 75, 28, 1.0), t + 2 * TR * bt, 0, 1, 0.3)
        tr.add(esnare(0.45, 150), t + 2 * bt, 0.05, 1, 0.6)


def bass(tr, bar, r, k, amp=1.0):
    t = tr.at(bar, 0); bt = tr.beat; c = triad(r, k)
    for b in range(4):                                          # gallop: on, rest, on (in threes)
        tr.add(chug(c[0] + 12, bt * 0.28, 0.2 * amp), t + b * bt, -0.1, 1, 0.08)
        tr.add(chug(c[0] + 12, bt * 0.28, 0.14 * amp), t + (b + 2 * TR) * bt, -0.1, 1, 0.08)
    tr.add(sub808(c[0], tr.beat * 4 * 0.98, 0.22 * amp), t, 0, 1, 0.05)
    tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], bt * 0.9, 0.1 * amp, 4500, 500, 6.0), t, 0.2, 1, 0.3)  # power chord on the one


def ostinato(tr, bar, r, k, amp=0.12):
    """the electric string section: spiccato triplets on the chord's root and fifth"""
    c = triad(r, k, 4)
    pat = [(c[0], TR), (c[0], TR), (c[2], TR)] * 2 + [(c[0], TR), (c[1], TR), (c[2], TR), (c[0] + 12, TR), (c[2], TR), (c[1], TR)]
    violin(tr, tr.at(bar, 0), pat, amp, 0.4, 0.3, port=0.005, drive=2.0, legato=0.55)


def compose():
    tr = Track('killerwatt5', BPM, BARS)
    assert round(tr.seconds) == 120
    bl = tr.beat * 4
    plan = [('war', P_HOOK, 0), ('hook', P_HOOK, 0), ('both', P_HOOK, 0), ('climb', P_CLIMB, 0), ('dread', P_HOOK, 0),
            ('surge', P_HOOK, 0), ('hook', P_HOOK, 2), ('climb', P_CLIMB, 2), ('all', P_HOOK, 0)]
    for s, (kind, prog, k) in enumerate(plan):
        base = s * 8; t0 = tr.at(base, 0)
        tr.add(crash(0.45, 3.0), t0, 0.3, 1, 0.55)
        for b in range(8):
            bar = base + b; r = prog[b]
            drums(tr, bar, 'tribal' if kind in ('war', 'surge', 'dread') else 'charge')
            if kind == 'dread': drums(tr, bar, 'heart')
            if kind != 'war' or b >= 4:
                tr.add(ekick(0.3, 6), tr.at(bar, 2 * TR), 0, 1, 0.06); tr.add(ekick(0.3, 6), tr.at(bar, 2 + 2 * TR), 0, 1, 0.06)
            bass(tr, bar, r, k, 1.15 if kind == 'all' else 1.0)
            ostinato(tr, bar, r, k, 0.1 if kind in ('war', 'surge', 'dread') else 0.08)
            if (kind != 'war' or b >= 4) and b % 2 == 0:
                c = triad(r, k, 4)
                tr.add(choir(c, bl * 2, 0.08 if kind in ('climb', 'all') else 0.06, 0.3, 'a'), tr.at(bar), 0, 1, 0.7)
                tr.add(bones([c[0] - 12, c[2] - 12], bl * 2 * 0.95, 0.07), tr.at(bar), -0.2, 1, 0.5)
            if kind == 'all' or b % 2 == 0: tr.add(crash(0.18 if kind == 'all' else 0.13), tr.at(bar), (-0.3, 0.3)[b % 2], 1, 0.5)
        if kind == 'war':
            for b in (3, 7): tr.add(arc(0.2, 0.9, b), tr.at(base + b, 3), 0.5, 1, 0.4)
            ther(tr, tr.at(base + 4), L('D5:8 A5:8'), 0.18, -0.3, 0.5, port=0.25)
        if kind in ('hook', 'both', 'all'):
            violin(tr, t0, [(x if x is None else M(x) + k, d) for x, d in HOOK], 0.32, -0.1)
            if kind in ('both', 'all'):
                ther(tr, t0, [(x if x is None else M(x) + 3, d) for x, d in HOOK], 0.17, 0.3, 0.45, port=0.04, echo_=False)
            if kind in ('all', 'hook'):
                violin(tr, t0, [(x if x is None else M(x) + k - 12, d) for x, d in HOOK], 0.16, 0.25, drive=3.0)
            if kind == 'all':
                ther(tr, t0, [(x if x is None else M(x) + 12, d) for x, d in HOOK], 0.18, 0.3, 0.45, port=0.04, echo_=False)
        if kind == 'climb':
            violin(tr, t0, [(x if x is None else M(x) + k, d) for x, d in CLIMB], 0.32, -0.1)
            ther(tr, t0, [(x if x is None else M(x) + k - 12, d) for x, d in CLIMB], 0.12, 0.35, 0.5, port=0.05, echo_=False)
        if kind == 'dread':
            for b, f in ((0, 'D3'), (2, 'A2'), (4, 'Bb2'), (6, 'A2')):
                tr.add(waterphone(f, bl * 2.5, 0.26, seed=b), tr.at(base + b), (-0.5, 0.5)[b // 2 % 2], 1, 0.55)
            ther(tr, t0, WAIL, 0.27, 0.15, 0.5, port=0.12)
            tr.add(choir(['D3', 'A3', 'F4'], bl * 8, 0.07, 3.0, 'u'), t0, 0, 1, 0.8)
            tr.add(suck(bl, 0.22), tr.at(base + 7), 0.2, 1, 0.4)
        if kind == 'surge':
            violin(tr, t0, SURGE, 0.27, -0.1, port=0.008, drive=3.8)
            tr.add(shriek(bl * 1.5, 0.12, 'D6', 5), tr.at(base + 3, 2), 0.5, 1, 0.5)
    base = 72                                                   # BRINK
    for b in range(3):
        c = triad(('D', 'Bb', 'A')[b], 0)
        for x in (0, 2 * TR, 1, 1 + 2 * TR, 2, 2 + 2 * TR, 3, 3 + TR, 3 + 2 * TR):
            tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], tr.beat * 0.3, 0.13), tr.at(base + b, x), 0.2, 1, 0.3)
            tr.add(ekick(0.55), tr.at(base + b, x), 0, 1, 0.06)
        tr.add(sub808(c[0], bl * 0.98, 0.22), tr.at(base + b), 0, 1, 0.05)
    tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
    violin(tr, tr.at(base), L('D6:t C#6:t D6:t ' * 4 + 'F6:t E6:t D6:t C#6:t Bb5:t A5:t D6:4'), 0.28, -0.1, drive=4.2)
    for i in range(12): tr.add(tom(170 - 9 * i, 0.22, 8, 0.2), tr.at(base + 2, i * TR), -0.4 + 0.07 * i, 1, 0.25)
    tr.add(riser(bl * 2, 0.13), tr.at(base + 1), 0, 1, 0.4)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'killerwatt5.ogg'
    _guarded(render(seeded(53, compose), 2.4, 0.28), out, 6)
