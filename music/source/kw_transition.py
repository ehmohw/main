"""Democratus -> KillerWatt: 5 bars at Democratus's 150 BPM (8 s). The storm breaks over him: a great strike, his hook's
opening on the violin one last time under it, the choir and waterphone swelling, then a roll and a riser into KillerWatt."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from killerwatt5 import Track, riser, tom, crash, render, _guarded, seeded, choir, violin, waterphone, ther, TR, HOOK, M, sub808
from storm import strike, thunder, rain, spark

def compose():
    tr = Track('kw_trans', 150, 5)
    assert round(tr.seconds) == 8
    bl = tr.beat * 4
    tr.add(strike(0.7, 7), 0, 0, 1, 0.4); tr.add(crash(0.5, 3.0), 0, 0.3, 1, 0.55)
    tr.add(sub808(M('D1'), bl * 2, 0.25), 0, 0, 1, 0.05)
    violin(tr, tr.at(0, 0.5), HOOK[:10], 0.28, 0.0, drive=2.0)
    tr.add(choir(['D3', 'A3', 'D4', 'F4'], bl * 3, 0.09, 1.5, 'u'), 0, 0, 1, 0.8)
    tr.add(waterphone('D3', bl * 3, 0.3, bend=2.0, seed=3), tr.at(1), 0.4, 1, 0.6)
    tr.add(rain(bl * 4.5, 0.08, 2), 0, 0, 1, 0.4)
    tr.add(thunder(0.5, 4.0, 11), tr.at(2), -0.3, 1, 0.5)
    ther(tr, tr.at(2), [('D4', 4), ('C5', 4)], 0.2, -0.3, 0.5, port=0.4)
    for i in range(24): tr.add(tom(170 - 4 * i, 0.12 + 0.006 * i, 8, 0.2), tr.at(3, i * TR), -0.4 + 0.035 * i, 1, 0.25)
    for b in (3, 4): tr.add(spark(0.2, b), tr.at(b, 2), 0.5, 1, 0.3)
    tr.add(riser(bl * 2, 0.15), tr.at(3), 0, 1, 0.4)
    return tr

_guarded(render(seeded(3, compose), 2.4, 0.28), sys.argv[1], 6)
