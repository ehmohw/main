"""2.75: synthesises five more music discs (vendor/disc_*.ogg) with gv_music's instruments - mono, so a jukebox plays them
where it stands, each with a proper ending (the last bars are silence, so no tail wraps round to the start).
  big_score   THE BIG SCORE (a rare heist find) - a caper in C minor: walking bass, brushes, vibes, a sly muted lead, horns
  invasion    INVASION (invasion nights) - E phrygian: a theremin over pulsing arpeggios, a sub that throbs, ray-gun zaps
  lucky       LUCKY NIGHT (lucky nights) - a G-major jig: harp, a tin whistle, a fiddle, a bodhran
  market      THE BLACK MARKET (the market) - a slow noir swing in F minor: upright bass, brushes, smoky keys, a muted horn
  hollow      THE HOLLOW (found in the Hollow) - D minor, almost still: a choir, a drone, far bells, a falling motif, wind
Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg - only to rebuild, never to build the packs).
    python3 tools/disc_music.py [name ...]"""
import os, sys, wave, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gv_music as G
from gv_music import (Track, mix, T, env, lp, hp, bp, pluck, ep, bell, bass, sub, pad, organ, brass, choir, lead, strings, kick, snare,
                      brush, hat, tom, shaker, chord, hz, m, SR)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')


def save_mono(tr, name, room=1.8, bright=5000):
    st = tr.render(room, bright)
    mono = (st[0] + st[1]) * 0.5
    k = int(1.5 * SR); mono[:k] *= np.linspace(0, 1, k) ** 0.5          # (a soft start; the ending is written into the music)
    mono = mono / (np.abs(mono).max() + 1e-9) * 0.9
    wav = os.path.join('/tmp', f'disc_{name}.wav')
    with wave.open(wav, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mono * 32767).astype('<i2').tobytes())
    out = os.path.join(OUT, f'disc_{name}.ogg')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-ac', '1', '-c:a', 'libvorbis', '-q:a', '3', out], check=True)
    os.remove(wav)
    print(f'{out}: {tr.seconds:.0f} s, {os.path.getsize(out) // 1024} KB')


def glide(f0, f1, dur, amp=1.0, vib=6.0, depth=0.012):
    """a theremin note sliding from f0 to f1: a sine with a wide vibrato and a little breath"""
    t = T(dur)
    f = f0 * (f1 / f0) ** np.clip(t / min(0.18, dur), 0, 1)
    ph = 2 * np.pi * np.cumsum(f * (1 + depth * np.sin(2 * np.pi * vib * t))) / SR
    s = np.sin(ph) + 0.12 * np.sin(2 * ph)
    return amp * s * env(len(t), 0.06, 0.1, 0.9, 0.18)


def whistle(f, dur, amp=1.0):
    t = T(dur)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.25, 0, 1))) / SR
    breath = bp(G.R.noise(len(t)), f * 0.9, f * 1.3) * 0.08
    return amp * (np.sin(ph) + 0.05 * np.sin(2 * ph) + breath) * env(len(t), 0.02, 0.05, 0.85, 0.05)


def zap(amp=1.0):
    t = T(0.45)
    f = 1800 * np.exp(-t * 7) + 120
    return amp * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)


def crackle(dur, amp=1.0):
    n = int(dur * SR); x = np.zeros(n)
    idx = G.R.choice(n, size=int(dur * 9), replace=False) if hasattr(G.R, 'choice') else np.random.default_rng(7).choice(n, size=int(dur * 9), replace=False)
    x[idx] = np.random.default_rng(11).uniform(-1, 1, len(idx))
    return amp * hp(x, 1500)


def wind(dur, amp=1.0):
    t = T(dur)
    nz = G.R.noise(len(t))
    sweep = 500 + 350 * np.sin(2 * np.pi * 0.07 * t)
    out = lp(nz, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * t))
    return amp * hp(out, 120) * np.minimum(1, t / 3) * np.minimum(1, (dur - t) / 3)


# ------------------------------------------------------------------ THE BIG SCORE: a caper (rare heist find)
def big_score():
    tr = Track('big_score', 120, 50)
    prog = [('C3', 'm7'), ('F3', '7'), ('C3', 'm7'), ('G2', '7'), ('Ab2', 'M7'), ('G2', '7'), ('C3', 'm7'), ('G2', '7')]
    sw = 2 / 3
    END = 46                                                      # (bars 46-49: the last hit rings out, then silence)
    for bar in range(END):
        root, kind = prog[bar % 8]
        ch = chord(root, kind)
        nxt = m(prog[(bar + 1) % 8][0])
        walk = [ch[0] - 12, ch[1 + bar % 2] - 12, ch[2] - 12, nxt - 12 + (1 if bar % 2 else -1)]
        for b, x in enumerate(walk):
            tr.add(mix(pluck(hz(x), tr.beat * 0.95, 0.3, 0.993) * 0.9, bass(x, tr.beat * 0.9, 0.5, 650, 2.0)), tr.at(bar, b), 0, 0.95, 0.15)
        for b in (1, 3): tr.add(brush(0.55), tr.at(bar, b), 0, 1, 0.35)
        for b in (0, 1, 1 + sw, 2, 3, 3 + sw): tr.add(hat(0.17 if b % 1 else 0.24), tr.at(bar, b), 0, 1, 0.2)
        if bar >= 4:
            for b in (0, 1 + sw):
                for x in ch[1:] + [ch[0] + 12]:
                    tr.add(ep(hz(x + 12), 0.8, 0.13), tr.at(bar, b), 0, 1, 0.45)
    A = [(0, 'G4', .5), (sw, 'C5', .3), (1, 'Eb5', .5), (2, 'D5', .4), (2 + sw, 'C5', .3), (3, 'Bb4', .6), (4, 'C5', .4), (4 + sw, 'Eb5', .3),
         (5, 'G5', .7), (6, 'F5', .4), (6 + sw, 'Eb5', .3), (7, 'D5', .9)]
    A2 = [(0, 'G5', .4), (sw, 'G5', .3), (1, 'F5', .4), (1 + sw, 'Eb5', .3), (2, 'F5', .6), (3, 'D5', .3), (3 + sw, 'Bb4', .3),
          (4, 'C5', .6), (5, 'Eb5', .4), (5 + sw, 'D5', .3), (6, 'C5', .5), (7, 'G4', .9)]
    B = [(0, 'Ab5', .9), (1, 'G5', .4), (1 + sw, 'F5', .3), (2, 'Eb5', .9), (3, 'D5', .9), (4, 'Eb5', .4), (4 + sw, 'F5', .3), (5, 'G5', .9),
         (6, 'B4', .5), (6 + sw, 'D5', .3), (7, 'G5', .9)]
    for ph, mo in ((6, A), (10, A2), (14, B), (18, A2), (30, A), (34, A2), (38, B), (42, A)):
        for b, x, d in mo:
            tr.add(lead(x, d, 0.30, 1500, 5, 0.3), tr.at(ph, 0) + b * tr.beat, 0, 1, 0.35)
    for bar in range(14, 22, 1):                                  # horns
        for b in (0, 2 + sw):
            tr.add(brass([x + 12 for x in chord(prog[bar % 8][0], prog[bar % 8][1])[:3]], 0.25, 0.32, 2200, 0.01), tr.at(bar, b), 0, 1, 0.3)
    for bar in range(22, 30):                                     # the vibes take a solo
        x0 = chord(prog[bar % 8][0], prog[bar % 8][1])
        for k, b in enumerate((0, 0.5, 1 + sw, 2, 2.5, 3 + sw)):
            tr.add(ep(hz(x0[(k + bar) % len(x0)] + 24), 0.5, 0.2), tr.at(bar, b), 0, 1, 0.4)
    hit = chord('C3', 'm7')
    tr.add(brass([x + 12 for x in hit], 2.5, 0.5, 2600, 0.01), tr.at(END, 0), 0, 1, 0.5)
    tr.add(bass(m('C2'), 2.5, 0.8, 500, 1.0), tr.at(END, 0), 0, 1, 0.2)
    tr.add(kick(0.7, 6), tr.at(END, 0), 0, 1, 0.1)
    return tr


# ------------------------------------------------------------------ INVASION: E phrygian, a theremin over the arps (invasion nights)
def invasion():
    tr = Track('invasion', 100, 40)
    prog = [('E3', 'm'), ('F3', 'M'), ('E3', 'm'), ('D3', 'm')]
    END = 37
    for bar in range(END):
        root, kind = prog[(bar // 2) % 4]
        ch = chord(root, kind)
        if bar % 2 == 0:
            tr.add(pad([x + 12 for x in ch], 2 * 4 * tr.beat + 0.5, 0.18, 1200, 1.2, 1.2), tr.at(bar, 0), 0, 1, 0.5)
        if bar >= 2:                                               # the arpeggio, sixteenths
            seq = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2] + 12, ch[1] + 12, ch[2], ch[1]]
            for k in range(16):
                x = seq[k % 8] + 12
                tr.add(G.square(hz(x), T(tr.beat / 4 * 0.9)) * env(int(tr.beat / 4 * 0.9 * SR), 0.003, 0.05, 0.4, 0.03) * 0.07, tr.at(bar, k / 4), 0, 1, 0.3)
        if bar >= 4:
            for k in range(8):                                     # the sub throbs in eighths
                tr.add(sub(hz(ch[0] - 12), tr.beat / 2 * 0.8, 0.45), tr.at(bar, k / 2), 0, 1, 0.05)
            tr.add(kick(0.5, 9), tr.at(bar, 0), 0, 1, 0.05); tr.add(kick(0.4, 9), tr.at(bar, 2), 0, 1, 0.05)
            if bar >= 12: tr.add(snare(0.35, 220), tr.at(bar, 3), 0, 1, 0.3)
        if bar in (7, 15, 23, 31): tr.add(zap(0.35), tr.at(bar, 3.5), 0, 1, 0.5)
    mel = [('B4', 'B4', 2), ('B4', 'C5', 1), ('C5', 'E5', 1), ('E5', 'D5', 2), ('D5', 'C5', 1), ('C5', 'B4', 1),
           ('B4', 'G4', 2), ('G4', 'A4', 1), ('A4', 'B4', 3), ('B4', 'F5', 2), ('F5', 'E5', 2), ('E5', 'C5', 2), ('C5', 'B4', 2)]
    for start in (8, 24):
        t = tr.at(start, 0)
        for f0, f1, d in mel:
            tr.add(glide(hz(m(f0)), hz(m(f1)), d * tr.beat * 0.98, 0.28), t, 0, 1, 0.55)
            t += d * tr.beat
    t = tr.at(END, 0)
    tr.add(glide(hz(m('E5')), hz(m('E4')), 6 * tr.beat, 0.25, 4, 0.02), t, 0, 1, 0.7)        # one last fall
    tr.add(pad([m('E3'), m('B3'), m('E4')], 6 * tr.beat, 0.15, 900, 0.5, 3.0), t, 0, 1, 0.6)
    return tr


# ------------------------------------------------------------------ LUCKY NIGHT: a jig in G (lucky nights)
def lucky():
    tr = Track('lucky', 240, 64, beats=6)                          # (6/8: a beat is an eighth)
    prog = [('G3', 'M'), ('C3', 'M'), ('G3', 'M'), ('D3', 'M'), ('G3', 'M'), ('C3', 'M'), ('D3', 'M'), ('G3', 'M')]
    END = 60
    for bar in range(END):
        root, kind = prog[bar % 8]
        ch = chord(root, kind)
        for k, x in enumerate([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1]]):          # the harp
            tr.add(pluck(hz(x + 12), tr.beat * 1.6, 0.55, 0.995) * 0.35, tr.at(bar, k), 0, 1, 0.35)
        tr.add(bass(ch[0] - 12, tr.beat * 2.5, 0.45, 700, 2.5), tr.at(bar, 0), 0, 1, 0.15)
        tr.add(bass(ch[2] - 12, tr.beat * 2.5, 0.35, 700, 2.5), tr.at(bar, 3), 0, 1, 0.15)
        if bar >= 4:                                               # the bodhran
            tr.add(tom(85, 0.5, 9, 0.2), tr.at(bar, 0), 0, 1, 0.2); tr.add(tom(110, 0.25, 12, 0.1), tr.at(bar, 2), 0, 1, 0.2)
            tr.add(tom(95, 0.35, 10, 0.15), tr.at(bar, 3), 0, 1, 0.2); tr.add(tom(110, 0.2, 12, 0.1), tr.at(bar, 5), 0, 1, 0.2)
    J = ['D5', 'G5', 'G5', 'B5', 'A5', 'G5', 'E5', 'C6', 'C6', 'B5', 'A5', 'G5', 'D5', 'G5', 'G5', 'B5', 'A5', 'B5', 'A5', 'F#5', 'D5', 'E5', 'F#5', 'A5',
         'D5', 'G5', 'G5', 'B5', 'A5', 'G5', 'E5', 'C6', 'C6', 'B5', 'A5', 'G5', 'B5', 'A5', 'G5', 'A5', 'F#5', 'D5', 'G5', 'D5', 'B4', 'G4', 'G4', 'G4']
    K = ['B5', 'D6', 'D6', 'B5', 'G5', 'B5', 'C6', 'E6', 'E6', 'C6', 'A5', 'C6', 'B5', 'D6', 'D6', 'B5', 'G5', 'B5', 'A5', 'F#5', 'D5', 'D5', 'E5', 'F#5',
         'G5', 'B5', 'D6', 'B5', 'G5', 'B5', 'C6', 'A5', 'F#5', 'D5', 'E5', 'F#5', 'G5', 'F#5', 'G5', 'A5', 'F#5', 'D5', 'G5', 'D5', 'B4', 'G4', 'G4', 'G4']
    for ph, tune, inst in ((8, J, 'w'), (16, K, 'w'), (24, J, 'f'), (32, K, 'f'), (40, J, 'w'), (48, K, 'w'), (52, J, 'f')):
        if ph + 8 > END: tune = tune[:max(0, (END - ph) * 6)]
        for k, x in enumerate(tune):
            t = tr.at(ph, 0) + k * tr.beat
            if inst == 'w': tr.add(whistle(hz(m(x) + 12), tr.beat * 0.95, 0.22), t, 0, 1, 0.3)
            else: tr.add(strings(hz(m(x)), tr.beat * 1.05, 0.25, 2600), t, 0, 1, 0.3)
    t = tr.at(END, 0)
    for k, x in enumerate(['G4', 'B4', 'D5', 'G5']):
        tr.add(pluck(hz(m(x)), 3.0, 0.55, 0.997) * 0.5, t + k * 0.06, 0, 1, 0.5)
    tr.add(whistle(hz(m('G6')), 2.0, 0.2), t, 0, 1, 0.5)
    tr.add(tom(85, 0.6, 7, 0.3), t, 0, 1, 0.3)
    return tr


# ------------------------------------------------------------------ THE BLACK MARKET: a slow noir swing in F minor (the market)
def market():
    tr = Track('market', 84, 35)
    prog = [('F3', 'm7'), ('Db3', 'M7'), ('Bb2', 'm7'), ('C3', '7')]
    sw = 2 / 3
    END = 32
    tr.add(crackle(tr.seconds - 2, 0.05), 0.5, 0, 1, 0.0)
    for bar in range(END):
        root, kind = prog[bar % 4]
        ch = chord(root, kind)
        nxt = m(prog[(bar + 1) % 4][0])
        walk = [ch[0] - 12, ch[2] - 12, ch[1] - 12 + 12 * (bar % 2 == 0) - 12 * (bar % 2 == 0), nxt - 12 + 1]
        for b, x in enumerate(walk):
            tr.add(mix(pluck(hz(x), tr.beat * 0.95, 0.2, 0.992), bass(x, tr.beat * 0.9, 0.45, 500, 2.0)), tr.at(bar, b), 0, 0.95, 0.15)
        for b in (1, 3): tr.add(brush(0.5), tr.at(bar, b), 0, 1, 0.35)
        for b in (0, 1 + sw, 2, 3 + sw): tr.add(hat(0.12), tr.at(bar, b), 0, 1, 0.25)
        for b in (0, 2 + sw):
            for x in ch: tr.add(ep(hz(x + 12), 1.1, 0.13, 3.0), tr.at(bar, b), 0, 1, 0.5)
    A = [(0, 'C5', 1.4), (1.5, 'Ab4', .4), (2, 'G4', .6), (3, 'F4', .9), (4, 'Ab4', .5), (4 + sw, 'C5', .3), (5, 'Eb5', 1.4), (6.5, 'Db5', .4), (7, 'C5', 1.0)]
    A2 = [(0, 'Bb4', 1.0), (1, 'Db5', .5), (1 + sw, 'F5', .3), (2, 'Eb5', 1.2), (3 + sw, 'Db5', .3), (4, 'C5', .9), (5, 'Bb4', .5), (5 + sw, 'G4', .3),
          (6, 'E4', .9), (7, 'F4', 1.0)]
    for ph, mo in ((4, A), (8, A2), (12, A), (16, A2), (24, A), (28, A2)):
        for b, x, d in mo:
            tr.add(lead(x, d * tr.beat, 0.30, 1100, 4.5, 0.42), tr.at(ph, 0) + b * tr.beat, 0, 1, 0.4)
    for bar in range(18, 24):                                     # the keys take a chorus
        x0 = chord(prog[bar % 4][0], prog[bar % 4][1])
        for k, b in enumerate((0, 1, 1 + sw, 2.5, 3)):
            tr.add(ep(hz(x0[(k * 2 + bar) % len(x0)] + 24), 0.7, 0.18, 3.0), tr.at(bar, b), 0, 1, 0.45)
    t = tr.at(END, 0)
    for x in chord('F3', 'm7') + [m('G4')]: tr.add(ep(hz(x + 12), 4.0, 0.16, 2.5), t, 0, 1, 0.6)
    tr.add(bass(m('F2'), 3.0, 0.6, 500, 1.2), t, 0, 1, 0.2)
    tr.add(lead('C5', 2.5, 0.25, 1000, 4, 0.42), t + 0.3, 0, 1, 0.5)
    return tr


# ------------------------------------------------------------------ THE HOLLOW: almost still (found in the Hollow)
def hollow():
    tr = Track('hollow', 60, 26)
    prog = [[m('D3'), m('A3'), m('F4')], [m('Bb2'), m('F3'), m('D4')], [m('G2'), m('D3'), m('Bb3')], [m('A2'), m('E3'), m('C#4')]]
    END = 23
    tr.add(wind(tr.seconds - 1, 0.18), 0.2, 0, 1, 0.3)
    for bar in range(0, END, 2):
        ch = prog[(bar // 2) % 4]
        tr.add(choir(ch, 2 * 4 * tr.beat + 1.5, 0.30, 1.6), tr.at(bar, 0), 0, 1, 0.65)
        tr.add(sub(hz(ch[0] - 12), 2 * 4 * tr.beat, 0.25), tr.at(bar, 0), 0, 1, 0.2)
    for bar in range(END):
        if bar % 2 == 0 and bar >= 2: tr.add(tom(55, 0.35, 5, 0.4), tr.at(bar, 0), 0, 1, 0.5)
        if bar % 4 == 0: tr.add(bell(hz(m('D5') if bar % 8 == 0 else m('A4')), 6.0, 0.20, 3.5, 1.2, 2.5), tr.at(bar, 0), 0, 1, 0.7)
    fall = [('A5', 1), ('F5', 1), ('E5', 1), ('D5', 3), ('C#5', 1), ('D5', 1), ('E5', 1), ('A4', 3), ('Bb4', 1), ('A4', 1), ('G4', 1), ('F4', 2), ('E4', 1), ('D4', 4)]
    for start in (6, 14):
        t = tr.at(start, 0)
        for x, d in fall:
            tr.add(pluck(hz(m(x)), d * tr.beat + 1.2, 0.35, 0.998) * 0.32, t, 0, 1, 0.7)
            if start == 14: tr.add(bell(hz(m(x) + 12), 2.5, 0.05, 3.5, 1.5, 1.5), t, 0, 1, 0.8)
            t += d * tr.beat
    t = tr.at(END, 0)
    tr.add(choir([m('D3'), m('A3'), m('D4')], 9.0, 0.28, 2.0), t, 0, 1, 0.7)
    tr.add(bell(hz(m('D5')), 9.0, 0.22, 3.5, 0.8, 2.5), t + 1.0, 0, 1, 0.8)
    return tr


TRACKS = {'big_score': big_score, 'invasion': invasion, 'lucky': lucky, 'market': market, 'hollow': hollow}
LENGTH = {'big_score': 100, 'invasion': 96, 'lucky': 96, 'market': 100, 'hollow': 104}
ROOM = {'big_score': 1.6, 'invasion': 2.4, 'lucky': 1.4, 'market': 2.0, 'hollow': 3.2}

if __name__ == '__main__':
    for nm in (sys.argv[1:] or list(TRACKS)):
        tr = TRACKS[nm]()
        assert round(tr.seconds) == LENGTH[nm], (nm, tr.seconds)
        save_mono(tr, nm, ROOM[nm])
