"""KILLERWATT - the full battle theme. C minor, 164 BPM, 123 bars = 180 s loop.

Everything from the approved theme, in order (the storm, his theme, the climb, the strike, the violin cut off by thunder
and the full surge, his key, the tempest, all of it, again, the eye), rebuilt cleanly on the same instruments. The hook's
harmony is fixed as in Democratus's theme (here darker: D minor over an A bass where the old A major chord rubbed against
the melody), the theremin's climbing wail and the harmony guitars are now diatonic. New:

  THE RIFF      KillerWatt's own guitar riff, the loop's opening, and a chant of the hook's first notes over it
  BREAKDOWN     half time: crushing syncopated chugs, the theremin calling and the waterphone answering, then a build
  SOLO          a lead guitar solo over the blast beat
  TWIN          a melody of his own, two lead guitars in harmony
  THE RIFF      once more, hammered, before the eye

Material is written in D minor (Democratus's key) and played a whole step down (KEY = -2), as before.

  0 RIFF 8 | 1 STORM 8 | 2 THEME 8 | 3 CLIMB 8 | 4 STRIKE 8 | 5 HIM 12 | 6 HIS KEY 8 | 7 TEMPEST 8 | 8 BREAKDOWN 12 |
  9 SOLO 8 | 10 TWIN 8 | 11 ALL 8 | 12 AGAIN 8 | 13 RIFF 4 | 14 THE EYE 7
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track, riser, tom
from boss_music import crash
from sovereign_music import boom, seeded
from armada_music import stab, ther, ekick, esnare, mhat, sub808, addc
from divine_music import choir, bones, horns
from killerwatt_music import violin, waterphone, shriek, chug
from storm import spark, buzz, rain, thunder, strike
from guitar import power, lead_line
from full_common import (TR, L, bars, shift, head, tones, bass_note, harmonize, check, line, save, section_levels, midi, nm)
from democratus_full import HOOK, CLIMB, SURGE

BPM, KEY = 164, -2
DMIN = {2, 4, 5, 7, 9, 10, 0}

P_HOOK = ['Dm', 'Dm', 'Bb', 'Dm/A', 'Dm', 'C#o7', 'Bb', 'Dm/A']
P_CLIMB = ['Gm', 'Gm', 'Bb', 'A', 'Dm', 'Bb', 'Gm', 'A']
P_SURGE = ['Dm', 'Gm', 'F', 'A', 'Dm', 'Gm', 'F', 'A']
P_BREAK = ['Dm', 'Dm', 'Bb', 'Bb', 'Gm', 'Gm', 'A', 'A', 'A', 'A', 'A', 'A']
P_SOLO = ['Dm', 'Dm', 'Bb', 'Bb', 'Gm', 'Gm', 'A', 'A']
P_TWIN = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'Gm', 'A']
P_EYE = ['Dm', 'Dm', 'Bb', 'A', 'Dm', 'Bb', 'A']

# THE RIFF: (note, triplet slots, open?) - twelve slots a bar; muted chugs on D, open power chords moving above it
_m = lambda n: (n, 1, False)
RIFF_A = [_m('D3')] * 3 + [('F3', 2, True), _m('D3')] + [_m('D3')] * 3 + [('A3', 2, True), ('G3', 1, True)]
RIFF_B = [_m('D3')] * 3 + [('F3', 2, True), _m('D3')] + [_m('D3')] * 3 + [('Bb3', 2, True), ('A3', 1, True)]
RIFF_D = [_m('D3')] * 3 + [('F3', 2, True), _m('D3'), ('Bb3', 3, True), ('A3', 3, True)]
RIFF = [RIFF_A, RIFF_B, RIFF_A, RIFF_D]
for _b in RIFF: assert sum(s for _, s, _ in _b) == 12
CHANT = bars(L('D5:4 A5:4 G5:2 F5:2 D5:4'), 4)

# THE SOLO
SOLO = bars(L('A4:t D5:t F5:t A5:t D6:t F6:t A6:2  G6:t F6:t E6:t F6:t E6:t D6:t E6:t D6:t C6:t D6:t C6:t A5:t  '
              'Bb5:t D6:t F6:t Bb6:2 A6:t G6:t F6:t  D6:t F6:t D6:t Bb5:t D6:t Bb5:t F5:t Bb5:t F5:t D5:1  '
              'G5:t Bb5:t D6:t G6:2 F6:t E6:t D6:t  Bb6:1 A6:t G6:t F6:t G6:2  '
              'E6:t C#6:t A5:t E6:t C#6:t A5:t F6:t E6:t C#6:t E6:t F6:t G6:t  A6:4'), 8)
# THE TWIN: his own melody, two guitars a third apart
TWIN = bars(L('D5:2t E5:t F5:1 A5:2  Bb5:2t A5:t F5:1 D5:2  C5:2t D5:t F5:1 A5:2  G5:2t F5:t E5:1 C5:2  '
              'D5:2t E5:t F5:1 A5:1 D6:1  C6:2t Bb5:t A5:1 F5:1 D5:1  Bb5:2t A5:t G5:1 D6:2  C#6:3 E6:1'), 8)
def twin_harmony():
    """the second guitar a third under the first - except under the high D at the end of bar 5, where a third below (Bb)
    would rub against the chord's A: it holds A instead"""
    h = harmonize(TWIN, -2, P_TWIN, DMIN)
    t = 0.0
    for i, (x, d) in enumerate(h):
        if abs(t - 19) < 1e-6: h[i] = (midi('A5'), d)
        t += d
    return h


CALL1 = bars(L('D6:3 F6:1 E6:2 D6:2'), 2)
CALL2 = bars(L('G5:3 Bb5:1 A5:2 G5:2'), 2)
TRILL = L('D6:t C#6:t D6:t ' * 8 + 'F6:t E6:t D6:t C#6:t Bb5:t A5:t D6:2 A5:4')


def review():
    check('hook', HOOK, P_HOOK)
    for nm_, notes, prog in (('hook', HOOK, P_HOOK), ('climb', CLIMB, P_CLIMB)):
        check(nm_ + ' +3rd', harmonize(notes, 2, prog, DMIN), prog)
    check('solo', SOLO, P_SOLO); check('twin', TWIN, P_TWIN); check('twin -3rd', twin_harmony(), P_TWIN)
    check('chant', CHANT, ['Dm'] * 4)
    for i, st in enumerate((0, 2, 4, 7)):
        check(f'wail {i}', harmonize(head(HOOK, 4), st, ['Dm'], DMIN), [('Dm', 'Bb', 'Dm', 'Bb')[i]])


# ------------------------------------------------------------------ the band, as approved
def drums(tr, bar, style):
    t = tr.at(bar); bt = tr.beat
    if style == 'blast':                                          # kicks on every triplet, snare on every beat
        for i in range(12): tr.add(ekick(0.4 * (1.4 if i % 3 == 0 else 0.75), 10, 140, 44), t + i * TR * bt, 0, 1, 0.05)
        for b in (1, 3): tr.add(esnare(0.62, 170), t + b * bt, 0.05, 1, 0.38)
        for b in (0, 2): tr.add(esnare(0.5, 180), t + b * bt, -0.05, 1, 0.35)
        for i in range(12): tr.add(mhat(0.05 * (1.5 if i % 3 == 0 else 0.8), i % 3 == 2), t + i * TR * bt, 0.35, 1, 0.12)
    elif style == 'charge':
        for b in range(4):
            tr.add(ekick(0.6, 6, 140, 46), t + b * bt, 0, 1, 0.08)
            tr.add(ekick(0.35), t + (b + 2 * TR) * bt, 0, 1, 0.08)
            for i in range(3): tr.add(mhat(0.06 * (1.5 if i == 0 else 0.8), i == 2), t + (b + i * TR) * bt, 0.35, 1, 0.12)
        for b in (1, 3): tr.add(esnare(0.55, 170), t + b * bt, 0.05, 1, 0.35)
        for i, f in enumerate((120, 100, 80)): tr.add(tom(f, 0.18, 8, 0.25), t + (3 + i * TR) * bt, -0.3 + 0.3 * i, 1, 0.25)
    elif style == 'tribal':
        for b in range(4):
            tr.add(tom(70, 0.32, 6, 0.35), t + b * bt, -0.25, 1, 0.3)
            tr.add(tom(95, 0.2, 8, 0.25), t + (b + 2 * TR) * bt, 0.25, 1, 0.3)
        tr.add(ekick(0.6, 6), t, 0, 1, 0.1); tr.add(esnare(0.5, 170), t + 2 * bt, 0.05, 1, 0.45)
    elif style == 'half':                                         # the breakdown: one huge snare, kicks on the chugs
        for x in (0, 5, 6, 10): tr.add(ekick(0.7 if x == 0 else 0.5, 6, 130, 42), t + x * TR * bt, 0, 1, 0.08)
        tr.add(esnare(0.75, 140), t + 2 * bt, 0.05, 1, 0.6)
        tr.add(boom(0.3, 60, 24, 1.8), t, 0, 1, 0.3)
        for b in range(4): tr.add(mhat(0.07, True), t + b * bt, 0.4, 1, 0.2)
    tr.add(boom(0.22, 66, 24, 1.3), t, 0, 1, 0.25)
    if style in ('blast', 'charge', 'tribal') and bar % 2 == 1:
        for i in range(6): tr.add(tom(150 - 14 * i, 0.22, 8, 0.2), t + (2 + i * TR) * bt, -0.5 + 0.2 * i, 1, 0.25)
    tr.add(crash(0.12), t + 2 * bt, 0.45, 1, 0.45)


def bass(tr, bar, ch, k, amp=1.2):
    t = tr.at(bar); bt = tr.beat; b = bass_note(ch, 2, k); c = tones(ch, 2, k)
    for i in range(4):
        tr.add(chug(b + 12, bt * 0.28, 0.2 * amp), t + i * bt, -0.1, 1, 0.08)
        tr.add(chug(b + 12, bt * 0.28, 0.14 * amp), t + (i + 2 * TR) * bt, -0.1, 1, 0.08)
    tr.add(sub808(b, bt * 4 * 0.98, 0.22 * amp), t, 0, 1, 0.05)
    tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], bt * 0.9, 0.1 * amp, 4500, 500, 6.0), t, 0.2, 1, 0.3)


def ostinato(tr, bar, ch, k, amp=0.09):
    c = tones(ch, 4, k)
    pat = [(c[0], TR), (c[0], TR), (c[2], TR)] * 2 + [(c[0], TR), (c[1], TR), (c[2], TR), (c[0] + 12, TR), (c[2], TR), (c[1], TR)]
    violin(tr, tr.at(bar), pat, amp, 0.4, 0.3, port=0.005, drive=2.0, legato=0.55)


def current(tr, bar, ch, k, amp=1.2):
    f = 440 * 2 ** ((tones(ch, 4, k)[0] - 69) / 12)
    for x in (3 + TR, 3 + 2 * TR): tr.add(buzz(f, tr.beat * 0.25, 0.07 * amp), tr.at(bar, x), 0.45, 1, 0.2)
    tr.add(buzz(f * 2, tr.beat * 0.3, 0.06 * amp), tr.at(bar, 1 + 2 * TR), -0.45, 1, 0.2)


def hammer(tr, bar, ch, k):
    c = tones(ch, 2, k)
    for x in (0, 2 * TR, 1 + TR, 2, 2 + 2 * TR, 3 + TR):
        tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], tr.beat * 0.35, 0.12), tr.at(bar, x), 0.2, 1, 0.3)
        tr.add(ekick(0.5), tr.at(bar, x), 0, 1, 0.06)


def guitars(tr, bar, ch, k, trem=False):
    """two rhythm guitars hard left and right: a power chord on the one, palm-muted chugs on the gallop"""
    root = bass_note(ch, 3, k); t = tr.at(bar); bt = tr.beat
    for side, seed in ((-0.75, 0), (0.75, 50)):
        tr.add(power(root, bt * 0.95, False, 0.16, seed + bar), t, side, 1, 0.15)
        for b in range(4):
            for x in ((2 * TR,) if b == 0 else (0, 2 * TR)):
                tr.add(power(root, bt * 0.3, True, 0.15, seed + bar * 7 + b), t + (b + x) * bt, side, 1, 0.08)
    if trem:
        for i in range(12): tr.add(power(root + 12, bt * TR * 0.9, True, 0.1, 900 + bar * 12 + i), tr.at(bar, i * TR), 0.0, 1, 0.1)


def pads(tr, bar, ch, k, amp=0.07):
    c = tones(ch, 3, k); bl = tr.beat * 4
    tr.add(choir([x + 12 for x in c], bl * 2, amp, 0.3, 'a'), tr.at(bar), 0, 1, 0.7)
    tr.add(bones([bass_note(ch, 3, k), c[2]], bl * 2 * 0.95, 0.09), tr.at(bar), -0.2, 1, 0.5)


def bed(tr, bar, ch, k, style='blast', ham=False, trem=False, ost=0.09):
    drums(tr, bar, style); bass(tr, bar, ch, k); current(tr, bar, ch, k)
    if ost: ostinato(tr, bar, ch, k, ost)
    if ham: hammer(tr, bar, ch, k)
    guitars(tr, bar, ch, k, trem)
    tr.add(crash(0.15), tr.at(bar), (-0.3, 0.3)[bar % 2], 1, 0.5)
    if bar % 2 == 0: pads(tr, bar, ch, k)


def storm(tr, s, base, nb, lvl=0.8):
    bl = tr.beat * 4
    tr.add(rain(bl * nb, 0.03 + 0.08 * lvl, s), tr.at(base), 0, 1, 0.4)
    for b in range(0, nb, 2 if lvl < 1 else 1):
        tr.add(thunder(0.25 + 0.3 * lvl, 5.0, 100 * s + b, crack=True), tr.at(base + b), (-0.4, 0.4)[b % 2], 1, 0.5)
    for b in range(nb): tr.add(spark(0.15, 31 * s + b), tr.at(base + b, 2), (-0.5, 0.5)[b % 2], 1, 0.35)


def lead(tr, t0, notes, vol=0.27, pan=0.1):
    s = lead_line(notes, tr.beat, vol)
    addc(tr, s, t0, pan, 1, 0.35)
    addc(tr, s * 0.25, t0 + tr.beat * 0.75, -pan, 1, 0.6)


def hook_mass(tr, t0, notes, k, ther_up=True):
    """his theme, clear: lead guitar, the violin inside it, horns an octave under, the choir, the theremin over"""
    lead(tr, t0, shift(notes, k))
    violin(tr, t0, shift(notes, k), 0.15, -0.2)
    line(tr, t0, shift(notes, k - 12), lambda x, d: horns([x, x - 12], d, 0.12), 0.15, 0.5)
    line(tr, t0, shift(notes, k), lambda x, d: choir([x], d, 0.05, 0.1, 'a'), 0.0, 0.7)
    if ther_up: ther(tr, t0, shift(notes, k + 12), 0.15, 0.3, 0.45, port=0.04, echo_=False)


def harmony_leads(tr, t0, notes, prog, k):
    lead(tr, t0, harmonize(notes, 2, prog, DMIN, k), 0.2, -0.35)
    lead(tr, t0, shift(notes, k), 0.12, 0.35)


def water(tr, s, base, k):
    bl = tr.beat * 4
    for b, f in ((0, 'D3'), (4, 'A2')):
        tr.add(waterphone(midi(f) + k, bl * 3.5, 0.32, bend=1.8, seed=10 * s + b), tr.at(base + b), (-0.55, 0.55)[b // 4], 1, 0.5)
    for b in (3, 7):
        tr.add(shriek(bl * 1.4, 0.2, ('C6', 'G5', 'Eb6', 'Bb5')[(s + b) % 4], 100 + 10 * s + b), tr.at(base + b, 2.5), (0.6, -0.6)[b // 4], 1, 0.5)


# ------------------------------------------------------------------ the sections
def riff_section(tr, s, base, nb=8, hammered=False):
    """KillerWatt's riff on the guitars, everything else locked to it"""
    bt = tr.beat; bl = bt * 4; k = KEY
    storm(tr, s, base, nb, 0.9 if hammered else 0.7)
    for b in range(nb):
        bar = base + b; t = tr.at(bar); slot = 0
        drums(tr, bar, 'blast'); current(tr, bar, 'Dm', k)
        tr.add(sub808(midi('D2') + k, bl * 0.98, 0.24), t, 0, 1, 0.05)
        tr.add(crash(0.15), t, (-0.3, 0.3)[b % 2], 1, 0.5)
        for n, sl, op in RIFF[b % 4]:
            x = midi(n) + k; when = t + slot * TR * bt
            for side, seed in ((-0.75, 0), (0.75, 50)):
                tr.add(power(x, sl * TR * bt * (0.95 if op else 0.3), not op, 0.17 if op else 0.15, seed + bar * 13 + slot), when, side, 1, 0.1)
            tr.add(chug(x - 12, sl * TR * bt * 0.8, 0.22), when, -0.1, 1, 0.08)
            if op: tr.add(ekick(0.45), when, 0, 1, 0.06)
            slot += sl
        if hammered or b >= 4:
            if b % 2 == 0: pads(tr, bar, 'Dm', k, 0.06)
            if hammered: hammer(tr, bar, 'Dm', k)
    if not hammered:
        line(tr, tr.at(base + 4), shift(CHANT, k - 12), lambda x, d: horns([x, x - 12], d, 0.16), 0.15, 0.5)
        ther(tr, tr.at(base + 4), shift(CHANT, k), 0.2, -0.25, 0.5, port=0.15)
        water(tr, s, base, k)
    else:
        lead(tr, tr.at(base), shift(head(HOOK, 8), k), 0.25, 0.1)
        ther(tr, tr.at(base), shift(head(HOOK, 8), k + 12), 0.15, 0.3, 0.45, port=0.04, echo_=False)


def hook_section(tr, s, base, kind, kk=0):
    k = KEY + kk; t0 = tr.at(base)
    storm(tr, s, base, 8, 1.0 if kind == 'all' else 0.8)
    for b in range(8): bed(tr, base + b, P_HOOK[b], k, 'blast', ham=kind in ('strike', 'again'), trem=s >= 6)
    water(tr, s, base, k)
    if kind != 'strike':
        hook_mass(tr, t0, HOOK, k, ther_up=kind != 'theme')
        if kind == 'storm': ther(tr, t0, shift(HOOK, k), 0.16, 0.35, 0.45, port=0.04, echo_=False)
        if kind in ('key', 'all', 'again'): harmony_leads(tr, t0, HOOK, P_HOOK, k)
    if kind == 'theme':
        for b in (1, 3, 5, 7): tr.add(strike(0.3, 300 + b), tr.at(base + b, 3), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)
    if kind == 'strike':                                            # the hook's head, wailed a step higher each time
        for i, (b, st) in enumerate(zip((0, 2, 4, 6), (0, 2, 4, 7))):
            ther(tr, tr.at(base + b), harmonize(head(HOOK, 4), st, ['Dm'], DMIN, k + 12), 0.24, (-0.2, 0.2)[i % 2], 0.5, port=0.05)
        for b in (1, 3, 5, 7): tr.add(strike(0.4, 400 + b), tr.at(base + b, 2.5), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)


def climb_section(tr, s, base, kind):
    k = KEY; t0 = tr.at(base)
    storm(tr, s, base, 8, 1.0 if kind == 'tempest' else 0.8)
    for b in range(8): bed(tr, base + b, P_CLIMB[b], k, 'charge' if kind == 'climb' else 'blast', trem=s >= 6)
    water(tr, s, base, k)
    hook_mass(tr, t0, CLIMB, k, ther_up=kind == 'tempest')
    if kind == 'tempest':
        for b in range(8): tr.add(strike(0.28, 500 + b), tr.at(base + b, 1.5), (-0.5, 0.5)[b % 2], 1, 0.4)
        harmony_leads(tr, t0, CLIMB, P_CLIMB, k)


def him(tr, s, base):
    """four bars of him - the violin alone with the hook's opening, cut off by thunder - then the whole surge"""
    bl = tr.beat * 4; k = KEY; t0 = tr.at(base)
    tr.add(rain(bl * 3.4, 0.05, 77), t0, 0, 1, 0.5)
    for b in range(3): tr.add(sub808(bass_note(P_HOOK[b], 2, k), bl * 0.98, 0.1), tr.at(base + b), 0, 1, 0.05)
    violin(tr, t0, shift(HOOK[:13], k) + [(midi('A5') + k, 1.45)], 0.3, 0.0, drive=1.6, legato=1.0)
    cut = tr.at(base + 2, 2.5)
    tr.add(strike(0.75, 999), cut, 0, 1, 0.4); tr.add(crash(0.5, 3.0), cut, 0.3, 1, 0.55)
    for i in range(9): tr.add(tom(170 - 9 * i, 0.22, 8, 0.2), tr.at(base + 2, 2.5 + i * TR), -0.4 + 0.1 * i, 1, 0.25)
    storm(tr, s, base + 4, 8, 0.9)
    for b in range(8): bed(tr, base + 4 + b, P_SURGE[b], k, 'tribal' if b < 4 else 'blast', trem=True)
    tr.add(crash(0.45, 3.0), tr.at(base + 8), 0.3, 1, 0.55)
    violin(tr, tr.at(base + 4), shift(SURGE, k), 0.29, -0.1, port=0.008, drive=3.8)
    lead(tr, tr.at(base + 4), shift(SURGE, k), 0.17, 0.2)
    tr.add(waterphone(midi('D3') + k, bl * 4, 0.24, seed=4), tr.at(base + 4), 0.4, 1, 0.55)
    tr.add(waterphone(midi('A2') + k, bl * 4, 0.24, seed=5), tr.at(base + 8), -0.4, 1, 0.55)


def breakdown(tr, s, base):
    """half time: the chugs syncopated in threes, the theremin calling, the waterphone answering; then four bars of build"""
    bt = tr.beat; bl = bt * 4; k = KEY
    tr.add(rain(bl * 12, 0.08, s), tr.at(base), 0, 1, 0.4)
    for b, ch in enumerate(P_BREAK):
        bar = base + b; t = tr.at(bar); root = bass_note(ch, 3, k); c = tones(ch, 3, k)
        if b < 8:
            drums(tr, bar, 'half')
            for x in (0, 5, 6, 10):                                      # the crushing chug pattern
                for side, seed in ((-0.75, 0), (0.75, 50)):
                    tr.add(power(root, bt * (1.2 if x == 0 else 0.3), x != 0, 0.18, seed + bar * 11 + x), t + x * TR * bt, side, 1, 0.1)
                tr.add(chug(root - 12, bt * 0.5, 0.24), t + x * TR * bt, -0.1, 1, 0.08)
            tr.add(sub808(root - 12, bl * 0.98, 0.26), t, 0, 1, 0.05)
            tr.add(bones([root - 12, root], bl * 0.9, 0.12), t, -0.2, 1, 0.5)
            if b % 2 == 0:
                tr.add(choir([x + 12 for x in c], bl * 2, 0.08, 0.6, 'u'), t, 0, 1, 0.75)
                tr.add(thunder(0.55, 5.0, 700 + b, crack=True), t, (-0.4, 0.4)[b // 2 % 2], 1, 0.5)
            current(tr, bar, ch, k, 1.0)
        else:                                                            # the build: the gallop comes back and speeds up
            i = b - 8
            drums(tr, bar, 'charge' if i < 2 else 'blast'); bass(tr, bar, ch, k)
            guitars(tr, bar, ch, k, trem=i >= 1)
            for j in range(12 if i < 3 else 24):
                tr.add(esnare(0.05 + 0.03 * i + 0.002 * j, 190), t + j * (TR if i < 3 else TR / 2) * bt, 0.05, 1, 0.3)
            current(tr, bar, ch, k)
    for b, notes in ((0, CALL1), (4, CALL2)):
        ther(tr, tr.at(base + b), shift(notes, k), 0.27, -0.2, 0.55, port=0.1)
    for b, f, sf in ((2, 'Bb2', 'D6'), (6, 'A2', 'E6')):
        tr.add(waterphone(midi(f) + k, bl * 2.5, 0.34, bend=2.2, seed=40 + b), tr.at(base + b), 0.45, 1, 0.55)
        tr.add(shriek(bl * 1.5, 0.22, nm(midi(sf) + k), 140 + b), tr.at(base + b + 1), 0.55, 1, 0.5)
    lead(tr, tr.at(base + 8), shift(L('A4:4 C#5:4 E5:4 A5:4'), k), 0.24, 0.1)
    tr.add(choir([x + 12 for x in tones('A', 3, k)], bl * 4, 0.08, 2.0, 'a'), tr.at(base + 8), 0, 1, 0.7)
    tr.add(riser(bl * 4, 0.13), tr.at(base + 8), 0, 1, 0.4)
    for i in range(12): tr.add(tom(170 - 6 * i, 0.22, 8, 0.2), tr.at(base + 11, i * TR), -0.4 + 0.07 * i, 1, 0.25)


def solo(tr, s, base):
    k = KEY; t0 = tr.at(base)
    tr.add(crash(0.45, 3.0), t0, 0.3, 1, 0.55)
    storm(tr, s, base, 8, 0.8)
    for b in range(8): bed(tr, base + b, P_SOLO[b], k, 'blast', trem=True, ost=0.06)
    lead(tr, t0, shift(SOLO, k), 0.34, 0.15)
    lead(tr, tr.at(base + 7), shift(L('E6:4'), k), 0.2, -0.35)        # a second guitar joins on the last scream


def twin(tr, s, base):
    k = KEY; t0 = tr.at(base)
    storm(tr, s, base, 8, 0.8)
    for b in range(8): bed(tr, base + b, P_TWIN[b], k, 'charge', trem=True)
    lead(tr, t0, shift(TWIN, k), 0.25, 0.35)
    lead(tr, t0, shift(twin_harmony(), k), 0.22, -0.35)
    line(tr, t0, shift(TWIN, k - 12), lambda x, d: horns([x], d, 0.1), 0.0, 0.5)
    water(tr, s, base, k)


def eye(tr, s, base):
    bl = tr.beat * 4; k = KEY
    tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
    storm(tr, s, base, 7, 1.0)
    tr.add(strike(0.6, 900), tr.at(base), 0, 1, 0.4)
    for b in range(7): bed(tr, base + b, P_EYE[b], k, 'blast', ham=True, trem=True)
    hook_mass(tr, tr.at(base), head(HOOK, 8), k)
    violin(tr, tr.at(base + 3), shift(TRILL, k), 0.28, -0.1, drive=4.2)
    lead(tr, tr.at(base + 3), shift(TRILL, k), 0.14, 0.3)
    tr.add(shriek(bl * 1.4, 0.2, 'C6', 199), tr.at(base + 2, 2.5), 0.6, 1, 0.5)
    for b in (5, 6):
        for i in range(12): tr.add(tom(170 - 5 * (i + 12 * (b - 5)), 0.22, 8, 0.2), tr.at(base + b, i * TR), -0.4 + 0.07 * i, 1, 0.25)
    tr.add(riser(bl * 3, 0.13), tr.at(base + 4), 0, 1, 0.4)


PLAN = [('RIFF', 8, lambda tr, s, b: riff_section(tr, s, b)),
        ('STORM', 8, lambda tr, s, b: hook_section(tr, s, b, 'storm')),
        ('THEME', 8, lambda tr, s, b: hook_section(tr, s, b, 'theme')),
        ('CLIMB', 8, lambda tr, s, b: climb_section(tr, s, b, 'climb')),
        ('STRIKE', 8, lambda tr, s, b: hook_section(tr, s, b, 'strike')),
        ('HIM', 12, him),
        ('HIS KEY', 8, lambda tr, s, b: hook_section(tr, s, b, 'key', 2)),
        ('TEMPEST', 8, lambda tr, s, b: climb_section(tr, s, b, 'tempest')),
        ('BREAKDOWN', 12, breakdown),
        ('SOLO', 8, solo),
        ('TWIN', 8, twin),
        ('ALL', 8, lambda tr, s, b: hook_section(tr, s, b, 'all')),
        ('AGAIN', 8, lambda tr, s, b: hook_section(tr, s, b, 'again')),
        ('RIFF', 4, lambda tr, s, b: riff_section(tr, s, b, 4, True)),
        ('THE EYE', 7, eye)]
BARS = sum(n for _, n, _ in PLAN)


def compose():
    tr = Track('killerwatt_full', BPM, BARS)
    base = 0
    for s, (name, n, fn) in enumerate(PLAN):
        if name not in ('HIM', 'BREAKDOWN', 'SOLO', 'THE EYE'): tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
        fn(tr, s, base); base += n
    return tr


def marks():
    out, b = [], 0
    for name, n, _ in PLAN: out.append((name, b, n)); b += n
    return out


if __name__ == '__main__':
    review()
    if sys.argv[1:2] == ['check']: sys.exit()
    tr = seeded(71, compose)
    print(f'{BARS} bars, {tr.seconds:.0f} s'); section_levels(tr, marks())
    save(tr, sys.argv[1] if len(sys.argv) > 1 else 'killerwatt_full.ogg', 2.4, 0.27)
