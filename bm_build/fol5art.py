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
                 own_sets=None, fit_pose='idle_a', extra_poses=None, extra=()):
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
        self.RIGS = (rig,) + tuple(extra)                 # (3.1: the Sapling's three stages - one follower, a rig each, its displays the last's)
        self.PREFIXES = tuple(r.PREFIX for r in self.RIGS)
        sh = shiny[0]
        self.SHINY_TEX, self.LOOK_DRAWN, look = {}, {}, []
        for r in self.RIGS:
            pre = r.PREFIX
            base = [t for t in r._tex if not any(t.endswith(s) for s in r._skins)]
            look += [pre + t for t in look_tex if t in base]
            if sh:
                self.SHINY_TEX.update({pre + t: (lambda im: lambda b: im)(r._tex[t + sh]) for t in base if t + sh in r._tex})
            for k, sfx in (drawn or {}).items():
                self.LOOK_DRAWN.setdefault(k, {}).update({pre + t: r._tex[t + sfx] for t in base if t + sfx in r._tex})
        self.LOOK_TEX = tuple(look)
        drawn_keys = sorted({n for d in self.LOOK_DRAWN.values() for n in d})
        self.LOOK_SHINY_ONLY = tuple(n for n in sorted(set(self.SHINY_TEX) | set(drawn_keys)) if n not in self.LOOK_TEX)
        self.RECOL_KEYS = self.LOOK_TEX + self.LOOK_SHINY_ONLY
        keep_gold = set(r.PREFIX + t for r in self.RIGS for t in (gild if gild is not None else look_tex))
        self.LOOK_GILD_SKIP = tuple(n for n in self.RECOL_KEYS if n not in keep_gold)
        self.SHINY_COLS = shiny
        self.OWN_SETS = dict(own_sets or {})
        self.DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
        self.GROUPS = dict(doll_groups or {})
        self.DOLL_POSE = None             # (an art with a doll of its own - the Mimic's: doll(module) takes its DOLL_POSE, DOLL and DOLL_GROUPS)
        self.FIT = rig.fit(rig.POSES[fit_pose])

    def doll(self, mod):
        """(3.1) the art module's own doll source, if it has one: DOLL_POSE (the pose baked, its opt parts shown), DOLL (the warp and
        fit), DOLL_GROUPS - in place of the default warp at rest"""
        if getattr(mod, 'DOLL_POSE', None):
            self.DOLL_POSE = mod.DOLL_POSE
            self.DOLL = dict(getattr(mod, 'DOLL', self.DOLL))
            self.GROUPS = dict(getattr(mod, 'DOLL_GROUPS', self.GROUPS))
        return self

    # ---- rigpet / rigfol
    def HIDDEN(self, p, pose):
        return self.R.HIDDEN(p, pose)

    def model_name(self, p, pose=None, suffix=''):
        return self.R.model_name(p, pose, suffix)

    def models(self):
        out = {}
        for r in self.RIGS:
            out.update({n: v for n, v in r.models().items() if not any(n.endswith(s) for s in self.DROP)})
        return out

    # ---- phase138
    def textures(self):
        out = {}
        for r in self.RIGS:
            out.update({n: im for n, im in r.textures().items() if not any(n.endswith(s) for s in self.DROP if s)})
        return out

    def look_item(self, n):
        """phase138.ITEMS_OF: the models a look is copied onto - the follower's own sets (not its afterimages / effects)"""
        return n.startswith(self.PREFIXES) and not any(n.endswith(s) for s in getattr(self, 'NO_LOOK', ()))

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
    from fol5_kit import ghost
    base = [t for t in GA.TEX]
    for t in base:                                  # (3.1: the shiny's afterimages are gold - a '_gg' set of its own)
        GA.R.tex(t + '_gg', ghost(GA.TEX[t], '#ffd23a', 110))
    GA.R.skin('_gg', {t: t + '_gg' for t in base})
    A = Art('glitch', GA.R, {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'},
            ('case', 'case2', 'knob'), shiny=('_sh', '#c8962a', 'yellow'),
            doll_groups=GA.DOLL_GROUPS)
    A.NO_LOOK = ('_g', '_gr', '_gc', '_gg')            # (afterimages and the RGB split: never worn with a look)
    A.MOTION, A.SLICE_LAG, A.JIT_P, A.JIT_X = GA.MOTION, GA.SLICE_LAG, GA.JIT_P, GA.JIT_X
    return A


def _cake():
    import cake_pet_art as CA
    frost = ('frost', 'frost2', 'frosth')
    A = Art('cake', CA.R, {'happy': 'happy', 'surprised': 'wow', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'wow'},
            (), drop=('_sh', '_mint', '_lem', '_choc'), drawn={1: '_mint', 2: '_lem', 3: '_choc'}, gild=frost + ('cream',),
            shiny=('_sh', '#5a48b8', 'blue'), doll_groups=CA.DOLL_GROUPS)
    return A


def _sapling():
    import sapling_pet_art as SA
    leafy = ('leaf', 'leaft', 'blade', 'coty', 'fol', 'folt')
    A = Art('sapling', SA.RIGS[3], {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'},
            leafy, drop=('_sh', '_aut'), drawn={1: '_aut'}, shiny=('_sh', '#d0628e', 'pink'), doll_groups=SA.DOLL_GROUPS, extra=(SA.RIGS[1], SA.RIGS[2]))
    A.STAGES = SA.RIGS
    return A


def _spawner():
    import spawner_pet_art as WA
    A = Art('spawner', WA.R, {'happy': 'happy', 'surprised': 'wow', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'},
            ('bar', 'bar2', 'rivet'), drop=('_sh', '_cop', '_am'), drawn={1: '_cop', 2: '_am'}, shiny=('_sh', '#e8b830', 'yellow'), doll_groups=WA.DOLL_GROUPS)
    A.MINIONS = WA.MINIONS
    return A


def _cairn():
    """the Cairn: its blocks are block_displays (phase268) - the rig the game moves as item displays is only what is really IT,
    its EYES (the head block's front) and its HEART; every pose is still solved on the whole golem's joints"""
    import assembler_pet_art as AR
    from fol5_kit import Rig
    pv = dict(AR.PIVOT, eyes=AR.PIVOT['head']); par = dict(AR.PARENT, eyes='head')
    R = Rig('as_', AR.R.RIG_SCALE, pv, par, AR.FACES, face_part='eyes')
    for k in ('eyes', 'heart', 'heartglow') + tuple(f'eyes_{f}' for f in AR.FACES):
        R.tex(k, AR.R._tex[k])
    R._els['eyes'] = [e for e in AR.R._els['head'] if any(f['texture'] == '#EYES' for f in e['faces'].values())]
    R._els['heart'] = list(AR.R._els['heart'])
    R._pts['eyes'], R._pts['heart'] = list(AR.R._pts['head']), list(AR.R._pts['heart'])
    R.POSES = AR.POSES
    R.PARTS = ('eyes', 'heart')
    A = Art('cairn', R, {'happy': 'happy', 'surprised': 'blink', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'},
            ('heartglow',), drop=(), shiny=(None, '#c8962a', 'yellow'))     # (a look is a whole palette of blocks (phase268); the glow round its heart takes the look's colour)
    A.FIT = AR.R.fit(AR.POSES['idle_a'])
    A.FULL = AR
    return A


class KnightArt(types.ModuleType):
    """the Hollow Statue Knight: TWO rigs in one follower - the armour (hk_, knight_art's at companion size) and the soul serpent
    inside it (hs_, its parts 's_<part>'). rigpet sees one set of parts; phase269 writes every pose itself (each rig solved on
    its own joints, the serpent anchored at the helm's visor or wherever the pose puts it). Its looks are drawn sets: Freed (look
    1: the armour's freed finish and the serpent's '_f'), the shiny (Starlit: 'shiny' and '_s'); looks 2-3 recolour the cloak."""
    def __init__(self):
        super().__init__('f5art_knight')
        import hollowknight_pet_art as H
        self.H, self.AR, self.SR = H, H.ARMOUR, H.SERPENT
        A, S = self.AR, self.SR
        self.SP = tuple(f's_{p}' for p in S.PARTS)
        # (3.1, the owner: the statue knights' own size by default - knight_art's RIG_SCALE, ~3 blocks; Companion Size, his menu's
        #  toggle, twins it at H.COMPANION (compsize, phase269). FULL: the art's own lever if it gives one)
        self.FULL = getattr(H, 'FULL', H.KA.RIG_SCALE)
        self.F = self.FULL / H.COMPANION
        self.PREFIX, self.RIG_SCALE = 'hk_', self.FULL
        self.PARTS = tuple(A.PARTS) + self.SP
        self.PIVOT = dict(A.PIVOT, **{q: (0.0, 0.0, 0.0) for q in self.SP})
        self.PARENT = dict(A.PARENT, **{q: None for q in self.SP})
        self.PART_K = dict(A.PART_K, **{q: S.RIG_SCALE / H.COMPANION for q in self.SP})
        self.FACES, self.FACE_PARTS, self.FACE_PART = S.FACES, ('s_head',), 's_head'
        self.FACE_BASE, self.RIGS = 'hs_head', (S,)        # (his faces: the serpent's head's models; its bare joints wear empty models)
        self.FACE_MAP = {'happy': 'happy', 'surprised': 'focus', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'}
        self.POSES = {}                  # (phase269 fills these: name -> (armour pose, serpent pose or None, anchor) and a dict rigpet reads)
        self.SKINS = ['']
        at, st = A.textures(), S.textures()
        self._tex = dict({k: v for k, v in at.items() if k.startswith('hk_h_')}, **{k: v for k, v in st.items() if not (k[-2:] in ('_f', '_s') and k[:-2] in st)})
        self.LOOK_TEX = ('hk_h_cloth', 'hk_h_hem')
        self.LOOK_DRAWN = {1: dict({k: at['hk_f_' + k[5:]] for k in self._tex if k.startswith('hk_h_') and 'hk_f_' + k[5:] in at},
                                   **{k: st[k + '_f'] for k in self._tex if k + '_f' in st})}
        self.SHINY_TEX = dict({k: (lambda im: lambda b: im)(at['hk_s_' + k[5:]]) for k in self._tex if k.startswith('hk_h_') and 'hk_s_' + k[5:] in at},
                              **{k: (lambda im: lambda b: im)(st[k + '_s']) for k in self._tex if k + '_s' in st})
        keys = sorted(set(self.LOOK_DRAWN[1]) | set(self.SHINY_TEX))
        self.LOOK_SHINY_ONLY = tuple(k for k in keys if k not in self.LOOK_TEX)
        self.RECOL_KEYS = self.LOOK_TEX + self.LOOK_SHINY_ONLY
        self.LOOK_GILD_SKIP = tuple(k for k in self.RECOL_KEYS if k not in ('hk_h_plate', 'hk_h_trim', 'hk_h_dark'))
        self.SHINY_COLS = (None, '#3a4ab0', 'blue')
        self.OWN_SETS = {}
        self.DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
        self.GROUPS = {}
        self.DOLL_POSE = None
        self.FIT = tuple(round(v * self.F, 3) for v in (0.0, 1.5, -0.45, 0.45, -0.3, 0.35))     # (at companion size: 1.5 tall)

    def _split(self, p):
        return (p[2:], True) if p.startswith('s_') else (p, False)

    def HIDDEN(self, p, pose):
        q, ser = self._split(p)
        if p in pose.get('_hide', ()):
            return True
        if ser:
            sp = pose.get('_serp')
            return sp is None or self.SR.HIDDEN(q, sp)
        return self.AR.HIDDEN(q, pose.get('_arm', {}))

    def model_name(self, p, pose=None, suffix=''):
        q, ser = self._split(p)
        if ser:
            return self.SR.model_name(q, {k: v for k, v in ((pose or {}).get('_serp') or {}).items() if k != '_face'}, suffix)
        return self.AR.model_name(q, {}, suffix)

    def models(self):
        out = {n: v for n, v in self.AR.models().items() if n.startswith('hk_hollow_')}
        sm = self.SR.models()             # (its skins' sets dropped - a name that's another's plus '_f' / '_s'; its body shape 's' is hs_b_s)
        out.update({n: v for n, v in sm.items() if not (n[-2:] in ('_f', '_s') and n[:-2] in sm)})
        return out

    def textures(self):
        return dict(self._tex)

    def look_item(self, n):
        return n.startswith(('hk_hollow_', 'hs_'))

    @property
    def SHINY_LOOK(self):
        return ('Shiny Starlit', ('#060a2a', '#3a4ab0', '#c0c8ff'), 'blue')

    def face_cases(self, sfx=''):
        return {e: f'hs_head_x{f}' for e, f in self.FACE_MAP.items() if f in self.FACES}


def _knight():
    return KnightArt()


def _mimic():
    import mimic_pet_art as MA
    A = Art('mimic', MA.R, {'happy': 'happy', 'surprised': 'greedy', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce'},
            ('gum', 'tongue', 'throat'), drop=('_sh', '_crate', '_gild'), drawn={1: '_crate', 2: '_gild'}, gild=('brass', 'gold'), shiny=('_sh', '#7a3ad0', 'purple')).doll(MA)
    A.NO_LOOK = ()
    return A


class RexArt(types.ModuleType):
    """the Atomic Rex (rex_art - phase249's mount rig, its models as they are): a follower at companion size (FULL / K_UP, ~2.5
    blocks; its menu's Full Size twins it at FULL - compsize), its plated parts' models swapped per pose (the breath's glow: _charge).
    Its looks: the MECHA costume (look 1, handmade - every rx_atomic_ model's item definition worn as the rx_mecha_ one, phase272),
    the rest recolours of its hide and plates"""
    K_UP = 3.0

    def __init__(self):
        super().__init__('f5art_rex')
        import rex_art as R
        self.R, self.W = R, 'rex'
        self.PREFIX, self.FULL = 'rx_atomic_', R.RIG_SCALE
        self.RIG_SCALE = round(R.RIG_SCALE / self.K_UP, 4)
        self.PIVOT, self.PARENT, self.PARTS, self.PART_K = R.PIVOT, R.PARENT, R.PARTS, dict(R.PART_K)
        self.POSES = {n: dict(p, _kind='atomic') for n, p in R.POSES.items()}
        for n in ('breath_0', 'breath_1'):
            self.POSES[n]['_charge'] = True
        self.FACES, self.FACE_PARTS, self.FACE_PART, self.FACE_MAP = (), ('head',), 'head', {}
        self.SKINS = ['']
        at = {n: im for n, im in R.textures().items() if n.startswith('rx_a_')}
        self._tex = at
        self.LOOK_TEX = tuple(n for n in at if n not in ('rx_a_eye', 'rx_a_maw', 'rx_a_tooth', 'rx_a_claw', 'rx_a_steel', 'rx_a_stud', 'rx_a_strap', 'rx_a_leather'))
        self.LOOK_DRAWN, self.SHINY_TEX, self.LOOK_SHINY_ONLY = {}, {}, ()
        self.RECOL_KEYS = self.LOOK_TEX
        self.LOOK_GILD_SKIP = tuple(n for n in self.LOOK_TEX if n not in ('rx_a_pcore', 'rx_a_pcore_c', 'rx_a_pedge', 'rx_a_pedge_c', 'rx_a_crag'))
        self.SHINY_COLS = (None, '#d8d8d8', 'white')
        self.OWN_SETS = {}
        self.DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
        self.GROUPS = {'head': 'head', 'jaw': 'head', 'neck': 'head', 'thighr': 'legs', 'shinr': 'legs', 'footr': 'legs', 'thighl': 'legs', 'shinl': 'legs', 'footl': 'legs'}
        self.DOLL_POSE = None
        import rigkit as RK
        pts = []
        U = self.RIG_SCALE / 16
        xf = RK.solve(R.PIVOT, R.PARENT, R.POSES['idle_a'])
        for p in R.PARTS:
            q, t = xf[p]; pv = RK.D(R.PIVOT[p])
            pts.append(tuple((pv[i] + t[i]) * U for i in range(3)))
        ys = [p[1] for p in pts]; xs = [p[0] for p in pts]; zs = [p[2] for p in pts]
        self.FIT = (0.0, round(max(ys) * 1.12, 3), round(min(xs) - 0.25, 3), round(max(xs) + 0.25, 3), round(min(zs) - 0.3, 3), round(max(zs) + 0.3, 3))

    def HIDDEN(self, p, pose):
        return p in pose.get('_hide', ())

    def model_name(self, p, pose=None, suffix=''):
        pose = pose or {}
        return self.R.model_id(p, pose.get('_kind', 'atomic'), 'charged' if pose.get('_charge') else None) + suffix

    def models(self):
        return {}                         # (phase249's resource pack has them all)

    def textures(self):
        return dict(self._tex)

    def look_item(self, n):
        return n.startswith('rx_atomic_')

    @property
    def SHINY_LOOK(self):
        return ('Shiny Bone White', ('#3a3a3a', '#d8d8d8', '#9ff0ff'), 'white')

    def face_cases(self, sfx=''):
        return {}


def _rex():
    return RexArt()


def _ferro():
    import ferro_pet_art as FA
    FA.DOLL_POSE = 'doll'                         # (its doll's own pose: no puddle, hands tucked - and fitted 11 units wide)
    FA.DOLL = dict(FA.DOLL, width=FA.DOLL_W)
    A = Art('ferro', FA.R, {'happy': 'happy', 'surprised': 'wide', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce'},
            ('sx', 'sxd', 'up', 'dn', 'spk'), drop=('_sh', '_qs', '_au'), drawn={1: '_qs', 2: '_au'}, gild=('sx', 'sxd', 'up', 'dn', 'spk'),
            shiny=('_sh', '#c040a0', 'magenta'), doll_groups=FA.DOLL_GROUPS).doll(FA)
    A.NO_LOOK = ()
    A.FM = FA                                     # (its mimicry: ferro_form and the rest - phase271)
    return A


def _kaiju(mod, w, drawn, shiny, comp):
    """Talus and Trivyrn (fol5_kit rigs, built at their full size): the follower is built at its companion size (comp - its own
    RIG_SCALE / K_UP), Full Size (compsize) twins it at its own"""
    import importlib
    M = importlib.import_module(mod)
    A = Art(w, M.R, {'happy': 'happy', 'surprised': 'look', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce'},
            tuple(t for t in M.R._tex if not any(t.endswith(s) for s in M.R._skins)), drop=tuple(s for s in M.R._skins if s not in ('_ch', '_g')), drawn=drawn, shiny=shiny,
            doll_groups=getattr(M, 'DOLL_GROUPS', None))
    M.DOLL_POSE = 'doll'
    A.doll(M)
    A.FULL = M.R.RIG_SCALE
    A.K_UP = round(A.FULL / comp, 4)
    A.RIG_SCALE = comp
    A.FIT = tuple(round(v / A.K_UP, 3) for v in A.FIT)
    A.NO_LOOK = tuple(s for s in ('_g', '_ch'))
    A.M = M
    return A


_MADE = {}
_MAKERS = {'talus': lambda: _kaiju('kaiju_ape_art', 'talus', {1: '_au', 2: '_sn'}, ('_sh', '#3aa070', 'green'), 0.83),
           'trivyrn': lambda: _kaiju('kaiju_hydra_art', 'trivyrn', {1: '_dw', 2: '_ab'}, ('_sh', '#f0e8f8', 'white'), 0.77),
           'rex': _rex, 'ferro': _ferro, 'knight': _knight, 'mimic': _mimic, 'glitch': _glitch, 'cake': _cake, 'sapling': _sapling, 'spawner': _spawner, 'cairn': _cairn}


def get(w):
    if w not in _MADE:
        a = _MAKERS[w]()
        _MADE[w] = a
        sys.modules[a.__name__] = a
    return _MADE[w]


for _w in _MAKERS:
    fol5._ARTS[_w] = (lambda w: lambda: get(w))(_w)
