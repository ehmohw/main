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

THE NIGHTS (3.00): the same tune, chart, form and 75 s, re-dressed for each of the pack's custom nights (phase250 picks one):
  lucky     vendor/market_lucky.ogg     C MAJOR (Eb Gb Ab Bb up a half step, a chromatic run kept chromatic; the chart re-voiced:
                                        C6 Fmaj7 Am7 G7 Dm7, the bridge Fmaj7 Dm7 Em7 Am7), a lighter swing, the open horn,
                                        glockenspiel doubling the hook, chimes, wind chimes, a tambourine and a triangle
  blood     vendor/market_blood.ogg     CmM7 and the dominant's flat nine, a low string pedal (tremolo in the tag), the organ from
                                        the bridge on, war drums (boom, tom, rimshots, timpani rolls), the trumpet growling, a
                                        bass clarinet, the bridge on a cello's line, a bell tolling
  invasion  vendor/market_invasion.ogg  an arpeggiating analog synth bass, a drum machine (909 kick, clap, hats), synth-brass
                                        stabs comping, the hook on a pulse lead, a gliding theremin answering and taking the
                                        bridge, two-tone alarms, laser zaps, the ship's computer chattering
  dread     vendor/market_dread.ogg     35 cents flat and wavering (circular tape wow), a music box with the hook, a violin's
                                        answers with a ghost a tritone off, the bridge on the violin (a semitone ghost),
                                        a glassy cluster, a celesta, a heartbeat for the kick, a clock ticking

Deterministic; run it to rebuild (needs numpy, scipy and ffmpeg - only to rebuild, never to build the packs):
    python3 tools/market_music.py [base] [lucky|blood|invasion|dread|nights] [preview DIR]
        (no names: the theme alone, vendor/market_theme.ogg; "nights": all four variants; + DIR/<name>.mp3, two loops)"""
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


DETUNE = 0.0                                # (cents, the whole band: the Dread Night's variant sits flat)


def hz(x):
    return 440.0 * 2 ** ((m(x) - 69) / 12 + DETUNE / 1200)


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
    def __init__(self, bars=None, beat=None, swing=None):
        self.bars, self.beat, self.swing = bars or BARS, beat or BEAT, SWING if swing is None else swing
        self.seconds = self.bars * 4 * self.beat
        assert abs(self.seconds - round(self.seconds)) < 1e-9, self.seconds
        self.n = int(round(self.seconds * SR))
        self.L, self.R, self.wL, self.wR = (np.zeros(self.n) for _ in range(4))

    def at(self, bar, beat=0.0):
        b = beat
        fr = b - np.floor(b)
        if abs(fr - 0.5) < 1e-6: b = np.floor(b) + self.swing                            # (a swung "and"; swing 0.5 = straight)
        return (bar * 4 + b) * self.beat

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
            self.add(inst(m(x) + k, d * self.beat, **opt), self.at(bar, b), pan, gain, wet)

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
KINDS = {'m6': (0, 3, 7, 9), 'm7': (0, 3, 7, 10), '7': (0, 4, 7, 10), 'M7': (0, 4, 7, 11), 'hd': (0, 3, 6, 10), '7b9': (0, 4, 7, 10, 13),
         '6': (0, 4, 7, 9), 'mM7': (0, 3, 7, 11)}                      # (the last two: the Lucky Night's C6, the Blood Moon's CmM7)
# rootless voicings for the Rhodes (from the root, placed round middle C)
VOICE = {'m6': (3, 9, 14), 'm7': (3, 10, 14), '7': (4, 10, 14), 'M7': (4, 11, 14), 'hd': (3, 6, 10), '7b9': (4, 10, 13), '6': (4, 9, 14), 'mM7': (3, 11, 14)}
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
    return root + (2 if kind in ('M7', '7', 'm6', 'm7', '6') else 1)


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


def nm(x):
    """a written note as tonight's band plays it (the Lucky Night's major key; the others leave it be)"""
    return NOTEMAP(x) if isinstance(x, str) else x


NOTEMAP = m


def at_beat(bar, beat):
    """a beat counted across bars (the tunes run over 8 bars) -> (bar, beat in it)"""
    return bar + int(beat // 4), beat - 4 * int(beat // 4)


def play(tr, bar0, tune, inst, pan, gain, wet, k=0, **kw):
    for nt in tune:
        b, bt = at_beat(bar0, nt[0])
        tr.line(b, [(bt,) + tuple(nt[1:])], inst, pan, gain, wet, k=k, **kw)


# ====================================================================== the parts
def p_bass(tr, amp=0.55, inst=None):
    inst = inst or upright
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
            tr.add(inst(x, BEAT * 0.92, amp * g, 0.4 if b == 0 else 0.3), tr.at(bar, b), -0.05, 1, 0.08)
        if SECTION[bar] in ('A3', 'tag') and bar % 2 == 1:                               # (a skip-note ghost, now and then)
            r = notes[-1][1]
            while r > m('G2'): r -= 12
            tr.add(inst(r, BEAT * 0.3, amp * 0.28 / 0.55, 0.2), tr.at(bar, 3.5), -0.05, 1, 0.08)


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


def p_rhodes(tr, inst=None, gain=0.34, pan=-0.35, wet=0.35, only=None):
    inst = inst or rhodes
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
            if only and (b, d) != hits[0]: continue                                    # (only the bar's first hit, held: a sparser comp)
            tr.add(inst(vs, (only or d) * BEAT, gain * g), tr.at(bar, b), pan, 1, wet)


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


def p_vibes(tr, inst=None, gain=1.0):
    inst = inst or vibes
    # A2: sparkle in the long notes' wake
    for bar0 in (10,):
        for bb, x in ((7, 'G5'), (7.333, 'Bb5'), (7.667, 'D6'), (15, 'C6'), (15.333, 'Ab5'), (15.667, 'F5')):
            b, bt = at_beat(bar0, bb)
            tr.add(inst(nm(x), 1.6, 0.13 * gain), tr.at(b, bt), 0.45, 1, 0.45)
    # B: soft chords on the one, ringing
    for bar in range(18, 26):
        r, kind = chord_at(bar, 0)
        vs = [r + v for v in VOICE[kind]]
        while min(vs) < m('F4'): vs = [v + 12 for v in vs]
        for v in vs: tr.add(inst(v, 2.4, 0.06 * gain), tr.at(bar, 0), 0.45, 1, 0.5)
    # the vamp out: a slinking arpeggio down, then up into the turn
    arp = [(0, 'G5'), (0.5, 'Eb5'), (1, 'C5'), (1.5, 'A4'), (2, 'G4'), (3, 'C5'),
           (4, 'Ab5'), (4.5, 'Gb5'), (5, 'Eb5'), (5.5, 'C5'), (6, 'B4'), (6.5, 'D5'), (7, 'F5'), (7.5, 'Ab5')]
    for bb, x in arp:
        b, bt = at_beat(38, bb)
        tr.add(inst(nm(x), 1.4, 0.12 * gain), tr.at(b, bt), 0.45, 1, 0.45)
    # the intro: a two-note wink
    for bb, x in ((2.5, 'Eb5'), (3, 'G5'), (6.5, 'B4'), (7, 'D5')):
        b, bt = at_beat(0, bb)
        tr.add(inst(nm(x), 1.4, 0.09 * gain), tr.at(b, bt), 0.45, 1, 0.45)


def p_accordion(tr):
    def run(bar, beat, notes, step=1 / 3, last=0.9, gain=0.45):
        for i, x in enumerate(notes):
            d = (last if i == len(notes) - 1 else step * 1.05) * BEAT
            b, bt = at_beat(bar, beat + i * step)
            tr.add(accordion(nm(x), d, gain), tr.at(b, bt), -0.45, 1, 0.35)
    # the bridge: a flourish under the held notes (bar 4 of it) and at its end
    run(21, 1, ['C5', 'D5', 'Eb5', 'F5', 'G5', 'Ab5', 'G5', 'F5', 'Eb5'], last=0.6)
    run(25, 1, ['G4', 'B4', 'D5', 'F5', 'Ab5', 'B5'], last=0.5)
    for i in range(6):                                                                   # (a trill to finish it)
        b, bt = at_beat(25, 3 + i / 6)
        tr.add(accordion(nm('C6' if i % 2 == 0 else 'B5'), BEAT / 6 * 1.05, 0.33), tr.at(b, bt), -0.45, 1, 0.35)
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


# ====================================================================== THE NIGHTS (3.00): the same tune, re-dressed for each night
# Same chart, same form, same 40 bars and 75 s (phase250 times every one alike) - the band changes its clothes.
def glock(x, dur=1.4, amp=1.0, **_):
    """glockenspiel: a struck steel bar (1 : 2.76 : 5.40 : 8.93), the mallet's tick (it rings on past a short note)"""
    f = hz(x); t = tt(max(dur, 1.0)); n = len(t)
    s = np.zeros(n)
    for r, a, d in ((1.0, 1.0, 2.4), (2.76, .32, 6), (5.40, .16, 11), (8.93, .06, 18)):
        if f * r < SR * 0.45: s += a * np.sin(2 * np.pi * f * r * t + G.uniform(0, 6)) * np.exp(-t * d)
    s += 0.2 * hp(noise(n), 5000) * np.exp(-t * 500)
    return amp * s * adsr(n, 0.0005, 0, 1, 0.12)


def chime(x, dur=3.5, amp=1.0, **_):
    """a tubular bell (its strike tone and its long inharmonic ring)"""
    f = hz(x); t = tt(dur); n = len(t)
    s = np.zeros(n)
    for r, a, d in ((0.5, .25, 0.8), (1.0, .5, 1.2), (2.0, 1.0, 1.0), (3.0, .6, 1.6), (4.2, .45, 2.2), (5.4, .3, 3.0), (6.8, .18, 4.0)):
        if f * r < SR * 0.45: s += a * np.sin(2 * np.pi * f * r * t + G.uniform(0, 6)) * np.exp(-t * d)
    s += 0.2 * bp(noise(n), 2000, 7000) * np.exp(-t * 300)
    return amp * s / 2.2 * adsr(n, 0.001, 0, 1, 0.3)


def windchimes(tr, t0, amp=0.05, span=1.4, pan=0.55, notes=('C6', 'D6', 'E6', 'G6', 'A6', 'C7', 'D7', 'E7')):
    for i in range(12):
        x = notes[int(G.integers(len(notes)))]
        tr.add(glock(x, 1.6, amp * G.uniform(.6, 1.0)), t0 + span * i / 12 + G.uniform(0, 0.03), pan + G.uniform(-.25, .25), 1, 0.55)


def tamb(amp=1.0):
    t = tt(0.25); n = len(t)
    s = np.zeros(n)
    for d in (0, 0.006, 0.013, 0.021):                                                    # (the jingles, a hair apart)
        s += bp(noise(n), 6000, 14000) * np.exp(-np.maximum(t - d, 0) * 45) * (t >= d)
    return amp * s * 0.5


def triangle(amp=1.0):
    t = tt(1.5); f = 2640.0
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.71 * t) * np.exp(-t * 2) + 0.3 * np.sin(2 * np.pi * f * 4.1 * t) * np.exp(-t * 3)
    return amp * s * np.exp(-t * 1.8) * adsr(len(t), 0.001, 0, 1, 0.2) * 0.4


def bowed(x, dur, amp=1.0, bright=0.5, trem=0.0, vib=0.0, voices=3, attack=0.25, **_):
    """a bowed string section (voices > 1) or one string: band-limited sawtooths a hair apart, the bow's hiss"""
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for v in range(voices):
        det = 1 + (v - (voices - 1) / 2) * 0.004
        vb = vib * np.sin(2 * np.pi * (5.2 + 0.4 * v) * t + G.uniform(0, 6)) * np.clip((t - 0.15) / 0.3, 0, 1)
        s += additive(f * det * 2 ** (vb / 12), lambda k, fk: (1.0 / k) / (1 + (fk / (900 + 3500 * bright)) ** 2), n)
    s = lp(s / voices, 1200 + 5000 * bright) + 0.02 * bp(noise(n), 2000, 6000)
    if trem: s *= 0.6 + 0.4 * np.abs(np.sin(np.pi * trem * t))
    return amp * s * adsr(n, attack, 0.1, 0.9, min(0.3, dur * 0.3))


def organ(notes, dur, amp=1.0, **_):
    """a pipe organ: 16', 8', 4', 2 2/3', 2', 1 1/3', 1' - and a slow wobble"""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for x in notes:
        f = hz(x)
        for r, a in ((0.5, .5), (1, 1), (2, .6), (3, .35), (4, .3), (6, .12), (8, .1)):
            if f * r < SR * 0.45: s += a * np.sin(2 * np.pi * f * r * t + G.uniform(0, 6))
    s /= max(1, len(notes)) ** 0.7 * 2.5
    s *= 1 + 0.15 * np.sin(2 * np.pi * 5.8 * t)
    return amp * s * adsr(n, 0.06, 0.1, 0.95, 0.15)


def growl(x, dur, amp=1.0, **kw):
    """the muted trumpet growling (flutter-tongued, pushed into the mute)"""
    s = trumpet(x, dur, 1.0, **kw); t = np.arange(len(s)) / SR
    s = s * (1 + 0.4 * np.sin(2 * np.pi * 31 * t))
    return amp * np.tanh(s * 2.2) / 2.2 * 1.2


def boom(amp=1.0):
    t = tt(0.8); f = 42 + 90 * np.exp(-t * 25)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5) + 0.3 * lp(noise(len(t)), 1500) * np.exp(-t * 60)
    return amp * s * adsr(len(t), 0.001, 0, 1, 0.1)


def tom(x, amp=1.0):
    f = hz(x); t = tt(0.8)
    fr = f * (1 + 0.4 * np.exp(-t * 20))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 6) + 0.25 * bp(noise(len(t)), 200, 2500) * np.exp(-t * 30)
    return amp * s * adsr(len(t), 0.001, 0, 1, 0.1)


def timp(x, dur=1.8, amp=1.0, roll=0.0):
    """a timpani: a hit (or, roll=s, a roll crescendoing over that long)"""
    f = hz(x)
    def hit(a):
        t = tt(dur); s = np.zeros(len(t))
        for r, g, d in ((1, 1, 2.2), (1.5, .5, 3), (1.99, .35, 3.5), (2.44, .2, 5)):
            s += g * np.sin(2 * np.pi * f * r * t * (1 + 0.02 * np.exp(-t * 30)) + G.uniform(0, 6)) * np.exp(-t * d)
        s += 0.3 * lp(noise(len(t)), 900) * np.exp(-t * 40)
        return a * s
    if not roll: return amp * hit(1.0)
    k = int(roll / 0.055); out = np.zeros(int((roll + dur) * SR))
    for i in range(k):
        h = hit(0.25 + 0.75 * i / k); j = int(i * 0.055 * SR); out[j:j + len(h)] += h[:len(out) - j]
    return amp * out * 0.45


def rimshot(amp=1.0):
    t = tt(0.2)
    return amp * (bp(noise(len(t)), 1800, 9000) * np.exp(-t * 30) + 0.5 * np.sin(2 * np.pi * 330 * t) * np.exp(-t * 40) +
                  0.4 * np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 90))


def heartbeat(tr, t, amp=0.5):
    tr.add(boom(amp), t, 0, 1, 0.08); tr.add(boom(amp * 0.7), t + 0.3, 0, 1, 0.08)


def synbass(x, dur, amp=1.0, bright=0.4, cut=1600, res=0.8):
    """an analog synth bass: a sawtooth and a sine sub, its filter snapping shut (a resonant peak riding it)"""
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    saw = additive(np.full(n, f), lambda k, fk: (1.0 / k) / (1 + (fk / 7000) ** 2), n)
    env = np.exp(-t * (16 - 8 * bright))
    hi, lo = lp(saw, cut), lp(saw, 260)
    s = lo + (hi - lo) * env + res * bp(saw, cut * 0.6, cut * 1.0) * env
    return amp * (0.7 * s + 0.55 * np.sin(2 * np.pi * f * t)) * adsr(n, 0.002, 0.05, 0.85, 0.03)


def pulse(x, dur, amp=1.0, duty=0.28, vib=0.15, scoop=0.0, accent=1.0, **_):
    """a pulse-wave synth lead (its duty cycle the colour), a delayed vibrato"""
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    fr = _pitch(n, f, scoop, 0, vib if dur > 0.4 else 0, 0.15, 6.0)
    s = additive(fr, lambda k, fk: abs(np.sin(np.pi * k * duty)) / k / (1 + (fk / 5200) ** 2), n)
    return amp * s * 0.5 * adsr(n, 0.004, 0.08, 0.75, 0.04) * (1 + 0.4 * (accent - 1) * np.exp(-t * 15))


def stab(notes, dur, amp=1.0):
    """a synth-brass stab: sawtooths through a filter that opens and closes"""
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for x in notes:
        for c in (-8, 8):
            s += additive(np.full(n, hz(x) * 2 ** (c / 1200)), lambda k, fk: (1.0 / k) / (1 + (fk / 6000) ** 2), n)
    s /= 2 * max(1, len(notes)) ** 0.7
    env = np.clip(t / 0.03, 0, 1) * np.exp(-t * 6)
    s = lp(s, 500) + (lp(s, 3500) - lp(s, 500)) * env
    return amp * s * adsr(n, 0.005, 0.1, 0.7, 0.05)


def glide_line(notes, amp=1.0, vib=0.35, rate=6.2, glide=0.06, harm=(1, .18, .07), wobble=0.0, attack=0.04):
    """one continuous voice gliding from note to note - a theremin: notes are (start s, midi, length s); -> (signal, start)"""
    t0 = notes[0][0]; t1 = max(a + d for a, _x, d in notes) + 0.25
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    tgt = np.full(n, float(notes[0][1])); gate = np.zeros(n)
    for a, x, d in notes:
        i, j = int((a - t0) * SR), int((a + d - t0) * SR)
        tgt[i:] = x; gate[i:j] = 1
    from scipy.signal import lfilter
    k = np.exp(-1 / (glide * SR)); semis = lfilter([1 - k], [1, -k], tgt, zi=[tgt[0] * k])[0]
    ka = np.exp(-1 / (attack * SR)); g = lfilter([1 - ka], [1, -ka], gate)
    semis = semis + vib * np.sin(2 * np.pi * rate * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.37 * t)) + wobble * np.sin(2 * np.pi * 0.8 * t)
    f = 440.0 * 2 ** ((semis - 69) / 12 + DETUNE / 1200)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(h * np.sin((i + 1) * ph) for i, h in enumerate(harm))
    return amp * s * g * 0.6, t0


def kick909(amp=1.0):
    t = tt(0.45); f = 50 + 120 * np.exp(-t * 35)
    return amp * (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + 0.3 * hp(noise(len(t)), 2000) * np.exp(-t * 300))


def clap(amp=1.0):
    t = tt(0.3); n = len(t)
    s = np.zeros(n)
    for d in (0, 0.009, 0.018):
        s += bp(noise(n), 900, 5000) * np.exp(-np.maximum(t - d, 0) * 120) * (t >= d)
    s += 0.5 * bp(noise(n), 900, 4000) * np.exp(-t * 18) * (t >= 0.024)
    return amp * s


def hat(amp=1.0, open_=False):
    t = tt(0.5 if open_ else 0.08)
    return amp * hp(noise(len(t)), 7000) * np.exp(-t * (9 if open_ else 60))


def siren(dur, amp=1.0, lo='A5', hi='Eb6', rate=4.0):
    """a two-tone alarm: odd harmonics (a buzzer's square), lo-hi-lo-hi"""
    n = int(dur * SR); t = np.arange(n) / SR
    up = (np.floor(t * rate) % 2).astype(float)
    from scipy.signal import lfilter
    k = np.exp(-1 / (0.012 * SR)); up = lfilter([1 - k], [1, -k], up)
    f = hz(lo) * (hz(hi) / hz(lo)) ** up
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(h * ph) / h for h in (1, 3, 5, 7))
    return amp * lp(s, 4000) * adsr(n, 0.01, 0, 1, 0.05) * 0.5


def zap(amp=1.0, f0=3200, f1=180, dur=0.28):
    t = tt(dur); f = f1 + (f0 - f1) * np.exp(-t * 14)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * (np.sin(ph) + 0.3 * np.sin(3 * ph)) * np.exp(-t * 7) * adsr(len(t), 0.001, 0, 1, 0.03)


def blip(x, amp=1.0, dur=0.09):
    f = hz(x); t = tt(dur)
    return amp * np.sin(2 * np.pi * f * t * (1 + 0.03 * np.exp(-t * 60))) * np.exp(-t * 30) * adsr(len(t), 0.001, 0, 1, 0.01)


def musicbox(x, dur=1.6, amp=1.0, **_):
    """a music box's comb: a steel tine plucked (each a few cents out - a worn old box)"""
    f = hz(x) * 2 ** (G.uniform(-9, 9) / 1200); t = tt(max(dur, 1.4)); n = len(t)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6) + 0.2 * np.sin(2 * np.pi * 2.0 * f * t) * np.exp(-t * 5)
    if f * 5.4 < SR * 0.45: s += 0.25 * np.sin(2 * np.pi * 5.4 * f * t) * np.exp(-t * 14)
    if f * 11.2 < SR * 0.45: s += 0.08 * np.sin(2 * np.pi * 11.2 * f * t) * np.exp(-t * 30)
    s += 0.15 * hp(noise(n), 4000) * np.exp(-t * 600)
    return amp * s * adsr(n, 0.0005, 0, 1, 0.1)


def celesta(x, dur=1.6, amp=1.0, **_):
    f = hz(x); t = tt(max(dur, 1.2)); n = len(t)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6) + 0.25 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3) + 0.08 * np.sin(2 * np.pi * 3.98 * f * t) * np.exp(-t * 6)
    s += 0.2 * lp(noise(n), 1500) * np.exp(-t * 200)
    return amp * s * adsr(n, 0.001, 0, 1, 0.15)


def violin(x, dur, amp=1.0, trem=0.0, scoop=0.15, vib=0.17, bright=1.0, **_):
    """a bowed violin (after tools/dread_music.py's): a band-limited saw, the scoop and a vibrato that arrives late, the body's
    resonances, the bow on the string, an optional bowed tremolo"""
    f = hz(x); n = int(dur * SR); t = np.arange(n) / SR
    fr = _pitch(n, f, scoop, 0, vib if dur > 0.35 else 0.0, 0.14, 5.8)
    s = additive(fr, lambda k, fk: (1.0 / k) * (1.0 if k < 6 else 0.8 ** (k - 6) * bright) / (1 + (fk / 9000) ** 4), n)
    body = bp(s, 260, 520) * 1.1 + bp(s, 700, 1300) * 0.55 + bp(s, 2000, 3600) * 0.9 * bright + bp(s, 4200, 6500) * 0.25 * bright + s * 0.18
    s = body + 0.035 * hp(noise(n), 2500) * (1 + 3 * np.exp(-t / 0.03))
    if trem: s *= 0.65 + 0.35 * np.abs(np.sin(np.pi * trem * t))
    return amp * s * adsr(n, 0.035, 0.08, 0.85, 0.07) / 1.6


def tick(amp=1.0, f=1900):
    t = tt(0.08)
    return amp * (bp(noise(len(t)), 1200, 3500) * np.exp(-t * 120) + 0.6 * np.sin(2 * np.pi * f * t) * np.exp(-t * 70))


def rumble(dur, amp=1.0):
    t = tt(dur); n = len(t)
    return amp * lp(noise(n), 90, 4) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2 * 6


def wow(st, depth=0.009, cycles=17, fdepth=0.00018, fcycles=300):
    """tape wow and flutter, circular (a whole number of wobbles in the loop, so the seam stays seamless)"""
    n = st.shape[1]; i = np.arange(n)
    d = (depth * (1 + np.sin(2 * np.pi * cycles * i / n)) + fdepth * (1 + np.sin(2 * np.pi * fcycles * i / n))) / 2 * SR
    pos = (i - d) % n; j = np.floor(pos).astype(int); fr = pos - j
    return np.stack([c[j] * (1 - fr) + c[(j + 1) % n] * fr for c in st])


# ---- the night's notes: the Lucky Night plays in C major (Eb, Gb, Ab, Bb up a half step; a chromatic run kept chromatic)
LUCKY_PC = {3: 4, 6: 7, 8: 9, 10: 11}


def _major(x):
    x = m(x)
    return x - x % 12 + LUCKY_PC.get(x % 12, x % 12)


def brighten(tune):
    xs = [m(nt[1]) for nt in tune]
    ys = [_major(x) for x in xs]
    for i in range(len(ys) - 1):
        if ys[i] == ys[i + 1] and xs[i] != xs[i + 1] and abs(tune[i + 1][0] - tune[i][0]) < 1: ys[i] -= 1    # (G Ab A -> G G# A)
    return [(nt[0], ys[i]) + tuple(nt[2:]) for i, nt in enumerate(tune)]


def rechart(table):
    """the chart re-voiced: each (root, kind) -> (new root's pitch class, kind), the root kept nearest where it was"""
    out = []
    for bar in CHART:
        nb = []
        for b, root, kind in bar:
            r = m(root); pc = r % 12
            npc, nk = table.get((pc, kind), (pc, kind))
            nr = min((r - r % 12 + npc + o for o in (-12, 0, 12)), key=lambda v: abs(v - r))
            nb.append((b, nr, nk))
        out.append(nb)
    return out


LUCKY_CHART = {(0, 'm6'): (0, '6'), (5, 'm7'): (5, 'M7'), (8, '7'): (9, 'm7'), (2, 'hd'): (2, 'm7'), (10, '7'): (2, 'm7'),
               (3, 'M7'): (4, 'm7'), (8, 'M7'): (9, 'm7'), (7, '7b9'): (7, '7')}
BLOOD_CHART = {(0, 'm6'): (0, 'mM7'), (7, '7'): (7, '7b9')}


def tune_at(tr, bar0, tune):
    """a tune's notes as (seconds, midi, seconds) - for the gliding voices"""
    out = []
    for nt in tune:
        b, bt = at_beat(bar0, nt[0])
        out.append((tr.at(b, bt), m(nt[1]), nt[2] * tr.beat))
    return out


def glide(tr, bar0, tune, pan, gain, wet, k=0, **kw):
    s, t0 = glide_line([(a, x + k, d) for a, x, d in tune_at(tr, bar0, tune)], **kw)
    tr.add(s, t0, pan, gain, wet)


# ---- LUCKY NIGHT: "Members Only (Feeling Lucky)" - C major, a lighter swing, the open horn, glockenspiel and chimes, a tambourine
def v_lucky(tr):
    p_bass(tr, 0.55); p_rhodes(tr, gain=0.32)
    p_drums(tr)
    for bar in range(BARS):
        sec = SECTION[bar]
        if sec != 'vamp':
            for b in (1, 3): tr.add(tamb(0.28), tr.at(bar, b), 0.5, 1, 0.25)
            if sec in ('A3', 'tag'): tr.add(tamb(0.18), tr.at(bar, 3.5), 0.5, 1, 0.25)
    for bar in (2, 10, 18, 26, 34): tr.add(triangle(0.22), tr.at(bar, 0), 0.6, 1, 0.4)
    H, HE, AN, BR, SH = (brighten(x) for x in (HOOK, HOOK_END, ANSWER, BRIDGE, SHOUT))
    play(tr, 2, H, trumpet, 0.15, 0.75, 0.32)
    play(tr, 2, H, glock, 0.5, 0.11, 0.45, k=12)
    play(tr, 10, H, trumpet, 0.15, 0.7, 0.32, muted=False, scoop=0.3)
    play(tr, 10, AN, clarinet, -0.3, 0.55, 0.38)
    play(tr, 18, BR, clarinet, -0.15, 0.62, 0.36)
    for bar in range(18, 26):
        r, kind = chord_at(bar, 0)
        tr.add(chime(r + 36 + VOICE[kind][1] % 12, 3.0, 0.16), tr.at(bar, 0), 0.4, 1, 0.5)
    play(tr, 26, HE, trumpet, 0.15, 0.76, 0.32, muted=False, scoop=0.3)
    play(tr, 26, HE, clarinet, -0.25, 0.42, 0.32, k=-12, scoop=0.0)
    play(tr, 26, HE, glock, 0.5, 0.09, 0.45, k=12)
    play(tr, 34, SH, trumpet, 0.18, 0.76, 0.3, muted=False, scoop=0.3)
    play(tr, 34, SH, clarinet, -0.25, 0.4, 0.3, k=-12, scoop=0.0)
    p_stabs(tr)
    p_vibes(tr, glock, 0.9)
    p_vibes(tr, vibes, 0.5)
    p_accordion(tr)
    for bar in (0, 18, 26, 38): windchimes(tr, tr.at(bar, 0), 0.05)


# ---- BLOOD MOON: "Members Only (Blood Moon)" - CmM7, the dominant's flat nine, a low string pedal, the organ, war-drum swing,
#      the trumpet growling, a bass clarinet, a bell tolling
def v_blood(tr):
    p_bass(tr, 0.55)
    for bar in range(BARS):                                                              # (the low strings: a pedal under it all)
        sec = SECTION[bar]
        if bar % 2: continue
        r, _k = chord_at(bar, 0)
        ped = {'vamp': 'C2', 'A1': 'C2', 'A2': 'C2', 'A3': 'C2', 'B': None, 'tag': 'Ab1'}[sec]
        roots = [m(ped)] if ped else [r - 12 if r > m('G2') else r]
        if sec == 'tag' and bar == 36: roots = [m('G1')]
        for x in roots:
            for o in (0, 12, 19):
                tr.add(bowed(x + o, 8 * BEAT + 0.4, 0.09 if o else 0.11, 0.3, trem=(8 if sec == 'tag' else 0), voices=3, attack=0.6), tr.at(bar, 0), -0.2 + 0.2 * (o > 0), 1, 0.4)
    for bar in range(BARS):                                                              # (the organ: the chords, whole bars, from the bridge)
        if SECTION[bar] not in ('B', 'A3', 'tag'): continue
        for b0, root, kind in CHART[bar]:
            r = m(root); vs = [r + v for v in VOICE[kind]]
            while min(vs) < m('C3'): vs = [v + 12 for v in vs]
            d = (4 if len(CHART[bar]) == 1 else 2) * BEAT
            tr.add(organ(vs, d, 0.22 if SECTION[bar] == 'B' else 0.17), tr.at(bar, b0), 0.3, 1, 0.45)
    p_rhodes(tr, gain=0.24)
    # the drums: a war-drum swing - the boom on one and three, the tom on four's "and", rimshots on two and four
    for bar in range(BARS):
        sec = SECTION[bar]
        lvl = {'vamp': 0.8, 'A1': 0.85, 'A2': 0.95, 'B': 0.85, 'A3': 1.05, 'tag': 1.15}[sec]
        for b in ((0,) if sec == 'vamp' else (0, 2)): tr.add(boom(0.42 * lvl), tr.at(bar, b), 0, 1, 0.1)
        if sec != 'vamp':
            for b in (1, 3): tr.add(rimshot(0.3 * lvl), tr.at(bar, b), 0.1, 1, 0.3)
            tr.add(tom('A2', 0.3 * lvl), tr.at(bar, 3.5), -0.25, 1, 0.3)
            for b in (0, 1, 1.5, 2, 3, 3.5):
                a = 0.12 if b % 1 else 0.15
                tr.add(lp(ride(a * lvl), 5500), tr.at(bar, b), 0.35, 1, 0.25)
        for b in range(4): tr.add(swish(BEAT * 0.95, 0.04 * lvl), tr.at(bar, b), 0.15, 1, 0.3)
        if sec == 'vamp': heartbeat(tr, tr.at(bar, 1), 0.3); heartbeat(tr, tr.at(bar, 3), 0.25)
        if bar in (9, 17, 25, 33): tr.add(timp('G1', 1.4, 0.4, roll=2 * BEAT), tr.at(bar, 2), 0, 1, 0.3)
        if bar in (2, 18, 26, 34): tr.add(timp('C2', 2.0, 0.55), tr.at(bar, 0), 0, 1, 0.3); tr.add(crash(0.12), tr.at(bar, 0), -0.3, 1, 0.35)
        if bar == 39:
            for i, b in enumerate((2, 2.333, 2.667, 3, 3.333, 3.667)): tr.add(tom(('D3', 'C3', 'A2', 'G2', 'E2', 'C2')[i], 0.3 + 0.04 * i), tr.at(bar, b), -0.3 + 0.12 * i, 1, 0.3)
    for bar in (0, 18, 26, 34): tr.add(chime('C3', 5.0, 0.3), tr.at(bar, 0), -0.4, 1, 0.55)
    # the lead: the hook growled; a bass clarinet answering; the bridge on the low strings (a cello's line) and the clarinet
    play(tr, 2, HOOK, growl, 0.15, 0.8, 0.32)
    play(tr, 10, HOOK, growl, 0.15, 0.8, 0.32)
    play(tr, 10, ANSWER, clarinet, -0.3, 0.6, 0.38, k=-12)
    play(tr, 18, BRIDGE, bowed, -0.2, 0.42, 0.36, k=-12, voices=1, vib=0.18, bright=0.6, attack=0.06)
    play(tr, 18, BRIDGE, clarinet, 0.2, 0.3, 0.36)
    play(tr, 26, HOOK_END, growl, 0.15, 0.78, 0.32)
    play(tr, 26, HOOK_END, bowed, -0.25, 0.3, 0.32, k=-12, voices=3, vib=0.12, bright=0.5, attack=0.05)
    play(tr, 34, SHOUT, growl, 0.18, 0.78, 0.3)
    play(tr, 34, SHOUT, clarinet, -0.25, 0.45, 0.3, k=-12, scoop=0.0)
    p_stabs(tr)
    p_vibes(tr, chime, 0.6)


# ---- INVASION: "Members Only (Invasion)" - an arpeggiating synth bass, a drum machine, a pulse lead, a theremin answering, alarms
def v_invasion(tr):
    for bar in range(BARS):                                                              # (the synth bass: the chord's tones, every swung eighth)
        sec = SECTION[bar]
        for i in range(8):
            b = i / 2
            r, kind = chord_at(bar, b)
            while r > m('C2'): r -= 12
            iv = KINDS[kind]
            x = r + [0, 12, iv[2], 12, 0, iv[3] if len(iv) > 3 else 10, iv[2], 12][i]
            if sec == 'vamp' and i % 2: continue
            tr.add(synbass(x, BEAT * 0.42, 0.24 if i % 2 == 0 else 0.18, bright=0.5 if i % 4 == 0 else 0.3, cut=1500 + 500 * (sec in ('A3', 'tag'))),
                   tr.at(bar, b), -0.05, 1, 0.06)
    def stabs_ch(vs, d, g): return stab(vs, d, g)
    p_rhodes(tr, inst=stabs_ch, gain=0.3, pan=-0.3, wet=0.3)
    p_rhodes(tr, gain=0.16)
    for bar in range(BARS):
        sec = SECTION[bar]
        lvl = {'vamp': 0.8, 'A1': 0.85, 'A2': 0.95, 'B': 0.85, 'A3': 1.05, 'tag': 1.1}[sec]
        for b in ((0, 2) if sec == 'vamp' else range(4)): tr.add(kick909(0.4 * lvl), tr.at(bar, b), 0, 1, 0.05)
        for b in (1, 3): tr.add(clap(0.35 * lvl), tr.at(bar, b), 0.1, 1, 0.3)
        for i in range(8):
            if sec == 'vamp' and i % 2 == 0: continue
            tr.add(hat(0.16 * lvl * (1.3 if i % 2 else 0.8)), tr.at(bar, i / 2), 0.35, 1, 0.15)
        if bar % 2 and sec != 'vamp': tr.add(hat(0.08 * lvl, True), tr.at(bar, 3.5), 0.35, 1, 0.2)
        if sec in ('A3', 'tag'):
            for b in (0, 1, 1.5, 2, 3, 3.5): tr.add(ride(0.12 if b % 1 else 0.15), tr.at(bar, b), 0.4, 1, 0.22)
        if bar in (9, 17, 25, 33, 39):
            for j in range(8): tr.add(snare_brush(0.1 + 0.03 * j), tr.at(bar, 2) + j * BEAT / 4, 0.05, 1, 0.3)
        if bar in (2, 18, 26, 34): tr.add(crash(0.13), tr.at(bar, 0), -0.3, 1, 0.35)
    # the alarms: a two-tone buzzer into the hook, the bridge and the shout; laser zaps in the vamps
    for bar, beats in ((1, 2), (17, 2), (33, 2), (37, 2)):
        tr.add(siren(beats * BEAT, 0.2), tr.at(bar, 4 - beats), 0.3, 1, 0.35)
    for bar in (0, 1, 38, 39):
        for b in (1.5, 3.5): tr.add(zap(0.08, f0=G.uniform(2500, 4000)), tr.at(bar, b), G.uniform(-.6, .6), 1, 0.4)
    # the lead: the hook on the pulse; the theremin answers and takes the bridge
    play(tr, 2, HOOK, pulse, 0.15, 0.75, 0.3)
    play(tr, 10, HOOK, pulse, 0.15, 0.75, 0.3)
    glide(tr, 10, ANSWER, -0.3, 0.5, 0.4, k=0, vib=0.3)
    glide(tr, 18, BRIDGE, -0.15, 0.62, 0.38, vib=0.35, wobble=0.08)
    play(tr, 26, HOOK_END, pulse, 0.15, 0.75, 0.3)
    play(tr, 26, HOOK_END, pulse, -0.2, 0.22, 0.32, k=12, duty=0.5)
    play(tr, 34, SHOUT, pulse, 0.18, 0.75, 0.3)
    play(tr, 34, SHOUT, trumpet, -0.25, 0.4, 0.3, k=-12, muted=False, scoop=0.0)
    p_stabs(tr)
    for bar in range(18, 26):                                                            # (the bridge: the ship's computer, chattering)
        for i in range(16):
            if G.random() < 0.45: continue
            r, kind = chord_at(bar, i / 4)
            x = r + 48 + KINDS[kind][int(G.integers(len(KINDS[kind])))]
            tr.add(blip(x, 0.05), tr.at(bar, 0) + i * BEAT / 4, G.uniform(-.7, .7), 1, 0.4)
    p_vibes(tr, vibes, 0.7)


# ---- DREAD NIGHT: "Members Only (Dread)" - all of it flat and wavering (tape wow), a music box with the hook, a violin's dissonant
#      answers, a celesta, a heartbeat for the drums, a clock ticking
def v_dread(tr):
    p_bass(tr, 0.42)
    def dread_ep(vs, d, g): return lp(rhodes(vs, d, g), 1800)
    p_rhodes(tr, inst=dread_ep, gain=0.3, only=2.5)
    for bar in range(BARS):
        sec = SECTION[bar]
        if sec in ('vamp', 'B'): heartbeat(tr, tr.at(bar, 0), 0.36 if sec == 'vamp' else 0.3)
        if sec in ('A1', 'A2', 'A3', 'tag'):
            for b in range(4): tr.add(swish(BEAT * 0.95, 0.04), tr.at(bar, b), 0.15, 1, 0.35)
            for b in (1, 3): tr.add(chick(0.18), tr.at(bar, b), 0.3, 1, 0.15)
            if sec in ('A3', 'tag'): tr.add(boom(0.25), tr.at(bar, 0), 0, 1, 0.1)
        if sec in ('vamp', 'B'):
            for b in range(4): tr.add(tick(0.16 if b % 2 else 0.2, 1900 if b % 2 else 1500), tr.at(bar, b), 0.5 * (-1) ** b, 1, 0.3)
    for bar in (18, 34): tr.add(rumble(4.0, 0.5), tr.at(bar, 0), 0, 1, 0.2)
    # the lead: the hook on a music box, an octave up; a violin's answers, and a second a tritone off; the bridge on the violin
    play(tr, 2, HOOK, musicbox, 0.2, 0.36, 0.45, k=12)
    play(tr, 10, HOOK, musicbox, 0.2, 0.36, 0.45, k=12)
    play(tr, 10, ANSWER, violin, -0.3, 0.42, 0.42)
    play(tr, 10, ANSWER, violin, 0.35, 0.14, 0.5, k=-6, trem=9)
    play(tr, 18, BRIDGE, violin, -0.15, 0.5, 0.42)
    play(tr, 18, BRIDGE, violin, 0.4, 0.1, 0.5, k=1, trem=11, bright=0.5)
    for bar in range(18, 26):                                                            # (a glassy cluster under the bridge)
        r, _k = chord_at(bar, 0)
        for o in (24, 25): tr.add(bowed(r + o, 4 * BEAT + 0.3, 0.035, 0.8, trem=7, voices=2, attack=0.8), tr.at(bar, 0), 0.5 if o == 24 else -0.5, 1, 0.6)
    play(tr, 26, HOOK_END, celesta, 0.2, 0.4, 0.45, k=12)
    play(tr, 26, HOOK_END, violin, -0.25, 0.38, 0.4, k=-12)
    play(tr, 34, SHOUT, violin, -0.2, 0.45, 0.4)
    play(tr, 34, SHOUT, musicbox, 0.3, 0.3, 0.45, k=12)
    p_vibes(tr, celesta, 1.2)


NIGHTS = {'lucky': (v_lucky, 0.61, 0.0), 'blood': (v_blood, 0.67, 0.0), 'invasion': (v_invasion, 0.62, 0.0), 'dread': (v_dread, 0.64, -35.0)}
NIGHT_FILE = {'lucky': 'market_lucky', 'blood': 'market_blood', 'invasion': 'market_invasion', 'dread': 'market_dread'}


def build_night(name):
    """one night's re-dressing of the theme (each its own seed; the chart and the tunes put back after)"""
    global G, CHART, NOTEMAP, DETUNE
    part, swing, det = NIGHTS[name]
    saved = (G, CHART, NOTEMAP, DETUNE)
    G = np.random.default_rng(2990 + 1 + list(NIGHTS).index(name))
    try:
        if name == 'lucky': CHART, NOTEMAP = rechart(LUCKY_CHART), _major
        if name == 'blood': CHART = rechart(BLOOD_CHART)
        DETUNE = det
        tr = Track(swing=swing)
        part(tr)
        st = tr.render(room=2.4 if name in ('dread', 'blood') else 1.7)
        if name == 'dread': st = wow(st)
        return st
    finally:
        G, CHART, NOTEMAP, DETUNE = saved


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
    args = sys.argv[1:]
    d = args[args.index('preview') + 1] if 'preview' in args else None
    names = [a for a in args if a in NIGHTS or a in ('base', 'nights')]
    if 'nights' in names: names = [n for n in names if n != 'nights'] + list(NIGHTS)
    if not names: names = ['base']
    for name in dict.fromkeys(names):
        stem = 'market_theme' if name == 'base' else NIGHT_FILE[name]
        out = os.path.join(VENDOR, stem + '.ogg')
        if name == 'base': G = np.random.default_rng(2990)                               # (as on import: the theme as it was)
        y, L, pk = master(build().render() if name == 'base' else build_night(name), out)
        seam_check(y)
        if d: preview(y, os.path.join(d, stem + '.mp3'))
