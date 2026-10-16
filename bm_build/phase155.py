"""2.80a: THE COAT CHECK, AIRTIGHT - nothing from the overworld gets into the vault, however you come in.

The coat check stood at the heist's door and (2.80) the Lounge's. These were the ways round it:
THE LOCKER HALL  the Ledger took you there with everything you carried: a sword put in your locker could be taken out
                 again later - in the den before a heist, or carried into the Lounge. Now the Fixer checks your gear at the
                 Locker Hall's door too, as at the Lounge's; it all comes back when the hall's plate takes you home. (Coming
                 in from the Lounge, you're already checked.)
THE HALL TO THE LOUNGE  the Ledger's Lounge trip from the Locker Hall kept the hall as its way home; it now keeps the
                 hall's own way home (where you came from in the overworld).
THE PEARL OF RETURN  it took you to where you last died - into the vault, if you'd died on a heist. Not any more.
A BAG STILL HELD  (a restore that never ran - a crash, a lost connection) the heist's door said "this time you keep what you
                 carry" and let it all in. Now what you carry joins the bag, and it all comes home together.
ENCHANTED GEAR   the heist gear that passes the check (the Thief's Cowl, Smuggler's and Whisperstep Boots) goes in as the
                 Fixer sold it: enchanted at an anvil outside, it waits with the rest of your gear.
A CATCH-ALL      anyone in the vault who is neither on a heist nor through the coat check (any other way in: a mod, a
                 command, a stale state after a heist) is caught within a quarter second: in the Lounge or the Locker Hall
                 their gear is checked on the spot; anywhere else they're seen out - home, their gear handed back.
(2.80d) THE OTHER WAY   anyone still marked as on a heist while out of the gutter for half a minute (a command took them
                 out, a crash, a lost connection) is taken off it properly - their kept gear handed back - instead of
                 carrying the heist with them: until now a follower's "item put away" rule and a Bond Sigil's mending both
                 stood aside for them, as for a raider in the vault.
(The coffers and every room template carry no ender chest - nothing reaches your ender chest from inside.)"""
from items import T

WEAR = ['thiefs_cowl', 'smugglers_boots', 'whisperstep_boots']      # the heist gear an anvil could enchant (the Frisbee: mending at most)
LOUNGE = '#e8c070'
LOCK = '#c89a5a'


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])

    # ---- the Locker Hall's door: checked like the Lounge's (from outside the vault)
    enter = G.FUNCS['p84/lk/enter']
    enter[0:0] = ['scoreboard players set #lgno bm.rng 0',
                  'execute at @s unless dimension bm:gutter unless entity @s[tag=bm.lgbag] run function bm:p155/lk_check',
                  'execute if score #lgno bm.rng matches 1 run return 0']
    fn('p155/lk_check', ['function bm:p121/check',
                         'execute if entity @s[tag=bm.lgbag] run ' + tellraw('@s', [T('[', 'dark_gray'), T('Locker Hall', LOCK, bold=True), T('] ', 'dark_gray'),
                                                                               T('The Fixer checks your gear at the door - ', '#ffcf40'),
                                                                               T('the hall\'s plate hands it all back as it takes you home. (Heist tools, Tokens and the Ledger come in.)', 'gray')])])
    # (p121/check2's own word says "the Lounge's door": the Locker Hall's check says its own)
    c2 = G.FUNCS['p121/check2']
    assert c2[-1].startswith('tellraw'), c2[-1]
    c2[-1] = 'execute unless entity @s[tag=bm.lkchk] run ' + c2[-1]
    G.FUNCS['p155/lk_check'][0:0] = ['tag @s add bm.lkchk']
    G.FUNCS['p155/lk_check'].insert(2, 'tag @s remove bm.lkchk')

    # ---- a bag still held from before (a restore that never ran: a crash, a lost connection) - the heist's door let you
    # keep what you carried. Now what you carry joins it: what isn't heist gear waits with the Fixer, and comes home with the rest
    b2 = G.FUNCS['p72/bag/check2']
    assert 'still minding your last lot' in b2[0], b2[0][:80]
    b2[0] = '$execute if data storage bm:gv bag.p$(pid) run return run function bm:p155/stale_in'
    fn('p155/stale_in', ['tag @s add bm.lgchk', 'function bm:p121/strip', 'tag @s remove bm.lgchk',
                         say('The Fixer is still minding your last lot of gear - what you carry joins it. You\'ll have it all back at home.', '#ffcf40')])
    # (p121/strip says its own word in the Lounge; at the heist's door it's said above)
    st = G.FUNCS['p121/strip']
    k = next(i for i, l in enumerate(st) if l.startswith('tellraw'))
    st[k] = 'execute unless entity @s[tag=bm.lgchk] run ' + st[k]

    # ---- heist gear goes in as the Fixer sold it: a Thief's Cowl or a pair of the boots enchanted outside (Protection,
    # Feather Falling...) waits with the rest of your gear - the unenchanted ones still go in with you
    import phase72 as P72
    keep_any = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{t}"}}' for t in P72.KEEP) + ']'
    keep_not = '*[' + ','.join(f'!minecraft:custom_data~{{bm:"{t}"}}' for t in P72.KEEP) + ']'
    ench = 'minecraft:enchantments~[{levels:{min:1}}]'
    keep_plain = keep_any[:-1] + ',!' + ench + ']'
    wear_ench = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{w}"}}' for w in WEAR) + ',' + ench + ']'
    has_ench = lambda w: f'[{{components:{{"minecraft:custom_data":{{bm:"{w}"}},"minecraft:enchantments":{{}}}}}}]'

    def plain_slots(L):
        n = 0
        for i, l in enumerate(L):
            if any(f' {sl} {keep_any}' in l for sl in P72.SLOT_OF.values()):
                L[i] = l.replace(keep_any, keep_plain); n += 1
        return n
    b2 = G.FUNCS['p72/bag/check2']
    assert plain_slots(b2) == 2 * len(P72.SLOT_OF)
    rm = [i for i, l in enumerate(b2) if 'bag.p$(pid).inv[{components:' in l]
    assert rm == list(range(rm[0], rm[-1] + 1)) and len(rm) == len(P72.KEEP), rm
    b2[rm[-1] + 1:rm[-1] + 1] = ['$data modify storage bm:gv bag.p$(pid).inv append from storage bm:gv ench[]', 'data remove storage bm:gv ench']
    b2[rm[0]:rm[0]] = ['data modify storage bm:gv ench set value []'] + \
                      [f'$data modify storage bm:gv ench append from storage bm:gv bag.p$(pid).inv{has_ench(w)}' for w in WEAR]
    k = b2.index(f'clear @s {keep_not}')
    b2.insert(k + 1, f'clear @s {wear_ench}')
    b2[1:1] = ['scoreboard players set #ench bm.rng 0'] + \
              [f'execute if items entity @s {sl} {wear_ench} run scoreboard players set #ench bm.rng 1' for sl in ('container.*', 'armor.*')]
    b2.append('execute if score #ench bm.rng matches 1 run ' +
              say('Your enchanted heist gear waits with the rest - it goes in as the Fixer sold it, or not at all.', 'gray'))
    # (the same for what joins a bag already held - p121/strip)
    s1, s2 = G.FUNCS['p121/strip'], G.FUNCS['p121/strip2']
    s1[1:1] = [f'execute store result score #n2 bm.rng run clear @s {wear_ench} 0', 'scoreboard players operation #n bm.rng += #n2 bm.rng']
    assert plain_slots(s2) == len(P72.SLOT_OF)
    k = s2.index('$data modify storage bm:gv cb.p$(pid) append from storage bm:gv sq[]')
    s2[k + 1:k + 1] = [f'$data modify storage bm:gv cb.p$(pid) append from entity @s Inventory{has_ench(w)}' for w in WEAR]
    k = s2.index(f'clear @s {keep_not}')
    s2.insert(k + 1, f'clear @s {wear_ench}')

    # ---- the Lounge from the Locker Hall: its way home is the hall's way home
    le = G.FUNCS['p121/enter']
    k = le.index('function bm:p121/save with storage bm:lg tmp')
    le[k] = 'execute at @s unless dimension bm:gutter run function bm:p121/save with storage bm:lg tmp'      # (where the player is: p121/send calls this after its tp home)
    le.insert(k + 1, 'execute at @s if dimension bm:gutter run function bm:p155/lg_from_hall with storage bm:lg tmp')
    fn('p155/lg_from_hall', ['$execute if data storage bm:lk r.p$(pid) run data modify storage bm:lg r.p$(pid) set from storage bm:lk r.p$(pid)'])

    # ---- the Pearl of Return: not into the vault
    pe = G.FUNCS['p22/pearl']
    k = next(i for i, l in enumerate(pe) if 'bm:hollow_throne' in l)
    pe.insert(k + 1, pe[k].replace('bm:hollow_throne', 'bm:gutter').replace('What the Hollow takes, it keeps.', "The vault's doors don't open that way."))

    # ---- the catch-all: in the vault, neither on a heist nor checked
    # (bm.gvok: an operator's pass - only a command can give it - for staging a test or a build in the vault)
    line = ('execute as @a[tag=!bm.gvp,tag=!bm.lgbag,tag=!bm.gvok,gamemode=!spectator,gamemode=!creative] at @s if dimension bm:gutter '
            'run function bm:p155/stray')
    G.FUNCS['loop/fast'].append(line)
    fn('p155/stray', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                      'execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid',
                      'execute if function bm:p121/inside run return run function bm:p155/check_here with storage bm:gv tmp',
                      'execute if function bm:p84/lk/inside run return run function bm:p155/check_here with storage bm:gv tmp',
                      'function bm:p155/see_out with storage bm:gv tmp'])
    # in the Lounge or the Locker Hall: checked where they stand (a bag already held: what they carry joins the rest)
    fn('p155/check_here', ['$execute if data storage bm:gv bag.p$(pid) run function bm:p121/strip',
                           'tag @s add bm.lgchk', '$execute unless data storage bm:gv bag.p$(pid) run function bm:p72/bag/check2 with storage bm:gv tmp', 'tag @s remove bm.lgchk',
                           'tag @s add bm.lgbag',
                           say('The Fixer checks your gear - nothing from outside comes into the vault. You\'ll have it back at home.', '#ffcf40')])
    # the stray's own home: their respawn point (unless that's in the vault - a stale one from a heist)
    fn('p155/sp_read', ['data remove storage bm:gv sph', 'data modify storage bm:gv sph.d set from entity @s respawn.dimension',
                        'execute store result storage bm:gv sph.x int 1 run data get entity @s respawn.pos[0]',
                        'execute store result storage bm:gv sph.y int 1 run data get entity @s respawn.pos[1]',
                        'execute store result storage bm:gv sph.z int 1 run data get entity @s respawn.pos[2]',
                        'execute store result storage bm:gv sph.r int 1 run data get entity @s respawn.yaw',
                        'execute if data storage bm:gv {sph:{d:"bm:gutter"}} run data remove storage bm:gv sph.d'])
    # anywhere else: seen out - home (their respawn point, else the heist's way home, else the Lounge's, else the hall's),
    # their gear handed back
    fn('p155/see_out', [say('You\'re not on a job down here - the Fixer sees you out.', 'red'),
                        'scoreboard players set #ok bm.rng 0', 'function bm:p155/sp_read',
                        'execute if data storage bm:gv sph.d run function bm:p155/out_sp with storage bm:gv sph',
                        '$execute if score #ok bm.rng matches 0 if data storage bm:gv ret.p$(pid) run function bm:p70/home3 with storage bm:gv ret.p$(pid)',
                        '$execute if score #ok bm.rng matches 0 if data storage bm:lg r.p$(pid) run function bm:p155/out_lg with storage bm:lg r.p$(pid)',
                        '$execute if score #ok bm.rng matches 0 if data storage bm:lk r.p$(pid) run function bm:p155/out_lg with storage bm:lk r.p$(pid)',
                        'execute if score #ok bm.rng matches 0 in minecraft:overworld run tp @s 0 200 0',
                        'execute if score #ok bm.rng matches 0 run effect give @s minecraft:slow_falling 30 0 true',
                        'execute if entity @s[gamemode=adventure] run gamemode survival @s',
                        'function bm:p72/bag/restore'])
    fn('p155/out_sp', ['$execute in $(d) run tp @s $(x).5 $(y) $(z).5 $(r) 0', 'scoreboard players set #ok bm.rng 1'])
    fn('p155/out_lg', ['$execute in $(d) unless dimension bm:gutter run tp @s $(x) $(y) $(z) $(r) 0', '$execute in $(d) unless dimension bm:gutter run scoreboard players set #ok bm.rng 1'])
    # (checked where they stand: the Lounge's door and the hall's plate take them to their respawn point)
    G.FUNCS['p155/check_here'] += ['function bm:p155/sp_read', 'execute if data storage bm:gv sph.d run function bm:p155/home_set with storage bm:gv tmp']
    fn('p155/home_set', ['$data modify storage bm:lg r.p$(pid) set from storage bm:gv sph', '$data modify storage bm:lk r.p$(pid) set from storage bm:gv sph'])
    # ---- (2.80d) the other way: on a heist, but out of the gutter for 30 seconds - off it, properly (p70/unraid hands back the
    #      gear the coat check kept; it's what every exit of a heist ends with)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvstr dummy']
    G.OBJECTIVES += ['bm.gvstr']
    G.FUNCS['loop/second'][-1:-1] = ['execute as @a[tag=bm.gvp,tag=!bm.gvdead] at @s unless dimension bm:gutter run function bm:p155/left_out',
                                     'execute as @a[scores={bm.gvstr=1..}] at @s if dimension bm:gutter run scoreboard players reset @s bm.gvstr',
                                     'execute as @a[tag=!bm.gvp,scores={bm.gvstr=1..}] run scoreboard players reset @s bm.gvstr']
    fn('p155/left_out', ['scoreboard players add @s bm.gvstr 1', 'execute unless score @s bm.gvstr matches 30.. run return 0',
                      'scoreboard players reset @s bm.gvstr', 'function bm:p70/unraid',
                      say('You left the gutter mid-heist - the Fixer counts you out (your gear is back with you).', 'gray')])
