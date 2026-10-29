"""2.99a: synthesises THE BLACK MARKET's own theme - "Members Only" (vendor/market_theme.ogg), the music a key-holder hears
inside a market (phase250). A smugglers' den after hours: sly, swaggering noir swing.

THE BAND (all synthesised, no samples):
  upright bass   Karplus-Strong string with a body thump, walking quarter notes (chromatic approaches into every chord)
  drums          brushes (a swish stirred round every beat, taps on two and four), a swung ride (inharmonic partials),
                 the hi-hat's foot on two and four, a feathered kick, triplet fills; finger snaps in the vamps
  muted trumpet  additive brass through a Harmon-mute formant (nasal, ~1.9 kHz), breath, scoops, a hand-wah on long notes,
                 fall-offs - THE HOOK
  clarinet       additive, odd harmonics first (the woody chalumeau), answers the hook, takes the bridge, doubles the
                 last chorus an octave down
  Rhodes         FM electric piano, rootless voicings comping a Charleston (and its variations)
  vibraphone     1:4:10 partials and a motor tremolo - sparkles and the vamp's arpeggio
  accordion      three detuned reeds (a musette's wet tuning), bellows swell - the flourishes at the ends of phrases

THE FORM: C minor, 128 BPM swing (swung 8ths at 64%), 40 bars = exactly 75 s, rendered circularly (notes and reverb tails
that run past the end wrap round to the start), so it loops without a seam - the last two bars are the vamp and a drum fill
that land on bar 1.
   bars  0-1   the vamp           Cm6 | Ab7 G7      (bass, brushes, Rhodes, snaps)
         2-9   A1  THE HOOK       Cm6 Cm6 Fm7 Fm7 Ab7 G7 Cm6 Dm7b5-G7   (muted trumpet, the wah on its long notes)
        10-17  A2  the hook again, the clarinet answering in its rests, the vibes in
        18-25  B   the bridge     Fm7 Bb7 Ebmaj7 Abmaj7 Dm7b5 G7 Cm6 G7  (clarinet; the accordion's flourishes)
        26-33  A3  the hook, everyone (clarinet an octave down, horn stabs, the kick feathering)
        34-37  the shout tag      Ab7 G7 Ab7 G7      (trumpet + clarinet, the blue note, a button)
        38-39  the vamp, a vibes arpeggio, the accordion's run, the drum fill back to the top

Loudness: matched to the area tracks (the Armada's and the Undercrown's tiers sit -18..-10 LUFS, median about -14.7):
integrated -15 LUFS, sample peak <= -1 dBFS after the Vorbis encode (checked by decoding).

Deterministic; run it to rebuild (needs numpy, scipy and ffmpeg - only to rebuild, never to build the packs):
    python3 tools/market_music.py [preview DIR]      # writes vendor/market_theme.ogg (+ DIR/market_theme.mp3)"""
import os, sys, wave, tempfile, subprocess, re
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
BPM = 128
BEAT = 60.0 / BPM
BARS = 40
SWING = 0.64                                # (where a swung "and" falls in its beat)
TARGET_LUFS = -15.0
CEIL_DB = -1.2                              # (sample peak after encoding: under -1 dBFS with a little room)
G = np.random.default_rng(2990)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


# ====================================================================== basics
def m(x):
    if isinstance(x, (int, np.integer)): return int(x)
    n, acc, o = x[0], x[1:-1], int(x[-1])
    return 12 * (o + 1) + NOTE[n] + acc.count('#') - acc.count('b')


def hz(x):
    return 440.0 * 2 ** ((m(x) - 69) / 12)


def tt(dur):
    return np.arange(max(1, int(dur * SR))) / SR


def noise(n):
    return G.uniform(-1, 1, n)


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR * 0.47) / (SR / 2), 'low', output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc / (SR / 2), 'high', output='sos'), x)


def bp(x, f1, f2, order=2):
    return sosfilt(butter(order, [f1 / (SR / 2), min(f2, SR * 0.47) / (SR / 2)], 'band', output='sos'), x)


def adsr(n, a=0.005, d=0.1, s=0.7, r=0.08):
    t = np.arange(n) / SR
    L = n / SR
    e = np.where(t < a, t / max(a, 1e-4), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-4), s))
    return e * np.clip((L - t) / max(r, 1e-4), 0, 1)


def additive(fr, amps, n):
    """a band-limited tone from a frequency curve (Hz per sample) and a spectral recipe amps(k, f0) -> gain"""
    ph = 2 * np.pi * np.cumsum(fr) / SR
    f0 = float(np.median(fr))
    out = np.zeros(n)
    k = 1
    while k * f0 < SR * 0.45 and k <= 40:
        a = amps(k, k * f0)
        if a > 1e-4: out += a * np.sin(k * ph + G.uniform(0, 0.3))
        k += 1
    return out


def formant(fk, centre, width_oct, gain):
    return 1 + gain * np.exp(-0.5 * (np.log2(fk / centre) / width_oct) ** 2)


# ====================================================================== the band
def upright(x, dur, amp=1.0, bright=0.35):
    """plucked upright bass: Karplus-Strong, a body thump under it, the finger's release"""
    f = hz(x)
    n = int(dur * SR)
    N = max(2, int(round(SR / f)))
    buf = lp(noise(N), 500 + 2200 * bright, 1)
    buf -= buf.mean()
    total = n + N
    out = np.zeros(total)
    out[:N] = buf
    damp = 0.9965
    for i in range(N, total, N):
        prev = out[i - N:i]
        nxt = damp * (0.5 * prev + 0.5 * np.roll(prev, 1))
        k = min(N, total - i)
        out[i:i + k] = nxt[:k]
    s = out[:n] / (np.abs(buf).max() + 1e-9)
    t = tt(dur)[:n]
    body = np.sin(2 * np.pi * f * t) * np.exp(-t * 5.0) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 9)
    thump = lp(noise(n), 300) * np.exp(-t * 60) * 0.5
    s = lp(s * 0.8 + body * 0.75 + thump, 1400)
    return amp * s * adsr(n, 0.003, 0, 1, 0.06)


def ride(amp=1.0, bell_=False):
    t = tt(1.6)
    n = len(t)
    s = np.zeros(n)
    for _ in range(36):                                                                  # (a cloud of inharmonic partials, new each stroke)
        f = np.exp(G.uniform(np.log(2200), np.log(11000)))
        s += G.uniform(.3, 1) * np.sin(2 * np.pi * f * t + G.uniform(0, 6)) * np.exp(-t * G.uniform(3.5, 7.0))
    s = s / 14.0 + bp(noise(n), 4000, 12000) * np.exp(-t * 3.2) * 0.55
    s += hp(noise(n), 3000) * np.exp(-t * 90) * 0.9                         # (the stick)
    if bell_: s += 0.8 * np.sin(2 * np.pi * 1180 * t) * np.exp(-t * 2.2) + 0.4 * np.sin(2 * np.pi * 2950 * t) * np.exp(-t * 3)
    return amp * s * adsr(n, 0.001, 0, 1, 0.3)


def crash(amp=1.0):
    t = tt(2.6)
    n = len(t)
    s = hp(noise(n), 2500) * np.exp(-t * 1.6) + 0.4 * bp(noise(n), 800, 4000) * np.exp(-t * 2.5)
    return amp * lp(s, 11000) * adsr(n, 0.002, 0, 1, 0.4)


def chick(amp=1.0):
    t = tt(0.07)
    return amp * (hp(noise(len(t)), 5500) * np.exp(-t * 70) + 0.3 * bp(noise(len(t)), 600, 1800) * np.exp(-t * 90))


def brush_tap(amp=1.0):
    t = tt(0.22)
    s = bp(noise(len(t)), 1800, 9000) * np.exp(-t * 18) * np.clip(t * 400, 0, 1)
    s += 0.25 * np.sin(2 * np.pi * 210 * t) * np.exp(-t * 30)
    return amp * s


def swish(dur, amp=1.0):
    """the brush stirred round the head: a soft rising-and-falling sweep"""
    t = tt(dur)
    n = len(t)
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    s = bp(noise(n), 2500, 8000) * e
    return amp * s


def feather(amp=1.0):
    t = tt(0.4)
    f = 48 + 60 * np.exp(-t * 30)
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def snare_brush(amp=1.0):
    t = tt(0.3)
    s = bp(noise(len(t)), 1500, 8000) * np.exp(-t * 14) + 0.35 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 22)
    return amp * s


def snap(amp=1.0):
    t = tt(0.12)
    s = bp(noise(len(t)), 1400, 4200, 2) * np.exp(-t * 55) + 0.5 * hp(noise(len(t)), 5000) * np.exp(-t * 200)
    return amp * s * np.clip(t * 2000, 0, 1)


def rhodes(notes, dur, amp=1.0):
    t = tt(dur + 0.6)
    n = len(t)
    s = np.zeros(n)
    for x in notes:
        f = hz(x) * (1 + G.uniform(-.0008, .0008))
        idx = 1.4 * np.exp(-t * 5) + 0.25
        tone = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
        tine = 0.18 * np.sin(2 * np.pi * f * 7.02 * t) * np.exp(-t * 14)
        s += (tone * np.exp(-t * 1.1) + tine)
    s /= max(1, len(notes)) ** 0.7
    s *= 1 + 0.12 * np.sin(2 * np.pi * 4.8 * t)
    rel = np.clip((dur + 0.12 - t) / 0.12, 0, 1)                                         # (the key let go)
    return amp * s * rel * adsr(n, 0.002, 0, 1, 0.02)


def vibes(x, dur=1.8, amp=1.0, motor=5.2):
    f = hz(x)
    t = tt(dur)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.1) + 0.28 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t * 4.5) + \
        0.08 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 10)
    s += 0.3 * bp(noise(len(t)), 2000, 6000) * np.exp(-t * 300)                          # (the mallet)
    s *= 1 + 0.32 * np.sin(2 * np.pi * motor * t + G.uniform(0, 6))
    return amp * s * adsr(len(t), 0.001, 0, 1, 0.15)


def _pitch(n, f, scoop=0.0, fall=0.0, vib=0.0, vdelay=0.25, vrate=5.3, gliss_from=None):
    t = np.arange(n) / SR
    L = n / SR
    semis = np.zeros(n)
    if scoop: semis -= scoop * np.exp(-t / 0.045)
    if fall: semis -= fall * np.clip((t - (L - 0.22)) / 0.22, 0, 1) ** 2
    if vib: semis += vib * np.sin(2 * np.pi * vrate * t) * np.clip((t - vdelay) / 0.25, 0, 1)
    return f * 2 ** (semis / 12)


def trumpet(x, dur, amp=1.0, wah=False, fall=0.0, scoop=0.6, muted=True, accent=1.0):
    """a Harmon-muted trumpet: additive brass, the mute's nasal formant (moving with a hand-wah), breath, a scoop"""
    f = hz(x)
    n = int(dur * SR)
    fr = _pitch(n, f, scoop, fall, 0.22 if dur > 0.5 else 0.0)
    t = np.arange(n) / SR
    if muted:
        rec = lambda k, fk: k ** -0.55 * formant(fk, 1900, 0.42, 5.0) * (fk / 700) ** 2 / (1 + (fk / 700) ** 2) / (1 + (fk / 5200) ** 4)
    else:
        rec = lambda k, fk: k ** -0.7 * formant(fk, 1300, 0.7, 1.6) / (1 + (fk / 4200) ** 4)
    s = additive(fr, rec, n)
    if muted and wah and dur > 0.35:                                                     # (the hand opening the mute)
        w = np.clip(t / (dur * 0.7), 0, 1)
        dull = lp(s, 1000)
        s = dull * (1 - w) + s * w
    br = bp(noise(n), 1500, 3800) * 0.05                                                 # (breath)
    e = adsr(n, 0.022, 0.12, 0.72, 0.05)
    blat = 1 + 0.6 * accent * np.exp(-t * 18)
    out = (s / 6.0 * blat + br) * e
    if fall: out *= np.clip((dur - t) / 0.25, 0, 1) ** 0.5
    return amp * out


def clarinet(x, dur, amp=1.0, scoop=0.25, **_trumpet_only):
    f = hz(x)
    n = int(dur * SR)
    fr = _pitch(n, f, scoop, 0, 0.12 if dur > 0.6 else 0.0, 0.3, 5.0)
    def rec(k, fk):
        a = (1.0 / k) if k % 2 else (0.12 / k)
        return a / (1 + (fk / 2600) ** 3)
    s = additive(fr, rec, n)
    br = bp(noise(n), 1000, 3000) * 0.025
    return amp * (s * 0.7 + br) * adsr(n, 0.03, 0.1, 0.85, 0.06)


def accordion(x, dur, amp=1.0):
    """three reeds, the side ones a musette's 14 cents out, through a bellows swell"""
    f = hz(x)
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    rec = lambda k, fk: k ** -0.75 * formant(fk, 1400, 0.8, 1.2) / (1 + (fk / 5000) ** 3)
    for c in (-14, 0, 14):
        s += additive(np.full(n, f * 2 ** (c / 1200)), rec, n)
    s /= 9.0
    return amp * s * adsr(n, 0.018, 0.05, 0.9, 0.04) * (1 + 0.05 * np.sin(2 * np.pi * 3 * t))


# ====================================================================== the track: a circular stereo buffer
class Track:
    def __init__(self):
        self.seconds = BARS * 4 * BEAT
        assert abs(self.seconds - round(self.seconds)) < 1e-9, self.seconds
        self.n = int(round(self.seconds * SR))
        self.L, self.R, self.wL, self.wR = (np.zeros(self.n) for _ in range(4))

    @staticmethod
    def at(bar, beat=0.0):
        b = beat
        fr = b - np.floor(b)
        if abs(fr - 0.5) < 1e-6: b = np.floor(b) + SWING                                 # (a swung "and")
        return (bar * 4 + b) * BEAT

    def add(self, sig, t, pan=0.0, gain=1.0, wet=0.25):
        gl, gr = gain * np.sqrt((1 - pan) / 2), gain * np.sqrt((1 + pan) / 2)
        i0 = int(round(t * SR)) % self.n
        for buf, g in ((self.L, gl * (1 - wet * 0.4)), (self.R, gr * (1 - wet * 0.4)), (self.wL, gl * wet), (self.wR, gr * wet)):
            i, k = i0, 0
            while k < len(sig):                                                          # (wrapping round the end)
                c = min(len(sig) - k, self.n - i)
                buf[i:i + c] += sig[k:k + c] * g
                k += c; i = 0

    def line(self, bar, notes, inst, pan=0.0, gain=1.0, wet=0.3, k=0, **kw):
        """notes: (beat from the bar, note, beats long[, options]) - swung"""
        for nt in notes:
            b, x, d = nt[:3]
            opt = dict(kw); opt.update(nt[3] if len(nt) > 3 else {})
            self.add(inst(m(x) + k, d * BEAT, **opt), self.at(bar, b), pan, gain, wet)

    def render(self, room=1.7):
        n = self.n
        L = int(room * SR)
        ti = np.arange(L) / SR
        def ir():
            r = noise(L) * np.exp(-ti * 6.9 / room)
            r = lp(r, 5500) * np.clip(ti / 0.012, 0, 1)
            for d, g in ((0.011, .5), (0.019, .4), (0.027, .3), (0.041, .25)):          # (a few early reflections off the den's walls)
                r[int(d * SR * G.uniform(.9, 1.1))] += g
            return r / np.sqrt((r ** 2).sum()) * 0.5
        def circ(x, h):
            y = fftconvolve(np.concatenate([x, x[:len(h)]]), h)[:n + len(h)]
            out = y[:n].copy(); out[:len(h)] += y[n:n + len(h)]
            return out
        st = np.stack([self.L + circ(self.wL, ir()), self.R + circ(self.wR, ir())])
        st = hp(st, 36, 2)
        return st


# ====================================================================== the harmony
KINDS = {'m6': (0, 3, 7, 9), 'm7': (0, 3, 7, 10), '7': (0, 4, 7, 10), 'M7': (0, 4, 7, 11), 'hd': (0, 3, 6, 10), '7b9': (0, 4, 7, 10, 13)}
# rootless voicings for the Rhodes (from the root, placed round middle C)
VOICE = {'m6': (3, 9, 14), 'm7': (3, 10, 14), '7': (4, 10, 14), 'M7': (4, 11, 14), 'hd': (3, 6, 10), '7b9': (4, 10, 13)}
VAMP = [[(0, 'C2', 'm6')], [(0, 'Ab1', '7'), (2, 'G1', '7')]]
A = [[(0, 'C2', 'm6')], [(0, 'C2', 'm6')], [(0, 'F1', 'm7')], [(0, 'F1', 'm7')], [(0, 'Ab1', '7')], [(0, 'G1', '7')], [(0, 'C2', 'm6')],
     [(0, 'D2', 'hd'), (2, 'G1', '7')]]
B = [[(0, 'F1', 'm7')], [(0, 'Bb1', '7')], [(0, 'Eb2', 'M7')], [(0, 'Ab1', 'M7')], [(0, 'D2', 'hd')], [(0, 'G1', '7')], [(0, 'C2', 'm6')],
     [(0, 'G1', '7b9')]]
TAG = [[(0, 'Ab1', '7')], [(0, 'G1', '7')], [(0, 'Ab1', '7')], [(0, 'G1', '7')]]
CHART = VAMP + A + A + B + A + TAG + VAMP
assert len(CHART) == BARS
SECTION = ['vamp'] * 2 + ['A1'] * 8 + ['A2'] * 8 + ['B'] * 8 + ['A3'] * 8 + ['tag'] * 4 + ['vamp'] * 2


def chord_at(bar, beat):
    c = CHART[bar % BARS]
    cur = c[0]
    for e in c:
        if e[0] <= beat: cur = e
    return m(cur[1]), cur[2]


def scale_step(root, kind, up=True):
    return root + (2 if kind in ('M7', '7', 'm6', 'm7') else 1)


# ====================================================================== the tunes (beat in the bar, note, beats long[, options])
HOOK = [  # 8 bars, over A
    (0.5, 'G4', .42), (1, 'Ab4', .42), (1.5, 'A4', .42), (2, 'Bb4', 1.0, {'accent': 1.6}), (3.5, 'G4', .45),
    (4, 'Eb5', 1.45, {'wah': True}), (5.5, 'D5', .42), (6, 'C5', 1.0),
    (8.5, 'Ab4', .42), (9, 'A4', .42), (9.5, 'Bb4', .42), (10, 'C5', 1.0, {'accent': 1.6}), (11.5, 'Ab4', .45),
    (12, 'F5', 1.6, {'wah': True, 'fall': 3.0}), (13.5, 'Eb5', .42), (14, 'C5', 1.5),
    (16, 'Eb5', .45), (16.5, 'Gb5', .42, {'scoop': 1.0}), (17, 'F5', .42), (17.5, 'Eb5', .42), (18, 'C5', .9), (19, 'Eb5', .9),
    (20, 'D5', 1.45, {'wah': True}), (21.5, 'B4', .42), (22, 'G4', .9), (23, 'Ab4', .42), (23.5, 'B4', .45),
    (24, 'C5', 2.6, {'wah': True}),
    (28.5, 'Eb5', .42), (29, 'D5', .42), (29.5, 'C5', .42), (30, 'B4', .9), (31, 'G4', .6, {'fall': 2.0})]
HOOK_END = [h for h in HOOK if h[0] < 28] + [(28, 'C5', 2.2, {'wah': True, 'accent': 1.6})]       # (the last chorus lands home)
ANSWER = [  # the clarinet in the hook's rests (A2)
    (6.67, 'C5', .3), (7, 'Eb5', .3), (7.33, 'G5', .3), (7.67, 'Bb5', .55),
    (14.67, 'F5', .3), (15, 'Ab5', .3), (15.33, 'G5', .3), (15.67, 'F5', .3),
    (25, 'G5', .3), (25.33, 'F#5', .3), (25.67, 'G5', .3), (26, 'Bb5', .5), (26.67, 'G5', .3), (27, 'Eb5', .9)]
BRIDGE = [  # the clarinet, 8 bars over B
    (0, 'C5', 1.5), (1.5, 'Ab4', .5), (2, 'F4', .5), (2.5, 'G4', .5), (3, 'Ab4', 1.0),
    (4, 'D5', 1.5), (5.5, 'C5', .5), (6, 'Ab4', 1.0), (7, 'F4', 1.0),
    (8, 'G4', .5), (8.5, 'Bb4', .5), (9, 'Eb5', 1.5), (10.5, 'D5', .5), (11, 'Bb4', 1.0),
    (12, 'C5', 3.0), (15, 'Eb5', .5), (15.5, 'D5', .5),
    (16, 'F5', 1.5), (17.5, 'Eb5', .5), (18, 'D5', .5), (18.5, 'C5', .5), (19, 'Ab4', 1.0),
    (20, 'B4', 1.5), (21.5, 'D5', .5), (22, 'F5', 1.0), (23, 'Ab5', 1.0),
    (24, 'G5', 2.0), (26, 'Eb5', .5), (26.5, 'C5', .5), (27, 'A4', 1.0),
    (28, 'B4', 2.0)]
SHOUT = [  # the tag, 4 bars over Ab7 G7 Ab7 G7
    (0, 'Eb5', .45), (0.5, 'C5', .42), (1, 'Eb5', .45), (1.5, 'Gb5', .9, {'accent': 1.8}), (3, 'F5', .42), (3.5, 'Eb5', .42),
    (4, 'D5', .45), (4.5, 'B4', .42), (5, 'D5', .45), (5.5, 'F5', .9, {'accent': 1.8}), (7, 'G4', .8, {'fall': 2.0}),
    (8, 'Eb5', .45), (8.5, 'C5', .42), (9, 'Eb5', .45), (9.5, 'Gb5', .9, {'accent': 1.8}), (11, 'F5', .42), (11.5, 'Eb5', .42),
    (12, 'D5', .45), (12.5, 'B4', .42), (13, 'G4', .42), (13.5, 'Ab4', .42), (14, 'B4', .42), (14.5, 'D5', .42), (15, 'G5', .35, {'accent': 2.0})]


def at_beat(bar, beat):
    """a beat counted across bars (the tunes run over 8 bars) -> (bar, beat in it)"""
    return bar + int(beat // 4), beat - 4 * int(beat // 4)


def play(tr, bar0, tune, inst, pan, gain, wet, k=0, **kw):
    for nt in tune:
        b, bt = at_beat(bar0, nt[0])
        tr.line(b, [(bt,) + tuple(nt[1:])], inst, pan, gain, wet, k=k, **kw)


# ====================================================================== the parts
def p_bass(tr):
    for bar in range(BARS):
        c = CHART[bar]
        nr, nk = chord_at(bar + 1, 0)
        notes = []
        if len(c) == 1:
            r, kind = m(c[0][1]), c[0][2]
            iv = KINDS[kind]
            pat = [(r, r + iv[1], r + iv[2], None), (r, r + iv[2], r + 12, None), (r + 12, r + iv[3] if len(iv) > 3 else r + 10, r + iv[2], None),
                   (r, scale_step(r, kind), r + iv[1], None)][(bar * 3 + 1) % 4]
            for i, x in enumerate(pat[:3]): notes.append((i, x))
            app = nr + (1 if bar % 3 == 0 else -1)                                       # (a half step into the next chord)
            if app - r > 9: app -= 12
            notes.append((3, app))
        else:
            for (b0, root, kind), b1 in zip(c, [e[0] for e in c[1:]] + [4]):
                r = m(root)
                notes.append((b0, r))
                nxt = (m(c[c.index((b0, root, kind)) + 1][1]) if b1 < 4 else nr)
                notes.append((b0 + 1, nxt + (1 if (bar + b0) % 2 else -1) if b1 - b0 == 2 else r + 7))
        for b, x in notes:
            while x > m('G2'): x -= 12
            while x < m('G1'): x += 12
            sec = SECTION[bar]
            g = 1.0 if sec != 'vamp' else 0.9
            tr.add(upright(x, BEAT * 0.92, 0.55 * g, 0.4 if b == 0 else 0.3), tr.at(bar, b), -0.05, 1, 0.08)
        if SECTION[bar] in ('A3', 'tag') and bar % 2 == 1:                               # (a skip-note ghost, now and then)
            r = notes[-1][1]
            while r > m('G2'): r -= 12
            tr.add(upright(r, BEAT * 0.3, 0.28, 0.2), tr.at(bar, 3.5), -0.05, 1, 0.08)


def p_drums(tr):
    for bar in range(BARS):
        sec = SECTION[bar]
        lvl = 1.25 * {'vamp': 0.8, 'A1': 0.85, 'A2': 0.95, 'B': 0.85, 'A3': 1.05, 'tag': 1.1}[sec]
        # the brush's swish, round every beat; the taps on two and four
        for b in range(4):
            tr.add(swish(BEAT * 0.95, 0.05 * lvl), tr.at(bar, b), 0.15, 1, 0.3)
        for b in (1, 3): tr.add(snare_brush(0.22 * lvl), tr.at(bar, b), 0.1, 1, 0.25)
        for b in (1, 3): tr.add(chick(0.26 * lvl), tr.at(bar, b), 0.3, 1, 0.1)
        # the ride: ding, ding-da ding, ding-da (from the hook on; the vamps keep to brushes and snaps)
        if sec != 'vamp':
            for b in (0, 1, 1.5, 2, 3, 3.5):
                a = 0.16 if b % 1 else (0.22 if b in (1, 3) else 0.19)
                tr.add(ride(a * lvl, bell_=(sec == 'tag' and b == 0)), tr.at(bar, b), 0.35, 1, 0.22)
        # comping accents (a brushed snare on a swung "and", here and there)
        for b in (1.5, 2.5, 3.5):
            if G.random() < (0.35 if sec in ('A3', 'tag') else 0.18):
                tr.add(snare_brush(0.14 * lvl), tr.at(bar, b), 0.05, 1, 0.25)
        # the kick, feathered (felt more than heard); a bomb at the shout's accents
        if sec in ('A3', 'tag', 'A2'):
            for b in range(4): tr.add(feather(0.28 if sec != 'A2' else 0.18), tr.at(bar, b), 0, 1, 0.03)
        if sec == 'tag' and bar in (34, 36): tr.add(feather(0.55), tr.at(bar, 1.5), 0, 1, 0.05); tr.add(snare_brush(0.32), tr.at(bar, 1.5), 0.05, 1, 0.3)
        if sec == 'tag' and bar == 37: tr.add(feather(0.6), tr.at(bar, 3), 0, 1, 0.05); tr.add(crash(0.12), tr.at(bar, 3), -0.3, 1, 0.3)
        # finger snaps in the vamps
        if sec == 'vamp':
            for b in (1, 3): tr.add(snap(0.30), tr.at(bar, b) + G.uniform(-0.004, 0.004), -0.45, 1, 0.3)
            for b in (1, 3): tr.add(snap(0.22), tr.at(bar, b) + 0.012, 0.5, 1, 0.3)
        # fills: a triplet into each section; the big one (bar 39) back to the top
        if bar in (9, 17, 25, 33):
            for i, b in enumerate((3, 3.333, 3.667)):
                tr.add(snare_brush(0.16 + 0.05 * i), tr.at(bar, b), 0.05, 1, 0.3)
        if bar == 39:
            for i, b in enumerate((2, 2.333, 2.667, 3, 3.333, 3.667)):
                tr.add(snare_brush(0.14 + 0.035 * i), tr.at(bar, b), -0.1 + 0.05 * i, 1, 0.3)
            tr.add(feather(0.4), tr.at(bar, 3.667), 0, 1, 0.05)
        if bar in (2, 18, 26):
            tr.add(crash(0.10 if bar != 26 else 0.14), tr.at(bar, 0), -0.3, 1, 0.35)


def p_rhodes(tr):
    rhythms = [[(0, .9), (1.5, .45)], [(0.5, .4), (2, .9)], [(1.5, .45), (3, .7)], [(0, .45), (2.5, .9)]]
    for bar in range(BARS):
        sec = SECTION[bar]
        c = CHART[bar]
        g = {'vamp': 0.85, 'A1': 0.8, 'A2': 0.75, 'B': 0.8, 'A3': 0.85, 'tag': 0.8}[sec]
        hits = rhythms[bar % 4] if len(c) == 1 else [(0, .9), (1.5, .4), (2, .9), (3.5, .4)]
        if sec == 'vamp': hits = [(0, .9), (1.5, .45), (2, .9), (3.5, .45)] if len(c) > 1 else [(0, 1.4), (2.5, .45)]
        for b, d in hits:
            r, kind = chord_at(bar, b)
            vs = [r + v for v in VOICE[kind]]
            while min(vs) < m('E3'): vs = [v + 12 for v in vs]
            while min(vs) > m('C4'): vs = [v - 12 for v in vs]
            tr.add(rhodes(vs, d * BEAT, 0.34 * g), tr.at(bar, b), -0.35, 1, 0.35)


def p_lead(tr):
    # A1: the hook, muted trumpet
    play(tr, 2, HOOK, trumpet, 0.15, 0.75, 0.32)
    # A2: the hook, the clarinet answering, the vibes in its rests
    play(tr, 10, HOOK, trumpet, 0.15, 0.75, 0.32)
    play(tr, 10, ANSWER, clarinet, -0.3, 0.55, 0.38)
    # B: the bridge, clarinet; the trumpet sits out
    play(tr, 18, BRIDGE, clarinet, -0.15, 0.62, 0.36)
    # A3: everyone - the hook with the clarinet an octave down
    play(tr, 26, HOOK_END, trumpet, 0.15, 0.82, 0.32)
    play(tr, 26, HOOK_END, clarinet, -0.25, 0.42, 0.32, k=-12, scoop=0.0)
    # the shout: trumpet and clarinet in octaves
    play(tr, 34, SHOUT, trumpet, 0.18, 0.82, 0.3)
    play(tr, 34, SHOUT, clarinet, -0.25, 0.4, 0.3, k=-12, scoop=0.0)


def p_stabs(tr):
    """open horns, short and punchy, under the last chorus"""
    for bar, b in ((27, 3.5), (29, 3.5), (31, 2.5), (33, 1.5), (33, 2.5)):
        r, kind = chord_at(bar, b)
        vs = [r + v + 12 for v in VOICE[kind]]
        while min(vs) < m('G3'): vs = [v + 12 for v in vs]
        for v in vs: tr.add(trumpet(v, 0.32 * BEAT * 2, 0.45, muted=False, scoop=0.3, accent=1.4), tr.at(bar, b), -0.1 + 0.1 * vs.index(v), 1, 0.35)


def p_vibes(tr):
    # A2: sparkle in the long notes' wake
    for bar0 in (10,):
        for bb, x in ((7, 'G5'), (7.333, 'Bb5'), (7.667, 'D6'), (15, 'C6'), (15.333, 'Ab5'), (15.667, 'F5')):
            b, bt = at_beat(bar0, bb)
            tr.add(vibes(x, 1.6, 0.13), tr.at(b, bt), 0.45, 1, 0.45)
    # B: soft chords on the one, ringing
    for bar in range(18, 26):
        r, kind = chord_at(bar, 0)
        vs = [r + v for v in VOICE[kind]]
        while min(vs) < m('F4'): vs = [v + 12 for v in vs]
        for v in vs: tr.add(vibes(v, 2.4, 0.06), tr.at(bar, 0), 0.45, 1, 0.5)
    # the vamp out: a slinking arpeggio down, then up into the turn
    arp = [(0, 'G5'), (0.5, 'Eb5'), (1, 'C5'), (1.5, 'A4'), (2, 'G4'), (3, 'C5'),
           (4, 'Ab5'), (4.5, 'Gb5'), (5, 'Eb5'), (5.5, 'C5'), (6, 'B4'), (6.5, 'D5'), (7, 'F5'), (7.5, 'Ab5')]
    for bb, x in arp:
        b, bt = at_beat(38, bb)
        tr.add(vibes(x, 1.4, 0.12), tr.at(b, bt), 0.45, 1, 0.45)
    # the intro: a two-note wink
    for bb, x in ((2.5, 'Eb5'), (3, 'G5'), (6.5, 'B4'), (7, 'D5')):
        b, bt = at_beat(0, bb)
        tr.add(vibes(x, 1.4, 0.09), tr.at(b, bt), 0.45, 1, 0.45)


def p_accordion(tr):
    def run(bar, beat, notes, step=1 / 3, last=0.9, gain=0.45):
        for i, x in enumerate(notes):
            d = (last if i == len(notes) - 1 else step * 1.05) * BEAT
            b, bt = at_beat(bar, beat + i * step)
            tr.add(accordion(x, d, gain), tr.at(b, bt), -0.45, 1, 0.35)
    # the bridge: a flourish under the held notes (bar 4 of it) and at its end
    run(21, 1, ['C5', 'D5', 'Eb5', 'F5', 'G5', 'Ab5', 'G5', 'F5', 'Eb5'], last=0.6)
    run(25, 1, ['G4', 'B4', 'D5', 'F5', 'Ab5', 'B5'], last=0.5)
    for i in range(6):                                                                   # (a trill to finish it)
        b, bt = at_beat(25, 3 + i / 6)
        tr.add(accordion('C6' if i % 2 == 0 else 'B5', BEAT / 6 * 1.05, 0.33), tr.at(b, bt), -0.45, 1, 0.35)
    # the shout's end: a wink
    run(37, 2, ['F5', 'Ab5', 'G5'], step=0.25, last=0.4, gain=0.33)
    # the vamp: a run up to the top of the loop
    run(39, 2, ['C5', 'D5', 'Eb5', 'F5', 'G5', 'A5'], last=0.33, gain=0.36)
    # held chord swells under the shout (the musette's wheeze)
    for bar in range(34, 38):
        r, kind = chord_at(bar, 0)
        vs = [r + v + 12 for v in VOICE[kind]]
        while min(vs) < m('E4'): vs = [v + 12 for v in vs]
        for v in vs: tr.add(accordion(v, BEAT * 3.6, 0.1), tr.at(bar, 0), -0.45, 1, 0.4)


def build():
    tr = Track()
    p_bass(tr); p_drums(tr); p_rhodes(tr); p_lead(tr); p_stabs(tr); p_vibes(tr); p_accordion(tr)
    return tr


# ====================================================================== mastering
def _write_wav(st, path):
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1).T * 32767).astype('<i2').tobytes())


def lufs(path):
    r = subprocess.run(['ffmpeg', '-nostats', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True)
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r.stderr)[-1])


def decode(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '2', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).T


def limit(x, knee=0.62, ceil=0.84):
    """a soft knee: under the knee untouched, above it rounded off toward the ceiling"""
    a = np.abs(x)
    over = a > knee
    y = x.copy()
    y[over] = np.sign(x[over]) * (knee + (ceil - knee) * np.tanh((a[over] - knee) / (ceil - knee)))
    return y


def master(st, out):
    st = st / (np.sqrt((st ** 2).mean()) + 1e-12) * 0.1
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, 'm.wav')
    g = 1.0
    for _ in range(5):                                                                   # (to the target loudness, the peaks rounded)
        y = limit(st * g)
        _write_wav(y, wav)
        L = lufs(wav)
        if abs(L - TARGET_LUFS) < 0.15: break
        g *= 10 ** ((TARGET_LUFS - L) / 20)
    ceil = 10 ** (CEIL_DB / 20)
    for _ in range(5):                                                                   # (Vorbis overshoots: check the decoded peak)
        _write_wav(y, wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '4', out], check=True)
        pk = float(np.abs(decode(out)).max())
        if pk <= ceil: break
        y = y * (ceil * 0.995 / pk)
    L = lufs(out)
    os.remove(wav); os.rmdir(tmp)
    print(f'{out}: {y.shape[1] / SR:.2f} s, {L:.1f} LUFS, peak {20 * np.log10(pk):.2f} dBFS, {os.path.getsize(out) // 1024} KB')
    return y, L, pk


def preview(y, path):
    """the loop twice over (so its seam can be heard), the second time faded out"""
    two = np.concatenate([y, y], axis=1)
    k = int(6 * SR); two[:, -k:] *= np.linspace(1, 0, k)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, wav = tempfile.mkstemp(suffix='.wav'); os.close(fd)
    _write_wav(two, wav)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libmp3lame', '-q:a', '2', path], check=True)
    os.remove(wav)
    print(f'{path}: {two.shape[1] / SR:.0f} s (two loops)')


def seam_check(y):
    """the join: the jump across the loop point is no bigger than the music's own sample-to-sample steps"""
    d_seam = np.abs(y[:, 0] - y[:, -1]).max()
    d_typ = np.percentile(np.abs(np.diff(y, axis=1)), 99.9)
    print(f'seam: step {d_seam:.4f} across the loop point (the track\'s own 99.9th percentile step: {d_typ:.4f})')
    assert d_seam <= d_typ * 1.5, 'a click at the loop point'


if __name__ == '__main__':
    tr = build()
    out = os.path.join(VENDOR, 'market_theme.ogg')
    y, L, pk = master(tr.render(), out)
    seam_check(y)
    if 'preview' in sys.argv:
        d = sys.argv[sys.argv.index('preview') + 1]
        preview(y, os.path.join(d, 'market_theme.mp3'))
