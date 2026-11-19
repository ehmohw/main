"""DEMOCRATUS - the full battle theme. D minor, 150 BPM, the triplet gallop, 105 bars = 168 s loop.

Everything from the approved theme (the war cry, the hook, the climb, the dread, the surge, the climb a step up, the brink),
with the hook's harmony cleaned up (its held C# now sits on a diminished chord instead of rubbing against a D) and the
theremin's harmony made diatonic. New: an electric cello countermelody under the hook and climb, a lament (the prince who
handed out bread) after the violin is left alone, a duel between violin and theremin, and a final stand.

  0  WAR CRY     toms and the string ostinato, power chords; the theremin rising
  1  THE HOOK    the violin's hook, doubled an octave down
  2  BOTH        the hook, the theremin a third above, the cello's countermelody
  3  THE CLIMB   the climb on the violin, the theremin an octave under
  4  THE DREAD   the gallop held back: waterphone, the theremin's wail, a heartbeat
  5  THE SURGE   the violin's triplet arpeggios climbing for eight bars, the toms building
  6  HIGHER      the hook a whole step up, the cello with it
  7  CLIMB       the climb a whole step up - and a cut
  8  ALONE       4 bars: the violin alone with the hook's opening, slowed
  9  LAMENT      the prince who handed out bread: F major falling into D minor, violin and theremin, a heartbeat
  10 DUEL        the gallop back; violin and theremin trading phrases, then together
  11 FINALE      the hook with everything: violin, theremin, cello, choir
  12 LAST STAND  the climb with everything
  13 BRINK       5 bars: the hammer, the violin's trill, a roll and a riser - round again
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track, riser, tom
from boss_music import crash
from sovereign_music import boom, suck, seeded
from armada_music import stab, ther, ekick, esnare, mhat, sub808
from divine_music import choir, bones
from killerwatt_music import violin, waterphone, shriek, arc, chug
from storm import spark, buzz
from voices import cello
from full_common import (TR, L, bars, shift, stretch, head, tones, harmonize, check, line, save, section_levels, midi)

BPM = 150
DMIN = {2, 4, 5, 7, 9, 10, 0}

# ------------------------------------------------------------------ the material (approved lines, unchanged)
HOOK = bars(L('r:2t D5:t A5:2 G5:t F5:t E5:t  F5:1 D5:2t E5:t F5:1 G5:1  A5:2t Bb5:t A5:3  r:2t A5:t D6:2 C6:t Bb5:t A5:t  '
              'G5:1 F5:2t G5:t A5:1 E5:1  C#5:4  r:2t D5:t A5:2 Bb5:2t C6:t  D6:2 C6:t Bb5:t A5:t A5:1'), 8)
CLIMB = bars(L('G5:2t A5:t Bb5:1 D6:2  C6:2t Bb5:t A5:1 G5:2  Bb5:2t C6:t D6:1 F6:2  E6:3 C#6:1  '
               'D6:2t E6:t F6:1 A6:2  G6:2t F6:t E6:1 D6:2  Bb5:2t C6:t D6:1 E6:2  C#6:4'), 8)
SURGE = bars(L(' '.join(['D5:t F5:t A5:t'] * 4 + ['D5:t G5:t Bb5:t'] * 4 + ['F5:t A5:t C6:t'] * 4 + ['E5:t A5:t C#6:t'] * 4 +
                        ['A5:t D6:t F6:t'] * 4 + ['Bb5:t D6:t G6:t'] * 4 + ['C6:t F6:t A6:t'] * 4 + ['C#6:t E6:t A6:t'] * 2) + ' A6:2'), 8)
WAIL = bars(L('A4:4 Bb4:2 A4:2 A4:2 G4:2 F4:4 E4:4 F4:2 G4:2 A4:4 A4:4'), 8)

# ------------------------------------------------------------------ new material
HOOK_CELLO = bars(L('F3:3 A3:1  D4:2 C4:1 A3:1  Bb3:3 D4:1  D4:2 E4:2  F4:3 E4:1  E4:2 G4:2  F4:2 D4:2  E4:4'), 8)
# a descant for the theremin over the second hook: high, slow, soaring (in place of a parallel third)
DESCANT = bars(L('D6:4 F6:4 F6:4 A6:4 F6:4 E6:4 D6:2 F6:2 A6:2 E6:2'), 8)
CLIMB_CELLO = bars(L('Bb3:4  D4:2 Bb3:2  F4:4  E4:2 C#4:2  D4:4  D4:2 F4:2  Bb3:2 D4:2  C#4:4'), 8)
# THE LAMENT: the prince who handed out bread - a long-breathed line in F major that falls into D minor
LAMENT = bars(L('A5:3 G5:2t F5:t  G5:2 E5:2  F5:2t E5:t D5:3  r:2t D5:t F5:1 Bb5:2  Bb5:2t A5:t G5:3  F5:2 D5:2  '
                'E5:2t F5:t E5:3  C#5:4'), 8)
LAMENT_CELLO = bars(L('F3:4  E3:4  D3:4  D3:2 F3:2  G3:4  Bb3:2 D4:2  C#4:4  A3:4'), 8)
# THE DUEL: violin, theremin, violin, then both
DUEL_V1 = bars(L('D5:t F5:t A5:t D6:t A5:t F5:t E5:t F5:t G5:t A5:1  Bb5:2t A5:t G5:t F5:t E5:t F5:2'), 2)
DUEL_T1 = bars(L('G5:2 Bb5:2  D6:3 C6:1'), 2)
DUEL_V2 = bars(L('Bb5:t D6:t F6:t Bb6:t F6:t D6:t Bb5:t C6:t D6:t F6:1  E6:2t D6:t C6:t G5:t E5:t G5:2'), 2)
DUEL_BOTH = bars(L('A5:t C#6:t E6:t A6:1 G6:t F6:t E6:t D6:t C#6:t D6:t  E6:4'), 2)
TRILL = L('D6:t C#6:t D6:t ' * 4 + 'F6:t E6:t D6:t C#6:t Bb5:t A5:t D6:4 ' + 'D6:t C#6:t D6:t ' * 2 + 'E6:2 C#6:2 A5:4')

P_HOOK = ['Dm', 'Dm', 'Bb', 'Asus4', 'Dm', 'C#o7', 'Bb', 'Asus4']
P_CLIMB = ['Gm', 'Gm', 'Bb', 'A', 'Dm', 'Bb', 'Gm', 'A']
P_SURGE = ['Dm', 'Gm', 'F', 'A', 'Dm', 'Gm', 'F', 'A']
P_DREAD = ['Dm', 'Gm', 'F', 'Dm', 'A', 'Dm', 'Dm', 'A']
P_LAMENT = ['F', 'C', 'Dm', 'Bb', 'Gm', 'Bb', 'A', 'A']
P_DUEL = ['Dm', 'Dm', 'Gm', 'Gm', 'Bb', 'C', 'A', 'A']
P_BRINK = ['Dm', 'Bb', 'A', 'A', 'A']


def review():
    check('hook', HOOK, P_HOOK); check('hook cello', HOOK_CELLO, P_HOOK)
    check('descant', DESCANT, P_HOOK)
    check('climb', CLIMB, P_CLIMB, ok_ext=(9,)); check('climb cello', CLIMB_CELLO, P_CLIMB)
    check('climb +3rd', harmonize(CLIMB, 2, P_CLIMB, DMIN), P_CLIMB, ok_ext=(9,))
    check('wail', WAIL, P_DREAD); check('lament', LAMENT, P_LAMENT); check('lament cello', LAMENT_CELLO, P_LAMENT)
    check('lament -6th', harmonize(LAMENT, -5, P_LAMENT, DMIN), P_LAMENT)
    check('duel', DUEL_V1 + DUEL_T1 + DUEL_V2 + DUEL_BOTH, P_DUEL)


# ------------------------------------------------------------------ the band (as approved, reading chord names)
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
    elif style == 'soft':                                       # the lament's heartbeat, felt more than heard
        tr.add(boom(0.2, 70, 28, 1.6), t, 0, 1, 0.35); tr.add(boom(0.12, 70, 28, 1.2), t + 2 * TR * bt, 0, 1, 0.35)


def pickups(tr, bar):
    tr.add(ekick(0.3, 6), tr.at(bar, 2 * TR), 0, 1, 0.06); tr.add(ekick(0.3, 6), tr.at(bar, 2 + 2 * TR), 0, 1, 0.06)


def bass(tr, bar, ch, k=0, amp=1.0):
    t = tr.at(bar, 0); bt = tr.beat; c = tones(ch, 2, k)
    for b in range(4):                                          # gallop: on, rest, on (in threes)
        tr.add(chug(c[0] + 12, bt * 0.28, 0.2 * amp), t + b * bt, -0.1, 1, 0.08)
        tr.add(chug(c[0] + 12, bt * 0.28, 0.14 * amp), t + (b + 2 * TR) * bt, -0.1, 1, 0.08)
    tr.add(sub808(c[0], bt * 4 * 0.98, 0.22 * amp), t, 0, 1, 0.05)
    tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24] if len(c) == 3 else [x + 12 for x in c[:3]], bt * 0.9, 0.1 * amp, 4500, 500, 6.0),
           t, 0.2, 1, 0.3)


def ostinato(tr, bar, ch, k=0, amp=0.08):
    """the electric string section: spiccato triplets on the chord"""
    c = tones(ch, 4, k)
    pat = [(c[0], TR), (c[0], TR), (c[2], TR)] * 2 + [(c[0], TR), (c[1], TR), (c[2], TR), (c[0] + 12, TR), (c[2], TR), (c[1], TR)]
    violin(tr, tr.at(bar, 0), pat, amp, 0.4, 0.3, port=0.005, drive=2.0, legato=0.55)


def pads(tr, bar, ch, k=0, amp=0.06, vowel='a'):
    c = tones(ch, 4, k); bl = tr.beat * 4
    tr.add(choir(c, bl * 2, amp, 0.3, vowel), tr.at(bar), 0, 1, 0.7)
    tr.add(bones([c[0] - 12, c[2] - 12], bl * 2 * 0.95, 0.07), tr.at(bar), -0.2, 1, 0.5)


def current(tr, bar, ch, k=0, more=False):
    """his electricity: buzz-stabs on the pickups, a spark on three, an arc every fourth bar"""
    bt = tr.beat; f = 440 * 2 ** ((tones(ch, 4, k)[0] - 69) / 12)
    for x in (3 + TR, 3 + 2 * TR): tr.add(buzz(f, bt * 0.25, 0.07), tr.at(bar, x), 0.45, 1, 0.2)
    if more or bar % 2 == 1: tr.add(buzz(f * 2, bt * 0.3, 0.06), tr.at(bar, 1 + 2 * TR), -0.45, 1, 0.2)
    tr.add(spark(0.16, bar), tr.at(bar, 2), (-0.5, 0.5)[bar % 2], 1, 0.35)
    if bar % 4 == 3: tr.add(arc(0.2, 0.9, 200 + bar), tr.at(bar, 3), 0.5, 1, 0.4)


def hum(tr, t0, notes, k=0):
    """the long notes of the hook humming with current, an octave down"""
    t = t0
    for x, d in notes:
        if x is not None and d >= 1: tr.add(buzz(440 * 2 ** ((midi(x) + k - 12 - 69) / 12), d * tr.beat * 0.9, 0.035), t, -0.3, 1, 0.3)
        t += d * tr.beat


def band(tr, base, prog, k=0, style='charge', ost=0.08, choir_amp=0.06, crash_every=2, more=False, from_bar=0):
    for b in range(from_bar, len(prog)):
        bar = base + b; ch = prog[b]
        drums(tr, bar, style)
        if style != 'tribal' or b >= 4: pickups(tr, bar)
        bass(tr, bar, ch, k, 1.15 if more else 1.0)
        ostinato(tr, bar, ch, k, ost)
        if b % 2 == 0 and choir_amp: pads(tr, bar, ch, k, choir_amp)
        if b % crash_every == 0: tr.add(crash(0.18 if crash_every == 1 else 0.13), tr.at(bar), (-0.3, 0.3)[b % 2], 1, 0.5)
        current(tr, bar, ch, k, more)


# ------------------------------------------------------------------ the sections
def war(tr, base):
    band(tr, base, P_HOOK, 0, 'tribal', 0.1, 0)
    for b in range(4, 8, 2): pads(tr, base + b, P_HOOK[b], 0, 0.06)
    for b in (3, 7): tr.add(arc(0.2, 0.9, b), tr.at(base + b, 3), 0.5, 1, 0.4)
    ther(tr, tr.at(base + 4), L('D5:8 A5:8'), 0.18, -0.3, 0.5, port=0.25)


def hook(tr, base, k=0, kind='hook'):
    t0 = tr.at(base)
    band(tr, base, P_HOOK, k, 'charge', 0.08, 0.08 if kind == 'finale' else 0.06, 1 if kind == 'finale' else 2, kind == 'finale')
    violin(tr, t0, shift(HOOK, k), 0.32, -0.1)
    hum(tr, t0, HOOK, k)
    if kind in ('hook', 'finale', 'higher'): violin(tr, t0, shift(HOOK, k - 12), 0.16, 0.25, drive=3.0)
    if kind in ('both', 'higher', 'finale'): cello(tr, t0, shift(HOOK_CELLO, k), 0.22, -0.3)
    if kind == 'both': ther(tr, t0, shift(DESCANT, k), 0.17, 0.3, 0.5, port=0.12)
    if kind == 'finale':
        ther(tr, t0, shift(HOOK, k + 12), 0.18, 0.3, 0.45, port=0.04, echo_=False)
        line(tr, t0, shift(HOOK, k), lambda x, d: choir([x], d, 0.05, 0.1, 'a'), 0.05, 0.7)


def climb(tr, base, k=0, kind='climb'):
    t0 = tr.at(base)
    band(tr, base, P_CLIMB, k, 'charge', 0.08, 0.08, 1 if kind == 'stand' else 2, kind == 'stand')
    violin(tr, t0, shift(CLIMB, k), 0.32, -0.1)
    if kind == 'climb': ther(tr, t0, shift(CLIMB, k - 12), 0.12, 0.35, 0.5, port=0.05, echo_=False)
    if kind in ('stand', 'higher'): cello(tr, t0, shift(CLIMB_CELLO, k), 0.22, -0.3)
    if kind == 'stand':
        ther(tr, t0, harmonize(CLIMB, 2, P_CLIMB, DMIN, k), 0.17, 0.3, 0.45, port=0.04, echo_=False)
        line(tr, t0, shift(CLIMB, k), lambda x, d: choir([x], d, 0.05, 0.1, 'a'), 0.05, 0.7)
        violin(tr, t0, shift(CLIMB, k - 12), 0.14, 0.25, drive=3.0)


def dread(tr, base):
    bl = tr.beat * 4; t0 = tr.at(base)
    band(tr, base, P_DREAD, 0, 'tribal', 0.1, 0, 2)
    for b in range(8): drums(tr, base + b, 'heart')
    for b, f in ((0, 'D3'), (2, 'G2'), (4, 'A2'), (6, 'D3')):
        tr.add(waterphone(f, bl * 2.5, 0.26, seed=b), tr.at(base + b), (-0.5, 0.5)[b // 2 % 2], 1, 0.55)
    ther(tr, t0, WAIL, 0.27, 0.15, 0.5, port=0.12)
    tr.add(choir(tones('Dm', 3), bl * 8, 0.07, 3.0, 'u'), t0, 0, 1, 0.8)
    tr.add(suck(bl, 0.22), tr.at(base + 7), 0.2, 1, 0.4)


def surge(tr, base):
    bl = tr.beat * 4; t0 = tr.at(base)
    band(tr, base, P_SURGE, 0, 'tribal', 0.1, 0, 2)
    for b in range(4, 8, 2): pads(tr, base + b, P_SURGE[b], 0, 0.05 + 0.01 * (b - 4))
    violin(tr, t0, SURGE, 0.27, -0.1, port=0.008, drive=3.8)
    cello(tr, t0, L('D3:4 G3:4 F3:4 A3:4 D4:4 G4:4 F4:4 E4:4'), 0.16, -0.35)
    tr.add(shriek(bl * 1.5, 0.12, 'D6', 5), tr.at(base + 3, 2), 0.5, 1, 0.5)
    for i in range(12): tr.add(esnare(0.06 + 0.02 * i, 190), tr.at(base + 7, i * TR), 0.05, 1, 0.3)
    tr.add(riser(bl * 2, 0.1), tr.at(base + 6), 0, 1, 0.4)


def alone(tr, base):
    """the violin alone: the hook's opening at half speed, over a held D minor and nothing else"""
    bl = tr.beat * 4; t0 = tr.at(base)
    tr.add(crash(0.3, 3.0), t0, 0.2, 1, 0.8)
    tr.add(boom(0.3, 60, 26, 3.0), t0, 0, 1, 0.5)
    violin(tr, t0, stretch(head(HOOK, 8), 2), 0.28, 0.0, 0.75, drive=1.6, depth=0.014)
    tr.add(choir(tones('Dm', 3), bl * 4, 0.06, 2.5, 'u'), t0, 0, 1, 0.85)
    tr.add(sub808(midi('D2'), bl * 4, 0.12), t0, 0, 1, 0.1)
    for b in (1, 3): tr.add(spark(0.08, 900 + b), tr.at(base + b, 2), (-0.6, 0.6)[b // 2], 1, 0.7)


def lament(tr, base):
    """the prince who handed out bread"""
    bl = tr.beat * 4; t0 = tr.at(base)
    for b, ch in enumerate(P_LAMENT):
        bar = base + b; c = tones(ch, 3)
        drums(tr, bar, 'soft')
        tr.add(sub808(tones(ch, 2)[0], bl * 0.98, 0.12), tr.at(bar), 0, 1, 0.1)
        if b % 2 == 0: tr.add(choir([x + 12 for x in c], bl * 2, 0.05, 0.9, 'u'), tr.at(bar), 0, 1, 0.8)
        if b >= 4: ostinato(tr, bar, ch, 0, 0.035 + 0.008 * (b - 4))
    violin(tr, t0, LAMENT, 0.28, -0.05, 0.6, drive=1.8, depth=0.013, port=0.06)
    ther(tr, t0, harmonize(LAMENT, -5, P_LAMENT, DMIN), 0.13, 0.35, 0.6, port=0.08)
    cello(tr, t0, LAMENT_CELLO, 0.2, -0.35, 0.55)
    tr.add(waterphone('A2', bl * 3, 0.12, seed=21), tr.at(base + 6), 0.4, 1, 0.7)
    tr.add(riser(bl * 1.5, 0.08), tr.at(base + 6, 2), 0, 1, 0.4)


def duel(tr, base):
    t0 = tr.at(base)
    band(tr, base, P_DUEL, 0, 'charge', 0.08, 0.06, 2)
    violin(tr, t0, DUEL_V1, 0.32, -0.25)
    ther(tr, tr.at(base + 2), DUEL_T1, 0.26, 0.3, 0.5, port=0.06)
    violin(tr, tr.at(base + 4), DUEL_V2, 0.32, -0.25)
    ther(tr, tr.at(base + 5), L('E5:2 G5:2'), 0.2, 0.3, 0.5, port=0.06)
    violin(tr, tr.at(base + 6), DUEL_BOTH, 0.32, -0.2)
    ther(tr, tr.at(base + 6), harmonize(DUEL_BOTH, -2, P_DUEL, DMIN, 0, 24), 0.2, 0.3, 0.45, port=0.04, echo_=False)
    cello(tr, t0, L('D3:8 G3:8 Bb3:4 C4:4 A3:8'), 0.18, -0.35)


def brink(tr, base):
    bl = tr.beat * 4
    for b, ch in enumerate(P_BRINK):
        c = tones(ch, 2); bar = base + b
        hits = (0, 2 * TR, 1, 1 + 2 * TR, 2, 2 + 2 * TR, 3, 3 + TR, 3 + 2 * TR) if b < 3 else (0, 1, 2, 3)
        for x in hits:
            tr.add(stab([c[0] + 12, c[2] + 12, c[0] + 24], tr.beat * 0.3, 0.13), tr.at(bar, x), 0.2, 1, 0.3)
            tr.add(ekick(0.55), tr.at(bar, x), 0, 1, 0.06)
        tr.add(sub808(c[0], bl * 0.98, 0.22), tr.at(bar), 0, 1, 0.05)
        if b < 4: current(tr, bar, ch, 0, True)
    tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
    violin(tr, tr.at(base), TRILL, 0.28, -0.1, drive=4.2)
    tr.add(choir(tones('A', 4), bl * 3, 0.07, 1.0, 'a'), tr.at(base + 2), 0, 1, 0.7)
    for b in (3, 4):
        for i in range(12): tr.add(tom(170 - 4 * (i + 12 * (b - 3)), 0.2 + 0.004 * i, 8, 0.2), tr.at(base + b, i * TR), -0.4 + 0.07 * i, 1, 0.25)
    tr.add(riser(bl * 2, 0.13), tr.at(base + 3), 0, 1, 0.4)
    for b in range(5): tr.add(spark(0.2, 700 + b), tr.at(base + b, 0), 0.4, 1, 0.3)


PLAN = [('WAR CRY', 8, war), ('HOOK', 8, lambda tr, b: hook(tr, b)), ('BOTH', 8, lambda tr, b: hook(tr, b, 0, 'both')),
        ('CLIMB', 8, lambda tr, b: climb(tr, b)), ('DREAD', 8, dread), ('SURGE', 8, surge),
        ('HIGHER', 8, lambda tr, b: hook(tr, b, 2, 'higher')), ('CLIMB +2', 8, lambda tr, b: climb(tr, b, 2, 'higher')),
        ('ALONE', 4, alone), ('LAMENT', 8, lament), ('DUEL', 8, duel), ('FINALE', 8, lambda tr, b: hook(tr, b, 0, 'finale')),
        ('LAST STAND', 8, lambda tr, b: climb(tr, b, 0, 'stand')), ('BRINK', 5, brink)]
BARS = sum(n for _, n, _ in PLAN)


def compose():
    tr = Track('democratus_full', BPM, BARS)
    base = 0
    for name, n, fn in PLAN:
        if name not in ('ALONE', 'LAMENT', 'WAR CRY'): tr.add(crash(0.45, 3.0), tr.at(base), 0.3, 1, 0.55)
        fn(tr, base); base += n
    return tr


def marks():
    out, b = [], 0
    for name, n, _ in PLAN: out.append((name, b, n)); b += n
    return out


if __name__ == '__main__':
    review()
    if sys.argv[1:2] == ['check']: sys.exit()
    tr = seeded(53, compose)
    print(f'{BARS} bars, {tr.seconds:.0f} s'); section_levels(tr, marks())
    save(tr, sys.argv[1] if len(sys.argv) > 1 else 'democratus_full.ogg', 2.4, 0.28)
