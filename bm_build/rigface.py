"""2.97a: FOLLOWERS WHOSE SHAPE IS A MODEL - the glue rigpet needs for a rig whose parts change model from pose to pose (the Ink
Blot's shapes, the Cursor's pointer forms, the Speech Bubble's shout and its words, the Doodle Dragon's fire, the Pale Dryad's
glowing mushrooms) and whose face may sit on a part that isn't called 'head' (the Eraser's face is on its body, the Bubble's on
a decal of its own).

  art(A)            the art seen without its faces: a pose's model is its shape, never its face (the face is the mood's -
                    phase95's custom_model_data string - so a swap never fights the expression).
  swapping(A)       the parts whose model changes across the poses: what Cfg.SWAP should be.
  setup(C, part)    after RP.register: the mood's faces on that part (FX.FOLK); the shape swaps keep the wardrobe's look
                    (Cfg.POSE_EXTRA re-dresses a swapped part).
  faces(C, part, R) (rp) every model the face part can wear gets an item definition picking the mood's face model."""
import phase95 as FX


class _Faceless:
    """the art module, its model names taken without the pose's face"""
    def __init__(self, A):
        self._A = A

    def __getattr__(self, k):
        return getattr(self._A, k)

    def model_name(self, p, pose, suffix=''):
        return self._A.model_name(p, {k: v for k, v in pose.items() if k != '_face'}, suffix)


def art(A):
    return _Faceless(A)


def swapping(A):
    """the parts whose (faceless) model differs between poses"""
    out = []
    for p in A.PARTS:
        names = {A.model_name(p, {k: v for k, v in pz.items() if k != '_face'}) for pz in A.POSES.values()}
        if len(names) > 1:
            out.append(p)
    return tuple(out)


def setup(C, part):
    """(after RP.register(C)) the mood's faces go on `part`; every pose that swaps a model re-dresses it in the look"""
    if part != 'head':
        h = FX.FOLK[C.W]
        FX.FOLK[C.W] = (h[0], h[1], f'type=minecraft:item_display,tag=bm.{C.ab}p,tag=bm.{C.ab}p_{part},tag=bm.{C.ab}p_pet,tag=!bm.{C.ab}fade') + h[3:]
    swaps, ab = C.SWAP, C.ab

    def extra(name, psel):
        if not swaps:
            return []
        return ['scoreboard players set #wk bm.rng 0', f'execute on owner run scoreboard players operation #wk bm.rng = @s bm.cos{ab}'] + \
               [f'execute if score #wk bm.rng matches 1.. as {psel(p)} run function bm:p138/sfx' for p in swaps]
    C.POSE_EXTRA = staticmethod(extra)


def faces(C, part, R):
    """(rp) the item definitions of the face part's models: each picks the mood's face (Cfg.FACE) - one per shape it can take"""
    A = C.A._A if isinstance(C.A, _Faceless) else C.A
    names = set(A.models())
    bases = {}
    for pz in A.POSES.values():
        bare = {k: v for k, v in pz.items() if k != '_face'}
        base = A.model_name(part, bare)
        if base not in names:
            continue
        cases = bases.setdefault(base, {})
        for e in C.EXPR:
            f = C.FACE.get(e)
            if not f:
                continue
            m = A.model_name(part, dict(bare, _face=f))
            if m in names and m != base:
                cases[e] = m

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for base, cases in bases.items():
            R2.wj(f'assets/bm/items/{base}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cases.items()], 'fallback': mdl(base)}})
    R.POST.append(post)                     # (after rigpet's - before phase138 copies the item definitions for the looks)
