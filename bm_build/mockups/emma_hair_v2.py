"""EMMA'S 3D HAIR, REVISED FROM HER FRONTAL ART (mockup - not in the pack): her shipped head (phase57_art) with the hair rebuilt
from the owner's front view of her:
  a big swept bang - from the part on her left, across her brow, stepping lower toward her right and flipping out past her face;
  a tuft standing up on top, toward her right; more volume on the crown;
  side locks down to her jaw, each curling out at the end;
  the ponytail high on her left, sweeping out and hanging beside her head to her shoulder, ragged at the end;
  a purple bow at the ponytail's root, one loop standing up and one out to the side.
Everything else is her shipped model. models() gives the shipped parts as 'em_*' and the revision as 'ev_*' (for a
before/after sheet)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import phase57_art as EM
from phase57_art import _el, PIVOT, _fabric

RIG_SCALE, PARTS, PIVOT, part_xf, POSES = EM.RIG_SCALE, EM.PARTS, EM.PIVOT, EM.part_xf, EM.POSES


def textures():
    T = EM.textures()
    T['ev_bow'] = _fabric('#b45cc8', 40, folds=1, weave=False, top=1.12)
    T['ev_bowdk'] = _fabric('#8a3aa0', 41, folds=1, weave=False)
    return T


def head(face):
    pv = PIVOT['head']
    hr = lambda fr, to, rot=None: _el(fr, to, 'em2_hair', pv, rot)
    els = [_el((-4.5, 24.0, -4.0), (4.5, 32.0, 4.0), face, pv, uv={'north': [0, 0, 9, 8]}),
           _el((4.5, 26.2, -0.6), (5.0, 28.0, 0.6), 'em2_cheek', pv), _el((-5.0, 26.2, -0.6), (-4.5, 28.0, 0.6), 'em2_cheek', pv)]
    for f in els[0]['faces']:
        if f != 'north': els[0]['faces'][f]['texture'] = '#em2_skin'
    # crown (fuller), back, sides
    els += [hr((-4.9, 30.6, -4.4), (4.9, 33.4, 4.4)), hr((-4.9, 25.0, 3.4), (4.9, 30.8, 4.6)),
            hr((4.5, 25.6, -2.4), (5.2, 30.8, 4.4)), hr((-5.2, 25.6, -2.4), (-4.5, 30.8, 4.4))]
    # the swept bang: from the part (her left, -x) across, stepping down toward her right and flipping out past her face
    els += [hr((-4.9, 30.6, -4.7), (4.9, 31.6, -4.0)),
            hr((-4.9, 30.2, -4.75), (-2.8, 30.7, -4.0)),                                        # (high at the part)
            hr((-2.9, 29.9, -4.85), (0.6, 30.7, -4.0)),
            hr((0.4, 29.5, -5.0), (3.2, 30.7, -4.0)),
            hr((3.0, 29.0, -5.1), (5.0, 30.7, -4.0)),                                           # (lowest and fullest at her right)
            hr((-1.5, 29.2, -4.75), (-0.5, 30.0, -4.05)),                                       # (a strand down onto her brow)
            hr((4.6, 29.4, -5.1), (7.4, 30.8, -3.0), ('z', 30, (4.8, 30.0, -4.0))),             # (the flip, out past her face)
            hr((2.4, 32.9, -3.8), (3.8, 34.6, -2.2), ('z', -22.5, (3.1, 33.0, -3.0)))]          # (the tuft)
    # side locks to her jaw, each curling out at the end
    for sx in (1, -1):
        x = lambda a, b: tuple(sorted((sx * a, sx * b)))
        (a0, a1), (b0, b1), (c0, c1) = x(4.0, 5.6), x(5.0, 6.6), x(5.9, 6.8)
        els += [hr((a0, 24.4, -4.3), (a1, 30.2, -1.4)), hr((b0, 23.6, -4.1), (b1, 24.7, -1.8)), hr((c0, 24.4, -4.0), (c1, 25.8, -1.9))]
    # the ponytail: high on her left, out and down beside her head, ragged at the end
    els += [hr((-4.4, 31.2, -0.8), (-2.2, 33.6, 2.0)),
            hr((-9.6, 30.2, -0.4), (-4.0, 32.6, 2.4), ('z', 12, (-4.0, 31.4, 1.0))),
            hr((-10.8, 28.6, 0.0), (-9.0, 29.8, 2.0), ('z', -30, (-9.4, 29.2, 1.0))),
            hr((-9.8, 23.4, -0.2), (-6.6, 30.4, 2.2)),
            hr((-9.4, 21.2, 0.0), (-7.0, 23.6, 2.0)),
            hr((-9.2, 20.2, 0.2), (-8.2, 21.4, 1.8)), hr((-7.8, 20.6, 0.2), (-7.1, 21.4, 1.8))]
    # the bow at its root
    els += [_el((-4.3, 32.8, -0.5), (-3.1, 36.0, 0.5), 'ev_bow', pv, ('z', 18, (-3.7, 33.0, 0))),
            _el((-7.0, 32.4, -0.5), (-4.0, 33.8, 0.5), 'ev_bow', pv, ('z', -22.5, (-4.0, 33.1, 0))),
            _el((-4.4, 32.4, -0.7), (-3.0, 33.6, 0.7), 'ev_bowdk', pv)]
    return els


def models():
    M = EM.models()
    out = dict(M)
    TX = {k: f'bm:block/{k}' for k in textures()}
    for n, v in M.items():
        if n.startswith('em_'): out['ev_' + n[3:]] = v
    els = head('em2_face')
    used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
    out['ev_head'] = ({k: TX[k] for k in used}, els)
    return out
