"""2.65: synthesises the Gilded Gutter Vault's music (vendor/gv_*.ogg) - one loop per tier, and the boss, the rave, the rats'
rest and the arena. Every track is an exact whole number of seconds and renders circularly (notes and reverb tails that
run past the end wrap round to the start), so it loops without a seam. Stereo, so it plays head-locked in game.
Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg - only to rebuild, never to build the packs).
    python3 tools/gv_music.py [name ...]"""
import numpy as np, subprocess, os, sys, wave
from scipy.signal import lfilter, butter, fftconvolve, sosfilt

SR = 22050
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def m(name):
    """'C#4' -> midi"""
    n, acc, octv = name[0], name[1:-1], int(name[-1])
    return 12 * (octv + 1) + NOTE[n] + acc.count('#') - acc.count('b')


def hz(x):
    if isinstance(x, str): x = m(x)
    return 440.0 * 2 ** ((x - 69) / 12)


def fq(f):
    """a pitch: a note name ('C#4'), a MIDI number (int) or a frequency (float, Hz)"""
    if isinstance(f, str): return hz(m(f))
    if isinstance(f, (int, np.integer)): return hz(int(f))
    return float(f)


def mix(*sigs):
    n = max(len(x) for x in sigs)
    out = np.zeros(n)
    for x in sigs: out[:len(x)] += x
    return out


def T(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, a=0.005, d=0.1, s=0.7, r=0.1, dur=None):
    """ADSR over n samples (r inside the length)"""
    t = np.arange(n) / SR
    L = n / SR
    e = np.where(t < a, t / max(a, 1e-4), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-4), s))
    rel = np.clip((L - t) / max(r, 1e-4), 0, 1)
    return e * rel


def lp(x, fc, order=2):
    sos = butter(order, min(fc, SR / 2 * 0.95) / (SR / 2), 'low', output='sos')
    return sosfilt(sos, x)


def hp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), 'high', output='sos')
    return sosfilt(sos, x)


def bp(x, f1, f2, order=2):
    sos = butter(order, [f1 / (SR / 2), min(f2, SR / 2 * 0.95) / (SR / 2)], 'band', output='sos')
    return sosfilt(sos, x)


class Rng:
    def __init__(self, seed): self.g = np.random.default_rng(seed)
    def noise(self, n): return self.g.uniform(-1, 1, n)
    def r(self): return self.g.random()


R = Rng(265)


# ------------------------------------------------------------------ instruments (mono)
def saw(f, t, detune=0.0):
    ph = t * f * (1 + detune)
    return 2 * (ph - np.floor(ph + 0.5))


def square(f, t, duty=0.5):
    ph = (t * f) % 1.0
    return np.where(ph < duty, 1.0, -1.0)


def pluck(f, dur, bright=0.5, damp=0.996):
    """Karplus-Strong string"""
    n = int(dur * SR); N = max(2, int(SR / fq(f)))
    buf = lp(R.noise(N), 1500 + 5000 * bright, 1)
    out = np.zeros(n + N)
    out[:N] = buf
    for i in range(N, n + N, N):
        prev = out[i - N:i]
        nxt = damp * 0.5 * (prev + np.roll(prev, 1))
        k = min(N, n + N - i)
        out[i:i + k] = nxt[:k]
    s = out[:n]
    return s * env(n, 0.001, 0.0, 1.0, min(0.08, dur / 3))


def ep(f, dur, amp=1.0, trem=4.5):
    """electric piano / vibraphone: FM, a bell-ish attack and a slow tremolo"""
    f = fq(f)
    t = T(dur)
    idx = 1.8 * np.exp(-t * 6)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t * 1.6)
    s *= 1 + 0.25 * np.sin(2 * np.pi * trem * t)
    return amp * s * env(len(t), 0.002, 0, 1, 0.08)


def bell(f, dur, amp=1.0, ratio=3.5, decay=2.0, index=3.0):
    f = fq(f)
    t = T(dur)
    s = np.sin(2 * np.pi * f * t + index * np.exp(-t * 3) * np.sin(2 * np.pi * f * ratio * t))
    return amp * s * np.exp(-t * decay) * env(len(t), 0.001, 0, 1, 0.05)


def bass(f, dur, amp=1.0, cut=900, dec=3.0):
    f = fq(f)
    t = T(dur)
    s = 0.8 * np.sin(2 * np.pi * f * t) + 0.35 * saw(f, t)
    s = lp(s, cut)
    return amp * s * np.exp(-t * dec) * env(len(t), 0.004, 0, 1, 0.04)


def sub(f, dur, amp=1.0):
    f = fq(f)
    t = T(dur)
    return amp * np.sin(2 * np.pi * f * t) * env(len(t), 0.02, 0, 1, 0.15)


def pad(notes, dur, amp=1.0, cut=1400, attack=0.6, release=0.8, voices=3, det=0.006):
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in range(voices):
            s += saw(f, t + R.r(), det * (v - (voices - 1) / 2))
    s = lp(s / (len(notes) * voices), cut, 2)
    return amp * s * env(len(t), attack, 0, 1, release)


def organ(notes, dur, amp=1.0):
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for k, a in ((1, 1.0), (2, 0.6), (3, 0.35), (4, 0.25), (6, 0.12)):
            s += a * np.sin(2 * np.pi * f * k * t)
    s *= 1 + 0.12 * np.sin(2 * np.pi * 6.2 * t)
    return amp * s / len(notes) * env(len(t), 0.01, 0, 1, 0.06) / 2.3


def brass(notes, dur, amp=1.0, bright=2400, swell=0.08):
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in (-0.004, 0.0, 0.004):
            s += saw(f, t, v) * (1 + 0.03 * np.sin(2 * np.pi * 5.5 * t))
    s /= len(notes) * 3
    a = lp(s, bright * 0.45); b = lp(s, bright)
    fe = np.exp(-t * 4)
    s = a * (1 - fe) + b * fe
    return amp * s * env(len(t), swell, 0.2, 0.8, 0.12)


def choir(notes, dur, amp=1.0, attack=0.8):
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in (-0.007, -0.002, 0.003, 0.008):
            s += saw(f, t + R.r(), v) * (1 + 0.05 * np.sin(2 * np.pi * (5 + v * 100) * t))
    s /= len(notes) * 4
    s = bp(s, 600, 1100, 1) * 1.4 + bp(s, 1050, 1500, 1) * 0.7 + bp(s, 2300, 3000, 1) * 0.25     # an 'ah' vowel
    return amp * s * env(len(t), attack, 0, 1, 0.9)


def supersaw(notes, dur, amp=1.0, cut=3500):
    t = T(dur)
    s = np.zeros(len(t))
    for x in notes:
        f = hz(x)
        for v in np.linspace(-0.012, 0.012, 7):
            s += saw(f, t + R.r(), v)
    s = lp(s / (len(notes) * 7), cut)
    return amp * s * env(len(t), 0.01, 0.1, 0.85, 0.08)


def lead(f, dur, amp=1.0, cut=2200, vib=5.5, duty=0.35):
    f = fq(f)
    t = T(dur)
    fv = f * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t * 3, 0, 1))
    ph = np.cumsum(fv) / SR
    s = np.where(ph % 1 < duty, 1.0, -1.0) * 0.6 + 0.4 * (2 * (ph % 1) - 1)
    return amp * lp(s, cut) * env(len(t), 0.01, 0.08, 0.75, 0.06)


def strings(f, dur, amp=1.0, cut=1800):
    """a staccato string section note"""
    f = fq(f)
    t = T(dur)
    s = sum(saw(f, t + R.r(), v) for v in (-0.005, 0, 0.005)) / 3
    return amp * lp(s, cut) * env(len(t), 0.01, 0.06, 0.6, 0.05)


# drums
def kick(amp=1.0, dec=8.0):
    t = T(0.45)
    f = 45 + 110 * np.exp(-t * 28)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * dec)
    s[:60] += R.noise(60) * 0.3
    return amp * s


def snare(amp=1.0, tone=190):
    t = T(0.3)
    nz = bp(R.noise(len(t)), 1200, 7000) * np.exp(-t * 16)
    to = np.sin(2 * np.pi * tone * t) * np.exp(-t * 25)
    return amp * (nz * 0.9 + to * 0.5)


def brush(amp=1.0):
    t = T(0.25)
    return amp * lp(R.noise(len(t)), 5000) * np.exp(-t * 10) * np.clip(t * 60, 0, 1) * 0.6


def hat(amp=1.0, open_=False):
    t = T(0.35 if open_ else 0.06)
    return amp * hp(R.noise(len(t)), 7000) * np.exp(-t * (8 if open_ else 60))


def clap(amp=1.0):
    t = T(0.25)
    e = np.exp(-t * 30) + 0.6 * np.exp(-np.maximum(t - 0.012, 0) * 30) * (t > 0.012) + 0.5 * np.exp(-np.maximum(t - 0.024, 0) * 20) * (t > 0.024)
    return amp * bp(R.noise(len(t)), 900, 5000) * e


def tom(f=90, amp=1.0, dec=6.0, ring=0.3):
    t = T(0.8)
    fr = f * (1 + 0.6 * np.exp(-t * 20))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * dec)
    s += ring * lp(R.noise(len(t)), 900) * np.exp(-t * 18)
    return amp * s


def tick(amp=1.0, f=3200):
    t = T(0.03)
    return amp * np.sin(2 * np.pi * f * t) * np.exp(-t * 200)


def shaker(amp=1.0):
    t = T(0.08)
    return amp * hp(R.noise(len(t)), 5000) * np.sin(np.pi * t / 0.08)


def riser(dur, amp=1.0):
    t = T(dur)
    nz = R.noise(len(t))
    out = np.zeros(len(t)); step = len(t) // 16
    for i in range(16):
        seg = nz[i * step:(i + 1) * step]
        out[i * step:i * step + len(seg)] = bp(seg, 400 + 400 * i, 900 + 600 * i)
    return amp * out * (t / dur) ** 2


# ------------------------------------------------------------------ the track: a circular stereo buffer
class Track:
    def __init__(self, name, bpm, bars, beats=4):
        self.name, self.bpm, self.bars, self.beats = name, bpm, bars, beats
        self.beat = 60.0 / bpm
        self.seconds = bars * beats * self.beat
        assert abs(self.seconds - round(self.seconds)) < 1e-6, (name, self.seconds)
        self.n = int(round(self.seconds * SR))
        self.L = np.zeros(self.n); self.R = np.zeros(self.n)
        self.wetL = np.zeros(self.n); self.wetR = np.zeros(self.n)

    def at(self, bar, beat=0.0):
        return (bar * self.beats + beat) * self.beat

    def add(self, sig, t, pan=0.0, gain=1.0, wet=0.3):
        gl, gr = gain * np.sqrt((1 - pan) / 2), gain * np.sqrt((1 + pan) / 2)
        for buf, g in ((self.L, gl * (1 - wet * 0.5)), (self.R, gr * (1 - wet * 0.5)), (self.wetL, gl * wet), (self.wetR, gr * wet)):
            i = int(round(t * SR)) % self.n; k = 0
            while k < len(sig):                                    # (wrapping round the end, as often as it takes)
                c = min(len(sig) - k, self.n - i)
                buf[i:i + c] += sig[k:k + c] * g
                k += c; i = 0

    def render(self, room=1.8, bright=5000):
        n = self.n
        ir_t = np.arange(int(room * SR)) / SR
        irs = []
        for _ in range(2):
            ir = R.noise(len(ir_t)) * np.exp(-ir_t * 6.9 / room)
            irs.append(lp(ir, bright) * 0.12)
        def circ(x, ir):
            y = fftconvolve(np.concatenate([x, x[:len(ir)]]), ir)[:n + len(ir)]
            out = y[:n].copy(); out[:len(ir)] += y[n:n + len(ir)]
            return out
        L = self.L + circ(self.wetL, irs[0]); Rr = self.R + circ(self.wetR, irs[1])
        mix = np.stack([L, Rr])
        rms = np.sqrt((mix ** 2).mean())
        if rms < 1e-9: return mix.astype(np.float32)
        mix = np.tanh(mix * (0.21 / rms)) * 0.92                    # every track to the same loudness, peaks rounded off
        return mix.astype(np.float32)

    def save(self, room=1.8, bright=5000):
        mix = self.render(room, bright)
        wav = os.path.join('/tmp', f'gv_{self.name}.wav')
        with wave.open(wav, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((mix.T * 32767).astype('<i2').tobytes())
        out = os.path.join(OUT, f'gv_{self.name}.ogg')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '0', out], check=True)
        os.remove(wav)
        print(f'{out}: {self.seconds:.0f} s, {os.path.getsize(out) // 1024} KB')


def chord(root, kind):
    iv = {'m': (0, 3, 7), 'M': (0, 4, 7), 'm7': (0, 3, 7, 10), '7': (0, 4, 7, 10), 'M7': (0, 4, 7, 11), 'dim': (0, 3, 6), 'sus': (0, 5, 7)}[kind]
    r = m(root)
    return [r + i for i in iv]


# ------------------------------------------------------------------ the tracks
def copper():
    """THE COPPER STRONGROOM - a light-fingered swing in D dorian: walking bass, brushes, vibes, a sneaky muted lead"""
    tr = Track('copper', 120, 28)
    prog = [('D3', 'm7'), ('G3', '7'), ('D3', 'm7'), ('A2', 'm7')]
    sw = 2 / 3
    for bar in range(28):
        root, kind = prog[bar % 4]
        ch = chord(root, kind)
        # walking bass: root, chord tone, chord tone, an approach to the next root
        nxt = m(prog[(bar + 1) % 4][0])
        walk = [ch[0] - 12, ch[1 + bar % 2] - 12, ch[2] - 12, nxt - 12 + (1 if bar % 2 else -1)]
        for b, x in enumerate(walk):
            tr.add(mix(pluck(hz(x), tr.beat * 0.95, 0.25, 0.993) * 0.9, bass(x, tr.beat * 0.9, 0.5, 600, 2.0)), tr.at(bar, b), -0.1, 0.9, 0.15)
        # brushes and a swung ride
        if bar < 24 or bar % 2 == 0:
            for b in (1, 3): tr.add(brush(0.6), tr.at(bar, b), 0.2, 1, 0.35)
            for b in (0, 1, 1 + sw, 2, 3, 3 + sw): tr.add(hat(0.18 if b % 1 else 0.25), tr.at(bar, b), 0.45, 1, 0.2)
            tr.add(kick(0.45, 12), tr.at(bar, 0), 0, 1, 0.05)
        # vibes comp (the Charleston: the 1 and the and-of-2)
        if bar < 24:
            for b in (0, 1 + sw):
                for x in ch[1:] + [ch[0] + 12]:
                    tr.add(ep(hz(x + 12), 0.9, 0.16), tr.at(bar, b), -0.35, 1, 0.45)
    motif = [(0, 'D5', .4), (sw, 'F5', .3), (1, 'G5', .4), (1 + sw, 'A5', .3), (2, 'C6', .9), (3 + sw, 'A5', .3),
             (4, 'G5', .5), (4 + sw, 'F5', .3), (5, 'E5', .4), (5 + sw, 'D5', .3), (6, 'C5', .6), (7, 'D5', 1.0)]
    motif2 = [(0, 'A5', .3), (sw, 'A5', .3), (1, 'G5', .3), (1 + sw, 'F5', .3), (2, 'G5', .6), (3, 'E5', .3), (3 + sw, 'C5', .3),
              (4, 'D5', .5), (5, 'F5', .4), (5 + sw, 'E5', .3), (6, 'D5', .4), (6 + sw, 'C5', .3), (7, 'D5', .9)]
    for ph, mo in ((8, motif), (12, motif2), (16, motif), (20, motif2)):
        for b, x, d in mo:
            tr.add(lead(x, d, 0.32, 1500, 5, 0.3), tr.at(ph, 0) + b * tr.beat, 0.25, 1, 0.35)
    for bar in (16, 18, 20, 22):                                   # horn stabs
        for b in (0, 2.5):
            tr.add(brass([x + 12 for x in chord(prog[bar % 4][0], prog[bar % 4][1])[:3]], 0.25, 0.35, 2200, 0.01), tr.at(bar, b), -0.2, 1, 0.3)
    return tr


def silver():
    """THE SILVER VAULTS - cold and careful in A minor: a music box, a ticking clock, strings, a harp"""
    tr = Track('silver', 96, 24)
    prog = [('A3', 'm'), ('F3', 'M'), ('C3', 'M'), ('E3', 'M')]
    for bar in range(24):
        ch = chord(*prog[bar % 4])
        tr.add(pad([x for x in ch], tr.beat * 4 + 0.6, 0.22, 1100, 0.9, 1.0), tr.at(bar), 0, 1, 0.5)
        tr.add(sub(ch[0] - 12, tr.beat * 3.8, 0.5), tr.at(bar), 0, 1, 0.05)
        for b in range(8): tr.add(tick(0.22 if b % 2 == 0 else 0.12, 3600 if b % 2 == 0 else 2900), tr.at(bar, b / 2), 0.5, 1, 0.25)
        arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24, ch[2] + 12, ch[1] + 12, ch[0] + 24, ch[1] + 24]
        if bar >= 4:
            for i, x in enumerate(arp + arp):
                tr.add(bell(hz(x + 12), 0.7, 0.10, 2.0, 3.5, 1.2), tr.at(bar, i / 4), (-0.6 if i % 2 else 0.6), 1, 0.5)
    mel = ['E5', 'A5', 'C6', 'B5', 'A5', 'G5', 'A5', 'E5', 'F5', 'A5', 'C6', 'D6', 'C6', 'B5', 'G5', 'E5']
    for ph in (8, 16):
        for i, x in enumerate(mel):
            tr.add(bell(x, 1.8, 0.28, 3.01, 1.4, 2.2), tr.at(ph + i // 2, (i % 2) * 2), 0.1, 1, 0.55)
    for bar in (7, 15, 23):                                         # a harp glissando into each section
        for i, x in enumerate([57, 60, 64, 65, 69, 72, 76, 77, 81, 84]):
            tr.add(pluck(hz(x), 1.2, 0.7, 0.995) * 0.35, tr.at(bar, 3) + i * 0.05, -0.3 + i * 0.06, 1, 0.5)
    return tr


def gold():
    """THE GOLD RESERVE - a spy-film surf riff in E minor: twang guitar, organ stabs, a driving beat"""
    tr = Track('gold', 135, 36)
    riff = ['E2', 'E2', 'G2', 'E2', 'A2', 'E2', 'A#2', 'B2']
    for bar in range(36):
        sec = bar // 4
        alt = 'C' if 20 <= bar < 28 else 'E'
        for i, x in enumerate(riff):
            xx = m(x) + (8 if alt == 'C' and bar % 2 == 0 else (7 if alt == 'C' else 0))
            tr.add(mix(pluck(hz(xx), tr.beat * 0.5, 0.6, 0.99) * 0.75, bass(xx, tr.beat * 0.45, 0.35, 900, 5)), tr.at(bar, i / 2), -0.15, 1, 0.15)
        if bar >= 4:
            for b in (0, 2): tr.add(kick(0.75), tr.at(bar, b), 0, 1, 0.05)
            for b in (1, 3): tr.add(snare(0.5), tr.at(bar, b), 0.1, 1, 0.3)
            for b in range(8): tr.add(hat(0.14 + 0.06 * (b % 2 == 0)), tr.at(bar, b / 2), 0.4, 1, 0.15)
        if 4 <= bar < 32 and bar % 2 == 1:
            stab = [m('E4'), m('G4'), m('B4'), m('D#5')] if alt == 'E' else [m('C4'), m('E4'), m('G4'), m('B4')]
            for b in (1.5, 3):
                tr.add(organ(stab, 0.3, 0.5), tr.at(bar, b), 0.35, 1, 0.3)
    theme = [('E4', 1), ('F#4', .5), ('G4', .5), ('F#4', 1), ('E4', 1), ('B3', 1.5), ('D4', .5), ('E4', 2),
             ('G4', 1), ('A4', .5), ('A#4', .5), ('B4', 1.5), ('A4', .5), ('G4', 1), ('F#4', 1), ('E4', 2)]
    for ph in (4, 12, 28):
        t0 = tr.at(ph)
        for x, d in theme:
            s = pluck(hz(x) * 2, d * tr.beat * 0.98, 0.8, 0.997)
            s = s * (1 + 0.2 * np.sin(2 * np.pi * 7 * T(len(s) / SR)))         # tremolo arm
            tr.add(s * 0.6, t0, 0.3, 1, 0.55); t0 += d * tr.beat
    bridge = ['G5', 'E5', 'C5', 'E5', 'G5', 'B5', 'A5', 'G5', 'F#5', 'D#5', 'B4', 'D#5', 'F#5', 'A5', 'G5', 'F#5']
    for i, x in enumerate(bridge):
        tr.add(lead(x, tr.beat * 1.9, 0.25, 1800), tr.at(20 + i // 2, (i % 2) * 2), 0.2, 1, 0.45)
    return tr


def diamond():
    """THE DIAMOND DEPOSIT - deep and drifting in F# minor: wide pads, sonar pings, a slow pulse"""
    tr = Track('diamond', 80, 20)
    prog = [('F#3', 'm'), ('D3', 'M'), ('A3', 'M'), ('E3', 'M')]
    for bar in range(20):
        ch = chord(*prog[bar % 4])
        tr.add(pad(ch + [ch[0] + 12], tr.beat * 4 + 1.2, 0.25, 900, 1.6, 1.5, 4, 0.009), tr.at(bar), 0, 1, 0.6)
        tr.add(sub(ch[0] - 12, tr.beat * 4, 0.55), tr.at(bar), 0, 1, 0.05)
        if bar % 2 == 0: tr.add(kick(0.35, 5), tr.at(bar, 0), 0, 1, 0.2)
        if bar >= 2:
            for i in range(16):                                       # bubbles: a soft plucked arpeggio
                x = ch[i % 3] + 24 + (12 if i % 8 == 7 else 0)
                tr.add(pluck(hz(x), 0.3, 0.2, 0.98) * 0.12, tr.at(bar, i / 4), np.sin(i) * 0.7, 1, 0.6)
        if bar % 2 == 1:                                              # sonar: a ping and its echoes
            for k in range(4):
                tr.add(bell(hz('C#6'), 1.5, 0.22 * 0.55 ** k, 1.0, 2.5, 0.4), tr.at(bar, 2) + k * tr.beat * 0.75, (-0.5, 0.5)[k % 2], 1, 0.6)
    mel = ['C#5', 'E5', 'F#5', 'A5', 'G#5', 'E5', 'C#5', 'B4']
    for ph in (8, 12):
        for i, x in enumerate(mel):
            tr.add(bell(x, 2.4, 0.2, 2.0, 1.2, 1.0), tr.at(ph + i // 2, (i % 2) * 2), 0.2, 1, 0.7)
    return tr


def hoard():
    """THE GUTTER KING'S HOARD - ominous and grand in C minor: ostinato strings, brass, timpani, a choir, a tolling bell"""
    tr = Track('hoard', 90, 24)
    prog = [('C3', 'm'), ('G#2', 'M'), ('F3', 'm'), ('G3', 'M')]
    for bar in range(24):
        ch = chord(*prog[bar % 4])
        ost = [ch[0], ch[0] + 12, ch[1], ch[0] + 12, ch[2], ch[0] + 12, ch[1], ch[0] + 12]
        for i, x in enumerate(ost):
            tr.add(strings(x, tr.beat * 0.45, 0.33, 1600), tr.at(bar, i / 2), -0.3, 1, 0.3)
        tr.add(tom(55, 0.9, 4), tr.at(bar, 0), 0, 1, 0.35)
        tr.add(tom(55, 0.5, 5), tr.at(bar, 3.5), 0, 1, 0.35)
        if bar >= 4:
            tr.add(brass([ch[0] + 12, ch[1] + 12, ch[2] + 12], tr.beat * 3.6, 0.4, 2000, 0.25), tr.at(bar), 0.25, 1, 0.45)
        if bar >= 12:
            tr.add(choir([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[0] + 24], tr.beat * 4 + 0.5, 0.5, 1.0), tr.at(bar), 0, 1, 0.6)
        if bar % 4 == 0:
            tr.add(bell(hz('C3'), 4.0, 0.35, 1.41, 0.7, 2.5), tr.at(bar), -0.1, 1, 0.6)
    theme = [('G4', 2), ('C5', 1), ('D#5', 1), ('D5', 2), ('C5', 1), ('G#4', 1), ('F4', 2), ('G#4', 1), ('C5', 1), ('B4', 4)]
    for ph in (8, 16):
        t0 = tr.at(ph)
        for x, d in theme:
            tr.add(brass([x], d * tr.beat * 0.95, 0.42, 2600, 0.06), t0, 0.1, 1, 0.5); t0 += d * tr.beat
    return tr


def boss():
    """THE GUARDIAN - 150 BPM in D minor: driving bass, pounding drums, brass hits, a racing arpeggio, a choir"""
    tr = Track('boss', 150, 40)
    prog = [('D3', 'm'), ('A#2', 'M'), ('C3', 'M'), ('A2', 'M')]
    for bar in range(40):
        ch = chord(*prog[bar % 4])
        for i in range(8):
            x = ch[0] - 12 + (12 if i % 4 == 3 else 0)
            tr.add(bass(x, tr.beat * 0.45, 0.7, 700, 6), tr.at(bar, i / 2), 0, 1, 0.05)
        for b in range(4): tr.add(kick(0.8), tr.at(bar, b), 0, 1, 0.05)
        for b in (1, 3): tr.add(snare(0.6), tr.at(bar, b), 0.1, 1, 0.3)
        for b in range(16): tr.add(hat(0.1 + 0.05 * (b % 4 == 2)), tr.at(bar, b / 4), 0.4, 1, 0.1)
        if bar % 2 == 0:
            for b in (0, 1.5):
                tr.add(brass([x + 12 for x in ch], 0.35, 0.45, 2600, 0.01), tr.at(bar, b), -0.25, 1, 0.35)
        if bar >= 8:
            arp = [ch[0] + 24, ch[1] + 24, ch[2] + 24, ch[1] + 24]
            for i in range(16):
                tr.add(lead(hz(arp[i % 4] + (12 if bar % 8 >= 4 and i % 8 == 7 else 0)), tr.beat * 0.24, 0.16, 2600, 0, 0.25), tr.at(bar, i / 4), 0.35, 1, 0.3)
        if bar >= 24:
            tr.add(choir([ch[0] + 12, ch[1] + 12, ch[2] + 12], tr.beat * 4, 0.45, 0.4), tr.at(bar), 0, 1, 0.5)
        if bar % 8 == 7: tr.add(riser(tr.beat * 4, 0.25), tr.at(bar), 0, 1, 0.3)
    return tr


def rave():
    """THE RAT RAVE - 128 BPM in A minor: four on the floor, a pumping supersaw, an offbeat bass, a hook"""
    tr = Track('rave', 128, 32)
    prog = [('A3', 'm'), ('F3', 'M'), ('C4', 'M'), ('G3', 'M')]
    pump = lambda n: np.clip((np.arange(n) / SR) / (tr.beat * 0.45), 0.25, 1.0) ** 1.5
    for bar in range(32):
        ch = chord(*prog[bar % 4])
        brk = 12 <= bar < 16
        if not brk:
            for b in range(4): tr.add(kick(1.0, 9), tr.at(bar, b), 0, 1, 0.03)
            for b in (1, 3): tr.add(clap(0.55), tr.at(bar, b), 0.05, 1, 0.3)
            for b in range(4): tr.add(hat(0.3, True), tr.at(bar, b + 0.5), 0.3, 1, 0.15)
            for b in range(4):
                x = ch[0] - 12 + (12 if b % 2 else 0)
                tr.add(bass(x, tr.beat * 0.4, 0.75, 1200, 3), tr.at(bar, b + 0.5), 0, 1, 0.05)
        for b in range(4):
            s = supersaw([x + 12 for x in ch], tr.beat * 0.95, 0.42 if not brk else 0.6, 2400 if not brk else 1500)
            if not brk: s = s * pump(len(s))
            tr.add(s, tr.at(bar, b), 0, 1, 0.4)
        if bar == 15: tr.add(riser(tr.beat * 4, 0.4), tr.at(bar), 0, 1, 0.3)
    hook = [('A5', .5), ('C6', .5), ('E6', .5), ('A5', .5), ('G5', .5), ('E5', .5), ('C6', 1), ('A5', .5), ('C6', .5), ('E6', .5), ('G6', .5),
            ('F6', 1), ('E6', .5), ('D6', .5)]
    for ph in range(16, 32, 4):
        t0 = tr.at(ph)
        for x, d in hook + hook[:6]:
            tr.add(supersaw([m(x)], d * tr.beat * 0.9, 0.28, 3800), t0, 0.15, 1, 0.4); t0 += d * tr.beat
    return tr


def rest():
    """THE RATS' REST - 72 BPM in G major: a fingerpicked guitar, a warm pad, a music box tune"""
    tr = Track('rest', 72, 18)
    prog = [('G3', 'M'), ('E3', 'm'), ('C3', 'M'), ('D3', 'M')]
    for bar in range(18):
        ch = chord(*prog[bar % 4])
        tr.add(pad(ch, tr.beat * 4 + 1, 0.14, 800, 1.5, 1.5), tr.at(bar), 0, 1, 0.5)
        pick = [ch[0] - 12, ch[2], ch[1] + 12, ch[2], ch[0] + 12, ch[2], ch[1] + 12, ch[2]]
        for i, x in enumerate(pick):
            tr.add(pluck(hz(x), tr.beat * 1.5, 0.35, 0.997) * 0.5, tr.at(bar, i / 2), (-0.3 if i % 2 else 0.2), 1, 0.4)
        if bar % 2 == 1: tr.add(shaker(0.08), tr.at(bar, 1.5), 0.6, 1, 0.3)
    tune = ['B5', 'D6', 'G6', 'F#6', 'E6', 'D6', 'B5', 'A5', 'G5', 'A5', 'B5', 'D6', 'C6', 'B5', 'A5', 'G5']
    for ph in (2, 10):
        for i, x in enumerate(tune):
            tr.add(bell(x, 1.6, 0.18, 2.0, 2.2, 1.6), tr.at(ph + i // 2, (i % 2) * 2), 0.25, 1, 0.5)
    return tr


def arena():
    """THE PIT - 144 BPM in E minor: war drums, brass, a choir, racing strings"""
    tr = Track('arena', 144, 36)
    prog = [('E3', 'm'), ('C3', 'M'), ('D3', 'M'), ('B2', 'M')]
    for bar in range(36):
        ch = chord(*prog[bar % 4])
        for i, f in enumerate((90, 0, 120, 90, 0, 120, 75, 75)):
            if f: tr.add(tom(f, 0.55, 7, 0.4), tr.at(bar, i / 2), (-0.4, 0.4)[i % 2], 1, 0.3)
        tr.add(kick(0.8), tr.at(bar, 0), 0, 1, 0.05); tr.add(kick(0.6), tr.at(bar, 2), 0, 1, 0.05)
        tr.add(snare(0.65), tr.at(bar, 1), 0.1, 1, 0.3); tr.add(snare(0.65), tr.at(bar, 3), 0.1, 1, 0.3)
        for i in range(16):
            tr.add(strings(ch[i % 3] + 12, tr.beat * 0.22, 0.2, 2200), tr.at(bar, i / 4), -0.3, 1, 0.25)
        if bar % 2 == 0: tr.add(brass([x + 12 for x in ch], tr.beat * 1.8, 0.4, 2600, 0.03), tr.at(bar), 0.25, 1, 0.4)
        if bar >= 12: tr.add(choir([x + 12 for x in ch] + [ch[0] + 24], tr.beat * 4, 0.4, 0.3), tr.at(bar), 0, 1, 0.5)
    theme = [('E5', 1.5), ('G5', .5), ('B5', 2), ('A5', 1), ('G5', 1), ('F#5', 2), ('G5', 1.5), ('A5', .5), ('B5', 1), ('D6', 1), ('B5', 4)]
    for ph in (12, 20, 28):
        t0 = tr.at(ph)
        for x, d in theme:
            tr.add(brass([x], d * tr.beat * 0.95, 0.38, 3000, 0.04), t0, 0.1, 1, 0.45); t0 += d * tr.beat
    return tr


def silence():
    tr = Track('silence', 120, 1)
    return tr


TRACKS = {'copper': copper, 'silver': silver, 'gold': gold, 'diamond': diamond, 'hoard': hoard, 'boss': boss, 'rave': rave,
          'rest': rest, 'arena': arena, 'silence': silence}
LENGTH = {'copper': 56, 'silver': 60, 'gold': 64, 'diamond': 60, 'hoard': 64, 'boss': 64, 'rave': 60, 'rest': 60, 'arena': 60, 'silence': 2}

if __name__ == '__main__':
    for nm in (sys.argv[1:] or list(TRACKS)):
        tr = TRACKS[nm]()
        assert round(tr.seconds) == LENGTH[nm], (nm, tr.seconds)
        tr.save(room=2.6 if nm in ('diamond', 'hoard', 'silver') else 1.6)
