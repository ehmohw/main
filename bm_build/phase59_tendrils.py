"""2.42: KillerWatt's four back tendrils - two blade segments each (a sharp electric elbow), their poses.

Directions are in the display frame: your front is +z, your left +x, up +y. The base segment turns at its mount on your
back; the tip segment hangs from the base's end. When one lunges it climbs past the side of your head (or out past your
arm, for a lower one) and only then strikes forward - so it never passes through you (scratchpad tclip.py checks it)."""
L1_UNITS, L2_UNITS, SCALE = 12, 17, 0.95


def _mirror(v): return (-v[0], v[1], v[2])


LEFT = {
    'u': ((0.18, 1.30, -0.26), {'idle': ((0.70, 0.65, -0.30), (0.95, 0.10, -0.30)),
                                'sway_a': ((0.74, 0.60, -0.28), (0.92, 0.25, -0.30)), 'sway_b': ((0.66, 0.70, -0.32), (0.97, -0.05, -0.25)),
                                'mid': ((0.72, 0.68, -0.14), (0.62, 0.55, 0.55)), 'lunge': ((0.70, 0.71, 0.05), (-0.15, -0.10, 0.98))}),
    'l': ((0.16, 1.02, -0.26), {'idle': ((0.80, -0.05, -0.60), (0.30, -0.90, -0.30)),
                                'sway_a': ((0.84, 0.05, -0.54), (0.40, -0.85, -0.35)), 'sway_b': ((0.76, -0.12, -0.64), (0.22, -0.93, -0.28)),
                                'mid': ((0.93, 0.15, -0.34), (0.62, -0.10, 0.78)), 'lunge': ((0.95, 0.28, 0.06), (-0.08, 0.05, 0.99))}),
}
TENDRILS = {}
for _row, (_m, _p) in LEFT.items():
    TENDRILS[_row + 'l'] = (_m, _p)
    TENDRILS[_row + 'r'] = ((-_m[0], _m[1], _m[2]), {k: (_mirror(b), _mirror(t)) for k, (b, t) in _p.items()})
