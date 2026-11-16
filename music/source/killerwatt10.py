"""KILLERWATT - what's left after the fall. C minor, 164 BPM, 82 bars = 120 s loop.

Relentless from bar one, the storm already raging. Democratus's hook and climb are always there and always clear - but played
by the overwhelming forces (brass, choir, theremin), his violin doubling them inside the mass. Once a loop, four bars of the
violin alone with the hook's opening - cut off by thunder mid-phrase.

  0 THE STORM  the hook: theremin and horns, the violin under them, the triplet blast
  1 HIS THEME  the hook: choir, brass and violin, lightning on the accents
  2 THE CLIMB  the climb in brass and choir, the violin with it
  3 STRIKE     the hammer, strikes, waterphone shrieks, the theremin wailing his hook's head
  4 HIM        4 bars: the violin alone, the hook's opening - thunder cuts it off; the surge builds back
  5 HIS KEY    the hook in D minor - everything
  6 TEMPEST    the climb, a strike every bar
  7 ALL        the hook: theremin, horns, choir, violin; thunder every bar
  8 AGAIN      the hook once more, back in C minor, the hammer under it
  9 THE EYE    10 bars: the hammer, the violin's trill, a great strike, a roll - round again
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from killerwatt9 import (Track, riser, tom, crash, esnare, boom, render, _guarded, seeded, M, ther, ekick, sub808, choir, bones, horns,
                         violin, waterphone, shriek, TR, L, HOOK, CLIMB, SURGE, P_HOOK, P_CLIMB, triad, bass, ostinato,
                         spark, rain, thunder, strike, shift, line, drums, current, hammer)

BPM, BARS, KEY = 164, 82, -2


def storm(tr, s, base, nb, lvl=1.0):
    bl = tr.beat * 4
    tr.add(rain(bl * nb, 0.03 + 0.08 * lvl, s), tr.at(base), 0, 1, 0.4)
    for b in range(0, nb, 2 if lvl < 1 else 1):
        tr.add(thunder(0.25 + 0.3 * lvl, 5.0, 100 * s + b, crack=True), tr.at(base + b), (-0.4, 0.4)[b % 2], 1, 0.5)
    for b in range(nb): tr.add(spark(0.15, 31 * s + b), tr.at(base + b, 2), (-0.5, 0.5)[b % 2], 1, 0.35)


def hook_mass(tr, t0, notes, k, violin_amp=0.3, ther_up=True):
    """his theme, clear: the violin carries the line, horns an octave under, the choir with it, the theremin over"""
    violin(tr, t0, shift(notes, k), violin_amp, -0.15)
    line(tr, t0, shift(notes, k - 12), lambda x, d: horns([x, x - 12], d, 0.15), 0.15, 0.5)
    line(tr, t0, shift(notes, k), lambda x, d: choir([x], d, 0.06, 0.1, 'a'), 0.0, 0.7)
    if ther_up: ther(tr, t0, shift(notes, k + 12), 0.18, 0.3, 0.45, port=0.04, echo_=False)


def bed(tr, bar, r, k, style='blast', ham=False):
    bl = tr.beat * 4
    drums(tr, bar, style)
    bass(tr, bar, r, k, 1.2)
    ostinato(tr, bar, r, k, 0.09)
    current(tr, bar, r, k, 1.2)
    if ham: hammer(tr, bar, r, k)
    tr.add(crash(0.15), tr.at(bar), (-0.3, 0.3)[bar % 2], 1, 0.5)
    if bar % 2 == 0:
        c = triad(r, k, 3)
        tr.add(choir([c[0] + 12, c[1] + 12, c[2] + 12], bl * 2, 0.07, 0.3, 'a'), tr.at(bar), 0, 1, 0.7)
        tr.add(bones([c[0], c[2]], bl * 2 * 0.95, 0.09), tr.at(bar), -0.2, 1, 0.5)


def compose():
    tr = Track('killerwatt10', BPM, BARS)
    assert round(tr.seconds) == 120
    bl = tr.beat * 4
    plan = [('storm', P_HOOK, 0), ('theme', P_HOOK, 0), ('climb', P_CLIMB, 0), ('strike', P_HOOK, 0), ('him', P_HOOK, 0),
            ('key', P_HOOK, 2), ('tempest', P_CLIMB, 0), ('all', P_HOOK, 0), ('again', P_HOOK, 0)]
    for s, (kind, prog, kk) in enumerate(plan):
        k = KEY + kk; base = s * 8 + (4 if s > 4 else 0); t0 = tr.at(base)
        if kind != 'him':
            tr.add(crash(0.45, 3.0), t0, 0.3, 1, 0.55)
            storm(tr, s, base, 8, 1.0 if kind in ('tempest', 'all') else 0.8)
            for b in range(8):
                bed(tr, base + b, prog[b], k, 'charge' if kind == 'climb' else 'blast', ham=kind in ('strike', 'again'))
        if kind in ('storm', 'theme', 'key', 'all', 'again'):
            hook_mass(tr, t0, HOOK, k, 0.3, ther_up=kind != 'theme')
            if kind == 'storm': ther(tr, t0, shift(HOOK, k), 0.16, 0.35, 0.45, port=0.04, echo_=False)
        if kind in ('climb', 'tempest'):
            hook_mass(tr, t0, CLIMB, k, 0.28, ther_up=kind == 'tempest')
            if kind == 'tempest':
                for b in range(8): tr.add(strike(0.28, 500 + b), tr.at(base + b, 1.5), (-0.5, 0.5)[b % 2], 1, 0.4)
        if kind == 'theme':
            for b in (1, 3, 5, 7): tr.add(strike(0.3, 300 + b), tr.at(base + b, 3), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)
        if kind == 'strike':
            for i, b in enumerate((0, 2, 4, 6)):                       # the hook's head, wailed higher each time
                ther(tr, tr.at(base + b), shift(HOOK[:6], k + 12 + 2 * i), 0.24, (-0.2, 0.2)[i % 2], 0.5, port=0.05)
            for b in (1, 3, 5, 7):
                tr.add(strike(0.4, 400 + b), tr.at(base + b, 2.5), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)
                tr.add(shriek(bl * 1.2, 0.11, ('C6', 'G5', 'Bb5', 'G5')[b // 2], b), tr.at(base + b, 3), 0.5, 1, 0.5)
        if kind == 'him':                                              # four bars of him
            tr.add(rain(bl * 3.4, 0.05, 77), t0, 0, 1, 0.5)
            for b in range(3): tr.add(sub808(triad(prog[b], k)[0], bl * 0.98, 0.1), tr.at(base + b), 0, 1, 0.05)
            violin(tr, t0, shift(HOOK[:13], k) + [(M('A5') + k, 1.45)], 0.3, 0.0, drive=1.6, legato=1.0)   # the opening ... cut off
            cut = tr.at(base + 2, 2.5)
            tr.add(strike(0.75, 999), cut, 0, 1, 0.4)
            tr.add(crash(0.5, 3.0), cut, 0.3, 1, 0.55)
            for i in range(9): tr.add(tom(170 - 9 * i, 0.22, 8, 0.2), tr.at(base + 2, 2.5 + i * TR), -0.4 + 0.1 * i, 1, 0.25)
            storm(tr, s, base + 4, 8, 0.9)
            for b in range(4, 12): bed(tr, base + b, prog[b % 8], k, 'tribal' if b < 8 else 'blast')
            tr.add(crash(0.45, 3.0), tr.at(base + 8), 0.3, 1, 0.55)
            violin(tr, tr.at(base + 4), shift(SURGE, k), 0.29, -0.1, port=0.008, drive=3.8)
            tr.add(waterphone('C3', bl * 4, 0.24, seed=4), tr.at(base + 4), 0.4, 1, 0.55)
            tr.add(waterphone('G2', bl * 4, 0.24, seed=5), tr.at(base + 8), -0.4, 1, 0.55)
    base = 76; prog = ['D', 'Bb', 'A', 'D', 'Bb', 'A']   # THE EYE
    tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
    storm(tr, 9, base, 6, 1.0)
    tr.add(strike(0.6, 900), tr.at(base), 0, 1, 0.4)
    for b in range(6): bed(tr, base + b, prog[b], KEY, 'blast', ham=True)
    hook_mass(tr, tr.at(base), HOOK[:12], KEY, 0.3)
    violin(tr, tr.at(base + 2), shift(L('D6:t C#6:t D6:t ' * 8 + 'F6:t E6:t D6:t C#6:t Bb5:t A5:t D6:2 ' + 'A5:4 '), KEY), 0.28, -0.1, drive=4.2)
    for b in (4, 5):
        for i in range(12): tr.add(tom(170 - 5 * (i + 12 * (b - 4)), 0.22, 8, 0.2), tr.at(base + b, i * TR), -0.4 + 0.07 * i, 1, 0.25)
    tr.add(riser(bl * 3, 0.13), tr.at(base + 3), 0, 1, 0.4)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'killerwatt10.ogg'
    _guarded(render(seeded(71, compose), 2.6, 0.27), out, 6)
