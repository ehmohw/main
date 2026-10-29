"""2.99a: synthesises THE DREAD MIRE's sound effects (vendor/mire_<name>.ogg, mono, short) - mire_art.rp ships them as
assets/bm/sounds/mire/<name>.ogg, the sound events bm:mire.<name>:

  bubble  (3.6 s) the dormant puddle: a slow, thick bubbling (bloops rising out of a low wet bed) and, under it, a whisper
  rise    (3.6 s) rising: a long groan in a throat too big for it ('oh' opening to 'ah', the pitch climbing), wet tearing and
          squelching as it pulls up out of the ground, a sub-rumble swelling under it
  idle    (3.0 s) risen, waiting: a slow wet breath in and out (a growl in the out-breath), a clicker's rattle in its throat,
          a chorus of whispers
  lash    (1.2 s) a tentacle whipping out: a rising whoosh, a wet CRACK, a splatter of goo
  shriek  (2.6 s) the cross's light on it: an inhuman shriek - five voices in an 'ee', each with its own wild vibrato,
          ring-modulated, over a roar - climbing, holding, breaking
  death   (3.6 s) dissolving: the groan falling away, a gurgle thinning out, a hiss of something burning off, a last wet plop

Deterministic (seeded); run it to rebuild them (needs numpy, scipy and ffmpeg):   python3 tools/mire_sfx.py [names...]"""
import os, sys, wave, subprocess, tempfile
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(HERE)
VENDOR = os.path.join(BM, 'vendor')
NAMES = ('bubble', 'rise', 'idle', 'lash', 'shriek', 'death')


# ---------------------------------------------------------------------------------------------------- kit
def T(sec): return np.arange(int(sec * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [max(20, lo), min(hi, SR / 2 - 100)], 'bandpass', fs=SR, output='sos'), x)


def lp(x, f, order=2): return sosfilt(butter(order, min(f, SR / 2 - 100), 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'highpass', fs=SR, output='sos'), x)


def sweep_lp(x, f0, f1, steps=24):
    """a low-pass whose cutoff glides f0 -> f1 (blockwise, crossfaded)"""
    n = len(x); out = np.zeros(n); edges = np.linspace(0, n, steps + 1).astype(int)
    for i in range(steps):
        f = f0 * (f1 / f0) ** (i / max(1, steps - 1)); a, b = edges[i], edges[i + 1]
        pad = min(a, 2048); y = lp(x[a - pad:b], f)[pad:]; out[a:b] = y
    return out


def osc(freq, kind='saw', phase0=0.0):
    """an oscillator following a frequency curve (array, Hz)"""
    ph = phase0 + np.cumsum(freq) / SR
    if kind == 'sin': return np.sin(2 * np.pi * ph)
    if kind == 'saw': return 2 * (ph % 1.0) - 1
    if kind == 'sq': return np.sign(np.sin(2 * np.pi * ph))
    raise KeyError(kind)


FORMANT = {'oh': (420, 800, 2400), 'ah': (720, 1150, 2500), 'ee': (300, 2300, 3100), 'uh': (520, 1000, 2400), 'oo': (320, 760, 2300)}


def voice(src, vowel, q=6.0):
    """a source through three formant resonances"""
    F = FORMANT[vowel] if isinstance(vowel, str) else vowel
    return sum(bp(src, f * (1 - 1 / q), f * (1 + 1 / q)) * g for f, g in zip(F, (1.0, 0.6, 0.25)))


def morph(src, v0, v1, steps=12):
    """formants gliding from one vowel to another"""
    n = len(src); out = np.zeros(n); edges = np.linspace(0, n, steps + 1).astype(int)
    for i in range(steps):
        t = i / max(1, steps - 1); F = tuple(a + (b - a) * t for a, b in zip(FORMANT[v0], FORMANT[v1]))
        a, b = edges[i], edges[i + 1]; pad = min(a, 4096)
        out[a:b] = voice(src[a - pad:b], F)[pad:]
    return out


def env(n, a, r, hold=None):
    """attack a s, release r s (exponential-ish), the rest held"""
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na) ** 1.6
    if nr: e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e


def place(out, x, at, g=1.0):
    i = int(at * SR); j = min(len(out), i + len(x))
    if i < len(out): out[i:j] += g * x[:j - i]


def bloop(rnd, f0=None, dur=None, low=False):
    """a bubble: a sine chirping up as it bursts, decaying fast; a soft plop under the bigger ones"""
    f0 = f0 or rnd.uniform(110, 260) if low else f0 or rnd.uniform(160, 460); dur = dur or rnd.uniform(0.05, 0.11)
    t = T(dur); f = f0 * (1 + 1.6 * (t / dur) ** 1.4)
    y = osc(f, 'sin') * np.exp(-t / (dur * 0.35)) * np.minimum(1, t / 0.004)
    return y


def whisper(rnd, sec, syl=(0.09, 0.2), level=1.0):
    """breathy unvoiced speech: noise in the fricative and vowel bands, shaped into syllables"""
    n = int(sec * SR); e = np.zeros(n); t = 0.05
    while t < sec - 0.1:
        d = rnd.uniform(*syl); a = int(t * SR); b = min(n, a + int(d * SR))
        e[a:b] = np.sin(np.linspace(0, np.pi, b - a)) ** 1.5 * rnd.uniform(0.5, 1.0)
        t += d + rnd.uniform(0.02, 0.12)
    src = rnd.standard_normal(n)
    v = rnd.choice(list(FORMANT))
    e = lp(e, 30)
    y = 0.6 * voice(src, v, 4.0) + 0.5 * bp(src, 3500, 7500) * np.clip(e - 0.4, 0, 1) * 1.6     # (the 's' only at a syllable's height)
    return y * e * level


def clicks(rnd, n_clicks, gap=(0.022, 0.045)):
    """a clicker's rattle: tiny bright clicks in a quick series"""
    out = np.zeros(int((n_clicks * gap[1] + 0.05) * SR)); t = 0.0
    for _ in range(n_clicks):
        c = rnd.standard_normal(int(0.004 * SR)) * np.exp(-np.arange(int(0.004 * SR)) / (0.0008 * SR))
        place(out, bp(c, 1800, 5200), t, rnd.uniform(0.6, 1.0)); t += rnd.uniform(*gap)
    return out


def room(x, sec=0.6, mix=0.25, bright=4000, seed=1):
    """a cave around it: a short decaying-noise reverb"""
    r = np.random.default_rng(seed); t = T(sec)
    ir = lp(r.standard_normal(len(t)), bright) * np.exp(-t * 6.9 / sec)
    wet = fftconvolve(x, ir)[:len(x)]; wet *= np.abs(x).max() / (np.abs(wet).max() + 1e-9)
    return x * (1 - mix) + wet * mix


def finish(x, fade=0.04, level=0.9, drive=1.4):
    x = np.tanh(x / (np.abs(x).max() + 1e-9) * drive) / np.tanh(drive)
    nf = int(fade * SR); x[-nf:] *= np.linspace(1, 0, nf); x[:64] *= np.linspace(0, 1, 64)
    return (x / (np.abs(x).max() + 1e-9) * level).astype(np.float32)


# ---------------------------------------------------------------------------------------------------- the sounds
def s_bubble():
    rnd = np.random.default_rng(461); sec = 3.6; n = int(sec * SR); out = np.zeros(n)
    bed = lp(rnd.standard_normal(n), 260, 4) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.7 * T(sec)) ** 2)
    out += bed * 0.5
    t = 0.12
    while t < sec - 0.2:                                    # (slow, thick: in clusters)
        for k in range(rnd.integers(1, 4)):
            place(out, bloop(rnd, low=rnd.random() < 0.5), t + k * rnd.uniform(0.04, 0.09), rnd.uniform(0.35, 0.9))
        t += rnd.uniform(0.28, 0.62)
    w = whisper(rnd, 2.4, level=0.55); place(out, hp(w, 600), 0.7)
    return finish(room(out, 0.7, 0.3), level=0.85, drive=1.2)


def s_rise():
    rnd = np.random.default_rng(462); sec = 3.6; t = T(sec); n = len(t); out = np.zeros(n)
    f = 46 + 26 * (t / sec) ** 1.3 + 3 * np.sin(2 * np.pi * 5.2 * t) + 1.5 * lp(rnd.standard_normal(n), 8) * 40
    src = osc(f, 'saw') + 0.6 * osc(f * 1.505, 'saw') + 0.3 * rnd.standard_normal(n) * 0.2
    groan = morph(src, 'oh', 'ah') * env(n, 0.9, 0.5) * (0.6 + 0.4 * t / sec)
    out += groan * 1.0
    out += np.sin(2 * np.pi * np.cumsum(30 + 12 * t / sec) / SR) * env(n, 1.6, 0.6) * 0.5           # (the sub, swelling)
    tt = 0.15                                                                                    # (tearing: crackle bursts, denser as it comes up)
    while tt < sec - 0.3:
        m = int(rnd.uniform(0.02, 0.07) * SR); c = rnd.standard_normal(m) * (rnd.random(m) < 0.08)
        place(out, bp(c, 700, 3800) * np.exp(-np.arange(m) / (0.3 * m)), tt, rnd.uniform(1.0, 2.2))
        tt += rnd.uniform(0.02, 0.16) * (1.2 - 0.7 * tt / sec)
    for at in (0.4, 1.1, 1.7, 2.3, 2.8, 3.1):                                                    # (squelches)
        m = int(0.22 * SR); sq = sweep_lp(rnd.standard_normal(m), 2400, 260, 10) * np.sin(np.linspace(0, np.pi, m)) ** 2
        place(out, sq, at + rnd.uniform(-0.05, 0.05), 0.9)
    return finish(room(out, 0.9, 0.3), drive=1.8)


def s_idle():
    rnd = np.random.default_rng(463); sec = 3.0; t = T(sec); n = len(t); out = np.zeros(n)
    nin, nout = int(1.0 * SR), int(1.4 * SR)
    inh = bp(rnd.standard_normal(nin), 350, 1600) * np.sin(np.linspace(0, np.pi, nin)) ** 1.2
    place(out, inh, 0.05, 0.8)
    exn = rnd.standard_normal(nout); tt = T(1.4)
    growl = voice(osc(58 + 4 * np.sin(2 * np.pi * 3 * tt), 'saw') * (1 + 0.6 * (rnd.random(nout) - 0.5)), 'uh')
    ex = (bp(exn, 200, 1100) * 0.8 + growl * 0.9) * np.sin(np.linspace(0, np.pi, nout)) ** 0.9
    place(out, ex, 1.2, 1.0)
    place(out, clicks(rnd, 7), 0.75, 0.55); place(out, clicks(rnd, 5, (0.03, 0.05)), 2.45, 0.45)
    for k, at in enumerate((0.2, 0.9, 1.6)):                                                     # (the chorus of whispers)
        place(out, hp(whisper(np.random.default_rng(470 + k), 1.3, level=0.5), 700), at)
    return finish(room(out, 0.8, 0.3), level=0.85, drive=1.3)


def s_lash():
    rnd = np.random.default_rng(464); sec = 1.2; n = int(sec * SR); out = np.zeros(n)
    wl = int(0.3 * SR); w = rnd.standard_normal(wl); edges = np.linspace(0, wl, 13).astype(int); wo = np.zeros(wl)
    for i in range(12):                                                                          # (the whoosh: a band sweeping up)
        c = 350 * (8.0 ** (i / 11)); a, b = edges[i], edges[i + 1]; pad = min(a, 2048)
        wo[a:b] = bp(w[a - pad:b], c * 0.7, c * 1.4)[pad:]
    place(out, wo * np.linspace(0, 1, wl) ** 1.5, 0.0, 1.8)
    m = int(0.012 * SR); crack = hp(rnd.standard_normal(m), 1500) * np.exp(-np.arange(m) / (0.0025 * SR))    # (the crack)
    place(out, crack, 0.29, 1.3)
    tt = T(0.09); place(out, np.sin(2 * np.pi * (95 - 40 * tt / 0.09) * tt) * np.exp(-tt / 0.03), 0.29, 1.2)     # (its thump)
    tt0 = 0.31                                                                                   # (the splatter)
    for _ in range(14):
        m = int(rnd.uniform(0.012, 0.04) * SR); s = lp(rnd.standard_normal(m), rnd.uniform(900, 2200)) * np.exp(-np.arange(m) / (0.25 * m))
        place(out, s, tt0, rnd.uniform(0.3, 0.9) * (1 - (tt0 - 0.31) / 0.7)); tt0 += rnd.uniform(0.01, 0.05)
    return finish(room(out, 0.5, 0.22), drive=2.4)


def s_shriek():
    rnd = np.random.default_rng(465); sec = 2.6; t = T(sec); n = len(t); out = np.zeros(n)
    rise = np.minimum(1, t / 0.35) ** 0.6; fall = 1 - 0.35 * np.clip((t - 1.9) / 0.7, 0, 1) ** 1.5
    for k, (f0, vr, vd) in enumerate(((520, 9.0, 0.03), (615, 11.5, 0.035), (790, 7.2, 0.025), (1040, 13.0, 0.04), (1330, 10.2, 0.03))):
        jit = lp(rnd.standard_normal(n), 6) * 18
        f = f0 * (0.72 + 0.28 * rise) * fall * (1 + vd * np.sin(2 * np.pi * vr * t + k)) * (1 + jit * 0.01)
        v = voice(osc(f, 'saw', k * 0.17), 'ee', 5.0)
        out += v * (0.9 - 0.12 * k) * env(n, 0.06 + 0.03 * k, 0.5)
    out *= 0.6 + 0.4 * np.sin(2 * np.pi * 71 * t)                                                 # (ring-modulated: inhuman)
    roar = morph(osc(78 * (0.9 + 0.1 * rise) * fall, 'saw') + 0.3 * rnd.standard_normal(n), 'ah', 'oh')
    out += roar * 0.9 * env(n, 0.1, 0.6)
    out += bp(rnd.standard_normal(n), 3000, 9000) * 0.12 * env(n, 0.05, 0.8)                    # (breath in it)
    return finish(room(out, 0.9, 0.28), drive=1.6)


def s_death():
    rnd = np.random.default_rng(466); sec = 3.6; t = T(sec); n = len(t); out = np.zeros(n)
    f = 74 * (1 - 0.6 * (t / sec) ** 0.8) + 2 * np.sin(2 * np.pi * 4 * t)
    g = morph(osc(f, 'saw') + 0.4 * osc(f * 1.49, 'saw'), 'ah', 'oo') * np.exp(-t / 1.4) * env(n, 0.05, 0.4)
    out += g * 1.1
    tt = 0.05                                                                                    # (the gurgle, thinning)
    while tt < sec - 0.5:
        place(out, bloop(rnd, low=True), tt, rnd.uniform(0.4, 1.0) * np.exp(-tt / 1.6))
        tt += rnd.uniform(0.03, 0.09) + 0.1 * tt / sec
    hs = hp(rnd.standard_normal(n), 2500) * (rnd.random(n) < 0.35)                              # (the hiss: burning off, dulling)
    out += sweep_lp(hs, 9000, 1200, 16) * 0.12 * env(n, 0.3, 1.2) * np.exp(-t / 2.2)
    m = int(0.25 * SR); place(out, sweep_lp(rnd.standard_normal(m), 1600, 180, 8) * np.sin(np.linspace(0, np.pi, m)) ** 2, 3.0, 1.2)   # (a last plop)
    return finish(room(out, 1.0, 0.3), drive=1.5)


SFX = {'bubble': s_bubble, 'rise': s_rise, 'idle': s_idle, 'lash': s_lash, 'shriek': s_shriek, 'death': s_death}


# ---------------------------------------------------------------------------------------------------- saving
def encode(x, out, q=3):
    fd, wav = tempfile.mkstemp(suffix='.wav'); os.close(fd)
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-c:a', 'libvorbis', '-q:a', str(q), out], check=True)
    os.remove(wav)


if __name__ == '__main__':
    want = [a for a in sys.argv[1:] if a in SFX] or list(NAMES)
    for nm in want:
        x = SFX[nm](); p = os.path.join(VENDOR, f'mire_{nm}.ogg'); encode(x, p)
        rms = float(np.sqrt((x ** 2).mean()))
        print(f'{p}: {len(x) / SR:.1f} s, peak {20 * np.log10(np.abs(x).max()):.1f} dBFS, rms {20 * np.log10(rms):.1f} dBFS, {os.path.getsize(p) // 1024} KB')
