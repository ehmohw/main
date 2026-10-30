"""3.0b: THE PARTICLE TOGGLER (the Fence, 1 Token) - and the switch every piece of gear's own particles answer to.

THE ITEM   right-click it (it's never used up - useitem's hold, as the Backpack): a little menu (menu 6900) with four
           switches, each showing its state - Charms, Armour, Weapons and Everything. A press flips it (a click, a line on
           the action bar) and the menu comes back showing the new state. Sneak + right-click flips Everything at once,
           without the menu. The choice is a tag on the player, so it holds through death, relogs and new versions.
THE TAGS   one per kind of gear (CATS): bm.np_charm, bm.np_armor, bm.np_weap. "Everything" sets all three.
           - charm: carried charms, trinkets and relics (in the pack or the off hand): the charm auras, the off-hand
             trinkets, laurels, talismans, the Ethereal Gem's motes
           - armor: armour set effects and every worn piece's own particles: the set orbits, crowns, halos, hats, boots,
             the Regalia's tiers, wings and elytra trails (Wings of the Damned / Holy Wings, the Last Night / First Light,
             the Dread Carapace, the Rat King's, the dragon's, the Golden Rat's) - never movement exhaust (EXHAUST: rocket and
             spring / triple-jump boots, the Squad Jetpack, the Starforged jet, the Gravitic Core's trail): it always shows
           - weap: a held weapon's idle glow (the boss weapons' bm_res auras, Democratus's scythe, the Horseman's heads,
             Apophiss's mace, Leo's trident in water)
           Only the player's own gear goes quiet: followers, hits on monsters, bosses, dungeons, the world, and the particles
           that tell you something (a proc firing, a ward up, a secret found, a charge building) are left as they are.

FOR NEW GEAR (the rule): a cosmetic particle a player gives off because of what they wear, hold or carry answers to one of
these tags. Either
  - put the particles in their own function and register it here: `noparts.gear('armor', 'p300/halo')` (the pass skips
    every particle line in it for a player with that kind off - the function must run as the player), or
  - write a root-loop line in the usual shape - `execute as @a[...] if items entity @s <slot> *[minecraft:custom_data~{bm...}]
    at @s run particle ...` in tick / loop/fast / loop/second: the pass gates those by their slot on its own.
apply() fails the build if a registered function is gone or has no particle line left (renamed? moved? say so here)."""
import re
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt
import economy as ECON

ITEM = 'particle_toggler'
COL = '#7ad8ff'
PRICE = ('token', 1)                          # (a convenience: the cheapest thing on the Fence's table)
ECON.DIRECT[ITEM] = (PRICE, None)             # (a final price: not run through the market's rescale)
CATS = (('charm', 'Charms', 'carried charms, trinkets, relics and their auras'),
        ('armor', 'Armour', 'set effects, crowns, halos, hats, boots, wings and trails'),
        ('weap', 'Weapons', 'held weapons\' idle glow'))
TAG = {k: f'bm.np_{k}' for k, _, _ in CATS}
MENU = 6900                                   # (bm.menu while the toggler's menu is up)
BTN = {'charm': 6901, 'armor': 6902, 'weap': 6903, 'all': 6904}

item(ITEM, TOTEM, 'Particle Toggler', COL,
     ['A brass switch the Fence swears by.', ('Right-click: switch off (or back on) the', 'blue'),
      ('particles your own gear gives off -', 'blue'), ('charms, armour, weapons, or everything.', 'blue'),
      ('Sneak + right-click: everything at once.', 'blue'), ('Only yours: followers, fights and the', 'gray'),
      ('world keep their sparkle. It remembers.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='misc', comps=hold())
HOLD[ITEM] = 'bm:np/use'


def extend_offers(O, offer):
    O['fence'].append(offer(PRICE, (ITEM, 1)))


# ===================================================================== what answers to which switch
FNS = {}       # function -> kind: every particle line in it is skipped for a player with that kind switched off


def gear(kind, *names):
    assert kind in TAG, kind
    for n in names: FNS[n] = kind


# (2.84c / phase15 / phase177 / phase179 / phase242's sets: their bonus function keeps its bonus, only its particle lines are gated;
#  sets/<id> and fx/<id> for every sets/has/<id> are added by apply())
gear('armor', 'sets/wings_trail', 'p2/sets/conqueror', 'p2/fx/conqueror', 'p34/lucky_set', 'p76/phantom_set', 'p35/sun/salute',
     # crowns and halos
     'p29/aurora', 'p131/crown/sec', 'p182/crown', 'p164/soul/aura', 'p215/crown', 'p238/crown', 'p242/crown',
     # the Hollow King's Regalia, tier by tier (and its angelic twin) - not the nova's gesture, which shows it charging
     'p2/rg/fx_1', 'p2/rg/fx_2', 'p2/rg/fx_3', 'p2/rg/fx_4', 'p2/rg/fx_5',
     'p182/fx_0', 'p182/fx_1', 'p182/fx_2', 'p182/fx_3', 'p182/fx_5',
     # wings and elytra trails
     'p20/dragon_trail', 'p29/rkwings', 'p2/ht/wings', 'p2/ht/wings_holy', 'p2/ht/trail', 'p2/ht/trail_holy',
     'p2/ht/launch', 'p2/ht/launch_holy', 'p2/ht/burn', 'p2/ht/burn_holy', 'p164/w/beat', 'p164/w/beating', 'p164/w/glide_fx',
     'p206/aura_dread', 'p206/aura_holy', 'p206/aura_glide', 'p206/aura_glide_holy',
     # boots (3.0b, the owner's: movement exhaust always shows - EXHAUST below)
     'p39/wwalk/hover')
gear('charm',
     # the charms (phase17/38/43: one picked a beat, in the pack or the off hand) - p17/charm/pick and all it calls, added by apply()
     'p117/aura/notes', 'p117/aura/firefly', 'p117/aura/honey', 'p117/aura/trial', 'p117/aura/gale',
     'p60/eth/carry', 'p71/laurel', 'p105/crown1', 'p105/crown2', 'p105/crown3', 'p105/crown4', 'p105/crown5',
     'p160/tal/blood', 'p160/tal/lucky', 'p160/tal/inv', 'p37/charm/night')
gear('weap', 'p42/aura', 'p42/aura_1', 'p42/aura_2', 'p42/aura_3', 'p42/aura_4', 'p131/mace/held', 'p59/leo/tide')
TREES = {'p17/charm/pick': 'charm'}       # (a function and everything it calls as the same player)
# (3.0b, the owner's call) MOVEMENT EXHAUST ALWAYS SHOWS - it shows you (and everyone round you) the gear is working, and where
# you're going: rocket boots, spring and triple-jump boots, the Squad Jetpack, the Starforged jet, the Gravitic Core's flight
# trail. Never registered above - apply() asserts none is, and leaves their inline root lines alone (EXHAUST_ITEMS).
EXHAUST = ('p26/rocket/boost', 'p26/rocket/burn', 'p33/triple/big', 'p33/spring/jumped', 'p33/spring/tick', 'p241/relic/jet',
           'p242/sf/jet', 'p32/gcore/fly')
EXHAUST_ITEMS = ('rocket_boots', 'rocket_boots_2', 'spring_boots', 'triple_boots', 'gravitic_core')

# root-loop lines that give off a worn / held / carried item's particles inline (phase16's bm_res, phase29's bm_fx cosmetics, ...)
ROOTS = ('tick', 'loop/fast', 'loop/second', 'loop/second_b')
INLINE = re.compile(r'^execute as @a\[([^\]]*)\] if items entity @s (armor\.\w+|weapon\.\w+|container\.\*) '
                    r'\*\[minecraft:custom_data~\{\w+:"\w+"\}\] at @s run particle ')
SLOT_KIND = lambda slot: 'armor' if slot.startswith('armor.') else 'weap' if slot == 'weapon.mainhand' else 'charm'
ROOT_LINES = {'execute as @a[tag=bm.kweth,tag=bm.eth] at @s run particle ': 'armor'}      # (the Ethereal Tendrils, worn while ethereal)

PART = re.compile(r'(^\$?|\brun )particle ')
CALL = re.compile(r'function bm:([\w/]+)')


def _gate_line(l, tag):
    """the line, skipped for a player with `tag` (the condition reads @s before anything the line changes)"""
    if l.startswith('$execute '): return f'$execute unless entity @s[tag={tag}] ' + l[len('$execute '):]
    if l.startswith('execute '): return f'execute unless entity @s[tag={tag}] ' + l[len('execute '):]
    if l.startswith('$particle '): return f'$execute unless entity @s[tag={tag}] run ' + l[1:]
    assert l.startswith('particle '), l
    return f'execute unless entity @s[tag={tag}] run ' + l


def _tree(F, root):
    """root and every function it calls without leaving the player (no as / on / summon in the way)"""
    out, st = [], [root]
    while st:
        f = st.pop()
        if f in out or f not in F: continue
        out.append(f)
        for l in F[f]:
            pre = l.split(' run function ')[0]
            if re.search(r'\b(as|on) (?!@s\b)', pre): continue
            st += CALL.findall(l)
    return out


def apply(G):
    """the gate (late: after every phase has written its gear, before optimize / prune). Returns (functions, lines, root lines)."""
    F = G.FUNCS
    todo = dict(FNS)
    assert not set(EXHAUST) & set(todo), f'noparts: movement exhaust must always show: {sorted(set(EXHAUST) & set(todo))}'
    for f in sorted(F):
        if f.startswith('sets/has/'):
            sid = f[len('sets/has/'):]
            for g in (f'sets/{sid}', f'fx/{sid}'):
                if g in F: todo.setdefault(g, 'armor')
    for root, kind in TREES.items():
        for g in _tree(F, root): todo.setdefault(g, kind)
    nf = nl = 0
    for f, kind in sorted(todo.items()):
        if f not in F:
            assert not G.PHASE2 or f.startswith(('sets/', 'fx/')), f'noparts: {f} is gone - register its new name'
            continue
        k = 0
        for i, l in enumerate(F[f]):
            if PART.search(l) and not l.startswith(('return ', '$return ')):
                F[f][i] = _gate_line(l, TAG[kind]); k += 1
        assert k or f in TREES or f.startswith(('sets/', 'p17/', 'p38/', 'p43/')) or not G.PHASE2, f'noparts: {f} has no particle line to gate'
        nf += bool(k); nl += k
    nr = 0
    for r in ROOTS:
        L = F.get(r, [])
        for i, l in enumerate(L):
            m = INLINE.match(l)
            kind = SLOT_KIND(m.group(2)) if m else next((v for s, v in ROOT_LINES.items() if l.startswith(s)), None)
            if not kind or any(f'"{x}"' in l for x in EXHAUST_ITEMS): continue
            L[i] = l.replace('execute as @a[', f'execute as @a[tag=!{TAG[kind]},', 1); nr += 1
    return nf, nl, nr


# ===================================================================== the item and its menu
def generate(G):
    import phase28 as P28
    fn, title = G.fn, G.title
    say = lambda comp: title('@s', 'actionbar', comp)
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4'

    fn('np/use', ['execute if predicate bm:p20/sneaking run return run function bm:np/flip_all', 'function bm:np/open'])
    fn('np/open', [f'scoreboard players set @s bm.menu {MENU}'] +
       [f'execute if entity @s[{",".join(("tag=" if (b >> i) & 1 else "tag=!") + TAG[k] for i, (k, _, _) in enumerate(CATS))}] '
        f'run return run function bm:np/dlg/{b}' for b in range(8)])
    state = lambda off: T('OFF', 'red', bold=True) if off else T('ON', 'green', bold=True)
    for b in range(8):
        offs = [(b >> i) & 1 for i in range(3)]
        btns = [P28.btn([T(f'{nm}: ', 'white'), state(offs[i])], BTN[k],
                        tooltip=T(f'Your {what}. Press to switch them {"back on" if offs[i] else "off"}.', 'gray'))
                for i, (k, nm, what) in enumerate(CATS)]
        allw = state(True) if all(offs) else state(False) if not any(offs) else T('SOME', 'gold', bold=True)
        btns.append(P28.btn([T('Everything: ', 'white'), allw], BTN['all'],
                            tooltip=T('Every particle your own gear gives off. Press to switch them all ' +
                                      ('back on.' if all(offs) else 'off.'), 'gray')))
        d = P28.multi([T('PARTICLE TOGGLER', COL, bold=True), T('  ·  your gear\'s sparkle', 'gray')],
                      [P28.body([T('Switch off the particles your own gear gives off. ', 'gray'),
                                 T('Followers, fights and the world keep theirs.', 'dark_gray')], 300)],
                      btns, columns=2, exit_label='Done')
        fn(f'np/dlg/{b}', [f'dialog show @s {snbt(d)}'])

    # ---- the buttons (exact codes; the router checks bm.menu)
    for code in BTN.values():
        G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {code} run return run function bm:np/act')
    fn('np/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale'] +
       [f'execute if score #act bm.pay matches {BTN[k]} run function bm:np/flip_{k}' for k, _, _ in CATS] +
       [f'execute if score #act bm.pay matches {BTN["all"]} run function bm:np/flip_all', 'function bm:np/open'])
    for k, nm, _ in CATS:
        fn(f'np/flip_{k}', [f'execute if entity @s[tag={TAG[k]}] run return run function bm:np/on_{k}',
                            f'tag @s add {TAG[k]}', click, say([T(f'{nm}: ', COL, bold=True), T('particles OFF', 'red')])])
        fn(f'np/on_{k}', [f'tag @s remove {TAG[k]}', click.replace('1.4', '1.8'), say([T(f'{nm}: ', COL, bold=True), T('particles ON', 'green')])])
    every = ','.join(f'tag={t}' for t in TAG.values())
    fn('np/flip_all', [f'execute if entity @s[{every}] run return run function bm:np/on_all'] + [f'tag @s add {t}' for t in TAG.values()] +
       [click, say([T('Everything: ', COL, bold=True), T('your gear\'s particles OFF', 'red')])])
    fn('np/on_all', [f'tag @s remove {t}' for t in TAG.values()] +
       [click.replace('1.4', '1.8'), say([T('Everything: ', COL, bold=True), T('your gear\'s particles ON', 'green')])])
    G.FUNCS['admin/uninstall'][0:0] = [f'tag @a remove {t}' for t in TAG.values()]


# ===================================================================== the icon
PAL = dict(k='#2a1c0c', b='#6e4a1c', g='#b07e2c', G='#e2b446', H='#fff0a0',     # (the brass plate: dark -> lit)
           s='#4c4e5c', S='#9ea2b4',                                             # (the lever's steel stem)
           r='#8a1414', R='#e83c3c', P='#ffa0a0',                                # (its knob)
           y='#ffd23a', w='#ffffff', c='#4ad8ff', p='#ff6ad0')                   # (sparkles: gold, white hearts, cyan, pink)
ROWS = ['................',
        '..y.........rr..',
        '.ywy.......rRPr.',
        '..y........rRRr.',
        '......c....srr..',
        '.....cwc..sS....',
        '......c..sS.....',
        '........sS......',
        '..p....sS.......',
        '.pwp..sS........',
        '..p.ksSkkkk.....',
        '...kbHGGGGgbk...',
        '..kbGGgggggGbk..',
        '..kbggbbbbbgbk..',
        '...kkkkkkkkkk...',
        '................']
assert all(len(r_) == 16 for r_ in ROWS)


def icon():
    """a 16 x 16 brass toggle switch, its red-knobbed lever thrown, three sparkles (gold, cyan, pink) beside it - in sprites280's
    look (outlined, lit from the top left; gen_rp's vanilla.process finishes it)"""
    from sprites280 import S
    im = S().g(ROWS, PAL).image()
    px = im.load()
    add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
           any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in add:
        px[x, y] = (18, 14, 14, 255)
    return im


def rp(R):
    R.ICONS[ITEM] = icon()
