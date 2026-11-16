"""DEMOCRATUS - battle theme: killerwatt5.py's composition (take six) with his electricity woven in: a buzz-stab figure on
the triplet pickups, sparks on the accents, crackle under the strings, arcs, and a buzzing doubling of the hook's long notes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import killerwatt5 as K
from killerwatt5 import M, TR, HOOK, P_HOOK, P_CLIMB, triad, render, _guarded, seeded
from killerwatt_music import arc
from storm import spark, buzz, crackle

PLAN = [('war', P_HOOK, 0), ('hook', P_HOOK, 0), ('both', P_HOOK, 0), ('climb', P_CLIMB, 0), ('dread', P_HOOK, 0),
        ('surge', P_HOOK, 0), ('hook', P_HOOK, 2), ('climb', P_CLIMB, 2), ('all', P_HOOK, 0)]


def compose():
    tr = K.compose()
    bt = tr.beat; bl = bt * 4
    for s, (kind, prog, k) in enumerate(PLAN):
        for b in range(8):
            bar = s * 8 + b; c = triad(prog[b], k, 4)
            f = 440 * 2 ** ((c[0] - 69) / 12)
            for x in (3 + TR, 3 + 2 * TR):                                   # the current: buzz stabs on the pickups
                tr.add(buzz(f, bt * 0.25, 0.07), tr.at(bar, x), 0.45, 1, 0.2)
            if b % 2 == 1 or kind in ('surge', 'all'):
                tr.add(buzz(f * 2, bt * 0.3, 0.06), tr.at(bar, 1 + 2 * TR), -0.45, 1, 0.2)
            tr.add(spark(0.16, bar), tr.at(bar, 2), (-0.5, 0.5)[b % 2], 1, 0.35)
            if b % 4 == 3: tr.add(arc(0.2, 0.9, 200 + bar), tr.at(bar, 3), 0.5, 1, 0.4)
        pass
        if kind in ('hook', 'all'):                                          # long hook notes hum with current
            t = tr.at(s * 8)
            for x, d in HOOK:
                if x is not None and d >= 1:
                    tr.add(buzz(440 * 2 ** ((M(x) + k - 12 - 69) / 12), d * bt * 0.9, 0.035), t, -0.3, 1, 0.3)
                t += d * bt
    for b in range(3):
        tr.add(spark(0.2, 700 + b), tr.at(72 + b, 0), 0.4, 1, 0.3)
    return tr


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'democratus_battle.ogg'
    _guarded(render(seeded(53, compose), 2.4, 0.28), out, 6)
