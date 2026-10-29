"""2.99a: synthesises THE LAST LIGHT - the Divine One's coming, and the end of the Dread Sovereign (vendor/boss_divine.ogg,
30 s, played once by phase238's falling scene at tick 2). Triumphant and cinematic, scored to the scene's own timeline: every
cue below is placed from the scene's tick (cue(tick) = (tick - 2) / 20 s), so it lands where the scene does.

F MAJOR, 120 BPM in 4/4 (a bar is 2 s) from His revealing: bar 0 is tick 160, the smiting (tick 320) is bar 4's downbeat.
The tune is Aurel's cell in major (C F A G F E F; tools/sovereign_music.py): what the Sovereign was, sung back to it.

  0.0 - 7.9   THE DESCENT   hushed and awed: a high shimmer (string harmonics, a far 'oo' choir); the beam (tick 40) - a
                            soft bell; HE appears (tick 60) - the choir opens to 'ah', light motes fall in celesta and bells
                            as He comes down, a horn far off hints the call; a pianissimo timpani roll and a cymbal swell
  7.9 - 15.9  THE SWELL     REVEALED (tick 160): six wings of choir sweep up onto F major, a timpani stroke; the horns'
                            call, the trumpets' answer (tick 200, He looks down); AUREL named (tick 250): the cell in the
                            trumpets over Bb - F - Gm - C - Dm; His hand rises (tick 290): Db major, Eb major, the thirds
                            climbing in the trumpets (F, G), the timpani rolling, a cymbal swelling, the air drawn in -
  15.9        THE SMITING   (tick 320) - A: F major, everything. Full brass, the great organ, the full choir, the bells, a
                            boom, two crashes, timpani on the fanfare's rhythm; the cell made a hero's tune
                            (A C A C | D C Bb A G | F), the horns in counterpoint, the strings rushing up into the cadence
 19.9 - 21.4  IT IS OVER    (tick 400) the last F major struck and let ring
 21.4 - 30.0  REST          ("Rest now", tick 430) warm and still: a soft organ, a hushed choir, the violin sings the cell
                            gently; "you" (tick 460) on Bb major 7 over the F (an amen), home to F as He rises (tick 480),
                            light rising in the celesta; the last flash (tick 548) a far bell - and it fades with the scene

Deterministic; run it to rebuild the .ogg (needs numpy, scipy and ffmpeg), and optionally an MP3 preview:
    python3 tools/divine_music.py [preview.mp3]"""
import os, sys, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, T, env, lp, hp, bp, sub
from boss_music import timp, crash, mel, thunder
from sovereign_music import (great_bell, chorus, wing, great_organ, soft_organ, glass, boom, suck, edge, render, _guarded, _decode,
                             seeded)
from dread_music import violin
from armada_music import horn, stab, apad, sbell

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
SECS = 30                        # (the file; the scene is 550 ticks, 27.4 s of it after the music starts)
PAD = 4                          # (rendered 4 s longer, then cut, so no reverb wraps round into the hush at the start)
BPM = 120


def cue(tick):
    """the scene's tick -> seconds into the track (it is played at tick 2)"""
    return (tick - 2) / 20.0


T_BEAM, T_HE, T_REVEAL, T_GAZE, T_NAME, T_RAISE, T_SMITE = cue(40), cue(60), cue(160), cue(200), cue(250), cue(290), cue(320)
T_END, T_REST, T_YOU, T_ASCEND, T_FADE, T_FLASH = cue(400), cue(430), cue(460), cue(480), cue(520), cue(548)
BEAT = 60.0 / BPM


def g(bar, beat=0.0):
    """the grid from His revealing: bar 0 = tick 160"""
    return T_REVEAL + (bar * 4 + beat) * BEAT


assert abs(g(4) - T_SMITE) < 1e-9 and abs(g(2, 1) - T_NAME) < 1e-9 and abs(g(3, 1) - T_RAISE) < 1e-9


# ====================================================================== instruments (mono)
def trumpet(x, d, amp=1.0):
    """a trumpet: polyBLEP saws through a resonant filter that opens as it speaks (a scoop up into the pitch), a bright
    bell-formant, a breath at the lip"""
    s = horn([x], d, 1.0, bright=4800, close=900, swell=0.03, vib=5.4, scoop=0.5, q=1.25)
    s = s + bp(s, 1100, 2600, 1) * 0.6
    t = T(len(s) / SR)
    s = s + hp(R.noise(len(s)), 2500) * 0.05 * np.exp(-t / 0.04)
    return amp * s / 1.4


def horns(notes, d, amp=1.0):
    """French horns: warm, round, a slow speech"""
    return amp * horn(notes, d, 1.0, bright=1900, close=420, swell=0.14, vib=4.8, scoop=0.25, q=0.9)


def bones(notes, d, amp=1.0):
    """trombones and tuba: the low brass, a little blat"""
    return amp * horn(notes, d, 1.0, bright=1500, close=300, swell=0.06, vib=0.0, scoop=0.2, q=1.1)


def choir(notes, d, amp=1.0, attack=0.6, vowel='a'):
    """the heavenly choir: sovereign_music's formant choir, sung twice (two sections, a hair apart), with breath in it"""
    a = chorus(notes, d, 1.0, attack, vowel, 4.6)
    b = chorus(notes, d, 1.0, attack * 1.2, vowel, 5.3)
    n = min(len(a), len(b))
    s = a[:n] + b[:n] * 0.8
    s += bp(R.noise(n), 1800, 4500) * 0.035 * env(n, attack, 0, 1, 0.9)
    return amp * 2.6 * s / 1.5


def shimmer(notes, d, amp=1.0, attack=2.5, release=2.0):
    """high strings in harmonics: pure tones, a slow chorus of three each, a glittering tremble"""
    t = T(d); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = fq(x)
        for v in (-0.0025, 0.0, 0.0028):
            fr = f * (1 + v) * (1 + 0.0018 * np.sin(2 * np.pi * (5.1 + 40 * v) * t + R.r() * 6.28))
            s += np.sin(2 * np.pi * np.cumsum(fr) / SR + R.r() * 6.28) + 0.12 * np.sin(4 * np.pi * np.cumsum(fr) / SR)
    s *= 0.8 + 0.2 * np.sin(2 * np.pi * 7.3 * t) * np.sin(2 * np.pi * 0.37 * t)
    return amp * s / (len(notes) * 3) * env(n, attack, 0, 1, release)


def celesta(x, d=1.8, amp=1.0):
    """a celesta: a struck bar, its octave partial and a quick metallic tick"""
    f = fq(x); t = T(d)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6) + 0.35 * np.sin(2 * np.pi * f * 4.0 * t) * np.exp(-t * 9)
    s += 0.12 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 14)
    return amp * s * env(len(t), 0.001, 0, 1, 0.1)


def strings(notes, d, amp=1.0, attack=0.8, release=1.0, cut=2600):
    """a string section, sustained: detuned band-limited saws, a slow filter breathing"""
    return amp * 2.2 * apad(notes, d, 1.0, cut, attack, release, voices=4, det=0.006, lfo=0.21, depth=0.18, q=0.9)


def timpani(x, amp=1.0, dec=2.0):
    """a timpani stroke: boss_music's pitched drum with the felt's thud and a noise burst under it"""
    s = timp(x, 1.0, dec)
    t = T(len(s) / SR)
    s = s + lp(R.noise(len(s)), 420) * np.exp(-t * 22) * 0.7
    return amp * 0.42 * s


def cym_swell(d, amp=1.0):
    """a suspended cymbal rolled with soft mallets: noise and a cloud of inharmonic partials, swelling to a peak at the end"""
    t = T(d); n = len(t)
    s = hp(R.noise(n), 3200) * 0.8 + bp(R.noise(n), 6000, 9500) * 0.5
    for i, f in enumerate((3120, 4410, 5230, 6870, 7930, 9150)):
        s += 0.05 * np.sin(2 * np.pi * f * t * (1 + 0.003 * np.sin(2 * np.pi * (3 + i) * t)))
    return edge(amp * s * (t / d) ** 2.6, 0.01)


def splash(amp=1.0, d=4.0):
    """a crash cymbal with a ringing body"""
    t = T(d)
    s = crash(1.0, d)
    for f, a in ((3350, 0.06), (4870, 0.05), (6210, 0.04), (8120, 0.03)):
        s = s + a * np.sin(2 * np.pi * f * t) * np.exp(-t * 1.8)
    return amp * s


# ====================================================================== players
def line(tr, t0, notes, inst, pan=0.0, gain=1.0, wet=0.35, legato=0.96):
    t = t0
    for x, d in notes:
        if x is not None: tr.add(inst(x, d * BEAT * legato), t, pan, gain, wet)
        t += d * BEAT
    return t


def roll(tr, t0, d, x, a0, a1, rate=15.0, pan=0.0, wet=0.4):
    """a timpani roll: strokes at rate a second, each a hair off the grid, swelling from a0 to a1"""
    k = int(d * rate)
    gg = np.random.default_rng(int(t0 * 100))
    for i in range(k):
        u = i / max(1, k - 1)
        tr.add(timpani(x, (a0 + (a1 - a0) * u ** 1.5) * gg.uniform(0.85, 1.0), 3.0), t0 + i / rate + gg.uniform(-0.006, 0.006),
               pan + (0.08 if i % 2 else -0.08), 1, wet)


def runs(tr, t0, notes, amp=0.3, pan=0.25, wet=0.35, dur=0.25):
    """fast detached violin notes (spiccato), dur beats each"""
    t = t0
    for x in notes:
        tr.add(violin(x, BEAT * dur * 0.8, amp, attack=0.012, scoop=0.004, depth=0.0), t, pan, 1, wet)
        t += BEAT * dur
    return t


def snare_roll(tr, t0, d, a0, a1, rate=24.0):
    from gv_music import snare
    k = int(d * rate)
    for i in range(k):
        u = i / max(1, k - 1)
        tr.add(snare(a0 + (a1 - a0) * u ** 2, 200), t0 + i / rate, 0.15, 1, 0.4)


def ch(root, kind):
    r = m(root) if isinstance(root, str) else root
    return [r + i for i in {'M': (0, 4, 7), 'm': (0, 3, 7), 'M7': (0, 4, 7, 11), 'add9': (0, 4, 7, 14), 'sus': (0, 5, 7), 'm7': (0, 3, 7, 10),
                            '7': (0, 4, 7, 10)}[kind]]


def broot(c):
    """the chord's root in the low brass's range (E2 - Eb3)"""
    return m('E2') + (c[0] - m('E2')) % 12


def voice(c, lo, k):
    """the chord's tones from lo upwards, k of them"""
    out, x = [], lo
    while len(out) < k:
        if any((x - y) % 12 == 0 for y in c): out.append(x)
        x += 1
    return out


def organ(notes, *k, **kw):
    """the great organ, brought up to sit with the brass; its low notes an octave up (its 16' stop is under every note, and
    the low brass have the floor)"""
    notes = [x + 12 if x < m('C3') else x for x in (m(y) if isinstance(y, str) else y for y in notes)]
    return 1.7 * great_organ(notes, *k, **kw)


def thud(amp=1.0, *k):
    return boom(amp * 0.5, *k)


def low(x, d, amp=1.0):
    return sub(x, d, amp * 0.2)


# ====================================================================== the score
def compose(tr):
    a = tr.add
    F, Bb, C, Dm, Gm, Db, Eb = ch('F2', 'M'), ch('Bb1', 'M'), ch('C2', 'M'), ch('D2', 'm'), ch('G1', 'm'), ch('Db2', 'M'), ch('Eb2', 'M')

    # ---------------------------------------------------------------- 1. THE DESCENT (0 - 7.9): hushed, awed
    a(shimmer(['F5', 'C6', 'A6'], T_REVEAL + 0.6, 0.08, 3.0, 1.0), 0.15, 0.0, 1, 0.75)            # (the light, before anything)
    a(choir(['F4', 'C5', 'F5'], T_HE + 0.4, 0.07, 2.5, 'u'), 0.9, -0.1, 1, 0.8)                  # (tick 20: dragged into the beam)
    a(great_bell('C5', 7.0, 0.06, 0.7, 31), T_BEAM, 0.15, 1, 0.8)                               # (tick 40: the beam - a far bell)
    a(sbell('C7', 3.0, 0.035), T_BEAM + 0.02, -0.4, 1, 0.8); a(sbell('F6', 3.0, 0.035), T_BEAM + 0.06, 0.4, 1, 0.8)
    # (tick 60: HE appears - the choir opens to 'ah', the strings beneath, light falling with Him)
    a(choir(voice(F, m('F4'), 5), T_REVEAL - T_HE + 0.5, 0.1, 3.8, 'a'), T_HE, 0, 1, 0.7)
    a(strings(voice(F, m('F3'), 4), T_REVEAL - T_HE + 0.4, 0.07, 3.5, 0.6, 1500), T_HE, 0, 1, 0.6)
    a(great_bell('F5', 6.0, 0.05, 0.6, 32), T_HE, -0.2, 1, 0.8)
    falling = [m('F7'), m('C7'), m('A6'), m('G6'), m('F6'), m('C6'), m('A5'), m('G5')]
    for k in range(20):                                                    # (motes of light, coming down with Him)
        x = falling[k % 8] - (12 if k >= 12 else 0)
        a(celesta(x, 2.0, 0.05 + 0.002 * k), T_HE + 0.2 + 0.24 * k, -0.7 + 1.4 * ((k * 0.382) % 1), 1, 0.75)
    for k, x in enumerate(('A6', 'F6', 'C6', 'A5')):
        a(sbell(x, 3.0, 0.045), T_HE + 1.0 + 1.1 * k, (0.5, -0.5)[k % 2], 1, 0.8)
    a(soft_organ(['C3', 'F3', 'A3'], T_REVEAL - cue(98) + 0.3, 0.12, 2.5, 0.4), cue(98), 0, 1, 0.55)   # (the floor of it)
    line(tr, cue(110), mel('C4:1 F4:1 G4:.5 A4:3.5'), lambda x, d: horns([x], d, 0.12), -0.35, 1, 0.75)  # (a horn, far off: the call)
    roll(tr, T_REVEAL - 2.2, 2.2, 'C2', 0.03, 0.2, 14)                  # (a pianissimo roll, swelling)
    a(cym_swell(2.0, 0.16), T_REVEAL - 2.0, 0.2, 1, 0.5)
    a(suck(1.2, 0.18), T_REVEAL - 1.2, -0.2, 1, 0.35)

    # ---------------------------------------------------------------- 2. THE SWELL (7.9 - 15.9)
    # bar 0 - REVEALED: the wings open (six choir voices sweeping up onto F major), a timpani stroke, the horns' call
    targets = [m('F4'), m('A4'), m('C5'), m('F5'), m('A5'), m('C6')]
    for i, x in enumerate(targets):
        a(wing(hz(x - 14 - (i % 3)), hz(x), 3.6 - 0.08 * i, 0.07 * (1 - 0.05 * i), 0.45, 'a'), g(0) + 0.06 * i, -0.7 + 0.28 * i, 1, 0.6)
    a(timpani('F2', 0.55), g(0), 0, 1, 0.4); a(thud(0.25, 80, 34, 2.2), g(0), 0, 1, 0.4)
    a(splash(0.22, 3.5), g(0), 0.25, 1, 0.55)
    a(great_bell('F3', 7.0, 0.32, 0.9, 33), g(0), -0.15, 1, 0.65)
    a(choir(voice(F, m('F3'), 7), 4.1, 0.26, 0.5, 'a'), g(0), 0, 1, 0.6)
    a(strings(voice(F, m('F3'), 6), 4.1, 0.12, 0.4, 0.5, 2400), g(0), 0, 1, 0.55)
    a(organ(['F2', 'C3', 'F3', 'A3'], 4.1, 0.16, 0.5, 0.5), g(0), 0, 1, 0.55)
    line(tr, g(0, 0.5), mel('C4:.5 F4:.5 G4:.5 A4:2'), lambda x, d: horns([m(x), m(x) - 5], d, 0.3), -0.3, 1, 0.45)   # (the call)
    # bar 1 - He looks down (tick 200): Dm, Bb; the trumpets answer, softly; the timpani murmur
    a(choir(voice(Dm, m('D3'), 6), 2.1, 0.2, 0.3, 'o'), g(1), 0, 1, 0.65); a(choir(voice(Bb, m('D3'), 6), 2.2, 0.2, 0.3, 'o'), g(1, 2), 0, 1, 0.65)
    a(strings(voice(Dm, m('D3'), 5), 2.1, 0.12, 0.3, 0.4), g(1), 0, 1, 0.55); a(strings(voice(Bb, m('D3'), 5), 2.2, 0.12, 0.3, 0.4), g(1, 2), 0, 1, 0.55)
    a(bones([m('D3'), m('A3')], 2.0, 0.16), g(1), 0, 1, 0.4); a(bones([m('Bb2'), m('F3')], 2.0, 0.16), g(1, 2), 0, 1, 0.4)
    line(tr, g(1, 0.5), mel('A4:.5 D5:.5 E5:.5 F5:1.5 D5:.5 F5:.5'), lambda x, d: trumpet(x, d, 0.16), 0.3, 1, 0.5)
    roll(tr, g(1), 1.8, 'F2', 0.05, 0.12, 12)
    a(timpani('Bb1', 0.3), g(1, 2), 0, 1, 0.4)
    # bar 2 - AUREL (tick 250, beat 1): the cell in the trumpets - Bb, F, Gm, C, Dm
    a(timpani('F2', 0.42), g(2, 1), 0, 1, 0.4); a(great_bell('C4', 6.0, 0.28, 1.0, 34), g(2, 1), 0.2, 1, 0.6)
    a(splash(0.16, 3.0), g(2, 1), -0.25, 1, 0.55)
    harm = [(g(2, 0), 1, Bb), (g(2, 1), 1.5, F), (g(2, 2.5), 0.5, Gm), (g(2, 3), 1, C), (g(3, 0), 1, Dm)]
    for t0, nb, c in harm:
        d = nb * BEAT + 0.15
        a(choir(voice(c, m('F3') if c is F else m('D3'), 6), d + 0.2, 0.27, 0.12, 'a'), t0, 0, 1, 0.6)
        a(strings(voice(c, m('C3'), 6), d + 0.2, 0.14, 0.1, 0.3, 2800), t0, 0, 1, 0.55)
        a(horns(voice(c, m('A3'), 3), d, 0.22), t0, -0.35, 1, 0.45)
        a(bones([broot(c), broot(c) + 7], d, 0.22), t0, 0.1, 1, 0.4)
        a(low(broot(c) - 12, d, 0.14), t0, 0, 1, 0.1)
    cell = mel('r:1 C5:.5 F5:.5 A5:1 G5:.5 F5:.5 E5:.5 F5:.5')
    line(tr, g(2), cell, lambda x, d: trumpet(x, d, 0.3), 0.15, 1, 0.45)
    line(tr, g(2), cell, lambda x, d: trumpet(m(x) - 12, d, 0.16), -0.2, 1, 0.45)        # (doubled an octave down)
    for t0 in (g(2, 3), g(2, 3.5)): a(timpani('C2', 0.3), t0, 0, 1, 0.4)
    # bar 3 - His hand rises (tick 290): Db, Eb - the thirds climbing (F, G) into the A of the smiting; everything gathers
    for t0, nb, c, top in ((g(3, 1), 1.5, Db, 'F5'), (g(3, 2.5), 1.5, Eb, 'G5')):
        d = nb * BEAT + 0.1
        a(choir(voice(c, m('Ab3') if c is Db else m('Bb3'), 6), d + 0.15, 0.32, 0.15, 'a'), t0, 0, 1, 0.6)
        a(strings(voice(c, m('Db3') if c is Db else m('Eb3'), 7), d + 0.15, 0.17, 0.15, 0.2, 3200), t0, 0, 1, 0.5)
        a(horns(voice(c, m('Ab3') if c is Db else m('Bb3'), 4), d, 0.3), t0, -0.35, 1, 0.45)
        a(bones([broot(c), broot(c) + 7, broot(c) + 12], d, 0.3), t0, 0.1, 1, 0.4)
        a(organ([broot(c)] + voice(c, broot(c) + 7, 5), d, 0.17, 0.08, 0.7), t0, 0, 1, 0.55)
        a(trumpet(top, d - 0.05, 0.32), t0, 0.15, 1, 0.45); a(trumpet(m(top) - 12 + (3 if c is Db else 3), d - 0.05, 0.2), t0, -0.15, 1, 0.45)
    line(tr, g(3, 1), mel('Ab4:.25 Bb4:.25 C5:.25 Db5:.25 Eb5:.25 F5:.25 Bb4:.25 C5:.25 D5:.25 Eb5:.25 F5:.25 G5:.25'),
         lambda x, d: violin(x, d * 0.85, 0.11, attack=0.012, scoop=0.004, depth=0.0), 0.35, 1, 0.4)      # (the strings rushing up)
    roll(tr, g(3, 1), 1.5, 'C2', 0.14, 0.5, 18)
    snare_roll(tr, g(3, 1), 1.5, 0.03, 0.22)
    a(cym_swell(1.5, 0.45), g(3, 1), 0.2, 1, 0.45)
    a(suck(1.0, 0.35), g(4) - 1.0, -0.2, 1, 0.3)

    # ---------------------------------------------------------------- 3. THE SMITING (15.9): F major, everything
    hit = g(4)
    a(thud(0.7, 120, 30, 3.5), hit, 0, 1, 0.4); a(thunder(0.4, 4.0), hit, -0.2, 1, 0.5)
    a(splash(0.6, 4.5), hit, 0.25, 1, 0.5); a(splash(0.45, 4.0), hit + 0.01, -0.3, 1, 0.5)
    a(great_bell('F2', 9.0, 0.5, 1.2, 35), hit, 0, 1, 0.6); a(great_bell('C4', 6.0, 0.3, 1.0, 36), hit + 0.02, 0.3, 1, 0.6)
    # the harmony, bar by bar: F | Bb C | F (struck, let ring)
    plan = [(g(4), 4, F), (g(5), 2, Bb), (g(5, 2), 2, C)]
    for t0, nb, c in plan:
        d = nb * BEAT + 0.12
        a(organ([broot(c)] + voice(c, broot(c) + 7, 6), d, 0.24, 0.02, 1.0), t0, 0, 1, 0.55)
        a(choir(voice(c, m('F3') if c is F else m('D3') if c is Bb else m('E3'), 8), d + 0.2, 0.36, 0.05, 'a'), t0, 0, 1, 0.55)
        a(strings(voice(c, m('C3'), 8), d + 0.15, 0.2, 0.03, 0.25, 3600), t0, 0, 1, 0.5)
        a(bones([broot(c), broot(c) + 7, broot(c) + 12], d, 0.36), t0, 0.1, 1, 0.35)
        a(low(broot(c) - 12, d, 0.22), t0, 0, 1, 0.1)
        a(horns(voice(c, m('A3') if c is not Bb else m('Bb3'), 3), d, 0.22), t0, 0.35, 1, 0.45)
    # the hero's tune (the cell, made one): A C A C | D C Bb A G | F
    hero = mel('A5:2 C6:1 A5:.5 C6:.5 D6:1.5 C6:.5 Bb5:.5 A5:.5 G5:1')
    line(tr, g(4), hero, lambda x, d: trumpet(x, d, 0.36), 0.15, 1, 0.4)
    line(tr, g(4), hero, lambda x, d: trumpet(m(x) - 12, d, 0.22), -0.1, 1, 0.4)
    line(tr, g(4), mel('F4:1 A4:1 C5:2 Bb4:1 F4:1 C5:1 E5:1'), lambda x, d: horns([x], d, 0.3), -0.4, 1, 0.45)   # (counterpoint)
    line(tr, g(4), hero, lambda x, d: violin(x, d, 0.13, depth=0.006, voices=3), 0.3, 1, 0.45)                        # (the violins with it)
    # timpani on the fanfare's rhythm; the stabs; the strings rushing up into the cadence
    for (b, beat), x, amp in (((4, 0), 'F2', 0.9), ((4, 0), 'C2', 0.6), ((4, 2), 'C2', 0.4), ((4, 3), 'F2', 0.45), ((4, 3.5), 'F2', 0.5),
                              ((5, 0), 'Bb1', 0.7), ((5, 1.5), 'F2', 0.4), ((5, 2), 'C2', 0.65), ((5, 3), 'C2', 0.5), ((5, 3.25), 'C2', 0.52),
                              ((5, 3.5), 'C2', 0.56), ((5, 3.75), 'C2', 0.62)):
        a(timpani(x, amp), g(b, beat), 0, 1, 0.4)
    for t0, c in ((g(4, 3), F), (g(4, 3.5), F), (g(5, 1.5), Bb)):
        a(stab(voice(c, m('A3'), 4), 0.32, 0.18, 5200, 600, 11), t0, -0.1, 1, 0.35)
    runs(tr, g(5, 2), [m(x) for x in ('C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'Bb5', 'C6')], 0.12, 0.35, 0.4, 0.25)
    runs(tr, g(5, 2), [m(x) for x in ('C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5')], 0.1, -0.35, 0.4, 0.25)
    a(cym_swell(1.0, 0.4), g(6) - 1.0, 0.2, 1, 0.45)

    # ---------------------------------------------------------------- 4. IT IS OVER (19.9): the last F major, struck and let ring
    end = g(6)
    a(timpani('F2', 1.0, 1.4), end, 0, 1, 0.4); a(timpani('C2', 0.55, 1.4), end, 0, 1, 0.4); a(thud(0.5, 100, 32, 3.0), end, 0, 1, 0.4)
    a(splash(0.5, 5.0), end, 0.2, 1, 0.55)
    a(great_bell('F3', 9.0, 0.45, 1.0, 37), end, -0.15, 1, 0.6)
    ring = 2.4
    swell_down = lambda s: s * np.linspace(1.0, 0.25, len(s)) ** 1.6
    a(swell_down(trumpet('F5', ring, 0.36)), end, 0.15, 1, 0.45); a(swell_down(trumpet('A5', ring, 0.22)), end, 0.3, 1, 0.45)
    a(swell_down(trumpet('C5', ring, 0.2)), end, -0.1, 1, 0.45)
    a(swell_down(horns(['F3', 'A3', 'C4', 'F4'], ring, 0.34)), end, -0.35, 1, 0.45)
    a(swell_down(bones(['F2', 'C3', 'F3'], ring, 0.34)), end, 0.1, 1, 0.4)
    a(swell_down(organ(['F2', 'C3', 'F3', 'A3', 'C4', 'F4'], ring + 0.6, 0.26, 0.02, 1.0)), end, 0, 1, 0.6)
    a(swell_down(choir(voice(F, m('F3'), 9), ring + 0.6, 0.38, 0.04, 'a')), end, 0, 1, 0.6)
    a(swell_down(strings(voice(F, m('F3'), 8), ring + 0.6, 0.2, 0.03, 0.6, 3600)), end, 0, 1, 0.55)
    a(violin('F6', ring, 0.12, voices=3, depth=0.006), end, 0.3, 1, 0.5)
    a(low(m('F1'), ring, 0.25), end, 0, 1, 0.1)
    for k in range(12):                                                    # (it comes apart into light: motes rising and falling)
        x = (m('F6'), m('A6'), m('C7'), m('F7'))[k % 4] - 12 * (k // 8)
        a(celesta(x, 2.0, 0.06), g(4, 0.5) + 0.33 * k, (-0.7, 0.7)[k % 2], 1, 0.75)
        a(glass(x + 12 if k % 3 == 0 else x, 1.4, 0.03), g(4, 0.6) + 0.33 * k, (0.6, -0.6)[k % 2], 1, 0.75)

    # ---------------------------------------------------------------- 5. REST (21.4 - 30): warm, peaceful, radiant
    rest_d = SECS - T_REST + 0.5
    a(soft_organ(['C3', 'F3', 'A3', 'C4'], T_YOU - T_REST + 0.6, 0.3, 0.9, 0.8), T_REST - 0.1, 0, 1, 0.6)
    a(soft_organ(['D3', 'F3', 'A3', 'Bb3'], T_ASCEND - T_YOU + 0.7, 0.3, 0.6, 0.8), T_YOU, 0, 1, 0.6)          # (Bbmaj7 over F: amen)
    a(soft_organ(['C3', 'F3', 'A3', 'C4', 'G4'], SECS - T_ASCEND, 0.3, 0.6, 2.5), T_ASCEND, 0, 1, 0.6)
    a(soft_organ(['F2'], SECS - T_REST, 0.07, 1.5, 2.5), T_REST, 0, 1, 0.5)                          # (the pedal, under it all)
    a(strings(['C3', 'A3', 'C4', 'F4'], T_YOU - T_REST + 0.7, 0.11, 1.0, 0.8, 1600), T_REST - 0.1, 0, 1, 0.6)
    a(strings(['D3', 'Bb3', 'D4', 'F4'], T_ASCEND - T_YOU + 0.8, 0.11, 0.7, 0.8, 1600), T_YOU, 0, 1, 0.6)
    a(strings(['C3', 'A3', 'C4', 'F4', 'G4'], SECS - T_ASCEND, 0.11, 0.7, 3.0, 1700), T_ASCEND, 0, 1, 0.6)
    a(choir(['F3', 'A3', 'C4', 'F4'], T_YOU - T_REST + 0.6, 0.14, 1.2, 'o'), T_REST, 0, 1, 0.7)
    a(choir(['F3', 'Bb3', 'D4', 'A4'], T_ASCEND - T_YOU + 0.6, 0.14, 0.8, 'o'), T_YOU, 0, 1, 0.7)
    a(great_bell('F4', 8.0, 0.14, 0.6, 38), T_REST, 0.25, 1, 0.75)
    # the violin sings the cell gently: C F A (over the amen, "you") G F E F
    sing = lambda x, d: violin(x, d, 0.26, vib=5.0, depth=0.008, attack=0.15, scoop=0.008, bright=0.8)
    t = line(tr, T_REST + 0.25, mel('C5:1 F5:1'), sing, 0.1, 1, 0.6, 0.98)
    t = line(tr, T_YOU - 0.3, mel('A5:2.6 G5:.7 F5:.7 E5:1'), sing, 0.1, 1, 0.6, 0.98)
    a(violin('F5', T_FLASH - t + 1.2, 0.25, vib=5.0, depth=0.008, attack=0.2, scoop=0.006, bright=0.8), t, 0.1, 1, 0.6)
    # He rises (tick 480): the choir lifts, light rises with Him in the celesta, a high shimmer
    a(choir(['F4', 'A4', 'C5', 'F5', 'G5'], SECS - T_ASCEND, 0.13, 1.6, 'a'), T_ASCEND, 0, 1, 0.7)
    rising = [m(x) for x in ('F5', 'G5', 'A5', 'C6', 'F6', 'G6', 'A6', 'C7')]
    for k in range(14):
        a(celesta(rising[k % 8] + (12 if k >= 8 else 0), 2.0, 0.055 - 0.002 * k), T_ASCEND + 0.15 + 0.3 * k, -0.6 + 1.2 * ((k * 0.618) % 1), 1, 0.75)
    a(shimmer(['F6', 'A6', 'C7'], SECS - T_FADE, 0.09, 1.5, 2.5), T_FADE, 0, 1, 0.8)
    # the last flash (tick 548): a far bell, high
    a(great_bell('F5', 6.0, 0.12, 0.6, 39), T_FLASH, -0.2, 1, 0.8); a(sbell('A6', 3.0, 0.05), T_FLASH + 0.04, 0.4, 1, 0.8)
    a(sbell('F7', 2.5, 0.03), T_FLASH + 0.1, -0.4, 1, 0.85)


def divine():
    tr = Track('divine', BPM, (SECS + PAD) // 2)
    compose(tr)
    return tr


def save(tr, out, room=3.2, level=0.2, ceil=0.89):
    """rendered with the old piece's room, the same loudness as the other cinematic tracks; cut at SECS, faded out with the
    scene (from He fading, tick 520, to the end), and the peak kept under -1 dBFS"""
    for b in ('L', 'R', 'wetL', 'wetR'):                              # (no rumble under the floor)
        setattr(tr, b, hp(getattr(tr, b), 32))
    st = render(tr, room, level)
    k = SECS * SR
    st = st[:, :k].copy()
    t = np.arange(k) / SR
    f0, f1 = T_FLASH - 0.5, SECS
    fade = np.where(t < f0, 1.0, np.clip((f1 - t) / (f1 - f0), 0, 1) ** 1.6)
    st *= fade
    st[:, :int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    st = st * (ceil * 0.97 / np.abs(st).max())
    _guarded(st, out, 4, ceil=ceil)


def preview(ogg, mp3):
    os.makedirs(os.path.dirname(mp3), exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', ogg, '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '192k', mp3], check=True)
    print(mp3)


if __name__ == '__main__':
    out = os.path.join(VENDOR, 'boss_divine.ogg')
    save(seeded(10, divine), out)
    x = _decode(out)
    db = lambda v: 20 * np.log10(max(float(v), 1e-9))
    print(f'peak {db(np.abs(x).max()):.2f} dBFS, RMS {db(np.sqrt((x ** 2).mean())):.1f} dBFS, clipped {int((np.abs(x) >= 0.999).sum())}')
    for nm, t0 in (('descent', 0), ('reveal', T_REVEAL), ('name', T_NAME), ('raise', T_RAISE), ('smite', T_SMITE), ('over', T_END),
                   ('rest', T_REST), ('you', T_YOU), ('ascend', T_ASCEND), ('fade', T_FADE)):
        print(f'  {nm:8s} {t0:5.2f} s  (tick {round(t0 * 20 + 2)})')
    if len(sys.argv) > 1: preview(out, sys.argv[1])
