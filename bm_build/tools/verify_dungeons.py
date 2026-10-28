"""Run the Phase 2 layout verifier (p2/verify.py) on every dungeon (2.14).

It proves, on the built templates: every puzzle element is wired and reachable once the gates before it are open, nothing
later is reachable early (no skipping), hidden rooms are sealed until their secret door opens, pressure-plate paths have a
safe route and can't be bypassed, the altar/arena open only after the last gate, and stairs don't bump heads.

    python3 tools/verify_dungeons.py            # all seven (the Hollow Throne, a 152-block citadel in open void, takes a few minutes)
    python3 tools/verify_dungeons.py brood hex
    python3 tools/verify_dungeons.py under      # the Undercrown (2.98: built on its own, not in the list above by default)
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import p2
from p2.verify import verify

# surface dungeons (and the Hollow's open void) are entered from open air; underground/sea ones only through their door
OUTSIDE = {'frost': 'air', 'hex': 'air', 'keep': 'air', 'hollow': 'void', 'brood': 'solid', 'tide': 'solid', 'lucky': 'solid',
           'under': 'solid'}      # 2.98: the Undercrown is not in p2.builds() - it is built on its own, cut into the Nether's rock

if __name__ == '__main__':
    flags = [a for a in sys.argv[1:] if a.startswith('-')]
    want = [a for a in sys.argv[1:] if not a.startswith('-')] or [d for d in OUTSIDE if d != 'under']
    bad = 0
    for d in want:
        t = time.time()
        if d == 'under':
            from p2.dungeons import undercrown
            B = undercrown.build()
        else:
            B = p2.builds()[d]
        errs, notes = verify(B, outside=OUTSIDE[d])
        print(f'{d}: {len(errs)} errors ({time.time() - t:.0f}s)', flush=True)
        for e in errs: print('   ', e, flush=True)
        if '-v' in flags:
            for n_ in notes: print('    .', n_)
        bad += len(errs)
    sys.exit(1 if bad else 0)
