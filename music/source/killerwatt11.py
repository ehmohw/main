"""KILLERWATT - killerwatt10 with electric guitars leading and the percussion pushed harder.

Rhythm guitars (double-tracked, hard left and right): palm-muted triplet gallop chugs, open power chords ringing on the one.
Lead guitar carries Democratus's hook and climb (the violin under it now). Drums: kicks on every triplet, snare on every
beat in the peaks, tom fills every other bar, china-like crashes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import killerwatt10 as K
from killerwatt10 import render, _guarded, seeded, M, TR, triad, shift, line, horns, choir, ther, violin, tom, esnare, crash
from armada_music import addc
from guitar import power, lead_line

NOTE = lambda m: ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B'][m % 12] + str(m // 12 - 1)
_bed = K.bed


def guitars(tr, bar, r, k):
    root = NOTE(triad(r, k, 2)[0] + 12)                            # E2-ish register
    t = tr.at(bar); bt = tr.beat
    for side, seed in ((-0.75, 0), (0.75, 50)):
        tr.add(power(root, bt * 0.95, False, 0.16, seed + bar), t, side, 1, 0.15)
        for b in range(4):
            for x in ((2 * TR,) if b == 0 else (0, 2 * TR)):
                tr.add(power(root, bt * 0.3, True, 0.15, seed + bar * 7 + b), t + (b + x) * bt, side, 1, 0.08)


def bed(tr, bar, r, k, style='blast', ham=False):
    _bed(tr, bar, r, k, style, ham)
    globals()['guitars'](tr, bar, r, k)
    t = tr.at(bar); bt = tr.beat
    if style == 'blast':
        for b in (0, 2): tr.add(esnare(0.5, 180), t + b * bt, -0.05, 1, 0.35)
    if bar % 2 == 1:
        for i in range(6): tr.add(tom(150 - 14 * i, 0.22, 8, 0.2), t + (2 + i * TR) * bt, -0.5 + 0.2 * i, 1, 0.25)
    tr.add(crash(0.12), t + 2 * bt, 0.45, 1, 0.45)


def lead(tr, t0, notes, vol=0.27, pan=0.1):
    s = lead_line(notes, tr.beat, vol)
    addc(tr, s, t0, pan, 1, 0.35)
    addc(tr, s * 0.25, t0 + tr.beat * 0.75, -pan, 1, 0.6)


def hook_mass(tr, t0, notes, k, violin_amp=0.3, ther_up=True):
    lead(tr, t0, shift(notes, k))
    violin(tr, t0, shift(notes, k), violin_amp * 0.5, -0.2)
    line(tr, t0, shift(notes, k - 12), lambda x, d: horns([x, x - 12], d, 0.12), 0.15, 0.5)
    line(tr, t0, shift(notes, k), lambda x, d: choir([x], d, 0.05, 0.1, 'a'), 0.0, 0.7)
    if ther_up: ther(tr, t0, shift(notes, k + 12), 0.15, 0.3, 0.45, port=0.04, echo_=False)


K.bed = bed
K.hook_mass = hook_mass

if __name__ == '__main__' and sys.argv[1:2] == ['v1']:
    out = sys.argv[1] if len(sys.argv) > 1 else 'killerwatt11.ogg'
    _guarded(render(seeded(71, K.compose), 2.4, 0.27), out, 6)


# ---- take 2: keep the guitars' intensity through the second minute, bring the waterphone forward
from killerwatt10 import HOOK, CLIMB, KEY, waterphone, shriek
_compose, _guitars = K.compose, guitars


def guitars(tr, bar, r, k):
    _guitars(tr, bar, r, k)
    if bar >= 36:                                                  # the second minute: a third guitar, tremolo-picked
        root = NOTE(triad(r, k, 2)[0] + 24)
        for i in range(12): tr.add(power(root, tr.beat * TR * 0.9, True, 0.1, 900 + bar * 12 + i), tr.at(bar, i * TR), 0.0, 1, 0.1)


def compose():
    tr = _compose()
    bl = tr.beat * 4
    for s, (notes, kk) in {5: (HOOK, 2), 6: (CLIMB, 0), 7: (HOOK, 0), 8: (HOOK, 0)}.items():   # harmony lead, a third up
        h = [(None if x is None else M(x) + KEY + kk + (4 if (M(x) % 12) in (5, 10, 0) else 3), d) for x, d in notes]
        lead(tr, tr.at(s * 8 + 4), h, 0.2, -0.35)
        lead(tr, tr.at(s * 8 + 4), shift(notes, KEY + kk), 0.12, 0.35)
    lead(tr, tr.at(36), shift(K.SURGE, KEY), 0.17, 0.2)
    for s in range(10):                                            # the waterphone, every section
        if s == 4: continue
        o = 4 if s > 4 else 0
        if s == 9:
            tr.add(shriek(bl * 1.4, 0.2, 'C6', 199), tr.at(78, 2.5), 0.6, 1, 0.5); continue
        for b, f in ((0, 'C3'), (4, 'G2')):
            tr.add(waterphone(f, bl * 3.5, 0.32, bend=1.8, seed=10 * s + b), tr.at(s * 8 + o + b), (-0.55, 0.55)[b // 4], 1, 0.5)
        for b in (3, 7):
            tr.add(shriek(bl * 1.4, 0.2, ('C6', 'G5', 'Eb6', 'Bb5')[(s + b) % 4], 100 + 10 * s + b), tr.at(s * 8 + o + b, 2.5), (0.6, -0.6)[b // 4], 1, 0.5)
    return tr


K.guitars_ = guitars
globals()['guitars'] = guitars

if __name__ == '__main__':
    _guarded(render(seeded(71, compose), 2.4, 0.27), sys.argv[2] if len(sys.argv) > 2 else 'killerwatt11b.ogg', 6)
