"""3.0g: PROTECTED GROUND, FOR EVERYONE - the owner: "I keep getting spammed on my hotbar that blocks can't be broken. Yet I can
break blocks in every protected area. Could it be because I'm OP? I'm playing on a multi-player server."

Every protected place (a market's or a crypt's floors, a dungeon, a ship, the Kingdom, the Undercrown, the Armada, the Loom
Sanctuary, the Locker Hall, the Lounge, the Gutter) protects the same way: a survival player in it is put in Adventure mode,
under the place's own tag (IN), and the place puts them back in Survival when they leave. Operator status plays no part
anywhere (no selector or command here looks at it); CREATIVE (and spectator) players are left alone by design - that's how
an operator builds in a market.

What went wrong is a player whose switch to Adventure didn't stick - whatever turned them back to Survival (another place's
"you left" that ran while they were still in this one, a server plugin or mod that enforces a game mode, an operator's own
/gamemode survival): the market's sweep then dropped their tag every tick (bm.adv with no Adventure mode) and its way in ran
again - its "Protected ground" line on the action bar twenty times a second - while they, in Survival, could break anything.
Now:
  THE TAG STAYS   a player in Survival keeps their protected place's tag (only Creative or Spectator drops the market's): its
                  way in doesn't run again, its way out still does when they leave.
  THE LOCK        a Survival player holding any place's tag (STUCK) is LOCKED, every fast loop: their block-breaking speed set
                  to nothing (an attribute modifier, bm:guard_nobreak - it works whatever their game mode or permissions) and
                  Adventure asked for again; unlocked the moment they're in Adventure, out of every place, or in Creative.
  THE WORD        each place's action-bar word on the way in is said once, then not again for MSG_CD seconds (bm.gdmsg) - a
                  way in that runs every second for someone it can't switch says it once.
"""
from items import T

# each place's way in (the function that switches a player to Adventure mode there) and the tag it gives them
IN = {'zone/enter': 'bm.adv', 'p148/ship/enter': 'bm.advs', 'p199/adv/in': 'bm.kadv', 'p237/adv/in': 'bm.uadv', 'p241/adv/in': 'bm.aadv',
      'p253/adv/in': 'bm.kbadv', 'p84/lk/adv': 'bm.lkadv', 'p121/adv': 'bm.lgadv', 'p74/vault_adv': 'bm.gvadv'}
MSG_CD = 15
MOD = 'bm:guard_nobreak'


def generate(G):
    fn, title = G.fn, G.title
    n_msg = 0
    tags = []
    for f, tag in IN.items():
        L = G.FUNCS.get(f)
        if L is None: continue
        tags.append(tag)
        for i, l in enumerate(L):
            if l.startswith('title @s actionbar '):
                L[i] = 'execute unless score @s bm.gdmsg matches 1.. run ' + l; n_msg += 1
        L.append(f'scoreboard players set @s bm.gdmsg {MSG_CD}')
    assert 'bm.adv' in tags, 'the market zone\'s way in (zone/enter) is gone'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gdmsg dummy']
    G.OBJECTIVES.append('bm.gdmsg')
    G.FUNCS['loop/second'][-1:-1] = ['scoreboard players remove @a[scores={bm.gdmsg=1..}] bm.gdmsg 1']
    # the tag stays on a player in Survival (the market's sweep dropped it from anyone not in Adventure)
    fast = G.FUNCS['loop/fast']
    old = 'tag @a[tag=bm.adv,gamemode=!adventure] remove bm.adv'
    assert old in fast, 'the market zone\'s tag sweep moved (guard.py keeps it from dropping a Survival player\'s tag)'
    new_sweep = 'tag @a[tag=bm.adv,gamemode=!adventure,gamemode=!survival] remove bm.adv'
    fast[fast.index(old)] = new_sweep
    # the lock
    fn('guard/stuck', [f'execute if entity @s[gamemode=survival,tag={t}] run return 1' for t in tags] + ['return fail'])
    fn('guard/lock', ['tag @s add bm.gdlk', f'attribute @s minecraft:block_break_speed modifier add {MOD} -1 add_multiplied_total', 'gamemode adventure @s'])
    fn('guard/unlock', ['tag @s remove bm.gdlk', f'attribute @s minecraft:block_break_speed modifier remove {MOD}'])
    lock = [f'execute as @a[tag={t},gamemode=survival,tag=!bm.gdlk] run function bm:guard/lock' for t in tags] + \
           ['execute as @a[tag=bm.gdlk,gamemode=survival] run gamemode adventure @s',
            'execute as @a[tag=bm.gdlk] unless function bm:guard/stuck run function bm:guard/unlock']
    # (3.0i) THE MARKET'S AND THE CRYPTS' WAY IN, ON ITS OWN CLOCK, BY WHERE YOU STAND. The owner, an operator on a server, on a
    #  team: "in Survival when I enter, and no message" - the way in never ran. It lived in loop/fast, among a thousand lines, and
    #  asked for no market tag (bm.adv) on you: a loop that stops re-arming itself (a run cut short at the server's command limit,
    #  a line its version can't read) or a tag left on from before kept it from ever running. Now the way in, the way out, the
    #  tag sweep and the lock run in zone/tick (the game's own tick tag, every 4 ticks - no schedule to lose, nothing else in it),
    #  and a Survival player on a protected floor by a zone marker is let in whatever tags they hold.
    zl = [l for l in fast if l.endswith('run function bm:zone/enter') or l.endswith('run function bm:zone/exit') or l == new_sweep]
    assert len(zl) >= 4, zl
    for l in zl: fast.remove(l)
    zl = [l.replace('@a[gamemode=survival,tag=!bm.adv]', '@a[gamemode=survival]') for l in zl]
    fn('zone/tick', ['scoreboard players add #zt bm.timer 1', 'execute if score #zt bm.timer matches ..3 run return 0', 'scoreboard players set #zt bm.timer 0'] +
       zl + lock)
    # (and the loops re-arm themselves first: a run cut short still comes round again)
    for name in ('loop/fast', 'loop/second', 'loop/second_b'):
        L = G.FUNCS.get(name)
        if not L: continue
        sch = [l for l in L if l.startswith(f'schedule function bm:{name} ')]
        if len(sch) == 1:
            L.remove(sch[0]); L.insert(0, sch[0])
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.gdlk] run function bm:guard/unlock']
    return n_msg, len(tags)
