"""2.26: synthesises the Blood Moon music disc (vendor/blood_moon.ogg) - a slow D harmonic-minor piece: an organ pad,
a heartbeat, a tolling bell and a music-box melody. Deterministic; run it to rebuild the .ogg (needs numpy + ffmpeg)."""
import numpy as np, subprocess, wave, os, sys
SR = 22050
BPM = 72
BEAT = 60 / BPM
BARS = 28
N = int(SR * (BARS * 4 * BEAT + 4))
out = np.zeros(N)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def add(sig, t0):
    i = int(t0 * SR)
    j = min(N, i + len(sig))
    out[i:j] += sig[:j - i]


def pad(notes, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.4).clip(0)
    s = np.zeros_like(t)
    for m in notes:
        f = hz(m)
        for k in range(1, 7):                                   # a soft organ: odd-leaning harmonics
            s += np.sin(2 * np.pi * f * k * t * (1 + 0.0015 * (k % 2))) / k ** 1.6
    trem = 1 + 0.12 * np.sin(2 * np.pi * 0.35 * t)
    return amp * s * env * trem / len(notes)


def box(m, dur, amp):                                           # a music-box tine
    t = np.arange(int((dur + 1.5) * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) + 0.15 * np.sin(2 * np.pi * 3.01 * f * t) * np.exp(-t * 9)
    return amp * s * np.exp(-t * 2.2) * np.minimum(1, t / 0.004)


def beat(amp):                                                  # lub-dub
    t = np.arange(int(0.35 * SR)) / SR
    th = lambda a: a * np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    s = th(1.0)
    d = int(0.22 * SR)
    s2 = np.zeros(len(s) + d); s2[:len(s)] += s; s2[d:] += th(0.7)
    return amp * s2


def bell(m, amp):
    t = np.arange(int(5 * SR)) / SR
    f = hz(m)
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * dcy) for r, a, dcy in ((0.5, 0.5, 0.6), (1, 1, 0.9), (1.19, 0.4, 1.4), (1.56, 0.35, 1.8), (2.0, 0.3, 2.2), (2.74, 0.2, 3)))
    return amp * s * np.minimum(1, t / 0.003)


CHORDS = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]       # Dm, Bb, Gm, A
MEL = [[(81, 1), (77, 1), (74, 1), (76, .5), (77, .5), (76, 2), (74, 1), (73, 1)],
       [(74, 1), (77, 1), (82, 1), (81, 1), (79, 2), (77, 2)],
       [(79, 1), (82, 1), (86, 1), (85, .5), (82, .5), (81, 3), (None, 1)],
       [(85, 1), (81, 1), (76, 1), (79, 1), (77, 1), (76, 1), (73, 2)]]
for bar in range(0, BARS, 2):
    c = CHORDS[(bar // 2) % 4]
    fade = 1.0 if bar < 24 else (BARS - bar) / 5
    add(pad(c, 8 * BEAT + 1.2, 0.30 * fade), bar * 4 * BEAT)
for bar in range(BARS):
    grow = 0.25 + 0.5 * min(1, bar / 16)
    if bar < 26:
        add(beat(0.55 * grow), bar * 4 * BEAT)
        add(beat(0.40 * grow), (bar * 4 + 2) * BEAT)
    if bar % 4 == 0:
        add(bell(62 if bar % 8 == 0 else 57, 0.22), bar * 4 * BEAT)
for bar in range(8, 26, 2):
    phrase = MEL[(bar // 2) % 4]
    t = bar * 4 * BEAT
    for m, d in phrase:
        if m is not None:
            add(box(m, d * BEAT, 0.20), t)
            if 16 <= bar < 24: add(box(m + 12, d * BEAT, 0.07), t + 0.02)        # the second time round, an octave shimmer
        t += d * BEAT
add(box(74, 4 * BEAT, 0.18), 26 * 4 * BEAT)                                      # one last D
tail = int(3 * SR)
out[-tail:] *= np.linspace(1, 0, tail)
out /= np.abs(out).max() * 1.12
pcm = (out * 32767).astype('<i2')
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'vendor', 'blood_moon.ogg')
tmp = dst + '.wav'
with wave.open(tmp, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ac', '1', '-c:a', 'libvorbis', '-q:a', '4', dst], check=True)
os.remove(tmp)
print(dst, round(N / SR, 1), 's')
