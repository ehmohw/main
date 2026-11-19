"""Extra voices for the full-length themes: an electric cello, a clean solo violin, a music box."""
import numpy as np
from gv_music import SR, R, T, env, lp, hp, bp
from armada_music import osc, smooth, addc
from full_common import midi


def _bowed(notes, beat, amp, port, vib, depth, drive, legato, bands, bright, rasp=0.18):
    total = sum(d for _, d in notes) * beat
    n = int((total + 0.4) * SR)
    tgt = np.zeros(n); gate = np.zeros(n); onset = np.zeros(n); accent = np.zeros(n)
    first = next((midi(x) for x, _ in notes if x is not None), 50)
    tgt[:] = first
    t = 0.0
    for x, d in notes:
        i0, i1 = int(t * SR), int((t + d * beat) * SR)
        if x is not None:
            tgt[i0:] = midi(x)
            gate[i0:int((t + d * beat * legato) * SR)] = 1.0
            onset[i0:i1] = np.arange(i1 - i0) / SR
            a = min(i0 + int(0.05 * SR), n); accent[i0:a] = np.linspace(1, 0, a - i0)
        t += d * beat
    m = smooth(tgt, port)
    tt = np.arange(n) / SR
    vb = depth * np.clip((onset - 0.18) / 0.35, 0, 1) * np.sin(2 * np.pi * vib * tt)
    fr = 440.0 * 2 ** ((m - 69) / 12) * (1 + vb)
    s = osc(fr) * 0.65 + osc(fr * 1.002) * 0.35
    s = s + bp(R.noise(n), 1800, 6000) * (rasp + 0.4 * accent)
    body = sum(bp(s, a, b, 1) * g for a, b, g in bands)
    y = np.tanh(body * drive) / np.tanh(drive)
    y = lp(y, bright)
    return amp * y * smooth(gate, 0.02)


def cello_line(notes, beat, amp=0.25, port=0.05, vib=5.2, depth=0.009, drive=1.6, legato=0.97):
    """an electric cello: the violin's build an octave and a half down - lower body resonances, a darker top, a slower vibrato"""
    bands = ((90, 140, 1.0), (180, 260, 1.2), (330, 480, 1.0), (800, 1200, 0.6), (1900, 2800, 0.45))
    return _bowed(notes, beat, amp, port, vib, depth, drive, legato, bands, 4200, 0.12)


def cello(tr, t0, notes, amp=0.25, pan=-0.25, wet=0.4, **k):
    s = cello_line(notes, tr.beat, amp, **k)
    addc(tr, s, t0, pan, 1, wet)


def clean_violin_line(notes, beat, amp=0.2, port=0.05, vib=5.6, depth=0.008, legato=0.97):
    """an acoustic-sounding violin: the same bowing, no amp"""
    bands = ((260, 340, 1.1), (430, 560, 1.0), (900, 1300, 0.7), (2600, 3600, 0.7), (4500, 6000, 0.25))
    return _bowed(notes, beat, amp, port, vib, depth, 0.8, legato, bands, 5500, 0.1)


def musicbox(x, dur=2.5, amp=1.0):
    """a music-box tine: a pure tone with a bright, quick, slightly inharmonic ping"""
    t = T(max(dur, 1.2)); f = 440.0 * 2 ** ((midi(x) - 69) / 12)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.6) + 0.35 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 7)
         + 0.12 * np.sin(2 * np.pi * f * 5.43 * t) * np.exp(-t * 14))
    return amp * s * env(len(t), 0.001, 0, 1, 0.15)
