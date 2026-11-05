"""3.1: THE RAT PACK - the Partner Wheel renamed, made the pack's one carry-all (design_ratpack.md, the owner's go).

THE NAME     the Partner Wheel is "The Rat Pack" wherever a player reads it (its name and lore, every menu title and chat line).
             Its id stays partner_wheel (every check keeps working); a wheel already in a world is re-issued as a Rat Pack the
             first second it's in a pocket (custom_data bmrp, phase129's way) - and keeps everything, since what it holds was
             always kept per player (storage bm:pw p<pid>), never in the item. Sold by THE FENCE now (3 Medallions; was Cecil).
THE FRONT    using it opens a short front page: Partners ›, Pocket ›, Keyring ›, Charms ›, Maps ›, Mounts ›, Bags ›, Collectors ›,
             ⚙ Settings ›, the Handbook (when it's in the Pocket) and Guide ›. Each section is its own page; the Partners page is the
             old wheel (with « Rat Pack). Sneak + use still brings your partners to your side.
PAGES        Pocket, Keyring, Charms, Maps and Mounts are one list each: the things you've put on, eight a page (‹ Previous /
             Next ›), each row its item's own icon and name (× how many). "Press to: Use" or "Press to: Take back" (a switch on
             the page) says what a row does; the Keyring only takes back. Put on: hold it in your off hand and use the Rat Pack.
             Taken back: the same item, once (at your feet, yours to pick up).
  USE        a Pocket tool, a map, a mount call: as using the item - it's put in your main hand for that moment, used (its own
             use function, as the hold-to-use trigger runs it), and whatever's left of it goes back on the Pack (a map is used
             up; a whistle that's spent is gone). Your own main-hand item is put back.
  CARRIED    while you carry the Pack, everything on it counts as carried wherever the pack checks for that item (each check
             of "in your pockets / off hand" also takes the Pack - tag bm.rqt_<item>, set each second) - the keys at the
             market gates, the charms' effects, the Ledger's welcome gift, the bond compass at the Keeper's island...
             A check that USES one up (clear) takes it off the Pack instead when it isn't in your pockets.
  CHARMS     every charm held is listed with a clear ● (active) / ○; pressing switches it. The charms that work only in the
             off hand (the Four-Leaf, the Lucky Horseshoe, the Mudlark's and the Fletcher's) are "worn": one at a time.
AUTO-PACK    the ⚙ Settings page: a switch per kind (followers' items, Pocket tools, keys, charms, maps, mount calls, bags,
             collectors; the first five on by default). Once a second, an item of a kind switched on that's in your own
             inventory (never your off hand, a chest or a bundle; never in a heist) goes on the Pack, with a line in chat.
             Nothing is pulled the Pack can't hold (a second of a one-of-a-kind, an 11th bag), and the item leaves your
             inventory only once it's stored.
BAGS / COLLECTORS (up to 10 of each: Backpacks, Vacuum Satchels, Pistachio's Spirit Jars, Dennis's Ore Magnets, Prime Coolers)
             each keeps its own contents (the item, container and all, in bm:pw p<pid>.rb.<kind>). Bags › / Collectors › list
             them with their fill and first two stacks; a row opens it: a look inside (its stacks as item icons with their
             counts - hover for the tooltip), Unfold (phase33's barrel, exactly as using the item: the same fold rules; it folds
             back onto the Pack), Take it back, its own Vacuum / Auto-collect switch (on ones fill first-with-room-first, as
             carried), the Prime Cooler's Cuts -> Tokens, and for the collectors Deposit / Withdraw a stack / Withdraw all.
             No bag in a bag (phase248's rule stands: the Pack is no bag); none of it in a heist (the Pack waits at the coat check).
THE HEIST LEDGER  the Pack never goes into a heist. On every entry every raider is handed a Heist Ledger (the Fixer's Ledger, marked
             bm_hl: heist-only), whatever Ledger they own. Dropped, framed or put in a chest near you, it's pulled back and a
             fresh one is in your pocket within a moment; leaving the heist (any way out: p70/unraid) takes every one off you,
             and anyone outside a heist loses one at once. The welcome gift (p80/first_ledger) counts a Ledger on your Pack.
Codes 8660-8999 (p277/act, each line menu-checked) and 9160-9249 (p277/b/act) - see BUTTON_CODES.md."""
import re
from items import T, ITEMS, ITEM_VERSION, TOTEM
from nbt import snbt, B, Int
from useitem import HOLD

PURPLE = '#b48cff'
PRE = [T('[', 'dark_gray'), T('Rat Pack', PURPLE, bold=True), T('] ', 'dark_gray')]
RQV = 1                                            # (custom_data bmrp: a wheel without it is re-issued as a Rat Pack)

# ------------------------------------------------------------------ menus and codes
M_FRONT, M_SET = 8660, 8673
M_CAT = {'pocket': 8690, 'keys': 8691, 'charms': 8692, 'maps': 8693, 'mounts': 5640}      # (the Mounts page keeps phase249's menu)
B_SEC = {'partners': 8661, 'pocket': 8662, 'keys': 8663, 'charms': 8664, 'maps': 8665, 'mounts': 8666, 'bags': 8667,
         'cols': 8668, 'settings': 8669, 'handbook': 8670, 'guide': 8671}
B_BACK, B_MODE, B_PREV, B_NEXT, B_YOURS = 8672, 8682, 8683, 8684, 8685
B_AP0 = 8674                                       # (8674-8681: the auto-pack switches)
B_E0 = 8700                                        # (8700+n: an entry's row)
M_BAGS, M_COLS, M_BAG = 9160, 9161, 9170
B_UNFOLD, B_TAKE, B_AUTO, B_CONV, B_DEP, B_WD1, B_WDA, B_BBACK, B_DEPALL = 9162, 9163, 9164, 9165, 9166, 9167, 9168, 9169, 9172
B_ROW0 = 9200                                      # (9200 + kind*10 + slot: a bag's / collector's row)

# ------------------------------------------------------------------ what goes where (keyed by item id in storage and scores: no numbering to keep)
POCKET = ['bm_handbook', 'fixers_ledger', 'particle_toggler', 'waytoken', 'crew_flare', 'courier_whistle', 'fixers_card', 'renewal_key',
          'ender_pouch', 'wayfarers_lodestar', 'enchanted_sundial', 'merchants_bell', 'lodestone_locket', 'bond_compass', 'chorus_compass',
          'surface_charm', 'lava_wader_charm',
          'bankers_card', 'ring_burrows', 'pocket_rift', 'fair_weather_bell']     # (3.0y: the owner - the Banker's Card was missed; so were phase29's other right-click tools)
KEYS = ['market_key', 'silver_key', 'gold_key', 'rat_king_key', 'mail_key', 'trial_key_fob'] + \
       [f'key_{d}' for d in ('brood', 'frost', 'tide', 'hex', 'keep')] + \
       [f'vkey_{d}' for d in ('brood', 'frost', 'tide', 'hex', 'keep', 'hollow', 'lucky')] + \
       [f'bkey_{d}' for d in ('brood', 'frost', 'tide', 'hex', 'keep', 'hollow', 'lucky')] + ['ukey', 'ukey_victor', 'akey', 'akey_victor']
COSMETIC = ['charm_eclipse', 'charm_ember', 'charm_frost', 'charm_petal', 'charm_soul', 'charm_gilded', 'charm_heart', 'charm_storm',
            'charm_rainbow', 'charm_cinder', 'charm_starlit', 'charm_glimmer', 'charm_bloom', 'charm_void', 'charm_ashen', 'charm_crimson_drip',
            'charm_bloodbat', 'charm_blood_halo', 'charm_clover', 'charm_gold_rush', 'charm_jackpot_crown', 'charm_xenite_glow',
            'charm_tractor_beam', 'charm_saucer_orbit', 'charm_wings_angel', 'charm_wings_evil']
CARRY_CHARMS = COSMETIC + ['water_charm', 'lava_charm', 'four_leaf_charm', 'shark_tooth_charm', 'xp_charm', 'showstopper_charm', 'grave_charm']
WORN_CHARMS = ['lucky_charm', 'horseshoe_charm', 'mudlarks_charm', 'fletchers_charm']           # (off hand only: one worn at a time)
CHARMS = CARRY_CHARMS + WORN_CHARMS
MAPS = ['sealed_map_market', 'sealed_map_graveyard', 'sealed_map_frog', 'sealed_map_leo', 'sealed_map_omega', 'sealed_map_mothership',
        'sealed_map_dread', 'sealed_map_kingdom', 'sealed_explorer_map', 'sealed_map_db_snow', 'sealed_map_db_witch', 'sealed_map_db_shark',
        'sealed_map_brood', 'sealed_map_frost', 'sealed_map_tide', 'sealed_map_hex', 'sealed_map_keep', 'hive_coords', 'message_bottle']
MOUNTS = ['mecha_remote', 'ember_call', 'void_call']
# (3.0y) the carrot-on-a-stick tools phase29 dispatches from the main hand (not in useitem.HOLD): used from a row the same way
CARROT = {'bankers_card': 'bm:p31/bank/card', 'ring_burrows': 'bm:p29/burrow/use', 'pocket_rift': 'bm:p29/rift/use', 'fair_weather_bell': 'bm:p29/bell/use'}
CATS = {'pocket': POCKET, 'keys': KEYS, 'charms': CHARMS, 'maps': MAPS, 'mounts': MOUNTS}
HELD = {'bond_compass'}                            # (checked "in either hand" - weapon.* - too)
# the Pack's auto-pack kinds: (key, label, default on)
AP = [('fol', 'Followers\' items', True), ('pocket', 'Pocket tools', True), ('keys', 'Keys', True), ('charms', 'Charms', True),
      ('maps', 'Maps', True), ('mounts', 'Mount calls', False), ('bags', 'Bags', False), ('cols', 'Collectors', False)]
PAGE_OF = {'fol': 'Partners', 'pocket': 'Pocket', 'keys': 'Keyring', 'charms': 'Charms', 'maps': 'Maps', 'mounts': 'Mounts',
           'bags': 'Bags', 'cols': 'Collectors'}
SEC = {'pocket': ('✦', 'Pocket', '#e8c070'), 'keys': ('⚿', 'Keyring', '#ffd700'), 'charms': ('✿', 'Charms', '#ff9ad8'),
       'maps': ('⚑', 'Maps', '#7ad8ff'), 'mounts': ('◈', 'Mounts', '#7ad8ff')}
# bags and collectors: (key, item, page, name, phase33 kind, collects: (range, how many a pass, filter run as the item), switch)
BAGK = [('bp', 'backpack', 'bags', 'Backpack', 'pack', None, None),
        ('vs', 'vacuum_satchel', 'bags', 'Vacuum Satchel', 'box', (6, 4, 'unless items entity @s contents @@BAG@@'), 'vac'),
        ('sj', 'spirit_jar', 'cols', 'Spirit Jar', 'mobcol', (8, 16, 'if items entity @s contents #bm:p174_mob'), 'rpoff'),
        ('om', 'ore_magnet', 'cols', 'Ore Magnet', 'orecol', (8, 16, 'if items entity @s contents #bm:p174_ore'), 'rpoff'),
        ('pc', 'prime_cooler', 'cols', 'Prime Cooler', 'cool', (6, 16, 'if function bm:p148/cool/prime'), 'coff')]
BAGMAX = 10
HL = '*[minecraft:custom_data~{bm:"fixers_ledger",bm_hl:1b}]'
HLNOT = ',!minecraft:custom_data~{bm_hl:1b}'
NOPK = ',!minecraft:custom_data~{bm_rpno:1b}'          # (taken back on purpose: auto-pack leaves it be)

assert len(set(sum(CATS.values(), []))) == len(sum(CATS.values(), [])), 'an item on two pages'
for _i in sum(CATS.values(), []) + [b[1] for b in BAGK]:
    assert _i in ITEMS, _i

# ------------------------------------------------------------------ the item: renamed (import time - before any give, loot table or re-sync is written)
_W = ITEMS['partner_wheel']
_W['name'] = 'The Rat Pack'
_W['comps']['minecraft:item_name']['extra'][1]['text'] = 'The Rat Pack'
_W['comps']['minecraft:lore'] = [T(*l) if isinstance(l, tuple) else T(l, 'gray') for l in [
    'Everything you carry for the market, in one pack.', ('Hold a partner\'s item, a tool, a key, a charm,', 'blue'),
    ('a map, a mount call or a bag in your off hand', 'blue'), ('and use the Pack: it goes on.', 'blue'),
    ('Use it alone: its pages - call, use, take back.', 'blue'), ('Sneak + use: your partners come to your side.', 'blue'),
    ('Carry it: all it holds counts as carried.', 'dark_aqua'), ('It remembers everything - even a new Pack.', 'gray'),
    ('It waits at the coat check on a heist.', 'gray'), ('From the Fence.', 'dark_gray')]] + [_W['comps']['minecraft:lore'][-1]]
_W['custom']['bmrp'] = RQV
_W['comps']['minecraft:custom_data']['bmrp'] = RQV

# (every other item's own words: the wheel is the Rat Pack there too)
WORDS = [(r'\bPartner Wheel\b', 'Rat Pack'), (r'\bthe Partner Wheel\b', 'the Rat Pack'),
         (r'\bon your wheel\b', 'on your Rat Pack'), (r'\boff your wheel\b', 'off your Rat Pack'), (r'\byour wheel\b', 'your Rat Pack'),
         (r'\bon the wheel\b', 'on the Rat Pack'), (r'\boff the wheel\b', 'off the Rat Pack'), (r'\bor the wheel\b', 'or the Rat Pack'),
         (r'\b[Uu]se the wheel\b', lambda m: m.group(0)[0] + 'se the Rat Pack'), (r'\bThe wheel is still turning\b', 'The Rat Pack is still calling'),
         (r'\b[Tt]he wheel turns\b', lambda m: m.group(0)[0] + 'he Rat Pack calls'), (r'\ba new wheel\b', 'a new Pack'),
         (r'\bon one wheel\b', 'in one Pack'), (r'\bthe wheel\b', 'the Rat Pack'), (r'\bThe wheel\b', 'The Rat Pack')]
_KEEP = re.compile(r'[Cc]heese [Ww]heel|cartwheel|wheel within a wheel|shapes wheel|[Ww]heel of')


def reword(s):
    if 'heel' not in s or _KEEP.search(s): return s
    for a, b in WORDS: s = re.sub(a, b, s)
    return s


def _reword_comp(c):
    if isinstance(c, dict):
        return {k: (reword(v) if k == 'text' and isinstance(v, str) else _reword_comp(v)) for k, v in c.items()}
    if isinstance(c, list): return [_reword_comp(x) for x in c]
    return c


for _iid, _it in ITEMS.items():
    if _iid == 'partner_wheel': continue
    _l = _it['comps'].get('minecraft:lore')
    if _l and any('heel' in str(x) for x in _l): _it['comps']['minecraft:lore'] = _reword_comp(_l)


def holds(iid, extra=''):
    return f'*[minecraft:custom_data~{{bm:"{iid}"}}{extra}]'


def icon(iid, col='white'):
    mdl = ITEMS[iid]['comps'].get('minecraft:item_model', f'minecraft:{ITEMS[iid]["base"].split(":")[-1]}')
    ns_, p = mdl.split(':', 1) if ':' in mdl else ('minecraft', mdl)
    if ns_ == 'minecraft' and p in ('compass', 'recovery_compass', 'clock'): p += '_00'
    return {'type': 'object', 'object': 'atlas', 'atlas': 'minecraft:items', 'sprite': f'{ns_}:item/{p}', 'fallback': {'text': '◆', 'color': col}}


def colour(iid):
    try: return ITEMS[iid]['comps']['minecraft:item_name']['extra'][1]['color']
    except (KeyError, IndexError, TypeError): return 'white'


def stack_of(iid):
    return int(ITEMS[iid]['comps'].get('minecraft:max_stack_size', 64 if ITEMS[iid]['base'] != TOTEM else 1))


def generate(G):
    import phase28 as P28
    import phase148 as P148
    import phase18 as P18
    import phase248 as P248
    F, fn = G.FUNCS, G.fn
    tellraw, title, give = G.tellraw, G.title, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col) if isinstance(txt, str) else txt)
    second, fast, load = F['loop/second'], F['loop/fast'], F['load']
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4'
    page_turn = 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.2'
    pid = 'execute store result storage bm:rp t.pid int 1 run scoreboard players get @s bm.pid'
    on_txt, off_txt = T('on', 'white', bold=True), T('off', '#ff8a8a', bold=True)
    head = lambda sub: [T('THE RAT PACK', PURPLE, bold=True), T(f'  ·  {sub}', 'gray')]
    back_btn = P28.btn([T('« Rat Pack', 'gray')], B_BACK, width=150, tooltip=T('Back to the Rat Pack\'s front page', 'gray'))
    rep = {}
    objs = ['bm.rqhl', 'bm.rbk', 'bm.rbj'] + [f'bm.rqap_{k}' for k, *_r in AP] + [f'bm.pg_rp{c}' for c in list(CATS) + ['bags', 'cols']]

    # ================================================================== THE ENTRIES
    E = []                                    # dict(n, iid, cat, obj, path, tag, use (function or None), how ('hold'|'eat'|None), stack, kind)
    for cat, L in CATS.items():
        for iid in L:
            n = len(E)
            hb = iid == 'bm_handbook'
            kind = 'worn' if iid in WORN_CHARMS else ('carry' if iid in CARRY_CHARMS else 'item')
            use, how = None, None
            if hb: use, how = 'bm:p276/hb_open', 'fn'
            elif cat != 'keys' and kind == 'item':
                if iid in HOLD: use, how = HOLD[iid], 'hold'
                elif iid in CARROT: use, how = CARROT[iid], 'hold'
                else:
                    import json, os
                    p = G.path('data', 'bm', 'advancement', 'consume', f'{iid}.json')
                    if os.path.exists(p):
                        use, how = json.load(open(p))['rewards']['function'], 'eat'
            E.append(dict(n=n, iid=iid, cat=cat, obj='bm.pwhb' if hb else f'bm.rq_{iid}', path='hb' if hb else f'rq_{iid}',
                          tag='bm.pw_hb' if hb else f'bm.rqt_{iid}', use=use, how=how, stack=stack_of(iid), kind=kind,
                          name=ITEMS[iid]['name'], col=colour(iid)))
    BY = {e['iid']: e for e in E}
    assert len(E) <= 200, len(E)
    objs += [e['obj'] for e in E if e['obj'] != 'bm.pwhb'] + [f'bm.rqo_{i}' for i in CARRY_CHARMS] + [f'bm.rb_{k}' for k, *_r in BAGK]
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    rep['entries'] = len(E)
    rep['usable'] = sum(1 for e in E if e['use'])

    # ---------------------------------------------------------------- who has what counted as carried (each second, and at once on a change)
    tg = []
    for e in E:
        if e['iid'] == 'bm_handbook': continue
        T_, O = e['tag'], e['obj']
        tg += [f'tag @s remove {T_}', f'execute if entity @s[tag=bm.pwc,scores={{{O}=1..}}] run tag @s add {T_}']
        if e['kind'] == 'carry': tg.append(f'execute if score @s bm.rqo_{e["iid"]} matches 1 run tag @s remove {T_}')
        if e['kind'] == 'worn': tg.append(f'execute unless entity @s[tag=bm.rqw_{e["iid"]}] run tag @s remove {T_}')
    # the off-hand-only charms that are attributes: given while worn on the Pack (and not held in the off hand itself)
    for iid in WORN_CHARMS:
        mods = ITEMS[iid]['comps'].get('minecraft:attribute_modifiers', [])
        if not mods: continue
        add = [f'attribute @s {m["type"]} modifier add bm:rp_{iid}_{k} {m["amount"]} {m["operation"]}' for k, m in enumerate(mods)]
        rem = [f'attribute @s {m["type"]} modifier remove bm:rp_{iid}_{k}' for k, m in enumerate(mods)]
        fn(f'p277/w/on_{iid}', ['tag @s add bm.rqa_' + iid] + add)
        fn(f'p277/w/off_{iid}', ['tag @s remove bm.rqa_' + iid] + rem)
        tg += [f'execute if entity @s[tag=bm.rqt_{iid},tag=!bm.rqa_{iid}] unless items entity @s weapon.offhand {holds(iid)} run function bm:p277/w/on_{iid}',
               f'execute if entity @s[tag=bm.rqa_{iid}] unless entity @s[tag=bm.rqt_{iid}] run function bm:p277/w/off_{iid}',
               f'execute if entity @s[tag=bm.rqa_{iid}] if items entity @s weapon.offhand {holds(iid)} run function bm:p277/w/off_{iid}']
    fn('p277/tg', tg)
    second.append('execute as @a run function bm:p277/tg')

    # ================================================================== "COUNTS AS CARRIED": every check of an entry's item also takes the Pack
    skip = ('p277/', 'p179/', 'admin/', 'p18/', 'p129/', 'p84/lk/', 'p72/', 'p121/strip', 'p80/kit/', 'p104/key/', 'p28/key/', 'p175/',
            'p145/hand_free', 'p276/', 'p249/w/', 'p242/ms/upgrade', 'p173/ledger/', 'h3g/', 'p155/')
    bad_run = re.compile(r'run (?:.* )?(?:item replace entity @s|item modify entity @s|clear @s)')
    patched, dec_needed = {}, set()
    for name in list(F):
        if name.startswith(skip): continue
        L = F[name]
        ids = set(re.findall(r'custom_data~\{bm:"([a-z0-9_]+)"\}\]', '\n'.join(L)))
        if not ids & set(BY): continue
        changed = False
        for e in E:
            if e['iid'] not in ids: continue
            H = holds(e['iid'])
            if not any(f' {H}' in l for l in L): continue
            cont, off, wpn = f'items entity @s container.* {H}', f'items entity @s weapon.offhand {H}', f'items entity @s weapon.* {H}'
            Tq = f'entity @s[tag={e["tag"]}]'
            worn = e['kind'] == 'worn'
            out, n0 = [], 0
            for i, l in enumerate(L):
                out.append(l)
                if f' {H}' not in l: continue
                # "doesn't have it": nor on the Pack
                if not worn and f'unless {cont}' in l and f'if {off}' not in l and f'unless {Tq}' not in l:
                    if f'unless {cont} unless {off}' in l: out[-1] = l.replace(f'unless {cont} unless {off}', f'unless {cont} unless {off} unless {Tq}', 1)
                    else: out[-1] = l.replace(f'unless {cont}', f'unless {cont} unless {Tq}', 1)
                    n0 += 1; continue
                if worn and f'unless {off}' in l and f'unless {Tq}' not in l:
                    out[-1] = l.replace(f'unless {off}', f'unless {off} unless {Tq}', 1); n0 += 1; continue
                if e['iid'] in HELD and f'unless {wpn}' in l:
                    out[-1] = l.replace(f'unless {wpn}', f'unless {wpn} unless {Tq}', 1); n0 += 1; continue
                if bad_run.search(l.split(f' {H}', 1)[1]): continue
                # "has it": a twin line for the Pack (never both: the twin asks that it isn't in the pockets or the off hand)
                if not worn and f'if {cont}' in l and f'unless {cont}' not in l:
                    out.append(l.replace(f'if {cont}', f'if {Tq} unless {cont} unless {off}', 1)); n0 += 1; continue
                if f'if {off}' in l and f'unless {cont} if {off}' not in l:
                    if not worn and (l.replace(f'if {off}', f'if {cont}') in L): continue          # (its pockets line has the twin)
                    out.append(l.replace(f'if {off}', f'if {Tq} unless {off}' + ('' if worn else f' unless {cont}'), 1)); n0 += 1; continue
                if e['iid'] in HELD and f'if {wpn}' in l:
                    out.append(l.replace(f'if {wpn}', f'if {Tq} unless {wpn}', 1)); n0 += 1; continue
            if n0:
                # (a check that uses one up takes it off the Pack when it isn't in the pockets)
                out2 = []
                for l in out:
                    m = re.search(r'(?:^|run )clear @s ' + re.escape(H) + r'(?: (\d+))?$', l)
                    if m and 'store result' not in l and not worn:
                        out2.append(f'execute if {Tq} unless {cont} unless {off} run function bm:p277/q/dec_{e["iid"]}'); dec_needed.add(e['iid'])
                    out2.append(l)
                L[:] = out2; changed = True
                patched.setdefault(e['iid'], []).append(name)
        if changed: F[name] = L
    # the grave charm: a grave if it was on the Pack (the Pack among what you dropped)
    gd = F['p50/grave/died']
    k = next(i for i, l in enumerate(gd) if 'bm:"grave_charm"' in l and '#gc bm.rng 1' in l)
    gd.insert(k + 1, f'execute if entity @s[tag=bm.rqt_grave_charm] as @e[type=minecraft:item,tag=bm.gfresh,distance=..4] '
                     f'if items entity @s contents {holds("partner_wheel")} run scoreboard players set #gc bm.rng 1')
    patched.setdefault('grave_charm', []).append('p50/grave/died')
    for iid in sorted(dec_needed):
        e = BY[iid]
        fn(f'p277/q/dec_{iid}', [pid, f'data modify storage bm:rp t.k set value "{e["path"][1:]}"', 'function bm:p277/s/dec with storage bm:rp t',
                                 f'execute store result score @s {e["obj"]} run function bm:p277/s/cnt with storage bm:rp t',
                                 'function bm:p277/tg'])
    # (the market key turning in your pocket as your tier grows: on the Pack too - the key there becomes the new one)
    KUP = {2: 'silver_key', 3: 'gold_key', 4: 'rat_king_key'}
    for name in ('loop/second', 'loop/fast'):
        L = F[name]
        for i, l in enumerate(L):
            m = re.search(r'if entity @s\[tag=bm\.rqt_(\w+)\] .* run function bm:p28/key/to_(\d)$', l)
            if not m: continue
            src, nn = m.group(1), int(m.group(2))
            dst = KUP[nn]
            L[i] = l[:l.rindex('run function ')] + f'run function bm:p277/kup/{src}_{nn}'
            if f'p277/kup/{src}_{nn}' in F: continue
            fn(f'p277/kup/{src}_{nn}', [pid, f'data modify storage bm:rp t.k set value "{BY[src]["path"][1:]}"', 'function bm:p277/s/rm with storage bm:rp t',
                                        f'scoreboard players set @s {BY[src]["obj"]} 0',
                                        f'execute unless score @s {BY[dst]["obj"]} matches 1.. run function bm:p277/kup/put_{dst} with storage bm:rp t',
                                        f'scoreboard players set @s {BY[dst]["obj"]} 1', 'function bm:p277/tg',
                                        'playsound minecraft:block.bell.use player @s ~ ~ ~ 1 1.3',
                                        title('@s', 'actionbar', T(f'The key on your Rat Pack turns... it is now the {ITEMS[dst]["name"]}.', 'aqua'))])
            fn(f'p277/kup/put_{dst}', [f'$data modify storage bm:pw p$(pid).{BY[dst]["path"]} set value {snbt(G.stack(dst))}'])
    rep['items counted as carried'] = len(patched)
    rep['checks patched'] = sum(len(v) for v in patched.values())
    G.RQ_PATCHED = patched                        # (for the report)

    # ================================================================== STORAGE HELPERS (macro: pid, k = the entry's path)
    fn('p277/s/put', ['$data modify storage bm:pw p$(pid).r$(k) set from entity @s equipment.offhand', 'item replace entity @s weapon.offhand with minecraft:air',
                      '$data remove storage bm:pw p$(pid).r$(k).components."minecraft:custom_data".bm_rpno'])
    fn('p277/s/cnt', ['$execute unless data storage bm:pw p$(pid).r$(k) run return 0',
                      '$execute unless data storage bm:pw p$(pid).r$(k).count run return 1',
                      '$return run data get storage bm:pw p$(pid).r$(k).count'])
    fn('p277/s/rm', ['$data remove storage bm:pw p$(pid).r$(k)'])
    fn('p277/s/setc', ['$execute store result storage bm:pw p$(pid).r$(k).count int 1 run scoreboard players get #rqt bm.rng'])
    fn('p277/s/dec', ['$execute store result score #rqt bm.rng run function bm:p277/s/cnt {pid:$(pid),k:"$(k)"}', 'scoreboard players remove #rqt bm.rng 1',
                      '$execute if score #rqt bm.rng matches ..0 run return run data remove storage bm:pw p$(pid).r$(k)',
                      '$execute store result storage bm:pw p$(pid).r$(k).count int 1 run scoreboard players get #rqt bm.rng'])
    fn('p277/s/givehb', ['$execute unless data storage bm:pw p$(pid).hb run return 0',
                         'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                         '$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).hb', 'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item.components."minecraft:custom_data".bm_rpno set value 1b',
                         'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', '$data remove storage bm:pw p$(pid).hb', 'return 1'])
    fn('p277/s/give', ['$execute unless data storage bm:pw p$(pid).r$(k) run return 0',
                       'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                       '$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).r$(k)',
                       'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item.components."minecraft:custom_data".bm_rpno set value 1b',
                       'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                       'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', '$data remove storage bm:pw p$(pid).r$(k)', 'return 1'])
    # (the main-hand swap: the Pack's item into your hand for its use, then back - your own item restored)
    fn('p277/sw/in', ['$data remove storage bm:pw p$(pid).rqmh', '$data modify storage bm:pw p$(pid).rqmh set from entity @s SelectedItem',
                      'summon minecraft:item_display ~ ~ ~ {Tags:["bm.rqh"]}',
                      '$data modify entity @e[type=minecraft:item_display,tag=bm.rqh,limit=1,distance=..1] item set from storage bm:pw p$(pid).r$(k)',
                      'item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=bm.rqh,limit=1,distance=..1] contents',
                      'kill @e[type=minecraft:item_display,tag=bm.rqh,distance=..1]'])
    fn('p277/sw/out', ['$data remove storage bm:pw p$(pid).r$(k)',
                       '$execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"$(id)"}] run data modify storage bm:pw p$(pid).r$(k) set from entity @s SelectedItem',
                       '$data remove storage bm:pw p$(pid).r$(k).Slot',
                       '$execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"$(id)"}] if items entity @s weapon.mainhand * run function bm:p277/sw/spill',
                       '$execute unless data storage bm:pw p$(pid).rqmh run return run item replace entity @s weapon.mainhand with minecraft:air',
                       'summon minecraft:item_display ~ ~ ~ {Tags:["bm.rqh"]}',
                       '$data modify entity @e[type=minecraft:item_display,tag=bm.rqh,limit=1,distance=..1] item set from storage bm:pw p$(pid).rqmh',
                       'item replace entity @s weapon.mainhand from entity @e[type=minecraft:item_display,tag=bm.rqh,limit=1,distance=..1] contents',
                       'kill @e[type=minecraft:item_display,tag=bm.rqh,distance=..1]', '$data remove storage bm:pw p$(pid).rqmh'])
    # (whatever the use left in your hand that isn't the Pack's item - yours, at your feet)
    fn('p277/sw/spill', ['summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                         'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from entity @s SelectedItem',
                         'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout'])

    # ================================================================== PER ENTRY: on, use, take back, its row
    page_fn = {c: f'p277/pg/{c}' for c in CATS}
    page_fn['mounts'] = 'p249/m/open'
    for e in E:
        n, iid, O, P_, T_, nm, col = e['n'], e['iid'], e['obj'], e['path'], e['tag'], e['name'], e['col']
        setk = [pid, f'data modify storage bm:rp t.k set value "{P_[1:]}"', f'data modify storage bm:rp t.id set value "{iid}"']
        where = PAGE_OF[e['cat']]
        # put on (from the off hand: the Pack's use)
        if iid != 'bm_handbook':
            told = tellraw('@s', PRE + [T(nm, col, bold=True), T(f' goes on your Rat Pack ({where} page). ', 'gray'), T('(Use the Pack to take it out again.)', 'dark_gray')])
            if e['stack'] == 1:
                a = [f'execute if score @s {O} matches 1.. run return run ' + say([T(nm, col), T(' is on your Rat Pack already.', 'gray')])] + setk + \
                    ['function bm:p277/s/put with storage bm:rp t', f'scoreboard players set @s {O} 1']
            else:
                M = e['stack']
                a = setk + ['scoreboard players set #rqo bm.rng 1', 'execute store result score #rqo bm.rng run data get entity @s equipment.offhand.count',
                            f'execute store result score #rqt bm.rng run function bm:p277/s/cnt with storage bm:rp t',
                            f'execute if score #rqt bm.rng matches {M}.. run return run ' + say([T(nm, col), T(f' - your Rat Pack holds {M}, and it\'s full.', 'gray')]),
                            f'execute if score #rqt bm.rng matches 0 run return run function bm:p277/a/new_{iid}',
                            'scoreboard players operation #rqt bm.rng += #rqo bm.rng',
                            f'scoreboard players set #rqm bm.rng {M}', 'scoreboard players operation #rqr bm.rng = #rqt bm.rng',
                            'scoreboard players operation #rqr bm.rng -= #rqm bm.rng', 'scoreboard players operation #rqt bm.rng < #rqm bm.rng',
                            'function bm:p277/s/setc with storage bm:rp t',
                            'execute if score #rqr bm.rng matches ..0 run item replace entity @s weapon.offhand with minecraft:air',
                            'execute if score #rqr bm.rng matches 1.. store result storage bm:rp t.r int 1 run scoreboard players get #rqr bm.rng',
                            'execute if score #rqr bm.rng matches 1.. run function bm:p277/a/rest with storage bm:rp t',
                            f'scoreboard players operation @s {O} = #rqt bm.rng']
                fn(f'p277/a/new_{iid}', ['function bm:p277/s/put with storage bm:rp t', f'scoreboard players operation @s {O} = #rqo bm.rng',
                                         'function bm:p277/tg', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6', told])
            if iid == 'fixers_ledger':
                a.insert(0, f'execute if items entity @s weapon.offhand {HL} run return run ' + say('The Heist Ledger stays with you in the vault - it can\'t go on the Pack.'))
            if e['kind'] == 'worn': a.append(f'function bm:p277/c/aw_{iid}')
            fn(f'p277/a/{iid}', a + ['function bm:p277/tg', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6',
                                     'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20', told])
        # take back (once: the stored item, or nothing)
        if iid == 'bm_handbook':
            o = ['execute unless score @s bm.pwhb matches 1 run return run function bm:p28/stale', 'function bm:p179/w/pid',
                 pid, 'execute store result score #rqg bm.rng run function bm:p277/s/givehb with storage bm:rp t',
                 f'execute if score #rqg bm.rng matches 0 run {give("bm_handbook")}', 'scoreboard players set @s bm.pwhb 0', 'tag @s remove bm.pw_hb']
        else:
            o = [f'execute unless score @s {O} matches 1.. run return run function bm:p28/stale'] + setk + \
                ['function bm:p277/s/give with storage bm:rp t', f'scoreboard players set @s {O} 0', f'tag @s remove {T_}']
            if e['kind'] == 'worn': o += [f'tag @s remove bm.rqw_{iid}']
        fn(f'p277/o/{iid}', o + ['playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
                                 tellraw('@s', PRE + [T(nm, col, bold=True), T(' comes off your Rat Pack.', 'gray')]), 'function bm:p277/tg', f'function bm:{page_fn[e["cat"]]}'])
        # use: as using the item
        if e['how'] == 'hold':
            fn(f'p277/u/{iid}', ['dialog clear @s'] + setk + ['execute at @s run function bm:p277/sw/in with storage bm:rp t', f'execute at @s run function {e["use"]}',
                                 pid, f'data modify storage bm:rp t.k set value "{P_[1:]}"', f'data modify storage bm:rp t.id set value "{iid}"',
                                 'execute at @s run function bm:p277/sw/out with storage bm:rp t',
                                 f'execute store result score @s {O} run function bm:p277/s/cnt with storage bm:rp t', 'function bm:p277/tg'])
        elif e['how'] == 'eat':                    # (a consumable: one is used up first - as eating it - then its use; a seal that holds gives it back)
            fn(f'p277/u/{iid}', ['dialog clear @s'] + setk + ['function bm:p277/s/dec with storage bm:rp t',
                                 f'execute store result score @s {O} run function bm:p277/s/cnt with storage bm:rp t', 'function bm:p277/tg',
                                 f'execute at @s run function {e["use"]}'])
        elif e['how'] == 'fn':
            fn(f'p277/u/{iid}', ['dialog clear @s', f'function {e["use"]}'])
        # the charms' switch
        if e['kind'] == 'carry':
            fn(f'p277/c/{iid}', [click, f'execute if score @s bm.rqo_{iid} matches 1 run scoreboard players set @s bm.rqo_{iid} 2',
                                 f'execute unless score @s bm.rqo_{iid} matches 2 run scoreboard players set @s bm.rqo_{iid} 1',
                                 f'execute if score @s bm.rqo_{iid} matches 2 run scoreboard players reset @s bm.rqo_{iid}',
                                 f'execute unless score @s bm.rqo_{iid} matches 1 run ' + say([T(nm, col), T(': active', 'green')]),
                                 f'execute if score @s bm.rqo_{iid} matches 1 run ' + say([T(nm, col), T(': resting', 'red')]),
                                 'function bm:p277/tg', 'function bm:p277/pg/charms'])
        elif e['kind'] == 'worn':
            fn(f'p277/c/{iid}', [click, f'execute if entity @s[tag=bm.rqw_{iid}] run return run function bm:p277/c/unwear_{iid}'] +
               [f'tag @s remove bm.rqw_{j}' for j in WORN_CHARMS] + [f'tag @s add bm.rqw_{iid}', say([T(nm, col), T(': worn', 'green'), T(' (the one off-hand charm the Pack wears)', 'gray')]),
                                                                    'function bm:p277/tg', 'function bm:p277/pg/charms'])
            fn(f'p277/c/aw_{iid}', [f'execute if entity @s[tag=bm.rqw_{j}] run return 0' for j in WORN_CHARMS] + [f'tag @s add bm.rqw_{iid}'])
            fn(f'p277/c/unwear_{iid}', [f'tag @s remove bm.rqw_{iid}', say([T(nm, col), T(': resting', 'red')]), 'function bm:p277/tg', 'function bm:p277/pg/charms'])
        # its button: by the page's switch (Use / Take back); the Keyring only takes back; a charm's use is its switch
        h = [f'execute unless score @s {O} matches 1.. run return run function bm:p28/stale']
        if e['cat'] == 'keys': h.append(f'return run function bm:p277/o/{iid}')
        else:
            h.append(f'execute if entity @s[tag=bm.rqtb] run return run function bm:p277/o/{iid}')
            if e['cat'] == 'charms' and e['kind'] in ('carry', 'worn'): h.append(f'function bm:p277/c/{iid}')
            elif e['use']: h.append(f'function bm:p277/u/{iid}')
            else: h.append(say([T(nm, col), T(' works by being carried - nothing to press. (Switch the page to Take back to take it out.)', 'gray')]))
        fn(f'p277/e/{iid}', h)
        # its row on the page
        cnt = (lambda: [T(' ×$(c)', 'gray')]) if e['stack'] > 1 else (lambda: [])
        lab = lambda pre: [icon(iid, col), T(pre, 'white'), T(nm, col)] + cnt()
        code = B_E0 + n
        verb = {'pocket': 'Use it - as using the item', 'maps': 'Open it - the seal breaks (one is used up)',
                'mounts': 'Call it - as using the item'}.get(e['cat'], '')
        b_take = P28.btn(lab(' ↩ '), code, width=150, tooltip=T(f'Take {nm} back off the Pack (at your feet)', 'gray'))
        rows = []
        if e['cat'] == 'keys':
            rows.append(f'data modify storage bm:tmp rq.acts append value {snbt(P28.btn(lab(" "), code, width=150, tooltip=T(f"On your Rat Pack: it counts as carried. Press: take {nm} back out", "gray")))}')
        elif e['cat'] == 'charms':
            act_t = 'worn' if e['kind'] == 'worn' else 'active'
            b_on = P28.btn([T('● ', 'green')] + lab(' ')[0:1] + [T(' ' + nm, col)], code, width=150, tooltip=T(f'{nm}: {act_t}. Press: rest it', 'gray'))
            b_off = P28.btn([T('○ ', 'dark_gray')] + lab(' ')[0:1] + [T(' ' + nm, 'gray')], code, width=150,
                            tooltip=T(f'{nm}: resting. Press: ' + ('wear it (the one off-hand charm the Pack wears)' if e['kind'] == 'worn' else 'make it active'), 'gray'))
            rows += [f'execute if entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(b_take)}',
                     f'execute unless entity @s[tag=bm.rqtb] if entity @s[tag={T_}] run data modify storage bm:tmp rq.acts append value {snbt(b_on)}',
                     f'execute unless entity @s[tag=bm.rqtb] unless entity @s[tag={T_}] run data modify storage bm:tmp rq.acts append value {snbt(b_off)}']
        else:
            b_use = P28.btn(lab(' '), code, width=150, tooltip=T(f'{nm}: ' + (verb if e['use'] else 'it works by being carried'), 'gray'))
            rows += [f'execute if entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(b_take)}',
                     f'execute unless entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(b_use)}']
        rows = [('$' + r) if '$(' in r else r for r in rows]
        fn(f'p277/r/{iid}', rows)
    # (an off-hand stack bigger than what fits: the rest stays in your off hand)
    fn('p277/a/rest', ['$item modify entity @s weapon.offhand {function:"minecraft:set_count",count:$(r)}'])

    # ================================================================== PUT ON: the Pack's use with one of them in the off hand
    use = F['p179/w/use']
    k = use.index('execute if predicate bm:p20/sneaking run return run function bm:p179/w/recall')
    anyq = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{e["iid"]}"}}' for e in E if e['iid'] != 'bm_handbook') + '|' + \
           '|'.join(f'minecraft:custom_data~{{bm:"{b[1]}"}}' for b in BAGK) + ']'
    use[k:k] = [f'execute if items entity @s weapon.offhand {anyq} run return run function bm:p277/add']
    fn('p277/add', [f'execute if items entity @s weapon.offhand {holds(e["iid"])} run return run function bm:p277/a/{e["iid"]}' for e in E if e['iid'] != 'bm_handbook'] +
       [f'execute if items entity @s weapon.offhand {holds(b[1])} run return run function bm:p277/b/add_{b[0]}' for b in BAGK])
    use[-1] = 'function bm:p277/open' if use[-1] == 'function bm:p179/w/open' else use[-1]
    assert use[-1] == 'function bm:p277/open', use[-1]

    # ================================================================== THE PAGES
    # (a pager over bm:tmp rq.acts: phase261's cutter, 8 a page; its arrows and the page number)
    PER = 8
    for c in list(CATS) + ['bags', 'cols']:
        fn(f'p277/pgr/{c}', [f'scoreboard players operation #pgp bm.rng = @s bm.pg_rp{c}', f'scoreboard players set #pgN bm.rng {PER}',
                             'data modify storage bm:ui pg.src set from storage bm:tmp rq.acts', 'function bm:p261/pg/run',
                             f'scoreboard players operation @s bm.pg_rp{c} = #pgp bm.rng', 'data modify storage bm:tmp rq.acts set from storage bm:ui pg.out',
                             'execute if score #pgn bm.rng matches 2.. run function bm:p277/nav with storage bm:ui pg'])
    dim = lambda txt, code: P28.btn([T(txt, 'dark_gray')], code, width=150, tooltip=T('(no more this way)', 'dark_gray'))     # (3.0y: with its code: the pager holds you on the end page - an action-less button closes the dialog)
    fn('p277/nav', ['execute if score #pgp bm.rng matches 1.. run data modify storage bm:tmp rq.acts append value ' +
                    snbt(P28.btn([T('‹ Previous', 'white')], B_PREV, width=150, tooltip=T('The page before.', 'gray'))),
                    'execute if score #pgp bm.rng matches ..0 run data modify storage bm:tmp rq.acts append value ' + snbt(dim('‹ Previous', B_PREV)),
                    '$execute if score #pgp bm.rng < #pgl bm.rng run data modify storage bm:tmp rq.acts append value ' +
                    snbt(P28.btn([T('Next ›', 'white'), T('  $(p)/$(n)', 'gray')], B_NEXT, width=150, tooltip=T('The next page.', 'gray'))),
                    '$execute if score #pgp bm.rng >= #pgl bm.rng run data modify storage bm:tmp rq.acts append value ' +
                    snbt(P28.btn([T('Next ›', 'dark_gray'), T('  $(p)/$(n)', 'dark_gray')], B_NEXT, width=150, tooltip=T('(no more this way)', 'dark_gray')))])
    mode_use = P28.btn([T('Press to: ', 'gray'), T('Use', 'white', bold=True)], B_MODE, width=150,
                       tooltip=T('Pressing a row uses it. Press here: pressing a row takes it back off the Pack instead.', 'gray'))
    mode_take = P28.btn([T('Press to: ', 'gray'), T('Take back', '#ffb070', bold=True)], B_MODE, width=150,
                        tooltip=T('Pressing a row takes it back off the Pack. Press here: pressing a row uses it again.', 'gray'))
    TIPS = {'pocket': ('Your everyday tools, each as if carried. Press one: as using it.', 'Hold a tool in your off hand - the Handbook, the Fixer\'s Ledger, the Particle Toggler, a Waytoken, a Crew Flare, a compass... - and use the Rat Pack: it goes on this page.'),
            'keys': ('Every key on the ring counts as carried while the Pack is with you. Press one: it comes back off.', 'Hold a key in your off hand - the market keys, a dungeon\'s, a vault\'s, a victor\'s - and use the Rat Pack: it goes on the ring.'),
            'charms': ('● active / ○ resting - press one to switch it. The off-hand charms are worn one at a time.', 'Hold a charm in your off hand and use the Rat Pack: it goes in the pouch, active.'),
            'maps': ('Sealed maps, kept flat. Press one to break its seal - as opening it.', 'Hold a sealed map in your off hand and use the Rat Pack: it goes in the case.'),
            'mounts': ('Your mounts\' calls. Press one: as using it.', 'Hold a mount\'s call - a Vorn Skiff or Mothership Key, the Mecha Rex Remote, a rat\'s call - in your off hand and use the Rat Pack: it goes on this page.')}
    for c, L in CATS.items():
        sym, title_, scol = SEC[c]
        menu = M_CAT[c]
        tip, how = TIPS[c]
        build = [f'scoreboard players set @s bm.menu {menu}', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                 'data modify storage bm:tmp rq.acts set value []']
        if c == 'mounts':
            build += ['function bm:p277/mt/skiff']
        for iid in L:
            e = BY[iid]
            if e['stack'] > 1:
                build += [f'execute if score @s {e["obj"]} matches 1.. store result storage bm:rp rc.c int 1 run scoreboard players get @s {e["obj"]}',
                          f'execute if score @s {e["obj"]} matches 1.. run function bm:p277/r/{iid} with storage bm:rp rc']
            else:
                build.append(f'execute if score @s {e["obj"]} matches 1.. run function bm:p277/r/{iid}')
        empty = P28.multi(head(title_), [P28.body([T(f'Nothing on this page yet. ', 'white'), T(how, 'gray')], 300)], [back_btn], columns=2)
        build += [f'execute unless data storage bm:tmp rq.acts[0] run return run dialog show @s {snbt(empty)}', f'function bm:p277/pgr/{c}']
        if c != 'keys':
            build += [f'execute if entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(mode_take)}',
                      f'execute unless entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(mode_use)}']
        build += [f'data modify storage bm:tmp rq.acts append value {snbt(back_btn)}', f'function bm:p277/pg/{c}_show with storage bm:tmp rq', page_turn]
        full = P28.multi(head(title_), [P28.body([T(tip, 'gray')], 300)], '@@ACTS@@', columns=2)
        fn(f'p277/pg/{c}_show', ['$dialog show @s ' + snbt(full).replace('"@@ACTS@@"', '$(acts)')])
        if c == 'mounts':
            M_ = F['p249/m/open']
            M_[:] = ['dialog clear @s'] + build          # (phase249's Mounts page, now the Rat Pack's: the skiff's row and the calls)
        else:
            fn(f'p277/pg/{c}', build)
    # (the skiff's slot, phase249's: its own codes, by the page's switch)
    import phase249 as P249
    SKC = '#7dff6a'
    sk = ['scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #on bm.rxv 0',
          'execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if score @s bm.pid = #kp bm.pid run scoreboard players set #on bm.rxv 1']
    for nslot, (iid, nm) in ((1, ('skiff_key', 'Vorn Skiff')), (2, ('mothership_key', 'Mothership'))):
        b_call = P28.btn([icon(iid, SKC), T(f' Call your {nm}', 'white')], P249.C_SK, width=150, tooltip=T(f'Your {nm} comes to your side', 'gray'))
        b_home = P28.btn([icon(iid, SKC), T(f' Send it home', '#c8c8c8')], P249.C_SK, width=150, tooltip=T(f'Your {nm} goes home', 'gray'))
        b_out = P28.btn([icon(iid, SKC), T(' ↩ ', 'white'), T(ITEMS[iid]['name'], SKC)], P249.C_SKOUT, width=150, tooltip=T(f'{ITEMS[iid]["name"]} comes off the Pack', 'gray'))
        sk += [f'execute if score @s bm.pwsk matches {nslot} if entity @s[tag=bm.rqtb] run data modify storage bm:tmp rq.acts append value {snbt(b_out)}',
               f'execute if score @s bm.pwsk matches {nslot} unless entity @s[tag=bm.rqtb] if score #on bm.rxv matches 0 run data modify storage bm:tmp rq.acts append value {snbt(b_call)}',
               f'execute if score @s bm.pwsk matches {nslot} unless entity @s[tag=bm.rqtb] if score #on bm.rxv matches 1 run data modify storage bm:tmp rq.acts append value {snbt(b_home)}']
    fn('p277/mt/skiff', sk)
    # (the old "Mounts" button on the wheel, and its back to the wheel: the Rat Pack's front page has Mounts ›)
    so = F['p249/w/sk_out']; so.append('function bm:p249/m/open')
    pa = F['p249/act']
    pa[:] = [l.replace('run function bm:p179/w/open', 'run function bm:p277/open') for l in pa]

    # ---------------------------------------------------------------- the front page
    PW_N = len(F['admin/follower_items'])
    cnt = ['scoreboard players set #rqf bm.rng 0'] + [f'execute if score @s bm.pw{i} matches 1 run scoreboard players add #rqf bm.rng 1' for i in range(PW_N)] + \
          ['execute if score @s bm.pwesc matches 0.. run scoreboard players add #rqf bm.rng 1',
           'execute store result storage bm:tmp rqf.partners int 1 run scoreboard players get #rqf bm.rng']
    for c, L in CATS.items():
        cnt += ['scoreboard players set #rqf bm.rng 0'] + [f'execute if score @s {BY[i]["obj"]} matches 1.. run scoreboard players add #rqf bm.rng 1' for i in L]
        if c == 'mounts': cnt.append('execute if score @s bm.pwsk matches 1.. run scoreboard players add #rqf bm.rng 1')
        cnt.append(f'execute store result storage bm:tmp rqf.{c} int 1 run scoreboard players get #rqf bm.rng')
    for pg in ('bags', 'cols'):
        cnt += ['scoreboard players set #rqf bm.rng 0'] + [f'scoreboard players operation #rqf bm.rng += @s bm.rb_{b[0]}' for b in BAGK if b[2] == pg] + \
               [f'execute store result storage bm:tmp rqf.{pg} int 1 run scoreboard players get #rqf bm.rng']
    sec_btn = lambda key, sym, word, col, tip: P28.btn([T(sym + ' ', col), T(word, 'white'), T(' ›', 'gray'), T(f'  $({key})', 'dark_gray')], B_SEC[key], width=150, tooltip=T(tip, 'gray'))
    fbtns = [sec_btn('partners', '❖', 'Partners', PURPLE, 'Your partners: call them, send them home, their menus - the old wheel'),
             sec_btn('pocket', '✦', 'Pocket', '#e8c070', 'Your everyday tools: the Handbook, the Ledger, the toggler, tokens, flares, compasses'),
             sec_btn('keys', '⚿', 'Keyring', '#ffd700', 'Every key you\'ve put on - each counts as carried'),
             sec_btn('charms', '✿', 'Charms', '#ff9ad8', 'Your charms, and which of them are active'),
             sec_btn('maps', '⚑', 'Maps', '#7ad8ff', 'Your sealed maps - break a seal from here'),
             sec_btn('mounts', '◈', 'Mounts', '#7ad8ff', 'Your skiff\'s key and your mounts\' calls'),
             sec_btn('bags', '▣', 'Bags', '#c08a52', 'Up to ten Backpacks and ten Vacuum Satchels, each with its own load'),
             sec_btn('cols', '⚒', 'Collectors', '#9ae8c8', 'Spirit Jars, Ore Magnets and Prime Coolers - they keep collecting from here'),
             P28.btn([T('⚙ ', '#e8c070'), T('Settings', 'white'), T(' ›', 'gray')], B_SEC['settings'], width=150, tooltip=T('Auto-pack: what goes on the Pack by itself. And your own settings.', 'gray'))]
    b_hb = P28.btn([icon('bm_handbook', '#e8c070'), T(' Handbook', '#e8c070')], B_SEC['handbook'], width=150, tooltip=T('Open your Black Market Handbook (it\'s in the Pocket)', 'gray'))
    b_gd = P28.btn([T('✦ ', '#e8c070'), T('Guide', 'white'), T(' ›', 'gray')], B_SEC['guide'], width=150, tooltip=T('Your guide: on or off, and how it looks', 'gray'))
    front = P28.multi(head('everything you carry, in one pack'),
                      [P28.body([T('Hold something in your off hand and use the Pack: it goes on. ', 'gray'),
                                 T('Carry the Pack: all it holds counts as carried.', 'white')], 300)], '@@ACTS@@', columns=2)
    fn('p277/front_show', ['$dialog show @s ' + P28.inline(front).replace('"@@ACTS@@"', '$(acts)')])
    fbuild = [f'data modify storage bm:tmp rqf.acts set value []'] + \
             [('$' if '$(' in snbt(b) else '') + f'data modify storage bm:tmp rqf.acts append value {snbt(b)}' for b in fbtns] + \
             [f'execute if score @s bm.pwhb matches 1 run data modify storage bm:tmp rqf.acts append value {snbt(b_hb)}',
              f'data modify storage bm:tmp rqf.acts append value {snbt(b_gd)}']
    fn('p277/front_acts', fbuild)
    fn('p277/open', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'scoreboard players set @s bm.menu {M_FRONT}',
                     'tag @s remove bm.rqtb'] + cnt + ['function bm:p277/front_acts with storage bm:tmp rqf', 'function bm:p277/front_show with storage bm:tmp rqf',
                                                         'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.4'])

    for i in range(len(F['admin/follower_items'])):
        L_ = F[f'p179/w/outm{i}']
        k_ = next(j for j, l in enumerate(L_) if 'Item set from storage bm:pw p$(pid).k' in l)
        L_.insert(k_ + 1, 'data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Item.components."minecraft:custom_data".bm_rpno set value 1b')
    # ---------------------------------------------------------------- the Partners page: the old wheel, tidied (its sections went to the front)
    op = F['p179/w/open']
    gone = lambda l: any(f'/trigger bm.act set {c}"' in l for c in (7007, 7008, 7009, 5668)) or 'p249/m/wbtn' in l or l == 'tag @s remove bm.rxmb'
    n0 = len(op)
    op[:] = [l for l in op if not gone(l)]
    rep['partner rows moved to the front'] = n0 - len(op)
    k = op.index('function bm:p179/w/show with storage bm:tmp pw')
    op.insert(k, f'data modify storage bm:tmp pw.acts append value {snbt(P28.btn([T("« Rat Pack", "gray")], B_BACK, width=150, tooltip=T("Back to the Rat Pack\'s front page", "gray")))}')
    emp = next(i for i, l in enumerate(op) if l.startswith('execute unless data storage bm:tmp pw.acts[0] run return run dialog show @s'))
    gal = P28.btn([T('❖ ', PURPLE), T('Gallery', 'white')], 3352, width=150, tooltip=T('Every follower in the pack - who you\'ve met, and who\'s still out there.', 'gray'))
    op[emp] = 'execute unless data storage bm:tmp pw.acts[0] run return run dialog show @s ' + snbt(P28.multi(head('Partners'),
              [P28.body([T('No partners on your Rat Pack yet. ', 'white'),
                         T('Hold a partner\'s summoning item in your off hand and use the Pack: they go on, and come when you call.', 'gray')], 300)],
              [gal, P28.btn([T('« Rat Pack', 'gray')], B_BACK, width=150)], columns=2))
    sh = F['p179/w/show']
    s0 = sh[0]
    m = re.search(r'title:\[\{text:"Partner Wheel"[^\]]*\]', s0)
    assert m, s0[:200]
    sh[0] = s0.replace(m.group(0), 'title:' + snbt(head('Partners')), 1)
    # (its pages, the Teams page and the gallery keep their own way back to it; Your settings and the Handbook's take-back come home to the front / the Pocket)
    F['p260/ps/back'] = [l.replace('run function bm:p179/w/open', 'run function bm:p277/open') for l in F['p260/ps/back']]
    hbo = F['p276/hb_out']
    hbo[:] = [('function bm:p277/pg/pocket' if l == 'function bm:p179/w/open' else l) for l in hbo]
    for nm_ in ('p249/m/wbtn', 'p249/m/any', 'p249/m/show', 'p249/m/row_sk', 'p249/m/row_rx'):    # (the wheel's old "Mounts" button and page: the front page has Mounts ›)
        if nm_ not in F: continue
        txt = '\n'.join('\n'.join(v) for k_, v in F.items() if k_ != nm_)
        if f'bm:{nm_}' not in txt: del F[nm_]

    # ---------------------------------------------------------------- ⚙ Settings: auto-pack, and your own settings
    st = ['data remove storage bm:ui rqs']
    for key, lbl, dflt in AP:
        st += [f'data modify storage bm:ui rqs.r_{key} set value {snbt(on_txt if dflt else off_txt)}',
               f'execute if score @s bm.rqap_{key} matches 1 run data modify storage bm:ui rqs.r_{key} set value {snbt(on_txt)}',
               f'execute if score @s bm.rqap_{key} matches 2 run data modify storage bm:ui rqs.r_{key} set value {snbt(off_txt)}']
    sd = P28.multi(head('settings'), [P28.body([T('Auto-pack: once a second, a thing of a kind switched on that\'s in your own inventory goes on the Pack, '
                                                  'and chat says so. Never your off hand, a chest or a bundle; never in a heist.', 'gray')], 300)],
                   [P28.btn([T(f'{lbl}: ', 'gray'), f'@@RAW:r_{key}@@'], B_AP0 + i, width=150,
                            tooltip=T(f'Auto-pack {lbl.lower()}: found in your inventory, they go on the Pack by themselves ({PAGE_OF[key]} page).', 'gray'))
                    for i, (key, lbl, dflt) in enumerate(AP)] +
                   [P28.btn([T('⚙ ', '#e8c070'), T('Your settings', 'white')], B_YOURS, width=150, tooltip=T('Music, chatter, screen shake, keep up, particles - yours alone.', 'gray')),
                    P28.btn([T('« Rat Pack', 'gray')], B_BACK, width=150, tooltip=T('Back to the Rat Pack\'s front page', 'gray'))], columns=2)
    fn('p277/set_dlg', [f'$dialog show @s {P28.inline(sd)}'])
    fn('p277/settings', st + [f'scoreboard players set @s bm.menu {M_SET}', 'function bm:p277/set_dlg with storage bm:ui rqs'])
    for i, (key, lbl, dflt) in enumerate(AP):
        v_on, v_off = 1, 2
        fn(f'p277/ap/tog_{key}', [click] + (
            [f'execute unless score @s bm.rqap_{key} matches 2 run return run function bm:p277/ap/set_{key} {{v:2}}', f'function bm:p277/ap/set_{key} {{v:1}}'] if dflt else
            [f'execute if score @s bm.rqap_{key} matches 1 run return run function bm:p277/ap/set_{key} {{v:2}}', f'function bm:p277/ap/set_{key} {{v:1}}']))
        fn(f'p277/ap/set_{key}', [f'$scoreboard players set @s bm.rqap_{key} $(v)',
                                  f'execute if score @s bm.rqap_{key} matches 1 run ' + say([T(f'Auto-pack {lbl.lower()}: ', PURPLE), T('on', 'green')]),
                                  f'execute if score @s bm.rqap_{key} matches 2 run ' + say([T(f'Auto-pack {lbl.lower()}: ', PURPLE), T('off', 'red')]),
                                  'function bm:p277/settings'])

    # ================================================================== BAGS AND COLLECTORS (up to ten of each, each its own load)
    BAG = P248.BAG
    rb = lambda k, j=None: f'bm:pw p$(pid).rb_{k}' + (f'[{j}]' if j is not None else '')
    for ki, (k, iid, pg, nm, bxkind, coll, sw) in enumerate(BAGK):
        col = colour(iid)
        told = tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(f' goes on your Rat Pack ({PAGE_OF[pg]} page). ', 'gray'), T('(Its load goes with it.)', 'dark_gray')])
        full = say([T(f'Your Rat Pack holds {BAGMAX} {nm}s', col), T(f' - the {BAGMAX + 1}th stays with you.', 'gray')])
        fn(f'p277/b/add_{k}', [f'execute if score @s bm.rb_{k} matches {BAGMAX}.. run return run ' + full, pid,
                               f'function bm:p277/b/put_{k} with storage bm:rp t', 'item replace entity @s weapon.offhand with minecraft:air',
                               f'scoreboard players add @s bm.rb_{k} 1', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6',
                               'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20', told])
        fn(f'p277/b/put_{k}', [f'$data modify storage {rb(k)} append value {{it:{{}}}}', f'$data modify storage {rb(k)}[-1].it set from entity @s equipment.offhand',
                               f'$data remove storage {rb(k)}[-1].it.components."minecraft:custom_data".bm_rpno'])
        # its row on the list: the icon, its number, its fill, its first two stacks
        for j in range(BAGMAX):
            lab = [icon(iid, col), T(f' {nm} {j + 1}', col), T('  $(f)/27', 'gray')]
            b_row = P28.btn(lab + ['@@RAW:r_t@@'], B_ROW0 + ki * 10 + j, width=300, tooltip=T(f'{nm} {j + 1}: look inside - unfold it, take it back' +
                                                                                              ({'vac': ', its vacuum', 'rpoff': ', auto-collect, deposit, withdraw', 'coff': ', auto-collect, cuts to Tokens, deposit, withdraw'}.get(sw, '')), 'gray'))
            fn(f'p277/b/row_{k}{j}', [f'$execute unless data storage {rb(k, j)} run return 0',
                                     'data modify storage bm:rp row set value {c:[],r_t:[{text:"",color:"gray",italic:false}]}',
                                     f'$data modify storage bm:rp row.c set from storage {rb(k, j)}.it.components."minecraft:container"',
                                     'execute store result storage bm:rp row.f int 1 run data get storage bm:rp row.c',
                                     'execute if data storage bm:rp row.c[0] run data modify storage bm:rp nm.it set from storage bm:rp row.c[0].item',
                                     'execute if data storage bm:rp row.c[0] run data modify storage bm:rp row.r_t append value {text:"  ",color:"gray",italic:false}',
                                     'execute if data storage bm:rp row.c[0] run function bm:p277/b/nm',
                                     'execute if data storage bm:rp row.c[1] run data modify storage bm:rp row.r_t append value {text:", ",color:"gray",italic:false}',
                                     'execute if data storage bm:rp row.c[1] run data modify storage bm:rp nm.it set from storage bm:rp row.c[1].item',
                                     'execute if data storage bm:rp row.c[1] run function bm:p277/b/nm',
                                     'execute if data storage bm:rp row.c[2] run data modify storage bm:rp row.r_t append value {text:"…",color:"gray",italic:false}',
                                     f'$execute if data storage {rb(k, j)}.out run data modify storage bm:rp row.r_t append value {{text:"  (unfolded)",color:"#ffb070",italic:false}}',
                                     f'function bm:p277/b/rowb_{k}{j} with storage bm:rp row'])
            fn(f'p277/b/rowb_{k}{j}', [f'$data modify storage bm:tmp rq.acts append value {P28.inline(b_row)}'])
        # (unfold: as using the item - into your hand, phase33's box; it folds back onto the Pack)
        fn(f'p277/b/unfold_{k}', [f'$execute if data storage {rb(k)}[$(j)].out run return run ' + say('It\'s unfolded already - sneak or walk away to fold it.'),
                                  f'$data modify storage bm:pw p$(pid).rbt set from storage {rb(k)}[$(j)].it',
                                  '$execute at @s run function bm:p277/sw/in {pid:$(pid),k:"bt"}',
                                  f'execute at @s run function bm:p33/box/open {{path:"SelectedItem",slot:"weapon.mainhand",name:"{nm}",kind:"{bxkind}"}}',
                                  '$execute if score #ok bm.rng matches 1 run function bm:p277/b/opened {pid:$(pid),k:"' + k + '",j:$(j),ki:' + str(ki) + '}',
                                  '$execute at @s run function bm:p277/sw/out {pid:$(pid),k:"bt",id:"' + iid + '"}',
                                  '$execute if data storage bm:pw p$(pid).rbt run data modify storage ' + rb(k) + '[$(j)].it set from storage bm:pw p$(pid).rbt',
                                  '$data remove storage bm:pw p$(pid).rbt'])
    fn('p277/b/opened', ['scoreboard players operation #kp bm.pid = @s bm.pid',
                         '$execute as @e[type=minecraft:marker,tag=bm.bxm] if score @s bm.pid = #kp bm.pid run function bm:p277/b/mark {ki:$(ki),j:$(j)}',
                         '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].out set value 1b',
                         '$data remove storage bm:pw p$(pid).rbt'])
    fn('p277/b/mark', ['tag @s add bm.rbbox', '$scoreboard players set @s bm.rbk $(ki)', '$scoreboard players set @s bm.rbj $(j)'])
    # (folding: phase33's box/back, as the marker - a Pack bag goes back into its place on the Pack, not to your hand)
    bk = F['p33/box/back']
    k_ = bk.index('execute as @a[tag=bm.cown,limit=1] at @s run function bm:p33/give_back')
    bk.insert(k_, 'execute if entity @s[tag=bm.rbbox] run return run function bm:p277/b/fold')
    fold = ['execute store result storage bm:rp f.pid int 1 run scoreboard players get @s bm.pid', 'execute store result storage bm:rp f.j int 1 run scoreboard players get @s bm.rbj']
    fold += [f'execute if score @s bm.rbk matches {ki} run data modify storage bm:rp f.k set value "{b[0]}"' for ki, b in enumerate(BAGK)]
    fold += ['function bm:p277/b/fold_m with storage bm:rp f', 'execute as @a[tag=bm.cown,limit=1] at @s run playsound minecraft:block.barrel.close player @s ~ ~ ~ 1 1',
             title('@a[tag=bm.cown,limit=1]', 'actionbar', T('Folded back onto your Rat Pack.', PURPLE))]
    fn('p277/b/fold', fold)
    fn('p277/b/fold_m', ['$execute unless data storage bm:pw p$(pid).rb_$(k)[$(j)] run return run execute as @a[tag=bm.cown,limit=1] at @s run function bm:p33/give_back',
                         '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it set from storage bm:tmp give', '$data remove storage bm:pw p$(pid).rb_$(k)[$(j)].out'])
    # (an item's name in a row: its own item_name / custom_name, else the game's name for its id - item or block)
    fn('p277/b/nm', ['execute if data storage bm:rp nm.it.components."minecraft:custom_name" run data modify storage bm:rp row.r_t append from storage bm:rp nm.it.components."minecraft:custom_name"',
                     'execute unless data storage bm:rp nm.it.components."minecraft:custom_name" if data storage bm:rp nm.it.components."minecraft:item_name" run data modify storage bm:rp row.r_t append from storage bm:rp nm.it.components."minecraft:item_name"',
                     'execute unless data storage bm:rp nm.it.components."minecraft:custom_name" unless data storage bm:rp nm.it.components."minecraft:item_name" run function bm:p277/b/nm_id',
                     'data modify storage bm:rp nm.c set value 1', 'execute if data storage bm:rp nm.it.count run data modify storage bm:rp nm.c set from storage bm:rp nm.it.count',
                     'function bm:p277/b/nm_c with storage bm:rp nm'])
    fn('p277/b/nm_id', ['data modify storage bm:rp nm.p set string storage bm:rp nm.it.id 10', 'function bm:p277/b/nm_t with storage bm:rp nm'])
    fn('p277/b/nm_t', ['$data modify storage bm:rp row.r_t append value [{translate:"item.minecraft.$(p)",fallback:"",color:"white",italic:false},{translate:"block.minecraft.$(p)",fallback:"",color:"white",italic:false}]'])
    fn('p277/b/nm_c', ['$data modify storage bm:rp row.r_t append value {text:" ×$(c)",color:"gray",italic:false}'])

    # ---------------------------------------------------------------- the two lists
    for pg, menu, word, sym, col0 in (('bags', M_BAGS, 'Bags', '▣', '#c08a52'), ('cols', M_COLS, 'Collectors', '⚒', '#9ae8c8')):
        ks = [(ki, b) for ki, b in enumerate(BAGK) if b[2] == pg]
        names = ' or '.join(f'{ITEMS[b[1]]["name"]}' for ki, b in ks)
        tip = ('Each with its own load. Press one: a look inside, Unfold, Take it back.' if pg == 'bags' else
               'They keep collecting from here, each with its own switch. Press one: a look inside, Deposit / Withdraw, Unfold, Take it back.')
        empty = P28.multi(head(word), [P28.body([T('Nothing on this page yet. ', 'white'),
                                                T(f'Hold a {names} in your off hand and use the Rat Pack: it goes on, its load and all (up to {BAGMAX} of each).', 'gray')], 300)], [back_btn], columns=1, button_width=300)
        L = [f'scoreboard players set @s bm.menu {menu}', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', pid, 'data modify storage bm:tmp rq.acts set value []']
        L += [f'function bm:p277/b/row_{b[0]}{j} with storage bm:rp t' for ki, b in ks for j in range(BAGMAX)]
        L += [f'execute unless data storage bm:tmp rq.acts[0] run return run dialog show @s {snbt(empty)}', f'function bm:p277/pgr/{pg}']
        if pg == 'cols':
            L.append('data modify storage bm:tmp rq.acts append value ' + snbt(P28.btn([T('⬇ ', '#9ae8c8'), T('Deposit all they take', 'white')], B_DEPALL, width=300,
                                                                                   tooltip=T('Everything in your inventory a collector of yours takes goes into it - the first with room first', 'gray'))))
        L += [f'data modify storage bm:tmp rq.acts append value {snbt(dict(back_btn, width=Int(300)))}', f'function bm:p277/b/{pg}_show with storage bm:tmp rq', page_turn]
        d = P28.multi(head(word), [P28.body([T(tip, 'gray')], 300)], '@@ACTS@@', columns=1, button_width=300)
        fn(f'p277/b/{pg}_show', ['$dialog show @s ' + snbt(d).replace('"@@ACTS@@"', '$(acts)')])
        fn(f'p277/b/{pg}', L)
    # (the pager's arrows are 150 wide; a one-column list keeps them in pairs anyway)

    # ---------------------------------------------------------------- a bag's own page: a look inside, and what it can do
    sel = ['execute store result storage bm:rp s.j int 1 run scoreboard players get @s bm.rbj', pid, 'data modify storage bm:rp s.pid set from storage bm:rp t.pid']
    sel += [f'execute if score @s bm.rbk matches {ki} run data modify storage bm:rp s.k set value "{b[0]}"' for ki, b in enumerate(BAGK)]
    fn('p277/b/sel', sel)
    item_body = {'type': 'minecraft:item', 'item': {'id': 'minecraft:stone', 'count': Int(1)}, 'show_decorations': B(1), 'show_tooltip': B(1), 'width': Int(16), 'height': Int(16)}
    for ki, (k, iid, pg, nm, bxkind, coll, sw) in enumerate(BAGK):
        col = colour(iid)
        bl = [f'scoreboard players set @s bm.menu {M_BAG}', 'function bm:p277/b/sel',
              f'$execute unless data storage {rb(k)}[$(j)] run return run function bm:p277/b/{pg}',
              'data modify storage bm:rp v set value {body:[],acts:[]}',
              f'$data modify storage bm:rp v.c set from storage {rb(k)}[$(j)].it.components."minecraft:container"',
              'execute store result storage bm:rp v.f int 1 run data get storage bm:rp v.c',
              f'$data modify storage bm:rp v.it set from storage {rb(k)}[$(j)].it',
              f'$execute if data storage {rb(k)}[$(j)].out run data modify storage bm:rp v.out set value 1b']
        fn(f'p277/b/page_{k}', bl)
        # (the head line, then one item body per stack - icons with their counts, a tooltip on hover)
        top = [T(f'{nm} ', col, bold=True), T('$(j1)', col, bold=True), T('  ·  $(f) of 27 slots', 'gray')]
        fn(f'p277/b/page2_{k}', [f'$data modify storage bm:rp v.body append value {snbt(P28.body(top, 300))}'] +
           [l for i in range(27) for l in (f'execute if data storage bm:rp v.c[{i}] run data modify storage bm:rp v.body append value {snbt(item_body)}',
                                           f'execute if data storage bm:rp v.c[{i}] run data modify storage bm:rp v.body[-1].item set from storage bm:rp v.c[{i}].item')] +
           ['execute unless data storage bm:rp v.c[0] run data modify storage bm:rp v.body append value ' + snbt(P28.body([T('(empty)', 'dark_gray')], 300)),
            'execute if data storage bm:rp v.out run data modify storage bm:rp v.body append value ' + snbt(P28.body([T('Unfolded in front of you now - sneak or walk away and it folds back onto the Pack.', '#ffb070')], 300))])
        acts = [('unfold', P28.btn([T('▣ ', col), T('Unfold', 'white')], B_UNFOLD, width=150, tooltip=T(f'It unfolds into a barrel in front of you, as using the {nm} does - and folds back onto the Pack', 'gray'))),
                ('take', P28.btn([T('↩ ', 'white'), T('Take it back', 'white')], B_TAKE, width=150, tooltip=T(f'The {nm} comes off the Pack, its load and all (at your feet)', 'gray')))]
        if sw == 'vac':
            acts += [('vac_on', P28.btn([T('Vacuum: ', 'gray'), on_txt], B_AUTO, width=150, tooltip=T('On: it pulls dropped items near you into itself from the Pack (on ones fill first-with-room-first). Press: off.', 'gray'))),
                     ('vac_off', P28.btn([T('Vacuum: ', 'gray'), off_txt], B_AUTO, width=150, tooltip=T('Off: it just stores. Press: on.', 'gray')))]
        elif sw in ('rpoff', 'coff'):
            acts += [('ac_on', P28.btn([T('Auto-collect: ', 'gray'), on_txt], B_AUTO, width=150, tooltip=T('On: it keeps collecting from the Pack, as carried. Press: off (its load is kept).', 'gray'))),
                     ('ac_off', P28.btn([T('Auto-collect: ', 'gray'), off_txt], B_AUTO, width=150, tooltip=T('Off: it stops pulling; its load is kept. Press: on.', 'gray')))]
        if sw == 'coff':
            acts += [('cv_on', P28.btn([T('Cuts → Tokens: ', 'gray'), on_txt], B_CONV, width=150, tooltip=T('Every two Prime cuts in it become a Token, each second. Press: off.', 'gray'))),
                     ('cv_off', P28.btn([T('Cuts → Tokens: ', 'gray'), off_txt], B_CONV, width=150, tooltip=T('Press: every two Prime cuts in it become a Token, each second.', 'gray')))]
        if pg == 'cols':
            acts += [('dep', P28.btn([T('⬇ ', col), T('Deposit', 'white')], B_DEP, width=150, tooltip=T(f'Everything in your inventory the {nm} takes goes into it', 'gray'))),
                     ('wd1', P28.btn([T('⬆ ', col), T('Withdraw a stack', 'white')], B_WD1, width=150, tooltip=T('Its first stack, into your hands (at your feet)', 'gray'))),
                     ('wda', P28.btn([T('⬆ ', col), T('Withdraw all', 'white')], B_WDA, width=150, tooltip=T('All of it, into your hands (at your feet)', 'gray')))]
        acts.append(('back', P28.btn([T(f'« {PAGE_OF[pg]}', 'gray')], B_BBACK, width=150, tooltip=T(f'Back to the {PAGE_OF[pg]} page', 'gray'))))
        cond = {'vac_on': 'if data storage bm:rpc {c:{bm_vac:1b}}', 'vac_off': 'unless data storage bm:rpc {c:{bm_vac:1b}}',
                'ac_on': f'unless data storage bm:rpc {{c:{{bm_{sw}:1b}}}}', 'ac_off': f'if data storage bm:rpc {{c:{{bm_{sw}:1b}}}}',
                'cv_on': 'if data storage bm:rpc {c:{bm_cconv:1b}}', 'cv_off': 'unless data storage bm:rpc {c:{bm_cconv:1b}}'}
        fn(f'p277/b/acts_{k}', ['data remove storage bm:rpc c', 'data modify storage bm:rpc c set from storage bm:rp v.it.components."minecraft:custom_data"'] + [(f'execute {cond[a]} run ' if a in cond else '') + f'data modify storage bm:rp v.acts append value {snbt(b)}' for a, b in acts])
        F[f'p277/b/page_{k}'] += ['execute store result storage bm:rp v.j1 int 1 run scoreboard players add @s bm.rbj 1', 'scoreboard players remove @s bm.rbj 1',
                                  f'function bm:p277/b/page2_{k} with storage bm:rp v', f'function bm:p277/b/acts_{k}',
                                  'function bm:p277/b/page_show with storage bm:rp v', page_turn]
    bd = P28.multi(head('a look inside'), '@@BODY@@', '@@ACTS@@', columns=2)
    fn('p277/b/page_show', ['$dialog show @s ' + snbt(bd).replace('"@@BODY@@"', '$(body)').replace('"@@ACTS@@"', '$(acts)')])
    fn('p277/b/page', ['function bm:p277/b/sel'] + [f'execute if score @s bm.rbk matches {ki} run return run function bm:p277/b/page_{b[0]} with storage bm:rp s' for ki, b in enumerate(BAGK)])
    # (a row pressed: that one's page)
    for ki, b in enumerate(BAGK):
        for j in range(BAGMAX):
            fn(f'p277/b/pick_{b[0]}{j}', [f'scoreboard players set @s bm.rbk {ki}', f'scoreboard players set @s bm.rbj {j}', 'function bm:p277/b/page'])

    # ---------------------------------------------------------------- its buttons (as the selected one: bm.rbk / bm.rbj)
    for ki, (k, iid, pg, nm, bxkind, coll, sw) in enumerate(BAGK):
        col = colour(iid)
        fn(f'p277/b/do_unfold_{k}', ['function bm:p277/b/sel', 'dialog clear @s', f'function bm:p277/b/unfold_{k} with storage bm:rp s'])
        # take back: folded first if it's out; whatever is unfolded after it on the Pack keeps its place
        fn(f'p277/b/do_take_{k}', ['function bm:p277/b/sel', 'scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players operation #rbj bm.rng = @s bm.rbj',
                                   f'execute as @e[type=minecraft:marker,tag=bm.rbbox,scores={{bm.rbk={ki}}}] if score @s bm.pid = #kp bm.pid if score @s bm.rbj = #rbj bm.rng at @s run function bm:p33/box/close',
                                   'function bm:p277/b/take_m with storage bm:rp s',
                                   f'execute as @e[type=minecraft:marker,tag=bm.rbbox,scores={{bm.rbk={ki}}}] if score @s bm.pid = #kp bm.pid if score @s bm.rbj > #rbj bm.rng run scoreboard players remove @s bm.rbj 1',
                                   f'scoreboard players remove @s bm.rb_{k} 1', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
                                   tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(' comes off your Rat Pack, its load and all.', 'gray')]),
                                   f'function bm:p277/b/{pg}'])
        if sw:
            if sw == 'vac':
                tog = ['data remove storage bm:rpc c', '$data modify storage bm:rpc c set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data"', 'execute if data storage bm:rpc {c:{bm_vac:1b}} run return run function bm:p277/b/vac_off with storage bm:rp s',
                       'function bm:p277/b/vac_on with storage bm:rp s']
            elif sw == 'rpoff':
                tog = ['data remove storage bm:rpc c', '$data modify storage bm:rpc c set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data"', '$execute if data storage bm:rpc {c:{bm_rpoff:1b}} run return run data remove storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data".bm_rpoff',
                       '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data".bm_rpoff set value 1b']
            else:
                tog = ['data remove storage bm:rpc c', '$data modify storage bm:rpc c set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data"', 'execute if data storage bm:rpc {c:{bm_coff:1b}} run return run function bm:p277/b/cool_set with storage bm:rp s',
                       '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data" merge value {bm_coff:1b,bm_cconv:0b}',
                       '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:enchantment_glint_override" set value 0b']
            fn(f'p277/b/tog_{k}', tog)
            fn(f'p277/b/do_auto_{k}', ['function bm:p277/b/sel', click, f'function bm:p277/b/tog_{k} with storage bm:rp s', 'function bm:p277/b/page'])
    fn('p277/b/vac_on', ['$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data".bm_vac set value 1b',
                         '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:item_model" set value "bm:vacuum_satchel_on"',
                         '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:enchantment_glint_override" set value 1b',
                         'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.6 1.6'])
    fn('p277/b/vac_off', ['$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data".bm_vac set value 0b',
                          '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:item_model" set value "bm:vacuum_satchel"',
                          '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:enchantment_glint_override" set value 0b',
                          'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.6 1.6'])
    fn('p277/b/cool_set', ['$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data" merge value {bm_coff:0b}',
                           '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:enchantment_glint_override" set value 1b'])
    fn('p277/b/conv_tog', ['data remove storage bm:rpc c', '$data modify storage bm:rpc c set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data"', '$execute if data storage bm:rpc {c:{bm_cconv:1b}} run return run data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data".bm_cconv set value 0b',
                           '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:custom_data" merge value {bm_coff:0b,bm_cconv:1b}',
                           '$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:enchantment_glint_override" set value 1b'])
    fn('p277/b/do_conv', ['function bm:p277/b/sel', click, 'execute unless score @s bm.rbk matches 4 run return run function bm:p28/stale',
                          'function bm:p277/b/conv_tog with storage bm:rp s', 'function bm:p277/b/page'])
    fn('p277/b/take_m', ['$execute unless data storage bm:pw p$(pid).rb_$(k)[$(j)] run return 0',
                         'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                         '$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).rb_$(k)[$(j)].it',
                         'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item.components."minecraft:custom_data".bm_rpno set value 1b',
                         'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', '$data remove storage bm:pw p$(pid).rb_$(k)[$(j)]'])

    # ---------------------------------------------------------------- collecting from the Pack (as carried: the same items, the same range)
    for ki, (k, iid, pg, nm, bxkind, coll, sw) in enumerate(BAGK):
        if not coll: continue
        R, LIM, filt = coll
        filt = filt.replace('@@BAG@@', BAG)
        off = {'vac': 'unless data storage bm:rpc {c:{bm_vac:1b}}', 'rpoff': 'if data storage bm:rpc {c:{bm_rpoff:1b}}', 'coff': 'if data storage bm:rpc {c:{bm_coff:1b}}'}[sw]
        for j in range(BAGMAX):
            fn(f'p277/c/{k}{j}', [f'$execute unless data storage {rb(k, j)} run return 0', f'$execute if data storage {rb(k, j)}.out run return 0',
                                 'data remove storage bm:rpc c', f'$data modify storage bm:rpc c set from storage {rb(k, j)}.it.components."minecraft:custom_data"',
                                 'execute ' + off + ' run return 0',
                                 f'execute unless entity @e[type=minecraft:item,distance=..{R},nbt={{PickupDelay:0s}}] run return 0',
                                 'data remove storage bm:tmp vac.c', f'$data modify storage bm:tmp vac.c set from storage {rb(k, j)}.it.components."minecraft:container"',
                                 'execute unless data storage bm:tmp vac.c run data modify storage bm:tmp vac.c set value []',
                                 'scoreboard players set #vtak bm.rng 0', 'scoreboard players set #vfull bm.rng 0',
                                 f'execute as @e[type=minecraft:item,distance=..{R},nbt={{PickupDelay:0s}},limit={LIM},sort=nearest] {filt} at @s run function bm:p33/vac/take',
                                 f'$execute if score #vtak bm.rng matches 1.. run data modify storage {rb(k, j)}.it.components."minecraft:container" set from storage bm:tmp vac.c',
                                 'execute if score #vtak bm.rng matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 0.6'])
        fn(f'p277/c/{k}', [pid] + [f'function bm:p277/c/{k}{j} with storage bm:rp t' for j in range(BAGMAX)])
        fast.append(f'execute as @a[tag=bm.pwc,tag=!bm.gvp,tag=!bm.gvdead,gamemode=!spectator,scores={{bm.rb_{k}=1..}}] at @s '
                    f'if entity @e[type=minecraft:item,distance=..{R},nbt={{PickupDelay:0s}}] run function bm:p277/c/{k}')
    # (the Prime Coolers' cuts -> Tokens, each second: as p148/cool/conv, from the Pack)
    for j in range(BAGMAX):
        fn(f'p277/cv/{j}', ['data remove storage bm:rpc c', f'$data modify storage bm:rpc c set from storage {rb("pc", j)}.it.components."minecraft:custom_data"',
                           'execute unless data storage bm:rpc {c:{bm_cconv:1b}} run return 0',
                           f'$execute if data storage {rb("pc", j)}.out run return 0',
                           f'$data modify storage bm:tmp vac.c set from storage {rb("pc", j)}.it.components."minecraft:container"',
                           'execute unless data storage bm:tmp vac.c[0] run return 0', 'scoreboard players set #cn bm.rng 0'] +
           [l for i in range(27) for l in ('scoreboard players set #cc bm.rng 1',
                                           f'execute if data storage bm:tmp vac.c[{i}].item.count store result score #cc bm.rng run data get storage bm:tmp vac.c[{i}].item.count',
                                           f'execute if data storage bm:tmp vac.c[{i}] run scoreboard players operation #cn bm.rng += #cc bm.rng')] +
           ['execute if score #cn bm.rng matches ..1 run return 0',
            'scoreboard players operation #ct bm.rng = #cn bm.rng', 'scoreboard players operation #ct bm.rng /= #2 bm.rng',
            'scoreboard players operation #cl bm.rng = #cn bm.rng', 'scoreboard players operation #cl bm.rng %= #2 bm.rng',
            'data modify storage bm:tmp cpk.k set from storage bm:tmp vac.c[0]', 'data modify storage bm:tmp cpk.k.slot set value 0', 'data modify storage bm:tmp cpk.k.item.count set value 1',
            'data modify storage bm:tmp vac.c set value []', 'execute if score #cl bm.rng matches 1 run data modify storage bm:tmp vac.c append from storage bm:tmp cpk.k',
            f'$data modify storage {rb("pc", j)}.it.components."minecraft:container" set from storage bm:tmp vac.c',
            'scoreboard players operation #cg bm.rng = #ct bm.rng', 'function bm:p148/cool/pay', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.7 1.2',
            title('@s', 'actionbar', [T('Prime Cooler (Rat Pack): ', '#8ad8ff', bold=True), {'score': {'name': '#cn', 'objective': 'bm.rng'}, 'color': 'white'},
                                      T(' cuts -> ', 'gray'), {'score': {'name': '#ct', 'objective': 'bm.rng'}, 'color': '#ffcf40', 'bold': True}, T(' Tokens', '#ffcf40')])])
    fn('p277/cv', [pid] + [f'function bm:p277/cv/{j} with storage bm:rp t' for j in range(BAGMAX)])
    second.append('execute as @a[tag=bm.pwc,tag=!bm.gvp,tag=!bm.gvdead,gamemode=!spectator,scores={bm.rb_pc=1..}] at @s run function bm:p277/cv')

    # ---------------------------------------------------------------- deposit / withdraw (a collector's page)
    cut_sel = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{c}"}}' for c in P148.PRIME_CUTS) + ']'
    dfilt = {'sj': '#bm:p174_mob', 'om': '#bm:p174_ore', 'pc': cut_sel}
    for k, flt in dfilt.items():
        fn(f'p277/d/{k}', ['$data modify storage bm:tmp vac.c set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:container"',
                           'execute unless data storage bm:tmp vac.c run data modify storage bm:tmp vac.c set value []', 'scoreboard players set #rqd bm.rng 0'] +
           [f'execute if items entity @s container.{s} {flt} unless items entity @s container.{s} {BAG} run function bm:p277/d/slot {{s:{s}}}' for s in range(36)] +
           ['$data modify storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:container" set from storage bm:tmp vac.c'])
    fn('p277/d/slot', ['$data modify storage bm:rp d.it set from entity @s Inventory[{Slot:$(s)b}]', 'data remove storage bm:rp d.it.Slot',
                       'summon minecraft:item ~ ~ ~ {Tags:["bm.rqdep"],PickupDelay:32767s,Item:{id:"minecraft:stone",count:1}}',
                       'data modify entity @e[type=minecraft:item,tag=bm.rqdep,limit=1,distance=..1] Item set from storage bm:rp d.it',
                       'scoreboard players set #vtak bm.rng 0', 'scoreboard players set #vfull bm.rng 0',
                       'execute as @e[type=minecraft:item,tag=bm.rqdep,limit=1,distance=..1] at @s run function bm:p33/vac/take',
                       '$execute unless entity @e[type=minecraft:item,tag=bm.rqdep,distance=..1] run item replace entity @s container.$(s) with minecraft:air',
                       'execute unless entity @e[type=minecraft:item,tag=bm.rqdep,distance=..1] run scoreboard players add #rqd bm.rng 1',
                       'execute as @e[type=minecraft:item,tag=bm.rqdep,distance=..1] store result storage bm:rp d.n int 1 run data get entity @s Item.count',
                       '$data modify storage bm:rp d.s set value $(s)',
                       'execute if entity @e[type=minecraft:item,tag=bm.rqdep,distance=..1] run function bm:p277/d/left with storage bm:rp d',
                       'kill @e[type=minecraft:item,tag=bm.rqdep]'])
    fn('p277/d/left', ['$item modify entity @s container.$(s) {function:"minecraft:set_count",count:$(n)}'])
    fn('p277/d/do', ['function bm:p277/b/sel', 'execute unless score @s bm.rbk matches 2..4 run return run function bm:p28/stale',
                     'scoreboard players set #rqd bm.rng 0'] +
       [f'execute if score @s bm.rbk matches {ki} run function bm:p277/d/{b[0]} with storage bm:rp s' for ki, b in enumerate(BAGK) if b[0] in dfilt] +
       ['execute if score #rqd bm.rng matches 0 run ' + say('Nothing in your inventory it takes (or it\'s full).'),
        'execute if score #rqd bm.rng matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 0.8',
        'execute if score #rqd bm.rng matches 1.. run ' + title('@s', 'actionbar', [T('Deposited ', PURPLE), {'score': {'name': '#rqd', 'objective': 'bm.rng'}, 'color': 'white'}, T(' stacks.', PURPLE)]),
        'function bm:p277/b/page'])
    # (deposit all they take, from the Collectors page: every collector, the first with room first)
    da = ['scoreboard players set #rqd bm.rng 0', pid, 'data modify storage bm:rp s.pid set from storage bm:rp t.pid']
    for ki, b in enumerate(BAGK):
        if b[0] not in dfilt: continue
        for j in range(BAGMAX):
            da += [f'execute if score @s bm.rb_{b[0]} matches {j + 1}.. run data modify storage bm:rp s.k set value "{b[0]}"',
                   f'execute if score @s bm.rb_{b[0]} matches {j + 1}.. run data modify storage bm:rp s.j set value {j}',
                   f'execute if score @s bm.rb_{b[0]} matches {j + 1}.. run function bm:p277/d/{b[0]} with storage bm:rp s']
    da += ['execute if score #rqd bm.rng matches 0 run ' + say('Nothing in your inventory your collectors take (or they\'re full).'),
           'execute if score #rqd bm.rng matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 0.8',
           'execute if score #rqd bm.rng matches 1.. run ' + title('@s', 'actionbar', [T('Deposited ', PURPLE), {'score': {'name': '#rqd', 'objective': 'bm.rng'}, 'color': 'white'}, T(' stacks.', PURPLE)]),
           'function bm:p277/b/cols']
    fn('p277/d/all', da)
    fn('p277/w1/m', ['$execute unless data storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:container"[0] run return 0',
                     'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                     '$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:container"[0].item',
                     'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                     'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', '$data remove storage bm:pw p$(pid).rb_$(k)[$(j)].it.components."minecraft:container"[0]', 'return 1'])
    fn('p277/w1/do', ['function bm:p277/b/sel', 'execute unless score @s bm.rbk matches 2..4 run return run function bm:p28/stale',
                      'execute store result score #rqd bm.rng run function bm:p277/w1/m with storage bm:rp s',
                      'execute if score #rqd bm.rng matches 0 run ' + say('It\'s empty.'), 'execute if score #rqd bm.rng matches 1 run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 1.2',
                      'function bm:p277/b/page'])
    fn('p277/w1/all', ['execute store result score #rqw bm.rng run function bm:p277/w1/m with storage bm:rp s', 'execute if score #rqw bm.rng matches 1 run scoreboard players add #rqd bm.rng 1',
                       'execute if score #rqw bm.rng matches 1 if score #rqd bm.rng matches ..27 run function bm:p277/w1/all'])
    fn('p277/w1/doall', ['function bm:p277/b/sel', 'execute unless score @s bm.rbk matches 2..4 run return run function bm:p28/stale',
                         'scoreboard players set #rqd bm.rng 0', 'function bm:p277/w1/all',
                         'execute if score #rqd bm.rng matches 0 run ' + say('It\'s empty.'), 'execute if score #rqd bm.rng matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 1.2',
                         'function bm:p277/b/page'])

    # ================================================================== AUTO-PACK (each second, your own inventory only; never in a heist)
    fol = F['admin/follower_items']
    FOL = []
    for i, l in enumerate(fol):
        m = re.search(r'custom_data=\{[^}]*bm:"([a-z0-9_]+)"', l)
        assert m, l[:200]
        a_ = F[f'p179/w/add{i}']
        w = next(re.search(r'tag @s add (bm\.pw_\w+)', x).group(1) for x in a_ if 'tag @s add bm.pw_' in x)
        FOL.append((i, m.group(1), w))
    # (the slot it's in: the first, by its id - an extra predicate for the Ledger: never a Heist Ledger)
    fn('p277/ap/slot', ['scoreboard players set #rqs bm.rng -1'] +
       [f'$execute if items entity @s container.{s} *[minecraft:custom_data~{{bm:"$(id)"}}{NOPK}] run return run scoreboard players set #rqs bm.rng {s}' for s in range(36)])
    fn('p277/ap/slotl', ['scoreboard players set #rqs bm.rng -1'] +
       [f'execute if items entity @s container.{s} {holds("fixers_ledger", HLNOT + NOPK)} run return run scoreboard players set #rqs bm.rng {s}' for s in range(36)])
    fn('p277/ap/find', ['execute if data storage bm:rp {a:{l:1b}} run function bm:p277/ap/slotl', 'execute unless data storage bm:rp {a:{l:1b}} run function bm:p277/ap/slot with storage bm:rp a',
                        'execute if score #rqs bm.rng matches ..-1 run return fail',
                        'execute store result storage bm:rp a.s int 1 run scoreboard players get #rqs bm.rng', 'return 1'])
    fn('p277/ap/mv', ['$data modify storage bm:pw p$(pid).r$(k) set from entity @s Inventory[{Slot:$(s)b}]', '$data remove storage bm:pw p$(pid).r$(k).Slot',
                      '$execute if data storage bm:pw p$(pid).r$(k) run item replace entity @s container.$(s) with minecraft:air'])
    fn('p277/ap/mvhb', ['$data modify storage bm:pw p$(pid).hb set from entity @s Inventory[{Slot:$(s)b}]', '$data remove storage bm:pw p$(pid).hb.Slot',
                        '$execute if data storage bm:pw p$(pid).hb run item replace entity @s container.$(s) with minecraft:air'])
    fn('p277/ap/mvadd', ['$execute store result storage bm:pw p$(pid).r$(k).count int 1 run scoreboard players get #rqt bm.rng',
                         '$item replace entity @s container.$(s) with minecraft:air'])
    fn('p277/ap/bag', ['$data modify storage bm:pw p$(pid).rb_$(k) append value {it:{}}', '$data modify storage bm:pw p$(pid).rb_$(k)[-1].it set from entity @s Inventory[{Slot:$(s)b}]',
                       '$data remove storage bm:pw p$(pid).rb_$(k)[-1].it.Slot', '$item replace entity @s container.$(s) with minecraft:air'])
    fn('p277/ap/fol', ['$data modify storage bm:pw p$(pid).k$(i) set from entity @s Inventory[{Slot:$(s)b}]', '$data remove storage bm:pw p$(pid).k$(i).Slot',
                       '$item replace entity @s container.$(s) with minecraft:air', '$scoreboard players set @s bm.pw$(i) 1'])
    pull = lambda nm, col, where: tellraw('@s', PRE + [T(nm, col, bold=True), T(f' is on your Rat Pack now ({where} page). ', 'gray'), T('Take it out any time from there.', 'dark_gray')])
    run = ['execute store result storage bm:rp a.pid int 1 run scoreboard players get @s bm.pid', 'data remove storage bm:rp a.l']
    on_ = lambda key, dflt: (f'unless score @s bm.rqap_{key} matches 2' if dflt else f'if score @s bm.rqap_{key} matches 1')
    dfl = {k: d for k, l, d in AP}
    # followers
    anyf = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{iid}"}}' for i, iid, w in FOL) + ']'
    fa = []
    for i, iid, w in FOL:
        fn(f'p277/ap/f{i}', [f'data modify storage bm:rp a.id set value "{iid}"', f'data modify storage bm:rp a.i set value {i}', 'execute unless function bm:p277/ap/find run return 0',
                             'function bm:p277/ap/fol with storage bm:rp a', f'tag @s add {w}', pull(ITEMS[iid]['name'], colour(iid), 'Partners')])
        fa.append(f'execute unless score @s bm.pw{i} matches 1 if items entity @s container.* {holds(iid, NOPK)} run function bm:p277/ap/f{i}')
    fn('p277/ap/k_fol', fa)
    run.append(f'execute {on_("fol", True)} if items entity @s container.* {anyf} run function bm:p277/ap/k_fol')
    for c, L in CATS.items():
        ca = []
        for iid in L:
            e = BY[iid]
            x = HLNOT if iid == 'fixers_ledger' else ''
            if iid == 'bm_handbook':
                body = [f'data modify storage bm:rp a.id set value "{iid}"', 'execute unless function bm:p277/ap/find run return 0',
                        'function bm:p277/ap/mvhb with storage bm:rp a', 'scoreboard players set @s bm.pwhb 1', 'tag @s add bm.pw_hb']
                cond = 'unless score @s bm.pwhb matches 1'
            elif e['stack'] == 1:
                body = [f'data modify storage bm:rp a.id set value "{iid}"', f'data modify storage bm:rp a.k set value "{e["path"][1:]}"',
                        'execute unless function bm:p277/ap/find run return 0', 'function bm:p277/ap/mv with storage bm:rp a', f'scoreboard players set @s {e["obj"]} 1']
                cond = f'unless score @s {e["obj"]} matches 1..'
            else:                                  # (a stack: added to what's on, if it fits - else left be)
                body = [f'data modify storage bm:rp a.id set value "{iid}"', f'data modify storage bm:rp a.k set value "{e["path"][1:]}"',
                        'execute unless function bm:p277/ap/find run return 0',
                        f'execute if score @s {e["obj"]} matches ..0 run return run function bm:p277/ap/s1_{iid}',
                        'function bm:p277/ap/cnt with storage bm:rp a', f'scoreboard players operation #rqt bm.rng += @s {e["obj"]}',
                        f'execute if score #rqt bm.rng matches {e["stack"] + 1}.. run return 0',
                        'function bm:p277/ap/mvadd with storage bm:rp a', f'scoreboard players operation @s {e["obj"]} = #rqt bm.rng']
                fn(f'p277/ap/s1_{iid}', ['function bm:p277/ap/mv with storage bm:rp a', f'execute store result score @s {e["obj"]} run data get storage bm:rp a.c',
                                         'function bm:p277/ap/cnt1 with storage bm:rp a', 'function bm:p277/tg', pull(e['name'], e['col'], PAGE_OF[c])])
                cond = ''
            if x: body.insert(0, 'data modify storage bm:rp a.l set value 1b')
            if e['kind'] == 'worn': body.append(f'function bm:p277/c/aw_{iid}')
            body += ['function bm:p277/tg', pull(e['name'], e['col'], PAGE_OF[c])]
            if x: body.append('data remove storage bm:rp a.l')
            fn(f'p277/ap/e_{iid}', body)
            ca.append(' '.join(['execute'] + ([cond] if cond else []) + [f'if items entity @s container.* {holds(iid, x + NOPK)} run function bm:p277/ap/e_{iid}']))
        anyc = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{iid}"}}' for iid in L) + ']'
        fn(f'p277/ap/k_{c}', ca)
        run.append(f'execute {on_(c, dfl[c])} if items entity @s container.* {anyc} run function bm:p277/ap/k_{c}')
    fn('p277/ap/cnt', ['$execute store result score #rqt bm.rng run data get entity @s Inventory[{Slot:$(s)b}].count'])
    fn('p277/ap/cnt1', ['$execute store result score #rqt bm.rng run data get storage bm:pw p$(pid).r$(k).count'])
    for c in CATS:
        for iid in CATS[c]:
            if f'p277/ap/s1_{iid}' in F:
                e = BY[iid]
                F[f'p277/ap/s1_{iid}'] = ['function bm:p277/ap/mv with storage bm:rp a', 'function bm:p277/ap/cnt1 with storage bm:rp a',
                                          f'scoreboard players operation @s {e["obj"]} = #rqt bm.rng', f'execute if score @s {e["obj"]} matches ..0 run scoreboard players set @s {e["obj"]} 1',
                                          'function bm:p277/tg', pull(e['name'], e['col'], PAGE_OF[c])]
    # bags and collectors
    for pg in ('bags', 'cols'):
        ba = []
        for ki, (k, iid, pg_, nm, *_r) in enumerate(BAGK):
            if pg_ != pg: continue
            fn(f'p277/ap/b_{k}', [f'data modify storage bm:rp a.id set value "{iid}"', f'data modify storage bm:rp a.k set value "{k}"',
                                  'execute unless function bm:p277/ap/find run return 0', 'function bm:p277/ap/bag with storage bm:rp a',
                                  f'scoreboard players add @s bm.rb_{k} 1', pull(ITEMS[iid]['name'], colour(iid), PAGE_OF[pg])])
            ba.append(f'execute unless score @s bm.rb_{k} matches {BAGMAX}.. if items entity @s container.* {holds(iid, NOPK)} run function bm:p277/ap/b_{k}')
        fn(f'p277/ap/k_{pg}', ba)
        run.append(f'execute {on_(pg, dfl[pg])} run function bm:p277/ap/k_{pg}')
    fn('p277/ap/run', run)
    second.append('execute as @a[tag=bm.pwc,tag=!bm.gvp,tag=!bm.gvdead,gamemode=!spectator,scores={bm.pid=1..}] run function bm:p277/ap/run')

    # ================================================================== THE HEIST LEDGER
    import copy
    lc = copy.deepcopy(ITEMS['fixers_ledger']['comps'])
    lc['minecraft:item_name'] = {'text': '', 'italic': False, 'extra': [{'text': '✦ ', 'color': '#e8c070'}, {'text': 'The Heist Ledger', 'color': '#e8c070', 'bold': True}, {'text': ' ✦', 'color': '#e8c070'}]}
    lc['minecraft:lore'] = [T('The Fixer\'s Ledger, for this heist only.', 'gray'), T('Use: the crew, the skips, the rest.', 'blue'),
                            T('It can\'t be lost: drop it or put it away', 'blue'), T('and it\'s back in your pocket.', 'blue'),
                            T('The Fixer takes it back at the door.', 'dark_gray')]
    lc['minecraft:custom_data'] = dict(ITEMS['fixers_ledger']['comps']['minecraft:custom_data'], bm_hl=B(1))
    lc['minecraft:enchantment_glint_override'] = True
    hl_give = 'give @s ' + ITEMS['fixers_ledger']['base'] + '[' + ','.join(k_ if k_.startswith('!') else f'{k_}={snbt(v)}' for k_, v in lc.items()) + '] 1'
    fn('p277/hl/give', [hl_give])
    fn('p277/hl/enter', ['clear @s ' + HL, 'function bm:p277/hl/give',
                         tellraw('@s', [T('[Office] ', '#e8c070', bold=True), T('The Fixer hands you a Heist Ledger for this job. ', '#e8c070'),
                                        T('Your Rat Pack waits at the coat check with the rest.', 'gray')])])
    for s_ in range(__import__('phase70').SLOTS):
        for f in (f'p70/s{s_}/enter', f'p70/s{s_}/join'):
            F[f].append('function bm:p277/hl/enter')
    F['p70/unraid'].insert(0, 'clear @s ' + HL)
    # (the welcome gift counts a Ledger on your Pack, and never a Heist Ledger)
    fl = F['p80/first_ledger']
    fl[:] = [l.replace('*[minecraft:custom_data~{bm:"fixers_ledger"}]', '*[minecraft:custom_data~{bm:"fixers_ledger"}' + HLNOT + ']') for l in fl]
    k_ = next(i for i, l in enumerate(fl) if 'container.*' in l and 'fixers_ledger' in l)
    fl.insert(k_, f'execute if score @s {BY["fixers_ledger"]["obj"]} matches 1.. run return 0')
    fl[:] = [l for l in fl if not (l.startswith('execute if entity @s[tag=bm.rqt_fixers_ledger]') and 'return 0' in l)]
    # inside: missing (dropped, put away) -> a fresh one; more than one -> one; never in a frame, a chest near you or on the ground
    fast += [f'execute as @e[type=minecraft:item] if items entity @s contents {HL} run kill @s',
             f'execute as @a[tag=bm.gvp,tag=!bm.gvdead] unless items entity @s container.* {HL} unless items entity @s weapon.offhand {HL} '
             f'unless items entity @s player.cursor {HL} unless items entity @s player.crafting.* {HL} at @s run function bm:p277/hl/missing']
    sweep = [f'execute if items block ~{x} ~{y} ~{z} container.* {HL} positioned ~{x} ~{y} ~{z} run function bm:p277/hl/strip'
             for x in range(-4, 5) for y in range(-1, 3) for z in range(-4, 5)]
    fn('p277/hl/missing', sweep + ['function bm:p277/hl/give', title('@s', 'actionbar', T('Your Heist Ledger is back in your pocket - it stays with you in the vault.', '#e8c070'))])
    fn('p277/hl/strip', [f'execute if items block ~ ~ ~ container.{i} {HL} run item replace block ~ ~ ~ container.{i} with minecraft:air' for i in range(27)])
    second += [f'execute as @e[type=#bm:p277_frames] if items entity @s contents {HL} run item replace entity @s contents with minecraft:air',
               f'execute as @a[tag=bm.gvp,tag=!bm.gvdead] store result score @s bm.rqhl run clear @s {HL} 0',
               'execute as @a[tag=bm.gvp,tag=!bm.gvdead,scores={bm.rqhl=2..}] run function bm:p277/hl/one',
               f'clear @a[tag=!bm.gvp,tag=!bm.gvdead] {HL}',
               f'execute as @a if items entity @s enderchest.* {HL} run function bm:p277/hl/ender']
    G.wjson('bm/tags/entity_type/p277_frames.json', {'values': ['minecraft:item_frame', 'minecraft:glow_item_frame']})
    fn('p277/hl/one', [f'clear @s {HL}', 'function bm:p277/hl/give', 'scoreboard players reset @s bm.rqhl'])
    fn('p277/hl/ender', [f'execute if items entity @s enderchest.{i} {HL} run item replace entity @s enderchest.{i} with minecraft:air' for i in range(27)])

    # ================================================================== THE OLD WHEELS: re-issued as Rat Packs (keeping everything: it lives per player)
    old = f'*[minecraft:custom_data~{{bm:"partner_wheel"}},!minecraft:custom_data~{{bmrp:{RQV}}}]'
    fn('p277/reissue', [f'execute if items entity @s {slot} {old} run item modify entity @s {slot} bm:refresh/partner_wheel' for slot, _ in P18.SLOTS] +
       [tellraw('@s', PRE + [T('Your Partner Wheel is the Rat Pack now', PURPLE, bold=True), T(' - every partner still on it, and pages for your tools, keys, charms, maps, mounts and bags.', 'gray')])])
    second += [f'execute as @a if items entity @s container.* {old} run function bm:p277/reissue',
               f'execute as @a unless items entity @s container.* {old} if items entity @s weapon.offhand {old} run function bm:p277/reissue']

    # ================================================================== THE ROUTER
    act = [f'execute if score #act bm.pay matches {B_SEC["partners"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p179/w/open',
           f'execute if score #act bm.pay matches {B_SEC["settings"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p277/settings',
           f'execute if score #act bm.pay matches {B_SEC["handbook"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p277/u/bm_handbook',
           f'execute if score #act bm.pay matches {B_SEC["guide"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p276/open',
           f'execute if score #act bm.pay matches {B_SEC["bags"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p277/b/bags',
           f'execute if score #act bm.pay matches {B_SEC["cols"]} if score @s bm.menu matches {M_FRONT} run return run function bm:p277/b/cols']
    for c in CATS:
        act.append(f'execute if score #act bm.pay matches {B_SEC[c]} if score @s bm.menu matches {M_FRONT} run return run function bm:p277/go/{c}')
        fn(f'p277/go/{c}', ['tag @s remove bm.rqtb', f'scoreboard players set @s bm.pg_rp{c} 0', f'function bm:{page_fn[c]}'])
    back_menus = [M_SET, M_BAGS, M_COLS, 3350] + list(M_CAT.values())
    act += [f'execute if score #act bm.pay matches {B_BACK} if score @s bm.menu matches {m} run return run function bm:p277/open' for m in back_menus]
    act += [f'execute if score #act bm.pay matches {B_AP0 + i} if score @s bm.menu matches {M_SET} run return run function bm:p277/ap/tog_{key}' for i, (key, *_r) in enumerate(AP)]
    act += [f'execute if score #act bm.pay matches {B_YOURS} if score @s bm.menu matches {M_SET} run return run function bm:p260/ps/from_wh']
    for c in CATS:
        m = M_CAT[c]
        if c != 'keys':
            act.append(f'execute if score #act bm.pay matches {B_MODE} if score @s bm.menu matches {m} run return run function bm:p277/mode/{c}')
            fn(f'p277/mode/{c}', [click, 'execute if entity @s[tag=bm.rqtb] run tag @s add bm.rqtb2', 'tag @s add bm.rqtb',
                                  'execute if entity @s[tag=bm.rqtb2] run tag @s remove bm.rqtb', 'tag @s remove bm.rqtb2', f'function bm:{page_fn[c]}'])
        act += [f'execute if score #act bm.pay matches {B_PREV} if score @s bm.menu matches {m} run return run function bm:p277/pv/{c}',
                f'execute if score #act bm.pay matches {B_NEXT} if score @s bm.menu matches {m} run return run function bm:p277/nx/{c}']
    for c in list(CATS) + ['bags', 'cols']:
        target = page_fn.get(c, f'p277/b/{c}')
        fn(f'p277/pv/{c}', [f'scoreboard players remove @s bm.pg_rp{c} 1', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.6 1.2', f'function bm:{target}'])
        fn(f'p277/nx/{c}', [f'scoreboard players add @s bm.pg_rp{c} 1', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.6 1.2', f'function bm:{target}'])
    for e in E:
        act.append(f'execute if score #act bm.pay matches {B_E0 + e["n"]} if score @s bm.menu matches {M_CAT[e["cat"]]} run return run function bm:p277/e/{e["iid"]}')
    fn('p277/act', act + ['function bm:p28/stale'])
    F['p28/act'].append(f'execute if score #act bm.pay matches {M_FRONT}..8999 run return run function bm:p277/act')
    # (the bags' and collectors' block)
    bact = [f'execute if score #act bm.pay matches {B_DEPALL} if score @s bm.menu matches {M_COLS} run return run function bm:p277/d/all']
    for ki, b in enumerate(BAGK):
        mm = M_BAGS if b[2] == 'bags' else M_COLS
        bact += [f'execute if score #act bm.pay matches {B_ROW0 + ki * 10 + j} if score @s bm.menu matches {mm} run return run function bm:p277/b/pick_{b[0]}{j}' for j in range(BAGMAX)]
    bb = []
    for ki, (k, iid, pg, *_r) in enumerate(BAGK):
        bb += [f'execute if score @s bm.rbk matches {ki} if score #act bm.pay matches {B_UNFOLD} run return run function bm:p277/b/do_unfold_{k}',
               f'execute if score @s bm.rbk matches {ki} if score #act bm.pay matches {B_TAKE} run return run function bm:p277/b/do_take_{k}']
        if BAGK[ki][6]: bb.append(f'execute if score @s bm.rbk matches {ki} if score #act bm.pay matches {B_AUTO} run return run function bm:p277/b/do_auto_{k}')
        bb.append(f'execute if score @s bm.rbk matches {ki} if score #act bm.pay matches {B_BBACK} run return run function bm:p277/b/{pg}')
    fn('p277/b/det', bb + ['function bm:p28/stale'])
    bact += [f'execute if score #act bm.pay matches {c} if score @s bm.menu matches {M_BAG} run return run function bm:p277/b/det' for c in (B_UNFOLD, B_TAKE, B_AUTO, B_BBACK)]
    bact += [f'execute if score #act bm.pay matches {B_CONV} if score @s bm.menu matches {M_BAG} run return run function bm:p277/b/do_conv',
             f'execute if score #act bm.pay matches {B_DEP} if score @s bm.menu matches {M_BAG} run return run function bm:p277/d/do',
             f'execute if score #act bm.pay matches {B_WD1} if score @s bm.menu matches {M_BAG} run return run function bm:p277/w1/do',
             f'execute if score #act bm.pay matches {B_WDA} if score @s bm.menu matches {M_BAG} run return run function bm:p277/w1/doall']
    fn('p277/b/act', bact + ['function bm:p28/stale'])
    F['p28/act'].append(f'execute if score #act bm.pay matches {M_BAGS}..{B_ROW0 + 49} run return run function bm:p277/b/act')
    # (the pager's Previous / Next on the bag lists share the Rat Pack's codes: routed in p277/act too)
    for pg, mm in (('bags', M_BAGS), ('cols', M_COLS)):
        F['p277/act'][-1:-1] = [f'execute if score #act bm.pay matches {B_PREV} if score @s bm.menu matches {mm} run return run function bm:p277/pv/{pg}',
                                f'execute if score #act bm.pay matches {B_NEXT} if score @s bm.menu matches {mm} run return run function bm:p277/nx/{pg}']

    # ================================================================== the words: the wheel is the Rat Pack wherever a player reads it
    nw = 0
    tx = re.compile(r'(text:")((?:[^"\\]|\\.)*)(")')
    for name, L in F.items():
        for i, l in enumerate(L):
            if 'heel' not in l: continue
            nl = tx.sub(lambda mm: mm.group(1) + reword(mm.group(2)) + mm.group(3), l)
            if nl != l: L[i] = nl; nw += 1
    rep['lines reworded'] = nw
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/rat_pack', 'yellow'), T('  the Rat Pack, and one of every tool, key, charm, map and call it holds', 'gray')])]
    fn('admin/rat_pack', [give('partner_wheel')] + [give(e['iid']) for e in E] + [give(b[1]) for b in BAGK])
    F['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.rqh]']
    return rep
