"""2.94u: NO MORE BLINKING ONTO A FOE - the one-tick teleports in followers' attacks become dashes (atk.dash: carried a step a
tick in a short arc, a launch puff, a trail in their colour, a landing), and the blow lands when they arrive:
  Bloo's POUNCE and every leap of his WILD HUNT; Bender's TACKLE bound and each GOOD BOY! dart; Bones's TORPEDO (through the
  water, a step a tick, ramming what's in his way) and each FEEDING FRENZY lunge; Queen Ava's ghostly flit onto her foe; and
  Emma's FALLING STAR (Wraithfire) - she dives on it now, instead of appearing there.
(The Stalker's STEP FROM THE DARK stays a blink: it folds away to nothing and unfolds behind its foe - that's the point of it.)"""
import atk


def _split(L, pred):
    i = next(k for k, l in enumerate(L) if pred(l))
    return L[:i] + L[i + 1:], L[i]


def generate(G):
    import phase125 as P125
    fn, F = G.fn, G.FUNCS
    col = lambda w: P125.WHO[w][2]
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'

    def tick_line(pfx, line):
        T = F[f'{pfx}/tick']
        k = next(i for i, l in enumerate(T) if l.startswith('scoreboard players operation #me bm.pid = @s bm.pid')) + 1
        T.insert(k, line)

    # ---- BLOO: the pounce, the Wild Hunt's leaps
    for a, nm, rng, sel in ((1, 'p191/leap', 14, 'sort=nearest'), (2, 'p191/hunt_leap', 16, 'sort=random')):
        rest, tp = _split(F[nm], lambda l: l.endswith('run tp @s ~ ~ ~') and 'at @e[' in l)
        fn(f'p191/k/at{a}', rest)
        F[nm][:] = [f'tag @e[{foe},distance=..{rng},{sel},limit=1] add bm.ktn', f'function bm:p191/k/go {{a:{a}}}']
    tick_line('p191', atk.dash(G, 'p191', col('bloo'), reach=1.4, speed=1.0, onto=True))

    # ---- BENDER: the tackle's bound (the bowl-over comes on its own count, when he's there); GOOD BOY!'s darts
    F['p195/bound'][:] = [f'tag @e[{foe},distance=..12,sort=nearest,limit=1] add bm.ktn', 'function bm:p195/k/go {a:1}']
    fn('p195/k/at1', ['return 0'])
    rest, tp = _split(F['p195/good_hit'], lambda l: 'run tp @e[type=minecraft:wolf,tag=bm.bvme' in l or ('positioned ^ ^ ^1.2' in l and ' run tp ' in l))
    fn('p195/k/at2', rest)
    F['p195/good_hit'][:] = [f'tag @e[{foe},distance=..10,sort=random,limit=1] add bm.ktn', 'function bm:p195/k/go {a:2}']
    tick_line('p195', atk.dash(G, 'p195', col('bender'), reach=1.5, speed=1.0))

    # ---- BONES: the torpedo, through the water a step a tick (ramming what's in his way); the frenzy's lunges
    F['p196/torpedo'][:] = [f'tag @e[{foe},distance=..14,sort=nearest,limit=1] add bm.ktn', 'function bm:p196/k/go {a:1}', 'function bm:p196/blow']
    del F['p196/dash']                                    # (the old one-tick dash)
    fn('p196/k/at1', ['playsound minecraft:entity.dolphin.swim neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    fr = F['p196/frenzy_hit']
    t1 = next(i for i, l in enumerate(fr) if ' run tp @e[type=minecraft:wolf' in l)
    t2 = next(i for i, l in enumerate(fr) if l.startswith('execute at @s as @e['))
    fn('p196/k/at2', fr[2:t1] + fr[t2:])                     # (the bite, its heal, and on - once he's there)
    fr[:] = fr[:2] + ['tag @e[tag=bm.bjfzn,limit=1] add bm.ktn', 'tag @e[tag=bm.bjfzn] add bm.bjfz', 'tag @e[tag=bm.bjfzn] remove bm.bjfzn',
                      'function bm:p196/k/go {a:2}']
    tick_line('p196', atk.dash(G, 'p196', col('bones'), reach=1.6, speed=1.1, lift=0, pass_='#bm:swim_pass',
                               trail=['particle minecraft:bubble ~ ~0.6 ~ 0.3 0.3 0.3 0.02 3',
                                      'execute if score @s bm.ka matches 1 run function bm:p196/k/ram']))
    fn('p196/k/ram', ['tag @s add bm.bjme', 'scoreboard players set #pd bm.rng 10', 'function bm:p196/wake', 'tag @s remove bm.bjme'])   # (the torpedo: what's in his way)

    # ---- QUEEN AVA: her ghost flits onto the foe she touched
    rest, tp = _split(F['p189/melee_hit'], lambda l: l.endswith('run tp @s ~ ~ ~'))
    cond = tp[len('execute '):tp.index(' at @e[')]
    i = F['p189/melee_hit'].index(tp)
    F['p189/melee_hit'][i:i + 1] = [f'execute {cond} run tag @e[{foe},distance=..6,sort=nearest,limit=1] add bm.ktn',
                                    f'execute {cond} if entity @e[tag=bm.ktn] run function bm:p189/k/go {{a:1}}']
    fn('p189/k/at1', ['particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 6'])
    tick_line('p189', atk.dash(G, 'p189', col('ava'), reach=1.2, speed=1.0, lift=0))

    # ---- EMMA (Wraithfire): the Falling Star - a dive onto it
    sd = F['p130/x/star_dive']
    i = next(k for k, l in enumerate(sd) if l.startswith('execute at @e[tag=bm.emstar') and l.endswith('run tp @s ~ ~ ~'))
    sd[i:i + 1] = ['tag @e[tag=bm.emstar,distance=..40,limit=1] add bm.ktn', 'function bm:p57/k/go {a:1}']
    fn('p57/k/at1', ['particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.6 0.2 0.6 0.04 20'])
    line = atk.dash(G, 'p57', col('emma'), reach=1.4, speed=1.4, lift=0)
    T = F['p57/tick']
    T.insert(1, line)
