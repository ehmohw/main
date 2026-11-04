"""3.1: THE NEW FOLLOWERS' ART, AS THE GAME READS IT - one adapter per follower over its fol5_kit rig (glitch_pet_art.R ...), with
what the pack's machinery asks of an art module:

  rigpet / rigfol / phase134   PREFIX, RIG_SCALE, PIVOT, PARENT, PARTS, PART_K, HIDDEN, model_name, POSES, models()
  phase138 (the recolours)     textures(), RECOL_KEYS (what a look recolours, plus what only the shiny changes), LOOK_SHINY_ONLY,
                               LOOK_GILD_SKIP, SHINY_TEX (the shiny DRAWN: the art's own '_sh' set, not a recolour), LOOK_DRAWN
                               ({look: {texture: image}} - a look that is a drawn set: the Cake's flavours), OWN_SETS
  shiny                        SHINY_LOOK
  the doll                     DOLL (its chibi warp) and GROUPS (by part: phase141 turns them into model ids)
  faces                        FACE_MAP (rigpet's moods -> the art's faces), FACE_PART

models() leaves out the sets the game never wears as models: the shiny (a look, drawn - SHINY_TEX) and any drawn-look set
(LOOK_DRAWN). Each adapter is put in sys.modules as f5art_<w>, so phase138 finds it by name, as it finds every art module."""
import sys
import types
import fol5

EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')


class Art(types.ModuleType):
    def __init__(self, w, rig, face_map, look_tex, drop=('_sh',), drawn=None, gild=None, shiny=('_sh', '#3a2806', 'yellow'), doll_groups=None,
                 own_sets=None, fit_pose='idle_a', extra_poses=None):
        super().__init__(f'f5art_{w}')
        self.W, self.R = w, rig
        self.PREFIX, self.RIG_SCALE, self.PIVOT, self.PARENT, self.PARTS = rig.PREFIX, rig.RIG_SCALE, rig.PIVOT, rig.PARENT, rig.PARTS
        self.PART_K, self.POSES, self.FACES, self.FACE_PARTS = rig.PART_K, rig.POSES, rig.FACES, rig.FACE_PARTS
        self.FACE_PART = rig.FACE_PARTS[0]
        if extra_poses:
            self.POSES.update(extra_poses)
        self.FACE_MAP = dict(face_map)
        self.DROP = tuple(drop)
        self.SKINS = [''] + [s for s in rig._skins if s not in self.DROP]
        pre = rig.PREFIX
        base = [t for t in rig._tex if not any(t.endswith(s) for s in rig._skins)]
        self.BASE_TEX = base
        self.LOOK_TEX = tuple(pre + t for t in look_tex)
        sh = shiny[0]
        self.SHINY_TEX = {pre + t: (lambda im: lambda b: im)(rig._tex[t + sh]) for t in base if t + sh in rig._tex} if sh else {}
        self.LOOK_DRAWN = {}
        for k, sfx in (drawn or {}).items():
            self.LOOK_DRAWN[k] = {pre + t: rig._tex[t + sfx] for t in base if t + sfx in rig._tex}
        drawn_keys = sorted({n for d in self.LOOK_DRAWN.values() for n in d})
        self.LOOK_SHINY_ONLY = tuple(n for n in sorted(set(self.SHINY_TEX) | set(drawn_keys)) if n not in self.LOOK_TEX)
        self.RECOL_KEYS = self.LOOK_TEX + self.LOOK_SHINY_ONLY
        keep_gold = set(pre + t for t in (gild if gild is not None else look_tex))
        self.LOOK_GILD_SKIP = tuple(n for n in self.RECOL_KEYS if n not in keep_gold)
        self.SHINY_COLS = shiny
        self.OWN_SETS = dict(own_sets or {})
        self.DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
        self.GROUPS = dict(doll_groups or {})
        self.FIT = rig.fit(rig.POSES[fit_pose])

    # ---- rigpet / rigfol
    def HIDDEN(self, p, pose):
        return self.R.HIDDEN(p, pose)

    def model_name(self, p, pose=None, suffix=''):
        return self.R.model_name(p, pose, suffix)

    def models(self):
        return {n: v for n, v in self.R.models().items() if not any(n.endswith(s) for s in self.DROP)}

    # ---- phase138
    def textures(self):
        return {n: im for n, im in self.R.textures().items() if not any(n.endswith(s) for s in self.DROP if s)}

    def look_item(self, n):
        """phase138.ITEMS_OF: the models a look is copied onto - the follower's own sets (not its afterimages / effects)"""
        return n.startswith(self.PREFIX) and not any(n.endswith(s) for s in getattr(self, 'NO_LOOK', ()))

    @property
    def SHINY_LOOK(self):
        nm = fol5.SPEC[self.W].get('shiny_name', f'Shiny {fol5.SPEC[self.W]["NAME"][4:]}')
        return (nm, ('#1a1406', self.SHINY_COLS[1], '#fff0c0'), self.SHINY_COLS[2])

    def face_cases(self, sfx=''):
        """{mood: model} for the face part's item definition (rigpet's moods through FACE_MAP)"""
        out = {}
        for e in EXPR:
            f = self.FACE_MAP.get(e)
            if f and f in self.FACES:
                out[e] = f'{self.PREFIX}{self.FACE_PART}_x{f}{sfx}'
        return out


def _glitch():
    import glitch_pet_art as GA
    A = Art('glitch', GA.R, {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'},
            ('case', 'case2', 'knob'), shiny=('_sh', '#c8962a', 'yellow'),
            doll_groups=GA.DOLL_GROUPS)
    A.NO_LOOK = ('_g', '_gr', '_gc')            # (afterimages and the RGB split: never worn with a look)
    A.MOTION, A.SLICE_LAG, A.JIT_P, A.JIT_X = GA.MOTION, GA.SLICE_LAG, GA.JIT_P, GA.JIT_X
    return A


def _cake():
    import cake_pet_art as CA
    frost = ('frost', 'frost2', 'frosth')
    A = Art('cake', CA.R, {'happy': 'happy', 'surprised': 'wow', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'wow'},
            (), drop=('_sh', '_mint', '_lem', '_choc'), drawn={1: '_mint', 2: '_lem', 3: '_choc'}, gild=frost + ('cream',),
            shiny=('_sh', '#5a48b8', 'blue'), doll_groups=CA.DOLL_GROUPS)
    return A


_MADE = {}
_MAKERS = {'glitch': _glitch, 'cake': _cake}


def get(w):
    if w not in _MADE:
        a = _MAKERS[w]()
        _MADE[w] = a
        sys.modules[a.__name__] = a
    return _MADE[w]


for _w in _MAKERS:
    fol5._ARTS[_w] = (lambda w: lambda: get(w))(_w)
