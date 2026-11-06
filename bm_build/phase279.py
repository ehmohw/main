"""3.1c: THE SAFEKEEPER - a hard failsafe for every player's own progress.

The owner (after 3.1b): "it completely cleared my rat pack ... all my followers have been completely reset". Everything a
player owns in this pack hangs off two things: their scores (kept by NAME in the world's scoreboard - the Rat Pack's rows, every
follower's state, every unlock) and their Pack ID (bm.pid - itself a score), which files their Rat Pack, collectors and partner
wheel in storage. Lose the scores (a new name, a scoreboard reset, a lost scoreboard file) and the Pack ID goes with them: the
next menu hands out a NEW one, and the player's whole history looks gone though it is all still in storage.

THE REGISTRY   storage bm:safe, a file of its own: every player's Pack ID under their UUID (id."u<a>_<b>_<c>_<d>"), and the
               highest Pack ID ever handed out (nx) - so a lost scoreboard never hands out an old one again.
THE GUARD      before any Pack ID is handed out (p21/pid), and for anyone found without one or with one that isn't theirs, the
               registry is asked first: the old one is put back - and with it everything below, at once, with a word.
THE SNAPSHOT   every 10 minutes, spread over 35 seconds (100 a second), every score the pack keeps on a player (all its own
               objectives), their tags, and a copy of their Rat Pack's storage go into bm:safe p<pid>.
THE RESTORE    (automatic, when the guard puts a Pack ID back) every score the player has lost - only those that are unset now,
               never one that has a value - and every tag they've lost come back; the Rat Pack's rows are relinked
               (admin/rp_relink).
ADMIN          /function bm:admin/safe_restore - the same restore, by hand (your Pack ID from the registry, your lost scores and
               tags, your Pack's rows). /function bm:admin/safe_pack - puts back anything your Rat Pack held at the last
               snapshot that it no longer holds (things you took out since come back too: for a Pack that lost its things).
               /function bm:admin/safe_status - your Pack ID, what the registry holds for you, and when you were last kept.
NOT KEPT       advancements (they hand out their rewards again when granted) and the world's own counters (#-names)."""
from items import T

COL = '#8ad8ff'
PRE = [T('[', 'dark_gray'), T('Safekeeper', COL, bold=True), T('] ', 'dark_gray')]
CHUNK = 100                       # (objectives kept per player per second - light: about 6 commands a second on average)
EVERY = 600                       # (seconds between snapshots)
SKIP = {'bm.pid', 'bm.sfk', 'bm.sft', 'bm.rng', 'bm.act', 'bm.menu', 'bm.pay'}       # (its own, and the scratch ones)


def late(G):
    fn, tellraw = G.fn, G.tellraw
    F = G.FUNCS
    objs = [l.split()[3] for l in F['load'] if l.startswith('scoreboard objectives add ') and l.split()[4] == 'dummy']
    objs = [o for o in dict.fromkeys(objs) if o not in SKIP]
    q = lambda o: f'"{o}"'
    F['load'][-1:-1] = ['scoreboard objectives add bm.sfk dummy', 'scoreboard objectives add bm.sft dummy']
    G.OBJECTIVES += ['bm.sfk', 'bm.sft']

    # ---- the UUID key and the Pack ID, in bm:safe t
    uid = [f'execute store result storage bm:safe t.{c} int 1 run data get entity @s UUID[{i}]' for i, c in enumerate('abcd')]
    fn('p279/id/key', uid + ['execute store result storage bm:safe t.pid int 1 run scoreboard players get @s bm.pid'])
    fn('p279/id/rec', ['function bm:p279/id/key', 'function bm:p279/id/recm with storage bm:safe t',
                       # (the highest Pack ID known: never handed out again)
                       'execute store result score #snx bm.rng run data get storage bm:safe nx',
                       'execute if score @s bm.pid > #snx bm.rng store result storage bm:safe nx int 1 run scoreboard players get @s bm.pid',
                       'execute if score #next bm.pid > #snx bm.rng if score #next bm.pid > @s bm.pid store result storage bm:safe nx int 1 run scoreboard players get #next bm.pid'])
    fn('p279/id/recm', ['$data modify storage bm:safe id."u$(a)_$(b)_$(c)_$(d)" set value $(pid)'])
    # (the registry's Pack ID for this player -> #sid (0: none))
    fn('p279/id/get', ['scoreboard players set #sid bm.rng 0', 'function bm:p279/id/key', 'function bm:p279/id/getm with storage bm:safe t'])
    fn('p279/id/getm', ['$execute store result score #sid bm.rng run data get storage bm:safe id."u$(a)_$(b)_$(c)_$(d)"'])

    # ---- THE GUARD: before a Pack ID is handed out - and for anyone whose Pack ID isn't the registry's
    fn('p279/guard', ['function bm:p279/id/get',
                      'execute if score #sid bm.rng matches 1.. if score @s bm.pid = #sid bm.rng run return 0',
                      'execute if score #sid bm.rng matches 1.. run return run function bm:p279/back',
                      # (not in the registry yet: a Pack ID of their own goes in it)
                      'execute if score @s bm.pid matches 1.. run function bm:p279/id/rec'])
    # (the restore is a few thousand commands: it runs in a function of its own, scheduled - never inside the tick's own budget)
    fn('p279/back', ['scoreboard players operation @s bm.pid = #sid bm.rng', 'tag @s add bm.sfrest', 'schedule function bm:p279/rest_due 1t append',
                     tellraw('@s', PRE + [T('Your Pack ID had gone missing - it\'s back, and with it your partners, your Rat Pack and the '
                                            'rest of what you had. ', 'gray'), T('(Nothing was lost.)', 'dark_gray')])])
    pid = F['p21/pid']
    pid[0:0] = ['execute if entity @s[type=minecraft:player] run function bm:p279/guard',
                'execute if entity @s[type=minecraft:player] if score @s bm.pid matches 1.. run return 0',
                # (never an old Pack ID again, even with the scoreboard lost: the registry remembers the highest)
                'execute store result score #snx bm.rng run data get storage bm:safe nx',
                'execute if score #next bm.pid < #snx bm.rng run scoreboard players operation #next bm.pid = #snx bm.rng']
    pid += ['execute store result storage bm:safe nx int 1 run scoreboard players get #next bm.pid', 'execute if entity @s[type=minecraft:player] run function bm:p279/id/rec']
    # (at the very start of each tick: anyone without a Pack ID - a lost scoreboard - is asked about first)
    F['tick'][0:0] = ['execute as @a unless score @s bm.pid matches 1.. run function bm:p279/guard']

    # ---- THE SNAPSHOT: chunk k of the objectives into w.s, then into p<pid>.s
    chunks = [objs[i:i + CHUNK] for i in range(0, len(objs), CHUNK)]
    N = len(chunks)
    for k, ch in enumerate(chunks):
        fn(f'p279/snap/c{k}', ['data remove storage bm:safe w'] +
           [f'execute if score @s {o} matches -2147483648.. store result storage bm:safe w.s.{q(o)} int 1 run scoreboard players get @s {o}' for o in ch] +
           ['function bm:p279/id/key', 'function bm:p279/snap/put with storage bm:safe t'])
    fn('p279/snap/put', ['$data modify storage bm:safe p$(pid).s merge from storage bm:safe w.s'])
    fn('p279/snap/last', ['data modify storage bm:safe w.tags set from entity @s Tags', 'function bm:p279/id/key',
                          'execute store result storage bm:safe t.gt int 1 run time query gametime',
                          'function bm:p279/snap/lastm with storage bm:safe t', 'function bm:p279/id/rec'])
    fn('p279/snap/lastm', ['$data modify storage bm:safe p$(pid).tags set from storage bm:safe w.tags',
                           '$data modify storage bm:safe p$(pid).pw set from storage bm:pw p$(pid)',
                           '$data modify storage bm:safe p$(pid).t set value $(gt)'])
    step = ['scoreboard players add @s bm.sft 1',
            # (its Pack ID mismatched with the registry's - put right before anything is kept over the good copy)
            'function bm:p279/guard',
            f'execute if score @s bm.sft matches {EVERY}.. run scoreboard players set @s bm.sfk 0',
            f'execute if score @s bm.sft matches {EVERY}.. run scoreboard players set @s bm.sft 0',
            f'execute unless score @s bm.sfk matches 0..{N} run return 0'] + \
           [f'execute if score @s bm.sfk matches {k} run function bm:p279/snap/c{k}' for k in range(N)] + \
           [f'execute if score @s bm.sfk matches {N} run function bm:p279/snap/last', 'scoreboard players add @s bm.sfk 1']
    fn('p279/step', step)
    # (a player new to this: their first snapshot starts at once)
    F['loop/second'][-1:-1] = ['execute as @a[gamemode=!spectator] if score @s bm.pid matches 1.. unless score @s bm.sft matches 0.. run scoreboard players set @s bm.sft 0',
                               'execute as @a if score @s bm.pid matches 1.. if score @s bm.sft matches 0.. run function bm:p279/step']

    # ---- THE RESTORE: lost scores (unset only), lost tags, the Pack's rows
    for k, ch in enumerate(chunks):
        fn(f'p279/rest/c{k}', [f'execute unless score @s {o} matches -2147483648.. if data storage bm:safe w.s.{q(o)} store result score @s {o} run data get storage bm:safe w.s.{q(o)}' for o in ch])
    fn('p279/rest_due', ['execute as @a[tag=bm.sfrest] run function bm:p279/rest_one'])
    fn('p279/rest_one', ['tag @s remove bm.sfrest', 'function bm:p279/restore'])
    fn('p279/restore', ['function bm:p279/id/key', 'data remove storage bm:safe w', 'function bm:p279/rest/get with storage bm:safe t',
                        'execute unless data storage bm:safe w.s run return 0'] +
       [f'function bm:p279/rest/c{k}' for k in range(N)] +
       ['function bm:p279/rest/tags', 'function bm:admin/rp_relink',
        # (the next snapshot waits a full cycle: the restored state is kept, not the empty one)
        'scoreboard players set @s bm.sft 1', f'scoreboard players set @s bm.sfk {N + 1}'])
    fn('p279/rest/get', ['$data modify storage bm:safe w.s set from storage bm:safe p$(pid).s', '$data modify storage bm:safe w.tags set from storage bm:safe p$(pid).tags'])
    fn('p279/rest/tags', ['execute unless data storage bm:safe w.tags[0] run return 0', 'data modify storage bm:safe w.tg set from storage bm:safe w.tags[0]',
                          'function bm:p279/rest/tag with storage bm:safe w', 'data remove storage bm:safe w.tags[0]', 'function bm:p279/rest/tags'])
    fn('p279/rest/tag', ['$tag @s add $(tg)'])

    # ---- ADMIN
    fn('admin/safe_restore', ['function bm:p279/id/get',
                              'execute if score #sid bm.rng matches 1.. run scoreboard players operation @s bm.pid = #sid bm.rng',
                              'execute unless score @s bm.pid matches 1.. run return run ' + tellraw('@s', PRE + [T('Nothing kept for you yet.', 'gray')]),
                              'function bm:p279/restore',
                              tellraw('@s', PRE + [T('Restored from your last snapshot: ', 'gray'), T('your Pack ID, every score and tag you had lost, and your Rat Pack\'s rows.', 'white')])])
    fn('admin/safe_pack', ['function bm:p179/w/pid', 'execute store result storage bm:safe t.pid int 1 run scoreboard players get @s bm.pid',
                           'function bm:p279/pack with storage bm:safe t', 'function bm:admin/rp_relink'])
    fn('p279/pack', ['$execute unless data storage bm:safe p$(pid).pw run return run ' + tellraw('@s', PRE + [T('No copy of your Rat Pack kept yet.', 'gray')]),
                     '$data modify storage bm:safe w.pw set from storage bm:pw p$(pid)',
                     '$data modify storage bm:pw p$(pid) set from storage bm:safe p$(pid).pw',
                     '$data modify storage bm:pw p$(pid) merge from storage bm:safe w.pw',
                     tellraw('@s', PRE + [T('Your Rat Pack has everything it held at the last snapshot again', 'white'), T(' (and everything it holds now).', 'gray')])])
    fn('admin/safe_status', ['function bm:p279/id/get', 'function bm:p279/id/key',
                             tellraw('@s', PRE + [T('Your Pack ID: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.pid'}, 'color': 'white'},
                                                  T(' · in the registry: ', 'gray'), {'score': {'name': '#sid', 'objective': 'bm.rng'}, 'color': 'white'},
                                                  T(' · next snapshot in ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.sft'}, 'color': 'white'},
                                                  T(f' of {EVERY} s', 'gray')])])
    for c, d in (('safe_restore', 'put back your Pack ID, every score and tag you lost, and your Rat Pack\'s rows (from the last snapshot)'),
                 ('safe_pack', 'put back anything your Rat Pack held at the last snapshot and no longer holds'),
                 ('safe_status', 'your Pack ID, the registry\'s, and the snapshot clock')):
        F['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{c}', 'yellow'), T(f'  {d}', 'gray')]))
    F['admin/uninstall'][0:0] = ['scoreboard players reset * bm.sfk', 'scoreboard players reset * bm.sft']
    return len(objs), N
