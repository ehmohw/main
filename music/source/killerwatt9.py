"""KILLERWATT - rework on Democratus's engine. C minor (a step below him), 156 BPM, 78 bars = 120 s loop.

Clearly his motifs: the triplet charge, the spiccato strings, the buzz-stabs on the pickups, THE HOOK and THE CLIMB - but
played by something bigger. The hook moves from violin to the theremin and brass; the choir and low brass under everything,
the double kick in the peaks. His electricity grows into a storm across the loop: sparks, rain, thunder, lightning on the beat.

  0 GATHERING  toms, strings, buzz-stabs, far thunder, the waterphone, the theremin rising
  1 HIS HOOK   the hook on the violin - but the choir and brass are under it now
  2 TAKEN      the hook on the theremin and horns, the violin an octave under; rain begins
  3 THE CLIMB  the climb in brass and choir, the double kick, thunder
  4 STRIKE     the hammer, lightning on the accents, waterphone shrieks, the theremin wailing
  5 THE SURGE  his surge figure on the violin, the storm thickening
  6 HIGHER     the hook a whole step up (D minor - his key), everything
  7 TEMPEST    the climb, thunder every bar, a strike every bar
  8 ALL        the hook in theremin, horns, choir and violin together
  9 THE EYE    6 bars: the hammer, a great strike, a roll - round again
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import killerwatt5 as K
from killerwatt5 import (Track, riser, tom, crash, boom, render, _guarded, seeded, M, stab, ther, ekick, esnare, mhat, sub808,
                         choir, bones, violin, waterphone, shriek, TR, L, HOOK, CLIMB, SURGE, WAIL, P_HOOK, P_CLIMB, triad,
                         bass, ostinato)
from divine_music import horns
from storm import spark, buzz, rain, thunder, strike

BPM, BARS = 156, 78
KEY = -2


def shift(notes, k): return [(x if x is None else M(x) + k, d) for x, d in notes]


def line(tr, t0, notes, fn, pan, wet):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(fn(x, d * tr.beat), t, pan, 1, wet)
        t += d * tr.beat


def drums(tr, bar, style):
    t = tr.at(bar); bt = tr.beat
    if style == 'blast':                                          # the triplet gallop, doubled: kicks on every triplet
        for i in range(12): tr.add(ekick(0.4 * (1.4 if i % 3 == 0 else 0.75), 10, 140, 44), t + i * TR * bt, 0, 1, 0.05)
        for b in (1, 3): tr.add(esnare(0.62, 170), t + b * bt, 0.05, 1, 0.38)
        for i in range(12): tr.add(mhat(0.05 * (1.5 if i % 3 == 0 else 0.8), i % 3 == 2), t + i * TR * bt, 0.35, 1, 0.12)
    else:
        K.drums(tr, bar, style)
    tr.add(boom(0.22, 66, 24, 1.3), t, 0, 1, 0.25)


def current(tr, bar, r, k, amp=1.0):
    """his buzz-stabs on the pickups"""
    c = triad(r, k, 4); f = 440 * 2 ** ((c[0] - 69) / 12)
    for x in (3 + TR, 3 + 2 * TR): tr.add(buzz(f, tr.beat * 0.25, 0.07 * amp), tr.at(bar, x), 0.45, 1, 0.2)
    tr.add(buzz(f * 2, tr.beat * 0.3, 0.06 * amp), tr.at(bar, 1 + 2 * TR), -0.45, 1, 0.2)


def hammer(tr, bar, r, k):
    c = triad(r, k)
    for x in (0, 2 * TR, 1 + TR, 2, 2 + 2 * TR, 3 + TR):
        tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], tr.beat * 0.35, 0.12), tr.at(bar, x), 0.2, 1, 0.3)
        tr.add(ekick(0.5), tr.at(bar, x), 0, 1, 0.06)


def weather(tr, s, base, nb, lvl):
    bl = tr.beat * 4
    if lvl >= 0.3: tr.add(rain(bl * nb, 0.03 + 0.09 * lvl, s), tr.at(base), 0, 1, 0.4)
    every = 4 if lvl < 0.5 else 2 if lvl < 0.85 else 1
    for b in range(0, nb, every):
        tr.add(thunder(0.22 + 0.35 * lvl, 5.0, 100 * s + b, crack=lvl >= 0.5), tr.at(base + b), (-0.4, 0.4)[b // every % 2], 1, 0.5)
    for b in range(nb): tr.add(spark(0.1 + 0.08 * lvl, 31 * s + b), tr.at(base + b, 2), (-0.5, 0.5)[b % 2], 1, 0.35)


def compose():
    tr = Track('killerwatt9', BPM, BARS)
    assert round(tr.seconds) == 120
    bl = tr.beat * 4
    plan = [('gather', P_HOOK, 0, 0.15), ('hook', P_HOOK, 0, 0.25), ('taken', P_HOOK, 0, 0.35), ('climb', P_CLIMB, 0, 0.5),
            ('strike', P_HOOK, 0, 0.6), ('surge', P_HOOK, 0, 0.7), ('hook2', P_HOOK, 2, 0.8), ('tempest', P_CLIMB, 0, 1.0),
            ('all', P_HOOK, 0, 1.0), ('eye', ['C', 'Ab', 'G', 'C', 'Ab', 'G'], 0, 0.9)]
    for s, (kind, prog, kk, lvl) in enumerate(plan):
        k = KEY + kk; base = s * 8; nb = len(prog) if kind != 'eye' else 6; t0 = tr.at(base)
        tr.add(crash(0.45, 3.0), t0, 0.3, 1, 0.55)
        weather(tr, s, base, nb, lvl)
        for b in range(nb):
            bar = base + b
            r = prog[b] if kind != 'eye' else ('D', 'Bb', 'A', 'D', 'Bb', 'A')[b]     # (eye: shifted to C by KEY)
            style = 'tribal' if kind in ('gather', 'surge') else 'blast' if kind in ('climb', 'tempest', 'all', 'strike', 'eye') else 'charge'
            drums(tr, bar, style)
            bass(tr, bar, r, k, 1.2)
            ostinato(tr, bar, r, k, 0.09)
            current(tr, bar, r, k, 1.2 if lvl > 0.6 else 1.0)
            if kind in ('strike', 'eye'): hammer(tr, bar, r, k)
            if kind != 'gather' and b % 2 == 0:
                c = triad(r, k, 3)
                tr.add(choir([c[0] + 12, c[1] + 12, c[2] + 12], bl * 2, 0.08, 0.3, 'a'), tr.at(bar), 0, 1, 0.7)
                tr.add(bones([c[0], c[2]], bl * 2 * 0.95, 0.09), tr.at(bar), -0.2, 1, 0.5)
            if lvl >= 0.6 or b % 2 == 0: tr.add(crash(0.15), tr.at(bar), (-0.3, 0.3)[b % 2], 1, 0.5)
        if kind == 'gather':
            tr.add(waterphone(M('C3'), bl * 4, 0.22, seed=1) if False else waterphone('C3', bl * 4, 0.22, seed=1), t0, 0.4, 1, 0.6)
            ther(tr, tr.at(base + 2), shift(L('A4:8 D5:8 C#5:8'), KEY), 0.22, -0.3, 0.5, port=0.3)
        if kind in ('hook', 'hook2'):
            violin(tr, t0, shift(HOOK, k), 0.32, -0.1)
            violin(tr, t0, shift(HOOK, k - 12), 0.16, 0.25, drive=3.0)
            if kind == 'hook2':
                line(tr, t0, shift(HOOK, k - 12), lambda x, d: horns([x, x - 12], d, 0.15), 0.15, 0.5)
                ther(tr, t0, shift(HOOK, k + 12), 0.2, 0.3, 0.45, port=0.04)
        if kind == 'taken':
            ther(tr, t0, shift(HOOK, k), 0.28, 0.15, 0.45, port=0.04)
            line(tr, t0, shift(HOOK, k - 12), lambda x, d: horns([x, x - 12], d, 0.16), -0.15, 0.5)
            violin(tr, t0, shift(HOOK, k - 12), 0.18, -0.3, drive=3.0)
        if kind in ('climb', 'tempest'):
            line(tr, t0, shift(CLIMB, k - 12), lambda x, d: horns([x, x - 12], d, 0.17), 0.1, 0.5)
            line(tr, t0, shift(CLIMB, k), lambda x, d: choir([x], d, 0.07, 0.12, 'a'), -0.1, 0.7)
            violin(tr, t0, shift(CLIMB, k), 0.26, -0.25)
            if kind == 'tempest':
                ther(tr, t0, shift(CLIMB, k + 12), 0.2, 0.3, 0.45, port=0.04)
                for b in range(8): tr.add(strike(0.28, 500 + b), tr.at(base + b, 1.5), (-0.5, 0.5)[b % 2], 1, 0.4)
        if kind == 'strike':
            ther(tr, t0, shift(WAIL, KEY + 12), 0.25, 0.15, 0.5, port=0.1)
            for b in (1, 3, 5, 7):
                tr.add(strike(0.4, 400 + b), tr.at(base + b, 2.5), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)
                tr.add(shriek(bl * 1.2, 0.12, ('C6', 'G5', 'Bb5', 'G5')[b // 2], b), tr.at(base + b, 3), 0.5, 1, 0.5)
        if kind == 'surge':
            violin(tr, t0, shift(SURGE, KEY), 0.28, -0.1, port=0.008, drive=3.8)
            for b, f in ((0, 'C3'), (4, 'G2')): tr.add(waterphone(f, bl * 4, 0.2, seed=b), tr.at(base + b), 0.4, 1, 0.55)
        if kind == 'all':
            ther(tr, t0, shift(HOOK, k + 12), 0.22, 0.3, 0.45, port=0.04)
            line(tr, t0, shift(HOOK, k - 12), lambda x, d: horns([x, x - 12], d, 0.17), 0.1, 0.5)
            line(tr, t0, shift(HOOK, k), lambda x, d: choir([x], d, 0.07, 0.1, 'a'), -0.1, 0.7)
            violin(tr, t0, shift(HOOK, k), 0.3, -0.25)
        if kind == 'eye':
            tr.add(strike(0.6, 900), t0, 0, 1, 0.4)
            violin(tr, t0, shift(L('D6:t C#6:t D6:t ' * 4 + 'F6:t E6:t D6:t C#6:t Bb5:t A5:t D6:4 ' + 'D6:t C#6:t D6:t ' * 4 + 'A5:4 ' * 2), KEY), 0.28, -0.1, drive=4.2)
            for b in (4, 5):
                for i in range(12): tr.add(tom(170 - 5 * (i + 12 * (b - 4)), 0.22, 8, 0.2), tr.at(base + b, i * TR), -0.4 + 0.07 * i, 1, 0.25)
            tr.add(riser(bl * 3, 0.13), tr.at(base + 3), 0, 1, 0.4)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'killerwatt9.ogg'
    _guarded(render(seeded(67, compose), 2.6, 0.27), out, 6)
