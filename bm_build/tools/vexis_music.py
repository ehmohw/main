"""2.99: synthesises ADMIRAL VEXIS, VOICE OF THE HIVE - the Armada's boss music: its coming, one loop per phase, each phase's
entrance, the Unlinking, its record, and the quiet after (vendor/boss_vexis_*.ogg, disc_vexis.ogg, ar_after.ogg). Built on the
Armada's own synths (tools/armada_music.py: the theremin, the hive choir, the analog arpeggiator and sequencer, synth brass,
struck hull plates) and its themes, so the fight is where the fleet was going:

THE ADMIRAL'S THEME (V: D A Bb-A G#-A F E Eb D | D F A D Eb D C Bb-A G Eb A) - a fifth, its flat sixth leaning on it, the
tritone below the fifth (the hive's G#), a fall through the flat second; and THE CALL (D-A-Eb), the hive's signal. In the
Unlinking, V's opening comes back once more on the theremin - in D MAJOR, with a natural sixth: what Vexis was, before.

THE COMING (boss_vexis_intro, 20 s, once): a pre-roll, then ten bars of the Warframe's tempo ending on its downbeat. Darkness,
  a turbine spinning up; the systems lighting one by one - the legs (a clank, a servo), the reactor (the sequencer's first
  pulse, a thrum), the arms (pistons, the arpeggiator), the cockpit (the choir's first voice); the window flooding red (the
  choir swelling D minor to its flat second); the hive speaking (THE CALL, choir and horns); it stands - the cannon arm's
  whine - and THE PODS OPEN at 16.25 s on D minor, everything; then the Warframe's own last bar (a riser, a roll) into it.
I.  THE WARFRAME (boss_vexis1, a 120 s loop). D minor, 128 BPM (64 bars of 15/8 s): heavy, mechanical.
  bars  0-7   POWER       the hum, servos whining up, pistons, hull plates struck on the one; the sequencer in sixteenths
  bars  8-15  THE MARCH   V in the low horns over the mechanical march (pistons and plates), the driven riff
  bars 16-23  THE ADMIRAL V in the horns, the theremin an octave over it, the choir
  bars 24-31  PYLONS      the shields: shimmering arpeggios, star-bells, the pylon tune (P) on the theremin, half time
  bars 32-39  CANNON      the war drums, the riff, stabs hammered, the plasma cannon sweeping (long laser falls)
  bars 40-47  MISSILES    targeting pings in sixteenths, a lock tone, V at double speed on a driven lead, twice
  bars 48-55  ALL ARMS    V for everyone - horns in octaves, the choir on top, the theremin, a crash every bar
  bars 56-63  STOMP       half time, shockwaves (a plate and a boom on one and three), THE CALL hammered; the brink
THE TORN FRAME (boss_vexis_enter2, 14 s, once): the frame staggers (the klaxon, a plate struck again and again, a servo
  dying), the cockpit cracks and sparks, BLOWS (6.5 s); a breath; Vexis climbs out - the choir rising D minor to its tritone,
  the theremin emerging with THE CALL - and lifts on gravity (a sub rising, a reversed swell) into the Hive-Link's downbeat.
II. THE HIVE-LINK (boss_vexis2, a 120 s loop). D phrygian, its tritone (Ab minor) and its flat second; 96 BPM (48 bars of 5/2
  s): eerie. The hive's chatter (the choir's breath gated in sixteenths), the theremin.
  bars  0-7   THE LINK    a drone, the chatter, a heartbeat in the sub, the ticking arpeggiator, THE CALL on the theremin
  bars  8-15  THE VOICE   V on the theremin, slow, over the choir; the drums in half time
  bars 16-23  WELLS       gravity wells: subs falling away, reversed swells, the sequencer swirling; V's head in the horns
  bars 24-31  THE BEAM    the choir shrieking 'ee' in clusters; the link tune (L) wailing high; the drums driving
  bars 32-39  CLONES      four theremins in canon on V's first half - which is real? - then one alone with the rest of it
  bars 40-47  THE HIVE    the choir barking (COMPLY), V's end in the horns, THE CALL; the brink
THE STAR (boss_vexis_enter3, 15 s, once): it turns to the window and reaches - the choir climbing a semitone at a time, the
  theremin sliding up with it (5 s); the star's fire pours through the glass (a roaring flare, the horns swelling, 9 s); its
  skin cracks with light (star-bells, glass, a shriek); STARFIRE ignites (11 s): a blow, a double-kick roll, the riser.
III. STARFIRE (boss_vexis3, a 120 s loop). D minor, Eb minor for its height; 168 BPM (84 bars of 10/7 s): blazing, frantic.
  bars  0-7   IGNITION    a blow, the double kick, the sequencer driven, flares sweeping; THE CALL in the horns
  bars  8-23  FLARE       V in the horns in octaves; again with the theremin on top; the arpeggios frantic
  bars 24-39  THE LANCE   the riff and a sixteenth lance-line, beams sweeping, the theremin wailing, stabs
  bars 40-47  GRAVITY FLIP half time - everything thrown up; subs falling, the theremin alone with THE CALL
  bars 48-63  STARFIRE    V a semitone higher, Eb minor - everything, a crash every bar, the choir's COMPLY
  bars 64-79  FRENZY      "IMPROVE": the choir hammered, V at double speed in horns and theremin, twice
  bars 80-83  THE PLUNGE  D minor and its flat second hammered, a roll and a riser - and round again
THE UNLINKING (boss_vexis_unlink, 30 s, once, under the fall - timed to phase242's cinematic): the hive SCREAMS (a choir
  cluster, broken, stuttering); it calls him - "VEXIS." (1 s) "VEXIS. RESPOND." (2.2 s) "VEXIS VEXIS VEXIS VEX" (3.5 s); the
  implants burn out one by one (1.5 s on, every 0.9 s) and each takes a voice with it, sagging and closing; the sequencer
  slowing and sinking like a machine powering down; at 9 s SILENCE. A breath. At 13.5 s ("...one. I am only one.") a single
  fragile theremin: A, then D. 17 s (it shrinks to what it was): a soft pad, B flat, C - the line sighing down. 20.5 s ("Vexis.
  That was my name."): V's opening, but in D MAJOR, with a natural sixth. 24 s ("Show me?"): a rising question, held on G
  major's third. 27 s (THE HIVE-LINK IS CUT): D major, a star-bell - and it lets go.
THE RECORD (disc_vexis, mono, ~3 min): the coming, the Warframe, the torn frame, the Hive-Link, the star, Starfire's height
  and frenzy - and the Unlinking, whole, for an ending.
THE QUIET AFTER (ar_after, 36 s, once - phase244 plays it aboard after the fall): the Unlinking's last part again, slower,
  the one voice left: the theremin's D-major line over a soft pad and a little music-box arpeggio, coming to rest.

Deterministic; run it to rebuild the .ogg files (needs numpy, scipy and ffmpeg):
    python3 tools/vexis_music.py [p1 p2 p3 intro enter2 enter3 unlink after disc] [check]"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gv_music import SR, R, Track, m, hz, fq, T, env, lp, hp, bp, riser, tom
from boss_music import crash, mel, tp, bars_of
from sovereign_music import clank, boom, suck, edge, drone, whisper, gaze, glass, dur_x, render, _guarded, _decode, seeded, View
from armada_music import (M, ch, osc, vlp, smooth, mono, apad, horn, stab, ther_line, ther, hive, _formants, ekick, esnare, mhat,
                          hull, ping, sbell, servo, piston, creak, zap, alarm, sub808, ply, echo, addc, L_drone, L_hum, L_sub, L_pulse,
                          L_arp, L_pad, L_hive, L_call, L_stabs, L_riff, L_drums, L_pings, roll, brink, impact, comply, SEC, V, VF,
                          CALL, P_DOCK, P_V, P_WAR, P_FORGE)

VENDOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vendor')
WF_BPM, WF_BARS = 128, 64
HL_BPM, HL_BARS = 96, 48
SF_BPM, SF_BARS = 168, 84

P_PYL = [('D2', 'm'), ('G1', 'm'), ('F2', 'M'), ('D2', 'm'), ('Eb2', 'M7'), ('Bb1', 'M'), ('G1', 'm'), ('A1', '7b9')]      # (under P)
P_HL = [('D2', 'm'), ('D2', 'm'), ('Ab1', 'm'), ('Ab1', 'm'), ('Eb2', 'M'), ('Eb2', 'M'), ('Bb1', 'm'), ('A1', '7')]       # (the link)
P_HL2 = [('D2', 'm'), ('Eb2', 'M'), ('Ab1', 'm'), ('G1', 'm'), ('D2', 'm'), ('Eb2', 'M'), ('Bb1', 'm'), ('A1', '7b9')]
P_CLONE = [('D2', 'm'), ('Bb1', 'M'), ('G1', 'm'), ('D2', 'm'), ('D2', 'm'), ('C2', 'm'), ('Eb2', 'M'), ('A1', '7')]       # (= P_V)
P_PLUNGE = [('D2', 'm'), ('Eb2', 'M'), ('D2', 'm'), ('A1', '7b9')]

PYL = mel('A5:2 D6 C6 Bb5:2 A5 G5 A5:4 F5:2 G5 A5 D6:2 Eb6:2 D6:3 C6 Bb5:2 A5 G5 E5:2 F5 G5')          # (the pylons' tune: 8 bars)
LINK = mel('D5:4 Ab5:4 G5:2 F5:2 Eb5:4 D5:4 Ab4:4 A4:8')                                               # (the link: 8 bars)
WAIL = mel('D6:4 Eb6:4 D6:2 C6:2 Bb5:4 A5:8 G#5:4 A5:4')                                              # (8 bars)
for _x, _b in ((PYL, 8), (LINK, 8), (WAIL, 8)):
    assert bars_of(_x) == _b, (_b, bars_of(_x))


def tpp(prog, k):
    return [(M(r) + k, kd) for r, kd in prog]


def first(notes, bars, beats=4):
    """the first `bars` bars of a line"""
    out, t = [], 0.0
    for x, d in notes:
        if t >= bars * beats - 1e-6: break
        out.append((x, min(d, bars * beats - t))); t += d
    return out


def after_bars(notes, bars, beats=4):
    out, t = [], 0.0
    for x, d in notes:
        if t >= bars * beats - 1e-6: out.append((x, d))
        t += d
    return out


# ====================================================================== the boss's own sounds
def drop(f0, f1, dur, amp=1.0, drive=1.6):
    """a gravity well: a sine falling (or rising) away, driven"""
    t = T(dur); u = np.clip(t / dur, 0, 1)
    fr = fq(f0) * (fq(f1) / fq(f0)) ** (1 - (1 - u) ** 2)
    s = np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * drive) / np.tanh(drive)
    return amp * s * env(len(t), 0.02, 0, 1, dur * 0.35)


def flare(dur, amp=1.0, peak=0.45):
    """a star-flare: a roar of fire sweeping open and closed, crackling"""
    t = T(dur); n = len(t); u = t / dur
    nz = R.noise(n)
    shape = np.where(u < peak, (u / peak) ** 1.5, ((1 - u) / (1 - peak)) ** 0.8)
    s = vlp(nz, 300 + 6000 * shape, 1.4, 2, 128) * 0.9
    s += hp(nz, 4000) * (R.noise(n) > 0.985) * 0.6 * shape
    return amp * s * shape


def lance(amp=1.0, dur=1.2):
    """the plasma lance (or the cannon's sweep): a long laser falling, a beam hum under it"""
    t = T(dur)
    ph = np.cumsum(2600 * (120 / 2600) ** (t / dur)) / SR
    s = np.sin(2 * np.pi * ph + 2.5 * np.sin(2 * np.pi * ph * 0.502)) * np.exp(-t * 1.8)
    s += 0.5 * np.tanh(3 * np.sin(2 * np.pi * 73 * t)) * np.exp(-t * 2.5)
    return amp * s * env(len(t), 0.004, 0, 1, 0.1) * 0.6


def turbine(dur, amp=1.0, f0=20.0, f1=74.0):
    """spinning up: a low saw climbing, its filter opening, a whine of its fifth over it"""
    t = T(dur); n = len(t); u = np.clip(t / dur, 0, 1)
    fr = f0 * (f1 / f0) ** (u ** 1.4)
    s = osc(fr, 'saw') + 0.6 * osc(fr * 1.5, 'pulse', 0.3) + 0.3 * np.sin(2 * np.pi * np.cumsum(fr * 12) / SR)
    s = vlp(s, 120 + 2200 * u ** 2, 2.5, 4, 128)
    return amp * s * env(n, dur * 0.5, 0, 1, 0.1)


def hive_voice(x, dur, amp=1.0, vowel='a', sag_at=None, sag=7.0, close='u', die=0.9, attack=0.05):
    """one throat of the hive - and, at sag_at, the link burning out of it: its pitch sagging, its mouth closing, gone"""
    t = T(dur); n = len(t)
    f = hz(M(x))
    u = np.zeros(n) if sag_at is None else np.clip((t - sag_at) / die, 0, 1)
    u = u * u * (3 - 2 * u)
    fr = f * 2 ** (-sag / 12 * u) * (1 + 0.0065 * np.sin(2 * np.pi * 4.7 * t + R.r() * 6))
    s = sum(osc(fr * (1 + dv)) for dv in (-0.007, -0.0025, 0.0025, 0.007)) / 4
    y = _formants(s, vowel) * (1 - u) + _formants(s, close) * u
    y = y + 0.25 * bp(y * np.sin(2 * np.pi * f * 1.503 * t), 300, 4000, 1)
    return amp * 5.0 * y * env(n, attack, 0, 1, 0.15) * (1 - u) ** 1.5


def syll(notes, dur, amp, v1, v2):
    """the hive speaking a syllable: a chord barked on one vowel, closing on the next"""
    return hive(notes, dur, amp, v1, v2, 0.015, min(0.12, dur * 0.4), 4, alien=0.35)


def lock(amp=1.0):
    """the missile lock: a rapid tick-tick-tick, then a held tone"""
    t = T(0.5)
    s = np.sin(2 * np.pi * 2093 * t) * (np.floor(t * 24) % 2 == 0) * (t < 0.25) + np.sin(2 * np.pi * 2349 * t) * (t >= 0.25)
    return amp * s * env(len(t), 0.002, 0, 1, 0.04) * 0.5


def at(tr, bar, beat=0.0):
    return tr.at(bar, beat)


def want(tr, bar):
    return tr.want(bar) if hasattr(tr, 'want') else True


# ====================================================================== I. THE WARFRAME
WF_PLAN = [P_DOCK, P_V, P_V, P_PYL, P_WAR, P_FORGE, P_V, P_DOCK]


def wf_compose(tr):
    for s, prog in enumerate(WF_PLAN):
        if s == 0:                                                     # POWER
            L_hum(tr, s, 'D1', 0.2)
            L_sub(tr, s, prog, 0.26, 1)
            L_pulse(tr, s, prog, 0.12, 300, 1400, 0.25, 12, None, 2.6, drive=1.6)
            for b in range(SEC):
                if not want(tr, b): continue
                tr.add(hull(0.6, 72, 1.3, b), at(tr, b), 0, 1, 0.4); tr.add(ekick(0.55), at(tr, b), 0, 1, 0.08)
                tr.add(hull(0.3, 120, 0.8, 50 + b), at(tr, b, 2.5), 0.2, 1, 0.4)
                tr.add(esnare(0.3), at(tr, b, 2), 0.05, 1, 0.35)
                if b % 2 == 0: tr.add(servo(tr.barlen * 1.6, 0.1, 140 + 20 * b, 380 + 40 * b), at(tr, b, 0.5), (-0.5, 0.5)[b // 2 % 2], 1, 0.4)
                if b % 2 == 1: tr.add(piston(0.32), at(tr, b, 3), (0.4, -0.4)[b // 2 % 2], 1, 0.4)
                for i in range(4): tr.add(mhat(0.05, False), at(tr, b, i + 0.5), 0.35, 1, 0.15)
            for b in (2, 6):
                if want(tr, b): ply(tr, at(tr, b), tp(CALL, -24), lambda x, d: horn([x, M(x) + 12], d, 0.14, 1500, 500, 0.08), -0.1, 1, 0.4)
            continue
        if s == 7:                                                     # STOMP
            L_hum(tr, s, 'D1', 0.18)
            L_sub(tr, s, prog, 0.26, 1)
            L_pulse(tr, s, prog, 0.1, 400, 900, 0.5, 12, None, 2.4, drive=1.4)
            for b in range(SEC):
                bar = s * SEC + b
                if not want(tr, bar): continue
                for bt in (0, 2):
                    tr.add(hull(0.75, 58, 1.6, bar * 2 + bt), at(tr, bar, bt), 0, 1, 0.45)
                    tr.add(ekick(0.75, 4.5, 140, 38), at(tr, bar, bt), 0, 1, 0.1)
                    if bt == 0 and b % 2 == 0: tr.add(boom(0.35, 80, 26, 1.8), at(tr, bar, bt), 0, 1, 0.4)
                tr.add(esnare(0.45), at(tr, bar, 3), 0.05, 1, 0.4)
                for i in range(8): tr.add(mhat(0.06, i % 4 == 2), at(tr, bar, i / 2), 0.35, 1, 0.15)
            for b in (0, 2, 4):
                if want(tr, s * SEC + b):
                    ply(tr, at(tr, s * SEC + b), tp(CALL, -12), lambda x, d: horn([x, M(x) - 12], d, 0.16, 2400, 600, 0.05), -0.1, 1, 0.4)
                    ply(tr, at(tr, s * SEC + b), CALL, lambda x, d: hive([x, M(x) - 12], d + 0.2, 0.08, 'a', None, 0.06, 0.5), 0.15, 1, 0.55)
            brink(tr, s, 0.45)
            continue
        L_sub(tr, s, prog, 0.26, 1)
        if s == 3:                                                     # PYLONS
            L_drums(tr, s, 'half', 0.85, crash_=False)
            L_arp(tr, s, prog, 0.06, m('D5'), 'wide', 0.25, 1400, 3000, 2.2, 0.55, True, 'tri', wet=0.5)
            L_pulse(tr, s, prog, 0.1, 300, 900, 0.5, 12, None, 2.2)
            L_hive(tr, s, prog, 0.09, 'u', 'a', 12, 2, 0.6)
            for b in range(SEC):
                if want(tr, s * SEC + b):
                    cc = ch(prog[b]); tr.add(sbell(cc[2] + 36, 2.5, 0.05), at(tr, s * SEC + b, 1), 0.55, 1, 0.75)
                    tr.add(glass(cc[0] + 48, 1.0, 0.04), at(tr, s * SEC + b, 3), -0.5, 1, 0.7)
            ther(tr, at(tr, s * SEC), PYL, 0.26, 0.05, 0.45, port=0.06)
            ply(tr, at(tr, s * SEC), tp(PYL, -12), lambda x, d: horn([x], d, 0.07, 1400, 500, 0.1), -0.25, 1, 0.5)
            continue
        style = {1: 'march', 2: 'march', 4: 'war', 5: 'drive', 6: 'march'}[s]
        L_drums(tr, s, style, 1.0)
        if s in (1, 2, 4, 6): L_riff(tr, s, prog, 0.11, 12, (1, 1, 0, 1, 1, 0, 1, 1) if s != 4 else (1,) * 8, 5.0, 900)
        L_pulse(tr, s, prog, 0.09, 600, 1600, 0.25, 24, None, 2.4, pan=0.25)
        if s in (2, 6): L_hive(tr, s, prog, 0.1, 'a', None, 12, 2, 0.3, top=s == 6)
        if s == 1:
            ply(tr, at(tr, s * SEC), tp(V, -12), lambda x, d: horn([x, M(x) + 12], d, 0.2, 2200, 500), -0.1, 1, 0.4)
            ply(tr, at(tr, s * SEC), tp(V, -24), lambda x, d: horn([x], d, 0.12, 900, 300), 0.1, 1, 0.3)
            L_stabs(tr, s, prog, 0.1, (3.5,), 12, 2)
        if s == 2:
            ply(tr, at(tr, s * SEC), V, lambda x, d: horn([x, M(x) - 12], d, 0.19, 2800, 600), -0.1, 1, 0.4)
            ther(tr, at(tr, s * SEC), tp(V, 12), 0.27, 0.15, 0.4, port=0.05)
        if s == 4:                                                     # CANNON
            L_stabs(tr, s, prog, 0.13, (0, 1.5, 3), 12, 1)
            for b in range(0, SEC, 2):
                if want(tr, s * SEC + b):
                    tr.add(lance(0.14, tr.barlen * 1.4), at(tr, s * SEC + b, 2), (-0.5, 0.5)[b // 2 % 2], 1, 0.45)
                    tr.add(boom(0.25, 90, 30, 1.5), at(tr, s * SEC + b, 2), 0, 1, 0.4)
            ther(tr, at(tr, s * SEC), WAIL, 0.24, 0.2, 0.45, port=0.1)
            L_call(tr, s, (2, 6), 0.08, -12, 'a', -0.3)
        if s == 5:                                                     # MISSILES
            for b in range(SEC):
                bar = s * SEC + b
                if not want(tr, bar): continue
                cc = ch(prog[b])
                for i in range(16):
                    tr.add(ping(cc[i % 3] + 48, 0.025, 0.35), at(tr, bar, i / 4), (-0.7, 0.7)[i % 2], 1, 0.4)
                if b % 2 == 1: tr.add(lock(0.08), at(tr, bar, 3), 0.3, 1, 0.35)
            for k in (0, 4):
                ply(tr, at(tr, s * SEC + k), VF, lambda x, d: mono(x, d, 0.14, 'saw', 1500, 2600, 6, 1.8, 0.008, 0, 0.004, 0.1, 0.75, 0.05, drive=2.2), -0.05, 1, 0.35)
                ply(tr, at(tr, s * SEC + k), tp(VF, -12), lambda x, d: horn([x], d, 0.1, 1600, 500, 0.03), 0.2, 1, 0.35)
        if s == 6:                                                     # ALL ARMS
            ply(tr, at(tr, s * SEC), V, lambda x, d: horn([x, M(x) + 12, M(x) - 12], d, 0.2, 3200, 700), -0.1, 1, 0.4)
            ply(tr, at(tr, s * SEC), V, lambda x, d: hive([M(x) + 12], d + 0.2, 0.1, 'a', None, 0.06, 0.5), 0.25, 1, 0.5)
            ther(tr, at(tr, s * SEC), tp(V, 12), 0.25, 0.2, 0.4, port=0.05)
            L_stabs(tr, s, prog, 0.1, (1.5, 3.5), 12, 1)
            for b in range(SEC):
                if want(tr, s * SEC + b): tr.add(crash(0.2), at(tr, s * SEC + b), (-0.3, 0.3)[b % 2], 1, 0.5)
    return tr


def p1():
    tr = Track('vexis1', WF_BPM, WF_BARS)
    assert round(tr.seconds) == 120
    wf_compose(View(tr, WF_BPM))
    return tr


# ====================================================================== II. THE HIVE-LINK
HL_PLAN = [P_HL, P_HL, P_HL2, P_HL, P_CLONE, P_HL2]


def hl_compose(tr):
    chat = 4 / tr.beat                                                 # (the chatter: sixteenths)
    for s, prog in enumerate(HL_PLAN):
        base = s * SEC
        L_drone(tr, s, ['D2', 'A2'] if s != 2 else ['D2', 'Ab2'], 0.12)
        L_sub(tr, s, prog, 0.22, 2)
        if s == 0:                                                     # THE LINK
            L_hive(tr, s, prog, 0.1, 'u', 'o', 12, 2, 1.0, 0.65)
            for b in range(SEC):
                if want(tr, base + b):
                    tr.add(sub808(m('D1'), 0.5, 0.3), at(tr, base + b), 0, 1, 0.05); tr.add(sub808(m('D1'), 0.4, 0.2), at(tr, base + b, 0.6), 0, 1, 0.05)
            L_arp(tr, s, prog, 0.045, m('D5'), 'tick', 0.25, 900, 1600, 2.2, 0.5, True, 'tri', wet=0.5)
            for b in (2, 6):
                if want(tr, base + b): ther(tr, at(tr, base + b), CALL, 0.24, (-0.2, 0.2)[b // 4], 0.55, port=0.18, depth=0.016)
            L_pings(tr, s, ('D6', 'Ab5'), 2, 0.05)
        if s == 1:                                                     # THE VOICE
            L_hive(tr, s, prog, 0.1, 'o', None, 12, 2, 0.6, 0.4)
            L_drums(tr, s, 'half', 0.75, crash_=False)
            L_arp(tr, s, prog, 0.045, m('D4'), 'tick', 0.25, 800, 1600, 2.2, 0.5, True, 'tri', wet=0.45)
            ther(tr, at(tr, base), V, 0.27, 0.0, 0.55, port=0.13, depth=0.015)
            ply(tr, at(tr, base), tp(V, -12), lambda x, d: hive([x], d + 0.3, 0.06, 'u', 'o', 0.3, 0.8), -0.25, 1, 0.6)
        if s == 2:                                                     # WELLS
            L_hive(tr, s, prog, 0.09, 'u', 'o', 12, 2, 0.8, 0.5)
            L_pulse(tr, s, prog, 0.1, 300, 1500, 0.25, 12, None, 4.0)
            L_drums(tr, s, 'half', 0.8, crash_=False)
            for b in range(SEC):
                if not want(tr, base + b): continue
                if b % 2 == 0:
                    tr.add(drop('D2', 'D0', tr.barlen * 1.5, 0.3), at(tr, base + b, 1), 0, 1, 0.1)
                    tr.add(zap(0.05, 1200, 60, 1.2), at(tr, base + b, 1), (-0.5, 0.5)[b // 2 % 2], 1, 0.6)
                else:
                    tr.add(suck(tr.barlen, 0.22), at(tr, base + b), (0.4, -0.4)[b // 2 % 2], 1, 0.35)
            for b in (0, 4):
                if want(tr, base + b): ply(tr, at(tr, base + b), tp(first(V, 2), -12), lambda x, d: horn([x, M(x) - 12], d, 0.16, 1600, 450, 0.1), -0.1, 1, 0.45)
            ther(tr, at(tr, base + 2), [('Ab5', 4), ('G5', 2), ('F5', 2)], 0.17, 0.4, 0.6, port=0.16)
            ther(tr, at(tr, base + 6), [('D6', 4), ('Eb6', 4)], 0.17, -0.4, 0.6, port=0.16)
        if s == 3:                                                     # THE BEAM
            L_drums(tr, s, 'drive', 0.8)
            L_pulse(tr, s, prog, 0.1, 600, 1800, 0.25, 12, None, 2.6, drive=1.4)
            L_arp(tr, s, prog, 0.05, m('D5'), 'wave', 0.25, 1200, 2600, 2.6, 0.45)
            for b in range(0, SEC, 2):
                if want(tr, base + b):
                    cc = ch(prog[b])
                    tr.add(hive([cc[0] + 36, cc[1] + 36, cc[0] + 37], tr.barlen * 2, 0.07, 'i', 'e', 0.4, 0.5, gate=0.6, rate=chat), at(tr, base + b), 0.2, 1, 0.6)
            ther(tr, at(tr, base), tp(LINK, 12), 0.25, 0.1, 0.5, port=0.12)
            ply(tr, at(tr, base), LINK, lambda x, d: hive([x], d + 0.3, 0.09, 'o', 'a', 0.15, 0.6), -0.2, 1, 0.55)
        if s == 4:                                                     # CLONES
            L_hive(tr, s, prog, 0.08, 'u', None, 12, 2, 0.8)
            L_drums(tr, s, 'half', 0.8, crash_=False)
            L_arp(tr, s, prog, 0.04, m('D5'), 'tick', 0.25, 900, 1800, 2.2, 0.5, True, 'tri', wet=0.5)
            head = first(V, 4)
            for i, pan in enumerate((-0.85, 0.85, -0.4, 0.4)):
                if want(tr, base + i): ther(tr, at(tr, base + i), tp(head, 12 if i % 2 else 0), 0.17, pan, 0.55, echo_=False, port=0.08, vib=5.6 + 0.5 * i)
            if want(tr, base + 4): ther(tr, at(tr, base + 4), after_bars(V, 4), 0.27, 0.0, 0.45, port=0.08)
            for b in range(SEC):
                if want(tr, base + b) and b < 4: tr.add(glass(m('D7') - 5 * b, 0.8, 0.04), at(tr, base + b, 3.5), (0.6, -0.6)[b % 2], 1, 0.7)
        if s == 5:                                                     # THE HIVE
            L_hive(tr, s, prog, 0.1, 'a', None, 12, 2, 0.3, top=True)
            comply(tr, s, prog, 0.1, range(4))
            L_drums(tr, s, 'march', 0.9)
            L_pulse(tr, s, prog, 0.1, 700, 2000, 0.25, 12, None, 2.6, drive=1.4)
            L_call(tr, s, (0, 2), 0.09, 0, 'a', 0.3)
            if want(tr, base + 4): ply(tr, at(tr, base + 4), after_bars(V, 4), lambda x, d: horn([x, M(x) - 12], d, 0.2, 2600, 600), -0.1, 1, 0.4)
            if want(tr, base + 4): ther(tr, at(tr, base + 4), tp(after_bars(V, 4), 12), 0.22, 0.2, 0.45, port=0.07)
            brink(tr, s, 0.4)
    return tr


def p2():
    tr = Track('vexis2', HL_BPM, HL_BARS)
    assert round(tr.seconds) == 120
    hl_compose(View(tr, HL_BPM))
    return tr


# ====================================================================== III. STARFIRE
SF_PLAN = [(P_WAR, 0), (P_V, 0), (P_V, 0), (P_FORGE, 0), (P_WAR, 0), (P_DOCK, 0), (P_V, 1), (P_V, 1), (P_WAR, 1), (P_WAR, 0), (P_PLUNGE, 0)]


def sf_compose(tr):
    for s, (prog0, k) in enumerate(SF_PLAN):
        prog = tpp(prog0, k)
        base = s * SEC; nb = len(prog)
        if not any(want(tr, base + b) for b in range(nb)): continue
        L_sub(tr, s, prog, 0.27, 1)
        if s == 5:                                                     # GRAVITY FLIP
            L_hum(tr, s, 'D1', 0.16)
            L_pulse(tr, s, prog, 0.11, 400, 1200, 0.25, 12, None, 3.2)
            L_hive(tr, s, prog, 0.1, 'u', 'a', 12, 4, 1.0, top=True)
            for b in range(SEC):
                if not want(tr, base + b): continue
                tr.add(ekick(0.5, 6), at(tr, base + b), 0, 1, 0.1); tr.add(esnare(0.3), at(tr, base + b, 2), 0.05, 1, 0.45)
                if b % 2 == 0: tr.add(drop('A2', 'D0', tr.barlen * 1.6, 0.26), at(tr, base + b, 0.5), 0, 1, 0.1)
                else: tr.add(suck(tr.barlen * 0.9, 0.25), at(tr, base + b, 0.4), 0.3, 1, 0.3)
            for b in (0, 4):
                if want(tr, base + b): ther(tr, at(tr, base + b), CALL if b == 0 else tp(CALL, 12), 0.26, (-0.2, 0.2)[b // 4], 0.55, port=0.14)
            continue
        if s == 10:                                                    # THE PLUNGE
            for b, c in enumerate(prog):
                bar = base + b
                if not want(tr, bar): continue
                cc = ch(c)
                for bt in ((0, 0.5, 1, 2, 2.5, 3, 3.5) if b < 2 else (0, 1, 2)):
                    tr.add(stab([cc[0], cc[0] + 7, cc[0] + 12, cc[1] + 12], tr.beat * 0.4, 0.16), at(tr, bar, bt), 0, 1, 0.3)
                    tr.add(ekick(0.6), at(tr, bar, bt), 0, 1, 0.06)
                for bt in (1, 3): tr.add(esnare(0.45), at(tr, bar, bt), 0.05, 1, 0.3)
                tr.add(hull(0.4, 80, 1.0, bar), at(tr, bar), 0, 1, 0.4)
                tr.add(hive([cc[0] + 24, cc[1] + 24, cc[2] + 24], tr.barlen, 0.1, 'a', None, 0.05, 0.3), at(tr, bar), 0, 1, 0.5)
            if want(tr, base): tr.add(crash(0.4), at(tr, base), 0.3, 1, 0.5)
            brink(tr, s, 0.5, base + nb)
            continue
        drums = {0: 'war', 1: 'war', 2: 'war', 3: 'drive', 4: 'war', 6: 'war', 7: 'war', 8: 'war', 9: 'war'}[s]
        L_drums(tr, s, drums, 1.0)
        L_pulse(tr, s, prog, 0.1, 800, 2200, 0.25, 12, None, 2.6, drive=1.6)
        L_arp(tr, s, prog, 0.055, m('D5') + k, 'wave' if s % 2 else 'up', 0.25, 1600, 3400, 3.0, 0.45)
        if s == 0:                                                     # IGNITION
            if want(tr, 0): impact(tr, at(tr, 0), 1.0)
            for b in (0, 4):
                if want(tr, b): tr.add(flare(tr.barlen * 3, 0.14), at(tr, b), (-0.4, 0.4)[b // 4], 1, 0.4)
            for b in (2, 6):
                if want(tr, b): ply(tr, at(tr, b), tp(CALL, -12), lambda x, d: horn([x, M(x) - 12], d, 0.18, 2600, 600, 0.04), -0.1, 1, 0.4)
            L_hive(tr, s, prog, 0.1, 'a', None, 12, 2, 0.2, top=True)
        if s in (1, 2):                                                # FLARE
            ply(tr, at(tr, base), V, lambda x, d: horn([x, M(x) + 12, M(x) - 12], d, 0.2, 3200, 700, 0.03), -0.1, 1, 0.4)
            L_hive(tr, s, prog, 0.09, 'a', None, 12, 2, 0.2)
            if s == 2: ther(tr, at(tr, base), tp(V, 12), 0.26, 0.2, 0.4, port=0.04)
            if s == 1: L_stabs(tr, s, prog, 0.09, (3.5,), 12, 2)
        if s in (3, 4):                                                # THE LANCE
            L_riff(tr, s, prog, 0.12, 12, (1,) * 8, 6.0, 1100)
            L_stabs(tr, s, prog, 0.1, (1.5, 3.5), 12, 2)
            for b in range(0, SEC, 2):
                if want(tr, base + b): tr.add(lance(0.13, tr.barlen * 1.5), at(tr, base + b, 1), (-0.5, 0.5)[b // 2 % 2], 1, 0.45)
            ther(tr, at(tr, base), WAIL if s == 3 else tp(WAIL, -12), 0.25, 0.2, 0.45, port=0.08)
            if s == 4: comply(tr, s, prog, 0.08, range(0, 8, 2))
        if s in (6, 7):                                                # STARFIRE (Eb minor)
            ply(tr, at(tr, base), tp(V, k), lambda x, d: horn([x, M(x) + 12, M(x) - 12], d, 0.21, 3400, 800, 0.03), -0.1, 1, 0.4)
            ply(tr, at(tr, base), tp(V, k), lambda x, d: hive([M(x) + 12], d + 0.15, 0.1, 'a', None, 0.04, 0.4), 0.25, 1, 0.5)
            ther(tr, at(tr, base), tp(V, 12 + k), 0.26, 0.2, 0.4, port=0.04)
            L_hive(tr, s, prog, 0.09, 'a', None, 12, 2, 0.2, top=True)
            if s == 7: comply(tr, s, prog, 0.08, range(1, 8, 2))
            for b in range(SEC):
                if want(tr, base + b): tr.add(crash(0.2), at(tr, base + b), (-0.3, 0.3)[b % 2], 1, 0.5)
            if want(tr, base + 4): tr.add(flare(tr.barlen * 3, 0.12), at(tr, base + 4), 0.3, 1, 0.4)
        if s in (8, 9):                                                # FRENZY: IMPROVE
            comply(tr, s, prog, 0.11)
            L_riff(tr, s, prog, 0.1, 12, (1,) * 8, 6.0, 1200)
            for kk in (0, 4):
                ply(tr, at(tr, base + kk), tp(VF, k), lambda x, d: horn([x, M(x) + 12], d, 0.19, 3400, 800, 0.02), -0.1, 1, 0.35)
                ther(tr, at(tr, base + kk), tp(VF, 12 + k), 0.25, 0.2, 0.4, port=0.03)
            if want(tr, base): tr.add(flare(tr.barlen * 2, 0.12), at(tr, base), -0.3, 1, 0.4)
    return tr


def p3():
    tr = Track('vexis3', SF_BPM, SF_BARS)
    assert round(tr.seconds) == 120
    sf_compose(View(tr, SF_BPM))
    return tr


# ====================================================================== THE COMING (20 s): a pre-roll, ten bars at 128, onto the downbeat
IPRE, IBARS = 1.25, 10


def intro_compose(tr, t0=0.0):
    v = View(tr, WF_BPM, 4, t0 + IPRE)
    a = lambda sig, t, *k: tr.add(sig, t0 + t, *k)
    fm, eb, a7 = ch(('D2', 'm')), ch(('Eb2', 'M')), ch(('A1', '7b9'))
    # darkness; the turbine spinning up through the whole of it
    a(turbine(16.0, 0.16), 0.2, 0, 1, 0.3)
    a(drone(['D1', 'D2'], 16.5, 0.07, 0.25), 0.0, 0, 1, 0.5)
    for k in range(3): a(whisper(2.5, 0.03, 900 + k), 0.6 + 2.2 * k, (-0.6, 0.6)[k % 2], 1, 0.8)
    v.add(ping('D6', 0.05), v.at(0, 1), -0.4, 1, 0.7); v.add(ping('A5', 0.04), v.at(1, 1), 0.4, 1, 0.7)
    # the legs: a plate, a servo
    v.add(hull(0.3, 80, 1.3, 1), v.at(2), -0.3, 1, 0.45); v.add(servo(1.6, 0.07, 120, 300), v.at(2, 1), -0.4, 1, 0.4)
    v.add(hull(0.3, 90, 1.3, 2), v.at(2, 2), 0.3, 1, 0.45); v.add(servo(1.6, 0.07, 130, 340), v.at(2, 3), 0.4, 1, 0.4)
    # the reactor: the sequencer's first pulse, a thrum
    for bar in range(3, 8):
        for i in range(8 if bar < 5 else 16):
            r = 0.5 if bar < 5 else 0.25
            v.add(mono(m('D2'), v.beat * r * 0.85, 0.05 + 0.022 * (bar - 3), 'saw', 250 + 150 * (bar - 3), 600 + 250 * (bar - 3), 14, 2.4, 0.006, 0.5),
                  v.at(bar, i * r), 0, 1, 0.12)
        v.add(sub808(m('D1'), v.barlen * 0.95, 0.1 + 0.04 * (bar - 3)), v.at(bar), 0, 1, 0.05)
    v.add(hull(0.38, 64, 1.6, 3), v.at(3), 0, 1, 0.45)
    # the arms: pistons, and the arpeggiator wakes
    v.add(piston(0.28), v.at(4), -0.5, 1, 0.4); v.add(piston(0.28), v.at(4, 2), 0.5, 1, 0.4)
    v.add(servo(1.4, 0.09, 200, 520), v.at(4, 0.5), -0.5, 1, 0.4); v.add(servo(1.4, 0.09, 220, 560), v.at(4, 2.5), 0.5, 1, 0.4)
    for bar in range(4, 8):
        up = [fm[0] + 24, fm[1] + 24, fm[2] + 24, fm[0] + 36]
        for i in range(16):
            v.add(mono(up[(0, 1, 2, 3, 2, 1)[i % 6]] + (1 if bar == 6 and i >= 8 else 0), v.beat * 0.22, 0.03 + 0.016 * (bar - 4), 'saw',
                       600 + 300 * (bar - 4), 1500, 18, 2.6, 0.004, 0, 0.002, 0.08, 0.3, 0.05), v.at(bar, i / 4), (0.4, -0.4)[i % 2], 1, 0.35)
    # the cockpit, the pilot: the choir's first voice
    v.add(hive(['D4'], v.barlen * 1.2, 0.08, 'u', 'o', 1.0, 0.6), v.at(5), 0.2, 1, 0.65)
    v.add(ping('D6', 0.06), v.at(5, 2), 0.4, 1, 0.7)
    # the window floods red: the choir swelling, D minor to its flat second
    sw = lambda sig, a0, a1: sig * np.linspace(a0, a1, len(sig))
    v.add(sw(hive([fm[0] + 12, fm[2] + 12, fm[1] + 24, fm[0] + 24], v.barlen + 0.3, 0.16, 'u', 'a', 0.8, 0.3), 0.6, 1.0), v.at(6), 0, 1, 0.6)
    v.add(sw(hive([eb[0] + 12, eb[2] + 12, eb[1] + 24, eb[0] + 24], v.barlen * 0.6, 0.19, 'a', None, 0.2, 0.2), 0.8, 1.15), v.at(6, 2), 0, 1, 0.6)
    v.add(sw(horn([fm[0], fm[2], fm[0] + 12], v.barlen + 0.2, 0.19, 1800, 500, 0.6), 0.5, 1.0), v.at(6), -0.1, 1, 0.45)
    # the hive speaks: THE CALL, choir and horns
    ply(v, v.at(7), tp(CALL, -12), lambda x, d: horn([x, M(x) - 12], d, 0.23, 2600, 600, 0.05), -0.1, 1, 0.45)
    ply(v, v.at(7), CALL, lambda x, d: hive([x, M(x) - 12], d + 0.15, 0.13, 'a', None, 0.05, 0.4), 0.15, 1, 0.55)
    # it stands: the cannon arm comes up
    v.add(servo(v.barlen * 1.0, 0.13, 160, 900), v.at(7, 1), 0.3, 1, 0.4)
    for i in range(16): v.add(tom(70 * (1 + 0.6 * i / 16), 0.08 + 0.02 * i, 8, 0.3), v.at(7, 2 + i / 8), (-0.25, 0.25)[i % 2], 1, 0.35)
    v.add(suck(v.barlen * 0.5, 0.4), v.at(7, 2), 0, 1, 0.3)
    # THE PODS OPEN: ADMIRAL VEXIS
    hit = v.at(8)
    impact(v, hit, 1.2)
    v.add(boom(0.9, 110, 26, 3.0), hit, 0, 1, 0.4)
    v.add(horn([fm[0] - 12, fm[0], fm[2], fm[0] + 12, fm[1] + 12], v.barlen * 0.9, 0.24, 3000, 700, 0.01), hit, 0, 1, 0.4)
    v.add(hive([fm[0] + 24, fm[1] + 24, fm[2] + 24, fm[0] + 36], v.barlen * 0.8, 0.14, 'a', None, 0.02, 0.3), hit, 0, 1, 0.55)
    v.add(sub808(m('D1'), v.barlen, 0.35), hit, 0, 1, 0.05)
    v.add(lance(0.12, 1.4), hit + 0.1, 0.4, 1, 0.45)
    # the Warframe's own last bar: a riser and a roll into its downbeat
    t_end = v.at(10)
    v.add(edge(riser(v.barlen * 1.2, 0.22)), t_end - v.barlen * 1.2, 0, 1, 0.4)
    v.add(suck(v.barlen * 0.8, 0.25), t_end - v.barlen * 0.8, 0.2, 1, 0.3)
    roll(v, t_end, v.barlen * 0.9, 0.24)
    v.add(stab([a7[0] + 12, a7[1] + 12, a7[2] + 12, a7[0] + 24], v.beat * 0.4, 0.12), v.at(9, 3.5), 0, 1, 0.3)


def intro():
    tr = Track('vexis_intro', 60, 23, beats=1)                          # (20 s, and three spare, so nothing wraps round)
    intro_compose(tr)
    return tr


# ====================================================================== THE TORN FRAME (14 s), into the Hive-Link
def enter2_compose(tr, t0=0.0):
    a = lambda sig, t, *k: tr.add(sig, t0 + t, *k)
    a(alarm(6.0, 0.08), 0.0, -0.3, 1, 0.6)
    for k, t in enumerate((0.0, 1.3, 2.4, 3.3, 4.0)):                 # (staggering: the frame's weight coming down)
        a(hull(0.7 - 0.06 * k, 62 + 4 * k, 1.4, 300 + k), t, (-0.2, 0.2)[k % 2], 1, 0.45)
        a(ekick(0.7, 4.5, 130, 36), t, 0, 1, 0.1)
    a(boom(0.6, 90, 28, 2.5), 0.0, 0, 1, 0.4); a(crash(0.4, 3.0), 0.0, 0.2, 1, 0.5)
    a(stab(['D2', 'A2', 'D3', 'Eb3'], 0.6, 0.22), 0.0, 0, 1, 0.35)
    a(servo(3.6, 0.13, 520, 70), 0.3, 0.3, 1, 0.4)                      # (a servo dying)
    g = np.random.default_rng(3200)
    for k in range(10):                                                 # (sparks)
        a(zap(0.06, g.uniform(2500, 4500), g.uniform(300, 900), 0.18), 1.0 + 0.32 * k + g.uniform(0, 0.1), g.uniform(-0.8, 0.8), 1, 0.5)
    for i in range(24):                                                 # (the sequencer stuttering, faltering)
        if g.random() < 0.7:
            a(mono(m('D2') - (i // 8), 0.09, 0.09, 'saw', 400, 900, 14, 2.4, 0.006, 0.5), 0.2 + i * 0.16, 0, 1, 0.15)
    a(drone(['D2', 'Eb2'], 6.0, 0.12, 0.6), 0.0, 0, 1, 0.5)
    # the cockpit cracks, sparks - BLOWS
    for k in range(6): a(glass(m('D7') - 2 * k, 0.8, 0.07), 4.0 + 0.12 * k, (-0.5, 0.5)[k % 2], 1, 0.6)
    a(clank(0.4, 1800, 1.2, 3210), 4.05, 0, 1, 0.5); a(clank(0.35, 2600, 1.0, 3211), 5.4, 0.3, 1, 0.5)
    for k in range(6): a(zap(0.07, 4000, 600, 0.12), 5.5 + 0.13 * k, (-0.6, 0.6)[k % 2], 1, 0.5)
    a(suck(1.0, 0.4), 5.5, 0, 1, 0.3)
    a(boom(1.0, 120, 26, 3.5), 6.5, 0, 1, 0.45); a(crash(0.55, 4.0), 6.5, 0.2, 1, 0.55)
    a(flare(1.6, 0.25, 0.1), 6.5, 0, 1, 0.45); a(hull(0.9, 55, 1.8, 330), 6.5, 0, 1, 0.5)
    a(horn(['D2', 'D3', 'A3', 'D4', 'Eb4'], 1.2, 0.2, 3200, 600, 0.005), 6.5, 0, 1, 0.45)
    # a breath; Vexis climbs out: the choir rising, D minor to its tritone; the theremin, THE CALL
    a(hive(['D3', 'A3', 'D4', 'F4'], 3.8, 0.1, 'u', 'o', 1.5, 0.8), 7.4, 0, 1, 0.7)
    a(hive(['Ab2', 'Eb3', 'Ab3', 'Cb4'], 3.6, 0.11, 'o', 'a', 1.6, 0.5), 10.4, 0, 1, 0.65)
    s = ther_line(CALL, 0.55, 0.26, port=0.2, depth=0.016)
    a(s, 8.2, 0.1, 1, 0.6); a(lp(s, 2400), 8.2 + 0.41, -0.5, 0.3, 0.75)
    # it lifts on gravity: a sub rising, a reversed swell, the chatter beginning (the Hive-Link's sixteenths at 96)
    a(drop('D0', 'D2', 3.2, 0.3), 10.8, 0, 1, 0.1)
    a(suck(2.6, 0.55), 11.4, 0, 1, 0.3); a(edge(riser(3.0, 0.25)), 11.0, 0, 1, 0.35)
    for i in range(16):
        a(hive(['D4', 'A4'], 0.12, 0.02 + 0.004 * i, 'u', None, 0.01, 0.05, 3), 11.5 + i * 0.15625, (-0.4, 0.4)[i % 2], 1, 0.5)


def enter2():
    tr = Track('vexis_enter2', 60, 17, beats=1)
    enter2_compose(tr)
    return tr


# ====================================================================== THE STAR (15 s), into Starfire
def enter3_compose(tr, t0=0.0):
    a = lambda sig, t, *k: tr.add(sig, t0 + t, *k)
    a(drone(['D1', 'A1', 'D2'], 11.5, 0.16, 0.4), 0.0, 0, 1, 0.5)
    for k in range(5):                                                  # (it reaches: the choir a semitone higher each time)
        r = m('D3') + k
        a(hive([r, r + 7, r + 12], 1.25, 0.08 + 0.012 * k, 'u' if k < 2 else 'o', 'a', 0.4, 0.3), 0.2 + k * 1.0, 0, 1, 0.65)
    a(ther_line([('D5', 1.0), ('Eb5', 1.0), ('E5', 1.0), ('F5', 1.0), ('F#5', 1.0), ('G5', 1.0)], 1.0, 0.22, port=0.25, depth=0.015, dip=0.0), 0.2, 0.1, 1, 0.6)
    for k in range(5): a(ekick(0.35 + 0.05 * k, 7), 0.2 + k * 1.0, 0, 1, 0.1)
    # the star's fire pours through the glass
    a(flare(4.5, 0.3, 0.75), 5.0, 0, 1, 0.45)
    sw = lambda sig, a0, a1: sig * np.linspace(a0, a1, len(sig))
    a(sw(horn(['D3', 'A3', 'D4', 'F4'], 2.0, 0.14, 2400, 600, 0.6), 0.4, 1.0), 5.0, -0.1, 1, 0.45)
    a(sw(horn(['Bb2', 'F3', 'Bb3', 'D4'], 1.0, 0.16, 2800, 600, 0.2), 0.7, 1.0), 7.0, -0.1, 1, 0.45)
    a(sw(horn(['A2', 'E3', 'A3', 'C#4', 'Bb4'], 1.2, 0.18, 3200, 700, 0.2), 0.8, 1.1), 8.0, -0.1, 1, 0.45)
    a(sw(hive(['D4', 'A4', 'D5', 'F5'], 4.2, 0.12, 'a', None, 1.5, 0.4), 0.5, 1.0), 5.0, 0.1, 1, 0.6)
    for i in range(14): a(timp_like(55, 0.08 + 0.02 * i), 6.0 + i * 0.22, (-0.2, 0.2)[i % 2], 1, 0.35)
    # its skin cracks with light
    g = np.random.default_rng(3300)
    for k in range(10): a(sbell(m('D6') + int(g.choice([0, 3, 7, 10, 12, 15, 19])), 1.6, 0.06), 9.0 + 0.2 * k, g.uniform(-0.8, 0.8), 1, 0.7)
    for k in range(5): a(glass(m('A6') + int(g.integers(0, 6)), 0.8, 0.06), 9.2 + 0.3 * k, g.uniform(-0.7, 0.7), 1, 0.6)
    a(hive(['D6', 'Eb6', 'A6', 'Ab6'], 1.8, 0.07, 'i', 'e', 0.2, 0.6, gate=0.5, rate=12), 9.4, 0, 1, 0.55)
    # STARFIRE ignites
    impact(tr if t0 == 0 else _Shift(tr, t0), 11.0, 1.0)
    a(flare(2.0, 0.2, 0.15), 11.0, 0.2, 1, 0.4)
    beat = 60 / SF_BPM
    for i in range(16):                                                 # (a double-kick roll, quickening, the snare joining)
        t = 11.6 + 3.4 * (1 - (1 - i / 16) ** 1.4)
        a(ekick(0.35 + 0.03 * i, 10, 140, 46), t, 0, 1, 0.06)
    for i in range(20): a(esnare(0.06 + 0.02 * i), 12.3 + i * beat / 2.5, 0.05, 1, 0.35)
    a(edge(riser(3.0, 0.3)), 12.0, 0, 1, 0.35); a(suck(1.6, 0.4), 13.4, 0, 1, 0.3)
    a(stab(['A2', 'C#3', 'E3', 'G3', 'Bb3'], 0.4, 0.14), 15.0 - beat, 0, 1, 0.3)


class _Shift:
    def __init__(self, tr, t0): self.tr, self.t0 = tr, t0
    def add(self, s, t, *k): self.tr.add(s, self.t0 + t, *k)


def timp_like(f, amp):
    return tom(f, amp, 5, 0.3)


def enter3():
    tr = Track('vexis_enter3', 60, 18, beats=1)
    enter3_compose(tr)
    return tr


# ====================================================================== THE UNLINKING (30 s, once, under the fall's cinematic)
# ONE: the one voice left - (seconds from the fall)
ONE = [(13.5, [('A4', 1.6), ('D5', 1.9)]),                                                        # "...one. I am only one."
       (17.0, [('F5', 0.8), ('E5', 0.5), ('D5', 0.7), ('C5', 0.5), ('D5', 1.0)]),                  # (it shrinks to what it was)
       (20.5, [(None, 0.2), ('D5', 0.7), ('A5', 0.9), ('B5', 0.5), ('A5', 0.4), ('F#5', 0.8)]),    # "Vexis. That was my name."
       (24.0, [(None, 0.2), ('F#5', 0.5), ('G5', 0.5), ('A5', 0.6), ('B5', 1.2)]),                # "Show me?"
       (27.0, [('A5', 1.1), ('F#5', 1.7)])]                                                        # (THE HIVE-LINK IS CUT)


def one_line(tr, t0, phrases, amp=0.15, k=0, slow=1.0, pan=0.05):
    for t, notes in phrases:
        s = ther_line([(x, d * slow) for x, d in notes], 1.0, amp, port=0.16, vib=5.4, depth=0.017, legato=0.98, k=k, bright=0.1, dip=0.1)
        tr.add(s, t0 + t, pan, 1, 0.65)
        tr.add(lp(s, 2000), t0 + t + 0.42, -0.5, 0.25, 0.8)


def unlink_compose(tr, t0=0.0):
    a = lambda sig, t, *k: tr.add(sig, t0 + t, *k)
    # ---- the hive SCREAMS: eight throats on a cluster, each with its implant's moment to burn out
    burn = [1.5 + 0.9 * k for k in range(8)]
    voices = ['Eb5', 'A4', 'D5', 'Ab4', 'Eb4', 'D4', 'A3', 'D3']
    for k, (x, tb) in enumerate(zip(voices, burn)):
        a(hive_voice(x, tb + 1.2, 0.07, 'a', tb, 5 + k, 'u', 0.9, 0.03), 0.0, (-0.8 + 0.23 * k), 1, 0.55)
    g = np.random.default_rng(3400)
    gate = np.ones(int(9.0 * SR)); t = 0.6                              # (broken: the scream stuttering)
    while t < 8.5:
        d = g.uniform(0.04, 0.12); gate[int(t * SR):int((t + d) * SR)] = 0.15; t += d + g.uniform(0.15, 0.6)
    noise_bed = hp(R.noise(len(gate)), 2500) * 0.02 * smooth(gate, 0.01) * np.exp(-np.arange(len(gate)) / SR * 0.3)
    a(noise_bed, 0.0, 0, 1, 0.5)
    a(stab(['D3', 'Eb3', 'A3', 'D4', 'Ab4'], 0.8, 0.2), 0.0, 0, 1, 0.45); a(boom(0.5, 80, 26, 2.0), 0.0, 0, 1, 0.4)
    # ---- it calls him: "VEXIS." "VEXIS. RESPOND." "VEXIS VEXIS VEXIS VEX"
    ve = lambda t, dur, amp: (a(syll(['D4', 'A4', 'Eb5'], dur * 0.45, amp, 'e', 'e'), t, 0, 1, 0.5),
                              a(syll(['D4', 'A4', 'Eb5'], dur * 0.55, amp * 0.9, 'i', 'i'), t + dur * 0.45, 0, 1, 0.5))
    ve(1.0, 0.5, 0.12)
    ve(2.2, 0.45, 0.12); a(syll(['A3', 'D4', 'Ab4'], 0.18, 0.1, 'e', 'e'), 2.75, 0, 1, 0.5); a(syll(['A3', 'D4', 'Ab4'], 0.3, 0.1, 'o', 'u'), 2.95, 0, 1, 0.5)
    for k in range(4): ve(3.5 + 0.34 * k, 0.32 - 0.03 * k, 0.11 - 0.012 * k)
    a(syll(['D4', 'A4', 'Eb5'], 0.09, 0.07, 'e', 'e'), 4.86, 0, 1, 0.5)
    # ---- the implants burn out, one after another
    for k, tb in enumerate(burn):
        a(zap(0.08, 3800 - 200 * k, 200, 0.5), tb, (-0.6 + 0.17 * k), 1, 0.5)
        a(clank(0.12, 2200 + 120 * k, 0.5, 3410 + k), tb + 0.02, (0.5 - 0.15 * k), 1, 0.5)
    # ---- the machine powering down: the sequencer slowing, sinking, closing
    t, i = 0.0, 0
    while t < 8.6:
        u = t / 8.6
        a(mono(m('D2') - 7 * u ** 1.5, 0.12 + 0.2 * u, 0.1 * (1 - u) ** 0.7, 'saw', 1200 * (1 - u) + 120, 900 * (1 - u), 14, 2.4, 0.006, 0.5), t, 0, 1, 0.2)
        t += 0.12 + 0.55 * u ** 1.6; i += 1
    a(drop('D1', 'D0', 8.0, 0.3), 0.5, 0, 1, 0.08)
    a(drone(['D1', 'D2'], 8.6, 0.14, 0.5), 0.0, 0, 1, 0.5)
    # (SILENCE at 9 s - every sound above has ended)
    # ---- a breath; a single faint harmonic
    a(lp(R.noise(int(4.0 * SR)), 900) * 0.012 * np.sin(np.pi * np.arange(int(4.0 * SR)) / (4.0 * SR)), 9.4, 0, 1, 0.8)
    a(ther_line([('D6', 2.0)], 1.0, 0.035, port=0.1, depth=0.006, dip=0.0), 11.0, 0.3, 1, 0.85)
    # ---- ONE: the theremin, alone, then a soft pad under it, turning to D major
    one_line(tr, t0, ONE)
    pads = [(17.0, ['Bb2', 'D3', 'F3', 'A3'], 1.8), (18.8, ['C3', 'E3', 'G3', 'D4'], 1.8), (20.5, ['D3', 'F#3', 'A3', 'B3'], 3.6),
            (24.0, ['G2', 'D3', 'F#3', 'B3', 'A4'], 3.1), (27.0, ['D3', 'A3', 'D4', 'F#4', 'E4'], 3.0)]
    for t, notes, d in pads:
        last = t >= 27
        a(apad(notes, d + (0.4 if not last else 0.0), 0.045, 900, 0.7 if t > 17 else 1.4, 0.6 if not last else 2.4, 3, 0.006, 0.1, 0.2, 0.8, 'tri'), t, 0, 1, 0.65)
    a(sub808(m('D1'), 6.0, 0.06), 20.5, 0, 1, 0.1); a(sub808(m('G0'), 3.0, 0.05), 24.0, 0, 1, 0.1); a(sub808(m('D1'), 2.8, 0.06), 27.0, 0, 1, 0.1)
    a(sbell('A5', 3.0, 0.045), 27.0, 0.3, 1, 0.7); a(sbell('D6', 2.6, 0.035), 27.4, -0.3, 1, 0.75)
    for k, x in enumerate(('D5', 'F#5', 'A5', 'D6', 'E6')):             # (a music-box arpeggio: hope)
        a(sbell(x, 1.6, 0.02), 27.8 + 0.22 * k, (-0.4, 0.4)[k % 2], 1, 0.7)


def unlink():
    tr = Track('vexis_unlink', 60, 33, beats=1)
    unlink_compose(tr)
    return tr


# ====================================================================== THE QUIET AFTER (ar_after, 36 s, once)
def after():
    tr = Track('ar_after', 60, 40, beats=1)
    slow = 1.35
    phrases = [(1.5, ONE[0][1]), (6.4, ONE[1][1]), (11.4, ONE[2][1]), (16.6, ONE[3][1]), (21.4, ONE[4][1] + [('E5', 1.0), ('D5', 2.6)])]
    one_line(tr, 0.0, [(t, notes) for t, notes in phrases], 0.22, 0, slow, 0.0)
    pads = [(0.0, ['D3', 'A3', 'D4', 'E4'], 6.4), (6.4, ['Bb2', 'D3', 'F3', 'A3'], 2.5), (8.9, ['C3', 'E3', 'G3', 'D4'], 2.5),
            (11.4, ['D3', 'F#3', 'A3', 'B3'], 5.2), (16.6, ['G2', 'D3', 'F#3', 'B3', 'A4'], 4.8), (21.4, ['D3', 'A3', 'D4', 'F#4', 'E4'], 12.0)]
    for t, notes, d in pads:
        last = t > 21
        tr.add(apad(notes, d + (0.6 if not last else 0.0), 0.08, 1000, 1.2, 0.8 if not last else 6.0, 3, 0.006, 0.08, 0.2, 0.8, 'tri'), t, 0, 1, 0.65)
        tr.add(sub808(m(notes[0]) - 12, d, 0.09), t, 0, 1, 0.1)
        box = [m(x) + 24 for x in notes[:3]]
        k = 0; tt = t + 0.4
        while tt < t + d - 0.3 and tt < 33.0:                          # (the music box, slowly)
            tr.add(sbell(box[(0, 1, 2, 1)[k % 4]], 1.5, 0.022), tt, (-0.4, 0.4)[k % 2], 1, 0.7); k += 1; tt += 0.75
    tr.add(sbell('D6', 4.0, 0.05), 29.0, 0.2, 1, 0.75)
    tr.add(gaze('A6', 8.0, 0.012), 24.0, -0.3, 1, 0.85)
    return tr


# ====================================================================== THE RECORD: the fight condensed, the Unlinking for an ending
DISC_WF = [(0, 16)]
DISC_HL = [(0, 16)]
DISC_SF = [(0, 8), (48, 72)]


def disc():
    plan, t = [], 0.0
    plan.append(('intro', t)); t += 20.0
    for b0, b1 in DISC_WF: plan.append(('wf', b0, b1, t)); t += (b1 - b0) * 240 / WF_BPM
    plan.append(('enter2', t)); t += 14.0
    for b0, b1 in DISC_HL: plan.append(('hl', b0, b1, t)); t += (b1 - b0) * 240 / HL_BPM
    plan.append(('enter3', t)); t += 15.0
    for b0, b1 in DISC_SF: plan.append(('sf', b0, b1, t)); t += (b1 - b0) * 240 / SF_BPM
    plan.append(('unlink', t)); t += 30.0
    secs = int(np.ceil(t + 1.0)); secs += (4 - secs % 4) % 4
    tr = Track('vexis_disc', 60, secs // 4)
    for p in plan:
        kind = p[0]
        if kind == 'intro': intro_compose(tr, p[1]); continue
        if kind == 'enter2': enter2_compose(_Clip(tr, p[1], 14.0), 0.0); continue
        if kind == 'enter3': enter3_compose(_Clip(tr, p[1], 15.0), 0.0); continue
        if kind == 'unlink': unlink_compose(tr, p[1]); continue
        _, b0, b1, t0 = p
        bpm, fn = {'wf': (WF_BPM, wf_compose), 'hl': (HL_BPM, hl_compose), 'sf': (SF_BPM, sf_compose)}[kind]
        fn(View(tr, bpm, 4, t0, (b0, b1)))
    tr.disc_seconds = secs
    return tr


class _Clip:
    """a sting written into a record at t0, cut off where the next part begins (its riser's last moment faded)"""
    def __init__(self, tr, t0, span): self.tr, self.t0, self.span = tr, t0, span
    def add(self, s, t, *k):
        if t >= self.span: return
        n = int((self.span - t) * SR)
        if n < len(s):
            s = s[:n].copy(); f = min(n, int(0.03 * SR)); s[-f:] *= np.linspace(1, 0, f)
        self.tr.add(s, self.t0 + t, *k)


# ====================================================================== saving
def save_loop(tr, room, level):
    _guarded(render(tr, room, level), os.path.join(VENDOR, f'boss_{tr.name}.ogg'), 0)


def save_cut(tr, secs, room=2.4, level=0.25, fade=0.03, out=None, fade_in=0.0):
    """played once: rendered with spare time after it (so no tail wraps round to its start), cut at exactly `secs`"""
    st = render(tr, room, level)
    k = int(round(secs * SR)); st = st[:, :k].copy()
    f = int(fade * SR); st[:, -f:] *= np.linspace(1, 0, f)
    if fade_in: j = int(fade_in * SR); st[:, :j] *= np.linspace(0, 1, j)
    _guarded(st, out or os.path.join(VENDOR, f'boss_{tr.name}.ogg'), 4)


def save_disc(tr, name, room=2.4):
    from sovereign_music import save_disc as _sd
    _sd(tr, name, room)


def check(names=('boss_vexis_intro', 'boss_vexis1', 'boss_vexis_enter2', 'boss_vexis2', 'boss_vexis_enter3', 'boss_vexis3', 'boss_vexis_unlink',
                 'ar_after', 'disc_vexis')):
    from sovereign_music import check as _c
    _c(names)


if __name__ == '__main__':
    what = sys.argv[1:] or ['p1', 'p2', 'p3', 'intro', 'enter2', 'enter3', 'unlink', 'after', 'disc', 'check']
    if 'p1' in what: save_loop(seeded(21, p1), 2.6, 0.23)
    if 'p2' in what: save_loop(seeded(22, p2), 3.2, 0.22)
    if 'p3' in what: save_loop(seeded(23, p3), 2.4, 0.285)
    if 'intro' in what: save_cut(seeded(24, intro), 20, 2.6, 0.23)
    if 'enter2' in what: save_cut(seeded(25, enter2), 14, 2.6, 0.28)
    if 'enter3' in what: save_cut(seeded(26, enter3), 15, 2.6, 0.28)
    if 'unlink' in what: save_cut(seeded(27, unlink), 30, 3.2, 0.2, 1.5)
    if 'after' in what: save_cut(seeded(28, after), 36, 3.4, 0.14, 3.0, os.path.join(VENDOR, 'ar_after.ogg'), 1.0)
    if 'disc' in what:
        d = seeded(29, disc); assert 170 <= d.seconds <= 200, d.seconds
        save_disc(d, 'vexis', 2.6)
    if 'check' in what: check()
