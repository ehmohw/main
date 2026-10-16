"""Writes p115.json - the 2.72 rooms' data that t115a plays against (the brews, the chasms, the lanes, the bells, the
Minecart Run's targets and buttons, the Pipes' solutions), straight from p115data. Run it again whenever p115data changes:
    python3 tools/bots/mk_p115.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
import p115data as PD

pair = lambda L: [[it, pid] for (_nm, it, pid) in L]
data = {'brewA': {t: pair(L) for t, L in PD.BREW_A.items()}, 'brewB': {t: list(L) for t, L in PD.BREW_B.items()},
        'brewC': {t: pair(L) for t, L in PD.BREW_C.items()},
        'chasms': [[[list(p) for p in isl], h] for isl, h in PD.CHASMS], 'lanes': list(PD.LANES),
        'bells': [list(b) for b in PD.BELLS], 'targets': [list(t) for t in PD.TARGETS_A], 'buttons': [list(b) for b in PD.BUTTONS_C]}
# the Pipes: [start row, end row, the solution {"r,c": [shape, turns]}] - one per puzzle the room can draw (bm.gvc)
sol = lambda full: {f'{r},{c}': list(v) for (r, c), v in full.items()}
for k, L in (('pipeA', PD.PIPE_A), ('pipeB', PD.PIPE_B), ('pipeC', PD.PIPE_C)):
    data[k] = [[P[0], P[1], sol(P[3])] for P in L]
json.dump(data, open(os.path.join(HERE, 'p115.json'), 'w'), indent=1)
print('p115.json written')
