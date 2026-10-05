"""Run the Phase 2 layout verifier (p2/verify.py) on every dungeon (2.14).

It proves, on the built templates: every puzzle element is wired and reachable once the gates before it are open, nothing
later is reachable early (no skipping), hidden rooms are sealed until their secret door opens, pressure-plate paths have a
safe route and can't be bypassed, the altar/arena open only after the last gate, and stairs don't bump heads.

    python3 tools/verify_dungeons.py            # all seven (the Hollow Throne, a 152-block citadel in open void, takes a few minutes)
    python3 tools/verify_dungeons.py brood hex
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import p2
from p2.verify import verify

# surface dungeons (and the Hollow's open void) are entered from open air; underground/sea ones only through their door
OUTSIDE = {'frost': 'air', 'hex': 'air', 'keep': 'air', 'hollow': 'void', 'brood': 'solid', 'tide': 'solid', 'lucky': 'solid'}

if __name__ == '__main__':
    want = sys.argv[1:] or list(OUTSIDE)
    builds = p2.builds()
    bad = 0
    for d in want:
        t = time.time()
        errs, notes = verify(builds[d], outside=OUTSIDE[d])
        print(f'{d}: {len(errs)} errors ({time.time() - t:.0f}s)', flush=True)
        for e in errs: print('   ', e, flush=True)
        bad += len(errs)
    sys.exit(1 if bad else 0)
