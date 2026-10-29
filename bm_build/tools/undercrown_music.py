"""2.98a: synthesises THE UNDERCROWN's soundtrack - the final dungeon's own music, from the seam to the throne
(vendor/uc_*.ogg). Strings to the last: a solo violin, a violin section, cellos - and an ELECTRIC VIOLIN (the violin driven
through an overdrive and a cabinet, chorused, with a dotted-eighth delay), which arrives far off in the Drowned Ward and has
the lead by the Throne Gate.

ONE GRID FOR EVERY TRACK, SO THEY JOIN WITHOUT A SEAM. F minor, 120 BPM, 4/4 - a bar is exactly 2 s. Every track is built of
8-bar sections (16 s); every section starts on F minor and ends on a chord that leads back to it. phase240 switches from one
exploration tier to the next only on a section boundary (16 s into a track, 32, ...), with THE SWELL (uc_swell, 2 s: a reversed
cymbal, a riser and a timpani roll, landing on the downbeat) played over the last bar - so one track hands to the next as if it
were the same piece turning a page. A fight cuts in on the next bar with its own downbeat (an impact); it hands back on a
section boundary, through the swell.

THE SOVEREIGN'S MOTIF S (C F Ab Gb F E F...; tools/sovereign_music.py) runs through all of it, so the boss's music, when it
comes, is where the dungeon was going. Each tier is louder (its own render level) and fuller than the last.

  uc_t1  I.   THE DESCENT       128 s  the Hall of Chains and the Frozen Ward. A drone, far chains, a tolling bell, a heartbeat
                                       timpani; the solo violin carries S low and slow, ghostly harmonics above; a lament bass
  uc_t2  II.  THE HEXED DARK    128 s  the Hexed Ward. A cello pulse in eighths; a hex melody (H); the monks' choir; a theremin
                                       sliding in the dark; the taiko, softly
  uc_t3  III. THE DROWNED DEEP  128 s  the Drowned Ward. Driving low strings, half-time drums, organ, ship's bells; violins in
                                       octaves - and the electric violin, distant, answering through its delay
  uc_t4  IV.  THE THRONE GATE    96 s  the three Shards. Full drums; the electric violin has S; the violin cries the Dread's head
                                       three times (fear, hunger, war); frantic sixteenths
  uc_t5  V.   A THOUSAND EYES    96 s  the Stair of Eyes. Held breath: a ticking, the eye's tritone, whispers, a tremolo; the
                                       electric violin wails; one great swell where the eyes open, then back to the ticking
  uc_t6  VI.  THE LAST DOOR     128 s  the antechamber and the throne hall, before it wakes. Everything: bells, the great organ,
                                       the full choir, double-kick, the violins in octaves under the electric violin's S at the
                                       top - once, the light (S in F major, a single violin); then the end
  uc_c1  THE THRALLS             64 s  a fight in the upper wards: spiccato violins, taiko, chains as drums, S at double speed
  uc_c2  THE DREAD KNIGHTS       64 s  a fight in the deep: the electric violin's chugging riff, double-kick, organ stabs, S2
  uc_swell                        2 s  the page turn
(After the fall, phase240 plays AUREL - vendor/disc_aurel.ogg - once: the light it was.)

Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg):
    python3 tools/undercrown_music.py [t1 t2 t3 t4 t5 t6 c1 c2 swell] [check]"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, mix, T, env, lp, hp, bp, bell, sub, strings, kick, snare, hat, riser, tom
from boss_music import timp, crash, mel, tp, theremin
from dread_music import violin, cello
from sovereign_music import (great_bell, clank, rattle, chain_hit, taiko, chorus, great_organ, drone, gaze, whisper, boom, pop, glass,
                             suck, edge, S, DREAD_HEAD, dur_x, chd, ladder, frantic, render, _guarded, _decode, seeded)

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
BPM = 120                                   # (a bar: 2 s; a section: 8 bars, 16 s)
SEC = 8
LEN = {'t1': 64, 't2': 64, 't3': 64, 't4': 48, 't5': 48, 't6': 64, 'c1': 32, 'c2': 32}      # (bars)

# ---- the harmony: one chord a bar, each section from F minor back to the brink of it
H_S = [('F2', 'm'), ('Db2', 'M'), ('C2', 'M'), ('F2', 'm'), ('Bb1', 'm'), ('Gb2', 'M'), ('C2', 'M'), ('C2', '7b9')]      # (under S)
H_N = [('F2', 'm'), ('F2', 'm'), ('Gb2', 'M'), ('Gb2', 'M'), ('F2', 'm'), ('F2', 'm'), ('E2', 'dim'), ('C2', '7b9')]       # (the toll)
H_L = [('F2', 'm'), ('E2', 'aug'), ('Eb2', 'lam'), ('D2', 'hd'), ('Db2', 'M'), ('C2', 'sus'), ('C2', 'M'), ('C2', '7b9')]  # (the lament)
H_H = [('F2', 'm'), ('C2', 'M'), ('F2', 'm'), ('Db2', 'M'), ('Gb2', 'M'), ('Db2', 'M'), ('C2', 'M'), ('C2', 'M')]          # (under H)
H_D = [('F2', 'm'), ('Ab1', 'M'), ('Db2', 'M'), ('Bb1', 'm'), ('Gb2', 'M'), ('Db2', 'M'), ('C2', 'M'), ('C2', '7b9')]       # (driving)
H_E = [('F2', 'm'), ('F2', 'm'), ('F2', 'mt'), ('F2', 'mt'), ('F2', 'm'), ('F2', 'mt'), ('E2', 'dim'), ('C2', '7b9')]      # (the eyes)
H_M = [('F2', 'M'), ('Bb1', 'M'), ('C2', 'M'), ('F2', 'M'), ('Db2', 'M'), ('Bb1', 'm'), ('C2', 'M'), ('C2', '7b9')]         # (the light)
EXTRA = {'aug': (0, 4, 8), 'lam': (0, 5, 9), 'mt': (0, 3, 6, 7)}       # (E aug: C/E; Eb 'lam': Ab/Eb; F 'mt': F minor and its tritone)


def M(x):
    """a note as MIDI, whether named ('F5') or already a number (a transposed line's)"""
    return int(x) if isinstance(x, (int, np.integer)) else m(x)


def ch(c):
    root, kind = c
    if kind in EXTRA:
        r = m(root); return [r + i for i in EXTRA[kind]]
    return chd(root, kind)


H = mel('F5:1.5 G5:.5 Ab5:2 G5 F5 E5:2 F5 Ab5 C6:2 Db6:3 C6 Bb5:1.5 Ab5:.5 Gb5:2 F5 Gb5 Ab5:2 G5 F5 E5 G5 C5:4')   # (the hex melody: 8 bars)
SM = mel('C4:2 F4:2 A4:3 G4:1 F4:2 E4:2 F4:4 D5:2 C5:2 Bb4:2 A4:1 G4:1 F4:2 E4:1 D4:1 C4:4')                        # (S in F major: the light)
S2 = dur_x(S, 0.5)
assert sum(d for _, d in H) == 32 and sum(d for _, d in SM) == 32


def at(tr, bar, beat=0.0):
    return (bar * 4 + beat) * tr.beat


def ply(tr, t0, notes, inst, pan=0.0, gain=1.0, wet=0.3, legato=0.95):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(inst(x, d * tr.beat * legato), t, pan, gain, wet)
        t += d * tr.beat
    return t


# ====================================================================== the electric violin
def evln(x, d, amp=0.3, drive=5.0, seed=0, scoop=0.018, bright=1.15):
    """a violin through an overdrive and a cabinet: the bowed note, its lows cut, driven into a soft clip, the fizz rolled
    off, a presence bump - singing, with a bite"""
    s = violin(x, d + 0.04, 1.0, vib=6.3, depth=0.0085, scoop=scoop, attack=0.018, bright=bright, seed=seed)
    s = hp(s, 200)
    s = np.tanh(s * drive) / np.tanh(drive)
    s = lp(s, 5400, 2) * 0.85 + bp(s, 1700, 3300, 2) * 0.45
    return amp * edge(s, 0.02)


def eplay(tr, t, x, d, amp=0.3, pan=0.0, wet=0.3, fb=0.36, taps=3, drive=5.0, scoop=0.018):
    """one electric note: two takes a hair apart (the chorus), and its dotted-eighth echoes ping-ponging away"""
    s = evln(x, d, amp, drive, 0, scoop)
    s2 = evln(x, d, amp * 0.55, drive, 1, scoop)
    tr.add(s, t, pan - 0.15, 1, wet); tr.add(s2, t + 0.011, pan + 0.25, 1, wet)
    dl = tr.beat * 0.75
    e = lp(s, 3200)
    for i in range(1, taps + 1):
        tr.add(e, t + dl * i, -0.65 if i % 2 else 0.65, fb ** i, min(0.9, wet + 0.2))


def eline(tr, t0, notes, amp=0.3, pan=0.0, wet=0.3, legato=0.97, **k):
    t = t0
    for x, d in notes:
        if x is not None: eplay(tr, t, x, d * tr.beat * legato, amp, pan, wet, **k)
        t += d * tr.beat
    return t


def chug(tr, t, root, d, amp=0.3, pan=0.0):
    """the riff: a low electric note, short and hard, its fifth under it (a violin's power chord)"""
    r = m(root) if isinstance(root, str) else root
    s = evln(r, d, amp, 9.0, 3, 0.004, 0.9) + evln(r + 7, d, amp * 0.6, 9.0, 4, 0.004, 0.9)
    s *= np.exp(-T(len(s) / SR) * 3.0)
    tr.add(s, t, pan - 0.35, 1, 0.12); tr.add(s * 0.8, t + 0.009, pan + 0.35, 1, 0.12)


# ====================================================================== shared parts
def vsolo(x, d, amp=0.32, **k):
    return violin(x, d, amp, **k)


def vsec(x, d, amp=0.26):
    return violin(x, d, amp, voices=3, depth=0.005)


def harmonic(x, d, amp=0.08):
    """a flautando harmonic: barely touched, almost no bow"""
    return violin(x, d, amp, vib=4.5, depth=0.003, attack=0.4, bright=0.35)


def spic(tr, t, x, amp=0.22, pan=0.0, wet=0.3, dur=0.25):
    tr.add(violin(x, tr.beat * dur * 0.8, amp, attack=0.012, scoop=0.004, depth=0.0), t, pan, 1, wet)


def drone_sec(tr, s, notes, amp=0.25):
    """a drone under one section, overlapping the next a little (its release under their attack)"""
    tr.add(drone(notes, SEC * 2 + 2.5, amp), at(tr, s * SEC) - 0.5, 0, 1, 0.5)


def pad(tr, s, prog, amp=0.12, vowel='u', oct_=12, attack=0.6):
    for b, c in enumerate(prog):
        tr.add(chorus([x + oct_ for x in ch(c)], tr.beat * 4 + 0.4, amp, attack, vowel), at(tr, s * SEC + b), 0, 1, 0.55)


def organ(tr, s, prog, amp=0.12, oct_=12, every=1):
    for b, c in enumerate(prog):
        if b % every: continue
        tr.add(great_organ([x + oct_ for x in ch(c)] + [ch(c)[0]], tr.beat * 4 * every + 0.2, amp), at(tr, s * SEC + b), 0, 1, 0.45)


def bassline(tr, s, prog, amp=0.3, rhythm=(0,), dur=4.0):
    for b, c in enumerate(prog):
        r = ch(c)[0]
        for bt in rhythm:
            tr.add(cello(r, tr.beat * dur * 0.95, amp), at(tr, s * SEC + b, bt), 0, 1, 0.3)


def ostinato(tr, s, prog, amp=0.18, shape=(0, 12, 7, 12, 0, 12, 8, 7), lo=12):
    """the cello pulse: eighths over each bar's root"""
    for b, c in enumerate(prog):
        r = ch(c)[0] + lo
        for i, k in enumerate(shape):
            tr.add(cello(r + k, tr.beat * 0.42, amp * (1.0 if i % 2 == 0 else 0.7)), at(tr, s * SEC + b, i * 0.5), 0.15, 1, 0.25)


def drive16(tr, s, prog, amp=0.14, lo=m('C4'), pan=0.0):
    """sixteenths in the low strings: the chord's tones, rocking"""
    for b, c in enumerate(prog):
        up = ladder(ch(c), lo, 4)
        pat = [up[0], up[1], up[0], up[2], up[0], up[1], up[0], up[3]] * 2
        for i, x in enumerate(pat):
            spic(tr, at(tr, s * SEC + b, i * 0.25), x, amp * (1.0 if i % 4 == 0 else 0.65), pan, 0.25)


def frantic_sec(tr, s, prog, amp=0.12, lo=m('F5')):
    for b, c in enumerate(prog):
        for i, x in enumerate(frantic(ch(c), b, lo)):
            spic(tr, at(tr, s * SEC + b, i * 0.25), x, amp, 0.35 if i % 2 else -0.35, 0.3)


def toll(tr, s, bars=(0, 4), note='F2', amp=0.5):
    for b in bars:
        tr.add(great_bell(note, 7.0, amp, seed=s * 8 + b), at(tr, s * SEC + b), -0.2, 1, 0.55)


def chains(tr, s, k=6, amp=0.25, seed=0):
    g = np.random.default_rng(seed + s * 31)
    for i in range(k):
        tr.add(rattle(g.uniform(0.8, 2.0), amp * g.uniform(0.4, 1.0), 26, seed * 97 + s * 13 + i), at(tr, s * SEC) + g.uniform(0, SEC * 2 - 1),
               g.uniform(-0.9, 0.9), 1, 0.7)


def heartbeat(tr, s, amp=0.4, every=2):
    for b in range(0, SEC, every):
        tr.add(timp('F2', amp, 3.0), at(tr, s * SEC + b), 0, 1, 0.4)
        tr.add(timp('F2', amp * 0.6, 3.5), at(tr, s * SEC + b, 0.6), 0, 1, 0.4)


def drums(tr, s, style, amp=1.0, bars=range(SEC)):
    """half: kick on one, a chain-snare on three. drive: kick-kick, snare two and four, hats. double: sixteenth kicks.
    taiko: the war drums, eighths with accents"""
    for b in bars:
        t = at(tr, s * SEC + b)
        if style == 'half':
            tr.add(kick(0.55 * amp, 6), t, 0, 1, 0.15); tr.add(taiko(0.4 * amp), t, 0, 1, 0.35)
            tr.add(chain_hit(0.35 * amp, s * 8 + b, 5, False), t + 2 * tr.beat, 0.1, 1, 0.4)
            tr.add(snare(0.25 * amp), t + 2 * tr.beat, 0, 1, 0.35)
        elif style == 'drive':
            for bt in (0, 1.5, 2.5): tr.add(kick(0.6 * amp, 7), t + bt * tr.beat, 0, 1, 0.12)
            for bt in (1, 3): tr.add(snare(0.42 * amp), t + bt * tr.beat, 0, 1, 0.3)
            for i in range(8): tr.add(hat(0.12 * amp * (1.3 if i % 2 else 0.8)), t + i * 0.5 * tr.beat, 0.3, 1, 0.15)
            if b % 4 == 3:
                for k, f in enumerate((140, 110, 85, 65)): tr.add(tom(f, 0.4 * amp), t + (3 + k * 0.25) * tr.beat, -0.4 + 0.25 * k, 1, 0.3)
        elif style == 'double':
            for i in range(16): tr.add(kick(0.38 * amp * (1.2 if i % 4 == 0 else 0.85), 12), t + i * 0.25 * tr.beat, 0, 1, 0.08)
            for bt in (1, 3): tr.add(snare(0.5 * amp), t + bt * tr.beat, 0, 1, 0.3)
            for bt in (1, 3): tr.add(chain_hit(0.25 * amp, s * 8 + b + bt, 4, False), t + bt * tr.beat, 0.2, 1, 0.35)
            for i in range(8): tr.add(hat(0.1 * amp, i % 4 == 2), t + i * 0.5 * tr.beat, -0.3, 1, 0.15)
        elif style == 'taiko':
            for i in range(8):
                acc = i in (0, 3, 6)
                tr.add(taiko(0.48 * amp if acc else 0.24 * amp, 46 if acc else 58), t + i * 0.5 * tr.beat, (-0.3, 0.3)[i % 2], 1, 0.35)
            tr.add(snare(0.3 * amp), t + 3 * tr.beat, 0, 1, 0.3)
        if b == bars[0] and style in ('drive', 'double', 'taiko'):
            tr.add(crash(0.45 * amp), t, 0.3, 1, 0.5)


def roll(tr, t_end, dur=2.0, amp=0.4, note='C2'):
    """a timpani roll crescendo into t_end"""
    n = int(dur / 0.07)
    for i in range(n):
        u = (i + 1) / n
        tr.add(timp(note, amp * u ** 1.6, 4.0), t_end - dur + i * 0.07, (-0.2, 0.2)[i % 2], 1, 0.35)


def brink(tr, s, amp=0.4):
    """the last bar of a section that hands on: a riser and a roll into the next downbeat"""
    t = at(tr, s * SEC + SEC)
    tr.add(edge(riser(tr.beat * 4, amp * 0.5)), t - tr.beat * 4, 0, 1, 0.4)
    roll(tr, t, tr.beat * 2, amp * 0.6)


def three(tr, t, amp=0.3, colours=True):
    """the Dread's head, three times - fear (iced), hunger (a theremin under it), war (jaws) - a bar each, then a held note"""
    for k in range(3):
        t0 = t + k * tr.beat * 4
        notes = tp(DREAD_HEAD, -12 + 3 * k)
        ply(tr, t0, notes, lambda x, d: vsolo(x, d, amp, attack=0.015), (-0.3, 0, 0.3)[k], 1, 0.4)
        if not colours: continue
        if k == 0:
            for j, (x, d) in enumerate(notes):
                if x: tr.add(glass(M(x) + 12, 0.6, 0.12), t0 + j * 0.25 * tr.beat, -0.4, 1, 0.5)
        elif k == 1:
            tr.add(theremin(hz(M(notes[0][0]) - 12), tr.beat * 3.5, 0.12, glide_from=hz(M(notes[0][0]) - 17)), t0, 0.4, 1, 0.6)
        else:
            tr.add(timp('F2', 0.5), t0, 0, 1, 0.3); tr.add(chain_hit(0.4, 77 + k), t0 + tr.beat * 2, 0, 1, 0.35)


# ====================================================================== I. THE DESCENT
def t1():
    tr = Track('uc_t1', BPM, LEN['t1'])
    plan = [H_N, H_L, H_N, H_S, H_L, H_N, H_S, H_L]
    for s, prog in enumerate(plan):
        drone_sec(tr, s, ['F1', 'C2', 'F2'] if s % 2 == 0 else ['F1', 'C2', 'Gb2'], 0.22)
        chains(tr, s, 4, 0.16, 1)
        if s in (0, 2, 5, 7): toll(tr, s, (0, 4) if s != 5 else (0,), 'F2', 0.42)
        if s >= 1: heartbeat(tr, s, 0.22 + 0.03 * (s % 3), 2)
        if s in (1, 4, 6, 7): pad(tr, s, prog, 0.06 if s < 6 else 0.08, 'u', 12, 1.2)
        if prog is H_L: bassline(tr, s, prog, 0.2, (0,), 4.0)
    # the solo violin: S low and slow; then an octave up; then with the section
    ply(tr, at(tr, 1 * SEC), S, lambda x, d: vsolo(x, d, 0.28, depth=0.0075), -0.15, 1, 0.5)
    ply(tr, at(tr, 3 * SEC), tp(S, 12), lambda x, d: vsolo(x, d, 0.27), -0.1, 1, 0.5)
    ply(tr, at(tr, 3 * SEC), tp(S, 12), lambda x, d: harmonic(M(x) + 12, d, 0.04), 0.3, 1, 0.7)
    ply(tr, at(tr, 6 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.24), 0.1, 1, 0.5)
    ply(tr, at(tr, 6 * SEC), S, lambda x, d: cello(x, d, 0.18), -0.2, 1, 0.4)
    # its fragments, echoing: the first two bars, answered by a harmonic
    for b in (0, 4):
        ply(tr, at(tr, 4 * SEC + b), S[:3], lambda x, d: vsolo(M(x) + 12, d, 0.22), -0.3, 1, 0.6)
        ply(tr, at(tr, 4 * SEC + b + 2), S[:3], lambda x, d: harmonic(M(x) + 24, d, 0.06), 0.4, 1, 0.7)
    # the ghosts: harmonics hanging in the dark, and something watching
    for s in (0, 2, 5):
        for k, (x, b) in enumerate((('C7', 1), ('F6', 3), ('Gb6', 5), ('E6', 6.5))):
            tr.add(harmonic(x, tr.beat * 6, 0.05), at(tr, s * SEC + b), (-0.6, 0.6)[k % 2], 1, 0.8)
        tr.add(whisper(6.0, 0.05, s), at(tr, s * SEC + 2), 0.5, 1, 0.8)
    tr.add(gaze('C6', 10.0, 0.035), at(tr, 5 * SEC + 1), -0.4, 1, 0.8)
    for k in range(10):
        tr.add(pop(0.12, 60 + 9 * (k % 4)), at(tr, (k * 6) % 64, 1.5 + (k % 3)), (-0.5, 0.5)[k % 2], 1, 0.6)
    return tr


# ====================================================================== II. THE HEXED DARK
def t2():
    tr = Track('uc_t2', BPM, LEN['t2'])
    plan = [H_N, H_S, H_H, H_S, H_N, H_H, H_S, H_L]
    for s, prog in enumerate(plan):
        drone_sec(tr, s, ['F1', 'C2'], 0.16)
        ostinato(tr, s, prog, 0.14 if s in (0, 7) else 0.17)
        if s in (0, 4, 7): toll(tr, s, (0,), 'F2', 0.38)
        if s in (2, 3, 5, 6): pad(tr, s, prog, 0.08, 'o', 12, 0.8)
        if s >= 4 and s != 7: drums(tr, s, 'half', 0.5 + 0.1 * (s - 4))
        chains(tr, s, 2, 0.12, 2)
    ply(tr, at(tr, 1 * SEC), tp(S, 12), lambda x, d: vsolo(x, d, 0.3), -0.1, 1, 0.45)
    ply(tr, at(tr, 2 * SEC), H, lambda x, d: vsolo(M(x) - 12, d, 0.28), 0.05, 1, 0.45)
    ply(tr, at(tr, 3 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.24), 0, 1, 0.45)
    for b in (1, 5):
        ply(tr, at(tr, 3 * SEC + b, 2), tp(dur_x(DREAD_HEAD, 2), -12), lambda x, d: vsolo(x, d, 0.16), 0.45, 1, 0.55)
    ply(tr, at(tr, 5 * SEC), H, lambda x, d: vsec(M(x) - 12, d, 0.24), 0, 1, 0.45)
    ply(tr, at(tr, 5 * SEC), H, lambda x, d: harmonic(x, d, 0.05), 0.4, 1, 0.7)
    ply(tr, at(tr, 6 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.26), -0.1, 1, 0.45)
    ply(tr, at(tr, 6 * SEC), S, lambda x, d: cello(x, d, 0.2), 0.1, 1, 0.4)
    # the hexes: a theremin sliding between the chord's tones, and pings of something cast
    for s in (0, 2, 4, 5):
        for k in range(3):
            a, b = ('C5', 'Gb5', 'E5')[k], ('F5', 'F5', 'F5')[k]
            tr.add(theremin(hz(b), tr.beat * 5, 0.07, glide_from=hz(a)), at(tr, s * SEC + 1 + k * 2.5), (-0.5, 0.5, 0)[k], 1, 0.7)
    for s in (2, 5):
        for k in range(6):
            tr.add(glass(m('F6') + (0, 3, 6, 7, 11, 12)[k], 0.8, 0.05), at(tr, s * SEC + k, 3), (-0.7 + 0.28 * k), 1, 0.7)
    brink(tr, 7, 0.25)
    return tr


# ====================================================================== III. THE DROWNED DEEP
def t3():
    tr = Track('uc_t3', BPM, LEN['t3'])
    plan = [H_N, H_S, H_H, H_L, H_S, H_N, H_H, H_D]
    for s, prog in enumerate(plan):
        if s != 5:
            drive16(tr, s, prog, 0.1 + 0.01 * (s % 3), m('C3'))
            bassline(tr, s, prog, 0.26, (0, 2), 2.0)
            drums(tr, s, 'half', 0.7 if s < 4 else 0.85)
        else:
            drone_sec(tr, s, ['F1', 'C2', 'F2'], 0.22)
            for k in range(8): tr.add(whisper(2.5, 0.05, 30 + k), at(tr, s * SEC + k), (-0.7, 0.7)[k % 2], 1, 0.8)
        organ(tr, s, prog, 0.08 if s in (3, 4, 6) else 0.05, 12, 2)
        if s in (0, 5): toll(tr, s, (0, 4), 'F2', 0.4)
        # the ship's bells, in the deep
        if s in (1, 3, 5, 7):
            for k, x in enumerate(('C6', 'Ab5', 'F5', 'G5')):
                tr.add(bell(x, 2.5, 0.08, 3.5, 1.2, 2.0), at(tr, s * SEC + 6, k * 0.5), 0.5, 1, 0.65)
        chains(tr, s, 2, 0.12, 3)
    ply(tr, at(tr, 1 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.26), -0.1, 1, 0.4)
    ply(tr, at(tr, 1 * SEC), tp(S, 24), lambda x, d: vsolo(x, d, 0.2), 0.15, 1, 0.45)
    eline(tr, at(tr, 2 * SEC), H[:9], 0.12, 0.4, 0.65, fb=0.45, taps=4)          # (the electric violin, far off)
    ply(tr, at(tr, 2 * SEC + 4), H[9:], lambda x, d: vsolo(x, d, 0.24), -0.2, 1, 0.45)
    ply(tr, at(tr, 3 * SEC), tp(S, 12), lambda x, d: vsolo(x, d, 0.22), 0, 1, 0.5)
    pad(tr, 3, H_L, 0.08, 'a', 12, 0.7)
    ply(tr, at(tr, 4 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.28), -0.1, 1, 0.4)
    for b in (1, 3, 5, 7):
        eline(tr, at(tr, 4 * SEC + b, 2), DREAD_HEAD, 0.1, 0.45, 0.6, fb=0.42, taps=4)
    for k, (x, b) in enumerate((('F6', 1), ('E6', 3), ('Gb6', 5))):
        tr.add(harmonic(x, tr.beat * 7, 0.06), at(tr, 5 * SEC + b), (-0.5, 0.5)[k % 2], 1, 0.8)
    eline(tr, at(tr, 5 * SEC + 4), [('C5', 4), ('Db5', 2), ('C5', 2), ('B4', 4), ('C5', 4)], 0.1, -0.3, 0.7, fb=0.45, taps=4)
    ply(tr, at(tr, 6 * SEC), H, lambda x, d: vsec(x, d, 0.26), 0.05, 1, 0.4)
    eline(tr, at(tr, 6 * SEC), tp(H, 12), 0.08, 0.35, 0.6, fb=0.4, taps=3)
    ply(tr, at(tr, 7 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.26), -0.1, 1, 0.4)
    pad(tr, 7, H_D, 0.08, 'a')
    brink(tr, 7, 0.35)
    return tr


# ====================================================================== IV. THE THRONE GATE
def t4():
    tr = Track('uc_t4', BPM, LEN['t4'])
    plan = [H_S, H_H, H_N, H_D, H_S, H_L]
    for s, prog in enumerate(plan):
        bassline(tr, s, prog, 0.3, (0, 1.5, 2.5), 1.4)
        drums(tr, s, 'half' if s == 5 else 'drive', 0.9)
        if s != 2: frantic_sec(tr, s, prog, 0.07 if s in (0, 1) else 0.1, m('F5'))
        else: drive16(tr, s, prog, 0.12, m('C4'))
        organ(tr, s, prog, 0.09 if s == 4 else 0.06, 12, 1 if s == 4 else 2)
        if s in (0, 4): pad(tr, s, prog, 0.09 if s == 4 else 0.06, 'a')
        if s in (2, 5): toll(tr, s, (0, 4), 'F2', 0.45)
    eline(tr, at(tr, 0), tp(S, 12), 0.22, 0, 0.35)
    ply(tr, at(tr, 1 * SEC), H, lambda x, d: vsec(x, d, 0.27), -0.15, 1, 0.4)
    for b in (2, 6):
        eline(tr, at(tr, 1 * SEC + b, 2), [('F5', .5), ('Ab5', .5), ('C6', .5), ('E6', .5)], 0.14, 0.3, 0.4)
    three(tr, at(tr, 2 * SEC), 0.3)                                                    # (the three shards: fear, hunger, war)
    eline(tr, at(tr, 2 * SEC + 4), [('F5', 2), ('E5', 1), ('F5', 1), ('Gb5', 3), ('F5', 1), ('E5', 2), ('C5', 2), ('B4', 2), ('C5', 2)], 0.18, 0, 0.4)
    # the electric violin's solo: climbing runs, a held bend, the scale falling
    sol = mel('F5:.5 G5:.5 Ab5:.5 C6:.5 Db6:2 C6:.5 Ab5:.5 F5:.5 Ab5:.5 C6:2 '
              'Bb5:.5 Ab5:.5 Gb5:.5 F5:.5 Gb5:2 Ab5:.5 Bb5:.5 Db6:.5 F6:.5 E6:2 '
              'F6:.25 E6:.25 Db6:.25 C6:.25 Bb5:.25 Ab5:.25 G5:.25 F5:.25 E5:.5 G5:.5 C6:2 B5:.5 Db6:.5 C6:2 C6:4 r:4')
    assert sum(d for _, d in sol) == 32, sum(d for _, d in sol)
    eline(tr, at(tr, 3 * SEC), sol, 0.22, 0, 0.35, scoop=0.03)
    ply(tr, at(tr, 4 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.24), -0.2, 1, 0.4)
    ply(tr, at(tr, 4 * SEC), S, lambda x, d: chorus([M(x)], d, 0.09, 0.15, 'a'), 0, 1, 0.5)
    eline(tr, at(tr, 4 * SEC), tp(S, 24), 0.2, 0.15, 0.35)
    ply(tr, at(tr, 5 * SEC), tp(S, 12), lambda x, d: vsolo(x, d, 0.26), 0, 1, 0.5)
    brink(tr, 5, 0.4)
    return tr


# ====================================================================== V. A THOUSAND EYES
def t5():
    tr = Track('uc_t5', BPM, LEN['t5'])
    plan = [H_E, H_E, H_N, H_E, H_S, H_E]
    for s, prog in enumerate(plan):
        drone_sec(tr, s, ['F1', 'C2', 'B2'] if s != 4 else ['F1', 'C2'], 0.2)
        for b in range(SEC):                                                  # (the ticking: a clock with no hands)
            for i in range(4):
                tr.add(hat(0.09 if i == 0 else 0.05) + 0, at(tr, s * SEC + b, i), 0.5, 1, 0.2)
                tr.add(clank(0.04, 2600, 0.15, s * 64 + b * 4 + i), at(tr, s * SEC + b, i + 0.5), -0.5, 1, 0.3)
        if s != 4:
            for b, c in enumerate(prog):                                      # (the cellos' tremolo, held under it)
                r = ch(c)[0] + 12
                tr.add(violin(r, tr.beat * 4, 0.12 + 0.02 * s, trem=12, bright=0.6, voices=3), at(tr, s * SEC + b), -0.2, 1, 0.35)
            tr.add(gaze(('C6', 'B5', 'Db6', 'C6', 'C6', 'B5')[s], 14.0, 0.05), at(tr, s * SEC + 1), (-0.5, 0.5)[s % 2], 1, 0.8)
            for k in range(4): tr.add(whisper(3.0, 0.05, 50 + s * 4 + k), at(tr, s * SEC + 2 * k + 1), (-0.7, 0.7)[k % 2], 1, 0.8)
            if s >= 1:
                for b in range(0, SEC, 2): tr.add(tom(52, 0.3 + 0.05 * s), at(tr, s * SEC + b), 0, 1, 0.35)
            if s == 3: heartbeat(tr, s, 0.3, 1)
        else:
            drums(tr, s, 'double', 0.9)
            organ(tr, s, prog, 0.1, 12, 1); pad(tr, s, prog, 0.1, 'a')
            frantic_sec(tr, s, prog, 0.1, m('F5'))
            ply(tr, at(tr, s * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.26), -0.15, 1, 0.4)
            eline(tr, at(tr, s * SEC), tp(S, 24), 0.22, 0.15, 0.35)
            from sovereign_music import eyes
            eyes(tr, at(tr, s * SEC), 3.0, ch(prog[0]), 14, 0.08, 9)
    # the electric violin's wails: long notes leaning on the half-step above
    for s, line in ((0, [('C5', 8), ('Db5', 4), ('C5', 4), ('B4', 8), ('C5', 8)]),
                    (1, [('F5', 6), ('Gb5', 2), ('F5', 8), ('E5', 8), ('F5', 4), ('B4', 4)]),
                    (3, [('Ab5', 4), ('G5', 4), ('Gb5', 4), ('F5', 4), ('E5', 8), ('C5', 4), ('B4', 4)]),
                    (5, [('C5', 8), ('B4', 8), ('C5', 16)])):
        eline(tr, at(tr, s * SEC), line, 0.12 + 0.02 * s, (-0.3, 0.3)[s % 2], 0.55, fb=0.42, taps=4, scoop=0.05)
    three(tr, at(tr, 2 * SEC), 0.26)
    brink(tr, 3, 0.45)
    return tr


# ====================================================================== VI. THE LAST DOOR
def t6():
    tr = Track('uc_t6', BPM, LEN['t6'])
    plan = [H_N, H_S, H_H, H_D, H_M, H_S, H_L, H_D]
    for s, prog in enumerate(plan):
        if s == 4:                                                             # (the light: a single violin, and a breath)
            drone_sec(tr, s, ['F1', 'C2', 'A2'], 0.16)
            pad(tr, s, prog, 0.06, 'a', 24, 1.5)
            ply(tr, at(tr, s * SEC), tp(SM, 12), lambda x, d: vsolo(x, d, 0.3, depth=0.0075), 0, 1, 0.55)
            ply(tr, at(tr, s * SEC), SM, lambda x, d: harmonic(M(x) + 24, d, 0.04), 0.4, 1, 0.8)
            toll(tr, s, (0,), 'F2', 0.35)
            brink(tr, s, 0.5)
            continue
        bassline(tr, s, prog, 0.32, (0, 1.5, 2.5) if s != 0 else (0,), 1.4 if s else 4.0)
        drums(tr, s, ('half', 'double', 'drive', 'double', None, 'double', 'double', 'drive')[s], 1.0)
        organ(tr, s, prog, 0.11 if s in (1, 5) else 0.08, 12, 1)
        pad(tr, s, prog, 0.11 if s in (1, 5) else 0.08, 'a')
        if s not in (0,): frantic_sec(tr, s, prog, 0.09 if s != 5 else 0.11, m('F5'))
        bells = (0, 2, 4, 6) if s in (0, 5) else (0, 4)
        toll(tr, s, bells, 'F2', 0.42)
        if s in (0, 5, 7):
            for b in range(SEC): tr.add(great_bell('C3', 3.5, 0.18, seed=200 + s * 8 + b), at(tr, s * SEC + b, 2), 0.3, 1, 0.5)
    # 0: the threshold - timpani, a wail
    for b in range(0, SEC, 2): roll(tr, at(tr, b + 2), 1.4, 0.35, 'F2')
    eline(tr, at(tr, 0), [('C6', 8), ('Db6', 4), ('C6', 4), ('F6', 8), ('E6', 8)], 0.18, 0, 0.45, scoop=0.05)
    # 1: S - the organ, the choir, the violins in octaves, the electric violin at the top
    ply(tr, at(tr, 1 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.27), -0.25, 1, 0.4)
    ply(tr, at(tr, 1 * SEC), S, lambda x, d: chorus([M(x), M(x) + 12], d, 0.1, 0.12, 'a'), 0, 1, 0.5)
    eline(tr, at(tr, 1 * SEC), tp(S, 24), 0.24, 0.15, 0.35)
    # 2: H - the electric violin, the section an octave under
    eline(tr, at(tr, 2 * SEC), H, 0.24, 0, 0.35)
    ply(tr, at(tr, 2 * SEC), H, lambda x, d: vsec(M(x) - 12, d, 0.24), -0.2, 1, 0.4)
    # 3: the riff, and the three over it
    for b, c in enumerate(H_D):
        r = ch(c)[0] + 12
        for i, on in enumerate((1, 0, 1, 1, 0, 1, 1, 1)):
            if on: chug(tr, at(tr, 3 * SEC + b, i * 0.5), r, tr.beat * 0.42, 0.13)
    three(tr, at(tr, 3 * SEC), 0.3, False)
    eline(tr, at(tr, 3 * SEC + 4), dur_x(DREAD_HEAD, 2) + [('C6', 2)] + dur_x(DREAD_HEAD, 2) + [('F6', 2)] + [('E6', 4), ('C6', 4)], 0.2, 0.1, 0.35)
    # 5: S again - everything
    ply(tr, at(tr, 5 * SEC), tp(S, 12), lambda x, d: vsec(x, d, 0.28), -0.25, 1, 0.4)
    ply(tr, at(tr, 5 * SEC), tp(S, 24), lambda x, d: vsolo(x, d, 0.2), 0.25, 1, 0.4)
    ply(tr, at(tr, 5 * SEC), S, lambda x, d: chorus([M(x), M(x) + 12], d, 0.12, 0.12, 'a'), 0, 1, 0.5)
    eline(tr, at(tr, 5 * SEC), tp(S, 24), 0.26, 0, 0.35)
    for b in range(SEC): tr.add(crash(0.3), at(tr, 5 * SEC + b), (-0.3, 0.3)[b % 2], 1, 0.5)
    # 6: S at double speed, twice - the electric violin and the violins in unison
    for k in (0, 4):
        eline(tr, at(tr, 6 * SEC + k), tp(S2, 24), 0.22, 0, 0.3)
        ply(tr, at(tr, 6 * SEC + k), tp(S2, 12), lambda x, d: vsec(x, d, 0.26), -0.2, 1, 0.4)
    # 7: the end of the road - the riff, a last wail, the brink (and round to the threshold)
    for b, c in enumerate(H_D):
        r = ch(c)[0] + 12
        for i in range(8): chug(tr, at(tr, 7 * SEC + b, i * 0.5), r, tr.beat * 0.4, 0.12)
    eline(tr, at(tr, 7 * SEC), [('F6', 4), ('E6', 4), ('Gb6', 4), ('F6', 4), ('Db6', 4), ('C6', 4), ('B5', 4), ('C6', 4)], 0.22, 0, 0.4, scoop=0.05)
    brink(tr, 7, 0.5)
    return tr


# ====================================================================== THE FIGHTS
def impact(tr, t, amp=1.0):
    tr.add(boom(0.6 * amp), t, 0, 1, 0.4); tr.add(crash(0.5 * amp, 3.0), t, 0.2, 1, 0.5)
    tr.add(taiko(0.6 * amp, 40), t, 0, 1, 0.35); tr.add(chain_hit(0.5 * amp, 5), t, -0.2, 1, 0.4)


def c1():
    tr = Track('uc_c1', BPM, LEN['c1'])
    plan = [H_D, H_S, H_N, H_S]
    for s, prog in enumerate(plan):
        impact(tr, at(tr, s * SEC), 1.0 if s == 0 else 0.6)
        drums(tr, s, 'taiko', 1.0)
        drive16(tr, s, prog, 0.14, m('F4'), 0.2)
        bassline(tr, s, prog, 0.3, (0, 0.5, 1.5, 2, 3), 0.45)
        if s in (1, 3): pad(tr, s, prog, 0.08, 'o')
        for b, c in enumerate(prog):                                           # (brass-like stabs: the low choir and organ)
            if b % 2 == 1: tr.add(great_organ([x + 12 for x in ch(c)], tr.beat * 0.6, 0.12), at(tr, s * SEC + b, 3.5), 0, 1, 0.35)
    for k in (0, 4):
        ply(tr, at(tr, 1 * SEC + k), tp(S2, 12), lambda x, d: vsec(x, d, 0.3), -0.15, 1, 0.35)
    ply(tr, at(tr, 1 * SEC + 4), tp(S2, 24), lambda x, d: vsolo(x, d, 0.2), 0.25, 1, 0.4)
    for b in range(0, SEC, 2): ply(tr, at(tr, 2 * SEC + b), DREAD_HEAD + DREAD_HEAD, lambda x, d: vsolo(x, d, 0.24, attack=0.014), (-0.3, 0.3)[b // 2 % 2], 1, 0.4)
    frantic_sec(tr, 3, H_S, 0.11, m('F5'))
    for k in (0, 4):
        ply(tr, at(tr, 3 * SEC + k), S2, lambda x, d: chorus([M(x) + 12], d, 0.1, 0.08, 'a'), 0, 1, 0.45)
    brink(tr, 3, 0.4)
    return tr


def c2():
    tr = Track('uc_c2', BPM, LEN['c2'])
    plan = [H_D, H_S, H_N, H_D]
    for s, prog in enumerate(plan):
        impact(tr, at(tr, s * SEC), 1.0 if s == 0 else 0.7)
        drums(tr, s, 'double', 1.0)
        bassline(tr, s, prog, 0.3, (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5), 0.4)
        for b, c in enumerate(prog):
            r = ch(c)[0] + 12
            for i, on in enumerate((1, 1, 0, 1, 1, 0, 1, 1)):
                if on: chug(tr, at(tr, s * SEC + b, i * 0.5), r, tr.beat * 0.4, 0.14)
            if b % 2 == 0: tr.add(great_organ([x + 12 for x in ch(c)], tr.beat * 1.8, 0.1), at(tr, s * SEC + b), 0, 1, 0.4)
        if s in (1, 3): pad(tr, s, prog, 0.1, 'a')
    for k in (0, 4):
        ply(tr, at(tr, 0 * SEC + k), tp(S2, 12), lambda x, d: vsec(x, d, 0.28), -0.2, 1, 0.35)
    eline(tr, at(tr, 1 * SEC), tp(S, 24), 0.24, 0.1, 0.3)
    frantic_sec(tr, 1, H_S, 0.09, m('F5'))
    three(tr, at(tr, 2 * SEC), 0.3)
    eline(tr, at(tr, 2 * SEC + 4), mel('C6:.5 Db6:.5 C6:.5 B5:.5 C6:2 F6:.5 E6:.5 Db6:.5 C6:.5 Bb5:2 Ab5:.5 G5:.5 F5:.5 E5:.5 F5:2 B5:.5 C6:.5 Db6:.5 E6:.5 F6:2'), 0.22, 0, 0.3)
    for k in (0, 4):
        eline(tr, at(tr, 3 * SEC + k), tp(S2, 24), 0.22, 0.1, 0.3)
        ply(tr, at(tr, 3 * SEC + k), tp(S2, 12), lambda x, d: vsec(x, d, 0.28), -0.2, 1, 0.35)
    brink(tr, 3, 0.45)
    return tr


# ====================================================================== THE SWELL (the page turn)
def swell():
    tr = Track('uc_swell', BPM, 1)
    d = tr.seconds
    tr.add(suck(d, 0.7), 0, 0.2, 1, 0.2)
    tr.add(edge(riser(d, 0.35)), 0, -0.2, 1, 0.2)
    roll(tr, d - 0.02, d * 0.9, 0.35, 'C2')
    tr.add(edge(violin('C5', d, 0.12, trem=14, voices=3, attack=0.9)), 0, 0, 1, 0.3)
    tr.add(edge(violin('B4', d, 0.1, trem=14, voices=3, attack=0.9)), 0, 0.3, 1, 0.3)
    return tr


def save_swell(tr):
    """played once: no tail may wrap round to its start - rendered dry of the circular reverb's wrap, faded in, cut hard at
    the downbeat (the next track starts there)"""
    st = render(tr, 1.2, 0.11)
    k = int(0.4 * SR); st[:, :k] *= np.linspace(0, 1, k)
    f = int(0.012 * SR); st[:, -f:] *= np.linspace(1, 0, f)
    _guarded(st, os.path.join(VENDOR, 'uc_swell.ogg'), 4)


# (each tier louder than the last; the fights hot)
LEVEL = {'t1': 0.13, 't2': 0.15, 't3': 0.17, 't4': 0.195, 't5': 0.18, 't6': 0.24, 'c1': 0.22, 'c2': 0.24}
ROOM = {'t1': 3.4, 't2': 3.0, 't3': 2.8, 't4': 2.4, 't5': 3.0, 't6': 2.6, 'c1': 2.2, 'c2': 2.2}
BUILD = {'t1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 'c1': c1, 'c2': c2}


def check():
    db = lambda v: 20 * np.log10(max(float(v), 1e-9))
    for nm in list(BUILD) + ['swell']:
        p = os.path.join(VENDOR, f'uc_{nm}.ogg')
        if not os.path.exists(p): continue
        x = _decode(p); n = x.shape[1]
        rms, pk = np.sqrt((x ** 2).mean()), np.abs(x).max()
        seam = np.abs(x[:, 0] - x[:, -1]).max()
        step = np.percentile(np.abs(np.diff(x, axis=1)), 99.9)
        secs = [db(np.sqrt((x[:, i:i + 16 * SR] ** 2).mean())) for i in range(0, n - SR, 16 * SR)]
        print(f'uc_{nm:6s} {n / SR:6.1f} s  RMS {db(rms):6.1f} dBFS  peak {db(pk):5.1f}  seam {seam:.3f} (step {step:.3f})  '
              f'sections ' + ' '.join(f'{v:5.1f}' for v in secs))


def journey(out_dir):
    """a preview of the descent as phase240 plays it: each tier for a while, handed to the next on a section boundary
    under the swell; a fight cutting in on a bar and handing back on its section boundary"""
    from sovereign_music import _encode
    tr = {nm: _decode(os.path.join(VENDOR, f'uc_{nm}.ogg')) for nm in list(BUILD) + ['swell']}
    plan = [('t1', 32), ('t2', 32), ('c1', 32), ('t2', 16), ('t3', 32), ('c2', 32), ('t4', 32), ('t5', 32), ('t6', 48)]
    cuts, segs, pos = [], [], 0
    for i, (nm, sec) in enumerate(plan):
        x = tr[nm][:, :sec * SR].copy()
        segs.append(x); cuts.append((pos, nm)); pos += sec
    y = np.concatenate(segs, axis=1)
    for i, (t, nm) in enumerate(cuts[1:], 1):
        if nm.startswith('c'): continue                                     # (a fight cuts straight in, on its impact)
        a = (t - 2) * SR; y[:, a:a + 2 * SR] += tr['swell'][:, :2 * SR]
    k = int(3 * SR); y[:, -k:] *= np.linspace(1, 0, k)
    y = np.clip(y, -0.98, 0.98)
    os.makedirs(out_dir, exist_ok=True)
    _encode(y, os.path.join(out_dir, 'undercrown_journey.ogg'), 4)
    print('journey:', ' -> '.join(f'{nm}@{t}s' for t, nm in cuts))


if __name__ == '__main__':
    what = sys.argv[1:] or list(BUILD) + ['swell', 'check', 'journey']
    for i, nm in enumerate(BUILD):
        if nm in what:
            tr = seeded(40 + i, BUILD[nm])
            assert tr.seconds == LEN[nm] * 2, (nm, tr.seconds)
            _guarded(render(tr, ROOM[nm], LEVEL[nm]), os.path.join(VENDOR, f'uc_{nm}.ogg'), 3)
    if 'swell' in what: save_swell(seeded(49, swell))
    if 'check' in what: check()
    if 'journey' in what: journey(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'previews', 'v298a_soundtrack'))
