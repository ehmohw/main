"""FULLER - the approved Democratus, KillerWatt and Emma themes, note for note, with more body around them.

Nothing in the approved arrangements is changed or removed: each piece is composed exactly as it was approved (same code,
same random seed), then layers are added on top:

  DEMOCRATUS  a string section holding each chord, cellos and basses on the roots, a second violin doubling the lead
              (slightly detuned, the other side) so it sings wider, horns warming the climbs and the finale, a deeper hall
  KILLERWATT  a string section, low strings on the roots, a low choir under the existing one, the lead guitar
              double-tracked on the other side, a deeper hall
  EMMA        soft strings through every section (a second, higher layer where there were already strings), a cello on
              the roots, a harp touching each melody note, a gentle violin under the last statement, a deeper hall

Added sustained layers sit out the one bar where the hook holds C# over a G chord, so they don't thicken that rub.

    python3 fuller.py democratus|killerwatt|emma OUT.ogg
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sovereign_music import render, _guarded, seeded, boom
from armada_music import apad, addc, M
from divine_music import horns, choir
from voices import cello_line
from killerwatt_music import violin_line

TR = 1 / 3


def strings(tr, bar, notes, nbars=1, amp=0.035, cut=1600, pan=0.0, wet=0.7):
    """a string section holding a chord: five detuned bowed voices a note, a slow swell"""
    tr.add(apad(notes, tr.beat * 4 * nbars * 1.05, amp, cut, 0.6, 1.2, voices=5, det=0.005, lfo=0.11, depth=0.12, q=0.9),
           tr.at(bar), pan, 1, wet)


def low_strings(tr, bar, root, nbars=1, amp=0.11, clean=False):
    """cellos and basses on the root, an octave apart"""
    notes = [(root, 4 * nbars)]
    s = cello_line(notes, tr.beat, amp, drive=0.9 if clean else 1.3, depth=0.005, legato=1.0)
    s2 = cello_line([(root - 12, 4 * nbars)], tr.beat, amp * 0.7, drive=0.9, depth=0.003, legato=1.0)
    addc(tr, s, tr.at(bar), -0.3, 1, 0.5); addc(tr, s2, tr.at(bar), 0.3, 1, 0.45)


def double(tr, t0, notes, fn, pan, k=0.08, delay=0.018, wet=0.4):
    """a second player on the same line: a hair sharp, a hair late, on the other side"""
    s = fn(notes, k)
    addc(tr, s, t0 + delay, pan, 1, wet)


# ====================================================================== DEMOCRATUS
def democratus():
    import democratus_music as D
    import killerwatt5 as K5
    tr = D.compose()                                             # the approved theme, exactly
    bt = tr.beat; bl = bt * 4
    for s, (kind, prog, k) in enumerate(D.PLAN):
        base = s * 8; t0 = tr.at(base)
        for b in range(8):
            if kind == 'war' and b < 4: continue
            bar = base + b; r = prog[b]
            if not (prog is K5.P_HOOK and b == 5):              # (the C#-over-G bar: no added sustain)
                c3 = K5.triad(r, k, 3)
                strings(tr, bar, [c3[0], c3[2], c3[1] + 12, c3[0] + 12], 1, 0.03 if kind != 'all' else 0.038)
            low_strings(tr, bar, K5.triad(r, k, 2)[0] + 12, 1, 0.12)
        lead = lambda n, kk: violin_line(n, bt, 0.15, k=kk, drive=3.0)
        if kind in ('hook', 'both', 'all'): double(tr, t0, [(x if x is None else M(x) + k, d) for x, d in K5.HOOK], lead, 0.35)
        if kind == 'climb': double(tr, t0, [(x if x is None else M(x) + k, d) for x, d in K5.CLIMB], lead, 0.35)
        if kind == 'surge': double(tr, t0, K5.SURGE, lambda n, kk: violin_line(n, bt, 0.12, k=kk, port=0.008, drive=3.5), 0.4, -0.06)
        if kind in ('climb', 'all'):
            for b in range(0, 8, 2):
                c = K5.triad(prog[b], k, 3)
                tr.add(horns([c[1], c[2]], bl * 2 * 0.95, 0.05), tr.at(base + b), 0.25, 1, 0.55)
        if kind != 'war': tr.add(boom(0.18, 70, 26, 2.0), t0, 0, 1, 0.4)
    for b, r in enumerate(('D', 'Bb', 'A')):                    # the brink
        c3 = K5.triad(r, 0, 3)
        strings(tr, 72 + b, [c3[0], c3[2], c3[1] + 12, c3[0] + 12], 1, 0.04)
        low_strings(tr, 72 + b, K5.triad(r, 0, 2)[0] + 12, 1, 0.1)
    return tr


# ====================================================================== KILLERWATT
def killerwatt():
    import killerwatt11 as K11
    import killerwatt10 as K10
    from guitar import lead_line
    tr = K11.compose()                                           # the approved theme, exactly
    bt = tr.beat; bl = bt * 4
    plan = [('storm', K10.P_HOOK, 0), ('theme', K10.P_HOOK, 0), ('climb', K10.P_CLIMB, 0), ('strike', K10.P_HOOK, 0),
            ('him', K10.P_HOOK, 0), ('key', K10.P_HOOK, 2), ('tempest', K10.P_CLIMB, 0), ('all', K10.P_HOOK, 0),
            ('again', K10.P_HOOK, 0)]
    hooky = {'storm', 'theme', 'key', 'all', 'again'}
    for s, (kind, prog, kk) in enumerate(plan):
        k = K10.KEY + kk; base = s * 8 + (4 if s > 4 else 0); t0 = tr.at(base)
        bars_ = [(b, prog[b]) for b in range(8)] if kind != 'him' else [(b, prog[b % 8]) for b in range(4, 12)]
        for b, r in bars_:
            bar = base + b
            if not (prog is K10.P_HOOK and kind != 'him' and b == 5):
                c3 = K10.triad(r, k, 3)
                strings(tr, bar, [c3[0], c3[2], c3[1] + 12, c3[0] + 12], 1, 0.03, 1900)
            low_strings(tr, bar, K10.triad(r, k, 2)[0] + 12, 1, 0.15)
            if b % 2 == 0:
                c = K10.triad(r, k, 3)
                tr.add(choir([c[0], c[2], c[0] + 12], bl * 2, 0.04, 0.3, 'u'), tr.at(bar), 0, 1, 0.7)
        gtr = lambda n, kk: lead_line(n, bt, 0.17, k=kk)
        if kind in hooky: double(tr, t0, K10.shift(K10.HOOK, k), gtr, -0.3, 0.06, 0.022, 0.35)
        if kind in ('climb', 'tempest'): double(tr, t0, K10.shift(K10.CLIMB, k), gtr, -0.3, 0.06, 0.022, 0.35)
        if kind == 'him': double(tr, tr.at(base + 4), K10.shift(K10.SURGE, k), lambda n, kk: lead_line(n, bt, 0.12, k=kk), -0.35, 0.05, 0.02)
    for b, r in enumerate(['D', 'Bb', 'A', 'D', 'Bb', 'A']):    # the eye
        c3 = K10.triad(r, K10.KEY, 3)
        strings(tr, 76 + b, [c3[0], c3[2], c3[1] + 12, c3[0] + 12], 1, 0.035, 1900)
        low_strings(tr, 76 + b, K10.triad(r, K10.KEY, 2)[0] + 12, 1, 0.1)
    return tr


# ====================================================================== EMMA
def emma():
    import emma_music as E
    tr = E.compose()                                             # the approved theme, exactly
    bt = tr.beat
    secs = [(0, [('D', 'M'), ('G', 'M'), ('D', 'M'), ('A', 'M')], 'intro', None), (4, E.P_HOOK, 'hook', E.HOOKM),
            (12, E.P_CLIMB, 'climb', E.CLIMBM), (20, E.P_HOOK, 'high', [(x + 12, d) if x else (x, d) for x, d in E.HOOKM]),
            (28, E.P_HOME, 'home', E.HOOKM)]
    for base, prog, kind, mel in secs:
        for b, (r, q) in enumerate(prog):
            bar = base + b; c = E.chord(r, q, 3)
            clash = prog in (E.P_HOOK, E.P_HOME) and b == 5
            if not clash:
                if kind in ('climb', 'high'):                  # strings already here: a second, higher layer
                    strings(tr, bar, [c[1] + 12, c[2] + 12, c[0] + 24], 1, 0.016, 2600, 0.25, 0.8)
                else:
                    strings(tr, bar, [c[0], c[2], c[1] + 12], 1, 0.022 if kind != 'intro' else 0.016, 1300, -0.1, 0.8)
            if kind != 'intro':
                s = cello_line([(c[0] - 12, 4)], bt, 0.06, drive=0.8, depth=0.004, legato=1.0)
                addc(tr, s, tr.at(bar), -0.3, 1, 0.55)
        if mel:
            t = tr.at(base)
            for i, (x, d) in enumerate(mel):                       # a harp touching each melody note
                if x is not None: tr.add(E.harp(x, 0.022, 100 + i), t, 0.35, 1, 0.65)
                t += d * bt
        if kind == 'home':
            from voices import clean_violin_line
            addc(tr, clean_violin_line(E.HOOKM, bt, 0.06), tr.at(base), 0.3, 1, 0.6)
    return tr


ROOM = {'democratus': (2.8, 0.28, 53, 0.18), 'killerwatt': (2.6, 0.27, 71, 0.28), 'emma': (3.6, 0.2, 5, 0.0)}


def low_shelf(tr, g):
    """a little more weight under 140 Hz, so the added body doesn't thin the bottom once the mix is levelled"""
    from gv_music import lp
    for name in ('L', 'R', 'wetL', 'wetR'):
        x = getattr(tr, name); setattr(tr, name, x + g * lp(x, 140))

if __name__ == '__main__':
    which, out = sys.argv[1], sys.argv[2]
    room, level, seed, shelf = ROOM[which]
    tr = seeded(seed, globals()[which])
    if shelf: low_shelf(tr, shelf)
    _guarded(render(tr, room, level), out, 6)
