"""2.80b: THE MARKET, THE DUNGEONS AND BOSSES, THE HOLLOW AND THE ITEMS - debugged and polished (the regression sweep, as a
regular player).

APOPHISS UNBOUND  "something vast and winged tears free of his scales" - and nothing did: the change set his wings'
                 interpolation time and never their size, so they stayed folded away (scale 0) through the title and the
                 climb, until his flight loop's first wingbeat after it. They now unfurl at the title, over a second and a
                 half, in the lifting pose.
DEMOCRATUS'S DUEL  lost at three hearts - and he took a challenge from a player already at three and a half: the ten-second
                 countdown ran, and the duel was lost the moment it began, before he'd taken a step. Now he won't duel
                 anyone at five hearts or less ("Catch your breath first").
KILLERWATT'S JAB AND HIS VOID LANCES  shared one attack slot: every jab of the boss also ran the Ethereal form's Void
                 Lances - his punch pose overwritten by the lance charge (the jab rarely landed), and the plain boss throwing
                 void lances he should never have. The lances have a slot of their own now: the jab for both forms, the
                 lances only for the Ethereal KillerWatt.
"""


def generate(G):
    fn, title, T = G.fn, G.title, G.T
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    # ---- Democratus won't duel a player in no shape to fight (the duel is lost at 6 health)
    st = G.FUNCS['p97/duel/start']
    k = next(i for i, l in enumerate(st) if 'Not in the vault. Find open ground.' in l)
    st[k + 1:k + 1] = ['execute store result score #ph bm.rng run data get entity @s Health',
                       'execute if score #ph bm.rng matches ..10 run return run ' + say("Catch your breath first - he won't duel you half-dead.")]
    # ---- KillerWatt: the Void Lances (Ethereal only) off the jab's attack slot (6) onto their own (7)
    att = G.FUNCS['p79/boss/attack']
    k = att.index('execute if score @s bm.kxatk matches 6 run function bm:p83/a_lances')
    att[k] = 'execute if score @s bm.kxatk matches 7 run function bm:p83/a_lances'
    mind = G.FUNCS['p79/boss/mind']
    k = next(i for i, l in enumerate(mind) if l.startswith('execute if entity @s[tag=bm.kxeth] if score #r bm.rng matches 1..30') and l.endswith('{a:6}'))
    mind[k] = mind[k][:-len('{a:6}')] + '{a:7}'
    asc = G.FUNCS['p131/b/a_ascend']
    k = next(i for i, l in enumerate(asc) if 'matches 232' in l and 'app_wingr' in l and 'interpolation_duration:30' in l)
    asc.insert(k, 'execute if score @s bm.apt matches 232 run function bm:p131/b/pose/eth_lift')
