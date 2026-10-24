"""2.94g: synthesises THE DREAD - the Dread bosses' battle theme (vendor/boss_dread.ogg, a seamless loop) and its music disc
(vendor/disc_dread.ogg, mono, with an ending). The owner's brief: desperate, violin, "something truly wicked - a fight for your
life"; in the spirit of Zero Two's battle (Kirby 64: a tolling, ominous choir and organ) and Partners in Time's final battle
(frantic string ostinatos, urgent stabs). An original piece - neither tune is quoted.

C harmonic minor, 168 BPM (a bar is 10/7 s: 84 bars loop in exactly 120 s).
  bars  0-7   THE TOLLING   organ and choir on C minor and its Neapolitan, a bell on every bar, timpani; a lone violin trembles
  bars  8-23  THE CHASE     sixteenth-note string ostinato, war drums, low brass stabs; the violin's theme (A), twice
  bars 24-39  THE PLEA      the violin climbs (B), the choir behind it; brass doubles it the second time
  bars 40-55  THE WICKED    half-time: organ, chanting choir, timpani, and the violin tearing through harmonic-minor runs; a
                            snare roll builds
  bars 56-71  NO WAY OUT    the theme again, everything at once - violins in octaves, brass, choir
  bars 72-83  THE FALL      B's last phrase, then a chromatic plunge back into the tolling
The disc plays it once, then 7 bars of ending (a final hammered C minor and silence).

THE VIOLIN (violin()): a bowed string built here - a band-limited sawtooth (the bow's stick-slip), a pitch scoop into each note,
a vibrato that only arrives once the note has sounded, the violin body's resonances (a band-pass bank), bow noise, and an
optional bowed tremolo. Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg):
    python3 tools/dread_music.py [loop] [disc] [preview]"""
import os, sys, wave, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, mix, T, env, lp, hp, bp, bell, bass, sub, organ, brass, choir, strings, kick, snare, hat, riser, chord
from boss_music import timp, crash, mel, tp, bars_of, play, drums, save as save_loop
from disc_music import save_mono

BPM, BARS, END = 168, 84, 7


# ------------------------------------------------------------------ the violin
def violin(f, dur, amp=1.0, vib=5.8, depth=0.0065, trem=0.0, scoop=0.012, attack=0.035, bright=1.0, voices=1, seed=0):
    """a bowed violin note (voices > 1: a section, each its own vibrato and a hair apart)"""
    f0 = fq(f); t = T(dur + 0.08); n = len(t)
    rng = np.random.default_rng(int(f0 * 10) + seed)
    out = np.zeros(n)
    for v in range(voices):
        det = 1 + (v - (voices - 1) / 2) * 0.0035
        ph0 = rng.random()
        onset = np.clip((t - 0.12) / 0.25, 0, 1)                             # (vibrato arrives once the note has sounded)
        vb = depth * onset * np.sin(2 * np.pi * (vib + 0.3 * v) * t + ph0 * 6.28)
        sc = -scoop * np.exp(-t / 0.045)                                       # (a scoop up into the pitch)
        jit = 0.0012 * lp(rng.standard_normal(n), 8)
        fr = f0 * det * (1 + vb + sc + jit)
        ph = np.cumsum(fr) / SR + ph0
        K = max(1, int(min(9000, SR / 2 - 500) / f0))
        s = np.zeros(n)
        for k in range(1, K + 1):                                              # (band-limited saw: the bow's stick-slip)
            s += np.sin(2 * np.pi * k * ph) / k * (1.0 if k < 6 else 0.8 ** (k - 6) * bright + (1 - bright) * 0.0)
        out += s
    out /= voices
    body = (bp(out, 260, 520, 2) * 1.1 + bp(out, 700, 1300, 2) * 0.55 + bp(out, 2000, 3600, 2) * 0.9 * bright + bp(out, 4200, 6500, 2) * 0.25 * bright
            + out * 0.18)
    noise = hp(R.noise(n), 2500) * 0.035 * (1 + 3 * np.exp(-t / 0.03))         # (the bow on the string)
    s = body + lp(noise, 8000)
    e = env(n, attack, 0.08, 0.85, 0.07, dur + 0.08)
    swell = 1 + 0.12 * np.clip(t / max(dur, 0.2), 0, 1)                       # (a long note leans in)
    s = s * e * swell
    if trem:
        s *= 0.65 + 0.35 * np.abs(np.sin(np.pi * trem * t))
    return amp * s / 1.6


def vln(x, d, amp=0.42, **k):
    return violin(x, d, amp, **k)


def section(x, d, amp=0.3, **k):
    return violin(x, d, amp, voices=3, depth=0.005, **k)


def runs(tr, t0, notes, amp=0.3, pan=0.25, wet=0.35, dur=0.25):
    """fast detached violin notes (spiccato)"""
    t = t0
    for x in notes:
        tr.add(violin(x, tr.beat * dur * 0.8, amp, attack=0.012, scoop=0.004, depth=0.0), t, pan, 1, wet)
        t += tr.beat * dur
    return t


# ------------------------------------------------------------------ the tunes (original)
A1 = mel('G5:.5 C6:.5 D#6 D6:.5 C6:.5 B5:.5 C6:.5 '
         'G5:2 r:.5 G5:.25 G#5:.25 B5:.5 D6:.5 '
         'D#6:1.5 D6:.5 C6:.5 G#5:.5 C6:.5 D#6:.5 '
         'F6:1.5 D#6:.5 D6 A#5 '
         'G#6 G6:.5 F6:.5 D#6:.5 D6:.5 C6:.5 G#5:.5 '
         'F6 D#6:.5 D6:.5 C6 G#5 '
         'B5:.5 C6:.5 D6:.5 F6:.5 G#6 G6:.5 F6:.5 '
         'G6:.25 F6:.25 D#6:.25 D6:.25 C6:.25 B5:.25 G#5:.25 G5:.25 F5:.25 D#5:.25 D5:.25 B4:.25 G4')
A2 = A1[:-20] + mel('B5:.5 D6:.5 F6:.5 G#6:.5 G6 B5 C6:3 r')
B1 = mel('C7:2 A#6:.5 G#6:.5 G6:.5 G#6:.5 '
         'A#6:2 G#6:.5 G6:.5 F6:.5 D6:.5 '
         'G6:1.5 F6:.5 D6 A#5 '
         'C6:.5 D6:.5 D#6:.5 G6:.5 C7:2 '
         'D#7:1.5 D7:.5 C7 G#6 '
         'D7:1.5 C7:.5 A#6 F6 '
         'B6 C7:.5 D7:.5 F7 D#7:.5 D7:.5 '
         'D7:3 B6:.5 G6:.5')
PROG_A = [('C3', 'm'), ('C3', 'm'), ('G#2', 'M'), ('A#2', 'M'), ('F2', 'm'), ('F2', 'm'), ('G2', 'M'), ('G2', 'M')]
PROG_B = [('G#2', 'M'), ('A#2', 'M'), ('G2', 'm'), ('C3', 'm'), ('G#2', 'M'), ('A#2', 'M'), ('G2', 'M'), ('G2', 'M')]
PROG_T = [('C3', 'm'), ('C#3', 'M'), ('C3', 'm'), ('B2', 'dim')]            # (the tolling: C minor and its Neapolitan)
for _x in (A1, A2, B1):
    assert bars_of(_x) == 8, bars_of(_x)


def ch_of(kind, root):
    if kind == 'dim':
        r = m(root); return [r, r + 3, r + 6]
    return chord(root, kind)


def section_of(bar):
    if bar < 8: return 'toll'
    if bar < 24: return 'chase'
    if bar < 40: return 'plea'
    if bar < 56: return 'wicked'
    if bar < 72: return 'noway'
    if bar < 84: return 'fall'
    return 'end'


def compose(tr, ending=False):
    b16 = lambda bar, i: tr.at(bar, i / 4)
    for bar in range(BARS + (END if ending else 0)):
        sec = section_of(bar)
        if sec == 'toll':
            root, kind = PROG_T[(bar // 2) % 4]
        elif sec in ('chase', 'noway'):
            root, kind = PROG_A[bar % 8]
        elif sec == 'plea':
            root, kind = PROG_B[bar % 8]
        elif sec == 'wicked':
            root, kind = PROG_T[(bar // 2) % 4]
        elif sec == 'fall':
            root, kind = (PROG_B[bar % 8] if bar < 80 else [('G#2', 'M'), ('G2', 'M'), ('G2', 'M'), ('G2', 'M')][bar - 80])
        else:
            root, kind = ('C3', 'm')
        ch = ch_of(kind, root); r = ch[0]
        # ---- the tolling: organ, choir, a bell every bar, timpani, a trembling violin
        if sec == 'toll':
            if bar % 2 == 0:
                tr.add(organ([r - 12] + ch, tr.beat * 8, 0.42), tr.at(bar), 0, 1, 0.6)
                tr.add(choir([x + 12 for x in ch], tr.beat * 8, 0.4, 0.5), tr.at(bar), 0, 1, 0.7)
            tr.add(bell(hz(r + 24), 3.5, 0.2, 2.76, 1.2, 2.6), tr.at(bar), 0.2, 1, 0.6)
            tr.add(timp(r - 12, 0.75), tr.at(bar), 0, 1, 0.4)
            tr.add(timp(r - 12, 0.4), tr.at(bar, 3.5), 0, 1, 0.4)
            tr.add(sub(r - 12, tr.beat * 4, 0.35), tr.at(bar), 0, 1, 0.1)
            tr.add(violin(r + 12 + (3 if bar % 4 >= 2 else 0), tr.beat * 4, 0.2, trem=13, depth=0.003), tr.at(bar), -0.3, 1, 0.5)
            if bar >= 4:                                               # (the ostinato creeps in)
                for i in range(16):
                    tr.add(strings(r + 12 + [0, 1, 0, -1][i % 4], tr.beat * 0.22, 0.05 + 0.02 * (bar - 4), 2200), b16(bar, i), -0.3 if i % 2 else 0.3, 1, 0.3)
            if bar == 7:
                tr.add(riser(tr.beat * 4, 0.3), tr.at(bar), 0, 1, 0.3)
                for i in range(16): tr.add(snare(0.08 + 0.02 * i), b16(bar, i), 0.1, 1, 0.3)
        # ---- the chase and no way out: the ostinato, drums, bass, brass stabs
        if sec in ('chase', 'plea', 'noway', 'fall'):
            osti = [r + 12, r + 13 if kind != 'M' else r + 12, r + 12, r + 11] if sec != 'plea' else [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
            g = 0.15 if sec != 'noway' else 0.18
            for i in range(16):
                tr.add(strings(osti[i % 4], tr.beat * 0.22, g, 2500), b16(bar, i), -0.35 if i % 2 else 0.35, 1, 0.25)
            for i in range(8):
                tr.add(bass(r - 12 + (12 if i % 2 else 0), tr.beat * 0.45, 0.6, 800, 5), tr.at(bar, i / 2), 0, 1, 0.05)
            tr.add(sub(r - 12, tr.beat * 3.9, 0.3), tr.at(bar), 0, 1, 0.05)
            drums(tr, bar, kicks=(0, 0.75, 1.5, 2, 2.75, 3.5) if sec != 'plea' else (0, 1.5, 2, 3.5), snares=(1, 3), hats=[i / 2 for i in range(8)], k=0.85, s=0.55, h=0.1)
            for b in ((0.5, 2.5) if sec != 'plea' else (0,)):
                tr.add(brass([r - 12, r - 5], tr.beat * 0.4, 0.42, 900, 0.01), tr.at(bar, b), -0.15, 1, 0.3)
            if bar % 8 == 0: tr.add(crash(0.3), tr.at(bar), 0.3, 1, 0.35)
            if bar % 4 == 0: tr.add(timp(r - 12, 0.55), tr.at(bar), 0, 1, 0.4)
            if sec in ('plea', 'noway'):
                tr.add(choir([x + 12 for x in ch], tr.beat * 4, 0.26 if sec == 'plea' else 0.3, 0.4), tr.at(bar), 0, 1, 0.6)
            if sec == 'noway' and bar % 2 == 0:
                tr.add(organ([x + 12 for x in ch], tr.beat * 2, 0.16), tr.at(bar), -0.4, 1, 0.5)
        # ---- the wicked: half time, organ, chanting choir, timpani; the violin tears through runs
        if sec == 'wicked':
            if bar % 2 == 0:
                tr.add(organ([r - 12] + ch + [x + 12 for x in ch], tr.beat * 8, 0.4), tr.at(bar), 0, 1, 0.6)
                tr.add(choir([x + 12 for x in ch], tr.beat * 8, 0.46, 0.3), tr.at(bar), 0, 1, 0.7)
            for b in (0, 2.5): tr.add(timp(r - 12, 0.6), tr.at(bar, b), 0, 1, 0.4)
            tr.add(kick(0.75), tr.at(bar), 0, 1, 0.05); tr.add(snare(0.45), tr.at(bar, 2), 0.1, 1, 0.3)
            tr.add(sub(r - 12, tr.beat * 4, 0.4), tr.at(bar), 0, 1, 0.05)
            scale = [0, 2, 3, 5, 7, 8, 11]                              # (C harmonic minor)
            base = m('C5') if kind != 'M' else m('C#5')
            up = [base + scale[i % 7] + 12 * (i // 7) for i in range(14)]
            run_notes = (up + up[::-1][1:3]) if bar % 2 == 0 else (up[::-1][:14] + [up[0], up[2]])
            if bar >= 42:
                runs(tr, tr.at(bar), run_notes[:16], 0.24 + 0.01 * (bar - 42), 0.25 if bar % 2 else -0.15, 0.35)
            if bar >= 52:
                for i in range(16): tr.add(snare(0.1 + 0.02 * (bar - 52) * 4 + 0.005 * i), b16(bar, i), 0.1, 1, 0.3)
            if bar == 55:
                tr.add(riser(tr.beat * 4, 0.35), tr.at(bar), 0, 1, 0.3)
        # ---- the ending (the disc only)
        if sec == 'end':
            if bar == BARS:
                for b in (0, 0.5, 1, 1.5, 2):
                    tr.add(brass([r - 12, r - 5, r], tr.beat * 0.4, 0.5, 1200, 0.01), tr.at(bar, b), 0, 1, 0.3)
                    tr.add(kick(0.9), tr.at(bar, b), 0, 1, 0.05)
                tr.add(organ([r - 12] + ch + [x + 12 for x in ch], tr.beat * 10, 0.5), tr.at(bar, 2), 0, 1, 0.7)
                tr.add(choir([x + 12 for x in ch], tr.beat * 10, 0.5, 0.2), tr.at(bar, 2), 0, 1, 0.7)
                tr.add(violin('C6', tr.beat * 9, 0.4, trem=14), tr.at(bar, 2), 0, 1, 0.5)
                tr.add(timp('C2', 0.9), tr.at(bar, 2), 0, 1, 0.4); tr.add(crash(0.45), tr.at(bar, 2), 0, 1, 0.4)
                tr.add(bell('C7', 5.0, 0.22, 2.76, 0.8, 2.6), tr.at(bar, 2), 0.2, 1, 0.7)
    # ---- the violin's tunes
    play(tr, tr.at(8), A1, lambda x, d: vln(x, d, 0.44), 0.1, 1, 0.35)
    play(tr, tr.at(16), A2, lambda x, d: vln(x, d, 0.44), 0.1, 1, 0.35)
    play(tr, tr.at(24), B1, lambda x, d: vln(x, d, 0.42, depth=0.008), 0.1, 1, 0.4)
    play(tr, tr.at(32), B1, lambda x, d: vln(x, d, 0.42, depth=0.008), 0.1, 1, 0.4)
    play(tr, tr.at(32), tp(B1, -12), lambda x, d: brass([x], d, 0.3, 2400, 0.04), -0.2, 1, 0.4)
    play(tr, tr.at(56), A1, lambda x, d: section(x, d, 0.36), 0.15, 1, 0.35)
    play(tr, tr.at(56), tp(A1, -12), lambda x, d: section(x, d, 0.3), -0.15, 1, 0.35)
    play(tr, tr.at(64), A2, lambda x, d: section(x, d, 0.36), 0.15, 1, 0.35)
    play(tr, tr.at(64), tp(A2, -12), lambda x, d: brass([x], d, 0.32, 2800, 0.03), -0.15, 1, 0.35)
    play(tr, tr.at(72), B1, lambda x, d: vln(x, d, 0.42), 0.1, 1, 0.4)
    # (the plunge back: a chromatic run down into the tolling, in the last bar)
    runs(tr, tr.at(83), [m('G6') - i for i in range(16)], 0.3, 0.1, 0.35)
    return tr


def loop():
    tr = Track('dread', BPM, BARS)
    assert round(tr.seconds) == 120
    return compose(tr)


def disc():
    tr = Track('dread_disc', BPM, BARS + END)
    assert round(tr.seconds) == 130
    return compose(tr, ending=True)


if __name__ == '__main__':
    what = sys.argv[1:] or ['loop', 'disc']
    if 'loop' in what:
        save_loop(loop(), room=2.2)
    if 'disc' in what:
        save_mono(disc(), 'dread', 2.2)
    if 'preview' in what:                                              # (a quick listen: the violin alone, then a phrase)
        tr = Track('violin_test', 120, 4)
        play(tr, 0, mel('C5 D5 D#5 G5 C6:2 B5 G5 D#6:2 D6:.5 C6:.5 B5 C6:4'), lambda x, d: vln(x, d, 0.5), 0, 1, 0.3)
        save_mono(tr, 'violin_test', 1.6)
