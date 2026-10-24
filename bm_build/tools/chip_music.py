"""2.94k: THE 8-BIT SERPENT KING - the pixel Apophiss's battle theme, as an old cartridge would have played it: two pulse
channels (a lead at 25% duty, chord arpeggios at 12.5%), a triangle bass and a noise channel for the drums. E minor, 160 BPM,
a driving i-VI-VII-V; the theme, its answer, a bridge that climbs into the relative major, and the theme again with a
harmony line a third under it. The boss loop (vendor/boss_pxapo.ogg, 48 s) and the record (vendor/disc_pxapo.ogg: an intro,
the whole of it, a reprise, an ending).
    python3 tools/chip_music.py [loop|disc]"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, fq, lp
from boss_music import save as save_loop
from disc_music import save_mono

BPM = 160


# ---------------------------------------------------------------- the four channels
def pulse(f, dur, duty=0.25, amp=1.0, vib=0.0, decay=0.0):
    t = np.arange(int(dur * SR)) / SR
    fr = fq(f) * (1 + (0.012 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.18) / 0.2, 0, 1) if vib else 0))
    ph = np.cumsum(fr) / SR
    x = np.where((ph % 1.0) < duty, 1.0, -1.0)
    e = np.ones_like(t)
    a = int(0.004 * SR); r = int(0.02 * SR)
    e[:a] = np.linspace(0, 1, a)
    if decay:
        e *= np.exp(-t * decay) * 0.6 + 0.4
    e[-r:] *= np.linspace(1, 0, r)
    return lp(x * e, 7000) * amp


def triangle(f, dur, amp=1.0):
    t = np.arange(int(dur * SR)) / SR
    ph = (fq(f) * t) % 1.0
    q = np.round((1 - 4 * np.abs(ph - 0.5)) * 7.5) / 7.5           # (the 4-bit staircase of the NES triangle)
    r = int(0.01 * SR); q[-r:] *= np.linspace(1, 0, r)
    return q * amp


def noise(dur, amp=1.0, bright=1.0, decay=30.0):
    n = int(dur * SR); t = np.arange(n) / SR
    step = max(1, int(8 / bright))
    x = np.repeat(R.noise((n + step - 1) // step), step)[:n]        # (lo-fi: held samples)
    return x * np.exp(-t * decay) * amp


def kick():
    t = np.arange(int(0.16 * SR)) / SR
    return np.sin(2 * np.pi * np.cumsum(180 * np.exp(-t * 28) + 50) / SR) * np.exp(-t * 18) * 0.9 + noise(0.16, 0.25, 0.4, 40)


def snare():
    return noise(0.18, 0.6, 1.4, 18)


def hat():
    return noise(0.05, 0.22, 4.0, 70)


# ---------------------------------------------------------------- the music
S = 60.0 / BPM
CHORDS = {'Em': ('E', 'G', 'B'), 'C': ('C', 'E', 'G'), 'D': ('D', 'F#', 'A'), 'B': ('B', 'D#', 'F#'), 'Am': ('A', 'C', 'E'), 'G': ('G', 'B', 'D')}
ROOT = {'Em': 'E2', 'C': 'C2', 'D': 'D2', 'B': 'B1', 'Am': 'A1', 'G': 'G2'}
PROG = {'A': ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B'], 'B': ['Am', 'Am', 'Em', 'Em', 'C', 'D', 'B', 'B'],
        'C': ['C', 'C', 'D', 'D', 'Em', 'Em', 'B', 'B'], 'D': ['Em', 'Em', 'C', 'C', 'D', 'D', 'B', 'B']}
# (beat, note, beats) a bar
MEL = {
    'A': [[(0, 'E5', 1), (1, 'G5', .5), (1.5, 'B5', .5), (2, 'A5', 1), (3, 'G5', 1)],
          [(0, 'F#5', .5), (.5, 'G5', .5), (1, 'F#5', 1), (2, 'E5', 1), (3, 'B4', 1)],
          [(0, 'C5', 1), (1, 'E5', .5), (1.5, 'G5', .5), (2, 'E6', 1.5), (3.5, 'D6', .5)],
          [(0, 'C6', 1), (1, 'B5', 1), (2, 'G5', 2)],
          [(0, 'D5', .5), (.5, 'F#5', .5), (1, 'A5', 1), (2, 'D6', 1), (3, 'C6', .5), (3.5, 'B5', .5)],
          [(0, 'A5', 1.5), (1.5, 'G5', .5), (2, 'F#5', 2)],
          [(0, 'B4', .5), (.5, 'D#5', .5), (1, 'F#5', .5), (1.5, 'B5', .5), (2, 'A5', 1), (3, 'F#5', 1)],
          [(0, 'D#5', 1), (1, 'F#5', 1), (2, 'B5', 2)]],
    'B': [[(0, 'A5', .5), (.5, 'A5', .5), (1, 'C6', 1), (2, 'B5', .5), (2.5, 'A5', .5), (3, 'E5', 1)],
          [(0, 'G5', 1), (1, 'A5', 1), (2, 'E5', 2)],
          [(0, 'G5', .5), (.5, 'F#5', .5), (1, 'E5', 1), (2, 'B5', 1), (3, 'G5', 1)],
          [(0, 'E5', 4)],
          [(0, 'E5', .5), (.5, 'G5', .5), (1, 'C6', 1), (2, 'B5', .5), (2.5, 'C6', .5), (3, 'E6', 1)],
          [(0, 'D6', 1), (1, 'C6', .5), (1.5, 'B5', .5), (2, 'A5', 2)],
          [(0, 'F#5', .5), (.5, 'G5', .5), (1, 'A5', .5), (1.5, 'B5', .5), (2, 'C6', 1), (3, 'D#6', 1)],
          [(0, 'F#6', 2), (2, 'B5', 1)]],
    'C': [[(0, 'G5', 1), (1, 'E5', .5), (1.5, 'G5', .5), (2, 'C6', 2)],
          [(0, 'B5', 1), (1, 'A5', 1), (2, 'G5', 2)],
          [(0, 'A5', 1), (1, 'F#5', .5), (1.5, 'A5', .5), (2, 'D6', 2)],
          [(0, 'C6', 1), (1, 'B5', 1), (2, 'A5', 2)],
          [(0, 'B5', .5), (.5, 'C6', .5), (1, 'D6', 1), (2, 'E6', 1), (3, 'D6', .5), (3.5, 'B5', .5)],
          [(0, 'G5', 1), (1, 'B5', 1), (2, 'E6', 2)],
          [(0, 'F#6', 1), (1, 'E6', .5), (1.5, 'D#6', .5), (2, 'E6', 1), (3, 'F#6', 1)],
          [(0, 'B5', 4)]],
}
MEL['D'] = MEL['A']
NAMES = 'CDEFGAB'


def down_third(note, chord):
    """the chord tone under a melody note (the harmony line)"""
    from gv_music import m
    tones = sorted({m(n + str(o)) for n in CHORDS[chord] for o in range(3, 7)})
    x = m(note)
    below = [t for t in tones if x - 6 <= t < x - 1]
    return below[-1] if below else x - 4


def section(tr, bar0, name, lead=True, harm=False, arp=True, drums=True, bass=True, fill=False):
    for i, ch in enumerate(PROG[name]):
        b = bar0 + i
        t0 = tr.at(b)
        if arp:                                                           # (16ths up and down the chord, the second pulse)
            tones = [n + o for o in ('4', '5') for n in CHORDS[ch]]
            seq = tones + tones[-2:0:-1]
            for k in range(16):
                tr.add(pulse(seq[k % len(seq)], S / 4 * 0.9, 0.125, 0.11), t0 + k * S / 4, pan=0.35, wet=0.05)
        if bass:                                                          # (eighths, root and octave - and a walk into the next bar)
            r = ROOT[ch]
            for k in range(8):
                note = r if k % 2 == 0 else r[:-1] + str(int(r[-1]) + 1)
                tr.add(triangle(note, S / 2 * 0.92, 0.42), t0 + k * S / 2, wet=0.0)
        if drums:
            for k in range(4):
                tr.add(kick() if k % 2 == 0 else snare(), t0 + k * S, wet=0.05, gain=0.9)
            for k in range(8):
                tr.add(hat(), t0 + k * S / 2 + (S / 4 if fill and k % 2 else 0), pan=-0.3, wet=0.0)
            if i == len(PROG[name]) - 1:                                  # (a fill into the next part)
                for k in range(4):
                    tr.add(snare(), t0 + 2 * S + k * S / 2, gain=0.7, wet=0.05)
        if lead:
            for beat, note, dur in MEL[name][i]:
                tr.add(pulse(note, dur * S * 0.95, 0.25, 0.32, vib=dur >= 1.5, decay=1.2), t0 + beat * S, pan=-0.12, wet=0.12)
                if harm:
                    tr.add(pulse(down_third(note, ch), dur * S * 0.95, 0.5, 0.16, vib=dur >= 1.5, decay=1.2), t0 + beat * S, pan=0.2, wet=0.12)


def compose(tr, bar0):
    section(tr, bar0, 'A')
    section(tr, bar0 + 8, 'B', fill=True)
    section(tr, bar0 + 16, 'C')
    section(tr, bar0 + 24, 'D', harm=True, fill=True)


def loop():
    tr = Track('pxapo', BPM, 32)
    compose(tr, 0)
    return tr


def disc():
    tr = Track('pxapo', BPM, 64)
    # the intro: the bass alone, then the drums, then the arpeggios - the cartridge powering up
    for k in range(4):                                                    # (4 bars: bass, + drums, + arps)
        ch = ['Em', 'Em', 'C', 'B'][k]
        for j in range(8):
            r = ROOT[ch]
            tr.add(triangle(r if j % 2 == 0 else r[:-1] + str(int(r[-1]) + 1), S / 2 * 0.92, 0.42), tr.at(k) + j * S / 2, wet=0.0)
        if k >= 1:
            for j in range(4):
                tr.add(kick() if j % 2 == 0 else snare(), tr.at(k) + j * S, wet=0.05, gain=0.9)
        if k >= 2:
            tones = [n + '4' for n in CHORDS[ch]] + [n + '5' for n in CHORDS[ch]]
            for j in range(16):
                tr.add(pulse(tones[j % 6], S / 4 * 0.9, 0.125, 0.11), tr.at(k) + j * S / 4, pan=0.35, wet=0.05)
    compose(tr, 4)                                                        # (the whole of it)
    section(tr, 36, 'A', harm=True)                                       # (the reprise, harmonised)
    section(tr, 44, 'B', fill=True)
    section(tr, 52, 'D', harm=True, fill=True)
    # the ending: the last B held - then Em, hit four times and left ringing
    end = 60
    for k, (beat, d) in enumerate(((0, 1), (1, 1), (2, .5), (2.5, .5), (3, 1))):
        for n in ('E5', 'G5', 'B5'):
            tr.add(pulse(n, d * S * 0.9, 0.25, 0.18), tr.at(end) + beat * S, wet=0.15)
        tr.add(triangle('E2', d * S * 0.9, 0.45), tr.at(end) + beat * S, wet=0.0)
        tr.add(kick() if k % 2 == 0 else snare(), tr.at(end) + beat * S, wet=0.05)
    for n, a in (('E4', 0.12), ('B4', 0.12), ('E5', 0.2), ('G5', 0.14), ('B5', 0.12)):
        tr.add(pulse(n, 6 * S, 0.25, a, vib=True, decay=0.5), tr.at(end + 1), wet=0.3)
    tr.add(triangle('E2', 6 * S, 0.45), tr.at(end + 1), wet=0.0)
    tr.add(noise(1.4, 0.4, 0.6, 3), tr.at(end + 1), wet=0.3)
    return tr


if __name__ == '__main__':
    what = sys.argv[1:] or ['loop', 'disc']
    if 'loop' in what:
        save_loop(loop(), 0.6, 6000)
    if 'disc' in what:
        save_mono(disc(), 'pxapo', 0.8)
