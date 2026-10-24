"""2.67d: THE VAULT, SMOOTHED OUT - exits that ask first, a crew that needn't wait, a den laid out by job, three shopkeepers,
a clearer Raid Crew, one end-of-heist card, followers that come home with you, a ready check, and the Fixer's Door.

EXITS ASK FIRST WHILE A HEIST IS ON: step into the way out mid-run and the Fixer asks - leave now (your share stays behind,
  the crew carries on) or stay. Before the heist begins, after a win or after a fail, it's instant as ever.
NOBODY WAITS ON THE LEADER: when a heist ends the crew gets their own card - HEAD HOME NOW, or I'M IN IF WE GO AGAIN (you're
  taken along without being asked again, and pay your own fee then). A leader who hasn't chosen in 75 seconds passes the
  choice on to the crew (a solo raider takes as long as they like). Closed the card? Use the Fixer's Ledger: while it's
  your call it opens your choice again (its Office button carries on to the Office).
THE DEN, LAID OUT BY JOB: the market counter (Goldtooth, the Recruiter and the Tailor, behind it - nothing behind them); the
  office counter on the north wall (the Gutter Bank, the Armory, the haul lectern and the RAID CREW board); the Lockers
  through a copper door on the north wall (right-click it), well away from the way out; and "back to the crew" is a plate
  you can see now, by the far door.
THREE SHOPKEEPERS: GOLDTOOTH keeps the heist supplies (tools, potions, food, spoils, Bond Sigils, the Ledger, a Token); THE
  RECRUITER sells the Raid Contracts, the hirelings' contracts and the vault gems; THE TAILOR sells the follower outfits and
  the display cases from a menu that shows what you own already - pick a follower, pick an outfit, and it's in their
  wardrobe for good. The Tailor takes coins from your Gutter Bank and your pockets (a Gutter Medallion is 16, a Trophy 128;
  the change goes to your bank). Goldtooth no longer changes coins: the Gutter Bank does that.
THE RAID CREW PAGE says where everyone is: IN THE VAULT, RESTING (with the seconds left), WAITING (crew full), ON THE WAY,
  ON, OFF or no contract - and "2/2 with you now" on a heist. WHO COMES FIRST is whoever you switched ON first (switch one
  off and on to send it to the back); the page lists them in that order, then the OFF ones, then the rest. A crew over the
  limit (someone joined your heist) sends home the one last in line.
ONE CARD AT THE END: the payout's run of chat lines is one line now ("Heist won! The Haul: 5 Tokens, 23 coins"), and the
  end-of-heist card - the leader's and the crew's - opens with how it went: won (the tier, your shares, Tokens, coins,
  any Medallions or a BM Trophy) or failed. It comes up three seconds after the payout.
FOLLOWERS AND THE VAULT: an Overworld follower you leave behind going into a heist "waits outside the vault" (it goes home
  as before, and says so) - and three seconds after you're home again, it's called back to you (if it isn't resting and
  you're under the cap).
BEGIN HAS A READY CHECK: it starts the heist at once only if everyone has a kit and nobody's at the Lockers; otherwise it
  names who isn't ready - press BEGIN again within ten seconds to go anyway (no kit: the Offense loaners, as before).
THE FIXER'S DOOR: the way out is an archway (in the tier's metal) with a swirl you walk into - in the den (against the west wall) and in
  the treasury (against the far wall, swirling once the vault opens), in place of the old plates. Mid-heist it asks first.
THE LEDGER'S LOCKER HALL TRIP brings you back to where you stood, so it starts only from safe ground (the Overworld, the
  Nether or the End): not falling, flying, mounted or in water or lava; not hurt in the last 10 seconds; not inside a boss
  dungeon or the Hollow - then hold still for 3 seconds (moving or getting hurt cancels it). Each refusal says why. The
  Office pages open anywhere, and the den's copper door (before a heist begins) is as it was.
"""
from items import T, ITEMS
from nbt import snbt, B, Int, F
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM

GOLD = '#ffcf40'
LUCKY = '#7dff6a'
SL = P70.SLOTS
C_LEAVE, C_STAY, C_MHOME, C_PREIN, C_OFFICE = 7724, 7725, 7726, 7727, 7728
DECIDE_S = 75                                  # seconds a leader has before the choice passes on (with a crew waiting)
def _retext(v, old, new):
    if isinstance(v, dict):
        return {k: (_retext(x, old, new) if k != 'text' or not isinstance(x, str) else x.replace(old, new)) for k, x in v.items()}
    if isinstance(v, list):
        return [_retext(x, old, new) for x in v]
    return v


for _iid, _it in ITEMS.items():
    if _iid.startswith('cos_') and 'minecraft:lore' in _it['comps']:
        _it['comps']['minecraft:lore'] = _retext(_it['comps']['minecraft:lore'], 'a Gutter Trophy at Goldtooth', 'a Gutter Trophy at the Tailor')
DEN_EXIT = (2, 4, 4)                           # the den's way out (local)
VAULT_EXIT = (34, 4, 12)                       # the treasury's way out, once the vault is open (local)
DEN_DOOR, VAULT_DOOR = (0, 4, 12), (35, 4, 12)  # (2.67d) the Fixer's Doors (the arches - phase70_rooms; 2.68: the den's in its west doorway)
GOLDTOOTH_AT = (3, 4, 20)                      # (2.67d) behind his counter (z 19), facing the room
RECRUITER_AT = (5, 4, 20)
RECRUITER_OFFERS = []                       # (his stock, as offers: phase131/132 add theirs; 2.78 sells it from a dialog - phase137)
RECRUITER_NPC = {}                          # (his villager, for phase137 to summon without the old trades)
TAILOR_AT = (7, 4, 20)
TL_MET = {'kw': 'killerwatt', 'don': 'donado'}         # (the Tailor's follower keys -> their bm:met/<kind> advancements)
tl_met = lambda w: f'entity @s[advancements={{bm:met/{TL_MET.get(w, w)}=true}}]'
EXTRA_MAIN, EXTRA_PAGES, EXTRA_ACT = [], [], []   # (2.78: more Tailor pages - phase138's auras: main-page buttons, page names, routes)
STOCK = []                                  # (the outfits the Tailor sells, as built - for phase138)
BANK_AT, ARMORY_AT, CREW_AT = (16, 4, 2), (18, 4, 2), (22, 4, 2)     # the office counter, north wall (the haul lectern at 20)
LOCKER_AT = (8, 4, 1)                          # the copper door to the Lockers (north wall)
TO_CREW_AT = (21, 4, 17)                       # "back to the crew", by the far door


def generate(G):
    fn, tellraw, title, PREFIX = G.fn, G.tellraw, G.title, G.PREFIX
    P = PREFIX
    rel = RM.rel
    tick, fast, second = [], [], []
    objs = ['bm.gvdt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    crew = lambda s: f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]'
    chat = lambda txt, col, code, tip: T(txt, col, bold=True, click_event={'action': 'run_command', 'command': f'/trigger bm.act set {code}'},
                                         hover_event={'action': 'show_text', 'value': T(tip, 'gray')})
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {C_LEAVE}..{C_OFFICE} run return run function bm:p103/act')
    fn('p103/act', [f'execute if score #act bm.pay matches {C_LEAVE} run return run function bm:p103/leave_yes',
                    f'execute if score #act bm.pay matches {C_STAY} run return run function bm:p103/leave_no',
                    f'execute if score #act bm.pay matches {C_MHOME} run return run function bm:p103/mem_home',
                    f'execute if score #act bm.pay matches {C_PREIN} run return run function bm:p103/pre_in',
                    f'execute if score #act bm.pay matches {C_OFFICE} run return run function bm:p80/office'])

    # ================================================================== 1a. THE WAY OUT ASKS FIRST WHILE THE HEIST IS ON
    # (each way out is a marker, bm.exitm: the den's from the start, the treasury's once the vault opens. Standing in one shows
    #  the question once - step out and back in to see it again.)
    lt = G.FUNCS['p70/r/lobby/tick']
    old = f'execute positioned {rel(*DEN_EXIT)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p70/leave'
    assert old in lt, 'the den\'s leave plate line moved'
    lt.remove(old)
    vt = G.FUNCS['p70/r/vault/tick']
    old = f'execute if score @s bm.gvs matches 2.. positioned {rel(*VAULT_EXIT)} as @a[tag=bm.gvp,distance=..0.9] at @s run function bm:p70/leave'
    assert old in vt, 'the treasury\'s way-out line moved'
    vt.remove(old)
    G.FUNCS['p70/r/lobby/init'].append(f'summon minecraft:marker {rel(*DEN_DOOR)} {{Tags:["bm.gvprop","bm.exitm"]}}')
    G.FUNCS['p70/r/vault/open'].append(f'summon minecraft:marker {rel(*VAULT_DOOR)} {{Tags:["bm.gvprop","bm.exitm"]}}')
    tick += ['execute as @e[type=minecraft:marker,tag=bm.exitm] at @s as @a[tag=bm.gvp,tag=!bm.exon,distance=..0.9] at @s run function bm:p103/exit',
             'execute as @a[tag=bm.exon] at @s unless entity @e[type=minecraft:marker,tag=bm.exitm,distance=..1.8] run function bm:p103/exit_off']
    fn('p103/exit_off', ['tag @s remove bm.exon', 'tag @s remove bm.exask'])
    fn('p103/exit', ['tag @s add bm.exon', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                     'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                     'execute unless score #st bm.rng matches 2..3 run return run function bm:p70/leave',
                     'tag @s add bm.exask', 'function bm:p103/exit_ask', 'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 0.8 0.8'])
    ask = P28.multi([T('Leave the heist?', GOLD, bold=True)],
                    [P28.body([T('The heist is still on. ', 'white'), T('Leave now and your share stays behind', '#ff9a7a'),
                               T(' - the crew carries on without you, and you go home as you came.', 'gray')])],
                    [P28.btn([T('Leave now', '#ff9a7a', bold=True)], C_LEAVE, width=200, tooltip=T('Home, out of the heist.', 'gray')),
                     P28.btn([T('Stay', LUCKY, bold=True)], C_STAY, width=200, tooltip=T('Back to the job.', 'gray'))],
                    columns=1, exit_label='Stay')
    fn('p103/exit_ask', [f'dialog show @s {snbt(ask)}'])
    fn('p103/leave_yes', ['execute unless entity @s[tag=bm.exask] run return 0', 'tag @s remove bm.exask',
                          'execute unless entity @s[tag=bm.gvp] run return 0', 'execute at @s run function bm:p70/leave'])
    fn('p103/leave_no', ['execute unless entity @s[tag=bm.exask] run return 0', 'tag @s remove bm.exask', say('You stay with the job.', LUCKY)])

    # ================================================================== 1b. NOBODY WAITS ON THE LEADER
    mem = P28.multi([T('The heist is over', GOLD, bold=True)],
                    [P28.body('@@RAW:r_res@@', 300),
                     P28.body([T('Your leader is choosing: ', 'gray'), T('home', 'white', bold=True), T(', or ', 'gray'), T('another job', GOLD, bold=True), T('.', 'gray')]),
                     P28.body([T('You needn\'t wait. Head home now - or say you\'re in, and if they go again you come along (and pay your own fee then).',
                                 'dark_gray')])],
                    [P28.btn([T('Head home now', 'white', bold=True)], C_MHOME, width=200, tooltip=T('Back to the Overworld, as usual.', 'gray')),
                     P28.btn([T('I\'m in if we go again', GOLD, bold=True)], C_PREIN, width=200, tooltip=T('Come along if there\'s another job.', 'gray')),
                     P28.btn([T('The Fixer\'s Office', 'gray')], C_OFFICE, width=200)],
                    columns=1, exit_label='Decide later')
    mem_chat = tellraw('@s', P + [T('Waiting on ', 'gray'), {'selector': '@a[tag=bm.gvask]', 'color': 'white'}, T(': ', 'gray'),
                                  chat('[Head home now]', 'white', C_MHOME, 'Back to the Overworld, as usual.'), T('  '),
                                  chat('[I\'m in if we go again]', GOLD, C_PREIN, 'Come along if there\'s another job.')])
    G.FUNCS['p101/wait_note'][:] = ['tag @s add bm.gvwaitd', 'function bm:p103/mem_show', mem_chat, 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.0']
    fn('p103/mem_show', ['function bm:p103/res_load', 'function bm:p103/mem_dlg with storage bm:ui res'])
    fn('p103/mem_dlg', [f'$dialog show @s {P28.inline(mem)}'])
    # (the member's buttons: home now - any time while it's being decided; in - only while waiting)
    notify = lambda txt, col: ['scoreboard players operation #mi bm.rng = @s bm.gvi', 'tag @s add bm.gvjust',
                               'execute as @a[tag=bm.gvp] if score @s bm.gvi = #mi bm.rng unless entity @s[tag=bm.gvjust] run ' +
                               tellraw('@s', P + [{'selector': '@a[tag=bm.gvjust]', 'color': 'white'}, T(txt, col)]),
                               'tag @s remove bm.gvjust']
    fn('p103/mem_home', ['execute unless entity @s[tag=bm.gvwaitd] unless entity @s[tag=bm.gvoffer] unless entity @s[tag=bm.gvin] run return 0'] +
       notify(' heads home.', 'gray') + ['execute at @s run function bm:p101/send_home'])
    fn('p103/pre_in', ['execute unless entity @s[tag=bm.gvwaitd] run return 0', 'tag @s add bm.gvpre'] + notify(' is in if you go again.', GOLD) +
       [say('You\'re in - if the leader goes again, you come along (and pay your own fee then).', GOLD)])
    # (a new raid: whoever said they're in is taken along without being asked again)
    G.FUNCS['p101/offer'][0:0] = ['tag @s remove bm.gvwaitd', 'execute if entity @s[tag=bm.gvpre] run return run function bm:p103/auto_in']
    fn('p103/auto_in', ['tag @s remove bm.gvpre', 'tag @s add bm.gvoffer', 'function bm:p101/opt_in'])
    # (every way the deciding ends clears the member tags)
    clear = ['tag @s remove bm.gvwaitd', 'tag @s remove bm.gvpre']
    G.FUNCS['p101/send_home'][0:0] = clear
    G.FUNCS['p70/unraid'] += clear + ['tag @s remove bm.exon', 'tag @s remove bm.exask']
    G.FUNCS['p101/claimed'].append('execute as @a[tag=bm.gvp] if score @s bm.pty = #me bm.pty run function bm:p103/mem_clear')
    fn('p103/mem_clear', clear)
    G.FUNCS['p101/ask_lead'][0:0] = clear                             # (the choice passed to someone who'd said they're in)

    # ================================================================== 1c. A LEADER WHO DOESN'T CHOOSE PASSES THE CHOICE ON
    for s in range(SL):
        a = G.FUNCS[f'p101/s{s}/ask']
        assert a[0] == 'tag @a[tag=bm.gvask] remove bm.gvask'
        a[0] = f'tag {crew(s)} remove bm.gvask'                       # (2.67d: only this heist's - two heists could end together)
        a.append(f'scoreboard players set #dt{s} bm.gvdt {DECIDE_S}')
        second.append(f'execute if score #dt{s} bm.gvdt matches 1.. run function bm:p103/s{s}/dt')
        asker = f'@a[tag=bm.gvask,scores={{bm.gvnx={s + 1}}}]'
        fn(f'p103/s{s}/dt', [f'execute unless entity {asker} run return run scoreboard players set #dt{s} bm.gvdt 0',
                             f'execute store result score #n bm.rng if entity {crew(s)}',
                             f'execute if score #n bm.rng matches ..1 run return run scoreboard players set #dt{s} bm.gvdt 0',
                             f'scoreboard players remove #dt{s} bm.gvdt 1',
                             f'execute if score #dt{s} bm.gvdt matches 15 run ' + tellraw(asker, P + [T('15 seconds to choose', GOLD, bold=True),
                                                                                                   T(' - then the choice passes to your crew.', 'gray')]),
                             f'execute if score #dt{s} bm.gvdt matches 0 run function bm:p103/s{s}/pass'])
        fn(f'p103/s{s}/pass', [f'tag {asker} add bm.gvskip',
                               f'execute as {crew(s)[:-1]},tag=!bm.gvskip,limit=1] run scoreboard players operation #ld{s} bm.gvld = @s bm.pid',
                               tellraw('@a[tag=bm.gvskip]', P + [T('Time\'s up - ', 'gray'), T('the choice passes to your crew.', GOLD)]),
                               'scoreboard players reset @a[tag=bm.gvskip] bm.gvnx', 'tag @a[tag=bm.gvskip] remove bm.gvask', 'tag @a[tag=bm.gvskip] remove bm.gvskip',
                               f'function bm:p101/s{s}/ask'])

    # ================================================================== 1d. CLOSED THE CARD? THE LEDGER OPENS YOUR CHOICE AGAIN
    L = G.FUNCS['p80/ledger']
    k = L.index('function bm:p80/office')
    L[k:k] = ['execute if entity @s[tag=bm.gvask] run return run function bm:p101/ask_lead',
              'execute if entity @s[tag=bm.gvnext] run return run function bm:p70/menu',
              'execute if entity @s[tag=bm.gvoffer] run return run function bm:p103/offer_show',
              'execute if entity @s[tag=bm.gvwaitd] run return run function bm:p103/mem_show']
    off = G.FUNCS['p101/offer']
    dlg = next(l for l in off if l.startswith('dialog show @s '))
    fn('p103/offer_show', [dlg])

    # ================================================================== 2. THE DEN, LAID OUT BY JOB
    # the market counter (south-west): the vendors stand BEHIND it, nothing behind them; the office counter (north wall):
    # the Bank, the Armory, the haul lectern and the Raid Crew board side by side; the Lockers through a copper door on the
    # north wall, well away from the way out; "back to the crew" gets a plate you can see, by the far door
    from items import T as _T
    ident = '[0f,0f,0f,1f]'
    lab = lambda x, y, z, text, sc=0.5: (f'summon minecraft:text_display {rel(x, y, z)} {{Tags:["bm.gvprop"],billboard:"vertical",background:1879048192,'
                                          f'text:{snbt(text)},transformation:{{left_rotation:{ident},right_rotation:{ident},translation:[0f,0f,0f],scale:[{sc}f,{sc}f,{sc}f]}}}}')
    li = G.FUNCS['p70/r/lobby/init']
    def move(old, new, must=1, only=None):
        n = 0
        for i, l in enumerate(li):
            if old in l and (only is None or only in l):
                li[i] = l.replace(old, new); n += 1
        assert n >= must, (old, n)
    # Goldtooth: behind his counter (the counter one block longer, for three)
    move(rel(5, 4, 18), rel(*GOLDTOOTH_AT), must=2)
    move('tp @e[type=minecraft:villager,tag=bm.gvgt,distance=..12,', 'tp @e[type=minecraft:villager,tag=bm.gvgt,distance=..16,')   # (he's further from the middle now)
    li[0:0] = [f'setblock {rel(8, 4, 19)} minecraft:dark_oak_planks']
    move(rel(7, 5, 19), rel(8, 5, 19), only='bm.gvdrat')                      # (the grey rat to the counter's end)
    li += [lab(GOLDTOOTH_AT[0], 6.75, GOLDTOOTH_AT[2], [_T('heist supplies', 'gray')], 0.45)]
    # the office counter: Bank and Armory off the back wall, onto the north wall beside the haul lectern
    move(rel(5, 4, 21), rel(*BANK_AT), must=2); move(rel(5, 5.3, 21), rel(BANK_AT[0], 5.3, BANK_AT[2]))
    move(rel(7, 4, 21), rel(*ARMORY_AT), must=2); move(rel(7, 5.3, 21), rel(ARMORY_AT[0], 5.3, ARMORY_AT[2]))
    move('minecraft:vault[facing=north]', 'minecraft:vault[facing=south]')
    move(rel(19, 6, 1), rel(19, 7.4, 1), only='bm.gvboard')                    # (the records board up out of the way)
    cx, cy, cz = CREW_AT
    li += [f'fill {rel(21, 4, 3)} {rel(22, 5, 3)} minecraft:air',              # (the loot pile in front of the office cleared)
           f'setblock {rel(cx, cy, cz)} minecraft:chiseled_bookshelf[facing=south,slot_0_occupied=true,slot_1_occupied=true,slot_3_occupied=true,slot_5_occupied=true]',
           f'summon minecraft:interaction {rel(cx, cy, cz)} {{Tags:["bm.gvprop","bm.ofcrew"],width:1.02f,height:1.02f,response:1b}}',
           lab(cx, 5.3, cz, [_T('RAID CREW\n', '#9ad0ff', bold=True), _T('who comes along', 'gray')])]
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.ofcrew] at @s if data entity @s interaction run function bm:p103/crew_click',
             'execute as @e[type=minecraft:interaction,tag=bm.ofcrew] if data entity @s attack run data remove entity @s attack']
    fn('p103/crew_click', ['execute on target at @s run function bm:p98/crew', 'data remove entity @s interaction'])
    # the Lockers: a copper door on the north wall (click it) - the plate by the way out is gone
    lx, ly, lz = LOCKER_AT
    before = len(li)
    li[:] = [l for l in li if not (rel(2, 3, 7) in l or rel(2, 4, 7) in l or rel(2, 5.6, 7) in l)]
    assert before - len(li) == 3, 'the Locker plate lines moved'
    lt2 = G.FUNCS['p70/r/lobby/tick']
    old = f'execute positioned {rel(2, 4, 7)} as @a[tag=bm.gvp,distance=..0.7] at @s run function bm:p84/lk/from_den'
    assert old in lt2; lt2.remove(old)
    li += [f'setblock {rel(lx, ly, lz)} minecraft:waxed_copper_door[facing=south,half=lower,hinge=left,open=false]',
           f'setblock {rel(lx, ly + 1, lz)} minecraft:waxed_copper_door[facing=south,half=upper,hinge=left,open=false]',
           f'summon minecraft:interaction {rel(lx, ly, lz + 0.3)} {{Tags:["bm.gvprop","bm.lkdoor"],width:1.1f,height:2.05f,response:1b}}',
           lab(lx, 6.4, lz + 0.2, [_T('THE LOCKERS\n', '#c89a5a', bold=True), _T('(before the heist begins)', 'gray')])]
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.lkdoor] if data entity @s interaction run function bm:p103/lk_click',
             'execute as @e[type=minecraft:interaction,tag=bm.lkdoor] if data entity @s attack run data remove entity @s attack']
    fn('p103/lk_click', ['execute on target at @s run function bm:p84/lk/from_den', 'data remove entity @s interaction'])
    G.FUNCS['p84/lk/from_ledger'] = [l.replace('The Lockers are through the copper plate in the den', 'The Lockers are through the copper door in the den')
                                     for l in G.FUNCS['p84/lk/from_ledger']]
    # back to the crew: a plate you can see, by the far door (it was an unmarked spot by the office)
    bx, by, bz = TO_CREW_AT
    k = next(i for i, l in enumerate(G.FUNCS['p70/r/lobby/tick']) if 'function bm:p75/to_crew' in l)
    G.FUNCS['p70/r/lobby/tick'][k] = G.FUNCS['p70/r/lobby/tick'][k].replace(rel(21, 4, 5), rel(bx, by, bz))
    move(rel(21, 5.4, 5), rel(bx, 5.4, bz))
    li += [f'setblock {rel(bx, by - 1, bz)} minecraft:emerald_block', f'setblock {rel(bx, by, bz)} minecraft:polished_blackstone_pressure_plate']

    # ================================================================== 3. THREE SHOPKEEPERS: Goldtooth (supplies), the Recruiter, the Tailor
    # Goldtooth's 101 trades, split: he keeps the heist supplies; the Recruiter (a villager) the contracts and the vault gems; the
    # Tailor (a dialog shop - it knows what you own) the follower outfits and the display cases. The coin/medallion/trophy
    # exchange goes: the Gutter Bank does that.
    import phase99 as P99
    import phase78 as P78
    gtd = P70.goldtooth()
    old_s = snbt(gtd)
    sid = lambda o: o['sell'].get('components', {}).get('minecraft:custom_data', {}).get('bm', '')
    worth = {'gutter_coin': 1, 'gutter_medallion': 16, 'gutter_trophy': 128}
    gt_rec, rec_rec, price = [], [], {}
    for o in gtd['Offers']['Recipes']:
        k_ = sid(o)
        if k_ in worth:
            continue                                                         # (the exchange: the bank does it)
        if 'contract' in k_ or k_.startswith('gem_'):
            rec_rec.append(o)
        elif k_.startswith('cos_') or k_.startswith('display_case'):
            b = o['buy']; bid = b.get('components', {}).get('minecraft:custom_data', {}).get('bm', '')
            assert bid in worth and 'buyB' not in o, (k_, b)
            price[k_] = int(b['count']) * worth[bid]
        else:
            gt_rec.append(o)
    assert len(rec_rec) >= 24 and len(price) >= 40 and len(gt_rec) <= 40, (len(rec_rec), len(price), len(gt_rec))
    gtd['Offers']['Recipes'] = gt_rec
    new_s = snbt(gtd)
    n = 0
    for i, l in enumerate(li):
        if old_s in l:
            li[i] = l.replace(old_s, new_s); n += 1
    assert n == 1, "Goldtooth's summon wasn't found to split"
    P70.goldtooth = lambda: gtd
    # the Recruiter: contracts and gems
    RECRUITER_OFFERS[:] = rec_rec
    recruiter = {'Tags': ['bm.gvrec', 'bm.npc', 'bm.gvprop'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
                 'CustomName': _T('The Recruiter', '#9ad0ff', bold=True), 'CustomNameVisible': B(1),
                 'VillagerData': {'type': 'minecraft:swamp', 'profession': 'minecraft:librarian', 'level': Int(5)}, 'Offers': {'Recipes': rec_rec}}
    RECRUITER_NPC.update(recruiter)
    tailor = {'Tags': ['bm.gvtail', 'bm.npc', 'bm.gvprop'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
              'CustomName': _T('The Tailor', '#ff8ac8', bold=True), 'CustomNameVisible': B(1),
              'VillagerData': {'type': 'minecraft:plains', 'profession': 'minecraft:leatherworker', 'level': Int(5)}, 'Offers': {'Recipes': []}}
    for nm, npc, at_, tag, sub in (('rec', recruiter, RECRUITER_AT, 'bm.gvrec', 'contracts & vault gems'), ('tail', tailor, TAILOR_AT, 'bm.gvtail', 'outfits & display cases')):
        li += [f'summon minecraft:villager {rel(*at_)} {snbt(npc)}',
               f'tp @e[type=minecraft:villager,tag={tag},distance=..16,sort=nearest,limit=1] {rel(*at_)} 180 0',
               lab(at_[0], 6.75, at_[2], [_T(sub, 'gray')], 0.45)]
    li += [f'summon minecraft:interaction {rel(*TAILOR_AT)} {{Tags:["bm.gvprop","bm.tailhit"],width:1.0f,height:2.1f,response:1b}}']
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.tailhit] if data entity @s interaction run function bm:p103/tail_click',
             'execute as @e[type=minecraft:interaction,tag=bm.tailhit] if data entity @s attack run data remove entity @s attack']
    fn('p103/tail_click', ['execute on target at @s run function bm:p103/tl/main', 'data remove entity @s interaction'])

    # ---- the wallet: coins in the bank and in your pockets, Gutter Medallions (16) and Trophies (128) counted
    hold = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    fn('p103/wallet', ['function bm:p80/init_me', 'scoreboard players operation #tw bm.rng = @s bm.gbc',
                       f'execute store result score #pc bm.rng run clear @s {hold("gutter_coin")} 0',
                       f'execute store result score #pm bm.rng run clear @s {hold("gutter_medallion")} 0',
                       f'execute store result score #pt bm.rng run clear @s {hold("gutter_trophy")} 0',
                       'scoreboard players operation #tw bm.rng += #pc bm.rng', 'scoreboard players set #k16 bm.rng 16', 'scoreboard players set #k128 bm.rng 128',
                       'scoreboard players operation #w bm.rng = #pm bm.rng', 'scoreboard players operation #w bm.rng *= #k16 bm.rng', 'scoreboard players operation #tw bm.rng += #w bm.rng',
                       'scoreboard players operation #w bm.rng = #pt bm.rng', 'scoreboard players operation #w bm.rng *= #k128 bm.rng', 'scoreboard players operation #tw bm.rng += #w bm.rng',
                       'execute store result storage bm:ui tl.w int 1 run scoreboard players get #tw bm.rng'])
    # (#need coins, right after p103/wallet, which found enough: the bank first, then pocket coins, Medallions, Trophies; change to the bank)
    fn('p103/spend', ['scoreboard players operation #b bm.rng = @s bm.gbc', 'scoreboard players operation #b bm.rng < #need bm.rng',
                      'scoreboard players operation @s bm.gbc -= #b bm.rng', 'scoreboard players operation #need bm.rng -= #b bm.rng',
                      'execute if score #need bm.rng matches 1.. run function bm:p103/spend_c',
                      'execute if score #need bm.rng matches 1.. run function bm:p103/spend_m',
                      'execute if score #need bm.rng matches 1.. run function bm:p103/spend_t',
                      'execute if score #need bm.rng matches ..-1 run function bm:p103/change'])
    for nm, iid, unit, have in (('c', 'gutter_coin', 1, '#pc'), ('m', 'gutter_medallion', 16, '#pm'), ('t', 'gutter_trophy', 128, '#pt')):
        fn(f'p103/spend_{nm}', ['scoreboard players operation #k bm.rng = #need bm.rng'] +
           ([f'scoreboard players add #k bm.rng {unit - 1}', f'scoreboard players set #u bm.rng {unit}', 'scoreboard players operation #k bm.rng /= #u bm.rng'] if unit > 1 else []) +
           [f'scoreboard players operation #k bm.rng < {have} bm.rng', 'execute store result storage bm:ui sp.n int 1 run scoreboard players get #k bm.rng',
            f'function bm:p103/take_{nm} with storage bm:ui sp'] +
           ([f'scoreboard players set #u bm.rng {unit}', 'scoreboard players operation #k bm.rng *= #u bm.rng'] if unit > 1 else []) +
           ['scoreboard players operation #need bm.rng -= #k bm.rng'])
        fn(f'p103/take_{nm}', [f'$clear @s {hold(iid)} $(n)'])
    fn('p103/change', ['scoreboard players operation #c bm.rng = #need bm.rng', 'scoreboard players set #u bm.rng -1', 'scoreboard players operation #c bm.rng *= #u bm.rng',
                       'scoreboard players operation @s bm.gbc += #c bm.rng', 'scoreboard players set #need bm.rng 0',
                       tellraw('@s', P + [T('Your change - ', 'gray'), {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                          T(' coins - is in your Gutter Bank.', 'gray')])])

    # ---- the Tailor's pages
    TL = 7740
    WHO = [('emma', 'Emma', P78.PINK), ('celi', 'Celi', '#9ad8ff'), ('zib', 'Zib', '#3ad8c8'), ('cecil', 'Cecil', '#b48cff'),
           ('kw', 'KillerWatt', '#ffe040'), ('leo', 'Leo', '#5ab8e0'), ('demo', 'Democratus', '#7ad06a'),
           ('apo', 'Apophiss', '#3ad06a'), ('tul', 'Tullius', '#7ad8ff'), ('frog', 'The Frog', '#6ac850'), ('don', 'Donado', '#e8d29a'),
           ('pearl', 'Pearlman', '#5ac8ff'), ('wil', 'Wilfrey', '#f4f4f4'), ('fishy', 'Fishy', '#ffa040'),
           ('dennis', 'Dennis', '#e0a040'), ('pistachio', 'Pistachio', '#7ae890'), ('omega', 'King Omega', '#9fb4ff'), ('ashur', 'Ashur', '#ff7a2a'), ('chef', 'The Chef', '#ffd07a'), ('neighbor', 'The Neighbor', '#7ab8ff'), ('ava', 'Queen Ava', '#6ad8e8'), ('pearlq', 'Queen Pearl', '#5ae0d8'), ('bloo', 'Bloo', '#5a9ae8'), ('stalker', 'The Stalker', '#a8ac70'), ('lantern', 'The Arachno-Lantern', '#ff8a2a'), ('bender', 'Bender', '#e0a860'), ('bones', 'Bones', '#8ab0c8'), ('capshun', 'Mr. Capshun', '#f0f0f0'), ('pxcecil', '8-Bit Cecil', '#b070ff'), ('pxleo', '8-Bit Leo', '#4ab0ff'), ('pxemma', '8-Bit Emma', '#ff6ac8'), ('sky', 'The Sky Buddies', '#ffd04a')]
    # 2.78: past the old block (TL..TL+59) the pages, stock and auras go on in 8100-8299
    TL2 = 8100
    pcode = lambda i: TL + 1 + i if i < 7 else (TL2 + i - 7 if i < 13 else (TL2 + i - 6 if i < 16 else 8270 + i - 16))      # a follower's page (2.79: past 8106, the Auras page; 2.82: 8270 on)
    scode = lambda j: TL + 10 + j if j < 40 else (TL2 + 10 + j - 40 if j < 80 else (TL2 + 64 + j - 80 if j < 112 else (8200 + j - 112 if j < 182 else 3600 + j - 182)))   # an outfit (2.80c: past 8150-8163, the auras; 2.82: 8200 on; 2.94: 3600 on)
    stock = []                                       # (who, group, unlock score, k, item, name, colour, price)
    for who, g, cur, un, ks, iid, off, apply in P99.groups():
        for k, (cn, col) in ks.items():
            it = iid.format(k)
            assert it in price, f'{it} is not on sale'
            stock.append((who, g, un, k, it, cn, col, price[it]))
    cases = [(k_, price[k_]) for k_ in price if k_.startswith('display_case')]
    assert len(stock) == len([k_ for k_ in price if k_.startswith('cos_')]) and (len(stock) <= 112 or scode(len(stock) - 1) < 8270 or 3600 <= scode(len(stock) - 1) < 3700) and len(cases) <= 9   # (codes TL..TL+59: the Office's start at 7800)
    STOCK.extend(stock)
    wal = [_T('You have ', 'gray'), _T('$(w)', GOLD, bold=True), _T(' coins to spend', 'gray'),
           _T(' (Gutter Bank and pockets; Medallions count 16, Trophies 128).', 'dark_gray')]
    back = P28.btn([_T('« The Tailor', 'gray')], TL, width=180)
    main = P28.multi([_T('THE TAILOR', '#ff8ac8', bold=True), _T('  ·  outfits for your followers', 'gray')],
                     [P28.body([_T('Every outfit is yours for good - put it on from the follower\'s own menu (sneak + use their item). ', 'gray')], 360),
                      P28.body(wal, 360)], [], columns=2, exit_label='Close')
    # (2.82c) only the followers you've met out in the world (bm:met/<kind>, phase137/158) - a name gave them away before you'd found them
    main['actions'] = '@@RAW:acts@@'
    acts = ['data modify storage bm:ui tl.acts set value []'] + \
        [f'execute if {tl_met(w)} run data modify storage bm:ui tl.acts append value {snbt(P28.btn([_T(nm, col, bold=True)], pcode(i), width=180))}'
         for i, (w, nm, col) in enumerate(WHO)] + \
        [f'data modify storage bm:ui tl.acts append value {snbt(b)}' for b in [P28.btn([_T('Display cases', GOLD, bold=True)], TL + 8, width=180)] + EXTRA_MAIN]
    fn('p103/tl/main', ['function bm:p103/wallet', f'scoreboard players set @s bm.menu {TL}'] + acts + ['function bm:p103/tl/main_dlg with storage bm:ui tl'])
    fn('p103/tl/main_dlg', [f'$dialog show @s {P28.inline(main)}'])
    for i, (w, nm, col) in enumerate(WHO):
        mine_ = [(j, x) for j, x in enumerate(stock) if x[0] == w]
        rows = []
        for j, (who, g, un, k, it, cn, ccol, pr) in mine_:
            rows += [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0',
                     f'data modify storage bm:ui tl.r_{j} set value {snbt(_T(f"{pr} coins", GOLD))}',
                     f'scoreboard players operation #q bm.rng = @s {un}', f'scoreboard players set #bit bm.rng {2 ** k}',
                     'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                     f'execute if score #q bm.rng matches 1 run data modify storage bm:ui tl.r_{j} set value {snbt(_T("OWNED", "#7aff7a", bold=True))}']
        dlg = P28.multi([_T(nm.upper(), col, bold=True), _T('  ·  the Tailor', 'gray')],
                        [P28.body(wal, 360)],
                        [P28.btn([_T(cn, ccol, bold=True), _T('  '), f'@@RAW:r_{j}@@'], scode(j), width=180) for j, (who, g, un, k, it, cn, ccol, pr) in mine_] + [back],
                        columns=2, exit_label='Close')
        fn(f'p103/tl/p_{w}', [f'execute unless {tl_met(w)} run return run function bm:p103/tl/main', 'function bm:p103/wallet', f'scoreboard players set @s bm.menu {TL}'] + rows + [f'function bm:p103/tl/p_{w}_dlg with storage bm:ui tl'])
        fn(f'p103/tl/p_{w}_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    cdlg = P28.multi([_T('DISPLAY CASES', GOLD, bold=True), _T('  ·  the Tailor', 'gray')],
                     [P28.body([_T('Glass cases for your trophies and finds - set one down and put something in it.', 'gray')], 360), P28.body(wal, 360)],
                     [P28.btn([_T(ITEMS[c]['name'], 'white', bold=True), _T('  '), _T(f'{pr} coins', GOLD)], TL + 50 + q, width=180)
                      for q, (c, pr) in enumerate(cases)] + [back], columns=2, exit_label='Close')
    fn('p103/tl/cases', ['function bm:p103/wallet', f'scoreboard players set @s bm.menu {TL}', 'function bm:p103/tl/cases_dlg with storage bm:ui tl'])
    fn('p103/tl/cases_dlg', [f'$dialog show @s {P28.inline(cdlg)}'])
    PAGES = [f'p_{w}' for w, nm, col in WHO] + ['cases'] + EXTRA_PAGES
    pg = lambda page: f'scoreboard players set #tlp bm.rng {PAGES.index(page)}'
    fn('p103/tl/reopen', [f'execute if score #tlp bm.rng matches {i} run return run function bm:p103/tl/{pname}' for i, pname in enumerate(PAGES)])
    poor = lambda pr, page: ('execute if score #tw bm.rng matches ..%d run return run function bm:p103/tl/poor {n:%d}' % (pr - 1, pr))
    fn('p103/tl/poor', ['$' + tellraw('@s', P + [T('That\'s $(n) coins - you have ', 'red'), {'score': {'name': '#tw', 'objective': 'bm.rng'}, 'color': 'white'},
                                                  T(' (bank and pockets).', 'red')]), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1', 'function bm:p103/tl/reopen'])
    for j, (who, g, un, k, it, cn, ccol, pr) in enumerate(stock):
        wn = next(nm for w, nm, c in WHO if w == who)
        fn(f'p103/tl/b{j}', [f'execute unless score @s bm.menu matches {TL} run return run function bm:p28/stale',
                             f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0',
                             f'scoreboard players operation #q bm.rng = @s {un}', f'scoreboard players set #bit bm.rng {2 ** k}',
                             'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                             pg(f'p_{who}'),
                             f'execute if score #q bm.rng matches 1 run return run function bm:p103/tl/note {{t:"{cn} is in {wn}\'s wardrobe already."}}',
                             f'execute if items entity @s container.* {hold(it)} run return run function bm:p103/tl/note {{t:"You have that one - use it to put it in {wn}\'s wardrobe."}}',
                             'function bm:p103/wallet', poor(pr, f'p_{who}'),
                             f'scoreboard players set #need bm.rng {pr}', 'function bm:p103/spend', f'function bm:p99/unlock/{g}{k}',
                             'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1', f'function bm:p103/tl/p_{who}'])
    for q, (c, pr) in enumerate(cases):
        fn(f'p103/tl/c{q}', [f'execute unless score @s bm.menu matches {TL} run return run function bm:p28/stale', pg('cases'), 'function bm:p103/wallet', poor(pr, 'cases'),
                             f'scoreboard players set #need bm.rng {pr}', 'function bm:p103/spend', f'loot give @s loot bm:items/{c}',
                             'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1', 'function bm:p103/tl/cases'])
    fn('p103/tl/note', ['$' + tellraw('@s', P + [T('$(t)', 'gray')]), 'function bm:p103/tl/reopen'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {TL}..{TL + 59} run return run function bm:p103/tl/act')
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {TL2}..{TL2 + 99} if score @s bm.menu matches {TL} run return run function bm:p103/tl/act')
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches 8200..8279 if score @s bm.menu matches {TL} run return run function bm:p103/tl/act')   # (2.82: the overflow block)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches 8293..8299 if score @s bm.menu matches {TL} run return run function bm:p103/tl/act')   # (2.86: the auras past the 18th)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches 8380..8399 if score @s bm.menu matches {TL} run return run function bm:p103/tl/act')   # (2.88: the auras past the 25th)
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches 3600..3699 if score @s bm.menu matches {TL} run return run function bm:p103/tl/act')   # (2.94: the outfits past the 182nd)
    fn('p103/tl/act', [f'execute if score #act bm.pay matches {TL} run return run function bm:p103/tl/main'] +
       [f'execute if score #act bm.pay matches {pcode(i)} run return run function bm:p103/tl/p_{w}' for i, (w, nm, col) in enumerate(WHO)] +
       [f'execute if score #act bm.pay matches {TL + 8} run return run function bm:p103/tl/cases'] +
       [f'execute if score #act bm.pay matches {scode(j)} run return run function bm:p103/tl/b{j}' for j in range(len(stock))] + EXTRA_ACT +
       [f'execute if score #act bm.pay matches {TL + 50 + q} run return run function bm:p103/tl/c{q}' for q in range(len(cases))])
    # ---- who sells what now, in the texts
    for old_t, new_t in (('Goldtooth sells Raid Contracts in the den', 'The Recruiter in the den sells Raid Contracts'),
                         ('Goldtooth sells them; use it once', 'the Recruiter in the den sells them; use it once'),
                         ('Goldtooth sells the contract; use it once', 'the Recruiter in the den sells the contract; use it once'),
                         (' to come into the vault. Goldtooth sells them.', ' to come into the vault. The Recruiter in the den sells them.'),
                         ('Goldtooth sells them all.', 'The Recruiter in the den sells them all.'),
                         ('is locked - Goldtooth sells it in the vault', 'is locked - the Tailor in the den has it'),
                         (' ones are sold by Goldtooth in the vault (the hidden ones for a Gutter Trophy).', ' ones are sold by the Tailor in the vault\'s den (the hidden ones for 128 coins).')):
        hit = 0
        for f_, L_ in G.FUNCS.items():
            for i, l in enumerate(L_):
                if old_t in l:
                    L_[i] = l.replace(old_t, new_t); hit += 1
        assert hit, old_t

    # ================================================================== 4. THE RAID CREW: who's here, who's resting, who's waiting - and who comes first
    # Priority is the order you switched them ON (a follower switched on later comes after the rest; switch one off and on to
    # send it to the back). The roster calls the eligible follower who's first in line; a crew over the limit sends home
    # the one who's last. The page lists the ON ones in that order, then the OFF ones, then the ones with no contract.
    import phase98 as P98
    import phase77 as P77
    import phase80 as P80
    MC = P80.MENU_CODE
    FOL = [(k, nm, col, cd) for (k, nm, col, host, tag, sel, cd, *_r) in P98.CALLED] + [(k, nm, col, cd) for (k, nm, col, tag, cd) in P98.HIRED]
    code_of = {k: P98.ccode(i) for i, (k, *_r) in enumerate(P98.CALLED)}
    code_of.update({k: P98.CODE + 20 + j for j, (k, *_r) in enumerate(P98.HIRED)})
    hired = {k for (k, *_r) in P98.HIRED}
    co = {k: f'bm.co_{k[:8]}' for k, *_r in FOL}
    objs4 = list(co.values()) + ['bm.coq']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs4]
    G.OBJECTIVES += objs4
    # (defaults: the old list order, ahead of anyone switched on from now on)
    G.FUNCS['p98/init'] += [f'execute unless score @s {co[k]} matches 0.. run scoreboard players set @s {co[k]} {1000 + i}' for i, (k, *_r) in enumerate(FOL)] + \
                           ['execute unless score @s bm.coq matches 2000.. run scoreboard players set @s bm.coq 2000']
    for k, *_r in FOL:
        G.FUNCS[f'p98/t/{k}_on'][0:0] = ['scoreboard players add @s bm.coq 1', f'scoreboard players operation @s {co[k]} = @s bm.coq']
    ok_k = lambda k: f'if function bm:p98/{"filed" if k in hired else "signed"}/{k}'
    elig = lambda k, cd: f'if entity @s[tag=bm.crw_{k}] if function bm:p98/on/{k} unless score @s {cd} matches 1.. unless function bm:p98/has/{k}'
    # the roster: marks cleared, the two best called (while there's room), then the new marks (called next second)
    R_ = ['function bm:p98/init', 'function bm:p98/count', 'execute if score #fc bm.rng > #lim bm.rng run function bm:p103/crew/bench'] + \
         [f'execute if entity @s[tag=bm.crw_{k}] if function bm:p98/has/{k} run tag @s remove bm.crw_{k}' for k, *_r in FOL] + \
         ['function bm:p103/crew/pick', 'function bm:p103/crew/pick'] + \
         [f'execute if function bm:p98/on/{k} unless score @s {cd} matches 1.. unless function bm:p98/has/{k} run tag @s add bm.crw_{k}' for k, nm, col, cd in FOL]
    G.FUNCS['p98/roster'][:] = R_
    fn('p103/crew/pick', ['execute unless function bm:p98/room run return 0', 'scoreboard players set #best bm.rng 2147483647', 'scoreboard players set #bk bm.rng -1'] +
       [f'execute {elig(k, cd)} if score @s {co[k]} < #best bm.rng run function bm:p103/crew/best_{i}' for i, (k, nm, col, cd) in enumerate(FOL)] +
       [f'execute if score #bk bm.rng matches {i} run function bm:p98/call/{k}' for i, (k, *_r) in enumerate(FOL)])
    for i, (k, *_r) in enumerate(FOL):
        fn(f'p103/crew/best_{i}', [f'scoreboard players operation #best bm.rng = @s {co[k]}', f'scoreboard players set #bk bm.rng {i}'])
    # the bench: over the limit, the one last in line goes home
    fn('p103/crew/bench', ['scoreboard players set #worst bm.rng -1', 'scoreboard players set #wk bm.rng -1'] +
       [f'execute if function bm:p98/has/{k} if score @s {co[k]} > #worst bm.rng run function bm:p103/crew/worst_{i}' for i, (k, *_r) in enumerate(FOL)] +
       [f'execute if score #wk bm.rng matches {i} run function bm:p98/bench_{k}' for i, (k, *_r) in enumerate(FOL)])
    for i, (k, *_r) in enumerate(FOL):
        fn(f'p103/crew/worst_{i}', [f'scoreboard players operation #worst bm.rng = @s {co[k]}', f'scoreboard players set #wk bm.rng {i}'])
    G.FUNCS.pop('p98/bench', None)
    # the page: built fresh each time (the ON ones in line order, then OFF, then no contract; the hirelings; back)
    ST = lambda txt, col: snbt(_T(txt, col, bold=True))
    in_h = 'if entity @s[tag=bm.gvp] if dimension bm:gutter'
    page = ['function bm:p98/init', f'scoreboard players set @s bm.menu {MC + 7}', 'data remove storage bm:ui crew', 'data modify storage bm:ui crew.acts set value []',
            'function bm:p98/count', 'execute store result storage bm:ui crew.fc int 1 run scoreboard players get #fc bm.rng',
            'execute store result storage bm:ui crew.lim int 1 run scoreboard players get #lim bm.rng'] + \
           [f'scoreboard players set #ad{i} bm.rng 0' for i in range(len(FOL))] + \
           ['function bm:p103/crew/next'] * len(FOL) + \
           [f'execute {ok_k(k)} unless function bm:p98/on/{k} run function bm:p103/crew/row_{i}' for i, (k, *_r) in enumerate(FOL)] + \
           [f'execute unless {ok_k(k)[3:]} run function bm:p103/crew/row_{i}' for i, (k, *_r) in enumerate(FOL)] + \
           ['function bm:p103/crew/hire_rows',
            f'data modify storage bm:ui crew.acts append value {snbt(P28.btn([_T("« The Office", "gray")], MC, width=180))}',
            f'execute {in_h} run return run function bm:p103/crew/show_in with storage bm:ui crew', 'function bm:p103/crew/show_out with storage bm:ui crew']
    G.FUNCS['p98/crew'][:] = page
    G.FUNCS.pop('p98/page_dlg', None)
    fn('p103/crew/next', ['scoreboard players set #best bm.rng 2147483647', 'scoreboard players set #bk bm.rng -1'] +
       [f'execute if score #ad{i} bm.rng matches 0 if function bm:p98/on/{k} if score @s {co[k]} < #best bm.rng run function bm:p103/crew/best_{i}' for i, (k, *_r) in enumerate(FOL)] +
       [f'execute if score #bk bm.rng matches {i} run function bm:p103/crew/row_{i}' for i, (k, *_r) in enumerate(FOL)])
    for i, (k, nm, col, cd) in enumerate(FOL):
        row = P28.btn([_T(nm if k != 'frog' else 'The Frog', col, bold=True), _T('  '), _T('')], code_of[k], width=180)
        fn(f'p103/crew/row_{i}', [f'scoreboard players set #ad{i} bm.rng 1', f'data modify storage bm:ui crew.row set value {snbt(row)}',
                                  f'data modify storage bm:ui crew.st set value {ST("no contract", "dark_gray")}',
                                  f'execute {ok_k(k)} run data modify storage bm:ui crew.st set value {ST("OFF", "#ff7a7a")}',
                                  f'execute if function bm:p98/on/{k} run data modify storage bm:ui crew.st set value {ST("ON", "#7aff7a")}',
                                  f'execute if function bm:p98/on/{k} {in_h} run function bm:p103/crew/st_{i}',
                                  'data modify storage bm:ui crew.row.label[2] set from storage bm:ui crew.st',
                                  'data modify storage bm:ui crew.acts append from storage bm:ui crew.row'])
        fn(f'p103/crew/st_{i}', [f'execute if function bm:p98/has/{k} run return run data modify storage bm:ui crew.st set value {ST("IN THE VAULT", "#7aff7a")}',
                                 f'execute if score @s {cd} matches 1.. store result storage bm:ui crew.n int 1 run scoreboard players get @s {cd}',
                                 f'execute if score @s {cd} matches 1.. run return run function bm:p103/crew/st_rest with storage bm:ui crew',
                                 f'execute unless function bm:p98/room run return run data modify storage bm:ui crew.st set value {ST("WAITING - crew full", "#ffe07a")}',
                                 f'data modify storage bm:ui crew.st set value {ST("ON THE WAY", "#7aff7a")}'])
    fn('p103/crew/st_rest', ['$data modify storage bm:ui crew.st set value {text:"RESTING $(n)s",color:"#ffb060",bold:1b}'])
    hrows = []
    for i, (hk, hnm, rat, hcol, *_r) in P77.HIRE.items():
        hrow = P28.btn([_T(hnm, hcol, bold=True), _T('  '), _T('')], P98.CODE + 30 + i, width=180)
        hrows += [f'data modify storage bm:ui crew.row set value {snbt(hrow)}', f'data modify storage bm:ui crew.st set value {ST("not hired", "dark_gray")}',
                  f'execute if function bm:p98/filed/h{i} run data modify storage bm:ui crew.st set value {ST("OFF", "#ff7a7a")}',
                  f'execute if function bm:p98/filed/h{i} if score @s bm.gvhr matches {i} run data modify storage bm:ui crew.st set value {ST("ON", "#7aff7a")}',
                  'data modify storage bm:ui crew.row.label[2] set from storage bm:ui crew.st', 'data modify storage bm:ui crew.acts append from storage bm:ui crew.row']
    fn('p103/crew/hire_rows', hrows)
    how = P28.body([_T('Click to switch on or off. Who comes first: whoever you switched ', 'gray'), _T('ON', '#7aff7a', bold=True),
                    _T(' first, top of the list (switch one off and on to send it to the back). Hirelings: one at a time. Leave the heist and the crew goes home.', 'gray')], 360)
    where = P28.body([_T('Followers sign on with a Raid Contract; hirelings and vault hires with theirs (used once, filed here). The Recruiter in the den sells them all.',
                         'dark_gray', italic=True)], 360)
    for nm, head in (('in', [_T('RAID CREW', '#9ad0ff', bold=True), _T('  ·  ', 'gray'), _T('$(fc)/$(lim)', 'white', bold=True), _T(' with you now', 'gray')]),
                     ('out', [_T('RAID CREW', '#9ad0ff', bold=True), _T('  ·  who comes into the vault with you', 'gray')])):
        bodies = [how, where] if nm == 'in' else [P28.body([_T('Raid alone and two come along; in a party, one each.', 'white')], 360), how, where]
        d = P28.multi(head, bodies, [], columns=2, exit_label='Close')
        d['actions'] = '@@RAW:acts@@'
        fn(f'p103/crew/show_{nm}', [f'$dialog show @s {P28.inline(d)}'])

    # ================================================================== 5. ONE CARD AT THE END: how it went, and what next
    # The payout's run of chat lines (your shares, the haul's kind, the pot, the prize, the extra, the crate) goes quiet; one
    # line sums it up, and the end-of-heist card (both the leader's and the crew's) opens with the result. A failed heist
    # says so on the card too. (The Lucky split, first clears, a Shifting Core, a BM Trophy - news - still go to chat.)
    QUIET = ('Your haul: ', 'THE PLAIN HAUL', 'THE BLACK MARKET HAUL', 'THE GUTTER HAUL', 'The pot: ', "The Fixer's prize: ", '...your fee back, and ',
             ' Medallion(s)!', 'your fee back, ', 'The Fixer hands you ')
    nq = 0
    for f_ in ('p70/haul', 'p75/prize', 'p101/fee_back', 'p74/haul_pack'):
        L_ = G.FUNCS[f_]
        for i, l in enumerate(L_):
            if 'tellraw @s' in l and any(q in l for q in QUIET):
                L_[i] = ('execute unless score #hq bm.rng matches 1 run ' + l) if l.startswith('tellraw ') else l.replace('execute ', 'execute unless score #hq bm.rng matches 1 ', 1)
                nq += 1
    assert nq >= 9, f'only {nq} payout lines quieted'
    GUT = '#c8a050'
    G.FUNCS['p70/haul'][0:0] = ['scoreboard players set #hq bm.rng 1']
    G.FUNCS['p70/haul'] += ['function bm:p103/res_won', 'scoreboard players set #hq bm.rng 0']
    sco = lambda n, col, bold=True: {'score': {'name': n, 'objective': 'bm.rng'}, 'color': col, 'bold': bold}
    fn('p103/res_won', ['scoreboard players operation #rtk bm.rng = #ptk bm.rng', 'scoreboard players operation #rtk bm.rng += #lpx bm.rng',
                        'execute store result storage bm:gv rs.pid int 1 run scoreboard players get @s bm.pid',
                        'execute store result storage bm:gv rs.tok int 1 run scoreboard players get #rtk bm.rng',
                        'execute store result storage bm:gv rs.coin int 1 run scoreboard players get #pot bm.rng',
                        'execute store result storage bm:gv rs.med int 1 run scoreboard players get #pmd bm.rng',
                        'execute store result storage bm:gv rs.sh int 1 run scoreboard players get #sh bm.rng',
                        'execute store result storage bm:gv rs.tier int 1 run scoreboard players get #gt bm.rng',
                        'function bm:p103/res_won2 with storage bm:gv rs',
                        'execute if score #pmd bm.rng matches 1.. run function bm:p103/res_med with storage bm:gv rs',
                        'execute if score #ptr bm.rng matches 1.. run function bm:p103/res_tro with storage bm:gv rs',
                        tellraw('@s', P + [T('Heist won! ', '#7aff7a', bold=True), T('The Haul: ', 'gray'), sco('#rtk', GOLD), T(' Tokens', GOLD), T(', ', 'gray'),
                                           sco('#pot', 'white'), T(' coins', GUT), T(' - in your pack.', 'gray')]),
                        'execute if score #pmd bm.rng matches 1.. run ' + tellraw('@s', P + [T('...and ', 'gray'), sco('#pmd', 'white'), T(' Medallion(s) in it too.', GOLD)])])
    won = [_T('HEIST WON', '#7aff7a', bold=True), _T(' - Tier $(tier), $(sh) shares. The Haul: ', 'gray'), _T('$(tok) Tokens', GOLD, bold=True),
           _T(', ', 'gray'), _T('$(coin) coins', GUT), _T('.', 'gray')]
    fn('p103/res_won2', [f'$data modify storage bm:gv res.p$(pid) set value {snbt(won)}'])
    fn('p103/res_med', [f'$data modify storage bm:gv res.p$(pid) insert -1 value {snbt(_T(", $(med) Medallion(s)", "light_purple", bold=True))}'])
    fn('p103/res_tro', [f'$data modify storage bm:gv res.p$(pid) insert -1 value {snbt(_T(", a BM Trophy", "#ffb300", bold=True))}'])
    lost = [_T('HEIST FAILED', '#ff7a7a', bold=True), _T(' - everything gathered is lost.', 'gray')]
    G.FUNCS['p101/after_fail'].append('function bm:p103/res_fail')
    fn('p103/res_fail', ['execute store result storage bm:gv rs.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p103/res_fail2 with storage bm:gv rs'])
    fn('p103/res_fail2', [f'$data modify storage bm:gv res.p$(pid) set value {snbt(lost)}'])
    # (as a player) the result into bm:ui res.r_res, for the card; gone once you've left
    fn('p103/res_load', ['execute store result storage bm:ui res.pid int 1 run scoreboard players get @s bm.pid',
                         f'data modify storage bm:ui res.r_res set value {snbt(_T("The heist is over.", "gray"))}', 'function bm:p103/res_load2 with storage bm:ui res'])
    fn('p103/res_load2', ['$execute if data storage bm:gv res.p$(pid) run data modify storage bm:ui res.r_res set from storage bm:gv res.p$(pid)'])
    G.FUNCS['p70/unraid'] += ['execute store result storage bm:gv rs.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p103/res_clear with storage bm:gv rs']
    fn('p103/res_clear', ['$data remove storage bm:gv res.p$(pid)'])

    # ================================================================== 6a. FOLLOWERS: "waits outside the vault" going in - and back with you coming out
    # (an Overworld follower left behind when you go into a heist goes home as before, but says why - and is remembered;
    #  three seconds after you're home again, it's called back to you - if it's not resting and you're under the cap)
    KINDS = [('cecil', 'p62/cecil_go', 'Cecil', '#b48cff', 'p46/pet/try_summon'), ('emma', 'p62/emma_go', 'Emma', '#ff8ad8', 'p57/try_summon'),
             ('celi', 'p66/go', 'Celi', '#bfe8ff', 'p66/try_summon'), ('zib', 'p72/zb/beamup', 'Zib', '#7ad87a', 'p72/zb/try_summon'),
             ('kw', 'p79/pet/vanish', 'KillerWatt', '#ffe040', 'p79/pet/try'), ('leo', 'p96/go', 'Leo', '#5ab8e0', 'p96/try_summon'),
             ('demo', 'p97/go', 'Democratus', '#7ad06a', 'p97/try_summon')]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.owt dummy', 'scoreboard objectives add bm.gvbc dummy', 'scoreboard objectives add bm.gvbw dummy']
    G.OBJECTIVES += ['bm.owt', 'bm.gvbc', 'bm.gvbw']
    for kind, go, nm, col, try_ in KINDS:
        far = G.FUNCS[f'p73/fol/{kind}_far']
        assert far[0] == f'function bm:{go}', (kind, far[0])
        far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{kind}')
        fn(f'p103/fol/wait_{kind}', [f'tag @a[tag=bm.fown] add bm.ow_{kind}', f'function bm:{go}',
                                     tellraw('@a[tag=bm.fown]', P + [T(f'{nm} waits outside the vault', col), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                     T('(Back with you when you\'re home.)', 'dark_gray')]),
                                     'tag @a remove bm.fown'])
    G.FUNCS['p70/unraid'].append('scoreboard players set @s bm.owt 3')
    second.append('execute as @a[scores={bm.owt=1..}] at @s run function bm:p103/fol/tick')
    fn('p103/fol/tick', ['execute if dimension bm:gutter run return run scoreboard players reset @s bm.owt', 'scoreboard players remove @s bm.owt 1',
                         'execute if score @s bm.owt matches 1.. run return 0', 'scoreboard players reset @s bm.owt'] +
       [f'execute if entity @s[tag=bm.ow_{kind}] run function bm:p103/fol/back_{kind}' for kind, *_r in KINDS])
    for kind, go, nm, col, try_ in KINDS:
        fn(f'p103/fol/back_{kind}', [f'tag @s remove bm.ow_{kind}', f'function bm:{try_}'])

    # ================================================================== 6b. BEGIN: a ready check
    # (the den's BEGIN buttons start the heist at once only if everyone has a kit and nobody's at the Lockers; otherwise they
    #  name who isn't ready - press again within ten seconds to go anyway: whoever has no kit gets the Offense one, as before)
    lt3 = G.FUNCS['p70/r/lobby/tick']
    nb = 0
    for i, l in enumerate(lt3):
        if l.endswith('minecraft:pale_oak_button[powered=true] run function bm:p70/begin'):
            lt3[i] = l.replace('run function bm:p70/begin', 'run function bm:p103/begin_try'); nb += 1
    assert nb == 2, nb
    lt3[0:0] = ['scoreboard players remove @s[scores={bm.gvbc=1..}] bm.gvbc 1', 'scoreboard players remove @s[scores={bm.gvbw=1..}] bm.gvbw 1']
    crew_here = '@a[tag=bm.gvp]'
    fn('p103/begin_try', ['execute if score @s bm.gvbc matches 1.. run return 0', 'scoreboard players set @s bm.gvbc 40',
                          'scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @a remove bm.nrdy',
                          f'execute as {crew_here} if score @s bm.gvi = #gi bm.rng unless score @s bm.gvrole matches 1.. run tag @s add bm.nrdy',
                          f'execute as {crew_here} if score @s bm.gvi = #gi bm.rng if function bm:p84/lk/inside run tag @s add bm.nrdy',
                          'execute unless entity @a[tag=bm.nrdy] run return run function bm:p70/begin',
                          'execute if score @s bm.gvbw matches 1.. run return run function bm:p103/begin_force',
                          'scoreboard players set @s bm.gvbw 200',
                          f'execute as {crew_here} if score @s bm.gvi = #gi bm.rng run ' + tellraw('@s', P + [T('Not everyone\'s ready: ', '#ffe07a', bold=True),
                                                                                                            {'selector': '@a[tag=bm.nrdy]', 'color': 'white'},
                                                                                                            T(' - no kit yet (right-click a rack), or still at the Lockers. ', 'gray'),
                                                                                                            T('Press BEGIN again to go anyway.', '#ffe07a')]),
                          f'execute as {crew_here} if score @s bm.gvi = #gi bm.rng at @s run playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.8 0.8',
                          'tag @a remove bm.nrdy'])
    fn('p103/begin_force', ['scoreboard players set @s bm.gvbw 0',
                            f'execute as {crew_here} if score @s bm.gvi = #gi bm.rng run ' + tellraw('@s', P + [T('Off you go', GOLD, bold=True), T(' - anyone without a kit takes the Offense loaners.', 'gray')]),
                            'tag @a remove bm.nrdy', 'function bm:p70/begin'])

    # ================================================================== 7. THE FIXER'S DOOR: an archway (the tier's metal), a swirl you walk into
    # (the den's against the west wall, always open; the treasury's against the far wall, swirling once the vault opens.
    #  The arches are in the rooms' templates; here the swirl, the labels and the sparkle. They ask first mid-heist - 1a.)
    swirl = lambda h=3, w=1: snbt({'Tags': ['bm.gvprop', 'bm.exdoor'], 'block_state': {'id': 'minecraft:nether_portal', 'properties': {'axis': 'z'}},
                                   'brightness': {'block': 15, 'sky': 15},
                                   'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                      'translation': [F(-0.5), F(0), F(-w / 2)], 'scale': [F(1), F(h), F(w)]}})
    li2 = G.FUNCS['p70/r/lobby/init']
    n_ = len(li2); li2[:] = [l for l in li2 if '"Leave the heist"' not in l]; assert len(li2) == n_ - 1, 'the den\'s leave label moved'
    vi = G.FUNCS['p70/r/vault/init']
    n_ = len(vi); vi[:] = [l for l in vi if '"The way out"' not in l]; assert len(vi) == n_ - 1, 'the treasury\'s way-out label moved'
    li2 += [f'fill {rel(-1, 4, 11)} {rel(-1, 7, 13)} {RM.WALL}',                  # (2.68: the doorway's backed - no more view into the void)
            f'summon minecraft:block_display {rel(*DEN_DOOR)} {swirl(4, 3)}',
            lab(DEN_DOOR[0] + 1.1, 8.25, DEN_DOOR[2], [_T('THE FIXER\'S DOOR\n', GOLD, bold=True), _T('home (it asks first, mid-heist)', 'gray')])]
    vi += [lab(VAULT_DOOR[0] - 0.3, 8.1, VAULT_DOOR[2], [_T('THE FIXER\'S DOOR\n', GOLD, bold=True), _T('home, with your haul', 'gray')])]
    G.FUNCS['p70/r/vault/open'] += [f'summon minecraft:block_display {rel(*VAULT_DOOR)} {swirl()}',
                                    f'particle minecraft:reverse_portal {rel(VAULT_DOOR[0], 5.5, VAULT_DOOR[2])} 0.1 0.9 0.4 0.05 60']
    fast.append('execute as @e[type=minecraft:marker,tag=bm.exitm] at @s if entity @a[distance=..20] run function bm:p103/door_fx')
    fn('p103/door_fx', ['particle minecraft:portal ~ ~1.5 ~ 0.05 0.8 0.35 0.4 3', 'particle minecraft:wax_on ~ ~1.5 ~ 0.1 0.9 0.4 0 1'])

    # ================================================================== 8. THE LEDGER'S LOCKER HALL TRIP: from solid, safe ground, after a 3-second hold
    # (the Office pages work anywhere; only the trip is gated - it saves where you stand and brings you back there, so that
    #  spot must be safe: on the ground (not mid-fall, mid-flight, mounted or in water or lava), not in a fight (hurt in the
    #  last 10 seconds), not inside a boss dungeon or the Hollow, and not in the gutter (the Locker Hall itself, or a heist).
    #  The Overworld, the Nether and the End are all fine. Moving, changing dimension or getting hurt cancels the hold.
    #  The den's copper door, before a heist begins, is as it was.)
    objs8 = ['bm.lkht', 'bm.lkch', 'bm.lkx', 'bm.lky', 'bm.lkz', 'bm.lkdm']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs8] + ['scoreboard objectives add bm.lkdt minecraft.custom:minecraft.damage_taken']
    G.OBJECTIVES += objs8 + ['bm.lkdt']
    G.wjson('bm/tags/worldgen/structure/boss_dungeons.json',
            {'values': [{'id': f'bm:p2_{d}', 'required': False} for d in ('brood', 'frost', 'tide', 'hex', 'keep', 'lucky')]})
    G.wjson('bm/predicate/p103/boss_dungeon.json', {'condition': 'minecraft:location_check', 'predicate': {'structures': '#bm:boss_dungeons'}})
    G.wjson('bm/predicate/p103/wet.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:location_check', 'predicate': {'fluid': {'fluids': f'#minecraft:{w}'}}} for w in ('water', 'lava')]})
    second += ['scoreboard players remove @a[scores={bm.lkht=1..}] bm.lkht 1',
               'scoreboard players set @a[scores={bm.lkdt=1..}] bm.lkht 10', 'scoreboard players reset @a[scores={bm.lkdt=1..}] bm.lkdt']
    PV = [T('[', 'dark_gray'), T('Vault', GOLD, bold=True), T('] ', 'dark_gray')]      # (the Locker Hall's own voice - as phase84's)
    lsay = lambda txt, col='gray': tellraw('@s', PV + [T(txt, col)])
    no = lambda txt: [lsay(txt, 'red'), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1']
    fl = G.FUNCS['p84/lk/from_ledger']
    k = next(i for i, l in enumerate(fl) if l == 'function bm:p84/lk/enter')
    fl[k] = 'execute at @s run function bm:p103/lh/try'
    fn('p103/lh/try', [
        'execute if dimension bm:gutter run return run function bm:p103/lh/no_gut',
        'execute if dimension bm:hollow_throne run return run function bm:p103/lh/no_dun',
        'execute if predicate bm:p103/boss_dungeon run return run function bm:p103/lh/no_dun',
        'execute if entity @s[tag=bm.adv] run return run function bm:p103/lh/no_dun',
        'execute if predicate bm:p21/riding run return run function bm:p103/lh/no_ride',
        'execute if predicate bm:p103/wet run return run function bm:p103/lh/no_wet',
        'execute unless entity @s[nbt={OnGround:1b}] run return run function bm:p103/lh/no_air',
        'execute if score @s bm.lkdt matches 1.. run scoreboard players set @s bm.lkht 10',
        'execute if score @s bm.lkht matches 1.. run return run function bm:p103/lh/no_hurt',
        'function bm:p103/lh/start'])
    for k_, txt in (('gut', 'You\'re in the gutter already - the Locker Hall\'s door is the copper one in the den.'),
                    ('dun', 'Not from inside a boss dungeon or the Hollow - head back out first.'),
                    ('ride', 'Get off your mount first.'),
                    ('wet', 'Get out of the water (or lava) first.'),
                    ('air', 'Find your feet first - not while you\'re falling, flying or climbing.')):
        fn(f'p103/lh/no_{k_}', no(txt))
    fn('p103/lh/no_hurt', [tellraw('@s', PV + [T('You were hurt just now - wait ', 'red'), {'score': {'name': '@s', 'objective': 'bm.lkht'}, 'color': 'white', 'bold': True},
                                             T(' more second(s), then try again.', 'red')]),
                           'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1'])
    fn('p103/lh/dim', ['scoreboard players set #lkdm bm.rng 4', 'execute if dimension minecraft:overworld run scoreboard players set #lkdm bm.rng 1',
                       'execute if dimension minecraft:the_nether run scoreboard players set #lkdm bm.rng 2',
                       'execute if dimension minecraft:the_end run scoreboard players set #lkdm bm.rng 3'])
    fn('p103/lh/start', ['tag @s add bm.lkch', 'scoreboard players set @s bm.lkch 60',
                         'function bm:p103/lh/dim', 'scoreboard players operation @s bm.lkdm = #lkdm bm.rng',
                         'execute store result score @s bm.lkx run data get entity @s Pos[0] 10',
                         'execute store result score @s bm.lky run data get entity @s Pos[1] 10',
                         'execute store result score @s bm.lkz run data get entity @s Pos[2] 10',
                         lsay('Hold still for 3 seconds - moving or getting hurt stops it.'),
                         title('@s', 'actionbar', [T('Opening the Locker Hall... ', '#c89a5a'), T('3', 'white', bold=True)]),
                         'playsound minecraft:block.iron_door.open player @s ~ ~ ~ 0.5 0.6',
                         'particle minecraft:wax_on ~ ~1 ~ 0.4 0.8 0.4 0 12'])
    tick.append('execute as @a[tag=bm.lkch] at @s run function bm:p103/lh/step')
    fn('p103/lh/step', ['function bm:p103/lh/dim', 'execute unless score #lkdm bm.rng = @s bm.lkdm run return run function bm:p103/lh/moved',
                        'execute if score @s bm.lkdt matches 1.. run return run function bm:p103/lh/hit',
                        'execute if score @s bm.lkht matches 1.. run return run function bm:p103/lh/hit'] +
       [l for a, o in ((0, 'bm.lkx'), (1, 'bm.lky'), (2, 'bm.lkz')) for l in (
           f'execute store result score #lkd bm.rng run data get entity @s Pos[{a}] 10', f'scoreboard players operation #lkd bm.rng -= @s {o}',
           'execute unless score #lkd bm.rng matches -8..8 run return run function bm:p103/lh/moved')] +
       ['scoreboard players remove @s bm.lkch 1',
        'execute if score @s bm.lkch matches 40 run ' + title('@s', 'actionbar', [T('Opening the Locker Hall... ', '#c89a5a'), T('2', 'white', bold=True)]),
        'execute if score @s bm.lkch matches 20 run ' + title('@s', 'actionbar', [T('Opening the Locker Hall... ', '#c89a5a'), T('1', 'white', bold=True)]),
        'execute if score @s bm.lkch matches 20 run playsound minecraft:block.note_block.hat player @s ~ ~ ~ 0.6 1.2',
        'execute if score @s bm.lkch matches 40 run playsound minecraft:block.note_block.hat player @s ~ ~ ~ 0.6 1',
        'execute if score @s bm.lkch matches ..0 run function bm:p103/lh/go'])
    fn('p103/lh/stop', ['tag @s remove bm.lkch', 'scoreboard players reset @s bm.lkch'])
    fn('p103/lh/go', ['function bm:p103/lh/stop', 'function bm:p84/lk/enter'])
    fn('p103/lh/moved', ['function bm:p103/lh/stop', title('@s', 'actionbar', T('You moved - the Locker Hall stays shut.', 'red')),
                         lsay('You moved, so the Locker Hall stays shut. Stand still and try again from the Ledger.', 'red'),
                         'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 0.5 0.8'])
    fn('p103/lh/hit', ['function bm:p103/lh/stop', 'scoreboard players set @s bm.lkht 10', title('@s', 'actionbar', T('You were hurt - the Locker Hall stays shut.', 'red')),
                       lsay('You were hurt, so the Locker Hall stays shut. Get clear of the fight - 10 seconds unhurt - and try again.', 'red'),
                       'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 0.5 0.8'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second
