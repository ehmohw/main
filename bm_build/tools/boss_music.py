"""2.80: synthesises the boss themes (vendor/boss_*.ogg) - one loop per kind of fight, and the vault's fanfare.
Built on the heist's synth (tools/gv_music.py): every loop is an exact whole number of seconds and renders circularly, so it
loops without a seam; stereo, so it plays head-locked. Deterministic; run it to rebuild the .ogg files (needs numpy, scipy
and ffmpeg - only to rebuild, never to build the packs).
    python3 tools/boss_music.py [name ...]

    hunt      THE WILD HUNT       the Headless Horseman, the Elder Treant
    sands     SANDS OF THE DEAD   the Sand Pharaoh, the Storm Roc
    abyss     THE ABYSS           the Magma Colossus, the Voidwalker
    dungeon   INTO THE DEPTHS     the dungeon bosses (the Broodmother ... the Lucky Rooster)
    hollow    THE HOLLOW KING     the Hollow King
    hollow2   UNBOUND             the Hollow King, Unbound (his second form)
    serpent   APOPHISS            Apophiss
    serpent2  THE SERPENT RISEN   Apophiss, transformed
    storm     STORMBORN           KillerWatt, Democratus's duel
    tide      THE DROWNED CAPTAIN Captain Tullius
    blood     BLOOD MOON          the Scorching Arachno-Lantern
    vorn      MOTHERSHIP          the Vorn mothership bosses
    omega     KING OF THE DEAD    King Omega (2.82)
    palace    THE OMEGA PALACE    the palace's haunted halls (2.82: a quiet waltz, not a fight)
    vault     (a fanfare, once)   the vault opens"""
import os, sys, subprocess, tempfile, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import (SR, OUT, R, Track, m, hz, fq, mix, T, env, lp, hp, bp, pluck, bell, bass, sub, pad, organ, brass, choir,
                      supersaw, lead, strings, kick, snare, brush, hat, clap, tom, tick, shaker, riser, chord)


# ------------------------------------------------------------------ more instruments
def timp(f, amp=1.0, dec=2.2):
    """a timpani: a pitched drum with a long, slightly sharp-then-settling boom"""
    f = fq(f); t = T(1.8)
    fr = f * (1 + 0.12 * np.exp(-t * 25))
    ph = np.cumsum(fr) / SR
    s = np.sin(2 * np.pi * ph) + 0.4 * np.sin(2 * np.pi * ph * 1.5) * np.exp(-t * 3) + 0.2 * np.sin(2 * np.pi * ph * 1.99) * np.exp(-t * 4)
    s *= np.exp(-t * dec)
    s[:200] += R.noise(200) * np.linspace(0.5, 0, 200)
    return amp * s * env(len(t), 0.002, 0, 1, 0.1)


def crash(amp=1.0, dur=2.5):
    t = T(dur)
    return amp * hp(R.noise(len(t)), 3500) * np.exp(-t * 2.0) * 0.6


def harpsi(f, dur, amp=1.0):
    return amp * pluck(f, dur, 1.0, 0.985)


def reed(f, dur, amp=1.0, vib=6.0, depth=0.012, cut=2600):
    """a nasal reed (a snake charmer's pipe, a shawm)"""
    f = fq(f); t = T(dur)
    fv = f * (1 + depth * np.sin(2 * np.pi * vib * t) * np.clip(t * 4, 0, 1))
    ph = np.cumsum(fv) / SR
    s = bp(2 * (ph % 1) - 1, 700, cut, 1) * 1.5 + 0.3 * np.where(ph % 1 < 0.3, 1.0, -1.0)
    return amp * lp(s, cut) * env(len(t), 0.02, 0.05, 0.85, 0.06)


def theremin(f, dur, amp=1.0, glide_from=None, glide=0.12):
    f1 = fq(f); t = T(dur)
    f0 = fq(glide_from) if glide_from is not None else f1
    fr = f1 + (f0 - f1) * np.exp(-t / glide * 3)
    fr = fr * (1 + 0.018 * np.sin(2 * np.pi * 6.5 * t) * np.clip(t * 2, 0, 1))
    ph = np.cumsum(fr) / SR
    s = np.sin(2 * np.pi * ph) + 0.15 * np.sin(4 * np.pi * ph)
    return amp * s * env(len(t), 0.05, 0, 1, 0.12)


def accordion(notes, dur, amp=1.0):
    t = T(dur); s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in (-0.0035, 0.0035):                    # two reeds a hair apart: the squeezebox's beating
            ph = t * f * (1 + v)
            s += 0.6 * (2 * (ph % 1) - 1) + 0.4 * np.where(ph % 1 < 0.4, 1.0, -1.0)
    s = bp(s / (len(notes) * 2), 300, 3000, 1) * 1.6
    return amp * s * env(len(t), 0.03, 0.05, 0.85, 0.06)


def thunder(amp=1.0, dur=3.5):
    t = T(dur); nz = R.noise(len(t))
    s = lp(nz, 180, 2) * 4 * np.exp(-t * 1.2) * np.clip(t * 8, 0, 1)
    s += lp(nz, 1500) * 0.5 * np.exp(-t * 12)
    return amp * s


def laser(amp=1.0, f0=2400.0, f1=300.0, dur=0.35):
    t = T(dur)
    ph = np.cumsum(f0 * (f1 / f0) ** (t / dur)) / SR
    return amp * np.sin(2 * np.pi * ph) * np.exp(-t * 6)


def hiss(dur, amp=1.0):
    t = T(dur)
    return amp * hp(R.noise(len(t)), 4500) * np.sin(np.pi * t / dur) ** 2 * 0.5


# ------------------------------------------------------------------ melody helpers
def mel(s):
    """'D5:1.5 E5:.5 F5 r:2' -> [(note, beats)]; a bare note is one beat, r a rest"""
    out = []
    for tok in s.split():
        n, _, d = tok.partition(':')
        out.append((None if n == 'r' else n, float(d) if d else 1.0))
    return out


def tp(notes, k):
    return [(None if x is None else (m(x) if isinstance(x, str) else x) + k, d) for x, d in notes]


def bars_of(notes, beats=4):
    n = sum(d for _, d in notes)
    assert abs(n % beats) < 1e-6, (n, notes[:4])
    return int(round(n / beats))


def play(tr, t0, notes, inst, pan=0.0, gain=1.0, wet=0.3, legato=0.95):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(inst(x, d * tr.beat * legato), t, pan, gain, wet)
        t += d * tr.beat
    return t


def drums(tr, bar, kicks=(), snares=(), hats=(), k=0.8, s=0.55, h=0.12):
    for b in kicks: tr.add(kick(k), tr.at(bar, b), 0, 1, 0.05)
    for b in snares: tr.add(snare(s), tr.at(bar, b), 0.1, 1, 0.3)
    for b in hats: tr.add(hat(h), tr.at(bar, b), 0.4, 1, 0.1)


# ------------------------------------------------------------------ the themes
def hunt():
    """THE WILD HUNT - 120 BPM in D minor: galloping strings and toms, a church organ, a tolling bell, a brass call"""
    tr = Track('hunt', 120, 30)
    prog = [('D3', 'm'), ('A#2', 'M'), ('G2', 'm'), ('A2', 'M')]
    A = mel('D5:1.5 E5:.5 F5 A5 A#5:2 A5 G5 G5:1.5 F5:.5 E5 D5 C#5:3 A4')
    B = mel('D5:1.5 E5:.5 F5 A5 D6:2 C6 A#5 A#5:1.5 A5:.5 G5 E5 A5:3 r')
    assert bars_of(A) == bars_of(B) == 4
    for bar in range(30):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 16 <= bar < 20
        for b in range(4):                              # the gallop: da-da-DUM
            for off, acc in ((0, 1.0), (0.5, 0.65), (0.75, 0.65)):
                tr.add(strings(root, tr.beat * 0.22, 0.30 * acc * (0.6 if brk else 1), 1400), tr.at(bar, b + off), -0.25, 1, 0.2)
                tr.add(strings(root + 7, tr.beat * 0.22, 0.20 * acc * (0.6 if brk else 1), 1400), tr.at(bar, b + off), 0.25, 1, 0.2)
        tr.add(organ([x + 12 for x in ch], tr.beat * 4, 0.32), tr.at(bar), 0, 1, 0.55)
        tr.add(sub(root - 12, tr.beat * 3.9, 0.45), tr.at(bar), 0, 1, 0.05)
        if 4 <= bar < 28 and not brk:
            for b in range(4):
                tr.add(tom(70, 0.42, 7, 0.2), tr.at(bar, b), 0, 1, 0.2)
                for off in (0.5, 0.75): tr.add(tom(96, 0.26, 9, 0.2), tr.at(bar, b + off), 0.15, 1, 0.2)
            drums(tr, bar, snares=(1, 3), s=0.35)
            if bar >= 8: tr.add(crash(0.25) if bar % 8 == 0 else hat(0.2, True), tr.at(bar), 0.3, 1, 0.3)
        if brk:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.5, 0.5), tr.at(bar), 0, 1, 0.6)
            tr.add(timp(root - 12, 0.6), tr.at(bar), 0, 1, 0.4); tr.add(timp(root - 12, 0.4), tr.at(bar, 2), 0, 1, 0.4)
        if bar % 4 == 0 and (bar < 4 or brk):
            tr.add(bell('D4', 4.0, 0.32, 2.76, 0.9, 2.0), tr.at(bar), -0.1, 1, 0.6)
        if bar in (7, 15, 27, 29): tr.add(riser(tr.beat * 4, 0.22), tr.at(bar), 0, 1, 0.3)
    for ph in (8, 20):
        for half, mo in ((0, A), (4, B)):
            play(tr, tr.at(ph + half), mo, lambda x, d: brass([x], d, 0.42, 2800, 0.05), 0.1, 1, 0.4)
            if ph == 20:
                play(tr, tr.at(ph + half), tp(mo, -12), lambda x, d: brass([x], d, 0.3, 2000, 0.05), -0.2, 1, 0.4)
                play(tr, tr.at(ph + half), mo, lambda x, d: choir([x], d + 0.2, 0.28, 0.15), 0, 1, 0.5)
    return tr


def sands():
    """SANDS OF THE DEAD - 100 BPM in E hijaz: a drone, an oud, a darbuka's maqsum, a pipe over the dunes"""
    tr = Track('sands', 100, 25)
    oud = [mel('E3:.5 F3:.5 G#3:.5 A3:.5 G#3:.5 F3:.5 E3:.5 r:.5'), mel('B3:.5 C4:.5 B3:.5 A3:.5 G#3:.5 A3:.5 G#3:.5 F3:.5')]
    M = mel('E5:.5 F5:.5 G#5 A5 B5:.5 A5:.5 G#5:.5 A5:.5 G#5:.5 F5:.5 E5:2 '
            'B5:.5 C6:.5 D6 C6:.5 B5:.5 A5 G#5:.5 A5:.5 F5:.5 G#5:.5 E5:2 '
            'E6:1.5 D6:.5 C6 B5 C6:.5 B5:.5 A5:.5 G#5:.5 A5:2 '
            'G#5:.5 A5:.5 B5:.5 A5:.5 G#5 F5 E5:3 r')
    assert bars_of(M) == 8
    for bar in range(25):
        brk = 13 <= bar < 17
        tr.add(pad(['E2', 'B2', 'E3'], tr.beat * 4 + 0.5, 0.24, 900, 0.8, 0.8), tr.at(bar), 0, 1, 0.45)
        tr.add(sub('E2', tr.beat * 3.9, 0.4), tr.at(bar), 0, 1, 0.05)
        if not brk:
            play(tr, tr.at(bar), oud[(bar // 2) % 2], lambda x, d: pluck(x, d * 1.6, 0.55, 0.992) * 0.5, -0.3, 1, 0.3)
        if 5 <= bar < 25 and not brk:                   # maqsum: DUM tek . tek DUM . tek .
            for b in (0, 2): tr.add(tom(150, 0.55, 10, 0.15), tr.at(bar, b), 0, 1, 0.2)
            for b in (0.5, 1.5, 3): tr.add(mix(tick(0.3, 2600), brush(0.35)), tr.at(bar, b), 0.25, 1, 0.25)
            for b in range(16): tr.add(shaker(0.08 + 0.05 * (b % 2 == 0)), tr.at(bar, b / 4), 0.5, 1, 0.1)
        if brk:
            tr.add(choir(['E3', 'B3', 'E4'], tr.beat * 4, 0.45, 0.6), tr.at(bar), 0, 1, 0.6)
            tr.add(tom(110, 0.4, 5, 0.3), tr.at(bar), 0, 1, 0.4); tr.add(tom(110, 0.3, 5, 0.3), tr.at(bar, 2.5), 0, 1, 0.4)
            tr.add(hiss(tr.beat * 4, 0.25), tr.at(bar), (bar % 2) * 0.6 - 0.3, 1, 0.5)
        if bar in (4, 16): tr.add(riser(tr.beat * 4, 0.2), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(5), M, lambda x, d: reed(x, d, 0.38), 0.15, 1, 0.4)
    play(tr, tr.at(17), M, lambda x, d: reed(x, d, 0.36, cut=3200), 0.15, 1, 0.4)
    play(tr, tr.at(17), tp(M, -12), lambda x, d: brass([x], d, 0.3, 2200, 0.04), -0.2, 1, 0.4)
    return tr


def abyss():
    """THE ABYSS - 80 BPM in C phrygian: a chugging low brass, timpani, a choir in clusters, cold metal bells"""
    tr = Track('abyss', 80, 20)
    prog = [('C3', 'm'), ('C#3', 'M'), ('C3', 'm'), ('G2', 'M')]
    M = mel('C5:1.5 D5:.5 D#5:2 F5 D#5 C#5:2 C5:1.5 D5:.5 D#5 G5 G5:3 r '
            'C6:2 A#5 G#5 G#5:1.5 F5:.5 C#5:2 D#5 D5 C5 B4 B4:3 r')
    assert bars_of(M) == 8
    for bar in range(20):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = bar >= 16
        tr.add(sub(root - 12, tr.beat * 3.95, 0.55), tr.at(bar), 0, 1, 0.05)
        if not brk:
            for b in (0, 0.75, 1.5, 2.5, 3):            # the chug
                tr.add(brass([root - 12, root - 5], tr.beat * 0.4, 0.42, 900, 0.01), tr.at(bar, b), 0, 1, 0.25)
            tr.add(timp(root - 12, 0.7), tr.at(bar), 0, 1, 0.35); tr.add(timp(root - 12, 0.5), tr.at(bar, 2.5), 0, 1, 0.35)
        if bar >= 4 and not brk:
            drums(tr, bar, kicks=(0, 0.75, 2.5), snares=(2,), k=0.85, s=0.6)
            tr.add(choir([root + 12, root + 13, root + 18], tr.beat * 4, 0.3, 0.8), tr.at(bar), 0, 1, 0.6)
        if bar >= 8:
            for b in range(0, 4, 2):
                x = ch[(bar + b) % 3] + 36
                tr.add(bell(hz(x), 2.0, 0.12, 2.76, 1.4, 2.5), tr.at(bar, b + 1), (-0.6 if b else 0.6), 1, 0.6)
        if brk:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.5, 0.9), tr.at(bar), 0, 1, 0.7)
            tr.add(timp(root - 12, 0.5), tr.at(bar), 0, 1, 0.5)
            if bar == 19: tr.add(riser(tr.beat * 4, 0.3), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(8), M, lambda x, d: brass([x], d, 0.45, 2600, 0.06), 0.1, 1, 0.45)
    play(tr, tr.at(8), tp(M, -12), lambda x, d: brass([x], d, 0.3, 1600, 0.06), -0.15, 1, 0.45)
    return tr


def dungeon():
    """INTO THE DEPTHS - 140 BPM in C minor: a racing string ostinato, a rock beat, a brass theme, then the choir"""
    tr = Track('dungeon', 140, 35)
    prog = [('C3', 'm'), ('G#2', 'M'), ('A#2', 'M'), ('G2', 'M')]
    A = mel('G4 C5 D5:.5 D#5:.5 D5:.5 C5:.5 G#4 C5 D#5 D5:.5 C5:.5 A#4 D5 F5 D#5:.5 D5:.5 B4:2 D5 G5 '
            'C6:1.5 G5:.5 D#5 C5 C6:1.5 G#5:.5 D#5 C5 D6:1.5 A#5:.5 F5 D5 D6:2 B5:2')
    Bm = mel('G5:2 D#5:2 G#5:2 C6:2 A#5:2 F5:2 G5:4 D#6:2 D6:2 C6:2 G#5:2 A#5:2 D6:2 B5:4')
    assert bars_of(A) == bars_of(Bm) == 8
    for bar in range(35):
        ch = chord(*prog[(bar - 3) % 4]) if bar >= 3 else chord('C3', 'm')
        root = ch[0]
        brk = 19 <= bar < 27
        pat = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24]
        for i, x in enumerate(pat):
            tr.add(strings(x, tr.beat * 0.42, 0.22 if not brk else 0.14, 2200), tr.at(bar, i / 2), (-0.35 if i % 2 else 0.35), 1, 0.25)
        if not brk:
            for i in range(8): tr.add(bass(root - 12 + (12 if i % 2 else 0), tr.beat * 0.45, 0.6, 800, 5), tr.at(bar, i / 2), 0, 1, 0.05)
        if 3 <= bar and not brk:
            drums(tr, bar, kicks=(0, 1.5, 2.5), snares=(1, 3), hats=[i / 2 for i in range(8)])
            if (bar - 3) % 8 == 0: tr.add(crash(0.3), tr.at(bar), 0.3, 1, 0.3)
        if brk:
            tr.add(pad([x + 12 for x in ch], tr.beat * 4 + 0.3, 0.25, 1600), tr.at(bar), 0, 1, 0.5)
            for b in (0, 0.75, 1.5, 3): tr.add(tom(90 - 15 * (b == 3), 0.5, 6, 0.3), tr.at(bar, b), 0, 1, 0.3)
            arp = [ch[0] + 24, ch[2] + 24, ch[1] + 36, ch[2] + 24]
            for i in range(16): tr.add(lead(hz(arp[i % 4]), tr.beat * 0.22, 0.12, 2000, 0, 0.3), tr.at(bar, i / 4), 0.35, 1, 0.35)
        if 11 <= bar < 19:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.3, 0.4), tr.at(bar), 0, 1, 0.55)
        if bar in (2, 18, 26, 34): tr.add(riser(tr.beat * 4, 0.25), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(3), A, lambda x, d: brass([x], d, 0.44, 2800, 0.04), 0.1, 1, 0.4)
    play(tr, tr.at(11), Bm, lambda x, d: choir([x], d + 0.2, 0.4, 0.2), 0, 1, 0.5)
    play(tr, tr.at(11), tp(Bm, -12), lambda x, d: brass([x], d, 0.3, 2200, 0.08), -0.2, 1, 0.4)
    play(tr, tr.at(19), tp(Bm, 0), lambda x, d: lead(x, d, 0.18, 1800), 0.2, 1, 0.45)
    play(tr, tr.at(27), A, lambda x, d: brass([x], d, 0.44, 3000, 0.04), 0.1, 1, 0.4)
    play(tr, tr.at(27), tp(A, 12), lambda x, d: lead(x, d, 0.14, 2600), 0.3, 1, 0.4)
    return tr


HOLLOW = mel('F#5:1.5 E5:.5 D5 C#5 B4:2 D5 E5 G5:1.5 F#5:.5 E5 D5 C#5:3 A#4 '
             'F#5:1.5 G5:.5 A5 F#5 G5:2 B5 A5 G5 F#5 E5 G5 F#5:4')


def hollow():
    """THE HOLLOW KING - 90 BPM in B minor: a cathedral organ, a harpsichord, timpani, a choir crowning his theme"""
    tr = Track('hollow', 90, 24)
    prog = [('B2', 'm'), ('G2', 'M'), ('E3', 'm'), ('F#2', 'M')]
    assert bars_of(HOLLOW) == 8
    for bar in range(24):
        ch = chord(*prog[bar % 4]); root = ch[0]
        tr.add(organ([root] + [x + 12 for x in ch], tr.beat * 4, 0.36), tr.at(bar), 0, 1, 0.65)
        tr.add(sub(root - 12, tr.beat * 3.9, 0.4), tr.at(bar), 0, 1, 0.05)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 12, ch[1] + 12]
        for i, x in enumerate(arp): tr.add(harpsi(hz(x + 12), 0.6, 0.32), tr.at(bar, i / 2), (-0.4 if i % 2 else 0.4), 1, 0.35)
        if bar >= 4:
            tr.add(timp(root - 12, 0.65), tr.at(bar), 0, 1, 0.45); tr.add(timp(root - 12, 0.45), tr.at(bar, 2), 0, 1, 0.45)
            tr.add(brush(0.35), tr.at(bar, 3.5), 0.2, 1, 0.4)
        if bar >= 20:
            for b in range(4): tr.add(timp(root - 5, 0.35), tr.at(bar, b + 0.5), 0, 1, 0.45)
        if bar in (7, 15, 23): tr.add(riser(tr.beat * 4, 0.2), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(8), HOLLOW, lambda x, d: choir([x], d + 0.2, 0.45, 0.25), 0, 1, 0.55)
    play(tr, tr.at(8), tp(HOLLOW, -12), lambda x, d: brass([x], d, 0.28, 1800, 0.08), -0.2, 1, 0.45)
    play(tr, tr.at(16), tp(HOLLOW, 12), lambda x, d: brass([x], d, 0.34, 3000, 0.05), 0.15, 1, 0.45)
    play(tr, tr.at(16), HOLLOW, lambda x, d: choir([x], d + 0.2, 0.4, 0.2), 0, 1, 0.55)
    for bar in range(16, 24, 2): tr.add(bell('B5', 3.0, 0.15, 3.01, 1.2, 2.0), tr.at(bar), 0.4, 1, 0.6)
    return tr


def hollow2():
    """UNBOUND - 160 BPM in B minor: his theme again, unchained: four on the floor, organ stabs, saws, the full choir"""
    tr = Track('hollow2', 160, 40)
    prog = [('B2', 'm'), ('G2', 'M'), ('E3', 'm'), ('F#2', 'M')]
    pump = lambda n: np.clip((np.arange(n) / SR) / (tr.beat * 0.45), 0.3, 1.0) ** 1.4
    for bar in range(40):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 16 <= bar < 24
        if not brk:
            drums(tr, bar, kicks=range(4), snares=(1, 3), hats=[i / 2 for i in range(8)], k=0.9, s=0.6, h=0.13)
            for i in range(8): tr.add(bass(root - 12 + (12 if i % 2 else 0), tr.beat * 0.45, 0.65, 900, 5), tr.at(bar, i / 2), 0, 1, 0.05)
            for b in (0, 1.5, 3): tr.add(organ([x + 12 for x in ch], tr.beat * 0.45, 0.42), tr.at(bar, b), -0.2, 1, 0.4)
            for b in range(4):
                s = supersaw([x + 12 for x in ch], tr.beat * 0.95, 0.26, 2600)
                tr.add(s * pump(len(s)), tr.at(bar, b), 0.15, 1, 0.35)
            if bar % 8 == 0: tr.add(crash(0.32), tr.at(bar), 0.3, 1, 0.3)
        else:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.5, 0.4), tr.at(bar), 0, 1, 0.6)
            tr.add(organ([root] + [x + 12 for x in ch], tr.beat * 4, 0.3), tr.at(bar), 0, 1, 0.6)
            for b in (0, 2): tr.add(timp(root - 12, 0.65), tr.at(bar, b), 0, 1, 0.4)
            if bar >= 20:
                for b in range(8): tr.add(snare(0.12 + 0.05 * (bar - 20) + 0.01 * b), tr.at(bar, b / 2), 0.1, 1, 0.3)
        if bar >= 24:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.32, 0.3), tr.at(bar), 0, 1, 0.55)
        if bar in (15, 23, 39): tr.add(riser(tr.beat * 4, 0.3), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(8), HOLLOW, lambda x, d: brass([x], d, 0.42, 3000, 0.03), 0.1, 1, 0.4)
    play(tr, tr.at(16), tp(HOLLOW, 12), lambda x, d: lead(x, d, 0.2, 2400), 0.2, 1, 0.45)
    play(tr, tr.at(24), HOLLOW, lambda x, d: brass([x], d, 0.42, 3200, 0.03), 0.1, 1, 0.4)
    play(tr, tr.at(32), tp(HOLLOW, 12), lambda x, d: brass([x], d, 0.36, 3400, 0.03), 0.15, 1, 0.4)
    play(tr, tr.at(32), HOLLOW, lambda x, d: choir([x], d + 0.15, 0.36, 0.1), 0, 1, 0.5)
    return tr


SERPENT = mel('D5:.5 D#5:.5 F#5:.5 G5:.5 A5 G5:.5 F#5:.5 D#5:.5 F#5:.5 D#5:.5 D5:.5 D5:2 '
              'A5:.5 A#5:.5 C#6:.5 D6:.5 C#6:.5 A#5:.5 A5 G5:.5 F#5:.5 D#5:.5 F#5:.5 D5:2 '
              'D6:1.5 C#6:.5 A#5 A5 A#5:.5 A5:.5 G5:.5 F#5:.5 G5:2 '
              'F#5:.5 G5:.5 A5:.5 G5:.5 F#5 D#5 D5:3 r')


def serpent():
    """APOPHISS - 105 BPM in D double harmonic: a drone, hand drums, a snake charmer's pipe, a hissing dark choir"""
    tr = Track('serpent', 105, 28)
    assert bars_of(SERPENT) == 8
    for bar in range(28):
        brk = 12 <= bar < 16
        tr.add(pad(['D2', 'A2', 'D3'], tr.beat * 4 + 0.5, 0.26, 800, 0.8, 0.8), tr.at(bar), 0, 1, 0.45)
        tr.add(sub('D2', tr.beat * 3.9, 0.45), tr.at(bar), 0, 1, 0.05)
        if bar % 2 == 0: tr.add(brass(['D2', 'A2'], tr.beat * 1.5, 0.4, 700, 0.05), tr.at(bar), 0, 1, 0.3)
        if 4 <= bar < 24 and not brk:
            for b in (0, 1.5): tr.add(tom(160, 0.55, 10, 0.15), tr.at(bar, b), 0, 1, 0.2)
            for b in (1, 2.5, 3, 3.5): tr.add(mix(tick(0.28, 2800), brush(0.3)), tr.at(bar, b), 0.3, 1, 0.25)
            for b in range(8): tr.add(shaker(0.1), tr.at(bar, b / 2 + 0.25), -0.4, 1, 0.1)
        if brk:
            tr.add(choir(['D4', 'D#4', 'A4'], tr.beat * 4, 0.45, 0.9), tr.at(bar), 0, 1, 0.7)
            tr.add(hiss(tr.beat * 2, 0.35), tr.at(bar, 1), (bar % 2) * 1.2 - 0.6, 1, 0.5)
            tr.add(timp('D2', 0.6), tr.at(bar), 0, 1, 0.5)
        if bar >= 16 and bar < 24:
            tr.add(choir(['D3', 'A3', 'D#4'], tr.beat * 4, 0.28, 0.6), tr.at(bar), 0, 1, 0.6)
        if bar >= 24:
            for b in (0, 2): tr.add(bell(hz(m('D6') + (1 if b else 0)), 2.0, 0.14, 2.76, 1.4, 2.5), tr.at(bar, b), 0.3, 1, 0.6)
        if bar in (3, 15, 27): tr.add(riser(tr.beat * 4, 0.2), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(4), SERPENT, lambda x, d: reed(x, d, 0.4, 5.5, 0.015), 0.1, 1, 0.4)
    play(tr, tr.at(16), SERPENT, lambda x, d: reed(x, d, 0.36, 5.5, 0.015, 3200), 0.1, 1, 0.4)
    play(tr, tr.at(16), tp(SERPENT, -12), lambda x, d: brass([x], d, 0.28, 1800, 0.05), -0.25, 1, 0.45)
    return tr


def serpent2():
    """THE SERPENT RISEN - 150 BPM in D double harmonic: his pipe tune as a brass anthem, sixteenth-note strings, the choir"""
    tr = Track('serpent2', 150, 40)
    prog = [('D3', 'M'), ('D#3', 'M'), ('G2', 'm'), ('A2', 'M')]
    for bar in range(40):
        ch = chord(*prog[(bar // 2) % 4]); root = ch[0]
        brk = 16 <= bar < 24
        osti = [root + 12, root + 13, root + 12, root + 11]
        for i in range(16):
            tr.add(strings(osti[i % 4], tr.beat * 0.22, 0.17 if not brk else 0.1, 2400), tr.at(bar, i / 4), (-0.3 if i % 2 else 0.3), 1, 0.25)
        tr.add(sub(root - 12, tr.beat * 3.9, 0.45), tr.at(bar), 0, 1, 0.05)
        if not brk:
            drums(tr, bar, kicks=(0, 0.75, 2, 2.75), snares=(1, 3), hats=[i / 2 for i in range(8)], k=0.9, s=0.6)
            for b in (0, 1.5, 3): tr.add(tom(80, 0.3, 6, 0.3), tr.at(bar, b + 0.5), -0.2, 1, 0.3)
            if bar % 8 == 0: tr.add(crash(0.32), tr.at(bar), 0.3, 1, 0.3)
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.3, 0.3), tr.at(bar), 0, 1, 0.6)
        else:
            tr.add(choir(['D4', 'D#4', 'A4'], tr.beat * 4, 0.42, 0.6), tr.at(bar), 0, 1, 0.7)
            tr.add(timp(root - 12, 0.6), tr.at(bar), 0, 1, 0.5)
            tr.add(hiss(tr.beat * 2, 0.3), tr.at(bar, 2), (bar % 2) * 1.2 - 0.6, 1, 0.5)
        if bar in (15, 23, 39): tr.add(riser(tr.beat * 4, 0.3), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(8), SERPENT, lambda x, d: brass([x], d, 0.44, 3000, 0.03), 0.1, 1, 0.4)
    play(tr, tr.at(16), SERPENT, lambda x, d: reed(x, d, 0.32, 5.5, 0.015), 0.15, 1, 0.45)
    play(tr, tr.at(24), SERPENT, lambda x, d: brass([x], d, 0.44, 3200, 0.03), 0.1, 1, 0.4)
    play(tr, tr.at(24), tp(SERPENT, -12), lambda x, d: brass([x], d, 0.32, 2000, 0.03), -0.2, 1, 0.4)
    play(tr, tr.at(32), SERPENT, lambda x, d: choir([x], d + 0.15, 0.4, 0.1), 0, 1, 0.5)
    play(tr, tr.at(32), tp(SERPENT, 12), lambda x, d: lead(x, d, 0.16, 2600), 0.3, 1, 0.4)
    return tr


def storm():
    """STORMBORN - 144 BPM in E minor: a crackling sixteenth bass, square arps, brass stabs, thunder"""
    tr = Track('storm', 144, 36)
    prog = [('E3', 'm'), ('C3', 'M'), ('D3', 'M'), ('B2', 'M')]
    M = mel('E5 G5 B5:1.5 A5:.5 G5 E5 C5:2 D5 F#5 A5:1.5 G5:.5 F#5:3 D#5 '
            'E5 G5 B5 E6 D6:1.5 C6:.5 B5 G5 A5:1.5 B5:.5 C6 A5 B5:4')
    assert bars_of(M) == 8
    for bar in range(36):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 20 <= bar < 24
        for i in range(16):                             # the crackle: a sixteenth-note bass
            tr.add(lead(hz(root - 12 + (12 if i % 4 == 2 else 0)), tr.beat * 0.2, 0.3 if not brk else 0.15, 700, 0, 0.5), tr.at(bar, i / 4), 0, 1, 0.05)
        if bar >= 4:
            arp = [ch[0] + 24, ch[1] + 24, ch[2] + 24, ch[0] + 36, ch[2] + 24, ch[1] + 24]
            for i in range(16):
                tr.add(lead(hz(arp[i % 6]), tr.beat * 0.2, 0.1, 1400 if brk else 3000, 0, 0.5), tr.at(bar, i / 4), (0.5 if i % 2 else -0.5), 1, 0.35)
        if 4 <= bar and not brk:
            drums(tr, bar, kicks=(0, 1.75, 2.5), snares=(1, 3), hats=[i / 4 for i in range(16)], h=0.08)
        if bar >= 8 and not brk:
            for b in (0, 1.5): tr.add(brass([x + 12 for x in ch], 0.3, 0.4, 2800, 0.01), tr.at(bar, b), -0.2, 1, 0.3)
        if brk:
            tr.add(pad([x + 12 for x in ch], tr.beat * 4 + 0.3, 0.3, 1200), tr.at(bar), 0, 1, 0.55)
            for b in range(4 * (bar - 19)): tr.add(snare(0.1 + 0.04 * (bar - 20)), tr.at(bar, b / (bar - 19)), 0.1, 1, 0.3)
        if bar % 8 == 0 or bar == 22: tr.add(thunder(0.6), tr.at(bar), (bar % 3 - 1) * 0.4, 1, 0.4)
        if bar in (7, 19, 23, 35): tr.add(riser(tr.beat * 4, 0.25), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(12), M, lambda x, d: lead(x, d, 0.3, 2600, 5.5, 0.4), 0.15, 1, 0.4)
    play(tr, tr.at(24), M, lambda x, d: brass([x], d, 0.4, 3000, 0.03), 0.1, 1, 0.4)
    play(tr, tr.at(24), tp(M, 12), lambda x, d: lead(x, d, 0.16, 3200, 5.5, 0.4), 0.3, 1, 0.4)
    return tr


def tide():
    """THE DROWNED CAPTAIN - a 6/8 shanty in A minor: oom-pah squeezebox, a ship's bell, a choir of the drowned"""
    tr = Track('tide', 180, 30, 6)
    prog = [('A2', 'm'), ('G2', 'M'), ('A2', 'm'), ('E2', 'M'), ('A2', 'm'), ('G2', 'M'), ('FE', None), ('A2', 'm')]
    M = mel('A4:2 C5 E5:2 D5 D5:2 B4 G4:3 A4:2 C5 E5:2 A5 G#5:3 E5:3 '
            'A5:2 G5 E5:2 C5 D5:2 E5 D5:2 B4 C5:2 A4 B4:2 G#4 A4:6')
    assert bars_of(M, 6) == 8
    for bar in range(30):
        root, kind = prog[bar % 8]
        halves = [chord('F2', 'M'), chord('E2', 'M')] if kind is None else [chord(root, kind)] * 2
        brk = 14 <= bar < 18
        for h, ch in enumerate(halves):                  # oom-pah-pah, twice a bar
            tr.add(mix(pluck(hz(ch[0] - 12 + 7 * h * (kind is not None)), tr.beat * 2.5, 0.35, 0.993) * 0.8,
                       bass(ch[0] - 12 + 7 * h * (kind is not None), tr.beat * 2, 0.45, 600, 3)), tr.at(bar, 3 * h), 0, 1, 0.1)
            if not brk:
                for b in (1, 2): tr.add(accordion([x + 12 for x in ch], tr.beat * 0.8, 0.22), tr.at(bar, 3 * h + b), -0.3, 1, 0.35)
        if 6 <= bar < 26 and not brk:
            for b in (0, 3): tr.add(kick(0.55, 10), tr.at(bar, b), 0, 1, 0.1)
            for b in (1.5, 4.5): tr.add(brush(0.3), tr.at(bar, b), 0.3, 1, 0.3)
            tr.add(tom(110, 0.25, 7, 0.4), tr.at(bar, 5), 0.2, 1, 0.3)
        if bar % 4 == 0: tr.add(bell('A5', 3.0, 0.22, 2.0, 1.0, 2.5), tr.at(bar), 0.5, 1, 0.6)
        if brk:
            ch = halves[0]
            tr.add(choir([x + 12 for x in ch], tr.beat * 6, 0.5, 0.7), tr.at(bar), 0, 1, 0.7)
            tr.add(pad([ch[0] - 12, ch[0]], tr.beat * 6, 0.25, 500), tr.at(bar), 0, 1, 0.5)
        if 18 <= bar < 26:
            tr.add(choir([x + 12 for x in halves[0]], tr.beat * 3, 0.24, 0.4), tr.at(bar), 0, 1, 0.6)
            tr.add(choir([x + 12 for x in halves[1]], tr.beat * 3, 0.24, 0.4), tr.at(bar, 3), 0, 1, 0.6)
    play(tr, tr.at(6), M, lambda x, d: accordion([x], d, 0.36), 0.15, 1, 0.4)
    play(tr, tr.at(18), M, lambda x, d: accordion([x], d, 0.34), 0.15, 1, 0.4)
    play(tr, tr.at(18), M, lambda x, d: choir([x], d + 0.1, 0.26, 0.1), -0.1, 1, 0.5)
    return tr


def blood():
    """BLOOD MOON - 128 BPM in F# minor: a creeping chromatic harpsichord, a music box, a pipe organ, pounding drums"""
    tr = Track('blood', 128, 32)
    prog = [('F#2', 'm'), ('D2', 'M'), ('B2', 'm'), ('C#3', 'M')]
    box = mel('C#6:2 F#6:2 F6:2 E6:2 D6:2 C#6:2 B5:2 A5:2')
    M = mel('F#5:1.5 G#5:.5 A5 C#6 D6:2 C#6 A5 B5:1.5 A5:.5 F#5 D5 F5:3 r '
            'F#5 A5 C#6 F#6 F#6:2 E6 D6 D6 C#6 B5 F#5 G#5:2 F5:2')
    assert bars_of(M) == 8 and bars_of(box) == 4
    for bar in range(32):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 12 <= bar < 16
        fig = [ch[0] + 24, ch[0] + 23, ch[0] + 24, ch[2] + 12, ch[1] + 24, ch[1] + 23, ch[1] + 24, ch[2] + 12]
        for i, x in enumerate(fig): tr.add(harpsi(hz(x), 0.5, 0.3 if not brk else 0.2), tr.at(bar, i / 2), (-0.4 if i % 2 else 0.4), 1, 0.35)
        tr.add(organ([root + 12] + [x + 24 for x in ch], tr.beat * 4, 0.28 if not brk else 0.36), tr.at(bar), 0, 1, 0.6)
        tr.add(sub(root, tr.beat * 3.9, 0.45), tr.at(bar), 0, 1, 0.05)
        if 8 <= bar and not brk:
            drums(tr, bar, kicks=(0, 2.5), snares=(1, 3), hats=[i / 2 for i in range(8)], k=0.9, s=0.6, h=0.1)
            tr.add(tom(75, 0.4, 6, 0.3), tr.at(bar, 3.5), 0, 1, 0.3)
            if bar % 8 == 0: tr.add(crash(0.3), tr.at(bar), 0.3, 1, 0.3)
        if 16 <= bar < 24 or brk:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.36, 0.5), tr.at(bar), 0, 1, 0.65)
        if bar in (7, 15, 31): tr.add(riser(tr.beat * 4, 0.25), tr.at(bar), 0, 1, 0.3)
    for ph in (4, 12): play(tr, tr.at(ph), box, lambda x, d: bell(x, 2.2, 0.2, 3.01, 1.3, 1.6), 0.3, 1, 0.55)
    play(tr, tr.at(16), M, lambda x, d: brass([x], d, 0.42, 2800, 0.05), 0.1, 1, 0.4)
    play(tr, tr.at(24), M, lambda x, d: lead(x, d, 0.26, 2200, 5.5, 0.35), 0.15, 1, 0.4)
    play(tr, tr.at(24), tp(M, -12), lambda x, d: brass([x], d, 0.3, 2000, 0.05), -0.2, 1, 0.4)
    return tr


def vorn():
    """MOTHERSHIP - 120 BPM, chords from elsewhere: a theremin, a square-wave arpeggiator, a pulsing bass, lasers"""
    tr = Track('vorn', 120, 30)
    prog = [('C3', 'm'), ('G#2', 'm'), ('E3', 'm'), ('A#2', 'M')]
    M = mel('G5:2 D#5 C5 D#5:2 B4 G#4 G5 B5 E6:2 D6:3 r C6:2 G5:2 B5:1.5 G#5:.5 D#5:2 E5 G5 B5 D6 A#5:4')
    assert bars_of(M) == 8
    for bar in range(30):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 16 <= bar < 20
        tr.add(pad([x + 12 for x in ch], tr.beat * 4 + 0.4, 0.26, 900 + 60 * min(bar, 16), 0.5, 0.6, 4, 0.01), tr.at(bar), 0, 1, 0.5)
        arp = [ch[0] + 24, ch[1] + 24, ch[2] + 24, ch[1] + 36]
        for i in range(16):
            tr.add(lead(hz(arp[i % 4]), tr.beat * 0.2, 0.12, 1000 + 120 * min(bar, 16), 0, 0.5), tr.at(bar, i / 4), (0.45 if i % 2 else -0.45), 1, 0.35)
        if not brk:
            for i in range(8): tr.add(bass(root - 12, tr.beat * 0.4, 0.6, 700, 6), tr.at(bar, i / 2), 0, 1, 0.05)
        if 4 <= bar and not brk:
            drums(tr, bar, kicks=(0, 2, 2.75), hats=[i + 0.5 for i in range(4)], k=0.85, h=0.18)
            for b in (1, 3): tr.add(clap(0.5), tr.at(bar, b), 0.05, 1, 0.3)
        if brk:
            for b in range(8):
                if (bar * 8 + b) % 3 != 1: tr.add(tick(0.25, 1800 + 400 * ((bar * 5 + b * 3) % 7)), tr.at(bar, b / 2), ((b % 3) - 1) * 0.6, 1, 0.5)
        if bar % 4 == 2 and bar >= 8: tr.add(laser(0.25), tr.at(bar, 3.5), (0.6 if bar % 8 == 2 else -0.6), 1, 0.4)
        if bar in (7, 19, 29): tr.add(riser(tr.beat * 4, 0.25), tr.at(bar), 0, 1, 0.3)
    for ph in (8, 20):
        t, prev = tr.at(ph), None
        for x, d in M:
            if x is not None:
                tr.add(theremin(x, d * tr.beat * 0.98, 0.34, prev), t, 0.1, 1, 0.5); prev = x
            t += d * tr.beat
    return tr


def vault():
    """THE VAULT OPENS - a fanfare, once: a timpani roll, a brass call, a crash, the choir and bells on a D major chord"""
    tr = Track('vault', 120, 5)
    for i in range(16):                                 # the roll, swelling
        tr.add(timp('D2' if i % 2 else 'A1', 0.15 + 0.03 * i, 4), tr.at(0, i / 8), 0, 1, 0.35)
    call = [('D4', 1 / 3), ('D4', 1 / 3), ('D4', 1 / 3), ('A4', 1.5), ('F#4', 0.5), ('A4', 1 / 3), ('A4', 1 / 3), ('A4', 1 / 3)]
    t = tr.at(0, 2)
    for x, d in call:
        tr.add(brass([x], d * tr.beat * 0.92, 0.5, 3000, 0.01), t, 0.1, 1, 0.4)
        tr.add(brass([m(x) - 5], d * tr.beat * 0.92, 0.32, 2400, 0.01), t, -0.15, 1, 0.4)
        t += d * tr.beat
    big = tr.at(1, 3)
    tr.add(brass(['D4', 'F#4', 'A4', 'D5'], tr.beat * 7, 0.55, 3200, 0.02), big, 0, 1, 0.5)
    tr.add(choir(['D4', 'F#4', 'A4', 'D5'], tr.beat * 7, 0.42, 0.25), big, 0, 1, 0.6)
    tr.add(crash(0.5, 3.5), big, 0.2, 1, 0.4)
    tr.add(timp('D2', 0.9), big, 0, 1, 0.4); tr.add(kick(0.8), big, 0, 1, 0.2)
    tr.add(sub('D2', tr.beat * 6, 0.5), big, 0, 1, 0.05)
    for i, x in enumerate(['D6', 'A5', 'F#5', 'D5', 'A5', 'D6']):
        tr.add(bell(x, 2.5, 0.18, 3.01, 1.0, 1.8), big + i * tr.beat * 0.5, (-0.5 + 0.2 * i), 1, 0.6)
    tr.add(timp('A1', 0.5), tr.at(3, 1), 0, 1, 0.4); tr.add(timp('D2', 0.7), tr.at(3, 2), 0, 1, 0.4)
    return tr


# ------------------------------------------------------------------ 2.82: King Omega and his palace - one tune, two ways
OMEGA3 = mel('D5 G5 A#5 A5:2 G5 F#5 A5 D5 G5:3 D5 G5 A#5 D6:2 C6 A#5 A5 F#5 G5:3')                 # (the waltz, 3/4)
OMEGA4 = mel('D5:.5 G5:.5 A#5 A5:1.5 G5:.5 F#5 A5 D5 r G5:3 r D5:.5 G5:.5 A#5 D6:1.5 C6:.5 A#5 A5 F#5 D5 G5:3 r '
             'A#5:.5 A5:.5 G5:.5 F#5:.5 G5 D5 D#5:2 D5:2')                                                    # (the march, 4/4)


def musicbox(f, dur, amp=1.0):
    """a music box's tine: a bright FM ping, an octave of shimmer, a slow fade"""
    a = bell(f, max(dur, 1.6), amp, 2.0, 2.6, 1.6)
    b = bell(hz(m(f) + 12) if isinstance(f, str) else fq(f) * 2, 1.2, amp * 0.25, 3.0, 4.0, 1.0)
    a[:len(b)] += b[:len(a)]
    return a


def omega():
    """KING OF THE DEAD - 120 BPM in G harmonic minor: a cathedral organ, a heartbeat on the timpani, a ghost choir, his waltz
    turned to a march - the music box breaks through in the middle, the old king remembering"""
    tr = Track('omega', 120, 32)
    prog = [('G2', 'm'), ('D#2', 'M'), ('C3', 'm'), ('D2', 'M')]
    assert bars_of(OMEGA4) == 8
    for bar in range(32):
        ch = chord(*prog[bar % 4]); root = ch[0]
        brk = 20 <= bar < 24
        tr.add(organ([root] + [x + 12 for x in ch], tr.beat * 4, 0.32 if not brk else 0.18), tr.at(bar), 0, 1, 0.65)
        tr.add(sub(root - 12, tr.beat * 3.9, 0.42), tr.at(bar), 0, 1, 0.05)
        for b in (0, 0.4) if bar < 4 or brk else ():
            tr.add(timp(root - 12, 0.6 if b == 0 else 0.4, 3.0), tr.at(bar, b), 0, 1, 0.4)          # (a heartbeat)
        if 4 <= bar < 32 and not brk:
            drums(tr, bar, kicks=(0, 2, 2.5), snares=(1, 3), hats=[i / 2 for i in range(8)], k=0.85, s=0.5, h=0.1)
            for b in (0, 2): tr.add(timp(root - 12, 0.5), tr.at(bar, b), 0, 1, 0.45)
            osti = [root + 24, root + 27, root + 31, root + 27]
            for i in range(8): tr.add(strings(osti[i % 4], tr.beat * 0.45, 0.15, 2200), tr.at(bar, i / 2), (-0.3 if i % 2 else 0.3), 1, 0.3)
        if bar >= 12 and not brk:
            tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.3, 0.4), tr.at(bar), 0, 1, 0.6)
        if bar < 4:
            tr.add(choir(['G3', 'A#3', 'D4'], tr.beat * 4, 0.22, 1.2), tr.at(bar), 0, 1, 0.75)
            tr.add(hiss(tr.beat * 3, 0.25), tr.at(bar, 0.5), (bar % 2) * 1.4 - 0.7, 1, 0.6)
        if bar % 8 == 4: tr.add(crash(0.3), tr.at(bar), 0.3, 1, 0.3)
        if bar in (3, 11, 19, 23, 31): tr.add(riser(tr.beat * 4, 0.24), tr.at(bar), 0, 1, 0.3)
    play(tr, tr.at(4), OMEGA4, lambda x, d: organ([x], d, 0.5), 0.1, 1, 0.5)
    play(tr, tr.at(12), OMEGA4, lambda x, d: brass([x], d, 0.44, 2800, 0.04), 0.1, 1, 0.4)
    play(tr, tr.at(12), tp(OMEGA4, -12), lambda x, d: brass([x], d, 0.3, 1600, 0.06), -0.2, 1, 0.45)
    t = tr.at(20)
    for x, d in OMEGA3[:12]:                                         # (the break: the waltz on a music box, half the phrase)
        if x is not None: tr.add(musicbox(x, d * tr.beat, 0.4), t, 0.3, 1, 0.55)
        t += d * tr.beat * 4 / 3
    play(tr, tr.at(24), OMEGA4, lambda x, d: choir([x], d + 0.15, 0.42, 0.1), 0, 1, 0.55)
    play(tr, tr.at(24), tp(OMEGA4, 12), lambda x, d: lead(x, d, 0.16, 2600), 0.3, 1, 0.45)
    play(tr, tr.at(24), OMEGA4, lambda x, d: brass([x], d, 0.4, 3000, 0.03), 0.1, 1, 0.4)
    return tr


def palace():
    """THE OMEGA PALACE - a haunted waltz, 72 BPM in G minor (3/4): his tune on a music box in an empty ballroom, a slow pad,
    a far-off organ, the wind through the halls and a choir that is not quite there"""
    tr = Track('palace', 72, 24, beats=3)
    prog = [('G2', 'm'), ('G2', 'm'), ('D#2', 'M'), ('D2', 'M'), ('C3', 'm'), ('G2', 'm'), ('A2', 'dim'), ('D2', 'M')]
    assert bars_of(OMEGA3, 3) == 8
    for bar in range(24):
        ch = chord(*prog[bar % 8]); root = ch[0]
        tr.add(pad([x + 12 for x in ch], tr.beat * 3 + 0.6, 0.18, 900, 1.2, 1.2), tr.at(bar), 0, 1, 0.7)
        tr.add(pluck(hz(root), tr.beat * 1.2, 0.4, 0.99) * 0.5, tr.at(bar), -0.1, 1, 0.4)                     # (oom - pah - pah)
        for b in (1, 2): tr.add(harpsi(hz(ch[1] + 12), 0.5, 0.12) + harpsi(hz(ch[2] + 12), 0.5, 0.12), tr.at(bar, b), 0.2, 1, 0.5)
        if bar % 4 == 0: tr.add(organ([root] + [x + 12 for x in ch], tr.beat * 6, 0.12), tr.at(bar), -0.4, 1, 0.85)  # (far off)
        if bar % 3 == 1: tr.add(hiss(tr.beat * 4, 0.22), tr.at(bar, 1), (bar % 2) * 1.6 - 0.8, 1, 0.7)            # (the wind)
        if 8 <= bar < 16: tr.add(choir([ch[0] + 12, ch[2] + 12], tr.beat * 3, 0.14, 1.0), tr.at(bar), 0, 1, 0.8)
        if bar in (7, 15, 23): tr.add(bell('G6', 3.0, 0.06, 3.01, 1.0, 2.2), tr.at(bar, 2), 0.6, 1, 0.8)            # (a far-off chime)
    play(tr, tr.at(0), OMEGA3, lambda x, d: musicbox(x, d, 0.32), 0.25, 1, 0.55)
    play(tr, tr.at(8), OMEGA3, lambda x, d: musicbox(x, d, 0.28), -0.25, 1, 0.6)
    play(tr, tr.at(8), tp(OMEGA3, -12), lambda x, d: theremin(x, d, 0.1), 0.1, 1, 0.7)
    play(tr, tr.at(16), OMEGA3, lambda x, d: musicbox(x, d, 0.34), 0.25, 1, 0.55)
    play(tr, tr.at(16), tp(OMEGA3, 12), lambda x, d: musicbox(x, d, 0.1), -0.4, 1, 0.75)
    return tr


TRACKS = {'hunt': hunt, 'sands': sands, 'abyss': abyss, 'dungeon': dungeon, 'hollow': hollow, 'hollow2': hollow2, 'serpent': serpent,
          'serpent2': serpent2, 'storm': storm, 'tide': tide, 'blood': blood, 'vorn': vorn, 'vault': vault, 'omega': omega, 'palace': palace}
LENGTH = {'hunt': 60, 'sands': 60, 'abyss': 60, 'dungeon': 60, 'hollow': 64, 'hollow2': 60, 'serpent': 64, 'serpent2': 64,
          'storm': 60, 'tide': 60, 'blood': 60, 'vorn': 60, 'vault': 10, 'omega': 64, 'palace': 60}


def save(tr, room=1.8, bright=5000):
    mix_ = tr.render(room, bright)
    fd, wav = tempfile.mkstemp(suffix='.wav'); os.close(fd)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix_.T * 32767).astype('<i2').tobytes())
    out = os.path.join(OUT, f'boss_{tr.name}.ogg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '0', out], check=True)
    os.remove(wav)
    print(f'{out}: {tr.seconds:.0f} s, {os.path.getsize(out) // 1024} KB')


if __name__ == '__main__':
    for nm in (sys.argv[1:] or list(TRACKS)):
        tr = TRACKS[nm]()
        assert round(tr.seconds) == LENGTH[nm], (nm, tr.seconds)
        save(tr, room=2.6 if nm in ('hollow', 'abyss', 'vault', 'tide', 'omega') else 3.4 if nm == 'palace' else 1.8)
