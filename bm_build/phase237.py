"""2.98: THE UNDERCROWN - the final dungeon, hidden in the Nether (p2/dungeons/undercrown.py builds it; p2/undercfg.py holds
what's shared; undercrown_lore.py says everything it says). Its master's fight is phase238's; what's left of him, phase239's.

FINDING IT   hard mode. Beat all three Dread bosses (bm.dbwin_snow/witch/shark) and a voice speaks - "You broke my three.
             Come, then." - and THE SOVEREIGN'S SUMMONS is yours: a compass that, in the Nether, points to the Undercrown (one
             per world, at undercfg.ORIGIN, cut into the rock; placed - and re-placed - by command). Outside, it is a cliff in an
             ash cave with a seam of crying obsidian; stand at the seam carrying the three Dread Tokens and it opens.
INSIDE       it is a Phase 2 dungeon (p2/logic runs its seventeen trials, gates, secret doors, waves and vaults; a 20-minute idle
             reset re-locks it) with kinds of its own (logic.EXTRA):
  SIGIL      a follower's emblem in the floor: lit while that follower (anyone's) stands on it. All of a trial's lit at once:
             solved. The three wards are sealed by the trios their Dread bosses demanded (whoever got here has all nine).
  ECHO       walk into its room and the echo of a Dread boss rises (phase197's own boss, tagged bm.dbecho: weaker, nameless
             spoils); it falls -> solved, and everyone near gets its CROWN SHARD and an Undercrown Key.
  SHARDS     the Throne Gate: drop each Crown Shard on its socket.
             Bridges (bm.ubridge) appear when their trial is solved. Wave foes are DREAD (dressed by phase176's p176/mk/<type>).
THE STAIR OF A THOUSAND EYES (trial 17, a reach): the lids open every few seconds; anyone who MOVES while they're open is caught
             (Darkness, a wound, and Dread Knights step out of the walls). Move while they're shut.
HIDDEN ROOMS (undercfg.HIDDEN) open while their followers stand on their sigils by the door; each has a relic pedestal - its
             BLACK SEAL (once a player each rebuild) and its relic (once a player, ever) - and a chest. Two classic secret doors.
             Six Black Seals open THE SOVEREIGN'S HOARD behind the throne, after the fall.
             The Lantern Crawl is pitch dark (Darkness and Blindness) - unless the Arachno-Lantern is with you.
THE FALL     (phase238 calls p237/collapse) three minutes to loot - then everyone inside is carried out and the whole Undercrown
             is REBUILT: every block, chest, trial, sigil, shard and seal as it was.
THE DREAD NIGHTS END when it falls (#dfell bm.cfg): none is rolled, none can be rung. THE DREAD EMBER (its spoils) kindles them
             again - and, kindled again, puts them out.
RELICS       Dawnshard (held: the great eye's beam can't touch you - phase238), Page of Unwriting (monsters near lose you),
             Sovereign's Chain (a whip: reach, and a hit drags the foe in - phase238), Ninth Life (a fall a day), the Lantern's Wick
             (off hand: see in the dark, monsters within 16 glow), the Unbound Knight's Helm."""
import json
import math
from items import T, ITEMS
from nbt import snbt, B, F, Int
from structures import Build
import p2.undercfg as U
import undercrown_lore as L

d = U.d
COL, VCOL = L.SOV_COL, L.VOICE_COL
OX, OY, OZ = U.ORIGIN
SX, SY, SZ = U.SIZE
NETHER = 'minecraft:the_nether'
BOX = f'x={OX},y={OY},z={OZ},dx={SX - 1},dy={SY - 1},dz={SZ - 1}'
UVER = 1                                  # bump to re-place the Undercrown in every world (a rebuild: everyone inside is carried out)
COLLAPSE = 180                            # seconds between its fall and the rebuild
EYE = (110, 130, 160)                     # the eyes' cycle (ticks): shut .. twitch (warning) .. open .. (round again)
TOKENS = {'snow': 'tok_frost', 'witch': 'tok_hex', 'shark': 'tok_saw'}
TOK_COL = {'snow': '0.6,0.85,1.0', 'witch': '0.48,1.0,0.35', 'shark': '1.0,0.82,0.1'}
ECHO_HP = 380                             # (an echo's real pool - over phase197's FLOOR)
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
W = lambda x, y, z: (OX + x, OY + y, OZ + z)          # local -> world
BUILT = {}
# what a rebuild clears out of the box: only what the Undercrown itself made (never a follower or its parts)
CLEAR = [f'type=minecraft:marker,tag=bm.d_{d}', 'tag=bm.usgt', 'tag=bm.ushow', 'tag=bm.urelic_d', 'tag=bm.urelic_i', 'tag=bm.ueyed', 'tag=bm.vbtext',
         'tag=bm.dgmob', 'tag=bm.udread', 'tag=bm.usov', 'tag=bm.dbecho', 'type=minecraft:item', 'type=minecraft:experience_orb', 'type=minecraft:arrow',
         'type=minecraft:spectral_arrow']
RELIC_NAME = {'dawnshard': 'the Dawnshard', 'ulantern_wick': "the Lantern's Wick", 'unwriting': 'the Page of Unwriting', 'chainwhip': "the Sovereign's Chain",
              'nine_lives': 'a Ninth Life', 'unbound_helm': "an Unbound Knight's Helm"}


def build():
    if 'B' not in BUILT:
        from p2.dungeons import undercrown
        BUILT['B'] = undercrown.build()
    return BUILT['B']


def who(k):
    import phase125 as P125
    return P125.WHO[k]


def host(k, r):
    """the follower k's host, within r - anyone's"""
    return f'@e[tag={who(k)[4]},distance=..{r}]'


# ================================================================== the trials' own kinds (p2/logic.EXTRA)
def _sigil(G, d_, n, c):
    from p2.logic import el_sel
    fn, title = G.fn, G.title
    R = c['R']
    sig = [t[6:] for e in c['els'] if e[0] == 'sigil' for t in e[4] if t.startswith('bm.sw_')]
    body = ['execute if score #act bm.rng matches 0 run return 0', 'scoreboard players set #sl bm.rng 0']
    for k in sig:
        s = lambda extra='': el_sel(d, n, 'sigil', R, f',tag=bm.sw_{k}{extra}')
        body += [f'execute as {s()} at @s if entity {host(k, 1.8)} run scoreboard players add #sl bm.rng 1',
                 f'execute as {s(",tag=!bm.lit")} at @s if entity {host(k, 1.8)} run function bm:p237/sigil/lit',
                 f'execute as {s(",tag=bm.lit")} at @s unless entity {host(k, 1.8)} run function bm:p237/sigil/out']
    body += [f'execute if score #sl bm.rng matches {len(sig)}.. run function bm:p2/{d}/pz{n}_solve']
    reset = ['scoreboard players set @s bm.done 0', f'tag {el_sel(d, n, "sigil", R)} remove bm.lit']
    return body, reset


def _echo(G, d_, n, c):
    from p2.logic import el_sel
    fn, title = G.fn, G.title
    k = c['p']['data']['k']; r = int(c['p']['data']['r'])
    nm, col, sub = L.ECHO[k]
    fn(f'p2/{d}/pz{n}_rise', ['scoreboard players set @s bm.wv 1',
                              f'execute as {el_sel(d, n, "echo", c["R"] + 4)} at @s run function bm:p237/echo/rise_{k}',
                              f'title @a[distance=..{r + 16}] times 10 60 20', title(f'@a[distance=..{r + 16}]', 'subtitle', T(sub, 'gray', italic=True)),
                              title(f'@a[distance=..{r + 16}]', 'title', T(nm, col, bold=True))])
    body = ['execute if score #act bm.rng matches 0 run return 0',
            # (it sank - everyone left, or died: it rises again for the next to walk in)
            'execute if score @s bm.wv matches 1.. unless entity @e[tag=bm.dbecho,distance=..96] run scoreboard players set @s bm.wv 0',
            f'execute unless score @s bm.wv matches 1.. if entity @a[distance=..{r},gamemode=!spectator,gamemode=!creative] run function bm:p2/{d}/pz{n}_rise']
    reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.wv 0',
             f'execute as @e[tag=bm.dbecho,distance=..96] at @s run function bm:p237/echo/gone']
    return body, reset


def _shards(G, d_, n, c):
    from p2.logic import el_sel
    fn, title = G.fn, G.title
    R = c['R']
    body = ['execute if score #act bm.rng matches 0 run return 0',
            f'execute as {el_sel(d, n, "socket", R, ",tag=!bm.got")} at @s run function bm:p2/{d}/pz{n}_offer']
    off = []
    for k, sid in U.SHARD.items():
        off.append(f'execute if entity @s[tag=bm.ok_{k}] as @e[type=minecraft:item,distance=..1.6] if items entity @s contents {holds(sid)} run function bm:p2/{d}/pz{n}_take_{k}')
        fn(f'p2/{d}/pz{n}_take_{k}', ['kill @s', f'execute as {el_sel(d, n, "socket", 3, f",tag=bm.ok_{k},sort=nearest,limit=1")} at @s run function bm:p237/shard/set_{k}',
                                      f'execute as {c["ctrl"]} at @s run function bm:p2/{d}/pz{n}_tally'])
    fn(f'p2/{d}/pz{n}_offer', off)
    fn(f'p2/{d}/pz{n}_tally', [f'execute store result score #h bm.rng if entity {el_sel(d, n, "socket", R, ",tag=bm.got")}',
                               f'execute if score #h bm.rng matches 3.. run return run function bm:p237/shard/all',
                               title('@a[distance=..20]', 'actionbar', [T('The Throne Gate takes the shard: ', COL), {'score': {'name': '#h', 'objective': 'bm.rng'}, 'color': 'white'}, T(' / 3', COL)])])
    fn('p237/shard/all', ['execute as @a[distance=..24,gamemode=!spectator] run function bm:p237/key',
                          f'execute as {c["ctrl"]} at @s run function bm:p2/{d}/pz{n}_solve'])
    reset = ['scoreboard players set @s bm.done 0', f'tag {el_sel(d, n, "socket", R)} remove bm.got',
             f'execute as {el_sel(d, n, "socket", R)} at @s run kill @e[type=minecraft:item_display,tag=bm.ushow,distance=..2]']
    return body, reset


def setup():
    """(import time) the kinds, the items' extra parts"""
    from p2 import logic
    logic.EXTRA.update(sigil=_sigil, echo=_echo, shards=_shards)


setup()


# ================================================================== generate
def generate(G):
    fn, title, tellraw, give, wjson = G.fn, G.title, G.tellraw, G.give, G.wjson
    tick, fast, second = G.FUNCS['tick'], G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = G.PREFIX
    U.register()
    Bu = build()
    M = Bu.meta['under']
    Bu.export(G.path('data', 'bm', 'structure', 'p2_under.nbt'))
    # the arena's floor on its own: the fight puts back what fell (phase238: p237/floor)
    a = U.ARENA; acx, _, acz = a['c']; ar = a['r']; fy0, fy1 = a['floor']
    FL = Build(2 * ar + 1, fy1 - fy0 + 1, 2 * ar + 1)
    for (x, y, z), st in Bu.b.items():
        if fy0 <= y <= fy1 and abs(x - acx) <= ar and abs(z - acz) <= ar and 'air' not in st:
            FL.set(x - acx + ar, y - fy0, z - acz + ar, st, Bu.nbt.get((x, y, z)))
    FL.export(G.path('data', 'bm', 'structure', 'p2_under_floor.nbt'))
    fx0, fy0w, fz0 = W(acx - ar, fy0, acz - ar)
    fn('p237/floor', [f'execute in {NETHER} run place template bm:p2_under_floor {fx0} {fy0w} {fz0}'])

    objs = ['bm.uex', 'bm.uey', 'bm.uez', 'bm.u9cd', 'bm.uucd'] + [f'bm.urs_{k}' for k in U.HIDDEN]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        'execute unless score #uver bm.p2 matches 0.. run scoreboard players set #uver bm.p2 0',
        'execute unless score #urun bm.p2 matches 1.. run scoreboard players set #urun bm.p2 1',
        'execute unless score #dfell bm.cfg matches 0.. run scoreboard players set #dfell bm.cfg 0']
    G.OBJECTIVES += objs

    # ---- the framework runs it (only its own lines: the shared ones are already there)
    from p2 import logic
    parts = logic.generate(G, {d: Bu})
    mine = lambda ls: [l for l in ls if f'd_{d}' in l]
    tick += mine(parts['tick'])
    second[-1:-1] = mine(parts['second'])
    k = fast.index('scoreboard players reset @a bm.sneak')
    fast[k:k] = mine(parts['fast'])
    # its floors are dungeon floors (adventure mode)
    pth = G.path('data', 'bm', 'tags', 'block', 'dungeon_floor.json')
    floors = set(json.load(open(pth))['values'])
    for (x, y, z), st in Bu.b.items():
        if 'air' in st and (x, y - 1, z) in Bu.b:
            below = Bu.b[(x, y - 1, z)].split('[')[0]
            if 'air' not in below and 'light' not in below and 'lava' not in below and 'reinforced' not in below: floors.add(below)
    wjson('bm/tags/block/dungeon_floor.json', {'values': sorted(floors)})

    # ---- sigils: lit and out
    fn('p237/sigil/lit', ['tag @s add bm.lit', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.4 0.1 0.4 0.02 20', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.8 0.1 0.01 10',
                          'playsound minecraft:block.respawn_anchor.charge block @a[distance=..16] ~ ~ ~ 0.8 1.2',
                          title('@a[distance=..12]', 'actionbar', T('A sigil kindles under its follower...', COL, italic=True))])
    fn('p237/sigil/out', ['tag @s remove bm.lit', 'playsound minecraft:block.respawn_anchor.deplete block @a[distance=..12] ~ ~ ~ 0.6 1.4'])
    # every sigil (a trial's or a hidden room's) wears its follower's name, and burns while lit
    for k in sorted({s[4] for s in M['sigils']} | {w_[0] for h in M['hidden'].values() for w_ in h['sigils']}):
        nm, _pr, c = who(k)[:3]
        txt = {'Tags': ['bm.usgt', 'bm.p2'], 'billboard': 'center', 'see_through': B(0), 'background': Int(0), 'shadow': B(1),
               'text': T(nm.upper(), c, bold=True), 'brightness': {'block': Int(10), 'sky': Int(10)},
               'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                  'translation': [F(0), F(0.15), F(0)], 'scale': [F(0.8), F(0.8), F(0.8)]}}
        fn(f'p237/sigil/name_{k}', [f'summon minecraft:text_display ~ ~0.1 ~ {snbt(txt)}'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.d_{d},tag=bm.sw_{k},tag=!bm.uon] at @s run function bm:p237/sigil/name_{k}')
    second.append(f'tag @e[type=minecraft:marker,tag=bm.d_{d},tag=!bm.uon,tag=bm.pet_sigil] add bm.uon')
    second.append(f'tag @e[type=minecraft:marker,tag=bm.d_{d},tag=!bm.uon,tag=bm.uhsg] add bm.uon')
    fast.append(f'execute as @e[type=minecraft:marker,tag=bm.d_{d},tag=bm.lit] at @s run particle minecraft:dust{{color:[0.82,0.1,0.18],scale:1.6}} ~ ~0.1 ~ 0.6 0 0.6 0 6')

    # ---- bridges appear when their trial is solved; the reset takes them back
    fn('p237/bridge/make', ['$fill ~ ~ ~ ~$(dx) ~$(dy) ~$(dz) $(b) replace minecraft:air', 'particle minecraft:snowflake ~ ~1 ~ 3 1 3 0.02 60',
                            'playsound minecraft:block.glass.place block @a[distance=..32] ~ ~ ~ 1 0.6', 'playsound minecraft:block.powder_snow.place block @a[distance=..32] ~ ~ ~ 1 0.5'])
    fn('p237/bridge/clear', ['$fill ~ ~ ~ ~$(dx) ~$(dy) ~$(dz) minecraft:air replace $(b)'])
    for n in sorted({b_[0] for b_ in M['bridges']}):
        G.FUNCS[f'p2/{d}/pz{n}_solve'].insert(2, f'execute as @e[type=minecraft:marker,tag=bm.ubridge,tag=bm.g{n},tag=bm.d_{d},distance=..340] at @s run function bm:p237/bridge/make with entity @s data')
    # ---- the echoes: phase197's own Dread bosses, weaker, with nothing of their own to give
    import phase197 as P197
    for k, b in P197.BOSSES.items():
        nm, col, _ = L.ECHO[k]
        fn(f'p237/echo/rise_{k}', [f'function bm:p197/{k}/rise', f'execute as @e[tag=bm.db_{k},tag=!bm.dbecho,distance=..12,sort=nearest,limit=1] run function bm:p237/echo/init_{k}'])
        fn(f'p237/echo/init_{k}', ['tag @s add bm.dbecho', f'attribute @s minecraft:max_health base set {ECHO_HP + P197.FLOOR}',
                                   f'data modify entity @s Health set value {ECHO_HP + P197.FLOOR}.0f', f'data modify entity @s CustomName set value {snbt(T(nm, col))}',
                                   f'bossbar set bm:db_{k} name {snbt(T(nm, col))}', f'bossbar set bm:db_{k} max {ECHO_HP}',
                                   'particle minecraft:sculk_soul ~ ~2 ~ 1 1.5 1 0.05 60'])
        G.FUNCS[f'p197/{k}/rise'] += [f'bossbar set bm:db_{k} name {snbt(T(b["NAME"], b["COL"]))}', f'bossbar set bm:db_{k} max {b["hp"]}']
        G.FUNCS[f'p197/{k}/fall'].insert(0, f'execute if entity @s[tag=bm.dbecho] run return run function bm:p237/echo/fall_{k}')
        fn(f'p237/echo/fall_{k}', ['particle minecraft:sculk_soul ~ ~2 ~ 1.5 2 1.5 0.08 120', 'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
                                   'playsound minecraft:entity.warden.death hostile @a[distance=..64] ~ ~ ~ 1 0.6',
                                   tellraw('@a[distance=..64]', [T(L.FIGHT[f'echo_{k}'], VCOL, italic=True)]),
                                   f'execute as @a[distance=..64,gamemode=!spectator] run function bm:p237/echo/spoils_{k}',
                                   f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pzt_echo,tag=bm.d_{d},distance=..96,sort=nearest,limit=1] at @s run function bm:p237/echo/won',
                                   f'function bm:p197/{k}/sink'])
        fn(f'p237/echo/spoils_{k}', [give(U.SHARD[k]), 'function bm:p237/key', G.give('dread_token', 2),
                                     tellraw('@s', P + [T(L.ITEMS[f'shard_{k}'][0], COL, bold=True), T(' - set it in the Throne Gate, at the bottom of the Hall of Chains.', 'gray')])])
    fn('p237/echo/won', [f'execute if entity @s[tag=bm.pz{n}] run function bm:p2/{d}/pz{n}_solve' for n in U.ECHO_OF])
    fn('p237/echo/gone', ['scoreboard players operation #id bm.rng = @s bm.dbid',
                          'execute as @e[type=minecraft:item_display,tag=bm.dbr] if score @s bm.dbid = #id bm.rng run kill @s', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p237/key', [give('ukey'), 'playsound minecraft:block.vault.insert_item player @s ~ ~ ~ 0.8 1.2'])
    # ---- the Throne Gate's shards, set in their sockets
    for k, sid in U.SHARD.items():
        disp = {'Tags': ['bm.ushow'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{sid}'}},
                'billboard': 'vertical', 'brightness': {'block': Int(14), 'sky': Int(14)},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(0.7), F(0)], 'scale': [F(0.8), F(0.8), F(0.8)]}}
        fn(f'p237/shard/set_{k}', ['tag @s add bm.got', f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.4 0.3 0.04 20',
                                   'playsound minecraft:block.end_portal_frame.fill block @a[distance=..16] ~ ~ ~ 1 0.6'])

    # ---- the Dread in its waves are Dread (phase176 dresses them)
    mk = [f'execute if entity @s[tag=bm.udk_{t}] run function bm:p176/mk/{t}' for t in ('zombie', 'skeleton', 'stray', 'husk', 'vindicator', 'wither_skeleton', 'spider')
          if f'p176/mk/{t}' in G.FUNCS]
    fn('p237/dress', mk + ['tag @s add bm.dread', 'tag @s add bm.udone'])
    tick.append('execute as @e[tag=bm.udread,tag=!bm.udone] run function bm:p237/dress')

    # ---- the dungeon's voice: one line to each player, the first time they come near
    for key in sorted({v[0] for v in M['voices']}):
        fn(f'p237/voice/{key}', [f'tag @s add bm.uv_{key}', tellraw('@s', [T(L.VOICE[key], VCOL, italic=True)]),
                                 'playsound minecraft:entity.warden.nearby_closer hostile @s ~ ~ ~ 0.7 0.5'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.uv_{key}] at @s as @a[distance=..7,tag=!bm.uv_{key},gamemode=!spectator] run function bm:p237/voice/{key}')

    # ================================================================== FINDING IT: the Summons, the Hidden Gate
    ox_, oy_, oz_ = W(*M['outer']) if M['outer'] else W(205, 96, 205)
    ITEMS['usummons']['comps']['minecraft:lodestone_tracker'] = {'target': {'dimension': NETHER, 'pos': __import__('nbt').IntArray([ox_, oy_, oz_])}, 'tracked': B(0)}
    second.append('execute if score #hard bm.cfg matches 1 as @a[tag=!bm.usum,scores={bm.dbwin_snow=1..,bm.dbwin_witch=1..,bm.dbwin_shark=1..}] at @s run function bm:p237/summons')
    fn('p237/summons', ['tag @s add bm.usum', give('usummons'), 'scoreboard players set #uwant bm.p2 1',
                        'title @s times 10 80 30', title('@s', 'subtitle', T('Something under the Nether has noticed what you did.', 'gray', italic=True)),
                        title('@s', 'title', T(L.VOICE['gate'], VCOL, italic=True)),
                        'playsound minecraft:entity.warden.emerge hostile @s ~ ~ ~ 1 0.5', 'playsound minecraft:block.bell.resonate hostile @s ~ ~ ~ 1 0.4',
                        tellraw('@s', P + [T('The Sovereign\'s Summons', COL, bold=True), T(' is in your pack: in the Nether, it points to the Undercrown. ', 'gray'),
                                           T('Bring the three Dread Tokens.', COL)])])
    # the gate opens for anyone at the seam carrying all three tokens - or anyone coming out
    has = lambda t: f'if items entity @s container.* {holds(t)}'
    fn('p237/gate/has', [f'execute {has(TOKENS["snow"])} {has(TOKENS["witch"])} {has(TOKENS["shark"])} run return 1', 'return 0'])
    fn('p237/gate/tick', ['scoreboard players set #go bm.rng 0',
                          'execute as @a[distance=..4,gamemode=!spectator] if function bm:p237/gate/has run scoreboard players set #go bm.rng 1',
                          'execute as @a[distance=..4,gamemode=!spectator,tag=bm.uin] run scoreboard players set #go bm.rng 1',
                          'execute if score #go bm.rng matches 1 unless entity @s[tag=bm.open] run function bm:p237/gate/open',
                          'execute if entity @s[tag=bm.open] unless entity @a[distance=..14] run function bm:p237/gate/close',
                          'execute unless entity @s[tag=bm.open] if entity @a[distance=..5] unless score #go bm.rng matches 1 run function bm:p237/gate/barred'])
    fn('p237/gate/open', ['tag @s add bm.open', 'function bm:p237/door/open with entity @s data',
                          'playsound minecraft:block.respawn_anchor.deplete block @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:entity.warden.sonic_charge block @a[distance=..24] ~ ~ ~ 0.6 0.4',
                          'particle minecraft:dust{color:[0.82,0.1,0.18],scale:2} ~ ~2 ~ 1 1.5 1 0 60',
                          title('@a[distance=..10]', 'actionbar', T('The seam weeps itself open.', COL, italic=True))])
    fn('p237/gate/close', ['tag @s remove bm.open', 'function bm:p237/door/close with entity @s data'])
    fn('p237/gate/barred', ['scoreboard players set #gb bm.rng 0', 'execute as @a[distance=..5,tag=!bm.usum] run scoreboard players set #gb bm.rng 1',
                            'execute if score #gb bm.rng matches 1 run return run ' + title('@a[distance=..5]', 'actionbar', T('A seam of crying obsidian in the cliff. It does not know you.', 'gray', italic=True)),
                            title('@a[distance=..5]', 'actionbar', T('Three hollows in the rock, waiting. (Carry the three Dread Tokens.)', COL, italic=True))])
    # a door of marker data {ax, w, h, b}, opened (air) and shut (its block) - the gate, the hidden rooms, the Hoard
    for nm_, a_, b_ in (('open', '$(b)', 'minecraft:air'), ('close', 'minecraft:air', '$(b)')):
        fn(f'p237/door/{nm_}', ['$execute if data entity @s data{ax:"x"} run fill ~-$(w) ~ ~ ~$(w) ~' + '$(hh)' + f' ~ {b_} replace {a_}',
                                '$execute if data entity @s data{ax:"z"} run fill ~ ~ ~-$(w) ~ ~' + '$(hh)' + f' ~$(w) {b_} replace {a_}'])
    second.append(f'execute in {NETHER} as @e[type=minecraft:marker,tag=bm.ugate,{BOX}] unless data entity @s data.hh store result entity @s data.hh int 1 run data get entity @s data.h 0.999')
    second.append(f'execute in {NETHER} as @e[type=minecraft:marker,tag=bm.uhs,{BOX}] unless data entity @s data.hh store result entity @s data.hh int 1 run data get entity @s data.h 0.999')
    second.append(f'execute in {NETHER} as @e[type=minecraft:marker,tag=bm.uhoard,{BOX}] unless data entity @s data.hh store result entity @s data.hh int 1 run data get entity @s data.h 0.999')
    second.append('execute as @e[type=minecraft:marker,tag=bm.ugate] at @s if entity @a[distance=..16] run function bm:p237/gate/tick')
    for k, tok in TOKENS.items():
        fast.append(f'execute as @e[type=minecraft:marker,tag=bm.ugs_{k}] at @s if entity @a[distance=..6,gamemode=!spectator] run function bm:p237/gate/hollow_{k}')
        fn(f'p237/gate/hollow_{k}', ['scoreboard players set #hk bm.rng 0', f'execute as @a[distance=..6] {has(tok)} run scoreboard players set #hk bm.rng 1',
                                     f'execute if score #hk bm.rng matches 1 run particle minecraft:dust{{color:[{TOK_COL[k]}],scale:1.4}} ~ ~0.4 ~ 0.15 0.15 0.15 0 4',
                                     'execute if score #hk bm.rng matches 0 run particle minecraft:smoke ~ ~0.4 ~ 0.05 0.05 0.05 0 1'])
    # inside or out: anyone among its zone markers is "in" (the gate lets them out)
    second += [f'tag @a[tag=bm.uin] remove bm.uin',
               f'execute in {NETHER} as @a[{BOX}] at @s if entity @e[type=minecraft:marker,tag=bm.zone_d,tag=bm.d_{d},distance=..34] run tag @s add bm.uin']

    # ================================================================== THE PLACING (once; and again after every fall)
    sx, sz = SX // 16 + 1, SZ // 16 + 1
    fl = f'{OX - 8} {OZ - 8} {OX + SX + 8} {OZ + SZ + 8}'
    bio = []
    step = 56
    for bx in range(0, SX, step):
        for bz in range(0, SZ, step):
            bio.append(f'execute in {NETHER} run fillbiome {OX + bx} {OY} {OZ + bz} {OX + min(SX, bx + step) - 1} {OY + SY - 1} {OZ + min(SZ, bz + step) - 1} bm:undercrown')
    fn('p237/build/try', [f'execute in {NETHER} run forceload add {fl}',
                          f'execute in {NETHER} store success score #uload bm.p2 if loaded {OX} {OY} {OZ} if loaded {OX + SX - 1} {OY} {OZ + SZ - 1} if loaded {OX} {OY} {OZ + SZ - 1} if loaded {OX + SX - 1} {OY} {OZ}',
                          'execute unless score #uload bm.p2 matches 1 run return run scoreboard players set #uwait bm.p2 0',
                          'scoreboard players add #uwait bm.p2 1', 'execute unless score #uwait bm.p2 matches 4.. run return 0',
                          f'execute in {NETHER} as @a[{BOX}] run function bm:p237/out',
                          # (what the last copy left: its markers, displays, foes and dropped things - never anyone's follower)
                          *[f'execute in {NETHER} run kill @e[{s_},{BOX}]' for s_ in CLEAR],
                          'scoreboard players set #ubuilt bm.p2 0',
                          f'execute in {NETHER} store success score #ubuilt bm.p2 run place template bm:p2_{d} {OX} {OY} {OZ}',
                          'execute unless score #ubuilt bm.p2 matches 1 run return 0'] + bio + [
                          f'scoreboard players set #uver bm.p2 {UVER}', 'scoreboard players add #urun bm.p2 1', 'scoreboard players set #ufell bm.p2 0',
                          f'execute in {NETHER} run forceload remove {fl}'])
    second.append(f'execute if score #uwant bm.p2 matches 1 unless score #uver bm.p2 matches {UVER} unless score #ucol bm.p2 matches 1.. run function bm:p237/build/try')
    G.FUNCS['load'][-1:-1] = ['execute if entity @a[tag=bm.usum] run scoreboard players set #uwant bm.p2 1']
    # out: carried to the approach cave, outside the seam
    fn('p237/out', [f'execute in {NETHER} run tp @s {ox_ + 0.5} {oy_} {oz_ + 0.5}', 'tag @s remove bm.uin',
                    'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 30', 'playsound minecraft:block.respawn_anchor.deplete player @s ~ ~ ~ 0.6 1.4'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.urift] at @s as @a[distance=..1.3,gamemode=!spectator] run function bm:p237/out')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.urift] at @s if entity @a[distance=..24] run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.02 6')

    # ---- the fall: three minutes, then everyone out and the Undercrown re-formed (phase238 calls this)
    fn('p237/collapse', ['scoreboard players set #ufell bm.p2 1', f'scoreboard players set #ucol bm.p2 {COLLAPSE}',
                         f'execute in {NETHER} run ' + tellraw(f'@a[{BOX}]', [T('The Undercrown shudders. ', COL, bold=True),
                                                                             T(f'Without its master it will not hold its shape: in {COLLAPSE // 60} minutes it re-forms - and anyone still inside is carried out.', 'gray')])])
    fn('p237/collapse_sec', ['scoreboard players remove #ucol bm.p2 1',
                             *[f'execute if score #ucol bm.p2 matches {s} in {NETHER} run ' + title(f'@a[{BOX}]', 'actionbar', T(f'The Undercrown re-forms in {s} seconds.', COL))
                               for s in (120, 60, 30, 10, 5, 4, 3, 2, 1)],
                             'execute if score #ucol bm.p2 matches ..0 run scoreboard players set #uver bm.p2 0'])
    second.append('execute if score #ucol bm.p2 matches 1.. run function bm:p237/collapse_sec')

    # ---- the idle reset (20 minutes alone) re-locks what the framework doesn't know about
    G.FUNCS[f'p2/{d}/reset'] += [f'execute as @e[type=minecraft:marker,tag=bm.ubridge,tag=bm.d_{d},distance=..340] at @s run function bm:p237/bridge/clear with entity @s data',
                                 f'execute as @e[type=minecraft:marker,tag=bm.uhs,tag=bm.open,distance=..340] at @s run function bm:p237/hidden/close',
                                 f'kill @e[type=minecraft:item_display,tag=bm.ushow,distance=..340]',
                                 f'tag @e[type=minecraft:marker,tag=bm.d_{d},tag=bm.lit,distance=..340] remove bm.lit']

    # ================================================================== THE HIDDEN ROOMS
    for k, h in M['hidden'].items():
        title_, ws, relic = U.HIDDEN[k]
        req = [w_[0] for w_ in h['sigils']]
        lines = ['scoreboard players set #hs bm.rng 0']
        for w_ in req:
            lines.append(f'execute as @e[type=minecraft:marker,tag=bm.uhsg,tag=bm.uhs_{k},tag=bm.sw_{w_},distance=..40] at @s if entity {host(w_, 1.8)} run scoreboard players add #hs bm.rng 1')
        lines.append(f'execute if score #hs bm.rng matches {len(req)}.. run function bm:p237/hidden/open_{k}')
        fn(f'p237/hidden/try_{k}', lines)
        fn(f'p237/hidden/open_{k}', ['tag @s add bm.open', 'function bm:p237/door/open with entity @s data',
                                     'particle minecraft:end_rod ~ ~1.5 ~ 1 1.5 1 0.02 40', 'playsound minecraft:block.beacon.activate block @a[distance=..24] ~ ~ ~ 1 0.6',
                                     title('@a[distance=..16]', 'actionbar', [T(title_, '#c8a8ff', bold=True), T(' opens for its friends.', 'gray', italic=True)])])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.uhs_{k},tag=bm.uhs,tag=!bm.open] at @s if entity @a[distance=..20] run function bm:p237/hidden/try_{k}')
    fn('p237/hidden/close', ['tag @s remove bm.open', 'function bm:p237/door/close with entity @s data'])
    # the faint stir of a hidden sigil whose follower is near
    fast.append('execute as @e[type=minecraft:marker,tag=bm.uhsg] at @s if entity @a[distance=..10] run particle minecraft:soul ~ ~0.2 ~ 0.4 0 0.4 0.01 1')
    # ---- relic pedestals: the room's Black Seal (once a player each rebuild), its relic (once a player, ever)
    for k, (title_, ws, relic) in U.HIDDEN.items():
        disp = {'Tags': ['bm.urelic_d'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': ITEMS[relic]['comps'].get('minecraft:item_model', f'bm:{relic}')}},
                'billboard': 'vertical', 'brightness': {'block': Int(14), 'sky': Int(14)},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(0.9), F(0)], 'scale': [F(0.7), F(0.7), F(0.7)]}}
        fn(f'p237/relic/spawn_{k}', ['tag @s add bm.uon', f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}',
                                     f'summon minecraft:interaction ~ ~ ~ {{Tags:["bm.urelic_i","bm.urel_{k}"],width:1.0f,height:1.6f,response:1b}}'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.urel_{k},tag=!bm.uon] at @s run function bm:p237/relic/spawn_{k}')
        fn(f'p237/relic/take_{k}', [f'execute unless score @s bm.urs_{k} = #urun bm.p2 run function bm:p237/relic/seal_{k}',
                                    f'execute unless entity @s[tag=bm.urel_{k}] run function bm:p237/relic/first_{k}',
                                    'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 0.8 0.7'])
        fn(f'p237/relic/seal_{k}', [f'scoreboard players operation @s bm.urs_{k} = #urun bm.p2', give('ublack_seal'),
                                    tellraw('@s', [T('A Black Seal, ', '#8a7a8a', bold=True), T(f'from {title_}. ', 'gray'), T('Six of them open the Sovereign\'s Hoard.', 'dark_gray')])])
        fn(f'p237/relic/first_{k}', [f'tag @s add bm.urel_{k}', give(relic),
                                     tellraw('@s', P + [T(f'{title_}: ', '#c8a8ff', bold=True), T('you find ', 'gray'), T(RELIC_NAME[relic] + '.', 'white')])])
    fn('p237/relic/click', ['tag @s add bm.uhere', 'execute on target run function bm:p237/relic/take', 'tag @s remove bm.uhere', 'data remove entity @s interaction'])
    fn('p237/relic/take', [f'execute if entity @e[tag=bm.uhere,tag=bm.urel_{k}] run function bm:p237/relic/take_{k}' for k in U.HIDDEN])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.urelic_i] if data entity @s interaction at @s run function bm:p237/relic/click')
    # (the Last Light: the Lightbringer, if she's yours and here, remembers it)
    fn('p237/hidden/vigil', ['tag @s add bm.uvigil'] + [f'schedule function bm:p237/hidden/vigil{i} {40 + 60 * i}t' for i in range(3)])
    for i, line in enumerate(L.LAST_LIGHT):
        fn(f'p237/hidden/vigil{i}', [f'execute as @e[tag=bm.lhpet] at @s run ' + tellraw('@a[distance=..12]', [T('The Lightbringer: ', L.HOLY, bold=True), T(line, '#fff4d0', italic=True)])])
    second.append('execute as @e[type=minecraft:marker,tag=bm.uv_last_light] at @s as @a[distance=..8,tag=!bm.uvigil] at @s if entity @e[tag=bm.lhpet,distance=..12] run function bm:p237/hidden/vigil')
    # ---- the Lantern Crawl is pitch dark - unless the Arachno-Lantern is with you
    fn('p237/dark', ['$execute as @a[distance=..$(r),gamemode=!spectator] at @s unless entity @e[tag=bm.lnpet,distance=..10] run function bm:p237/dark_me'])
    fn('p237/dark_me', ['effect give @s minecraft:darkness 3 0 true', 'effect give @s minecraft:blindness 3 0 true',
                        'execute unless score @s bm.uucd matches -5.. run ' + title('@s', 'actionbar', T('You can\'t see your own hands. Something here wants a light.', 'gray', italic=True))])
    second.append('execute as @e[type=minecraft:marker,tag=bm.udark] at @s if entity @a[distance=..48] run function bm:p237/dark with entity @s data')

    # ================================================================== THE STAIR OF A THOUSAND EYES
    shut, twitch, open_ = EYE
    eye_d = lambda m: {'Tags': ['bm.ueyed'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': m}},
                       'brightness': {'block': Int(9), 'sky': Int(9)},
                       'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                          'translation': [F(0), F(0), F(-0.45)], 'scale': [F(1.4), F(1.4), F(0.2)]}}
    fn('p237/eyes/spawn', ['tag @s add bm.uon', f'summon minecraft:item_display ~ ~ ~ {snbt(eye_d("bm:ueye_shut"))}',
                           'execute rotated as @s run tp @e[type=minecraft:item_display,tag=bm.ueyed,distance=..0.1,limit=1] ~ ~ ~ ~ 0'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.ueye,tag=!bm.uon] at @s run function bm:p237/eyes/spawn')
    if M['eyes']:
        xs = [W(*e[:3]) for e in M['eyes']]
        x0, x1 = min(p[0] for p in xs) - 3, max(p[0] for p in xs) + 3
        y0, y1 = min(p[1] for p in xs) - 4, max(p[1] for p in xs) + 3
        z0, z1 = min(p[2] for p in xs) - 3, max(p[2] for p in xs) + 3
        STAIR = f'x={x0},y={y0},z={z0},dx={x1 - x0},dy={y1 - y0},dz={z1 - z0}'
    else:
        STAIR = 'distance=..0'
    fn('p237/eyes/tick', ['execute store result score #dpz bm.rng run scoreboard players get @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1,sort=nearest] bm.pz',
                          'execute unless score #dpz bm.rng matches 16 run return run scoreboard players set @s bm.at 0',
                          f'execute unless entity @a[{STAIR},gamemode=!spectator,gamemode=!creative] run return run scoreboard players set @s bm.at 0',
                          'scoreboard players add @s bm.at 1',
                          f'execute if score @s bm.at matches {shut} run function bm:p237/eyes/twitch',
                          f'execute if score @s bm.at matches {twitch} run function bm:p237/eyes/open',
                          f'execute if score @s bm.at matches {twitch}..{open_} run function bm:p237/eyes/watch',
                          f'execute if score @s bm.at matches {open_}.. run function bm:p237/eyes/shut'])
    fn('p237/eyes/twitch', [f'execute as @a[{STAIR}] at @s run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 1.2',
                            title(f'@a[{STAIR}]', 'actionbar', T('The lids twitch...', COL, italic=True)),
                            f'execute as @a[{STAIR}] run function bm:p237/eyes/mark'])
    fn('p237/eyes/open', [f'execute as @e[type=minecraft:item_display,tag=bm.ueyed,{STAIR}] run data modify entity @s item.components."minecraft:item_model" set value "bm:ueye_open"',
                          f'execute as @a[{STAIR}] at @s run playsound minecraft:entity.warden.nearby_closest hostile @s ~ ~ ~ 1 0.6',
                          title(f'@a[{STAIR}]', 'actionbar', T('THE EYES ARE OPEN. Do not move.', COL, bold=True)),
                          f'tag @a[{STAIR}] remove bm.ucaught'])
    fn('p237/eyes/shut', ['scoreboard players set @s bm.at 0',
                          f'execute as @e[type=minecraft:item_display,tag=bm.ueyed,{STAIR}] run data modify entity @s item.components."minecraft:item_model" set value "bm:ueye_shut"',
                          title(f'@a[{STAIR}]', 'actionbar', T('The eyes close. Move!', 'gray', italic=True))])
    fn('p237/eyes/mark', ['execute store result score @s bm.uex run data get entity @s Pos[0] 10', 'execute store result score @s bm.uey run data get entity @s Pos[1] 10',
                          'execute store result score @s bm.uez run data get entity @s Pos[2] 10'])
    fn('p237/eyes/watch', [f'execute as @a[{STAIR},gamemode=!spectator,gamemode=!creative,tag=!bm.ucaught] at @s run function bm:p237/eyes/check'])
    fn('p237/eyes/check', ['execute store result score #mx bm.rng run data get entity @s Pos[0] 10', 'execute store result score #mz bm.rng run data get entity @s Pos[2] 10',
                           'execute store result score #my bm.rng run data get entity @s Pos[1] 10',
                           'scoreboard players operation #mx bm.rng -= @s bm.uex', 'scoreboard players operation #mz bm.rng -= @s bm.uez', 'scoreboard players operation #my bm.rng -= @s bm.uey',
                           'execute unless score #mx bm.rng matches -3..3 run return run function bm:p237/eyes/caught',
                           'execute unless score #mz bm.rng matches -3..3 run return run function bm:p237/eyes/caught',
                           'execute unless score #my bm.rng matches -3..3 run return run function bm:p237/eyes/caught'])
    fn('p237/eyes/caught', ['tag @s add bm.ucaught', 'effect give @s minecraft:darkness 5 0', 'effect give @s minecraft:glowing 5 0 true',
                            'damage @s 4 minecraft:magic', 'playsound minecraft:entity.warden.roar hostile @a[distance=..24] ~ ~ ~ 0.8 0.7',
                            title('@s', 'actionbar', T('IT SAW YOU.', COL, bold=True)),
                            'execute store result score #kn bm.rng if entity @e[tag=bm.ueknight]',
                            'execute if score #kn bm.rng matches ..7 at @e[type=minecraft:marker,tag=bm.ueyesp,distance=..32,sort=nearest,limit=2] run function bm:p237/eyes/knight'])
    fn('p237/eyes/knight', ['particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.03 20', 'particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.8 0.4 0.03 10',
                            f'summon minecraft:wither_skeleton ~ ~ ~ {{Tags:["bm.seen","bm.dgmob","bm.ueknight","bm.udread","bm.udk_wither_skeleton"],PersistenceRequired:1b,'
                            f'CustomName:{snbt(T("Dread Knight", COL))},equipment:{{mainhand:{{id:"minecraft:netherite_sword",count:1}}}},drop_chances:{{mainhand:0.0f}}}}'])
    tick.append(f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,tag=bm.d_{d}] at @s run function bm:p237/eyes/tick')
    # the knights go back into the walls when the stair is passed
    G.FUNCS[f'p2/{d}/pz17_solve'].insert(1, 'execute as @e[tag=bm.ueknight] at @s run function bm:p2/util/vanish')

    # ================================================================== THE HOARD (after the fall, six Black Seals)
    fn('p237/hoard/tick', ['execute if entity @s[tag=bm.open] run return 0',
                           'execute unless score #ufell bm.p2 matches 1 if entity @a[distance=..4] run return run ' + title('@a[distance=..4]', 'actionbar', T('A sealed door behind the throne. It will not open while its master sits there.', 'gray', italic=True)),
                           'execute as @a[distance=..4,gamemode=!spectator] if items entity @s container.* *[minecraft:custom_data~{bm:"ublack_seal"}] run function bm:p237/hoard/count',
                           'execute if score #ufell bm.p2 matches 1 as @a[distance=..4,tag=bm.uhoardok,limit=1] run function bm:p237/hoard/open'])
    fn('p237/hoard/count', ['tag @s remove bm.uhoardok', 'execute store result score #sc bm.rng run clear @s *[minecraft:custom_data~{bm:"ublack_seal"}] 0',
                            'execute if score #sc bm.rng matches 6.. run return run tag @s add bm.uhoardok',
                            title('@s', 'actionbar', [T('Six seal-hollows in the door. You carry ', 'gray'), {'score': {'name': '#sc', 'objective': 'bm.rng'}, 'color': 'white'}, T('.', 'gray')])])
    fn('p237/hoard/open', ['clear @s *[minecraft:custom_data~{bm:"ublack_seal"}] 6', 'tag @s remove bm.uhoardok',
                           'execute as @e[type=minecraft:marker,tag=bm.uhoard,distance=..6,sort=nearest,limit=1] at @s run function bm:p237/hoard/door'])
    fn('p237/hoard/door', ['tag @s add bm.open', 'function bm:p237/door/open with entity @s data', 'playsound minecraft:block.vault.open_shutter block @a[distance=..24] ~ ~ ~ 1 0.5',
                           'particle minecraft:wax_off ~ ~2 ~ 1 1.5 1 0 40', title('@a[distance=..16]', 'title', T('The Sovereign\'s Hoard', COL, bold=True))])
    second.append('execute as @e[type=minecraft:marker,tag=bm.uhoard] at @s if entity @a[distance=..6] run function bm:p237/hoard/tick')

    # ================================================================== THE DREAD NIGHTS END (and the Ember)
    G.FUNCS['p181/roll'].insert(1, 'execute if score #dfell bm.cfg matches 1 run return 0')
    G.FUNCS['p181/bell'].insert(1, 'execute if score #dfell bm.cfg matches 1 run return run function bm:p237/bell_dead')
    fn('p237/bell_dead', [give('dread_bell'), title('@s', 'actionbar', T('The bell is silent. What it called for is gone. (A Dread Ember could wake it.)', '#c8a0a0', italic=True)),
                          'playsound minecraft:block.bell.resonate player @s ~ ~ ~ 0.4 0.3'])
    fn('p237/nights_end', ['scoreboard players set #dfell bm.cfg 1', 'execute if score #dnight bm.bm matches 1 run function bm:p181/end',
                           'scoreboard players set #dnday bm.bm -1',
                           tellraw('@a', P + [T('The Dread Sovereign has fallen. ', COL, bold=True), T('The Dread Nights are over.', 'gray')])])
    from useitem import give_back
    G.consume_adv('dread_ember', 'bm:p237/ember')
    fn('p237/ember', ['advancement revoke @s only bm:consume/dread_ember'] + give_back(G.item_arg('dread_ember')) +
       ['execute if score #dfell bm.cfg matches 1 run return run function bm:p237/ember_kindle', 'function bm:p237/ember_smother'])
    fn('p237/ember_kindle', ['scoreboard players set #dfell bm.cfg 0', 'execute unless score #dnt bm.cfg matches 1.. run scoreboard players set #dnt bm.cfg 40',
                             'particle minecraft:flame ~ ~1.4 ~ 0.3 0.3 0.3 0.03 30', 'particle minecraft:sculk_soul ~ ~1.4 ~ 0.3 0.3 0.3 0.03 20',
                             'playsound minecraft:item.firecharge.use player @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:entity.warden.heartbeat ambient @a[distance=..24] ~ ~ ~ 1 0.5',
                             tellraw('@a', P + [T('Someone has kindled a Dread Ember. ', COL, bold=True), T('Somewhere, something remembers how to hunt: the Dread Nights will return.', 'gray')])])
    fn('p237/ember_smother', ['scoreboard players set #dfell bm.cfg 1', 'execute if score #dnight bm.bm matches 1 run function bm:p181/end', 'scoreboard players set #dnday bm.bm -1',
                              'particle minecraft:smoke ~ ~1.4 ~ 0.2 0.2 0.2 0.02 30', 'playsound minecraft:block.fire.extinguish player @a[distance=..24] ~ ~ ~ 1 0.6',
                              tellraw('@a', P + [T('Someone has smothered the Dread Ember. ', COL), T('The Dread Nights are over again.', 'gray')])])

    # ================================================================== THE RELICS AT WORK
    fn('p237/nine', ['scoreboard players set @s bm.u9cd 1200', 'effect give @s minecraft:slow_falling 4 0', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.02 20',
                     'playsound minecraft:entity.cat.purreow player @a[distance=..16] ~ ~ ~ 1 1.2', title('@s', 'actionbar', T('Your Ninth Life catches you. (Again tomorrow.)', '#d8d8e8'))])
    fast.append('execute as @a[gamemode=!spectator,gamemode=!creative] unless score @s bm.u9cd matches 1.. if items entity @s container.* *[minecraft:custom_data~{bm:"nine_lives"}] '
                'if function bm:p237/falling run function bm:p237/nine')
    fn('p237/falling', ['execute store result score #fd bm.rng run data get entity @s fall_distance', 'execute if score #fd bm.rng matches 9.. run return 1', 'return 0'])
    second.append('scoreboard players remove @a[scores={bm.u9cd=1..}] bm.u9cd 1')
    second.append('scoreboard players remove @a[scores={bm.uucd=1..}] bm.uucd 1')
    second.append('execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"ulantern_wick"}] at @s run function bm:p237/wick')
    fn('p237/wick', ['effect give @s minecraft:night_vision 15 0 true', 'effect give @e[type=#bm:hostile,distance=..16] minecraft:glowing 2 0 true'])
    G.consume_adv('unwriting', 'bm:p237/unwrite')
    fn('p237/unwrite', ['advancement revoke @s only bm:consume/unwriting'] + give_back(G.item_arg('unwriting')) +
       ['execute if score @s bm.uucd matches 1.. run return run ' + title('@s', 'actionbar', T('The page is still blank from the last time. (A minute.)', 'gray')),
        'scoreboard players set @s bm.uucd 60', 'effect give @s minecraft:invisibility 8 0', 'effect give @e[type=#bm:hostile,distance=..16] minecraft:slowness 8 2',
        'effect give @e[type=#bm:hostile,distance=..16] minecraft:blindness 8 0', 'effect give @e[type=#bm:hostile,distance=..16] minecraft:weakness 8 1',
        'particle minecraft:enchant ~ ~1 ~ 1 1 1 1 80', 'playsound minecraft:item.book.page_turn player @a[distance=..16] ~ ~ ~ 1 0.5',
        title('@s', 'actionbar', T('AUREL. The word is all that is left - and the monsters near forget you were ever here.', '#c8c0b0', italic=True))])

    # ================================================================== LOOT
    lt, uni, chance = G.loot_entry, G.uni, G.chance
    pool = lambda entries, rolls=1, cond=None: dict({'rolls': rolls, 'entries': entries}, **({'conditions': cond} if cond else {}))
    it = lambda name, lo=1, hi=1, w=1: dict({'type': 'minecraft:item', 'name': f'minecraft:{name}', 'weight': w},
                                            **({'functions': [{'function': 'minecraft:set_count', 'count': uni(lo, hi)}]} if hi > 1 else {}))
    rare = pool([it('netherite_ingot', w=2), it('diamond', 3, 6, 6), it('enchanted_golden_apple', w=3), it('netherite_upgrade_smithing_template', w=2),
                 it('emerald_block', 2, 4, 5), it('heavy_core', w=1)])
    wjson('bm/loot_table/p2/under/ward.json', {'type': 'minecraft:chest', 'pools': [pool([lt('dread_token', uni(3, 5))]), pool([it('diamond', 2, 4)]), rare,
                                                                                   pool([lt('dread_essence', uni(1, 3))], cond=[chance(0.5)])]})
    wjson('bm/loot_table/p2/under/vault.json', {'type': 'minecraft:chest', 'pools': [pool([lt('dread_token', uni(5, 8))]), rare, rare,
                                                                                    pool([it('netherite_scrap', 2, 4)]), pool([lt('trophy', uni(1, 2))])]})
    wjson('bm/loot_table/p2/under/hidden.json', {'type': 'minecraft:chest', 'pools': [pool([lt('dread_token', uni(2, 4))]), rare,
                                                                                     pool([it('gold_block', 1, 3)]), pool([lt('dread_essence', uni(1, 2))])]})
    wjson('bm/loot_table/p2/under/hoard.json', {'type': 'minecraft:chest', 'pools': [pool([lt('dread_token', uni(8, 14))]), rare, rare, rare,
                                                                                    pool([it('netherite_ingot', 1, 3)]), pool([it('gold_block', 4, 9)]),
                                                                                    pool([lt(i) for i in ('sov_edge', 'black_crown', 'sov_heart')], cond=[chance(0.35)])]})
    wjson('bm/loot_table/p2/under/victor.json', {'type': 'minecraft:chest', 'pools': [pool([lt('dread_token', uni(10, 16))]), rare, rare,
                                                                                     pool([it('netherite_ingot', 2, 4)]), pool([lt('trophy', uni(3, 5))]),
                                                                                     pool([lt(i) for i in ('sov_edge', 'black_crown', 'sov_heart')])]})

    # ================================================================== THE BIOME (no spawns; ash and red fog)
    wjson('bm/worldgen/biome/undercrown.json', {
        'attributes': {'minecraft:audio/ambient_sounds': {'loop': 'minecraft:ambient.basalt_deltas.loop',
                                                          'mood': {'block_search_extent': 8, 'offset': 2.0, 'sound': 'minecraft:ambient.soul_sand_valley.mood', 'tick_delay': 3000}},
                       'minecraft:audio/background_music': {'default': {'max_delay': 24000, 'min_delay': 12000, 'sound': 'minecraft:music.nether.soul_sand_valley'}},
                       'minecraft:gameplay/natural_mob_spawns': {'argument': {'spawn_costs': {}, 'spawns_by_category': {}}, 'modifier': 'override'},
                       'minecraft:visual/ambient_particles': {'argument': [{'particle': {'type': 'minecraft:ash'}, 'probability': 0.02},
                                                                           {'particle': {'type': 'minecraft:crimson_spore'}, 'probability': 0.004}], 'modifier': 'override'},
                       'minecraft:visual/fog_color': '#2a0408'},
        'carvers': [], 'downfall': 0.0, 'effects': {'water_color': '#3f76e4'}, 'features': [], 'has_precipitation': False, 'temperature': 2.0})

    # ================================================================== ADMIN
    fn('admin/under/place', ['scoreboard players set #uwant bm.p2 1', 'scoreboard players set #uver bm.p2 0', 'scoreboard players set #ucol bm.p2 0',
                             tellraw('@s', P + [T('The Undercrown will be (re)placed in the Nether in a few seconds (everyone inside is carried out first).', 'gray')])])
    ex, ey, ez = W(*Bu.meta['entrance']) if Bu.meta['entrance'] else (ox_, oy_, oz_)
    fn('admin/under/go', [f'execute unless score #uver bm.p2 matches {UVER} run return run ' + tellraw('@s', P + [T('Not placed yet: /function bm:admin/under/place', 'gray')]),
                          f'execute in {NETHER} run tp @s {ex + 0.5} {ey} {ez + 0.5}'])
    fn('admin/under/outside', [f'execute in {NETHER} run tp @s {ox_ + 0.5} {oy_} {oz_ + 0.5}'])
    fn('admin/under/summons', ['tag @s remove bm.usum', 'scoreboard players set @s bm.dbwin_snow 1', 'scoreboard players set @s bm.dbwin_witch 1', 'scoreboard players set @s bm.dbwin_shark 1',
                               give(TOKENS['snow']), give(TOKENS['witch']), give(TOKENS['shark'])])
    fn('admin/under/fell', ['function bm:p237/nights_end'])
    fn('admin/under/unfell', ['scoreboard players set #dfell bm.cfg 0', tellraw('@s', P + [T('The Dread Nights can come again.', 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/under/', 'yellow'), T('place | go | outside | summons | fell | unfell', 'yellow'),
                                                T('  the Undercrown (final dungeon): (re)place it, go in, go to its gate, earn the Summons, end or bring back the Dread Nights', 'gray')]))
