"""2.80a: THE RAID, DEBUGGED - loose ends found by playing it through, crew by crew.

A FINISHED HEIST WAS STILL OPEN  when the whole crew left together ("Go to the Lounge", "Back to the Overworld", the
                 Ledger's Leave), the heist kept its place for its 20-second tidy-up - still open to its own party. Plan a
                 Heist in that time (from the Lounge, straight away) and the crew "slipped into the vault to join the heist":
                 the old one, its rooms beaten, its vault paid out, no end-of-heist choice ever to come. Now a heist closes
                 the moment its last raider leaves; the next plan is a new heist.
THE VAULT DOOR   the door's opening (the 2.80 climax) marks the vault open as it finishes - and if the strongbox had
                 already paid out by then, that marked a paid heist back to "open": joinable, and short of its ending.
                 Now it never takes a heist back.
TULLIUS'S SHIP   (found on the way) come up in a frozen ocean, she could be built into an iceberg - packed ice over her
                 deck and her ladder, no way aboard. Her bounds are cleared of ice and snow as she's built."""


def generate(G):
    fn = G.fn
    # ---- the last raider out closes the heist (p70/joinable takes only a heist at 1..3)
    lf = G.FUNCS['p104/left']
    lf.append('execute if score #n bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng '
              'unless score @s bm.gvst matches 4.. run scoreboard players set @s bm.gvst 4')
    # ---- (found on the way) Tullius's ship, come up in a frozen ocean, could be built into an iceberg: packed ice on her
    # deck and over her ladder, no way aboard. Her bounds are cleared of ice and snow first (water below the waterline)
    sb = G.FUNCS['p132/ship/build']
    k = next(i for i, l in enumerate(sb) if 'place template bm:p132_ship' in l)
    sb[k:k] = ['fill ~-16 ~ ~-6 ~17 ~20 ~6 minecraft:air replace #minecraft:ice', 'fill ~-16 ~ ~-6 ~17 ~20 ~6 minecraft:air replace minecraft:snow_block',
               'fill ~-16 ~ ~-6 ~17 ~20 ~6 minecraft:air replace minecraft:snow', 'fill ~-16 ~ ~-6 ~17 ~20 ~6 minecraft:air replace minecraft:powder_snow',
               'fill ~-16 ~-5 ~-6 ~17 ~-1 ~6 minecraft:water replace #minecraft:ice']
    # ---- the vault door never takes a paid-out heist back to "open"
    op = G.FUNCS['p70/r/vault/opened']
    k = next(i for i, l in enumerate(op) if l.endswith('run scoreboard players set @s bm.gvst 3'))
    op[k] = op[k].replace('run scoreboard players set @s bm.gvst 3', 'unless score @s bm.gvst matches 4.. run scoreboard players set @s bm.gvst 3')
