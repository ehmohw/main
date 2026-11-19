"""EMMA - the full theme. D major, 72 BPM, peaceful, no drums. 57 bars = 190 s loop.

The approved theme (Democratus's hook and climb made gentle, on piano, with wind chimes, harp, flute and soft strings),
with its sixth bar re-harmonized (the held C# now sits on F# minor instead of rubbing against G), and new material:

  0  MORNING      4  wind chimes, the piano's slow arpeggios
  1  THE HOOK     8  the piano melody
  2  THE CLIMB    8  piano, flute and strings
  3  HER SONG     8  a melody of her own, in G major, on the cello, the piano rolling under it
  4  HER SONG II  8  the same song on a clean violin, the flute floating above, the cello under
  5  REFLECTION   4  B minor: a music box plays the opening of HIS theme, as he wrote it, in minor
  6  HIGH         8  the hook an octave up, the flute with it, more chimes
  7  HOME         8  the hook, the cello's countermelody, strings and harp, coming home to D
  8  REST         1  the chimes, and D
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import Track
from sovereign_music import seeded
from armada_music import apad, addc
from emma_music import piano, chimes, flute, harp
from voices import cello_line, clean_violin_line, musicbox
from full_common import (TR, L, bars, shift, head, tail, tones, check, line, save, section_levels, midi)
from democratus_full import HOOK, CLIMB

BPM = 72
MAJ = {5: 6, 10: 11, 0: 1}                                   # D minor -> D major: F->F#, Bb->B, C->C#


def major(notes):
    return [(None if x is None else x + (MAJ[x % 12] - x % 12 if x % 12 in MAJ else 0), d) for x, d in notes]


HOOKM = major(HOOK); HOOKM[-1] = (midi('D5'), HOOKM[-1][1])       # ends home on D
CLIMBM = major(CLIMB); CLIMBM[-1] = (midi('A5'), CLIMBM[-1][1])
SONG = bars(L('B4:2t A4:t G4:1 D5:2  F#5:2t E5:t D5:1 A4:2  G4:2t A4:t B4:1 E5:2  E5:2t D5:t C5:1 G4:2  '
              'B4:2t C5:t D5:1 G5:2  F#5:2t E5:t B4:1 E5:2  C#5:2t D5:t E5:1 A5:2  F#5:3 r:1'), 8)
SONG_FLUTE = bars(L('D6:4 A5:4 B5:4 C6:2 E6:2 D6:4 B5:4 C#6:4 D6:4'), 8)
SONG_BASS = bars(L('G2:4 F#2:4 E2:4 C3:4 D3:4 E3:4 C#3:4 D3:4'), 8)
HOME_CELLO = bars(L('F#3:3 A3:1  D4:2 C#4:1 A3:1  B3:3 D4:1  C#4:2 E4:2  F#4:3 E4:1  A3:2 F#3:2  B3:2 D4:2  D4:4'), 8)
REFLECT = bars(shift(head(HOOK, 12), -3) + L('E5:2 C#5:2'), 4)     # HIS opening, in B minor, as he wrote it

P_HOOK = ['D', 'D', 'Bm', 'A', 'D', 'F#m', 'Bm', 'A']
P_CLIMB = ['G', 'G', 'Bm', 'A', 'D', 'Bm', 'G', 'A']
P_HOME = ['D', 'D', 'Bm', 'A', 'D', 'F#m', 'Bm', 'D']
P_SONG = ['G', 'D', 'Em', 'C', 'G', 'Em', 'A', 'D']
P_REFLECT = ['Bm', 'Bm', 'G', 'A']
P_MORNING = ['D', 'G', 'D', 'A']


def review():
    check('hook', HOOKM, P_HOOK); check('climb', CLIMBM, P_CLIMB, ok_ext=(9,)); check('home', HOOKM, P_HOME)
    check('home cello', HOME_CELLO, P_HOME); check('song', SONG, P_SONG); check('song flute', SONG_FLUTE, P_SONG)
    check('song bass', SONG_BASS, P_SONG); check('reflection', REFLECT, P_REFLECT)


# ------------------------------------------------------------------ the players
def accomp(tr, bar, ch, amp=1.0, pad=True):
    """the left hand and a slow rolling arpeggio, in the triplet lilt"""
    c = tones(ch, 3); bt = tr.beat
    tr.add(piano(c[0] - 12, bt * 4, 0.12 * amp, 0.5), tr.at(bar), -0.2, 1, 0.5)
    arp = [c[0], c[2], c[1] + 12, c[2], c[0] + 12, c[2]]
    for i, x in enumerate(arp):
        tr.add(piano(x, bt * 1.5, 0.07 * amp, 0.4), tr.at(bar, i * 2 * TR), (-0.25, 0.1)[i % 2], 1, 0.55)
    if pad: tr.add(apad([x + 12 for x in c], bt * 4 * 1.05, 0.03 * amp, 900, 1.5, 1.5), tr.at(bar), 0, 1, 0.8)


def melody(tr, t0, notes, k=0, amp=0.16, pan=0.1):
    line(tr, t0, shift(notes, k), lambda x, d: piano(x, d, amp, 0.75), pan, 0.5)


def gliss(tr, t0, ch, amp=0.05):
    c = tones(ch, 4); notes = [c[0], c[1], c[2], c[0] + 12, c[1] + 12, c[2] + 12, c[0] + 24]
    for i, x in enumerate(notes): tr.add(harp(x, amp, i), t0 + i * 0.07, (-0.5 + 0.15 * i), 1, 0.6)


def strings(tr, bar, ch, amp=0.04):
    c = tones(ch, 3)
    tr.add(apad([c[0], c[2], c[1] + 12], tr.beat * 4 * 1.1, amp, 1400, 1.2, 1.5, voices=5, det=0.006, depth=0.15), tr.at(bar), -0.1, 1, 0.75)


def play(tr, t0, s, pan, wet):
    addc(tr, s, t0, pan, 1, wet)


# ------------------------------------------------------------------ the sections
def morning(tr, base):
    for b, ch in enumerate(P_MORNING): accomp(tr, base + b, ch, 0.8)
    chimes(tr, base, 4, 0.6, 0.02, 1)


def hook(tr, base, kind):
    t0 = tr.at(base); prog = P_HOME if kind == 'home' else P_HOOK
    for b in range(8): accomp(tr, base + b, prog[b], 0.9 if kind == 'high' else 1.0)
    gliss(tr, t0, prog[0])
    if kind == 'hook': melody(tr, t0, HOOKM)
    if kind == 'high':
        melody(tr, t0, HOOKM, 12, 0.11, 0.25)
        tr.add(flute(shift(HOOKM, 0), tr.beat, 0.06), t0, -0.3, 1, 0.65)
        for b in range(8): strings(tr, base + b, prog[b])
    if kind == 'home':
        melody(tr, t0, HOOKM, 0, 0.14)
        play(tr, t0, cello_line(HOME_CELLO, tr.beat, 0.1, drive=0.8, depth=0.008), -0.3, 0.55)
        for b in range(8): strings(tr, base + b, prog[b], 0.035)
        gliss(tr, tr.at(base + 4), prog[4], 0.04)
        play(tr, tr.at(base + 6), clean_violin_line(shift(tail(HOOKM, 24), 12), tr.beat, 0.09), 0.35, 0.65)  # his instrument, gentle
    chimes(tr, base, 8, 0.35 if kind == 'high' else 0.2, 0.014, base)


def climb(tr, base):
    t0 = tr.at(base)
    for b, ch in enumerate(P_CLIMB): accomp(tr, base + b, ch); strings(tr, base + b, ch)
    gliss(tr, t0, P_CLIMB[0])
    tr.add(flute(CLIMBM, tr.beat, 0.05), t0, 0.3, 1, 0.65)
    melody(tr, t0, CLIMBM)
    chimes(tr, base, 8, 0.2, 0.014, base)


def song(tr, base, second=False):
    """her own song: G major, a lilt of its own"""
    t0 = tr.at(base)
    for b, ch in enumerate(P_SONG):
        accomp(tr, base + b, ch, 0.85, pad=not second)
        if second: strings(tr, base + b, ch, 0.03)
    gliss(tr, t0, P_SONG[0], 0.045)
    if not second:
        play(tr, t0, cello_line(shift(SONG, -12), tr.beat, 0.11, drive=0.8, depth=0.01, port=0.06), -0.15, 0.55)
        line(tr, tr.at(base + 7, 3), L('A4:1'), lambda x, d: harp(x, 0.05, 3), 0.3, 0.6)
    else:
        play(tr, t0, clean_violin_line(SONG, tr.beat, 0.1), 0.15, 0.55)
        tr.add(flute(SONG_FLUTE, tr.beat, 0.035), t0, 0.4, 1, 0.7)
        play(tr, t0, cello_line(SONG_BASS, tr.beat, 0.08, drive=0.8, depth=0.006, legato=0.9), -0.35, 0.5)
    chimes(tr, base, 8, 0.12, 0.012, base + 300)


def reflection(tr, base):
    """a music box with his opening, in B minor - the theme she was given, before it was hers"""
    bl = tr.beat * 4; t0 = tr.at(base)
    for b, ch in enumerate(P_REFLECT):
        c = tones(ch, 3)
        tr.add(piano(c[0] - 12, bl, 0.1, 0.4), tr.at(base + b), -0.2, 1, 0.6)
        strings(tr, base + b, ch, 0.04)
    line(tr, t0, shift(REFLECT, 12), lambda x, d: musicbox(x, max(d, 1.5), 0.09), 0.2, 0.65)
    tr.add(harp(midi('B5'), 0.04, 7), tr.at(base + 2, 2), 0.4, 1, 0.7)


def rest(tr, base):
    accomp(tr, base, 'D', 0.7)
    chimes(tr, base, 1, 0.7, 0.02, 999)


PLAN = [('MORNING', 4, morning), ('HOOK', 8, lambda tr, b: hook(tr, b, 'hook')), ('CLIMB', 8, climb),
        ('HER SONG', 8, song), ('HER SONG II', 8, lambda tr, b: song(tr, b, True)), ('REFLECTION', 4, reflection),
        ('HIGH', 8, lambda tr, b: hook(tr, b, 'high')), ('HOME', 8, lambda tr, b: hook(tr, b, 'home')), ('REST', 1, rest)]
BARS = sum(n for _, n, _ in PLAN)


def compose():
    tr = Track('emma_full', BPM, BARS)
    base = 0
    for name, n, fn in PLAN: fn(tr, base); base += n
    return tr


def marks():
    out, b = [], 0
    for name, n, _ in PLAN: out.append((name, b, n)); b += n
    return out


if __name__ == '__main__':
    review()
    if sys.argv[1:2] == ['check']: sys.exit()
    tr = seeded(5, compose)
    print(f'{BARS} bars, {tr.seconds:.0f} s'); section_levels(tr, marks())
    save(tr, sys.argv[1] if len(sys.argv) > 1 else 'emma_full.ogg', 3.2, 0.2, pct=70)
