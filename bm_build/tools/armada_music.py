"""2.99: synthesises THE VORN ARMADA's soundtrack - the hive-fleet's own music, from the Dock to the Flagship's door
(vendor/ar_*.ogg). Not the Undercrown's strings: machines and a mind. Analog-synth arpeggios through resonant filters, a pulsing
sequencer, deep sub-bass, a THEREMIN for the lead (one continuous voice, gliding note to note), synth-brass stabs and horns, a
wordless HIVE CHOIR (formant-synth voices, many throats on one breath, a ring of something inhuman in them), and metallic
percussion - struck hull plates, servo-clanks, pistons, ring-modulated hats.

ONE GRID FOR EVERY TRACK, SO THEY JOIN WITHOUT A SEAM. D minor (its flat second, Eb, is the hive's colour), 160 BPM, 4/4 - a bar
is 1.5 s, two bars exactly 3 s; the early tiers feel it in half time (80). Every track is built of 8-bar sections (12 s); every
section starts on D minor and ends on a chord that leads back to it. phase244 switches from one tier to the next only on a section
boundary, with THE SWELL (ar_swell, 3 s - two bars: a reversed cymbal, a riser, the choir sliding up, a roll) over the last two
bars - one track turns into the next as if it were the same piece turning a page. A fight cuts in on the next two-bar line, on
its own downbeat (an impact); it hands back on a section boundary, through the swell.

THE ADMIRAL'S THEME V (D A Bb-A G#-A F E Eb D ...; tools/vexis_music.py) runs through all of it - slow and far off on the Dock, a
march by the Dreadnoughts - so the boss's music, when it comes, is where the fleet was going. THE CALL (D-A-Eb: a fifth, then the
flat ninth above it) is the hive's own signal, and the choir sends it everywhere. Each tier is louder and fuller than the last.

  ar_t1  I.   THE DOCK              96 s  the arrival frigate. A hum, sonar pings, the hull creaking; a sequencer ticking in the
                                          sub; the theremin carries V slow (half time), the choir far off answers with THE CALL
  ar_t2  II.  THE BROOD-CARRIER    120 s  the bio-labs. Specimen tanks bubbling, an acid bass squelching, the choir 'oo' turning
                                          to 'ah'; the brood melody (B) for theremin; the half-time drums wake
  ar_t3  III. THE STAR-FORGE       120 s  the foundry. The forge riff (a driven saw, a tritone in it), anvils on two and four,
                                          pistons, the drums driving; V in the horns, stabs, the arpeggiator opening up
  ar_t4  IV.  THE NAVIGATOR        120 s  the observatory, low gravity. Shimmering arpeggios with long echoes, star-bells, the
                                          navigator's theme (N, a wide one, lydian); V; a zero-G break where the floor drops away
  ar_t5  V.   THE DREADNOUGHTS     120 s  the warships and the Flagship, until it wakes. Everything: alarms, the double-kick
              AND THE FLAGSHIP            march, V in the brass in octaves, the choir hammering "COMPLY", the theremin wailing at
                                          the top - once, a hush before the bridge (the red window), and then the end
  ar_c1  THE BOARDERS               60 s  a fight on the early ships: the drums driving, 16th sequencer, stabs, V at double speed
  ar_c2  THE DREADNOUGHT GUARD      60 s  a fight from the Dreadnoughts on: double-kick, the riff driven harder, brass V in
                                          octaves, lasers, the choir's COMPLY
  ar_swell                          3 s  the page turn
(After the fall, phase244 plays the Unlinking's last part - vendor/ar_after.ogg, tools/vexis_music.py - once: the one voice left.)

Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg):
    python3 tools/armada_music.py [t1 t2 t3 t4 t5 c1 c2 swell] [check] [journey]"""
import os, sys
import numpy as np
from scipy.signal import lfilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, mix, T, env, lp, hp, bp, sub, riser, tom
from boss_music import timp, crash, mel, tp, bars_of, laser
from sovereign_music import (clank, boom, suck, edge, drone, whisper, gaze, glass, dur_x, ladder, render, _guarded, _decode, _encode,
                             seeded, View)

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
BPM = 160                                   # (a bar: 1.5 s; two bars 3 s; a section: 8 bars, 12 s)
SEC = 8
LEN = {'t1': 64, 't2': 80, 't3': 80, 't4': 80, 't5': 80, 'c1': 40, 'c2': 40}      # (bars)


# ====================================================================== the harmony
IVS = {'m': (0, 3, 7), 'M': (0, 4, 7), 'dim': (0, 3, 6), '7': (0, 4, 7, 10), '7b9': (0, 4, 7, 10, 13), 'm7': (0, 3, 7, 10),
       'M7': (0, 4, 7, 11), 'sus': (0, 5, 7), 'hd': (0, 3, 6, 10), 'wt': (0, 2, 4, 6, 8, 10), 'aug': (0, 4, 8), 'm9': (0, 3, 7, 10, 14),
       'M7#11': (0, 4, 7, 11, 18), 'add9': (0, 4, 7, 14), 'phr': (0, 1, 7), 'mt': (0, 3, 6, 7), 'sus2': (0, 2, 7), 'm6': (0, 3, 7, 9)}


def ch(c, k=0):
    root, kind = c
    r = (m(root) if isinstance(root, str) else int(root)) + k
    return [r + i for i in IVS[kind]]


def M(x):
    return int(x) if isinstance(x, (int, np.integer)) else m(x)


P_DOCK = [('D2', 'm'), ('D2', 'm'), ('Eb2', 'M'), ('Eb2', 'M'), ('D2', 'm'), ('D2', 'm'), ('Bb1', 'M'), ('A1', '7')]       # (the hum: D and its b2)
P_V = [('D2', 'm'), ('Bb1', 'M'), ('G1', 'm'), ('D2', 'm'), ('D2', 'm'), ('C2', 'm'), ('Eb2', 'M'), ('A1', '7')]            # (under V)
P_BROOD = [('D2', 'm'), ('Eb2', 'M'), ('Bb1', 'M'), ('G1', 'm'), ('F2', 'M'), ('E2', '7'), ('A1', 'sus'), ('A1', 'M')]     # (under B)
P_FORGE = [('D2', 'm'), ('D2', 'm'), ('C2', 'M'), ('C2', 'M'), ('Bb1', 'M'), ('Bb1', 'M'), ('Eb2', 'M'), ('A1', '7')]      # (the foundry)
P_NAV = [('D2', 'm'), ('C2', 'M'), ('F2', 'M'), ('Bb1', 'M7#11'), ('D2', 'm'), ('C2', 'M'), ('Bb1', 'M7#11'), ('A1', 'M')]   # (under N)
P_WAR = [('D2', 'm'), ('D2', 'm'), ('Bb1', 'M'), ('C2', 'M'), ('D2', 'm'), ('D2', 'm'), ('Eb2', 'M'), ('A1', '7b9')]       # (war)

# ====================================================================== the tunes
V = mel('D4:2 A4:2 Bb4:1.5 A4:.5 G#4 A4 F4:2 E4 Eb4 D4:4 D4 F4 A4 D5 Eb5:2 D5 C5 Bb4:1.5 A4:.5 G4 Eb4 A4:4')   # (the Admiral: 8 bars)
CALL = mel('D5:3 A5:1 Eb6:4')                                                                                   # (the hive's signal: 2 bars)
B = mel('D5:4 Eb5:4 D5:2 C5:2 Bb4:4 A4:4 G#4:4 A4:8')                                                            # (the brood: 8 bars)
N = mel('A4:2 D5:2 E5:1.5 F5:.5 E5:2 C5:2 D5 A4 Bb4:4 A4:2 F5:2 G5:1.5 A5:.5 G5:2 F5 E5 D5:2 C#5:2 A4:2')        # (the navigator: 8 bars)
V2 = dur_x(V, 2.0)                 # (16 bars: the Dock's slow V)
VF = dur_x(V, 0.5)                 # (4 bars: V at the fight's speed)
for _x, _b in ((V, 8), (CALL, 2), (B, 8), (N, 8), (V2, 16), (VF, 4)):
    assert bars_of(_x) == _b, (_b, bars_of(_x))


# ====================================================================== oscillators and the filter
def _blep(ph, dt):
    out = np.zeros_like(ph)
    a = ph < dt
    x = ph[a] / dt[a]; out[a] = x + x - x * x - 1
    b = ph > 1 - dt
    x = (ph[b] - 1) / dt[b]; out[b] = x * x + x + x + 1
    return out


def osc(fr, kind='saw', duty=0.5, ph0=None):
    """a band-limited (polyBLEP) oscillator over a frequency curve (Hz, one value a sample): 'saw', 'pulse' (duty), 'tri'"""
    fr = np.asarray(fr, float)
    dt = np.clip(fr / SR, 1e-6, 0.45)
    ph = (np.cumsum(dt) + (R.r() if ph0 is None else ph0)) % 1.0
    s = 2 * ph - 1 - _blep(ph, dt)
    if kind == 'saw':
        return s
    if kind == 'tri':
        return 2 * np.abs(2 * ph - 1) - 1
    p2 = (ph + duty) % 1.0
    return s - (2 * p2 - 1 - _blep(p2, dt))


def _lpc(fc, q):
    w = 2 * np.pi * min(max(fc, 20.0), SR * 0.45) / SR
    cw, al = np.cos(w), np.sin(w) / (2 * q)
    a0 = 1 + al
    return np.array([(1 - cw) / 2, 1 - cw, (1 - cw) / 2]) / a0, np.array([1.0, -2 * cw / a0, (1 - al) / a0])


def vlp(x, fc, q=0.707, poles=4, blk=64):
    """a resonant low-pass whose cut-off may move (an array, one value a sample): two biquads (24 dB), the resonance on the first"""
    stages = [q] + ([0.707] if poles == 4 else [])
    if np.isscalar(fc):
        y = x
        for qq in stages: y = lfilter(*_lpc(fc, qq), y)
        return y
    y = np.empty_like(x)
    zs = [np.zeros(2) for _ in stages]
    n = len(x)
    for i in range(0, n, blk):
        seg = x[i:i + blk]
        f = fc[min(i + blk // 2, n - 1)]
        for k, qq in enumerate(stages):
            b, a = _lpc(f, qq)
            seg, zs[k] = lfilter(b, a, seg, zi=zs[k])
        y[i:i + blk] = seg
    return y


def smooth(x, sec):
    """a one-pole smoother (glides, envelopes)"""
    a = 1 - np.exp(-1.0 / max(1.0, sec * SR))
    y, _ = lfilter([a], [1, -(1 - a)], x, zi=[x[0] * (1 - a)])
    return y


# ====================================================================== the synths (mono)
def mono(f, dur, amp=1.0, wave='saw', cut=600, sweep=2400, fdec=9.0, q=1.6, det=0.007, subosc=0.0, a=0.003, d=0.12, s=0.6, r=0.04,
         drive=0.0, duty=0.5, glide_from=None, glide=0.04, poles=4):
    """the analog mono-synth: two detuned oscillators (and a sub an octave down), a resonant 24 dB low-pass whose cut-off is
    flung open on the note and falls back, an amp envelope - an arpeggiator's pluck, a sequencer's pulse, a driven riff"""
    f1 = fq(f); t = T(dur); n = len(t)
    if n < 8: return np.zeros(8)
    fr = np.full(n, f1)
    if glide_from is not None:
        f0 = fq(glide_from); fr = f1 * (f0 / f1) ** np.exp(-t / glide)
    sg = osc(fr, wave, duty) + osc(fr * (1 + det), wave, duty) * 0.8
    if subosc: sg += subosc * osc(fr * 0.5, 'pulse', 0.5)
    sg /= 1.8 + subosc
    fc = cut + sweep * np.exp(-t * fdec)
    y = vlp(sg, fc, q, poles)
    if drive: y = np.tanh(y * drive) / np.tanh(drive)
    return amp * y * env(n, a, d, s, r)


def apad(notes, dur, amp=1.0, cut=1400, attack=0.9, release=1.2, voices=3, det=0.009, lfo=0.13, depth=0.4, q=1.3, wave='saw', duty=0.5):
    """the analog pad: detuned saws (or pulses), a slow filter breathing on an LFO"""
    t = T(dur); n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = hz(M(x))
        for v in range(voices):
            k = v - (voices - 1) / 2
            s += osc(np.full(n, f * (1 + det * k)) * (1 + 0.0015 * np.sin(2 * np.pi * (0.3 + 0.1 * v) * t)), wave, duty)
    s /= len(notes) * voices
    fc = cut * (1 + depth * np.sin(2 * np.pi * lfo * t + R.r() * 6.28))
    return amp * vlp(s, fc, q, 2, 128) * env(n, attack, 0, 1, release)


def horn(notes, dur, amp=1.0, bright=2600, close=700, swell=0.07, vib=5.2, scoop=0.35, q=1.0):
    """synth brass, held: detuned saws, the filter opening as the note speaks (a scoop up into the pitch), a late vibrato"""
    t = T(dur); n = len(t)
    if n < 8: return np.zeros(8)
    s = np.zeros(n)
    rise_ = 1 - np.exp(-t / max(swell, 0.01))
    vb = 1 + 0.004 * np.sin(2 * np.pi * vib * t) * np.clip((t - 0.3) * 2, 0, 1)
    for x in notes:
        f = hz(M(x))
        fr = f * 2 ** (-scoop / 12 * np.exp(-t * 25)) * vb
        for v in (-0.006, 0.0, 0.005):
            s += osc(fr * (1 + v))
    s /= len(notes) * 3
    fc = close + (bright - close) * rise_ * (0.75 + 0.25 * np.exp(-t * 1.5))
    y = np.tanh(1.4 * vlp(s, fc, q, 2, 96))
    return amp * y * env(n, swell * 0.6, 0.3, 0.8, 0.09)


def stab(notes, dur, amp=1.0, bright=6000, close=600, fdec=10.0, scoop=0.3):
    """a brass stab: a hard blat, the filter slamming shut"""
    t = T(dur); n = len(t)
    if n < 8: return np.zeros(8)
    s = np.zeros(n)
    for x in notes:
        f = hz(M(x))
        fr = f * 2 ** (-scoop / 12 * np.exp(-t * 40))
        for v in (-0.007, 0.0, 0.007):
            s += osc(fr * (1 + v))
    s /= len(notes) * 3
    fc = close + (bright - close) * np.exp(-t * fdec)
    y = np.tanh(1.8 * vlp(s, fc, 1.2, 2, 64))
    return amp * y * env(n, 0.004, 0.18, 0.45, 0.06)


def ther_line(notes, beat, amp=0.3, port=0.07, vib=6.3, depth=0.012, legato=0.97, k=0, bright=0.2, dip=0.2):
    """THE THEREMIN: one continuous voice over a whole line - the pitch gliding from note to note (never quite landing at once),
    a vibrato that blooms on every held note, the volume hand swelling each one in and dipping between them; a sine with a
    little of its octave and twelfth, a breath of the instrument's own grain"""
    total = sum(d for _, d in notes) * beat
    n = int((total + 0.35) * SR)
    tgt = np.zeros(n); gate = np.zeros(n); onset = np.zeros(n)
    t = 0.0; last = None
    first = next((M(x) for x, _ in notes if x is not None), 60)
    tgt[:] = first + k
    for x, d in notes:
        i0, i1 = int(t * SR), int((t + d * beat) * SR)
        if x is not None:
            last = M(x) + k
            tgt[i0:] = last
            i2 = int((t + d * beat * legato) * SR)
            gate[i0:i2] = 1.0
            onset[i0:i1] = np.arange(i1 - i0) / SR
            if dip and i2 > i0 + 200: gate[i0:i0 + int(0.025 * SR)] = 1 - dip       # (the hand, re-shaping each note)
        else:
            onset[i0:i1] = 0
        t += d * beat
    midi = smooth(tgt, port)
    tt = np.arange(n) / SR
    vb = depth * np.clip(onset / 0.35, 0, 1) * np.sin(2 * np.pi * vib * tt + 0.7)
    fr = 440.0 * 2 ** ((midi - 69) / 12) * (1 + vb)
    ph = np.cumsum(fr) / SR
    s = np.sin(2 * np.pi * ph) + 0.16 * np.sin(4 * np.pi * ph + 0.4) + 0.06 * np.sin(6 * np.pi * ph + 1.1)
    if bright: s += bright * np.tanh(3 * np.sin(2 * np.pi * ph)) * 0.25
    g = smooth(smooth(gate, 0.035), 0.02)
    return amp * 0.45 * s * g


def addc(tr, sig, t, pan=0.0, gain=1.0, wet=0.3):
    """add a long sound to a track - or, in a window of a piece (a record's excerpt, sovereign_music.View), only the part of
    it inside the window (cut with a short fade at its end), even if it starts a moment before it"""
    win = getattr(tr, 'win', None)
    if win is None:
        return tr.add(sig, t, pan, gain, wet)
    w0, w1 = tr.t0, tr.t0 + tr.span
    if t >= w1 - 1e-6 or t + len(sig) / SR <= w0 or t < w0 - 1.5: return
    k = int((w1 - t) * SR)
    if k < len(sig):
        sig = sig[:k].copy(); f = min(k, int(0.04 * SR)); sig[-f:] *= np.linspace(1, 0, f)
    tr.tr.add(sig, t, pan, gain, wet)


def ther(tr, t0, notes, amp=0.3, pan=0.0, wet=0.45, echo_=True, **k):
    """a theremin line into a track, with a dotted-eighth echo trailing it"""
    s = ther_line(notes, tr.beat, amp, **k)
    addc(tr, s, t0, pan, 1, wet)
    if echo_:
        e = lp(s, 2600)
        for i in (1, 2):
            addc(tr, e, t0 + tr.beat * 0.75 * i, -pan + (0.5 if i % 2 else -0.5), 0.3 ** i, min(0.9, wet + 0.25))


VOW = {'a': (730, 1090, 2440), 'e': (530, 1840, 2480), 'i': (300, 2200, 2950), 'o': (570, 840, 2410), 'u': (330, 800, 2240)}


def _formants(s, v, gains=(1.0, 0.5, 0.22)):
    return sum(bp(s, f * 0.86, f * 1.14, 1) * g for f, g in zip(VOW[v], gains))


def hive(notes, dur, amp=1.0, vowel='u', to=None, attack=0.7, release=0.9, voices=5, vib=4.6, alien=0.22, gate=0.0, rate=0.0, drift=0.006):
    """THE HIVE CHOIR: formant-synth voices - many throats on one breath (glottal saws, each a hair off the pitch, drifting),
    shaped into a vowel (and morphing to another as it holds), a ring of something inhuman under it (a ring-modulated copy at
    a fifth and a hair), and - for the hive's chatter - a pulse gating the breath"""
    t = T(dur); n = len(t)
    if n < 8: return np.zeros(8)
    s = np.zeros(n)
    for x in notes:
        f = hz(M(x))
        for v in range(voices):
            dv = drift * (v - (voices - 1) / 2) / max(1, (voices - 1) / 2)
            fr = f * (1 + dv) * (1 + 0.0065 * np.sin(2 * np.pi * (vib + 0.37 * v) * t + R.r() * 6.28))
            s += osc(fr)
    s /= len(notes) * voices
    y = _formants(s, vowel)
    if to:
        w = np.clip(t / max(dur * 0.85, 0.1), 0, 1); w = w * w * (3 - 2 * w)
        y = y * (1 - w) + _formants(s, to) * w
    if alien:
        f0 = hz(M(notes[0]))
        y = y + alien * bp(y * np.sin(2 * np.pi * f0 * 1.503 * t), 300, 4000, 1)
    if gate:
        y = y * (1 - gate * (0.5 - 0.5 * np.cos(2 * np.pi * rate * t)))
    return amp * 5.0 * y * env(n, attack, 0, 1, release)


# ====================================================================== percussion and machines
def ekick(amp=1.0, dec=7.0, f0=160.0, f1=43.0, sweep=32.0, drive=1.8, dur=0.55):
    """the hull drum: a deep sine thump, driven"""
    t = T(dur)
    fr = f1 + (f0 - f1) * np.exp(-t * sweep)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * dec)
    s = np.tanh(s * drive) / np.tanh(drive)
    s[:90] += hp(R.noise(90), 2000) * np.linspace(0.5, 0, 90)
    return amp * s * env(len(t), 0.001, 0, 1, 0.05)


def esnare(amp=1.0, tone=182.0, ring=0.4, dec=13.0):
    """a snare with a struck plate in it: noise, a body, two inharmonic rings"""
    t = T(0.38); n = len(t)
    nz = bp(R.noise(n), 1400, 8500) * np.exp(-t * dec)
    body = np.sin(2 * np.pi * tone * t * (1 + 0.15 * np.exp(-t * 40))) * np.exp(-t * 24)
    rg = (np.sin(2 * np.pi * 563 * t) + 0.7 * np.sin(2 * np.pi * 847 * t + 1) + 0.4 * np.sin(2 * np.pi * 1291 * t)) * np.exp(-t * 16)
    return amp * (nz * 0.85 + body * 0.5 + ring * rg * 0.35) * env(n, 0.0008, 0, 1, 0.04)


_HATF = (205.3, 304.4, 369.6, 522.7, 540.0, 800.0)


def mhat(amp=1.0, open_=False, f=1.0):
    """a metal hat: six square waves at clashing ratios (the old machines' cymbal), only their top left"""
    t = T(0.42 if open_ else 0.07); n = len(t)
    s = sum(osc(np.full(n, x * f * 1.6), 'pulse', 0.5, 0.13 * i) for i, x in enumerate(_HATF)) / 6
    s = hp(bp(s, 5200, 10500, 2), 6000)
    return amp * 9.0 * s * np.exp(-t * (7 if open_ else 55)) * env(n, 0.0005, 0, 1, 0.02)


_PLATE = ((1.0, 1.0, 1.6), (1.594, 0.8, 2.0), (2.136, 0.7, 2.6), (2.296, 0.55, 2.8), (2.653, 0.45, 3.4), (2.918, 0.35, 3.8),
          (3.156, 0.3, 4.4), (3.501, 0.25, 5.0), (4.06, 0.18, 6.0))


def hull(amp=1.0, f=96.0, ring=1.0, seed=0, thump=1.0):
    """the hull struck: a great steel plate's inharmonic modes ringing out over a thud - the fleet's bass drum and its bell"""
    g = np.random.default_rng(int(seed))
    t = T(0.6 + 1.8 * ring); n = len(t)
    s = np.zeros(n)
    for ratio, a, dec in _PLATE:
        fk = f * ratio * (1 + 0.01 * g.standard_normal())
        if fk > SR / 2 - 500: continue
        s += a * np.sin(2 * np.pi * fk * t * (1 - 0.004 * np.exp(-t * 6)) + 6.28 * g.random()) * np.exp(-t * dec / ring)
    s += thump * lp(R.noise(n), 260) * np.exp(-t * 14) * 2.0
    s += hp(R.noise(n), 3000) * np.exp(-t * 70) * 0.5
    return amp * s * env(n, 0.0008, 0, 1, 0.1) / 2.4


def ping(f, amp=1.0, dur=2.2):
    """sonar: a pure tone, sagging a little as it dies"""
    f = fq(f); t = T(dur)
    fr = f * (1 - 0.006 * (1 - np.exp(-t * 2)))
    ph = np.cumsum(fr) / SR
    s = np.sin(2 * np.pi * ph) + 0.2 * np.sin(4 * np.pi * ph) * np.exp(-t * 4)
    return amp * s * np.exp(-t * 2.3) * env(len(t), 0.004, 0, 1, 0.1)


def sbell(f, dur=2.5, amp=1.0):
    """a star-bell: FM, glassy, slow"""
    f = fq(f); t = T(dur)
    s = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 2.5) * np.sin(2 * np.pi * f * 3.51 * t))
    s += 0.3 * np.sin(2 * np.pi * f * 2.003 * t) * np.exp(-t * 3)
    return amp * s * np.exp(-t * 1.6) * env(len(t), 0.002, 0, 1, 0.2)


def servo(dur, amp=1.0, f0=180.0, f1=420.0):
    """a servo whining as it moves: a pulse gliding, through a nasal band"""
    t = T(dur); n = len(t)
    u = np.clip(t / dur, 0, 1); fr = f0 * (f1 / f0) ** (u * u * (3 - 2 * u))
    s = osc(fr, 'pulse', 0.3) + 0.5 * osc(fr * 2.01, 'saw')
    s = bp(s, 600, 3000, 1) + 0.2 * hp(R.noise(n), 4000)
    return amp * s * env(n, 0.04, 0, 1, 0.08) * 0.6


def piston(amp=1.0):
    """a piston: a thunk, then the steam let go"""
    t = T(0.7); n = len(t)
    th = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 18)
    hs = hp(R.noise(n), 3500) * np.exp(-((t - 0.25) / 0.16) ** 2) * 0.6
    return amp * (th + hs) * env(n, 0.001, 0, 1, 0.05)


def creak(dur, amp=1.0, f=60.0, seed=0):
    """the hull straining: a slow stick-slip groan"""
    g = np.random.default_rng(seed)
    t = T(dur); n = len(t)
    fr = f * (1 + 0.25 * np.sin(2 * np.pi * g.uniform(0.2, 0.5) * t + g.random() * 6))
    s = osc(fr, 'pulse', 0.12) * (0.5 + 0.5 * np.sin(2 * np.pi * g.uniform(9, 17) * t) ** 2)
    s = bp(s, 300, 1600, 1)
    return amp * s * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2


def blip(f, amp=1.0, up=7):
    """a specimen tank's bubble: a short sine blip, sliding up"""
    f = fq(f); t = T(0.14)
    fr = f * 2 ** (up / 12 * (1 - np.exp(-t * 30)))
    return amp * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 26) * env(len(t), 0.002, 0, 1, 0.02)


def zap(amp=1.0, f0=3000.0, f1=200.0, dur=0.4):
    t = T(dur)
    ph = np.cumsum(f0 * (f1 / f0) ** (t / dur)) / SR
    s = np.sin(2 * np.pi * ph + 2.0 * np.sin(2 * np.pi * ph * 0.5))
    return amp * s * np.exp(-t * 5) * env(len(t), 0.002, 0, 1, 0.03)


def alarm(dur, amp=1.0, lo=m('A4'), hi=m('Eb5'), rate=1.5):
    """the klaxon: two tones, a tritone apart, swapping"""
    t = T(dur); n = len(t)
    w = (np.floor(t * rate * 2) % 2)
    fr = smooth(np.where(w > 0, hz(hi), hz(lo)), 0.012)
    s = vlp(osc(fr, 'saw') + 0.6 * osc(fr * 1.006, 'pulse', 0.4), 2200, 1.2, 2, 128)
    return amp * s * env(n, 0.02, 0, 1, 0.08) * 0.5


def sub808(f, dur, amp=1.0, drive=1.3):
    """the deep sub: a sine, a little driven, a slow release"""
    f = fq(f); t = T(dur)
    s = np.tanh(np.sin(2 * np.pi * f * t) * drive) / np.tanh(drive)
    return amp * s * env(len(t), 0.01, 0, 1, 0.18)


# ====================================================================== the grid
def at(tr, bar, beat=0.0):
    return tr.at(bar, beat)


def ply(tr, t0, notes, inst, pan=0.0, gain=1.0, wet=0.3, legato=0.95):
    t = t0
    ok = getattr(tr, 'ok', lambda _t: True)
    for x, d in notes:
        if x is not None and ok(t): tr.add(inst(x, d * tr.beat * legato), t, pan, gain, wet)
        t += d * tr.beat
    return t


def echo(tr, sig, t, pan=0.0, gain=1.0, wet=0.3, dt=None, taps=3, fb=0.38, cut=2800):
    """a ping-pong echo: the signal, then its darkened repeats swinging side to side"""
    tr.add(sig, t, pan, gain, wet)
    e = lp(sig, cut); dt = dt or tr.beat * 0.75
    for i in range(1, taps + 1):
        tr.add(e, t + dt * i, (-0.6 if i % 2 else 0.6), gain * fb ** i, min(0.9, wet + 0.2))


def bars_(tr, s):
    """the bars of section s this view wants"""
    return [s * SEC + b for b in range(SEC) if getattr(tr, 'want', lambda _b: True)(s * SEC + b)]


# ====================================================================== the layers (one section each)
def L_drone(tr, s, notes, amp=0.2, nb=SEC):
    addc(tr, drone([M(x) for x in notes], nb * tr.barlen + 2.5, amp, 0.3), at(tr, s * SEC) - 0.5, 0, 1, 0.5)


def L_hum(tr, s, root='D1', amp=0.18, cut=180, nb=SEC):
    """the ship's hum: a low pulse-wave held through the section, its filter breathing"""
    addc(tr, apad([M(root), M(root) + 7], nb * tr.barlen + 1.0, amp, cut, 1.5, 1.5, 2, 0.004, 0.09, 0.5, 2.0, 'pulse', 0.3),
         at(tr, s * SEC) - 0.3, 0, 1, 0.3)


def L_sub(tr, s, prog, amp=0.3, every=1):
    for b, c in enumerate(prog):
        if b % every or not _w(tr, s, b): continue
        tr.add(sub808(ch(c)[0] - 12, tr.barlen * every * 0.98, amp), at(tr, s * SEC + b), 0, 1, 0.03)


def _w(tr, s, b):
    return getattr(tr, 'want', lambda _b: True)(s * SEC + b)


def L_pulse(tr, s, prog, amp=0.2, cut0=300, cut1=900, rate=0.5, oct_=12, shape=None, q=2.4, accent=(0,), pan=0.0, drive=0.0):
    """THE SEQUENCER: the root pulsing in eighths (or sixteenths), the filter opening across the section"""
    shape = shape or (0, 0, 12, 0, 0, 12, 0, 7) if rate == 0.5 else (shape or (0, 0, 12, 0, 0, 12, 0, 0, 0, 0, 12, 0, 7, 0, 12, 0))
    k = int(round(4 / rate))
    for b, c in enumerate(prog):
        if not _w(tr, s, b): continue
        r = ch(c)[0] + oct_
        for i in range(k):
            u = (b * k + i) / (SEC * k)
            cut = cut0 + (cut1 - cut0) * u
            acc = 1.0 if (i % len(shape)) in accent or i % 4 == 0 else 0.72
            tr.add(mono(r + shape[i % len(shape)], tr.beat * rate * 0.85, amp * acc, 'saw', cut, cut * 2.2 * acc, 14, q, 0.006, 0.5,
                        drive=drive), at(tr, s * SEC + b, i * rate), pan, 1, 0.12)


ARP_SHAPES = {'up': (0, 1, 2, 3, 4, 3, 2, 1), 'wave': (0, 2, 1, 3, 2, 4, 3, 5), 'tick': (0, 2, 4, 2, 5, 2, 4, 2), 'fall': (5, 4, 3, 2, 4, 3, 2, 1),
              'wide': (0, 3, 1, 4, 2, 5, 3, 6)}


def L_arp(tr, s, prog, amp=0.12, lo=m('D4'), shape='up', rate=0.5, cut0=700, cut1=2400, q=2.8, pan=0.35, echo_=True, wave='saw', duty=0.5,
          wet=0.3, bars=None):
    """THE ARPEGGIATOR: the chord's tones climbing and turning, a pluck each, the filter opening across the section; its echo
    on the other side"""
    sh = ARP_SHAPES[shape] if isinstance(shape, str) else shape
    k = int(round(4 / rate))
    for b, c in enumerate(prog):
        if not _w(tr, s, b) or (bars is not None and b not in bars): continue
        up = ladder(ch(c), lo, max(sh) + 1)
        for i in range(k):
            u = (b * k + i) / (SEC * k)
            cut = cut0 + (cut1 - cut0) * u
            x = up[sh[i % len(sh)]]
            sig = mono(x, tr.beat * rate * 0.9, amp * (1.0 if i % 4 == 0 else 0.8), wave, cut, cut * 1.6, 18, q, 0.004, 0, 0.002, 0.08, 0.3, 0.05, duty=duty)
            t = at(tr, s * SEC + b, i * rate)
            p = pan if i % 2 == 0 else pan * 0.4
            if echo_:
                tr.add(sig, t, p, 1, wet); tr.add(lp(sig, 2200), t + tr.beat * 0.75, -p, 0.32, min(0.9, wet + 0.25))
            else:
                tr.add(sig, t, p, 1, wet)


def L_pad(tr, s, prog, amp=0.1, oct_=12, cut=1300, every=2, attack=0.8, wave='saw'):
    for b in range(0, len(prog), every):
        if not _w(tr, s, b): continue
        c = ch(prog[b])
        tr.add(apad([x + oct_ for x in c[:4]], tr.barlen * every + 0.5, amp, cut, attack, 1.0, 3, 0.009, 0.11, 0.35, 1.2, wave),
               at(tr, s * SEC + b), 0, 1, 0.55)


def L_hive(tr, s, prog, amp=0.12, vowel='u', to=None, oct_=12, every=2, attack=0.7, gate=0.0, top=False):
    for b in range(0, len(prog), every):
        if not _w(tr, s, b): continue
        c = ch(prog[b])[:3]
        notes = [c[0] + oct_, c[2] + oct_, c[1] + oct_ + 12] + ([c[0] + oct_ + 24] if top else [])
        tr.add(hive(notes, tr.barlen * every + 0.6, amp, vowel, to, attack, 0.9, gate=gate, rate=1 / tr.beat * 2),
               at(tr, s * SEC + b), 0, 1, 0.6)


def L_call(tr, s, bars_at=(0, 4), amp=0.12, k=0, vowel='a', pan=0.3):
    """the hive sends THE CALL"""
    for b in bars_at:
        if not _w(tr, s, b): continue
        ply(tr, at(tr, s * SEC + b), tp(CALL, k), lambda x, d: hive([x], d + 0.25, amp, vowel, None, 0.12, 0.6, 4), pan, 1, 0.65)


def L_stabs(tr, s, prog, amp=0.16, beats=(1.5, 3.5), oct_=12, every=1):
    for b, c in enumerate(prog):
        if b % every or not _w(tr, s, b): continue
        cc = ch(c)[:3]
        for bt in beats:
            tr.add(stab([cc[0] + oct_, cc[1] + oct_, cc[2] + oct_, cc[0] + oct_ + 12], tr.beat * 0.45, amp), at(tr, s * SEC + b, bt), 0, 1, 0.3)


def L_riff(tr, s, prog, amp=0.13, oct_=12, pat=(1, 1, 0, 1, 1, 0, 1, 1), drive=4.0, cut=900):
    """THE FORGE RIFF: a driven low saw in eighths on the root, the octave and - the alien turn - the tritone"""
    for b, c in enumerate(prog):
        if not _w(tr, s, b): continue
        cc = ch(c); r = cc[0] + oct_
        line = [r, r, r + 12, r, cc[1] + oct_, r, r + 6, cc[2] + oct_]
        for i, on in enumerate(pat):
            if not on: continue
            sig = mono(line[i], tr.beat * 0.42, amp, 'saw', cut, 2600, 16, 1.4, 0.01, 0.6, drive=drive)
            tr.add(sig, at(tr, s * SEC + b, i * 0.5), -0.3, 1, 0.12); tr.add(sig * 0.8, at(tr, s * SEC + b, i * 0.5) + 0.011, 0.3, 1, 0.12)


def L_metal(tr, s, k=4, amp=0.2, seed=0):
    """the hull: creaks, far clanks, a plate settling"""
    g = np.random.default_rng(seed * 101 + s * 7)
    for i in range(k):
        t = at(tr, s * SEC) + g.uniform(0, SEC * tr.barlen - 1.5)
        if not getattr(tr, 'ok', lambda _t: True)(t): continue
        kind = g.integers(3)
        if kind == 0: tr.add(creak(g.uniform(1.0, 2.4), amp * 0.5, g.uniform(45, 90), int(g.integers(1000000))), t, g.uniform(-0.8, 0.8), 1, 0.7)
        elif kind == 1: tr.add(lp(clank(amp * g.uniform(0.3, 0.7), g.uniform(700, 2400), g.uniform(0.6, 1.6), int(g.integers(1000000))), 3000), t, g.uniform(-0.9, 0.9), 1, 0.8)
        else: tr.add(hull(amp * 0.45, g.uniform(140, 260), 0.8, int(g.integers(1000000)), 0.2), t, g.uniform(-0.7, 0.7), 1, 0.8)


def L_pings(tr, s, notes=('D6', 'A5'), every=2, amp=0.1, off=1):
    for b in range(off, SEC, every):
        if not _w(tr, s, b): continue
        x = notes[(b // every) % len(notes)]
        echo(tr, ping(x, amp), at(tr, s * SEC + b), (-0.5, 0.5)[(b // every) % 2], 1, 0.6, tr.beat * 1.5, 3, 0.45, 3500)


def L_drums(tr, s, style, amp=1.0, fill=True, crash_=True, nb=SEC):
    """pulse: the hull struck once a bar. half: half time - the kick, a plate-snare on three, metal hats. drive: kick-kick, the
    backbeat, sixteenth hats. war: the double kick. march: the mechanical march - pistons and plates"""
    amp *= 0.7
    for b in range(nb):
        if not _w(tr, s, b): continue
        bar = s * SEC + b; t = at(tr, bar); bt = tr.beat
        if style == 'pulse':
            tr.add(ekick(0.5 * amp, 5), t, 0, 1, 0.12)
            if b % 2 == 1: tr.add(hull(0.4 * amp, 82, 1.2, bar), t + 2 * bt, -0.1, 1, 0.4)
        elif style == 'half':
            tr.add(ekick(0.6 * amp), t, 0, 1, 0.1); tr.add(ekick(0.35 * amp), t + 2.5 * bt, 0, 1, 0.1)
            tr.add(esnare(0.42 * amp), t + 2 * bt, 0.05, 1, 0.4)
            if b % 2 == 0: tr.add(hull(0.28 * amp, 96, 0.9, bar), t, -0.15, 1, 0.4)
            for i in range(8): tr.add(mhat(0.11 * amp * (1.2 if i % 2 else 0.7)), t + i * 0.5 * bt, 0.35, 1, 0.15)
        elif style == 'drive':
            for x in (0, 1.5, 2.5) if b % 2 == 0 else (0, 0.75, 2, 2.5): tr.add(ekick(0.62 * amp), t + x * bt, 0, 1, 0.08)
            for x in (1, 3): tr.add(esnare(0.48 * amp), t + x * bt, 0.05, 1, 0.3)
            for i in range(16): tr.add(mhat(0.07 * amp * (1.4 if i % 4 == 2 else 0.8)), t + i * 0.25 * bt, 0.3, 1, 0.12)
            if b % 2 == 0: tr.add(hull(0.3 * amp, 104, 0.7, bar), t, -0.2, 1, 0.35)
        elif style == 'war':
            for i in range(16): tr.add(ekick(0.4 * amp * (1.25 if i % 4 == 0 else 0.85), 11, 140, 46), t + i * 0.25 * bt, 0, 1, 0.05)
            for x in (1, 3): tr.add(esnare(0.55 * amp), t + x * bt, 0.05, 1, 0.3)
            tr.add(hull(0.4 * amp, 88, 1.0, bar), t, -0.15, 1, 0.35)
            for i in range(8): tr.add(mhat(0.09 * amp, i % 4 == 2), t + i * 0.5 * bt, 0.35, 1, 0.12)
        elif style == 'march':
            for x in (0, 1.5, 2): tr.add(ekick(0.6 * amp), t + x * bt, 0, 1, 0.08)
            for x in (1, 3): tr.add(esnare(0.5 * amp), t + x * bt, 0.05, 1, 0.32)
            tr.add(hull(0.45 * amp, 78, 1.1, bar), t, 0, 1, 0.4)
            tr.add(piston(0.3 * amp), t + 3.5 * bt, 0.4, 1, 0.3)
            for i in range(8): tr.add(clank(0.08 * amp, 2400 + 300 * (i % 3), 0.2, int(bar) * 8 + i), t + i * 0.5 * bt + 0.25 * bt, -0.4, 1, 0.25)
        if fill and b == nb - 1 and style in ('drive', 'war', 'march'):
            for k, f in enumerate((180, 140, 110, 84, 64, 50)):
                tr.add(tom(f, 0.34 * amp, 7, 0.25), t + (2.5 + k * 0.25) * bt, -0.5 + 0.2 * k, 1, 0.3)
        if crash_ and b == 0 and style in ('drive', 'war', 'march'):
            tr.add(crash(0.4 * amp, 3.0), t, 0.3, 1, 0.5)


def roll(tr, t_end, dur=1.5, amp=0.4, f=70.0):
    """an electro-tom roll crescendo into t_end"""
    n = int(dur / (tr.beat / 4))
    for i in range(n):
        u = (i + 1) / n
        tr.add(tom(f * (1 + 0.6 * u), amp * u ** 1.6, 8, 0.3), t_end - dur + i * tr.beat / 4, (-0.25, 0.25)[i % 2], 1, 0.35)


def brink(tr, s, amp=0.4, end=None):
    """the last two bars of a section that hands on: a riser and a roll into the next downbeat (or into bar `end`)"""
    t = at(tr, s * SEC + SEC if end is None else end)
    tr.add(edge(riser(tr.barlen * 2, amp * 0.5)), t - tr.barlen * 2, 0, 1, 0.4)
    tr.add(suck(tr.barlen, amp * 0.5), t - tr.barlen, 0.2, 1, 0.3)
    roll(tr, t, tr.barlen, amp * 0.6)


def impact(tr, t, amp=1.0):
    tr.add(boom(0.6 * amp, 100, 30), t, 0, 1, 0.4); tr.add(crash(0.5 * amp, 3.0), t, 0.2, 1, 0.5)
    tr.add(hull(0.8 * amp, 70, 1.4, 7), t, 0, 1, 0.4); tr.add(ekick(0.8 * amp), t, 0, 1, 0.1)
    tr.add(stab(['D3', 'A3', 'D4', 'F4'], 0.5, 0.3 * amp), t, 0, 1, 0.35)


def comply(tr, s, prog, amp=0.16, bars=range(SEC)):
    """the hive's COMPLY: the choir barking the chord on the offbeats, its breath cut short"""
    for b in bars:
        if not _w(tr, s, b): continue
        cc = ch(prog[b])[:3]
        for bt in (0.5, 1.5, 2.5) if b % 2 == 0 else (0.5, 1.5, 3, 3.5):
            tr.add(hive([cc[0] + 24, cc[1] + 24, cc[2] + 24], tr.beat * 0.4, amp, 'o', 'a', 0.012, 0.06, 4, alien=0.3), at(tr, s * SEC + b, bt), 0, 1, 0.4)


def bubbles(tr, s, prog, k=14, amp=0.07, seed=0):
    g = np.random.default_rng(seed + s * 13)
    for i in range(k):
        b = int(g.integers(SEC))
        if not _w(tr, s, b): continue
        c = ch(prog[b]); x = c[int(g.integers(len(c)))] + 36 + 12 * int(g.integers(2))
        tr.add(blip(x, amp * g.uniform(0.5, 1.0), int(g.integers(3, 9))), at(tr, s * SEC + b, float(g.integers(16)) / 4), g.uniform(-0.8, 0.8), 1, 0.55)


def acid(tr, s, prog, amp=0.16, oct_=12, pat=(0, 0, 12, 0, 3, 0, 15, 12, 0, 0, 7, 0, 10, 0, 12, 13), slide=(6, 14)):
    """the brood's bass: a squelching acid line in sixteenths, sliding into some notes"""
    for b, c in enumerate(prog):
        if not _w(tr, s, b): continue
        r = ch(c)[0] + oct_
        prev = None
        for i, k in enumerate(pat):
            x = r + k
            acc = 1.0 if i % 4 == 0 else 0.7
            sig = mono(x, tr.beat * 0.24, amp * acc, 'saw', 380, 1800 * acc, 22, 5.0, 0.0, 0.3,
                       glide_from=prev if i in slide and prev is not None else None, glide=0.03)
            tr.add(sig, at(tr, s * SEC + b, i * 0.25), 0.1, 1, 0.15)
            prev = x


# ====================================================================== I. THE DOCK
def t1():
    tr = Track('ar_t1', BPM, LEN['t1'])
    tr.barlen = tr.beat * 4
    plan = [P_DOCK, P_DOCK, P_V, P_V, P_DOCK, P_V, P_V, P_DOCK]
    for s, prog in enumerate(plan):
        L_hum(tr, s, 'D1', 0.2 if s not in (0, 7) else 0.16)
        L_drone(tr, s, ['D2', 'A2'] if prog is not P_V else ['D2', 'A2', 'D3'], 0.08)
        L_metal(tr, s, 4 if s in (0, 6, 7) else 2, 0.22, 1)
        L_pings(tr, s, ('D6', 'A5') if s % 2 == 0 else ('Eb6', 'A5'), 4 if s in (2, 3, 5, 6) else 2, 0.07)
        if s >= 1: L_pulse(tr, s, prog, 0.1 + 0.015 * min(s, 4), 160, 380 + 40 * s, 0.5, 12, q=2.0)
        if s in (2, 3, 5, 6): L_drums(tr, s, 'pulse', 0.5 + 0.08 * (s >= 5))
        if s in (1, 4, 5, 6): L_hive(tr, s, prog, 0.06 if s == 1 else 0.075, 'u', 'o' if s >= 5 else None, 12, 2, 1.2)
        if s in (4, 5, 6): L_arp(tr, s, prog, 0.05 + 0.01 * (s - 4), m('D4'), 'up', 0.5, 300, 900 + 200 * (s - 4), 2.4, 0.4)
        if s in (0, 4, 7): L_call(tr, s, (2,) if s != 4 else (2, 6), 0.07, 0, 'u', 0.45)
    # the theremin: V slow (half time), far off; then again, nearer, with the choir under it an octave down
    ther(tr, at(tr, 2 * SEC), V2, 0.14, -0.1, 0.6, port=0.11, depth=0.014)
    ther(tr, at(tr, 5 * SEC), tp(V2, 12), 0.13, 0.1, 0.55, port=0.09)
    ply(tr, at(tr, 5 * SEC), V2, lambda x, d: hive([x], d + 0.3, 0.05, 'u', 'o', 0.4, 0.8, 4), -0.2, 1, 0.6)
    # the Dock waking: the first two bars of V as a far horn, answered
    for b in (1, 5):
        ply(tr, at(tr, 1 * SEC + b), V[:2], lambda x, d: horn([x], d, 0.07, 1100, 500, 0.15), -0.35, 1, 0.7)
    for k in range(6):
        tr.add(gaze(('A6', 'D7', 'Eb7')[k % 3], 6.0, 0.02), at(tr, (k * 11) % 64, 1), (-0.6, 0.6)[k % 2], 1, 0.85)
    brink(tr, 7, 0.22)
    return tr


# ====================================================================== II. THE BROOD-CARRIER
def t2():
    tr = Track('ar_t2', BPM, LEN['t2'])
    tr.barlen = tr.beat * 4
    plan = [P_BROOD, P_BROOD, P_V, P_V, P_BROOD, P_DOCK, P_BROOD, P_V, P_V, P_DOCK]
    for s, prog in enumerate(plan):
        L_hum(tr, s, 'D1', 0.14)
        bubbles(tr, s, prog, 10 if s in (0, 5) else 16, 0.06, 2)
        L_metal(tr, s, 2, 0.16, 2)
        if s not in (5,): acid(tr, s, prog, 0.07 + 0.012 * min(s, 6) if s else 0.06)
        if s in (2, 3, 4, 6, 7, 8): L_drums(tr, s, 'half', 0.55 + 0.05 * (s >= 6), crash_=False)
        if s in (1, 2, 3, 6, 7, 8): L_hive(tr, s, prog, 0.075, 'u' if s < 4 else 'o', 'a' if s in (3, 8) else None, 12, 2, 0.8)
        if s in (4, 6, 7, 8): L_arp(tr, s, prog, 0.06, m('D5'), 'wave', 0.25, 600, 1800, 3.0, 0.4)
        L_sub(tr, s, prog, 0.2 if s not in (5,) else 0.12, 2)
        if s == 5:
            L_drone(tr, s, ['D2', 'Eb2', 'A2'], 0.14)
            L_pings(tr, s, ('D6', 'Eb6'), 2, 0.07)
            L_call(tr, s, (0, 4), 0.09, 0, 'u', -0.4)
            for k in range(4): tr.add(whisper(3.0, 0.04, 30 + k), at(tr, s * SEC + 2 * k), (-0.7, 0.7)[k % 2], 1, 0.8)
    # the brood's melody: the theremin, sliding (a sick, slow lullaby for the tanks)
    ther(tr, at(tr, 1 * SEC), B, 0.16, 0.1, 0.5, port=0.14, depth=0.016)
    ther(tr, at(tr, 2 * SEC), V2, 0.14, -0.1, 0.5, port=0.1, k=12)
    ply(tr, at(tr, 2 * SEC + 2), tp(CALL, 0), lambda x, d: hive([x], d + 0.3, 0.06, 'a', None, 0.2, 0.7), 0.4, 1, 0.65)
    ply(tr, at(tr, 4 * SEC), B, lambda x, d: hive([x, M(x) - 12], d + 0.3, 0.1, 'u', 'a', 0.25, 0.8), 0, 1, 0.55)
    ply(tr, at(tr, 4 * SEC), tp(B, 12), lambda x, d: mono(x, d, 0.035, 'pulse', 1400, 800, 3, 1.0, 0.004, 0, 0.05, 0.3, 0.8, 0.2, duty=0.3), 0.35, 1, 0.6)
    ther(tr, at(tr, 6 * SEC), B, 0.15, 0.1, 0.5, port=0.12, k=12)
    ply(tr, at(tr, 6 * SEC), B, lambda x, d: hive([M(x) - 12], d + 0.3, 0.07, 'o', None, 0.3, 0.8), -0.2, 1, 0.55)
    ply(tr, at(tr, 7 * SEC), V2, lambda x, d: horn([x], d, 0.09, 1600, 500, 0.12), -0.15, 1, 0.5)
    for b in (1, 5, 9, 13):
        ther(tr, at(tr, 7 * SEC + b, 2), tp(CALL, 0), 0.11, 0.45, 0.6, echo_=True, port=0.06)
    brink(tr, 9, 0.28)
    return tr


# ====================================================================== III. THE STAR-FORGE
def t3():
    tr = Track('ar_t3', BPM, LEN['t3'])
    tr.barlen = tr.beat * 4
    plan = [P_FORGE, P_FORGE, P_V, P_V, P_FORGE, P_BROOD, P_V, P_FORGE, P_V, P_FORGE]
    for s, prog in enumerate(plan):
        L_sub(tr, s, prog, 0.24, 1)
        if s == 5:                                                      # (the slag pit: the drums drop out, steam, the choir)
            L_hum(tr, s, 'D1', 0.16)
            L_drums(tr, s, 'pulse', 0.6)
            L_hive(tr, s, prog, 0.1, 'o', 'a', 12, 2, 0.6)
            ply(tr, at(tr, s * SEC), B, lambda x, d: hive([x], d + 0.25, 0.08, 'u', 'o', 0.2, 0.7), 0.2, 1, 0.6)
            for b in range(0, SEC, 2): tr.add(piston(0.3), at(tr, s * SEC + b, 3), (-0.5, 0.5)[b // 2 % 2], 1, 0.5)
            L_arp(tr, s, prog, 0.05, m('D4'), 'tick', 0.25, 500, 1200, 2.6, 0.4)
            continue
        L_riff(tr, s, prog, 0.1 if s in (0, 9) else 0.12, 12, (1, 1, 0, 1, 1, 0, 1, 1) if s % 2 == 0 else (1, 0, 1, 1, 0, 1, 1, 1), 4.0, 700 + 60 * min(s, 6))
        L_drums(tr, s, 'drive' if s not in (0,) else 'half', 0.8 if s else 0.65)
        for b in range(SEC):                                            # (the anvils: two and four)
            if _w(tr, s, b):
                for x in (1, 3): tr.add(clank(0.2, 1500 + 110 * (b % 3), 0.7, s * 64 + b * 2 + x), at(tr, s * SEC + b, x), 0.45, 1, 0.35)
                if b % 4 == 3: tr.add(piston(0.25), at(tr, s * SEC + b, 3.5), -0.5, 1, 0.4)
        if s >= 1: L_arp(tr, s, prog, 0.06 + 0.01 * (s >= 6), m('A4'), 'wave' if s % 2 else 'up', 0.25, 600, 2600, 3.0, 0.4)
        if s in (1, 3, 7): L_stabs(tr, s, prog, 0.1, (1.5, 3.5), 12, 2)
        if s in (2, 3, 6, 8): L_hive(tr, s, prog, 0.08, 'a', None, 12, 2, 0.4)
        if s in (2, 6, 8): L_pad(tr, s, prog, 0.05, 12, 1600, 2, 0.4)
    # V in the horns; then the theremin with V an octave up and the horns calling under it
    ply(tr, at(tr, 2 * SEC), V, lambda x, d: horn([x, M(x) - 12], d, 0.16, 2400, 600), -0.1, 1, 0.4)
    ther(tr, at(tr, 3 * SEC), tp(V, 12), 0.2, 0.1, 0.45, port=0.06)
    for b in (0, 4): ply(tr, at(tr, 3 * SEC + b), tp(CALL, -12), lambda x, d: horn([x], d, 0.1, 1800, 500), -0.3, 1, 0.45)
    # the hammer: the arpeggiator's lead let loose - sixteenth runs over the riff
    run = mel('D5:.25 F5:.25 A5:.25 D6:.25 Eb6:1 D6:.5 A5:.5 F5:.5 D5:.5 '
              'D5:.25 F5:.25 A5:.25 D6:.25 Eb6:.5 D6:.5 C6:2 '
              'C5:.25 E5:.25 G5:.25 C6:.25 D6:1 C6:.5 G5:.5 E5:.5 C5:.5 '
              'C5:.25 E5:.25 G5:.25 C6:.25 D6:.5 C6:.5 Bb5:2 '
              'Bb4:.25 D5:.25 F5:.25 Bb5:.25 C6:1 Bb5:.5 F5:.5 D5:.5 Bb4:.5 '
              'Bb4:.25 D5:.25 F5:.25 Bb5:.25 C6:.5 Bb5:.5 A5:2 '
              'Bb5:.5 G5:.5 Eb5:.5 G5:.5 Bb5:.5 Eb6:.5 D6:.5 C6:.5 C#6:2 E6:1 A5:1')
    assert bars_of(run) == 8, bars_of(run)
    ply(tr, at(tr, 4 * SEC), run, lambda x, d: mono(x, d, 0.09, 'saw', 1200, 2400, 8, 2.2, 0.006, 0, 0.003, 0.1, 0.7, 0.04, drive=2.0), 0.15, 1, 0.3)
    ply(tr, at(tr, 4 * SEC) + tr.beat * 0.75, run, lambda x, d: lp(mono(x, d, 0.035, 'saw', 1200, 1200, 8, 2.0), 2000), -0.4, 1, 0.5)
    ply(tr, at(tr, 6 * SEC), V, lambda x, d: horn([x, M(x) + 12], d, 0.15, 2800, 700), -0.15, 1, 0.4)
    ply(tr, at(tr, 6 * SEC), tp(V, -12), lambda x, d: horn([x], d, 0.1, 1200, 400), 0.15, 1, 0.35)
    for b in (0, 2, 4, 6): L_call(tr, 7, (b,), 0.07, 0, 'a', (-0.4, 0.4)[b // 2 % 2])
    ply(tr, at(tr, 8 * SEC), V, lambda x, d: horn([x, M(x) - 12], d, 0.17, 3000, 700), -0.1, 1, 0.4)
    ther(tr, at(tr, 8 * SEC), tp(V, 12), 0.2, 0.15, 0.45, port=0.05)
    ply(tr, at(tr, 8 * SEC), V, lambda x, d: hive([M(x) + 12], d + 0.2, 0.08, 'a', None, 0.1, 0.6), 0.3, 1, 0.55)
    brink(tr, 9, 0.35)
    return tr


# ====================================================================== IV. THE NAVIGATOR
def t4():
    tr = Track('ar_t4', BPM, LEN['t4'])
    tr.barlen = tr.beat * 4
    plan = [P_NAV, P_NAV, P_V, P_NAV, P_V, P_DOCK, P_NAV, P_V, P_NAV, P_V]
    for s, prog in enumerate(plan):
        if s == 5:                                                      # (zero-G: the floor drops away)
            L_drone(tr, s, ['D2', 'A2', 'E3'], 0.16)
            L_hum(tr, s, 'D1', 0.12)
            tr.add(boom(0.4, 70, 24, 4.0), at(tr, s * SEC), 0, 1, 0.6)
            tr.add(gaze('E6', 10.0, 0.04), at(tr, s * SEC + 1), 0.3, 1, 0.8)
            for b in range(0, SEC, 2):
                tr.add(suck(tr.barlen * 1.5, 0.12), at(tr, s * SEC + b), (-0.5, 0.5)[b // 2 % 2], 1, 0.5)
                tr.add(sub808(m('D1'), tr.barlen * 2, 0.22), at(tr, s * SEC + b), 0, 1, 0.05)
            L_arp(tr, s, prog, 0.05, m('D5'), 'wide', 0.25, 1500, 2600, 2.0, 0.6, wave='tri')
            L_call(tr, s, (2, 6), 0.08, 0, 'u', 0.5)
            continue
        L_sub(tr, s, prog, 0.22, 2)
        L_pad(tr, s, prog, 0.07 if s in (0, 1, 3, 8) else 0.05, 12, 1500, 2, 1.0, 'pulse')
        L_arp(tr, s, prog, 0.06 + 0.008 * (s >= 6), m('A4') if s % 2 else m('D5'), 'wide' if s % 3 == 0 else 'up', 0.25,
              1100, 2800, 2.4, 0.5, True, 'saw' if s >= 6 else 'tri', wet=0.5)
        L_pulse(tr, s, prog, 0.09 + 0.01 * min(s, 6), 260, 800, 0.5, 12, q=2.2)
        for b in range(0, SEC, 2):                                     # (the star-bells)
            if _w(tr, s, b):
                cc = ch(prog[b])
                tr.add(sbell(cc[2] + 36, 3.0, 0.06), at(tr, s * SEC + b, 1), 0.55, 1, 0.75)
                tr.add(sbell(cc[1] + 36 + 12, 2.5, 0.04), at(tr, s * SEC + b, 2.5), -0.55, 1, 0.75)
        if s in (1, 3, 8): L_drums(tr, s, 'half', 0.6, crash_=False)
        if s in (2, 4, 6, 7, 9): L_drums(tr, s, 'drive', 0.8 if s < 7 else 0.9)
        if s in (3, 6, 9): L_hive(tr, s, prog, 0.08, 'a', None, 12, 2, 0.6)
    ther(tr, at(tr, 1 * SEC), N, 0.21, 0.05, 0.5, port=0.08)
    ply(tr, at(tr, 2 * SEC), V, lambda x, d: horn([x, M(x) - 12], d, 0.14, 2200, 600), -0.1, 1, 0.45)
    ply(tr, at(tr, 3 * SEC), N, lambda x, d: hive([x, M(x) - 12], d + 0.3, 0.1, 'o', 'a', 0.2, 0.8), 0, 1, 0.55)
    ther(tr, at(tr, 3 * SEC), tp(N, 12), 0.16, 0.2, 0.55, port=0.07)
    ther(tr, at(tr, 4 * SEC), tp(V, 12), 0.2, 0.1, 0.45, port=0.06)
    ply(tr, at(tr, 4 * SEC), V, lambda x, d: horn([x], d, 0.12, 1800, 500), -0.2, 1, 0.45)
    ply(tr, at(tr, 6 * SEC), N, lambda x, d: horn([x, M(x) - 12], d, 0.15, 2600, 700), -0.1, 1, 0.45)
    ply(tr, at(tr, 6 * SEC), tp(N, 12), lambda x, d: mono(x, d, 0.05, 'pulse', 1600, 1200, 4, 1.0, 0.004, 0, 0.01, 0.2, 0.8, 0.1, duty=0.25), 0.35, 1, 0.6)
    ply(tr, at(tr, 7 * SEC), V, lambda x, d: horn([x, M(x) + 12, M(x) - 12], d, 0.17, 3000, 700), -0.1, 1, 0.4)
    ther(tr, at(tr, 7 * SEC + 4), [('A5', 4), ('Bb5', 4), ('A5', 2), ('G#5', 2), ('A5', 4)], 0.16, 0.3, 0.5, port=0.12)
    ther(tr, at(tr, 8 * SEC), tp(N, 12), 0.2, 0.1, 0.5, port=0.07)
    ply(tr, at(tr, 9 * SEC), V, lambda x, d: horn([x, M(x) - 12], d, 0.17, 3000, 700), -0.1, 1, 0.4)
    ply(tr, at(tr, 9 * SEC), V, lambda x, d: hive([M(x) + 12], d + 0.2, 0.08, 'a', None, 0.1, 0.6), 0.25, 1, 0.55)
    ther(tr, at(tr, 9 * SEC), tp(V, 12), 0.18, 0.2, 0.45, port=0.05)
    brink(tr, 9, 0.38)
    return tr


# ====================================================================== V. THE DREADNOUGHTS AND THE FLAGSHIP
def t5():
    tr = Track('ar_t5', BPM, LEN['t5'])
    tr.barlen = tr.beat * 4
    plan = [P_WAR, P_V, P_V, P_WAR, P_V, P_DOCK, P_V, P_WAR, P_V, P_WAR]
    for s, prog in enumerate(plan):
        if s == 5:                                                      # (the Flagship: a hush before the bridge - the red window)
            L_hum(tr, s, 'D1', 0.13)
            L_drone(tr, s, ['D2', 'A2', 'Eb3'], 0.1)
            for b in range(0, SEC, 1): tr.add(ekick(0.2 + 0.035 * b, 9), at(tr, s * SEC + b), 0, 1, 0.1)
            L_hive(tr, s, prog, 0.06, 'u', 'a', 12, 4, 1.5, top=True)
            ther(tr, at(tr, s * SEC), [('D5', 6), ('A5', 2), ('Eb6', 8), ('D6', 6), ('C6', 2), ('A5', 8)], 0.13, 0.0, 0.6, port=0.15)
            tr.add(apad(['D5', 'A5', 'Eb6', 'D7'], tr.barlen * SEC, 0.04, 3200, 4.0, 2.0, 3, 0.012, 0.2, 0.3), at(tr, s * SEC), 0, 1, 0.8)
            L_pings(tr, s, ('D6', 'Eb6'), 2, 0.06)
            continue
        L_sub(tr, s, prog, 0.26, 1)
        L_pulse(tr, s, prog, 0.12, 500, 1600, 0.25, 12, None, 2.4, drive=1.5)
        L_drums(tr, s, ('march', 'war', 'war', 'march', 'war', None, 'war', 'march', 'war', 'march')[s], 0.95)
        L_arp(tr, s, prog, 0.06, m('D5'), 'wave' if s % 2 else 'up', 0.25, 1200, 3200, 3.0, 0.45)
        if s in (0, 3, 7, 9): L_riff(tr, s, prog, 0.1, 12, (1, 1, 1, 1, 1, 1, 1, 1), 5.0, 1000)
        if s in (0, 3, 7): L_stabs(tr, s, prog, 0.12, (0, 1.5, 3), 12, 1)
        if s in (1, 2, 4, 6, 8): L_hive(tr, s, prog, 0.1, 'a', None, 12, 2, 0.3, top=s >= 6)
        if s in (3, 7): comply(tr, s, prog, 0.1)
        if s == 0:
            tr.add(alarm(tr.barlen * 4, 0.07), at(tr, 0), -0.4, 1, 0.6); tr.add(alarm(tr.barlen * 4, 0.05), at(tr, 4), 0.4, 1, 0.7)
        if s in (2, 6, 8):
            for b in range(1, SEC, 2): tr.add(zap(0.06), at(tr, s * SEC + b, 3.5), (-0.6, 0.6)[b // 2 % 2], 1, 0.5)
        if s == 8:
            for b in range(SEC): tr.add(crash(0.22), at(tr, s * SEC + b), (-0.3, 0.3)[b % 2], 1, 0.5)
    # V: the brass in octaves, the theremin at the top
    for s in (1, 2, 4, 6, 8):
        lo = s in (1, 4)
        ply(tr, at(tr, s * SEC), tp(V, -12) if lo else V, lambda x, d: horn([x, M(x) + 12], d, 0.17, 2600 if lo else 3200, 600), -0.1, 1, 0.4)
        if not lo or s == 4: ply(tr, at(tr, s * SEC), tp(V, -24), lambda x, d: horn([x], d, 0.1, 900, 300), 0.1, 1, 0.3)
        if s in (2, 6, 8): ther(tr, at(tr, s * SEC), tp(V, 12), 0.2, 0.15, 0.45, port=0.05)
        if s in (6, 8): ply(tr, at(tr, s * SEC), V, lambda x, d: hive([M(x) + 12], d + 0.2, 0.09, 'a', None, 0.08, 0.5), 0.3, 1, 0.5)
    ther(tr, at(tr, 4 * SEC), [('A5', 8), ('Bb5', 4), ('A5', 4), ('G#5', 8), ('A5', 8)], 0.15, 0.3, 0.55, port=0.15, k=12)
    for s in (3, 7):                                                    # (the wail over the riff)
        ther(tr, at(tr, s * SEC), [('D6', 4), ('Eb6', 4), ('D6', 2), ('C6', 2), ('Bb5', 4), ('A5', 8), ('G#5', 4), ('A5', 4)], 0.17, 0.2, 0.5, port=0.12)
    brink(tr, 9, 0.42)
    return tr


# ====================================================================== THE FIGHTS
def c1():
    tr = Track('ar_c1', BPM, LEN['c1'])
    tr.barlen = tr.beat * 4
    plan = [P_WAR, P_V, P_FORGE, P_V, P_WAR]
    for s, prog in enumerate(plan):
        impact(tr, at(tr, s * SEC), 1.0 if s == 0 else 0.55)
        L_drums(tr, s, 'drive', 1.0)
        L_sub(tr, s, prog, 0.26, 1)
        L_pulse(tr, s, prog, 0.13, 700, 1800, 0.25, 12, None, 2.6, drive=1.4)
        L_arp(tr, s, prog, 0.06, m('D5'), 'wave', 0.25, 1500, 3200, 3.0, 0.45)
        L_stabs(tr, s, prog, 0.12, (1.5, 3.5) if s % 2 else (0.5, 1.5, 3), 12, 1)
        if s in (1, 3): L_hive(tr, s, prog, 0.08, 'a', None, 12, 2, 0.3)
        if s == 2: L_riff(tr, s, prog, 0.11, 12, (1, 1, 1, 1, 1, 1, 1, 1), 5.0, 1100)
    for k in (0, 4):
        ply(tr, at(tr, 1 * SEC + k), VF, lambda x, d: mono(x, d, 0.12, 'saw', 1600, 2400, 6, 1.8, 0.008, 0, 0.004, 0.1, 0.75, 0.05, drive=2.2), -0.1, 1, 0.35)
        ther(tr, at(tr, 3 * SEC + k), tp(VF, 12), 0.19, 0.15, 0.4, port=0.035)
        ply(tr, at(tr, 3 * SEC + k), VF, lambda x, d: horn([x, M(x) - 12], d, 0.13, 2600, 600, 0.03), -0.15, 1, 0.4)
    for b in range(0, SEC, 2): L_call(tr, 2, (b,), 0.07, 12 if b >= 4 else 0, 'a', (-0.4, 0.4)[b // 2 % 2])
    ply(tr, at(tr, 4 * SEC), V, lambda x, d: horn([x, M(x) + 12], d, 0.15, 3000, 700, 0.04), -0.1, 1, 0.4)
    brink(tr, 4, 0.4)
    return tr


def c2():
    tr = Track('ar_c2', BPM, LEN['c2'])
    tr.barlen = tr.beat * 4
    plan = [P_WAR, P_V, P_WAR, P_V, P_WAR]
    for s, prog in enumerate(plan):
        impact(tr, at(tr, s * SEC), 1.0 if s == 0 else 0.65)
        L_drums(tr, s, 'war' if s != 2 else 'march', 1.0)
        L_sub(tr, s, prog, 0.28, 1)
        L_riff(tr, s, prog, 0.12, 12, (1, 1, 1, 1, 1, 1, 1, 1), 6.0, 1200)
        L_pulse(tr, s, prog, 0.1, 900, 2000, 0.25, 24, None, 2.4, pan=0.2, drive=1.4)
        if s in (1, 3, 4): L_hive(tr, s, prog, 0.09, 'a', None, 12, 2, 0.25, top=True)
        if s in (0, 2): comply(tr, s, prog, 0.11)
        for b in range(0, SEC, 2): tr.add(zap(0.07, 3600, 300), at(tr, s * SEC + b, 3.5), (-0.6, 0.6)[b // 2 % 2], 1, 0.5)
    for k in (0, 4):
        ply(tr, at(tr, 1 * SEC + k), VF, lambda x, d: horn([x, M(x) + 12], d, 0.15, 3200, 700, 0.025), -0.1, 1, 0.35)
        ply(tr, at(tr, 1 * SEC + k), tp(VF, -12), lambda x, d: horn([x], d, 0.1, 1000, 300, 0.025), 0.1, 1, 0.3)
        ther(tr, at(tr, 3 * SEC + k), tp(VF, 12), 0.19, 0.15, 0.4, port=0.03)
        ply(tr, at(tr, 3 * SEC + k), VF, lambda x, d: horn([x, M(x) - 12], d, 0.15, 3000, 700, 0.025), -0.15, 1, 0.35)
    ther(tr, at(tr, 2 * SEC), [('D6', 4), ('Eb6', 4), ('D6', 2), ('C6', 2), ('Bb5', 4), ('A5', 8), ('G#5', 4), ('A5', 4)], 0.17, 0.25, 0.45, port=0.1)
    ply(tr, at(tr, 4 * SEC), V, lambda x, d: horn([x, M(x) + 12, M(x) - 12], d, 0.16, 3200, 700, 0.04), -0.1, 1, 0.4)
    ther(tr, at(tr, 4 * SEC), tp(V, 12), 0.18, 0.2, 0.4, port=0.05)
    brink(tr, 4, 0.45)
    return tr


# ====================================================================== THE SWELL (the page turn: two bars, 3 s)
def swell():
    tr = Track('ar_swell', BPM, 2)
    tr.barlen = tr.beat * 4
    d = tr.seconds
    tr.add(suck(d, 0.7), 0, 0.2, 1, 0.2)
    tr.add(edge(riser(d, 0.35)), 0, -0.2, 1, 0.2)
    roll(tr, d - 0.02, d * 0.6, 0.35, 64)
    tr.add(edge(hive(['A3', 'E4', 'A4'], d, 0.14, 'u', 'a', d * 0.8, 0.02)), 0, 0, 1, 0.3)
    sw = mono('A1', d, 0.16, 'saw', 150, 0, 1, 3.0, 0.01, 0.5, d * 0.9, 0, 1, 0.02)
    t = T(d); sw = vlp(sw, 200 + 2600 * (t / d) ** 2, 3.0, 2, 64)          # (a filter sweep up, into the downbeat)
    tr.add(edge(sw), 0, 0, 1, 0.2)
    return tr


def save_swell(tr):
    """played once: no tail may wrap round to its start - faded in, cut hard at the downbeat (the next track starts there)"""
    st = render(tr, 1.2, 0.11)
    k = int(0.5 * SR); st[:, :k] *= np.linspace(0, 1, k)
    f = int(0.012 * SR); st[:, -f:] *= np.linspace(1, 0, f)
    _guarded(st, os.path.join(VENDOR, 'ar_swell.ogg'), 4)


# (each tier louder than the last; the fights hot)
LEVEL = {'t1': 0.13, 't2': 0.15, 't3': 0.175, 't4': 0.18, 't5': 0.22, 'c1': 0.22, 'c2': 0.24}
ROOM = {'t1': 3.4, 't2': 3.0, 't3': 2.4, 't4': 3.2, 't5': 2.6, 'c1': 2.2, 'c2': 2.2}
BUILD = {'t1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 'c1': c1, 'c2': c2}


def check(prefix='ar_', names=None):
    db = lambda v: 20 * np.log10(max(float(v), 1e-9))
    for nm in names or (list(BUILD) + ['swell']):
        p = os.path.join(VENDOR, f'{prefix}{nm}.ogg')
        if not os.path.exists(p): continue
        x = _decode(p); n = x.shape[1]
        rms, pk = np.sqrt((x ** 2).mean()), np.abs(x).max()
        seam = np.abs(x[:, 0] - x[:, -1]).max()
        step = np.percentile(np.abs(np.diff(x, axis=1)), 99.9)
        secs = [db(np.sqrt((x[:, i:i + 12 * SR] ** 2).mean())) for i in range(0, n - SR, 12 * SR)]
        print(f'{prefix}{nm:6s} {n / SR:6.1f} s  RMS {db(rms):6.1f} dBFS  peak {db(pk):5.1f}  seam {seam:.3f} (step {step:.3f})  '
              f'sections ' + ' '.join(f'{v:5.1f}' for v in secs))


def journey(out):
    """a preview of the voyage as phase244 plays it: each tier for a while, handed to the next on a section boundary under the
    swell; a fight cutting in on a two-bar line and handing back on its section boundary through the swell"""
    tr = {nm: _decode(os.path.join(VENDOR, f'ar_{nm}.ogg')) for nm in list(BUILD) + ['swell']}
    plan = [('t1', 36), ('t2', 36), ('c1', 24), ('t2', 12), ('t3', 36), ('t4', 36), ('c2', 24), ('t5', 48)]
    cuts, segs, pos = [], [], 0
    for nm, sec in plan:
        segs.append(tr[nm][:, :sec * SR].copy()); cuts.append((pos, nm)); pos += sec
    y = np.concatenate(segs, axis=1)
    for t, nm in cuts[1:]:
        if nm.startswith('c'): continue                                     # (a fight cuts straight in, on its impact)
        a = (t - 3) * SR; y[:, a:a + 3 * SR] += tr['swell'][:, :3 * SR]
    k = int(3 * SR); y[:, -k:] *= np.linspace(1, 0, k)
    y = np.clip(y, -0.98, 0.98)
    _encode(y, out, 4)
    print('journey:', ' -> '.join(f'{nm}@{t}s' for t, nm in cuts))


if __name__ == '__main__':
    what = sys.argv[1:] or list(BUILD) + ['swell', 'check']
    for i, nm in enumerate(BUILD):
        if nm in what:
            tr = seeded(60 + i, BUILD[nm])
            assert abs(tr.seconds - LEN[nm] * 1.5) < 1e-6, (nm, tr.seconds)
            _guarded(render(tr, ROOM[nm], LEVEL[nm]), os.path.join(VENDOR, f'ar_{nm}.ogg'), 3)
    if 'swell' in what: save_swell(seeded(69, swell))
    if 'check' in what: check()
    if 'journey' in what:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'previews', 'v299_armada', 'music')
        os.makedirs(out, exist_ok=True)
        journey(os.path.join(out, 'armada_journey.ogg'))
