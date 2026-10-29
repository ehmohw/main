"""2.98: synthesises THE DREAD SOVEREIGN - the final boss's battle music, one loop per form, the turn between them, its record,
and AUREL, the elegy for the light it was (vendor/boss_sovereign1.ogg, boss_sovereign2.ogg, boss_sovereign3.ogg,
boss_sovereign_turn.ogg, disc_sovereign.ogg, disc_aurel.ogg). An original piece built on THE DREAD (tools/dread_music.py), whose
violin it plays: the Sovereign is the Dread's source, so its music is where the Dread's came from.

THE SOVEREIGN'S MOTIF (S) is the Dread's opening cell (5-1-b3-2-1-7-1: G C Eb D C B C) slowed to a march and sunk a fifth, to
F minor - the key the Dread's C minor is the dominant of - with the Neapolitan the Dread only tolled (its C#) bled into the line
itself (C F Ab Gb F E F). Played fast (S2, phase 2) it falls into the Dread's own rhythm; played slow (S3, phase 3), it is the
whole sky. Aurel's elegy sings the same cell in major (C F A G F E F): before it fell, it was a hymn.

FORM 1 - ARMORED (boss_sovereign1, a 120 s loop). F minor, 72 BPM (36 bars of 10/3 s). Still bound.
  bars  0-7   THE CHAINS     two great bells toll on F minor and its Neapolitan (Gb); a 32-foot organ pedal; a low choir;
                             the chains begin to beat (clanks, rattles, a struck anvil-link, a taiko)
  bars  8-15  THE BOUND      S in the low brass and choir, over the full organ; the chains march
  bars 16-23  THE WEIGHT     S again, heavier; the violin cries the Dread's own head (at the Dread's speed) above it
  bars 24-31  THE CROWN      S at the top: the violins in octaves, the full choir, bells on every half bar
  bars 32-35  THE TOLL       back down into the bells (and round again)
FORM 2 - BROKEN (boss_sovereign2, a 120 s loop). F minor; its three's music in C minor. 176 BPM (88 bars of 15/11 s).
  bars  0-7   THE WINGS      six choir glissandi rise (a wing each), and every eye in them opens (glass pings)
  bars  8-23  BROKEN         a new frantic ostinato, war drums; S2 (S at the Dread's speed) in brass, violin, choir
  bars 24-35  FEAR           the Dread's theme (A) on its own pitches, iced (glass doubling it); then volleys of ice shards
  bars 36-47  HUNGER         the Dread's plea (B), a theremin shadowing it an octave down, hex bolts; then the curse
                             circles (whole-tone clusters) bursting, one after another
  bars 48-59  WAR            the Dread's theme in the low brass, in F minor - the Sawshark's chug and its chomping stabs, a
                             whirlpool of violin runs
  bars 60-79  ALL THREE      the Dread's theme for the whole section in octaves, with ice, hexes and jaws all at once; then
                             S2 over the frantic runs, the wings beating
  bars 80-87  THE WINGS FOLD the glissandi fall (and rise again)
FORM 3 - TRUE (boss_sovereign3, a 120 s loop). F minor, the void, F# minor. 184 BPM (92 bars of 30/23 s).
  bars  0-31  EVERYTHING     S3 (S at half speed) in brass, choir and organ; the chains, the bells, the frantic strings, the
                             violin's runs, double-kick drums, jaws and wings - everything at once; the violins join S3
  bars 32-51  THE VOID       the floor falls into the lava; then hollow - a minor-second drone, a tritone eye that watches,
                             a heartbeat, whispers, the violin alone in ghostly harmonics, the lava popping below; a slow
                             rebuild
  bars 52-67  THE LAST LIGHT S3 a semitone higher, F# minor, everything again, bells on every beat
  bars 68-83  NO WAY OUT     the Dread's theme (A, then its ending) for the violins in octaves, F# minor
  bars 84-91  THE PLUNGE     F# minor hammered; the strings tumble a semitone down to C, the dominant - and round again
THE ENTRANCE (boss_sovereign_intro, 20 s, once, as it rises): six bars of form 1's tempo, ending on form 1's downbeat -
  near-silence (a heartbeat, chains far off), a choir building, the bells, the organ swelling to the dominant, THE ROAR at
  16.7 s, then form 1's own last bar (the Neapolitan, a snare roll, a riser) so the loop follows as if from itself.
THE TURN (boss_sovereign_turn, 8 s, once, between forms): the chains snap, six wings unfurl in a choir glissando, the bell, the
  Dread's head cried by the violin, a timpani and snare roll to the brink; the last second silence.
THE RECORD (disc_sovereign, mono, ~3 min): the three forms condensed, with both turns, and an ending - F# minor hammered, the
  bell, and very faintly, a violin on a major third (Aurel, listening).
AUREL (disc_aurel, mono, 2 min): an elegy. A solo violin over a soft (flute-stop) organ, 3/4, 66 BPM, D minor turning to F
  major; it climbs once, grieves through the minor iv (Bb minor), and comes to rest on F major.

Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg):
    python3 tools/sovereign_music.py [p1] [p2] [p3] [turn] [intro] [disc] [aurel] [check]"""
import os, sys, wave, subprocess, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, mix, T, env, lp, hp, bp, bell, bass, sub, organ, brass, choir, strings, kick, snare, hat, riser
from boss_music import timp, crash, mel, tp, bars_of, tom, theremin, thunder
from disc_music import save_mono
from dread_music import violin, vln, section, cello, heart, A1, A2, B1

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
P1BPM, P1BARS = 72, 36
P2BPM, P2BARS = 176, 88
P3BPM, P3BARS = 184, 92
ABPM, ABARS = 66, 44


# ====================================================================== instruments (mono)
def great_bell(f, dur=7.0, amp=1.0, bright=1.0, seed=0):
    """a tolling church bell: its partials (hum, prime, the minor-third tierce, quint, nominal...) each a pair a hair apart
    (the slow beating of a cast bell), dying at their own rates; the clapper's strike"""
    f0 = fq(f); t = T(dur); n = len(t)
    g = np.random.default_rng(int(f0 * 7) + seed)
    s = np.zeros(n)
    for ratio, a, dec in ((0.5, 1.0, 0.28), (1.0, 0.85, 0.45), (1.2, 0.75, 0.6), (1.5, 0.45, 0.8), (2.0, 0.7, 1.0),
                          (2.5, 0.3, 1.5), (2.67, 0.28, 1.7), (3.0, 0.25 * bright, 2.1), (4.2, 0.2 * bright, 2.9), (5.4, 0.12 * bright, 3.8)):
        fk = f0 * ratio
        if fk > SR / 2 - 600: continue
        b = 1 + 0.0012 + 0.0008 * g.random()
        s += a * (np.sin(2 * np.pi * fk * t + 6.28 * g.random()) + 0.6 * np.sin(2 * np.pi * fk * b * t)) * np.exp(-t * dec * (0.7 + f0 / 900))
    s += bp(R.noise(n), min(f0 * 3, 4000), min(f0 * 10, 9000)) * np.exp(-t * 45) * 1.2
    return amp * s * env(n, 0.002, 0, 1, 0.4) / 3.2


def clank(amp=1.0, f=1500.0, ring=1.0, seed=0):
    """struck iron: the free bar's inharmonic modes (1 : 2.76 : 5.40 : 8.93 : 13.3), a hard click"""
    g = np.random.default_rng(seed)
    t = T(0.08 + 0.5 * ring); n = len(t)
    s = np.zeros(n)
    for ratio, a, dec in ((1.0, 1.0, 7), (2.756, 0.75, 10), (5.404, 0.5, 14), (8.933, 0.32, 20), (13.34, 0.18, 28)):
        fk = f * ratio * (1 + 0.012 * g.standard_normal())
        if fk > SR / 2 - 400: continue
        s += a * np.sin(2 * np.pi * fk * t + 6.28 * g.random()) * np.exp(-t * dec / ring)
    s += hp(R.noise(n), 2500) * np.exp(-t * 90) * 0.9
    return amp * s * env(n, 0.0005, 0, 1, 0.03) / 2.2


def rattle(dur, amp=1.0, density=40, seed=0, fall=False):
    """a chain shaken (or falling): links clinking against links, thinning out"""
    g = np.random.default_rng(seed)
    out = np.zeros(int((dur + 0.6) * SR))
    k = max(1, int(dur * density))
    for i in range(k):
        u = g.random() ** (1.6 if fall else 1.0)
        t0 = u * dur
        a = (1 - u) ** (0.6 if fall else 0.2) * g.uniform(0.25, 1.0)
        c = clank(a, g.uniform(1300, 4200) * (1 - 0.35 * u if fall else 1), g.uniform(0.15, 0.4), seed * 977 + i)
        j = int(t0 * SR); out[j:j + len(c)] += c[:len(out) - j]
    return amp * out


def chain_hit(amp=1.0, seed=0, links=6, heavy=True):
    """the chains as a drum: a great link struck (an anvil's ring), its links jangling after it, and a deep thud under it"""
    g = np.random.default_rng(seed + 11)
    out = np.zeros(int(1.4 * SR))
    if heavy:
        th = tom(48, 1.0, 4.5, 0.6); out[:len(th)] += th * 0.9
    c = clank(1.0, g.uniform(330, 470), 2.2, seed); out[:len(c)] += c * 1.2
    t0 = 0.012
    for i in range(links):
        t0 += g.uniform(0.012, 0.045)
        c = clank(g.uniform(0.25, 0.55) * (1 - i / (links + 1)), g.uniform(1500, 3800), g.uniform(0.2, 0.35), seed * 131 + i)
        j = int(t0 * SR); out[j:j + len(c)] += c[:len(out) - j]
    return amp * out


def taiko(amp=1.0, f=42):
    return tom(f, amp, 3.2, 0.7)


VOWEL = {'a': ((650, 1100, 1.4), (1050, 1500, 0.7), (2300, 3000, 0.25)),
         'o': ((330, 620, 1.7), (650, 1000, 0.75), (2300, 2900, 0.12)),
         'u': ((240, 450, 1.6), (520, 850, 0.45), (2200, 2800, 0.06))}


def formant(s, vowel):
    return sum(bp(s, f1, f2, 1) * g for f1, f2, g in VOWEL[vowel])


def chorus(notes, dur, amp=1.0, attack=0.8, vowel='o', vib=4.8):
    """a choir on a vowel - 'o' and 'u' for the low monks, 'a' for the full choir"""
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in (-0.008, -0.003, 0.002, 0.007):
            fr = f * (1 + v) * (1 + 0.006 * np.sin(2 * np.pi * (vib + v * 90) * t + R.r() * 6.28))
            ph = np.cumsum(fr) / SR + R.r()
            s += 2 * (ph % 1) - 1
    s /= len(notes) * 4
    return amp * formant(s, vowel) * env(len(t), attack, 0, 1, 0.9)


def wing(f0, f1, dur, amp=1.0, hold=0.35, vowel='a'):
    """one wing: a choir voice sliding from f0 to f1 (an eased glissando), then holding"""
    a, b = fq(f0), fq(f1)
    t = T(dur); n = len(t)
    u = np.clip(t / (dur * (1 - hold)), 0, 1); sh = (1 - np.cos(np.pi * u)) / 2
    path = a * (b / a) ** sh
    s = np.zeros(n)
    for v in (-0.009, -0.003, 0.003, 0.009):
        fr = path * (1 + v) * (1 + 0.008 * np.sin(2 * np.pi * (5.2 + v * 60) * t))
        ph = np.cumsum(fr) / SR + R.r()
        s += 2 * (ph % 1) - 1
    return amp * formant(s / 4, vowel) * env(n, 0.25, 0, 1, min(0.8, dur * 0.3))


def great_organ(notes, dur, amp=1.0, attack=0.12, mixture=1.0):
    """the full organ: a 16-foot under each note, the 8', 4', 2 2/3', 2' and a mixture, two ranks a hair apart (the
    chorus of a big instrument), a slow pipe speech"""
    t = T(dur); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = hz(x)
        for k, a in ((0.5, 0.65), (1, 1.0), (2, 0.65), (3, 0.38), (4, 0.32), (6, 0.2 * mixture), (8, 0.14 * mixture), (10, 0.07 * mixture), (12, 0.06 * mixture)):
            fk = f * k
            if fk < 28 or fk > SR / 2 - 600: continue
            s += a * (np.sin(2 * np.pi * fk * t) + 0.7 * np.sin(2 * np.pi * fk * 1.0021 * t + 1.3))
    s *= 1 + 0.06 * np.sin(2 * np.pi * 5.6 * t)
    return amp * s / (len(notes) * 4.2) * env(n, attack, 0, 1, 0.25)


def soft_organ(notes, dur, amp=1.0, attack=0.9, release=1.2):
    """a quiet flute stop (8' and a little 4'), breathing - for Aurel"""
    t = T(dur); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = hz(x)
        s += np.sin(2 * np.pi * f * t + R.r() * 6) + 0.22 * np.sin(4 * np.pi * f * t) + 0.05 * np.sin(6 * np.pi * f * t)
        s += 0.4 * np.sin(2 * np.pi * f * 1.0017 * t + 0.7)
    s *= 1 + 0.04 * np.sin(2 * np.pi * 4.8 * t)
    s += lp(R.noise(n), 1800) * 0.015 * len(notes)                          # (wind in the pipes)
    return amp * s / (len(notes) * 1.6) * env(n, attack, 0, 1, release)


def glass(f, dur=1.2, amp=1.0):
    """ice: a glassy, high, short bell"""
    return mix(bell(f, dur, amp, 3.99, 3.2, 0.9), bell(fq(f) * 2.01, dur * 0.6, amp * 0.25, 2.0, 5.0, 0.4))


def boom(amp=1.0, f0=90.0, f1=28.0, dur=2.5):
    """a vast impact: a sine falling away under a thud"""
    t = T(dur)
    fr = f1 + (f0 - f1) * np.exp(-t * 2.2)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 1.3)
    s += lp(R.noise(len(t)), 300) * np.exp(-t * 7) * 1.5
    return amp * s * env(len(t), 0.003, 0, 1, 0.3)


def pop(amp=1.0, f=70.0):
    """lava, far below: a thick bubble bursting"""
    t = T(0.35)
    fr = f * (1 + 1.5 * np.exp(-t * 30))
    return amp * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 14) * env(len(t), 0.006, 0, 1, 0.05)


def drone(notes, dur, amp=1.0, beat=0.35):
    """the void: bare sines, beating, swelling and ebbing"""
    t = T(dur); n = len(t)
    s = np.zeros(n)
    for i, x in enumerate(notes):
        f = fq(x)
        s += np.sin(2 * np.pi * f * t + i) * (0.75 + 0.25 * np.sin(2 * np.pi * (0.13 + 0.07 * i) * t + i))
        s += 0.5 * np.sin(2 * np.pi * (f + beat * (1 + i)) * t)
    return amp * s / len(notes) * env(n, 2.0, 0, 1, 2.0)


def gaze(f, dur, amp=1.0):
    """the eye: a high, pure tone and its tritone, a slow, wide waver - something watching"""
    f = fq(f); t = T(dur); n = len(t)
    w = 1 + 0.01 * np.sin(2 * np.pi * 0.6 * t)
    s = np.sin(2 * np.pi * np.cumsum(f * w) / SR) + 0.55 * np.sin(2 * np.pi * np.cumsum(f * 2 ** 0.5 * w[::-1]) / SR)
    s *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t) ** 2
    return amp * s * env(n, dur * 0.4, 0, 1, dur * 0.4)


def whisper(dur, amp=1.0, seed=0):
    """breath shaped into syllables - the voice under the Nether"""
    g = np.random.default_rng(seed)
    t = T(dur); n = len(t)
    nz = R.noise(n)
    s = np.zeros(n)
    k = max(1, int(dur * 3.5))
    for i in range(k):
        f1 = g.uniform(500, 2600)
        c = bp(nz, f1, f1 * 1.5) * np.exp(-((t - g.uniform(0, dur)) / g.uniform(0.06, 0.18)) ** 2)
        s += c * g.uniform(0.4, 1.0)
    return amp * hp(s, 400) * env(n, 0.2, 0, 1, 0.3)


def edge(s, sec=0.025):
    """the last moment of a swell faded, so it stops without a click"""
    k = min(len(s), int(sec * SR)); s = s.copy(); s[-k:] *= np.linspace(1, 0, k)
    return s


def suck(dur=1.5, amp=1.0):
    """a reversed cymbal - the air drawn in before the blow"""
    t = T(dur)
    s = hp(R.noise(len(t)), 3000) * np.exp(-t * 2.4)
    return edge(amp * s[::-1] * 0.8)


def rise(dur, amp=1.0):
    return edge(riser(dur, amp))


def chomp(tr, t, r, amp=1.0, pan=0.0):
    """the Sawshark's jaws: a low brass bark, a timpani, iron on iron"""
    tr.add(brass([r - 24, r - 17, r - 12], 0.24, 0.55 * amp, 1500, 0.004), t, pan, 1, 0.25)
    tr.add(timp(r - 24, 0.5 * amp), t, 0, 1, 0.3)
    tr.add(clank(0.35 * amp, 620, 0.6, int(t * 100)), t, pan, 1, 0.3)


def wings(tr, t, ch, dur, amp=0.18, up=True, lo=-17):
    """six wings: six choir glissandi, a moment apart, from far below the chord up onto it (or from it, down)"""
    targets = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24, ch[1] + 24, ch[2] + 24]
    for i, x in enumerate(targets):
        a, b = (x + lo - (i % 3), x) if up else (x, x + lo - (i % 3))
        tr.add(wing(hz(a), hz(b), dur - 0.1 * i, amp * (1 - 0.06 * i)), t + 0.1 * i, (-0.7 + 0.28 * i), 1, 0.6)


def eyes(tr, t, dur, ch, k, amp=0.1, seed=0, lift=36):
    """every eye opening: glass pings, scattered"""
    g = np.random.default_rng(seed)
    for i in range(k):
        x = ch[g.integers(len(ch))] + lift + 12 * g.integers(2)
        tr.add(glass(x, 0.9, amp * g.uniform(0.5, 1.0)), t + g.random() * dur, g.uniform(-0.85, 0.85), 1, 0.6)


# ====================================================================== the tunes
S = mel('C4:2 F4:2 Ab4:3 Gb4:1 F4:2 E4:2 F4:4 Db5:2 C5:2 Bb4:2 Ab4:1 Gb4:1 F4:2 E4:1 Db4:1 C4:4')   # (the Sovereign: 8 bars)
DREAD_HEAD = mel('C6:.25 F6:.25 Ab6:.5 G6:.25 F6:.25 E6:.25 F6:.25')     # (the Dread's first bar in F minor, at the Dread's speed)


def dur_x(notes, k):
    return [(x, d * k) for x, d in notes]


S2 = dur_x(S, 0.5)                         # (4 bars: the Dread's rhythm)
S3 = dur_x(S, 2.0)                         # (16 bars: the sky)
IV = {'m': (0, 3, 7), 'M': (0, 4, 7), 'dim': (0, 3, 6), '7': (0, 4, 7, 10), '7b9': (0, 4, 7, 10, 13), 'm7': (0, 3, 7, 10),
      'M7': (0, 4, 7, 11), 'sus': (0, 5, 7), 'hd': (0, 3, 6, 10), 'wt': (0, 2, 4, 6, 8, 10)}


def chd(root, kind, k=0):
    r = (m(root) if isinstance(root, str) else root) + k
    return [r + i for i in IV[kind]]


PROG_S = [('F2', 'm'), ('Db2', 'M'), ('C2', 'M'), ('F2', 'm'), ('Db2', 'M'), ('Gb2', 'M'), ('C2', '7b9'), ('C2', 'M')]
PROG_T = [('F2', 'm'), ('Gb2', 'M'), ('F2', 'm'), ('E2', 'dim')]          # (the tolling: F minor and its Neapolitan)
PROG_A = [('C3', 'm'), ('C3', 'm'), ('G#2', 'M'), ('A#2', 'M'), ('F2', 'm'), ('F2', 'm'), ('G2', 'M'), ('G2', 'M')]    # (the Dread's)
PROG_B = [('G#2', 'M'), ('A#2', 'M'), ('G2', 'm'), ('C3', 'm'), ('G#2', 'M'), ('A#2', 'M'), ('G2', 'M'), ('G2', 'M')]
for _x in (S,):
    assert bars_of(_x) == 8, bars_of(_x)
assert bars_of(S2) == 4 and bars_of(S3) == 16


class View:
    """a stretch of a piece, written into a Track: its own tempo, and (for the record) only the bars of a window, placed at t0"""
    def __init__(self, tr, bpm, beats=4, t0=0.0, win=None):
        self.tr, self.bpm, self.beats, self.t0, self.win = tr, bpm, beats, t0, win
        self.beat = 60.0 / bpm; self.barlen = self.beat * beats; self.name = tr.name

    def at(self, bar, beat=0.0):
        return self.t0 + ((bar - (self.win[0] if self.win else 0)) * self.beats + beat) * self.beat

    def want(self, bar):
        return self.win is None or self.win[0] <= bar < self.win[1]

    def ok(self, t):
        if self.win is None: return True
        return self.t0 - 1e-6 <= t < self.t0 + (self.win[1] - self.win[0]) * self.barlen - 1e-6

    def add(self, sig, t, pan=0.0, gain=1.0, wet=0.3):
        if self.ok(t): self.tr.add(sig, t, pan, gain, wet)

    @property
    def span(self):
        return (self.win[1] - self.win[0]) * self.barlen


def ply(tr, t0, notes, inst, pan=0.0, gain=1.0, wet=0.3, legato=0.95):
    """play a line (only the notes a window keeps are synthesised)"""
    t = t0
    for x, d in notes:
        if x is not None and tr.ok(t): tr.add(inst(x, d * tr.beat * legato), t, pan, gain, wet)
        t += d * tr.beat
    return t


def runs(tr, t0, notes, amp=0.3, pan=0.25, wet=0.35, dur=0.25):
    """fast detached violin notes (spiccato)"""
    t = t0
    for x in notes:
        if tr.ok(t): tr.add(violin(x, tr.beat * dur * 0.8, amp, attack=0.012, scoop=0.004, depth=0.0), t, pan, 1, wet)
        t += tr.beat * dur
    return t


def ladder(ch, lo, k):
    """the chord's tones, climbing from lo (k of them)"""
    pcs = {x % 12 for x in ch}
    out = []; x = lo
    while len(out) < k:
        if x % 12 in pcs: out.append(x)
        x += 1
    return out


def frantic(ch, bar, lo=m('F5')):
    """a bar of the violin's frantic sixteenths over a chord: up and back, or down and back"""
    up = ladder(ch, lo - 7, 9)
    shape = [0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1] if bar % 2 == 0 else [8, 7, 6, 5, 4, 3, 2, 1, 0, 2, 1, 3, 2, 4, 3, 5]
    return [up[i] for i in shape]


HM = [0, 2, 3, 5, 7, 8, 11]                                                   # (harmonic minor)


def scale_run(tonic, k, up=True):
    out = [tonic + HM[i % 7] + 12 * (i // 7) for i in range(k)]
    return out if up else out[::-1]


# ====================================================================== FORM 1: ARMORED
def p1_chord(bar):
    if bar < 8 or bar >= 32: return chd(*PROG_T[(bar // 2) % 4])
    return chd(*PROG_S[bar % 8])


def p1_compose(tr, bars=range(P1BARS)):
    for bar in bars:
        if not tr.want(bar): continue
        ch = p1_chord(bar); r = ch[0]
        sec = 'toll' if (bar < 8 or bar >= 32) else 'bound' if bar < 16 else 'weight' if bar < 24 else 'crown'
        g = {'toll': 0.75, 'bound': 0.9, 'weight': 1.0, 'crown': 1.1}[sec]
        # ---- the bells: the great bell on every bar, the second bell answering
        tr.add(great_bell(hz(m('F3') if r % 12 == 5 else r + 12), 7.0, 0.55 * g, 1.0, bar), tr.at(bar), -0.15, 1, 0.55)
        if bar % 2 == 1 or sec == 'crown':
            tr.add(great_bell(hz(ch[2] + 24), 5.0, 0.28 * g, 1.2, bar + 50), tr.at(bar, 2), 0.35, 1, 0.6)
        if sec == 'crown':
            for b in (1, 3): tr.add(great_bell(hz(ch[1] + 36), 3.0, 0.14, 1.3, bar * 3 + b), tr.at(bar, b), 0.5, 1, 0.6)
        # ---- the organ: a 32-foot pedal, the chord above it
        if sec == 'toll':
            if bar % 2 == 0:
                tr.add(great_organ([r - 12, r] + ch[1:], tr.beat * 8, 0.42, 0.6, 0.4), tr.at(bar), 0, 1, 0.6)
        else:
            tr.add(great_organ([r - 12, r] + [x + 12 for x in ch], tr.beat * 4, 0.42 * g, 0.08, 0.6 + 0.4 * (sec == 'crown')), tr.at(bar), 0, 1, 0.55)
        tr.add(sub(r - 12, tr.beat * 3.9, 0.35), tr.at(bar), 0, 1, 0.05)
        # ---- the low choir: monks, 'oo', then 'oh'; the full choir at the crown
        if sec == 'toll' and bar >= 2 and bar % 2 == 0:
            tr.add(chorus([r, ch[2], r + 12], tr.beat * 8, 0.32, 1.2, 'u'), tr.at(bar), 0, 1, 0.7)
        elif sec in ('bound', 'weight'):
            tr.add(chorus([r, ch[1], ch[2], r + 12], tr.beat * 4, 0.32 if sec == 'bound' else 0.38, 0.4, 'o'), tr.at(bar), 0, 1, 0.65)
        elif sec == 'crown':
            tr.add(chorus([x + 12 for x in ch] + [r + 24], tr.beat * 4, 0.42, 0.3, 'a'), tr.at(bar), 0, 1, 0.65)
            tr.add(chorus([r, ch[2]], tr.beat * 4, 0.28, 0.3, 'o'), tr.at(bar), 0, 1, 0.6)
        # ---- the chains: a struck link and a taiko on the 1 and the 3, links dragged between, timpani
        if bar >= 2:
            hv = sec != 'toll' or (2 <= bar < 8)
            tr.add(chain_hit(0.7 * g, bar * 4, 7), tr.at(bar), -0.1, 1, 0.4)
            tr.add(taiko(0.75 * g), tr.at(bar), 0, 1, 0.35)
            tr.add(timp(r - 12, 0.55 * g), tr.at(bar), 0, 1, 0.4)
            if hv:
                tr.add(chain_hit(0.52 * g, bar * 4 + 1, 5), tr.at(bar, 2), 0.15, 1, 0.4)
                tr.add(taiko(0.5 * g, 48), tr.at(bar, 2), 0, 1, 0.35)
                tr.add(clank(0.42 * g, 1700 + 80 * (bar % 4), 0.4, bar * 9 + 2), tr.at(bar, 1.5), 0.45, 1, 0.4)
                tr.add(rattle(tr.beat * 0.9, 0.32 * g, 30, bar * 9 + 3), tr.at(bar, 3), -0.4, 1, 0.45)
                tr.add(clank(0.38 * g, 2100, 0.3, bar * 9 + 4), tr.at(bar, 3.5), 0.3, 1, 0.4)
                tr.add(clank(0.3 * g, 1900, 0.3, bar * 9 + 5), tr.at(bar, 3.75), -0.3, 1, 0.4)
            if sec in ('weight', 'crown'):
                for b in (1, 3): tr.add(snare(0.4, 160), tr.at(bar, b), 0.1, 1, 0.45)
                for b in (0.5, 1, 2.5, 3): tr.add(tom(70, 0.32, 7, 0.3), tr.at(bar, b), -0.2, 1, 0.3)
            if sec == 'crown':
                for b in (1.5, 3.5): tr.add(timp(r - 12, 0.4), tr.at(bar, b), 0, 1, 0.4)
                if bar % 4 == 0: tr.add(crash(0.32), tr.at(bar), 0.3, 1, 0.45)
        elif bar < 2:                                                        # (the first bars: a chain somewhere, dragged)
            tr.add(rattle(tr.beat * 3, 0.16, 12, bar + 700), tr.at(bar, 0.5), 0.5 - bar, 1, 0.6)
        # ---- the bound's walking bass: the low brass under S
        if sec != 'toll':
            for b in (0, 2):
                tr.add(brass([r - 12], tr.beat * 1.8, 0.28 * g, 700, 0.05), tr.at(bar, b), 0, 1, 0.3)
        # ---- the toll's trembling violin, alone (and a cry of the Dread's head as the chains begin)
        if sec == 'toll':
            tr.add(violin(r + 24 + (1 if bar % 4 >= 2 else 0), tr.beat * 4, 0.16, trem=11, depth=0.003), tr.at(bar), 0.3, 1, 0.55)
        if bar in (7, 35):
            tr.add(rise(tr.beat * 4, 0.22), tr.at(bar), 0, 1, 0.35)
            for i in range(16): tr.add(snare(0.06 + 0.02 * i, 170), tr.at(bar, i / 4), 0.1, 1, 0.4)
        if bar == 31:
            tr.add(suck(tr.beat * 2, 0.4), tr.at(bar, 2), 0, 1, 0.3)
        if sec == 'weight' and bar % 8 in (0, 3):                             # (the violin cries the Dread's own head: Fm bars)
            ply(tr, tr.at(bar, 2), DREAD_HEAD, lambda x, d: vln(x, d, 0.4), 0.15, 1, 0.45)
        if sec == 'weight' and bar % 8 in (6, 7):                             # (and holds its leading tone over the dominant)
            tr.add(violin(m('E6'), tr.beat * 3.8, 0.3, trem=12, depth=0.004), tr.at(bar), 0.15, 1, 0.5)
    # ---- S: the Sovereign's motif
    lo_brass = lambda x, d: brass([x], d, 0.42, 1500, 0.08)
    ply(tr, tr.at(8), tp(S, -12), lo_brass, -0.1, 1, 0.45)
    ply(tr, tr.at(8), S, lambda x, d: chorus([x], d + 0.2, 0.3, 0.15, 'o'), 0.1, 1, 0.55)
    ply(tr, tr.at(16), tp(S, -12), lambda x, d: brass([x, x + 12], d, 0.46, 1900, 0.06), -0.1, 1, 0.45)
    ply(tr, tr.at(16), tp(S, -24), lambda x, d: brass([x], d, 0.3, 900, 0.08), 0, 1, 0.35)
    ply(tr, tr.at(16), S, lambda x, d: chorus([x], d + 0.2, 0.32, 0.12, 'o'), 0.1, 1, 0.55)
    ply(tr, tr.at(24), tp(S, 12), lambda x, d: section(x, d, 0.4, attack=0.05), 0.2, 1, 0.45)
    ply(tr, tr.at(24), S, lambda x, d: section(x, d, 0.32, attack=0.05), -0.2, 1, 0.45)
    ply(tr, tr.at(24), tp(S, -12), lambda x, d: brass([x, x + 12], d, 0.5, 2300, 0.05), 0, 1, 0.45)
    ply(tr, tr.at(24), tp(S, 12), lambda x, d: chorus([x], d + 0.2, 0.3, 0.1, 'a'), 0, 1, 0.55)
    return tr


def p1():
    tr = Track('sovereign1', P1BPM, P1BARS)
    assert round(tr.seconds) == 120
    p1_compose(View(tr, P1BPM))
    return tr


# ====================================================================== FORM 2: BROKEN
S2_PROG = [('F2', 'm'), ('Db2', 'M'), ('C2', 'M'), ('F2', 'm'), ('Db2', 'M'), ('Gb2', 'M'), ('C2', '7b9'), ('C2', 'M')]   # (a half-bar each)


def p2_sec(bar):
    for lim, nm in ((8, 'wings'), (24, 'broken'), (36, 'fear'), (48, 'hunger'), (60, 'war'), (80, 'all'), (88, 'fold')):
        if bar < lim: return nm
    return 'end'


def p2_chord(bar, half=0):
    sec = p2_sec(bar)
    if sec == 'wings': return chd(*([PROG_T[0]] * 4 + [PROG_T[1]] * 2 + [('C2', 'M')] * 2)[bar])
    if sec == 'fold': return chd(*([PROG_T[0]] * 2 + [PROG_T[1]] * 2 + [PROG_T[0]] * 2 + [('C2', '7b9'), ('C2', 'M')])[bar - 80])
    if sec == 'broken' or (sec == 'all' and 68 <= bar < 76):
        return chd(*S2_PROG[((bar % 4) * 2 + half) % 8])
    if sec == 'fear':
        if bar < 32: return chd(*PROG_A[bar - 24])
        return chd(*[('C3', 'm'), ('C#3', 'M')][bar % 2])
    if sec == 'hunger':
        if bar < 44: return chd(*PROG_B[bar - 36])
        if bar < 47: return chd('C3', 'wt')
        return chd('C2', '7')
    if sec == 'war':
        if bar < 56: return chd(*PROG_A[bar - 48], k=5 - 12 * (PROG_A[bar - 48][0][-1] == '3'))
        return chd(*PROG_T[((bar - 56) // 2) % 2])
    if sec == 'all':
        if bar < 68: return chd(*PROG_A[bar - 60], k=5 - 12 * (PROG_A[bar - 60][0][-1] == '3'))
        return chd(*[('Db2', 'M'), ('Gb2', 'M'), ('C2', '7b9'), ('C2', 'M')][bar - 76])
    return chd('F2', 'm')


def osti(ch, kind):
    """the new frantic ostinato: sawing at the root with the fifth and the third flung between"""
    r = ch[0] + 12
    return [r + 12, ch[2] + 12, r + 12, ch[1] + 12, r + 12, ch[2] + 12, ch[1] + 24, ch[2] + 12]


def p2_compose(tr, bars=range(P2BARS)):
    g16 = lambda bar, i: tr.at(bar, i / 4)
    for bar in bars:
        if not tr.want(bar): continue
        sec = p2_sec(bar)
        ch = p2_chord(bar); r = ch[0]
        tri = ch[:3]
        # ---- the strings: tremolo in the wings, the frantic ostinato everywhere else (icy in fear, trembling in hunger)
        if sec in ('wings', 'fold'):
            for i in range(16):
                tr.add(strings(r + 24 + (0 if i % 2 == 0 else 1 if sec == 'wings' else 0), tr.beat * 0.22, 0.09 + 0.012 * (bar % 8), 2400), g16(bar, i), -0.35 if i % 2 else 0.35, 1, 0.35)
        elif sec == 'hunger':
            for i in range(16):
                tr.add(strings(tri[i % 3] + 24, tr.beat * 0.22, 0.1, 2000), g16(bar, i), -0.4 if i % 2 else 0.4, 1, 0.4)
        else:
            for half in (0, 1):
                c = p2_chord(bar, half)
                pat = osti(c, sec)
                for i in range(8):
                    k = half * 8 + i
                    tr.add(strings(pat[i] + (12 if sec == 'fear' else 0), tr.beat * 0.22, 0.16 if sec != 'fear' else 0.11, 2600 if sec != 'fear' else 4200),
                           g16(bar, k), -0.35 if k % 2 else 0.35, 1, 0.25)
        # ---- bass and sub
        if sec not in ('wings', 'hunger', 'fold') or bar % 8 >= 4:
            for i in range(8):
                c = p2_chord(bar, i // 4)
                tr.add(bass(c[0] - 12 + (12 if i % 2 else 0), tr.beat * 0.45, 0.55, 800, 5), tr.at(bar, i / 2), 0, 1, 0.05)
        tr.add(sub(r - 12, tr.beat * 3.9, 0.32), tr.at(bar), 0, 1, 0.05)
        # ---- the organ and the choir
        if sec in ('wings', 'fold') and bar % 4 == 0:
            tr.add(great_organ([r - 12, r] + [x + 12 for x in tri], tr.beat * 16, 0.36, 0.4, 0.6), tr.at(bar), 0, 1, 0.6)
        if sec in ('broken', 'all', 'war') and bar % 2 == 0:
            tr.add(great_organ([r] + [x + 12 for x in tri], tr.beat * 8, 0.2), tr.at(bar), -0.3, 1, 0.5)
        if sec == 'fear' and bar % 2 == 0:
            tr.add(chorus([x + 24 for x in tri], tr.beat * 8, 0.24, 0.6, 'u'), tr.at(bar), 0, 1, 0.7)
        if sec == 'hunger' and bar % 2 == 0:
            tr.add(chorus([x + 12 for x in tri], tr.beat * 8, 0.26, 0.8, 'o'), tr.at(bar), 0, 1, 0.7)
            tr.add(whisper(tr.beat * 6, 0.18, bar), tr.at(bar, 1), 0.6 * (1 if bar % 4 else -1), 1, 0.6)
        if sec in ('all',) or (sec == 'broken' and bar >= 16):
            tr.add(chorus([x + 12 for x in tri], tr.beat * 4, 0.26, 0.3, 'a'), tr.at(bar), 0, 1, 0.6)
        # ---- the drums
        if sec == 'wings':
            if bar >= 4:
                drums_ = ((0, 2), (), ()) if bar < 6 else ((0, 1, 2, 3), (1, 3), ())
                for b in drums_[0]: tr.add(kick(0.8), tr.at(bar, b), 0, 1, 0.05)
                for b in drums_[1]: tr.add(snare(0.45), tr.at(bar, b), 0.1, 1, 0.3)
                for b in (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5): tr.add(tom(80 + 10 * (b % 1 > 0), 0.3, 7, 0.3), tr.at(bar, b), -0.3, 1, 0.3)
            tr.add(timp(r - 12, 0.5), tr.at(bar), 0, 1, 0.4)
        elif sec == 'fold':
            for b in (0, 2): tr.add(kick(0.8), tr.at(bar, b), 0, 1, 0.05)
            tr.add(snare(0.5), tr.at(bar, 3), 0.1, 1, 0.3)
            for b in range(8): tr.add(hat(0.08), tr.at(bar, b / 2), 0.4, 1, 0.1)
            tr.add(timp(r - 12, 0.5), tr.at(bar), 0, 1, 0.4)
        elif sec == 'fear':
            for b in (0, 1.5, 2): tr.add(kick(0.75), tr.at(bar, b), 0, 1, 0.05)
            tr.add(snare(0.5), tr.at(bar, 3), 0.1, 1, 0.35)
            for i in range(16): tr.add(hat(0.05 + 0.04 * (i % 4 == 0)), g16(bar, i), 0.5 - (i % 2), 1, 0.2)
        elif sec == 'hunger':
            for b in (0, 2.5): tr.add(kick(0.85), tr.at(bar, b), 0, 1, 0.05)
            tr.add(snare(0.55), tr.at(bar, 2), 0.1, 1, 0.4)
            for i in range(16): tr.add(hat(0.05), g16(bar, i), 0.4, 1, 0.1)
            if bar % 2 == 0: tr.add(timp(r - 12, 0.45), tr.at(bar), 0, 1, 0.4)
        else:                                                               # (broken, war, all: the war drums)
            ks = (0, 0.75, 1.5, 2, 2.75, 3.5) if sec != 'war' else (0, 0.5, 0.75, 1.5, 2, 2.5, 2.75, 3.5)
            for b in ks: tr.add(kick(0.85), tr.at(bar, b), 0, 1, 0.05)
            for b in (1, 3): tr.add(snare(0.58), tr.at(bar, b), 0.1, 1, 0.3)
            for b in range(8): tr.add(hat(0.1), tr.at(bar, b / 2), 0.4, 1, 0.1)
            if sec in ('war', 'all'):
                for b in (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5): tr.add(tom(72 if b % 1 else 58, 0.32, 7, 0.3), tr.at(bar, b), -0.3, 1, 0.3)
            if bar % 4 == 0: tr.add(timp(r - 12, 0.55), tr.at(bar), 0, 1, 0.4)
            if bar % 8 == 0: tr.add(crash(0.3), tr.at(bar), 0.3, 1, 0.35)
            for b in (0.5, 2.5) if sec != 'war' else ():
                tr.add(brass([r - 12, r - 5], tr.beat * 0.4, 0.36, 900, 0.01), tr.at(bar, b), -0.15, 1, 0.3)
        # ---- the wings, and the eyes in them
        if sec == 'wings' and bar == 0:
            wings(tr, tr.at(0), chd('F2', 'm'), tr.barlen * 4, 0.2, True, -19)
        if sec == 'wings':
            eyes(tr, tr.at(bar), tr.barlen, tri, 2 + bar, 0.09, bar + 300)
        if sec == 'fold' and bar == 80:
            wings(tr, tr.at(80), chd('F2', 'm'), tr.barlen * 4, 0.17, False, -14)
        if sec == 'fold' and bar == 84:
            wings(tr, tr.at(84), chd('F2', 'm'), tr.barlen * 4, 0.15, True, -12)
        if sec == 'all' and bar in (68, 72):
            wings(tr, tr.at(bar), tri, tr.barlen * 3, 0.13, True, -12)
        # ---- FEAR: ice doubling the violin's theme, then the shards (volleys of glass, falling)
        if sec == 'fear' and bar >= 32:
            for i in range(16):
                vol = ladder(tri, m('C6'), 12)[::-1]
                tr.add(glass(vol[i % 12] + (12 if i < 4 else 0), 0.6, 0.12 + 0.05 * (i % 4 == 0)), g16(bar, i), 0.8 - 0.1 * i, 1, 0.5)
            tr.add(hp(R.noise(int(tr.barlen * SR)), 6000) * np.linspace(0.0, 0.1, int(tr.barlen * SR)), tr.at(bar), 0, 1, 0.6)
            if bar == 35:
                tr.add(suck(tr.barlen, 0.4), tr.at(bar), 0, 1, 0.3)
        # ---- HUNGER: hex bolts (a theremin swooping), then the curse circles bursting
        if sec == 'hunger' and bar < 44 and bar % 2 == 1:
            tr.add(theremin(hz(tri[2] + 24), tr.beat * 1.5, 0.16, glide_from=hz(tri[2] + 36), glide=0.4), tr.at(bar, 2.5), -0.5, 1, 0.55)
        if sec == 'hunger' and 44 <= bar < 47:
            for b in (0, 2.5):
                tr.add(great_organ([x + 12 for x in ch], tr.beat * 1.2, 0.28, 0.01), tr.at(bar, b), 0, 1, 0.5)
                tr.add(brass([x for x in ch[::2]], tr.beat * 0.6, 0.36, 2000, 0.004), tr.at(bar, b), 0.2, 1, 0.4)
                tr.add(clank(0.3, 2600, 0.8, bar * 7 + int(b)), tr.at(bar, b), -0.4, 1, 0.4)
            tr.add(suck(tr.beat * 2.5, 0.35), tr.at(bar), 0.3, 1, 0.3)
            runs(tr, tr.at(bar), [m('C7') - 2 * i for i in range(16)], 0.22, -0.2, 0.4)     # (the drain: whole tones, falling)
        if sec == 'hunger' and bar == 47:
            tr.add(rise(tr.barlen, 0.3), tr.at(bar), 0, 1, 0.3)
            for i in range(16): tr.add(snare(0.1 + 0.025 * i), g16(bar, i), 0.1, 1, 0.3)
        # ---- WAR: the jaws, and the whirlpool (violin runs, up and down the harmonic minor)
        if sec == 'war':
            for b in (2.5, 3):
                chomp(tr, tr.at(bar, b), m('F3') if bar < 56 else r + 12, 0.85, 0.2 * (1 if b == 3 else -1))
            if 52 <= bar < 56:
                runs(tr, tr.at(bar), scale_run(m('F5'), 16, bar % 2 == 0), 0.26, 0.3 if bar % 2 else -0.2, 0.35)
            if bar >= 56:
                for b in (0, 1):
                    chomp(tr, tr.at(bar, b), r + 12, 1.0, 0.0)
                for i in range(16): tr.add(snare(0.08 + 0.02 * (bar - 56) * 4 + 0.004 * i), g16(bar, i), 0.1, 1, 0.3)
                if bar == 59: tr.add(rise(tr.barlen, 0.35), tr.at(bar), 0, 1, 0.3)
        # ---- ALL THREE: ice, hexes and jaws together
        if sec == 'all' and bar < 76:
            eyes(tr, tr.at(bar), tr.barlen, tri, 3, 0.08, bar + 900)
            if bar % 2 == 1:
                tr.add(theremin(hz(tri[1] + 24), tr.beat * 1.2, 0.12, glide_from=hz(tri[1] + 31), glide=0.3), tr.at(bar, 1.5), -0.5, 1, 0.55)
            if bar % 4 == 3:
                for b in (2.5, 3): chomp(tr, tr.at(bar, b), r + 12, 0.8)
        if sec == 'all' and 68 <= bar < 76:
            runs(tr, tr.at(bar), frantic(ch, bar, m('F5')), 0.25, 0.3 if bar % 2 else -0.25, 0.35)
        if sec == 'all' and bar >= 76:                                         # (the head of S, hammered, before the wings fold)
            for b in (0, 0.5, 1, 2, 2.5, 3):
                tr.add(brass([r - 12, r - 5, r], tr.beat * 0.4, 0.42, 1700, 0.01), tr.at(bar, b), 0, 1, 0.3)
            for i in range(16): tr.add(snare(0.1 + 0.02 * (bar - 76) * 4 + 0.004 * i), g16(bar, i), 0.1, 1, 0.3)
            if bar == 79: tr.add(crash(0.4), tr.at(bar, 3.5), 0.3, 1, 0.4)
        if bar in (7, 23):
            tr.add(rise(tr.barlen, 0.3), tr.at(bar), 0, 1, 0.3)
            for i in range(16): tr.add(snare(0.08 + 0.02 * i), g16(bar, i), 0.1, 1, 0.3)
        if bar == 87:
            tr.add(rise(tr.barlen, 0.25), tr.at(bar), 0, 1, 0.3)
    # ---- the lines
    lo = lambda x, d: brass([x], d, 0.42, 1700, 0.03)
    ply(tr, tr.at(8), tp(S2, -12), lo, -0.1, 1, 0.4)
    ply(tr, tr.at(8), tp(S2, -24), lambda x, d: brass([x], d, 0.32, 900, 0.03), 0, 1, 0.3)
    ply(tr, tr.at(12), tp(S2, 12), lambda x, d: vln(x, d, 0.44), 0.1, 1, 0.35)
    ply(tr, tr.at(12), S2, lo, -0.15, 1, 0.4)
    for b in range(16, 20):
        if tr.want(b): runs(tr, tr.at(b), frantic(p2_chord(b, 0)[:3] if b % 2 == 0 else p2_chord(b, 1)[:3], b), 0.27, 0.25 if b % 2 else -0.2, 0.35)
    ply(tr, tr.at(16), S2, lambda x, d: chorus([x], d + 0.1, 0.32, 0.06, 'a'), 0, 1, 0.5)
    ply(tr, tr.at(16), tp(S2, -12), lo, -0.1, 1, 0.4)
    ply(tr, tr.at(20), tp(S2, 12), lambda x, d: section(x, d, 0.38), 0.15, 1, 0.35)
    ply(tr, tr.at(20), S2, lambda x, d: section(x, d, 0.3), -0.15, 1, 0.35)
    ply(tr, tr.at(20), tp(S2, -12), lambda x, d: brass([x], d, 0.36, 2400, 0.03), 0, 1, 0.4)
    # FEAR: the Dread's theme, on its own pitches - iced
    ply(tr, tr.at(24), A1, lambda x, d: vln(x, d, 0.44), 0.1, 1, 0.35)
    ply(tr, tr.at(24), tp(A1, 12), lambda x, d: glass(x, max(0.5, d * 1.5), 0.11), -0.3, 1, 0.55)
    # HUNGER: the Dread's plea, and a theremin's shadow an octave under it
    ply(tr, tr.at(36), B1, lambda x, d: vln(x, d, 0.42, depth=0.009), 0.15, 1, 0.4)
    ply(tr, tr.at(36), tp(B1, -12), lambda x, d: theremin(x, d, 0.2, glide=0.18), -0.3, 1, 0.5)
    # WAR: the Dread's theme in the low brass, F minor, and the cello under it
    ply(tr, tr.at(48), tp(A1, 5 - 24), lambda x, d: brass([x, x + 12], d, 0.46, 1500, 0.02), -0.05, 1, 0.35)
    ply(tr, tr.at(48), tp(A1, 5 - 12), lambda x, d: section(x, d, 0.28, attack=0.02), 0.25, 1, 0.35)
    # ALL THREE: the Dread's theme for everyone, then S2 for everyone
    ply(tr, tr.at(60), tp(A2, 5), lambda x, d: section(x, d, 0.36), 0.15, 1, 0.35)
    ply(tr, tr.at(60), tp(A2, 5 - 12), lambda x, d: section(x, d, 0.3), -0.15, 1, 0.35)
    ply(tr, tr.at(60), tp(A2, 5 - 24), lambda x, d: brass([x], d, 0.34, 2200, 0.02), 0, 1, 0.35)
    for k in (68, 72):
        ply(tr, tr.at(k), tp(S2, 0), lambda x, d: brass([x, x - 12], d, 0.44, 2600, 0.02), -0.1, 1, 0.4)
        ply(tr, tr.at(k), tp(S2, 12), lambda x, d: chorus([x], d + 0.1, 0.3, 0.05, 'a'), 0.1, 1, 0.5)
    return tr


def p2():
    tr = Track('sovereign2', P2BPM, P2BARS)
    assert round(tr.seconds) == 120
    p2_compose(View(tr, P2BPM))
    return tr


# ====================================================================== FORM 3: TRUE
P3_TAIL = [('F#2', 'm'), ('F#2', 'm'), ('D2', 'M'), ('Db2', 'M'), ('C2', '7b9'), ('C2', '7b9'), ('C2', 'M'), ('C2', 'M')]


def p3_sec(bar):
    for lim, nm in ((32, 'all'), (52, 'void'), (68, 'light'), (84, 'noway'), (92, 'plunge')):
        if bar < lim: return nm
    return 'end'


def p3_chord(bar):
    sec = p3_sec(bar)
    if sec == 'all': return chd(*PROG_S[(bar // 2) % 8])
    if sec == 'void': return [m('F2'), m('Gb2'), m('C3')]
    if sec == 'light': return chd(*PROG_S[((bar - 52) // 2) % 8], k=1)
    if sec == 'noway':
        if bar == 83: return chd('F#2', 'm')
        rt, kd = PROG_A[(bar - 68) % 8]
        return chd(rt, kd, k=6 - 12 * (rt[-1] == '3'))
    if sec == 'plunge': return chd(*P3_TAIL[bar - 84])
    return chd('F#2', 'm')


def p3_everything(tr, bar, ch, sec, lift=0):
    """everything at once: one bar of it"""
    r = ch[0]; tri = ch[:3]
    g16 = lambda i: tr.at(bar, i / 4)
    big = sec in ('light',)
    # strings: the frantic ostinato (a half bar each way)
    pat = osti(tri, sec)
    for i in range(16):
        tr.add(strings(pat[i % 8], tr.beat * 0.22, 0.17, 2800), g16(i), -0.35 if i % 2 else 0.35, 1, 0.25)
    for i in range(8):
        tr.add(bass(r - 12 + (12 if i % 2 else 0), tr.beat * 0.45, 0.6, 850, 5), tr.at(bar, i / 2), 0, 1, 0.05)
    tr.add(sub(r - 12, tr.beat * 3.9, 0.35), tr.at(bar), 0, 1, 0.05)
    # drums: double kick, the backbeat, toms, crashes
    for i in range(16):
        if i % 2 == 0 or (bar % 4 == 3 and i >= 8) or (big and i % 4 == 3):
            tr.add(kick(0.78), g16(i), 0, 1, 0.04)
    for b in (1, 3): tr.add(snare(0.62), tr.at(bar, b), 0.1, 1, 0.3)
    for i in range(16): tr.add(hat(0.07 + 0.04 * (i % 2 == 0)), g16(i), 0.4, 1, 0.1)
    for b in (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5): tr.add(tom(60 if b % 1 else 50, 0.28, 7, 0.3), tr.at(bar, b), -0.3, 1, 0.3)
    if bar % 4 == 0: tr.add(crash(0.32), tr.at(bar), 0.3, 1, 0.35)
    # the chains: struck on the 1, dragged on the 3
    tr.add(chain_hit(0.5, bar * 5, 6), tr.at(bar), -0.15, 1, 0.35)
    tr.add(clank(0.28, 1800 + 60 * (bar % 5), 0.4, bar * 5 + 1), tr.at(bar, 2.5), 0.4, 1, 0.35)
    if bar % 2 == 1: tr.add(rattle(tr.beat * 1.0, 0.18, 30, bar * 5 + 2), tr.at(bar, 3), -0.4, 1, 0.4)
    # the bells: the great bell every other bar, a smaller one on every beat in the last light
    if bar % 2 == 0:
        tr.add(great_bell(hz(r + 12), 6.0, 0.42, 1.0, bar), tr.at(bar), -0.15, 1, 0.55)
        tr.add(timp(r - 12, 0.6), tr.at(bar), 0, 1, 0.4)
    for b in ((0, 1, 2, 3) if big else (2,)):
        tr.add(great_bell(hz(ch[2] + 24 + (12 if b % 2 else 0)), 3.0, 0.14 if big else 0.18, 1.2, bar * 7 + b), tr.at(bar, b), 0.45, 1, 0.6)
    # the organ and the choir, a chord each two bars
    if bar % 2 == 0:
        tr.add(great_organ([r - 12, r] + [x + 12 for x in tri], tr.beat * 8, 0.36, 0.05, 1.0), tr.at(bar), 0, 1, 0.55)
        tr.add(chorus([x + 12 for x in tri] + [r + 24], tr.beat * 8, 0.36, 0.2, 'a'), tr.at(bar), 0, 1, 0.6)
        tr.add(chorus([r, ch[2]], tr.beat * 8, 0.22, 0.2, 'o'), tr.at(bar), 0, 1, 0.6)
    # jaws, wings, eyes
    if bar % 4 == 2:
        for b in (2.5, 3): chomp(tr, tr.at(bar, b), r + 12, 0.75, 0.3 * (b - 2.75) * 4)
    if bar % 8 == 0:
        wings(tr, tr.at(bar), tri, tr.barlen * 3, 0.12, True, -14)
    eyes(tr, tr.at(bar), tr.barlen, tri, 2, 0.07, bar + 4000)


def p3_compose(tr, bars=range(P3BARS)):
    g16 = lambda bar, i: tr.at(bar, i / 4)
    for bar in bars:
        if not tr.want(bar): continue
        sec = p3_sec(bar)
        ch = p3_chord(bar); r = ch[0]; tri = ch[:3]
        if sec in ('all', 'light'):
            p3_everything(tr, bar, ch, sec)
            if bar < 16 or sec == 'light' and bar >= 60:                   # (the violin's runs, frantic over the chords)
                runs(tr, tr.at(bar), frantic(tri, bar, m('F5') + (1 if sec == 'light' else 0)), 0.24, 0.3 if bar % 2 else -0.25, 0.35)
        elif sec == 'noway':
            p3_everything(tr, bar, ch, 'noway')
            for b in (0.5, 2.5):
                tr.add(brass([r - 12, r - 5], tr.beat * 0.4, 0.4, 1000, 0.01), tr.at(bar, b), -0.15, 1, 0.3)
        elif sec == 'void':
            v = bar - 32
            if v == 0:                                                     # (the floor falls into the lava)
                tr.add(boom(1.0, 95, 26, 4.0), tr.at(bar), 0, 1, 0.4)
                tr.add(thunder(0.8, 5.0), tr.at(bar), 0, 1, 0.5)
                tr.add(rattle(3.5, 0.45, 50, 33, True), tr.at(bar), -0.3, 1, 0.5)
                tr.add(rattle(3.0, 0.35, 40, 34, True), tr.at(bar, 1), 0.4, 1, 0.5)
                tr.add(crash(0.45, 4.0), tr.at(bar), 0.2, 1, 0.5)
                tr.add(great_organ([m('F1'), m('F2'), m('Gb2'), m('C3'), m('B3')], tr.beat * 12, 0.42, 0.01, 1.0), tr.at(bar), 0, 1, 0.75)
                tr.add(chorus([m('F4'), m('Gb4'), m('B4'), m('C5')], tr.beat * 6, 0.4, 0.02, 'a'), tr.at(bar), 0, 1, 0.75)
            if v % 4 == 0:
                tr.add(drone([m('F1'), m('Gb1'), m('F2'), m('B2')], tr.barlen * 4 + 1.5, 0.5, 0.4), tr.at(bar), 0, 1, 0.5)
            if v % 8 == 2:
                tr.add(gaze(m('F6'), tr.barlen * 6, 0.07), tr.at(bar), 0.6 - 0.2 * (v // 8), 1, 0.7)
            if v % 2 == 1:
                heart(tr, tr.at(bar), 0.42 + 0.02 * v)
            if v in (3, 9, 14):
                tr.add(great_bell(hz(m('F3')) * 0.985, 7.0, 0.3, 0.7, v), tr.at(bar), -0.4, 1, 0.75)
            if v in (5, 12):
                tr.add(chorus([m('F3'), m('Gb3'), m('G3')], tr.barlen * 4, 0.24, 2.0, 'u'), tr.at(bar), 0, 1, 0.75)
            if v in (6, 11, 15):
                tr.add(whisper(tr.barlen * 2, 0.2, v + 70), tr.at(bar), 0.6 if v % 2 else -0.6, 1, 0.65)
                tr.add(suck(tr.barlen, 0.18), tr.at(bar, 1), -0.2, 1, 0.5)
            if v in (4, 10):
                tr.add(rattle(tr.barlen * 2, 0.12, 10, v + 90), tr.at(bar), 0.7 - 0.14 * v, 1, 0.75)
            g = np.random.default_rng(v + 5000)
            for _ in range(2):                                             # (lava, popping far below)
                tr.add(pop(0.3, g.uniform(55, 110)), tr.at(bar, g.uniform(0, 4)), g.uniform(-0.6, 0.6), 1, 0.5)
            # (the rebuild: bars 44-51 - the eyes open again, a timpani roll and a snare roll, then everything drawn in)
            if v >= 12:
                eyes(tr, tr.at(bar), tr.barlen, [m('F2'), m('Gb2'), m('C3')], v - 10, 0.05 + 0.006 * v, bar + 6000)
                for i in range(0, 16, 1 if v >= 16 else 2):
                    tr.add(timp(m('C2'), 0.12 + 0.03 * (v - 12)), g16(bar, i), 0, 1, 0.4)
            if v >= 16:
                for i in range(16): tr.add(snare(0.06 + 0.012 * ((v - 16) * 16 + i) ** 0.9), g16(bar, i), 0.1, 1, 0.35)
            if v == 16:
                wings(tr, tr.at(bar), [m('C#2'), m('F2'), m('G#2')], tr.barlen * 4, 0.16, True, -24)
            if v == 18:
                tr.add(rise(tr.barlen * 2, 0.35), tr.at(bar), 0, 1, 0.3)
            if v == 19:
                tr.add(suck(tr.barlen, 0.5), tr.at(bar), 0, 1, 0.3)
        elif sec == 'plunge':
            pb = bar - 84
            if pb < 2:                                                     # (F# minor, hammered)
                for b in (0, 0.5, 1, 2, 2.5, 3, 3.5):
                    tr.add(brass([r - 12, r - 5, r, ch[1]], tr.beat * 0.35, 0.5, 1800, 0.006), tr.at(bar, b), 0, 1, 0.3)
                    tr.add(kick(0.85), tr.at(bar, b), 0, 1, 0.05)
                    tr.add(chain_hit(0.35, bar * 13 + int(b * 2), 4, False), tr.at(bar, b), 0.2, 1, 0.35)
                tr.add(great_organ([r - 12, r] + [x + 12 for x in tri], tr.beat * 4, 0.4, 0.02), tr.at(bar), 0, 1, 0.55)
                tr.add(chorus([x + 12 for x in tri], tr.beat * 4, 0.4, 0.1, 'a'), tr.at(bar), 0, 1, 0.6)
                tr.add(great_bell(hz(r + 24), 4.0, 0.3, 1.0, bar), tr.at(bar), -0.2, 1, 0.55)
                for b in (1, 3): tr.add(snare(0.6), tr.at(bar, b), 0.1, 1, 0.3)
                if pb == 0: tr.add(crash(0.45), tr.at(bar), 0.3, 1, 0.4)
            else:
                tr.add(great_organ([r - 12, r] + [x + 12 for x in tri], tr.beat * 4, 0.34, 0.05), tr.at(bar), 0, 1, 0.6)
                tr.add(sub(r - 12, tr.beat * 3.9, 0.35), tr.at(bar), 0, 1, 0.05)
                tr.add(chorus([x + 12 for x in tri], tr.beat * 4, 0.3, 0.2, 'a'), tr.at(bar), 0, 1, 0.6)
                for i in range(16):
                    tr.add(strings(tri[i % 3] + 24, tr.beat * 0.22, 0.12, 2600), g16(bar, i), -0.35 if i % 2 else 0.35, 1, 0.3)
                for i in range(0, 16, 2 if pb < 4 else 1):
                    tr.add(timp(r - 12 if pb < 4 else m('C2'), 0.2 + 0.03 * pb), g16(bar, i), 0, 1, 0.4)
                for b in (0, 2): tr.add(kick(0.8), tr.at(bar, b), 0, 1, 0.05)
                if pb >= 4:
                    for i in range(16): tr.add(snare(0.08 + 0.016 * ((pb - 4) * 16 + i) ** 0.85), g16(bar, i), 0.1, 1, 0.3)
                if pb == 2:                                                # (the strings tumble down: F#6 to C5, quickening)
                    for i in range(18):
                        t0 = tr.at(bar) + tr.barlen * 2 * (1 - (1 - i / 18) ** 1.3)
                        tr.add(violin(m('F#6') - i, 0.16, 0.36 - 0.006 * i, attack=0.01, scoop=0.0, depth=0.0, voices=2), t0, 0.25 - 0.03 * i, 1, 0.4)
                if pb == 4:
                    wings(tr, tr.at(bar), chd('C2', 'M'), tr.barlen * 4, 0.16, True, -16)
                    tr.add(chain_hit(0.5, 4321, 7), tr.at(bar), 0, 1, 0.4)
                if pb == 7:
                    tr.add(rise(tr.barlen, 0.35), tr.at(bar), 0, 1, 0.3)
                    tr.add(suck(tr.barlen, 0.4), tr.at(bar), 0, 1, 0.3)
    # ---- the lines
    big = lambda x, d: brass([x, x + 12], d, 0.46, 2600, 0.04)
    ply(tr, tr.at(0), tp(S3, -12), big, -0.1, 1, 0.4)
    ply(tr, tr.at(0), tp(S3, -24), lambda x, d: brass([x], d, 0.3, 900, 0.05), 0, 1, 0.3)
    ply(tr, tr.at(0), tp(S3, 12), lambda x, d: chorus([x], d + 0.15, 0.26, 0.1, 'a'), 0, 1, 0.5)
    ply(tr, tr.at(16), tp(S3, -12), big, -0.1, 1, 0.4)
    ply(tr, tr.at(16), tp(S3, 12), lambda x, d: section(x, d, 0.38, attack=0.04), 0.2, 1, 0.4)
    ply(tr, tr.at(16), S3, lambda x, d: section(x, d, 0.3, attack=0.04), -0.2, 1, 0.4)
    ply(tr, tr.at(16), tp(S3, -24), lambda x, d: brass([x], d, 0.3, 900, 0.05), 0, 1, 0.3)
    # the void: the violin alone, in ghostly harmonics - S, unravelled, on tritones
    ghost = lambda x, d: violin(x, d, 0.2, vib=4.0, depth=0.012, attack=0.4, bright=0.35, trem=0)
    ply(tr, tr.at(33), mel('F6:6 B5:6 C6:4 Db6:8 r:4 Gb6:6 C6:6 B5:8 r:4 E6:6 F6:10'), ghost, 0.3, 1, 0.7)
    ply(tr, tr.at(33), tp(mel('r:12 F5:8 r:12 C5:8 r:8 B4:12'), -12), lambda x, d: cello(x, d, 0.18), -0.3, 1, 0.65)
    # the last light: S3 a semitone higher
    ply(tr, tr.at(52), tp(S3, -11), big, -0.1, 1, 0.4)
    ply(tr, tr.at(52), tp(S3, 13), lambda x, d: section(x, d, 0.4, attack=0.04), 0.2, 1, 0.4)
    ply(tr, tr.at(52), tp(S3, 1), lambda x, d: section(x, d, 0.32, attack=0.04), -0.2, 1, 0.4)
    ply(tr, tr.at(52), tp(S3, 13), lambda x, d: chorus([x], d + 0.15, 0.26, 0.1, 'a'), 0, 1, 0.5)
    ply(tr, tr.at(52), tp(S3, -23), lambda x, d: brass([x], d, 0.32, 900, 0.05), 0, 1, 0.3)
    # no way out: the Dread's theme, F# minor, for the violins in octaves (and brass on the bass)
    for k, line in ((68, A1), (76, A2)):
        ply(tr, tr.at(k), tp(line, 6), lambda x, d: section(x, d, 0.38), 0.15, 1, 0.35)
        ply(tr, tr.at(k), tp(line, 6 - 12), lambda x, d: section(x, d, 0.32), -0.15, 1, 0.35)
        ply(tr, tr.at(k), tp(line, 6 - 24), lambda x, d: brass([x], d, 0.34, 2600, 0.02), 0, 1, 0.35)
    return tr


def p3():
    tr = Track('sovereign3', P3BPM, P3BARS)
    assert round(tr.seconds) == 120
    p3_compose(View(tr, P3BPM))
    return tr


# ====================================================================== THE TURN
def turn_compose(tr, t0=0.0):
    """8 s: the chains snap, the wings unfurl, the bell, the Dread's head cried out, a roll to the brink (silent last second)"""
    a = lambda s, t, *k: tr.add(s, t0 + t, *k)
    a(chain_hit(1.0, 777, 9), 0.0, 0, 1, 0.45)
    a(rattle(2.6, 0.55, 60, 778, True), 0.02, -0.3, 1, 0.5)
    a(rattle(2.2, 0.45, 50, 779, True), 0.1, 0.4, 1, 0.5)
    a(boom(0.9, 110, 28, 3.0), 0.0, 0, 1, 0.4)
    a(crash(0.5, 3.0), 0.0, 0.2, 1, 0.5)
    a(brass(['F2', 'C3', 'F3', 'Gb3', 'C4'], 0.9, 0.5, 2600, 0.005), 0.0, 0, 1, 0.4)
    a(great_organ(['F1', 'F2', 'C3', 'Gb3'], 1.4, 0.4, 0.01), 0.0, 0, 1, 0.6)
    a(timp('F2', 1.0), 0.0, 0, 1, 0.4)
    class _T:                                                            # (the wings, through the same offset)
        def add(self, s, t, *k): tr.add(s, t0 + t, *k)
    wings(_T(), 0.5, chd('F2', 'm'), 3.2, 0.24, True, -21)
    eyes(_T(), 1.2, 2.6, chd('F2', 'm'), 10, 0.1, 4242)
    a(great_bell('F3', 6.0, 0.6, 1.0, 1), 2.2, -0.15, 1, 0.6)
    a(great_bell('C4', 4.0, 0.35, 1.2, 2), 3.6, 0.3, 1, 0.6)
    a(great_organ(['C2', 'C3', 'E3', 'G3', 'Db4'], 4.4, 0.36, 0.5, 0.8), 2.4, 0, 1, 0.65)
    a(chorus(['C3', 'G3', 'C4', 'E4'], 4.2, 0.32, 0.8, 'o'), 2.6, 0, 1, 0.65)
    beat = 60 / 168                                                      # (the Dread's head, at the Dread's speed)
    t = 3.4
    for x, d in DREAD_HEAD:
        a(vln(x, d * beat * 0.95, 0.42), t, 0.15, 1, 0.45); t += d * beat
    a(violin('E6', 2.2, 0.32, trem=13, depth=0.004), t, 0.15, 1, 0.5)
    for i in range(24):                                                  # (a timpani roll on the dominant, to the brink)
        a(timp('C2', 0.12 + 0.018 * i, 3.0), 4.4 + i * 0.1, 0, 1, 0.4)
    for i in range(28):
        a(snare(0.05 + 0.017 * i, 180), 4.4 + i * 0.0857, 0.1, 1, 0.35)
    a(rise(2.6, 0.32), 4.4, 0, 1, 0.3)
    a(chain_hit(0.6, 780, 6), 6.85, 0, 1, 0.35)


def turn():
    tr = Track('sovereign_turn', 120, 4)
    turn_compose(tr)
    return tr



# ====================================================================== (2.98c) EACH FORM'S ENTRANCE
# THE BROKEN (boss_sovereign_enter2, 12 s): the Armored form on one knee, its plate splitting - a heartbeat under a low choir
# swelling on F minor, struck iron for every crack (4 s); then THE TURN itself (chains, the six wings, the eyes, the bell, the
# Dread's head, the roll), landing on the Broken form's loop.
# THE TRUE (boss_sovereign_enter3, 15 s): the helm cracking - glass under the heartbeat, the choir climbing a semitone at a
# time, the eye's tritone watching (5 s); THE HELM SHATTERS (5 s: the turn's blow, its wings); the great eye opens - a
# shrieking cluster; then the floor cracking: a vast rumble and a riser to the True form's downbeat.
def enter_build(tr, dur, seed, glassy=False):
    """the build before a form breaks: a drone, a quickening heartbeat, a low choir swelling (the eye's tritone, for the True
    form), a crack every so often (struck iron, or glass), a riser"""
    a = lambda sig, t, *k: tr.add(sig, t, *k)
    a(drone(['F1', 'C2', 'F2'], dur + 1.0, 0.32), 0.0, 0, 1, 0.5)
    t, i = 0.25, 0
    while t < dur - 0.2:
        a(timp('F1', 0.55 + 0.05 * i, 3.0), t, 0, 1, 0.35); a(timp('F1', 0.35 + 0.03 * i, 3.4), t + 0.28, 0, 1, 0.35)
        t += max(0.55, 1.0 - 0.07 * i); i += 1
    a(chorus(['F3', 'Gb3', 'C4'] if glassy else ['F3', 'Ab3', 'C4'], dur + 0.5, 0.34, dur * 0.8, 'u'), 0.0, 0, 1, 0.6)
    g = np.random.default_rng(seed)
    for k in range(6):
        t = 0.5 + k * (dur - 0.8) / 6
        a(glass(m('F6') + int(g.integers(0, 7)), 1.2, 0.18) if glassy else clank(0.5, g.uniform(500, 900), 1.6, seed + k), t, g.uniform(-0.6, 0.6), 1, 0.5)
        a(rattle(0.8, 0.25, 40, seed * 9 + k), t + 0.05, g.uniform(-0.6, 0.6), 1, 0.55)
    if glassy:
        a(gaze('C6', dur, 0.08), 0.0, 0.3, 1, 0.7)
    a(rise(dur * 0.7, 0.28), dur * 0.3, 0, 1, 0.35)


def enter2():
    tr = Track('sovereign_enter2', 120, 6)                               # (12 s: 4 s of build, then the turn)
    enter_build(tr, 4.0, 2381)
    turn_compose(tr, 4.0)
    return tr


def enter3():
    tr = Track('sovereign_enter3', 60, 15, beats=1)                      # (15 s: 5 s of build, the turn, the eye, the floor)
    enter_build(tr, 5.0, 2391, True)
    turn_compose(tr, 5.0)
    a = lambda sig, t, *k: tr.add(sig, t, *k)
    for k, x in enumerate(('C6', 'Db6', 'F#6', 'G6')):                    # (the great eye opens: a shrieking cluster)
        a(violin(x, 3.0, 0.16, trem=16, voices=3, attack=0.6), 8.8 + 0.12 * k, (-0.4, 0.4)[k % 2], 1, 0.5)
    a(gaze('F#6', 3.5, 0.14), 8.8, 0, 1, 0.6)
    a(boom(0.8, 70, 22, 4.0), 11.0, 0, 1, 0.5)                          # (the floor, cracking)
    a(rattle(2.5, 0.4, 50, 2399, True), 11.2, 0, 1, 0.5)
    a(rise(3.6, 0.36), 11.3, 0, 1, 0.35)
    for i in range(26):
        a(snare(0.05 + 0.016 * i, 180), 12.4 + i * 0.1, 0.1, 1, 0.35)
    return tr



# ====================================================================== (2.98c) THE LAST LIGHT (boss_divine, 28 s, once)
# Under the Divine One's coming: silence and one harmonic (0-2 s); the beam through the dome - a bell (2 s); a choir in F
# MAJOR swelling as He descends (3-8); REVEALED - the great organ, the full choir, the bells (8); while He looks down and
# names it, a single violin sings Aurel's cell, in major - the light it was (10-15); a riser as His hand rises; THE SMITING (16
# s): everything, once, on F major; the Sovereign comes apart into light - glass and bells falling (16-21); rest (21-24, a
# soft organ, the violin's last note a major third); He rises, and it fades (24-28).
def divine():
    tr = Track('divine', 60, 28, beats=1)
    a = lambda sig, t, *k: tr.add(sig, t, *k)
    a(violin('A6', 3.0, 0.08, vib=4.5, depth=0.003, attack=1.2, bright=0.4), 0.3, 0.2, 1, 0.8)
    a(great_bell('F3', 8.0, 0.55, 1.0, 21), 2.0, 0, 1, 0.65)
    a(soft_organ(['F3', 'A3', 'C4'], 7.0, 0.32, 2.5, 1.5), 2.2, 0, 1, 0.6)
    a(chorus(['F3', 'C4', 'F4', 'A4'], 6.0, 0.3, 4.5, 'a'), 3.0, 0, 1, 0.65)
    for k in range(8):                                                    # (light motes as He comes down)
        a(glass(m('C6') + (0, 4, 7, 12, 16, 19, 24, 28)[k], 1.4, 0.07), 3.4 + 0.55 * k, (-0.6 + 0.17 * k), 1, 0.7)
    a(great_organ(['F2', 'C3', 'F3', 'A3', 'C4', 'F4'], 8.0, 0.34, 0.4, 0.9), 8.0, 0, 1, 0.6)        # (revealed)
    a(chorus(['F3', 'A3', 'C4', 'F4', 'A4', 'C5'], 8.0, 0.36, 0.5, 'a'), 8.0, 0, 1, 0.65)
    a(great_bell('F3', 7.0, 0.6, 1.0, 22), 8.0, -0.2, 1, 0.65); a(great_bell('C4', 6.0, 0.45, 1.0, 23), 8.6, 0.25, 1, 0.65)
    a(timp('F2', 0.5, 2.0), 8.0, 0, 1, 0.4)
    t = 10.2
    for x, d in mel('C5:.75 F5:.75 A5:1.5 G5:.5 F5:.75 E5:.75 F5:2'):     # (Aurel's cell, in major: the light it was)
        a(violin(x, d * 0.95, 0.34, depth=0.007), t, 0.1, 1, 0.55); t += d
    a(rise(3.0, 0.3), 13.0, 0, 1, 0.35)
    for i in range(20):
        a(timp('C2', 0.1 + 0.02 * i, 3.0), 14.0 + i * 0.1, 0, 1, 0.4)
    # THE SMITING
    a(boom(0.9, 120, 30, 3.5), 16.0, 0, 1, 0.4); a(crash(0.6, 4.0), 16.0, 0.2, 1, 0.55); a(thunder(0.6, 4.0), 16.0, -0.2, 1, 0.5)
    a(great_organ(['F1', 'F2', 'C3', 'F3', 'A3', 'C4', 'F4', 'A4'], 5.0, 0.45, 0.02, 1.0), 16.0, 0, 1, 0.6)
    a(chorus(['F3', 'A3', 'C4', 'F4', 'A4', 'C5', 'F5'], 5.0, 0.42, 0.05, 'a'), 16.0, 0, 1, 0.65)
    a(great_bell('F2', 9.0, 0.7, 1.2, 24), 16.0, 0, 1, 0.65)
    for k in range(16):                                                   # (it comes apart: light falling)
        a(glass(m('F7') - (0, 3, 5, 7, 8, 10, 12, 15, 17, 19, 20, 22, 24, 27, 29, 31)[k], 1.6, 0.09), 16.6 + 0.28 * k, (-0.7, 0.7)[k % 2], 1, 0.7)
    a(soft_organ(['F3', 'A3', 'C4', 'F4'], 6.0, 0.28, 1.5, 2.0), 21.0, 0, 1, 0.6)                 # (rest)
    a(violin('A5', 4.0, 0.2, vib=4.8, depth=0.006, attack=0.8), 22.0, 0.1, 1, 0.6)
    a(chorus(['F4', 'A4', 'C5', 'F5'], 4.5, 0.2, 2.5, 'a'), 23.5, 0, 1, 0.7)                        # (He rises)
    a(violin('F6', 4.0, 0.06, vib=4.5, depth=0.003, attack=1.5, bright=0.4), 24.0, -0.2, 1, 0.8)
    return tr


# ====================================================================== THE ENTRANCE
# 20 s under the boss's entrance - six bars of form 1's tempo (72 BPM, 10/3 s a bar), so it ends on form 1's own downbeat:
# near-silence, a heartbeat and chains far off (bars 0-1); a choir building (from bar 1); the bells tolling (from bar 2); the
# organ swelling, F minor to the dominant (bars 3-4); THE ROAR (bar 5, 16.7 s) on F minor; then the drag into the fight - a
# snare roll and a riser on the Neapolitan (Gb), as form 1's own last bar has, so its first bar follows as if round the loop.
IBARS, ITAIL = 6, 3


def roar(dur=3.0, amp=1.0, f=62.0):
    """the Sovereign's roar: a throat of detuned low saws, its pitch flung up and dragged down, rasping (a growl at 31 and 47
    Hz), its vowel opening from 'o' to 'a', breath through it"""
    t = T(dur); n = len(t)
    f0 = f * (1 + 0.55 * (1 - np.exp(-t * 9)) * np.exp(-t * 0.8))
    growl = 1 + 0.35 * np.sin(2 * np.pi * 31 * t) + 0.2 * np.sin(2 * np.pi * 47 * t + 1)
    s = np.zeros(n)
    for mult, a in ((1.0, 1.0), (1.5, 0.55), (2.0, 0.45)):
        for v in (-0.02, -0.007, 0.0, 0.006, 0.019):
            ph = np.cumsum(f0 * mult * (1 + v)) / SR + R.r()
            s += a * (2 * (ph % 1) - 1)
    s = s / 10 * growl
    w = np.clip(t / (dur * 0.4), 0, 1)
    s = formant(s, 'o') * (1 - w) + formant(s, 'a') * w + lp(s, 380) * 0.8
    s += bp(R.noise(n), 400, 3500) * growl * 0.35 * np.exp(-t * 0.8)
    return amp * s * env(n, 0.03, 0.4, 0.75, dur * 0.55)


def intro_compose(tr):
    fm, c7, gb = chd('F2', 'm'), chd('C2', '7b9'), chd('Gb2', 'M')
    # ---- 1. near-silence: a faint pedal, a heartbeat, chains somewhere far off
    tr.add(drone([m('F1'), m('F2')], tr.barlen * 5, 0.08, 0.25), tr.at(0), 0, 1, 0.5)
    beats = [b * 2 for b in range(4)] + [8 + b * 2 for b in range(2)] + [12 + b for b in range(5)]          # (it quickens)
    for i, b in enumerate(beats):
        heart(tr, tr.at(0, b), 0.07 + 0.03 * i)
    for t0, pan, sd in ((0.9, -0.7, 1), (3.1, 0.65, 2), (5.6, -0.4, 3), (8.0, 0.8, 4), (10.4, -0.8, 5)):
        tr.add(lp(rattle(1.4, 0.04 + 0.012 * sd, 18, 8800 + sd), 3500), t0, pan, 1, 0.9)
    for t0, pan, sd in ((2.2, 0.5, 1), (6.9, -0.6, 2), (9.5, 0.3, 3)):
        tr.add(lp(clank(0.05 + 0.02 * sd, 420, 1.6, 8900 + sd), 2500), t0, pan, 1, 0.9)
    # ---- 2. the choir: monks, 'oo', then 'oh', then the full choir
    tr.add(chorus([m('F2'), m('F3')], tr.barlen * 2 + 0.5, 0.14, 3.0, 'u'), tr.at(1), 0, 1, 0.75)
    tr.add(chorus([m('F2'), m('C3'), m('F3'), m('Ab3')], tr.barlen + 0.5, 0.24, 1.5, 'o'), tr.at(2), 0, 1, 0.7)
    tr.add(chorus([m('F2'), m('C3'), m('F3'), m('Ab3'), m('C4')], tr.barlen + 0.5, 0.32, 1.0, 'o'), tr.at(3), 0, 1, 0.7)
    tr.add(chorus([x + 12 for x in c7[:4]] + [c7[4] + 12], tr.barlen + 0.3, 0.4, 0.8, 'a'), tr.at(4), 0, 1, 0.65)
    # ---- 3. the bells: far off at first, then near
    for (bar, b), a, f, wet in (((2, 0), 0.26, 'F3', 0.85), ((3, 0), 0.36, 'F3', 0.75), ((3, 2), 0.2, 'C4', 0.75),
                                ((4, 0), 0.46, 'C3', 0.65), ((4, 2), 0.3, 'E4', 0.65), ((4, 3), 0.26, 'Db5', 0.65)):
        tr.add(great_bell(f, 6.0, a, 1.0, bar * 4 + int(b)), tr.at(bar, b), 0.3 if b else -0.15, 1, wet)
    # ---- 4. the organ swells: F minor, then the dominant (its flat ninth), crescendo into the roar
    sw = lambda sig, a0, a1: sig * np.linspace(a0, a1, len(sig))
    tr.add(sw(great_organ([m('F1'), m('F2'), m('C3'), m('F3'), m('Ab3')], tr.barlen + 0.2, 0.42, 2.5, 0.5), 0.6, 1.0), tr.at(3), 0, 1, 0.65)
    tr.add(sw(great_organ([c7[0] - 12, c7[0]] + [x + 12 for x in c7], tr.barlen, 0.55, 0.3, 1.0), 0.7, 1.35), tr.at(4), 0, 1, 0.6)
    tr.add(sub(m('C1'), tr.barlen, 0.4), tr.at(4), 0, 1, 0.1)
    for i in range(16):                                                  # (a timpani roll, swelling)
        tr.add(timp(m('C2'), 0.12 + 0.03 * i), tr.at(4, i / 4), 0, 1, 0.4)
    tr.add(suck(tr.beat * 2, 0.5), tr.at(4, 2), 0, 1, 0.3)
    # ---- 5. THE ROAR, and every chain at once
    hit = tr.at(5)
    tr.add(roar(3.0, 0.9), hit, 0, 1, 0.45)
    tr.add(boom(1.0, 100, 26, 3.2), hit, 0, 1, 0.4)
    tr.add(crash(0.55, 3.5), hit, 0.2, 1, 0.5)
    tr.add(chain_hit(1.0, 9100, 9), hit, -0.1, 1, 0.4)
    tr.add(rattle(2.2, 0.5, 60, 9101, True), hit + 0.03, -0.4, 1, 0.5)
    tr.add(rattle(2.0, 0.42, 50, 9102, True), hit + 0.12, 0.45, 1, 0.5)
    tr.add(brass([m('F2'), m('C3'), m('F3'), m('Ab3'), m('C4')], 1.3, 0.55, 2600, 0.005), hit, 0, 1, 0.4)
    tr.add(great_organ([m('F1'), m('F2')] + [x + 12 for x in fm] + [m('F4')], tr.beat * 2, 0.55, 0.01), hit, 0, 1, 0.6)
    tr.add(chorus([m('F4'), m('Ab4'), m('C5'), m('F5')], tr.beat * 1.8, 0.45, 0.04, 'a'), hit, 0, 1, 0.6)
    tr.add(great_bell('F3', 6.0, 0.6, 1.0, 9103), hit, -0.15, 1, 0.55)
    tr.add(taiko(1.0), hit, 0, 1, 0.35); tr.add(timp('F2', 0.9), hit, 0, 1, 0.4)
    # ---- 6. into the fight: the Neapolitan, a roll and a riser (form 1's own last bar), its first bell next
    tr.add(great_organ([gb[0] - 12, gb[0]] + gb[1:], tr.beat * 2.2, 0.32, 0.3, 0.4), tr.at(5, 2), 0, 1, 0.6)
    tr.add(chorus([gb[0], gb[2], gb[0] + 12], tr.beat * 2.2, 0.26, 0.4, 'u'), tr.at(5, 2), 0, 1, 0.7)
    tr.add(violin(m('Gb4'), tr.beat * 2, 0.16, trem=11, depth=0.003), tr.at(5, 2), 0.3, 1, 0.55)
    for i in range(8): tr.add(snare(0.08 + 0.035 * i, 170), tr.at(5, 2 + i / 4), 0.1, 1, 0.4)
    tr.add(rise(tr.beat * 2, 0.28), tr.at(5, 2), 0, 1, 0.35)
    tr.add(clank(0.3, 2100, 0.3, 9104), tr.at(5, 3.5), 0.3, 1, 0.4)
    tr.add(clank(0.26, 1900, 0.3, 9105), tr.at(5, 3.75), -0.3, 1, 0.4)


def intro():
    tr = Track('sovereign_intro', P1BPM, IBARS + ITAIL)                 # (three spare bars, so nothing wraps round to its silence)
    intro_compose(View(tr, P1BPM))
    return tr


def save_intro(tr, room=3.0, level=0.23):
    """the entrance: rendered with form 1's room, then cut at exactly 20 s (the last 30 ms faded) - form 1 begins there"""
    st = render(tr, room, level)
    k = int(round(IBARS * 4 * 60 / P1BPM * SR)); assert k == 20 * SR
    st = st[:, :k].copy(); f = int(0.03 * SR); st[:, -f:] *= np.linspace(1, 0, f)
    _guarded(st, os.path.join(VENDOR, f'boss_{tr.name}.ogg'), 4)


# ====================================================================== THE RECORD: the three forms condensed, and an ending
DISC_P1 = [(0, 2), (8, 16), (28, 32)]
DISC_P2 = [(0, 4), (24, 32), (36, 44), (48, 56), (68, 76)]
DISC_P3 = [(0, 16), (32, 40), (48, 52), (52, 68)]


def disc():
    plan = []
    t = 0.0
    for b0, b1 in DISC_P1: plan.append(('p1', b0, b1, t)); t += (b1 - b0) * 4 * 60 / P1BPM
    plan.append(('turn', 0, 0, t)); t += 7.0
    for b0, b1 in DISC_P2: plan.append(('p2', b0, b1, t)); t += (b1 - b0) * 4 * 60 / P2BPM
    plan.append(('turn', 0, 0, t)); t += 7.0
    for b0, b1 in DISC_P3: plan.append(('p3', b0, b1, t)); t += (b1 - b0) * 4 * 60 / P3BPM
    t_end = t
    secs = int(np.ceil(t_end + 13.0))
    secs += (4 - secs % 4) % 4
    tr = Track('sovereign_disc', 60, secs // 4)
    for kind, b0, b1, t0 in plan:
        if kind == 'turn': turn_compose(tr, t0); continue
        bpm, fn = {'p1': (P1BPM, p1_compose), 'p2': (P2BPM, p2_compose), 'p3': (P3BPM, p3_compose)}[kind]
        fn(View(tr, bpm, 4, t0, (b0, b1)), range(b0, b1))
    # ---- the ending: F# minor hammered, the bell, silence - and very faintly, a violin on the major third
    v = View(tr, P3BPM, 4, t_end)
    ch = chd('F#2', 'm'); r = ch[0]
    for b in (0, 0.5, 1, 1.5, 2):
        v.add(brass([r - 12, r - 5, r, ch[1]], v.beat * 0.4, 0.5, 1800, 0.006), v.at(0, b), 0, 1, 0.3)
        v.add(kick(0.9), v.at(0, b), 0, 1, 0.05)
        v.add(chain_hit(0.4, 9000 + int(b * 2), 5, False), v.at(0, b), 0.2, 1, 0.35)
    v.add(great_organ([r - 12, r] + [x + 12 for x in ch] + [r + 24], v.beat * 14, 0.5, 0.02), v.at(0, 2), 0, 1, 0.7)
    v.add(chorus([x + 12 for x in ch] + [r + 24], v.beat * 14, 0.46, 0.15, 'a'), v.at(0, 2), 0, 1, 0.7)
    v.add(timp('F#2', 0.9), v.at(0, 2), 0, 1, 0.4); v.add(crash(0.5, 3.5), v.at(0, 2), 0.2, 1, 0.45)
    v.add(boom(0.6, 90, 30, 3.0), v.at(0, 2), 0, 1, 0.4)
    v.add(great_bell('F#3', 7.5, 0.6, 1.0, 9), v.at(0, 2), -0.1, 1, 0.65)
    v.add(violin('F#6', v.beat * 12, 0.34, trem=14), v.at(0, 2), 0.1, 1, 0.5)
    v.add(great_bell('F#4', 6.5, 0.3, 0.8, 10), v.at(4, 0), 0.2, 1, 0.75)
    v.add(violin('A#5', 3.6, 0.13, depth=0.01, attack=0.9, bright=0.5), v.at(4, 2), 0.1, 1, 0.75)       # (Aurel, listening)
    v.add(soft_organ(['F#3', 'A#3', 'C#4'], 4.0, 0.12, 1.5, 1.8), v.at(4, 2), 0, 1, 0.7)
    tr.disc_seconds = secs
    return tr


# ====================================================================== AUREL: an elegy for the first light
AU_PROG = ([('D3', 'm'), ('E2', 'hd'), ('A2', '7'), ('D3', 'm'), ('Bb2', 'M'), ('F2', 'M'), ('G2', 'm'), ('A2', 'M')] +
           [('F2', 'M'), ('C3', 'M'), ('C3', 'M'), ('F2', 'M'), ('Bb2', 'M'), ('F2', 'M'), ('C3', '7'), ('F2', 'M')] +
           [('Bb2', 'M'), ('C3', 'M'), ('A2', 'm'), ('D3', 'm'), ('G2', 'm'), ('Bb2', 'M'), ('C3', 'M'), ('C3', '7')] +
           [('F2', 'M'), ('C3', 'M'), ('D3', 'm'), ('Bb2', 'M'), ('F2', 'M'), ('G2', 'm'), ('C3', 'M'), ('D3', 'm')] +
           [('Bb2', 'M'), ('Bb2', 'm'), ('G2', 'm'), ('C3', '7'), ('F2', 'M'), ('F2', 'M')])
AU_A = mel('A4 D5 F5 E5:2 D5 C#5:2 D5 A4:3 D5 F5 Bb5 A5:2 G5 F5 E5 D5 E5:3')                  # (the cell in D minor - grief)
AU_L = mel('C5 F5 A5 G5:2 F5 E5:2 F5 C5:3 D5 F5 Bb5 C6:2 A5 G5 Bb5 E5 F5:3')                  # (the cell in F major - the light)
AU_B = mel('F5 Bb5 D6 E6:2 D6:.5 C6:.5 C6:2 A5 D6:3 Bb5 D6 G6 F6:2 D6 E6:1.5 F6:.5 G6 G6:3')    # (it climbs, once)
AU_R = mel('A6:1.5 G6:.5 F6 E6 D6 C6 D6:1.5 C6:.5 A5 Bb5:2 A5:.5 G5:.5 A5 C6 F6 D6:2 Bb5 G5 A5:.5 Bb5:.5 E5 F5:2 D5')
AU_C = mel('F5 Bb5 D6 Db6:2 C6 Bb5:1.5 A5:.5 G5 F5:2 E5 F5:6')                                 # (the minor iv, and home)
for _x in (AU_A, AU_L, AU_B, AU_R):
    assert bars_of(_x, 3) == 8, bars_of(_x, 3)
assert bars_of(AU_C, 3) == 6


def aurel():
    tr = Track('aurel', ABPM, ABARS, beats=3)
    assert round(tr.seconds) == 120
    v = View(tr, ABPM, 3)
    INTRO, LAST = 2, 38                                                 # (the organ alone for two bars; the last chord at 38)
    for bar in range(LAST + 1):
        ch = chd(*([('F2', 'M'), ('A2', '7')][bar] if bar < INTRO else AU_PROG[bar - INTRO]))
        r = ch[0]
        last = bar == LAST                                               # (the final F major: held three bars, then let go)
        dur = v.barlen * (3 if last else 1) + 0.6
        voicing = [r - 12 if r > m('C3') else r, ch[1] + 12, ch[2] + 12] + ([ch[3] + 12] if len(ch) > 3 else []) + ([r + 24] if bar % 2 == 0 or last else [])
        v.add(soft_organ(voicing, dur, 0.38 if last else 0.34, 1.2 if bar == 0 else 0.6, 3.5 if last else 1.4), v.at(bar), 0, 1, 0.6)
        if last:
            v.add(soft_organ([r - 12], v.barlen * 3, 0.2, 1.0, 3.5), v.at(bar), 0, 1, 0.5)
    sing = lambda amp, dep=0.009: (lambda x, d: violin(x, d, amp, vib=5.2, depth=dep, attack=0.11, scoop=0.008, bright=0.85))
    ply(v, v.at(2), AU_A, sing(0.36), 0.05, 1, 0.55)
    ply(v, v.at(10), AU_L, sing(0.38), 0.05, 1, 0.55)
    ply(v, v.at(18), AU_B, sing(0.42, 0.01), 0.05, 1, 0.55)
    ply(v, v.at(26), AU_R, sing(0.4), 0.05, 1, 0.55)
    ply(v, v.at(34), AU_C, sing(0.34), 0.05, 1, 0.6, legato=0.98)
    v.add(great_bell('F5', 8.0, 0.08, 0.6, 3), v.at(38, 1), 0.3, 1, 0.8)                 # (the light, very far up)
    v.add(violin('A6', v.barlen * 2.6, 0.07, vib=4.6, depth=0.006, attack=1.2, bright=0.4), v.at(38, 2), -0.2, 1, 0.8)
    return v


# ====================================================================== saving (and the listening-check)
def _decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    ch = int(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=channels', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())
    return np.frombuffer(raw, np.float32).reshape(-1, ch).T


def _encode(x, out, q, mono=False):
    fd, wav = tempfile.mkstemp(suffix='.wav'); os.close(fd)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1 if mono else 2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(((x if mono else x.T) * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav] + (['-ac', '1'] if mono else []) + ['-c:a', 'libvorbis', '-q:a', str(q), out], check=True)
    os.remove(wav)


def _guarded(x, out, q, mono=False, ceil=0.97):
    """encode; if the decoded file peaks over the ceiling (Vorbis overshoots a tanh-rounded mix), trim it and encode again"""
    for _ in range(4):
        _encode(x, out, q, mono)
        pk = float(np.abs(_decode(out)).max())
        if pk <= ceil: break
        x = x * (ceil * 0.995 / pk)
    print(f'{out}: {len(x if mono else x[0]) / SR:.1f} s, peak {20 * np.log10(pk):.2f} dBFS, {os.path.getsize(out) // 1024} KB')


def render(tr, room=1.8, level=0.21, bright=5000):
    """gv_music's Track.render (circular reverb, every track to one loudness, peaks rounded off by a tanh) - with that
    loudness as a parameter: a piece with a hollow in it (the TRUE form's void) is pushed so its fight is as loud as the rest"""
    from scipy.signal import fftconvolve
    n = tr.n
    ir_t = np.arange(int(room * SR)) / SR
    irs = [lp(R.noise(len(ir_t)) * np.exp(-ir_t * 6.9 / room), bright) * 0.12 for _ in range(2)]
    def circ(x, ir):
        y = fftconvolve(np.concatenate([x, x[:len(ir)]]), ir)[:n + len(ir)]
        out = y[:n].copy(); out[:len(ir)] += y[n:n + len(ir)]
        return out
    st = np.stack([tr.L + circ(tr.wetL, irs[0]), tr.R + circ(tr.wetR, irs[1])])
    rms = np.sqrt((st ** 2).mean())
    return (np.tanh(st * (level / rms)) * 0.92).astype(np.float32)


def save_loop(tr, room=2.4, level=0.21):
    """a battle loop: rendered circularly, stereo, the same loudness as every other theme"""
    _guarded(render(tr, room, level), os.path.join(VENDOR, f'boss_{tr.name}.ogg'), 0)


def save_sting(tr, room=2.2, level=0.21):
    """played once (the turn): its last second faded so no tail wraps round"""
    st = render(tr, room, level)
    k = int(1.0 * SR); st[:, -k:] *= np.linspace(1, 0, k)
    _guarded(st, os.path.join(VENDOR, f'boss_{tr.name}.ogg'), 4)


def save_disc(tr, name, room=2.4, rms_db=None):
    """a record: mono, as disc_music.save_mono (a soft start, the peak at -0.9 dBFS) - or, for a quiet one, brought down to
    a loudness (rms_db)"""
    st = render(tr, room)
    mono = (st[0] + st[1]) * 0.5
    k = int(1.5 * SR); mono[:k] *= np.linspace(0, 1, k) ** 0.5
    mono = mono / (np.abs(mono).max() + 1e-9) * 0.9
    if rms_db is not None:
        mono = mono * min(1.0, 10 ** (rms_db / 20) / np.sqrt((mono ** 2).mean()))
    _guarded(mono, os.path.join(VENDOR, f'disc_{name}.ogg'), 3, mono=True)


def check(names=('boss_sovereign_intro', 'boss_sovereign1', 'boss_sovereign2', 'boss_sovereign3', 'boss_sovereign_turn', 'disc_sovereign', 'disc_aurel',
                 'boss_dread', 'boss_dread2', 'disc_dread')):
    """levels (RMS, peak), clipping, and the loop seam: the jump across the wrap against the music's own steps, and the
    loudness either side of it"""
    db = lambda v: 20 * np.log10(max(float(v), 1e-9))
    for nm in names:
        p = os.path.join(VENDOR, f'{nm}.ogg')
        if not os.path.exists(p): continue
        x = _decode(p); n = x.shape[1]
        rms, pk = np.sqrt((x ** 2).mean()), np.abs(x).max()
        clip = int((np.abs(x) >= 0.999).sum())
        step = np.percentile(np.abs(np.diff(x, axis=1)), 99.9)
        seam = np.abs(x[:, 0] - x[:, -1]).max()
        h = SR // 4
        e1, e0 = np.sqrt((x[:, -h:] ** 2).mean()), np.sqrt((x[:, :h] ** 2).mean())
        print(f'{nm:22s} {n / SR:6.1f} s  ch{x.shape[0]}  RMS {db(rms):6.1f} dBFS  peak {db(pk):5.1f}  clipped {clip}  '
              f'seam jump {seam:.3f} (99.9% step {step:.3f})  last/first 0.25 s {db(e1):5.1f}/{db(e0):5.1f} dB')


def seeded(k, build, *a):
    """each piece from its own seed, so it renders the same alone or with the rest"""
    R.g = np.random.default_rng(2980 + k)
    return build(*a)


if __name__ == '__main__':
    what = sys.argv[1:] or ['p1', 'p2', 'p3', 'turn', 'intro', 'enter2', 'enter3', 'divine', 'disc', 'aurel', 'check']
    if 'p1' in what: save_loop(seeded(1, p1), 3.0, 0.23)
    if 'p2' in what: save_loop(seeded(2, p2), 2.2)
    if 'p3' in what: save_loop(seeded(3, p3), 2.6, 0.27)                # (the most intense: its fight hotter than the Dread's)
    if 'turn' in what: save_sting(seeded(4, turn), 2.4, 0.31)
    if 'intro' in what: save_intro(seeded(5, intro))
    if 'enter2' in what: save_sting(seeded(8, enter2), 2.4, 0.31)
    if 'enter3' in what: save_sting(seeded(9, enter3), 2.4, 0.31)
    if 'divine' in what: save_sting(seeded(10, divine), 3.2, 0.22)
    if 'disc' in what:
        d = seeded(6, disc); assert 170 <= d.seconds <= 200, d.seconds
        save_disc(d, 'sovereign', 2.6)
    if 'aurel' in what: save_disc(seeded(7, aurel).tr, 'aurel', 3.2, -17.0)                 # (quiet: the Lament's record's level)
    if 'check' in what: check()
