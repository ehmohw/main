"""2.80a: THE RAID, DEBUGGED - loose ends found by playing it through, crew by crew.

A FINISHED HEIST WAS STILL OPEN  when the whole crew left together ("Go to the Lounge", "Back to the Overworld", the
                 Ledger's Leave), the heist kept its place for its 20-second tidy-up - still open to its own party. Plan a
                 Heist in that time (from the Lounge, straight away) and the crew "slipped into the vault to join the heist":
                 the old one, its rooms beaten, its vault paid out, no end-of-heist choice ever to come. Now a heist closes
                 the moment its last raider leaves; the next plan is a new heist.
THE VAULT DOOR   the door's opening (the 2.80 climax) marks the vault open as it finishes - and if the strongbox had
                 already paid out by then, that marked a paid heist back to "open": joinable, and short of its ending.
                 Now it never takes a heist back."""


def generate(G):
    fn = G.fn
    # ---- the last raider out closes the heist (p70/joinable takes only a heist at 1..3)
    lf = G.FUNCS['p104/left']
    lf.append('execute if score #n bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng '
              'unless score @s bm.gvst matches 4.. run scoreboard players set @s bm.gvst 4')
    # ---- the vault door never takes a paid-out heist back to "open"
    op = G.FUNCS['p70/r/vault/opened']
    k = next(i for i, l in enumerate(op) if l.endswith('run scoreboard players set @s bm.gvst 3'))
    op[k] = op[k].replace('run scoreboard players set @s bm.gvst 3', 'unless score @s bm.gvst matches 4.. run scoreboard players set @s bm.gvst 3')
