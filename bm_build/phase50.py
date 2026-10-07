"""Phase 2.29: finding your way round the Black Market.

- THE NEWCOMERS' BOOK is rebuilt from the real trade lists every build: where each trader stands, then "who sells what"
  (names only - no prices), so it can never fall behind. Markets already in a world get the new book once.
- A BLACK MARKET ADVANCEMENT TAB: first token, first trade, the special nights, every boss, the rare finds.
- CRAFTING RECIPES for the simpler tinkering goods (in the recipe book once you've earned a token).
- SERVER SETTINGS for ops (/function bm:admin/settings): how often Blood Moons rise (or never on their own), the Block
  Breaker, the skiff's TNT bombs, and whether Black Market magic can hurt other players.
- THE GRAVE CHARM (the Fence, 10 Tokens): carry it and, when you die, your items are laid in a grave where you fell
  instead of scattering. Only you can open it (right-click). The charm goes in the grave with everything else.
- admin/help lists every admin command."""
from items import item, T, TOTEM, ITEMS
from useitem import hold
from nbt import snbt, B, F, Int

item('grave_charm', TOTEM, 'Grave Charm', '#a8b0b8',
     ['A little stone tablet on a chain.', ('Keep it anywhere in your inventory. When', 'blue'), ('you die, your items are laid in a grave', 'blue'),
      ('where you fell instead of scattering.', 'blue'), ('Only you can open it (right-click).', 'blue'), ('The charm goes in the grave too.', 'gray')],
     model='bm:grave_charm', stack=1, cat='charm')


def extend_offers(O, offer):
    O['fence'].insert(0, offer(('token', 10), ('grave_charm', 1)))


TRADERS = [  # offer key, name, where
    ('fence', 'The Fence', 'Pawn Alley (north, under the terrace)'), ('pawn', 'Old Barnaby', 'Pawn Alley'),
    ('outfitter', 'Madame Velour', 'the Plaza (centre, by the waterfall)'), ('wizard', 'Cecil the Wizard', "the Plaza, in the purple fortune teller's tent"),
    ('professor', 'Prof. Whiskerton', 'the Stacks (up on the terrace)'), ('arms', "Vinny 'Two-Blades'", 'the Forge Pit (east)'),
    ('armory', 'Sgt. Steelwhisker', 'the Forge Pit (east)'), ('chef', 'Chef Fromage', 'the Gnawed Flagon (east)'),
    ('blood', 'The Bloodbroker', 'the Blood Alcove (south-east)'), ('dock', 'Salty Sal', 'the Docks (west)'),
    ('lucky', 'Lucky Whiskers', 'the Lucky Den (across the river)'), ('captain', 'Capt. Cheddarbeard', 'behind a very small door by the docks')]
BOSSES = [('brood', 'The Broodmother', 'Into the Brood', 'minecraft:spider_eye'), ('frost', 'The Frost Marksman', 'Cold Shot', 'minecraft:blue_ice'),
          ('tide', 'The Drowned Tyrant', 'Low Tide', 'minecraft:trident'), ('hex', 'The Archmage', 'Spellbreaker', 'minecraft:enchanted_book'),
          ('keep', 'Bobbery', 'Siege Breaker', 'minecraft:tnt'), ('hollow', 'The Hollow King', 'Long Live the King', 'minecraft:netherite_helmet')]


def _name(st):
    c = st.get('components', {}).get('minecraft:custom_data')
    if c and c.get('bm') in ITEMS: return ITEMS[c['bm']]['name']
    return st['id'].split(':')[1].replace('_', ' ').title()


def guide_pages(O, zorp):
    """the trader directory and the who-sells-what index, as written-book pages (names only)"""
    H = '#6a2a8a'
    pages = [[T('NEWCOMERS,\nSTART HERE\n\n', H, bold=True), T('Welcome to the Black Market.\n\nWe trade in ', 'black'), T('Tokens', H), T(', ', 'black'),
              T('Medallions', H), T(' and ', 'black'), T('Trophies', H),
              T(' (1 Trophy = 6 Medallions = 54 Tokens). Monsters, Blood Moons, bosses and Old Barnaby pay them out.\n\nWho is where, then who sells what.', 'black')]]
    where = [(n, w) for _, n, w in TRADERS] + [('Zorp', 'aboard every Vorn mothership')]
    for i in range(0, len(where), 4):
        pg = [T('WHO IS WHERE\n\n' if i == 0 else '', H, bold=True)]
        for n, w in where[i:i + 4]: pg += [T(n, 'black', bold=True), T(f'\n {w}\n', 'dark_gray')]
        pages.append(pg)
    pages.append([T('THE BOUNTY BOARD\n', H, bold=True), T('(right here, by this book)\n\n', 'dark_gray'),
                  T('On Blood Moons, Lucky Nights and Invasion Nights it posts a bounty. Sign it to take it - one bounty a night.\n\n', 'black'),
                  T('BEHIND THE NORTH WALL: ', H, bold=True), T('the Dark Auction and the Gilded Gutter open as your ', 'black'), T('Standing', H),
                  T(' grows.\n\n- The Management', 'black')])
    sections = [(n, O.get(k, [])) for k, n, _ in TRADERS] + [('Zorp', zorp)]
    for n, offers in sections:
        names = []
        for o in offers:
            nm = _name(o['sell'])
            if nm not in names: names.append(nm)
        if not names: continue
        # pack by lines: a page holds 14 lines of about 19 characters, and a long name wraps (a page can't scroll)
        chunks, cur, used = [], [], 2
        for x in names:
            need = -(-len(f'- {x}') // 19)
            if used + need > 14 and cur: chunks.append(cur); cur, used = [], 2
            cur.append(x); used += need
        if cur: chunks.append(cur)
        for j, ch in enumerate(chunks):
            pages.append([T((n.upper() if j == 0 else n.upper() + ' (cont.)') + '\n', H, bold=True), T(''.join(f'- {x}\n' for x in ch), 'black')])
    return pages[:100]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.cfg dummy', 'bm.gdie deathCount']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    import phase24, phase32, phase35 as P35

    # ================================================================ 1) the newcomers' book, from the real trade lists
    O = G.P2_OFFERS() if hasattr(G, 'P2_OFFERS') else G.all_offers()
    zorp = [{'sell': G.stack(*s)} for _, _, s in phase24.OFFERS if s[0] not in phase32._ALTAR_MADE]
    pages = guide_pages(O, zorp)
    old_book = {'id': 'minecraft:written_book', 'count': Int(1), 'components': {'minecraft:written_book_content': {
        'title': 'Newcomers, Start Here', 'author': 'The Management', 'pages': [{'text': '', 'extra': pg} for pg in P35.GUIDE]}}}
    new_book = {'id': 'minecraft:written_book', 'count': Int(1), 'components': {'minecraft:written_book_content': {
        'title': 'Newcomers, Start Here', 'author': 'The Management', 'pages': [{'text': '', 'extra': pg} for pg in pages]}}}
    o_s, n_s = snbt(old_book), snbt(new_book)
    lect = None
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            if o_s in l:
                lines[i] = l.replace(o_s, n_s)
                if name == 'p41/patch': lect = lines[i]
    assert lect, 'the newcomers\' lectern line was not found'
    # markets already in the world: rewrite their book once
    p41 = next(l for l in G.FUNCS['loop/second'] if 'function bm:p41/patch' in l)
    second.append(p41.replace('tag=!bm.p41]', 'tag=!bm.p50]').replace('function bm:p41/patch', 'function bm:p50/book'))
    fn('p50/book', ['tag @s add bm.p50', lect])

    # ================================================================ 2) the advancement tab
    def icon(iid):
        if iid.startswith('minecraft:'): return {'id': iid}
        it = ITEMS[iid]
        return {'id': it['base'], 'components': {'minecraft:item_model': it['comps'].get('minecraft:item_model', it['base'])}}
    def adv(key, parent, ico, ttl, desc, crit, frame='task', root=False):
        d = {'display': {'icon': icon(ico), 'title': T(ttl, 'gold' if frame == 'challenge' else 'yellow'), 'description': T(desc, 'gray'),
                         'frame': frame, 'show_toast': True, 'announce_to_chat': not root, 'hidden': False}, 'criteria': crit}
        if root: d['display']['background'] = 'minecraft:gui/advancements/backgrounds/nether'
        else: d['parent'] = f'bm:story/{parent}'
        wjson(f'bm/advancement/story/{key}.json', d)
    has = lambda iid: {'got': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': ITEMS[iid]['base'],
                                                                                                   'predicates': {'minecraft:custom_data': snbt({'bm': iid})}}]}}}
    kill = lambda tag: {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}}
    granted = {'done': {'trigger': 'minecraft:impossible'}}
    adv('root', None, 'token', 'The Black Market', 'Earn your first Black Market Token', has('token'), root=True)
    adv('trade', 'root', 'minecraft:emerald', 'No Questions Asked', 'Trade with one of the market\'s traders', {'traded': {'trigger': 'minecraft:villager_trade'}})
    adv('grave', 'trade', 'grave_charm', 'Six Feet Under', 'Take your things back from your own grave', granted)
    adv('tinker', 'trade', 'tinker_wrench', 'Tinkerer', 'Place one of Prof. Whiskerton\'s tinkering blocks', granted)
    adv('cecil', 'trade', 'cecil_gem', 'A Friend in Purple', "Get Cecil's Summoning Gem", has('cecil_gem'), 'goal')
    adv('heartstone', 'root', 'heartstone', 'Change of Heart', 'Find a Heartstone', has('heartstone'))
    adv('blood_moon', 'root', 'blood_crystal', 'Red Sky at Night', 'Live to see the dawn after a Blood Moon', granted)
    adv('disc', 'blood_moon', 'music_disc_blood_moon', 'Spin the Red Record', 'Take the Blood Moon record from a steed\'s rider', has('music_disc_blood_moon'))
    adv('monstrosity', 'blood_moon', 'minecraft:ravager_spawn_egg', 'Monster Hunter', 'Slay the Blood Moon Monstrosity', kill('bm.monstrosity'), 'challenge')
    adv('eclipse', 'monstrosity', 'charm_eclipse', 'Torn from the Sky', 'Win the Blood Eclipse charm', has('charm_eclipse'), 'challenge')
    adv('lucky_night', 'root', 'lucky_token', 'Feeling Lucky', 'Live through a Lucky Night', granted)
    adv('horseman', 'lucky_night', 'minecraft:carved_pumpkin', 'Sleepy Hollow', 'Slay the Headless Horseman', kill('bm.hhm'), 'challenge')
    adv('invasion', 'root', 'xenite_green', 'Close Encounters', 'Live through an Invasion Night', granted)
    adv('skiff', 'invasion', 'skiff_key', 'Flying Saucer', 'Assemble a Vorn Skiff', has('skiff_key'), 'goal')
    adv('overseer', 'invasion', 'xenite_violet', 'Take Me to Your Leader', 'Defeat a Vorn mothership boss', kill('bm.vboss'), 'challenge')
    prev = 'root'
    for d, boss, ttl, ico in BOSSES:
        adv(f'boss_{d}', prev, ico, ttl, f'Defeat {boss}', kill(f'bm.boss_{d}'), 'challenge' if d == 'hollow' else 'goal')
        prev = f'boss_{d}'
    G.FUNCS['bloodmoon/end'].append('execute in minecraft:overworld run advancement grant @a[gamemode=!spectator,distance=0..] only bm:story/blood_moon')
    G.FUNCS['p22/lucky/end'].append('execute in minecraft:overworld run advancement grant @a[gamemode=!spectator,distance=0..] only bm:story/lucky_night')
    G.FUNCS['p32/inv/end'].append('execute in minecraft:overworld run advancement grant @a[gamemode=!spectator,distance=0..] only bm:story/invasion')
    G.FUNCS['p49/at_cell'].append('advancement grant @s only bm:story/tinker')

    # ================================================================ 3) recipes for the simpler tinkering goods (unlocked with the first token)
    RECIPES = {  # iid: (pattern, key)
        'tinker_wrench': (['  I', ' I ', 'I  '], {'I': 'minecraft:iron_ingot'}),
        'wireless_transmitter': ([' E ', 'RLR', ' R '], {'E': 'minecraft:ender_pearl', 'R': 'minecraft:redstone', 'L': 'minecraft:redstone_lamp'}),
        'wireless_receiver': ([' E ', 'RCR', ' R '], {'E': 'minecraft:ender_pearl', 'R': 'minecraft:redstone', 'C': 'minecraft:copper_block'}),
        'redstone_clock': ([' R ', 'RCR', ' R '], {'R': 'minecraft:redstone', 'C': 'minecraft:clock'}),
        'sorting_chest': ([' R ', 'RCR', ' R '], {'R': 'minecraft:comparator', 'C': 'minecraft:chest'}),
        'filter_hopper': ([' F ', 'CHC'], {'F': 'minecraft:item_frame', 'C': 'minecraft:comparator', 'H': 'minecraft:hopper'}),
        'vacuum_hopper': ([' E ', 'EHE'], {'E': 'minecraft:ender_pearl', 'H': 'minecraft:hopper'}),
        'block_breaker': (['P', 'D'], {'P': 'minecraft:iron_pickaxe', 'D': 'minecraft:dispenser'}),
        'block_placer': (['P', 'D'], {'P': 'minecraft:piston', 'D': 'minecraft:dropper'}),
        'item_compactor': ([' P ', 'PGP', ' P '], {'P': 'minecraft:piston', 'G': 'minecraft:copper_grate'}),
        'lag_lens': ([' G ', 'GSG', ' G '], {'G': 'minecraft:glass', 'S': 'minecraft:spyglass'}),
    }
    for iid, (pat, key) in RECIPES.items():
        it = ITEMS[iid]
        wjson(f'bm/recipe/{iid}.json', {'type': 'minecraft:crafting_shaped', 'category': 'redstone', 'pattern': pat, 'key': key,
                                        'result': {'id': it['base'], 'count': 1, 'components': it['comps']}})
    wjson('bm/advancement/recipes/tinkering.json', {'criteria': has('token'), 'rewards': {'recipes': [f'bm:{k}' for k in RECIPES]}})

    # ================================================================ 4) server settings
    DEF = {'#bmper': 30, '#bmoff': 0, '#breaker': 1, '#bombs': 1, '#pvp': 1}
    G.FUNCS['load'][-1:-1] = [f'execute unless score {k} bm.cfg matches -2147483648.. run scoreboard players set {k} bm.cfg {v}' for k, v in DEF.items()]
    # Blood Moon interval: the cycle length comes from #bmper; "off" stops natural ones (an Effigy still calls one)
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            if 'scoreboard players operation #cyc bm.bm %= #30 bm.bm' in l:
                lines[i] = l.replace('%= #30 bm.bm', '%= #bmper bm.cfg')
                lines[i + 1:i + 1] = ['scoreboard players operation #bmlast bm.bm = #bmper bm.cfg', 'scoreboard players remove #bmlast bm.bm 1']
            elif '#cyc bm.bm matches 29' in l:
                lines[i] = l.replace('#cyc bm.bm matches 29', '#cyc bm.bm = #bmlast bm.bm')
    tk = G.FUNCS['bloodmoon/tick']
    k = next(i for i, l in enumerate(tk) if 'run scoreboard players set #bday bm.bm 1' in l and '#cyc' in l)
    tk.insert(k + 1, 'execute if score #bmoff bm.cfg matches 1 run scoreboard players set #bday bm.bm 0')
    alm = G.FUNCS['blood/almanac']
    k = alm.index('scoreboard players set #left bm.bm 29')
    alm[k] = 'scoreboard players operation #left bm.bm = #bmlast bm.bm'
    alm.insert(k, 'execute if score #bmoff bm.cfg matches 1 run return run ' + tellraw('@s', PREFIX + [T('Blood Moons only rise when an Effigy calls one on this server.', 'gray')]))
    for i, l in enumerate(alm):
        if 'scoreboard players add #left bm.bm 30' in l: alm[i] = l.replace('scoreboard players add #left bm.bm 30', 'scoreboard players operation #left bm.bm += #bmper bm.cfg')
    G.FUNCS['p49/block_breaker/hit'].insert(0, 'execute if score #breaker bm.cfg matches 0 run return 0')
    G.FUNCS['p35/skiff/bomb'].insert(0, 'execute if score #bombs bm.cfg matches 0 run return run ' + say('The skiff\'s bomb bay is sealed on this server.', 'red'))
    # magic PvP: players carry bm.nopvp while it's off, and every Black Market spell's target list skips them
    foe = 'type=!#bm:p45_nonmob,tag=!bm.npc,tag=!bm.mcast,'
    n = 0
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            if foe in l: lines[i] = l.replace(foe, foe + 'tag=!bm.nopvp,'); n += 1
    assert n, 'no magic target lists found'
    second += ['execute if score #pvp bm.cfg matches 0 run tag @a add bm.nopvp', 'execute if score #pvp bm.cfg matches 1 run tag @a remove bm.nopvp']
    onoff = lambda key, label, desc: [tellraw('@s', [T(f'  {label}: ', 'white'), {'score': {'name': key, 'objective': 'bm.cfg'}, 'color': 'aqua'},
                                                     T('  ', 'gray'), T('[On]', 'green', click_event={'action': 'run_command', 'command': f'/function bm:admin/set/{key[1:]}_1'}),
                                                     T(' ', 'gray'), T('[Off]', 'red', click_event={'action': 'run_command', 'command': f'/function bm:admin/set/{key[1:]}_0'}),
                                                     T(f'  {desc}', 'gray')])]
    per = [tellraw('@s', [T('  Blood Moon every: ', 'white'), {'score': {'name': '#bmper', 'objective': 'bm.cfg'}, 'color': 'aqua'}, T(' days ', 'gray'),
                          T('(off: ', 'gray'), {'score': {'name': '#bmoff', 'objective': 'bm.cfg'}, 'color': 'aqua'}, T(')  ', 'gray')] +
                  sum(([T(f'[{d}]', 'yellow', click_event={'action': 'run_command', 'command': f'/function bm:admin/set/bmper_{d}'}), T(' ', 'gray')]
                       for d in (10, 20, 30, 45, 60)), []) + [T('[Never]', 'red', click_event={'action': 'run_command', 'command': '/function bm:admin/set/bmoff_1'})])]
    fn('admin/settings', [tellraw('@s', PREFIX + [T('Server settings', 'gold', bold=True), T('  (click to change; 1 = on)', 'gray')])] + per +
       onoff('#breaker', 'Block Breaker', 'breaks blocks when powered') + onoff('#bombs', 'Skiff TNT bombs', 'the skiff\'s bomb bay') +
       onoff('#pvp', 'Magic hurts players', "Cecil's staffs, bows, the Tidal Tear..."))
    for d in (10, 20, 30, 45, 60):
        fn(f'admin/set/bmper_{d}', [f'scoreboard players set #bmper bm.cfg {d}', 'scoreboard players set #bmoff bm.cfg 0', 'function bm:admin/settings'])
    fn('admin/set/bmoff_1', ['scoreboard players set #bmoff bm.cfg 1', 'function bm:admin/settings'])
    for key in ('breaker', 'bombs', 'pvp'):
        for v in (0, 1): fn(f'admin/set/{key}_{v}', [f'scoreboard players set #{key} bm.cfg {v}', 'function bm:admin/settings'])

    # ================================================================ 5) the Grave Charm
    tick.append('execute as @a[scores={bm.gdie=1..}] at @s run function bm:p50/grave/died')
    fn('p50/grave/died', ['scoreboard players reset @s bm.gdie',
                          # only the fresh drops (the charm among them) - nothing that was lying here already
                          'tag @e[type=minecraft:item,distance=..4] remove bm.gfresh',
                          'execute as @e[type=minecraft:item,distance=..4] run function bm:p50/grave/age',
                          'execute unless entity @e[type=minecraft:item,tag=bm.gfresh,distance=..4] run return 0',
                          'scoreboard players set #gc bm.rng 0',
                          'execute as @e[type=minecraft:item,tag=bm.gfresh,distance=..4] if items entity @s contents *[minecraft:custom_data~{bm:"grave_charm"}] run scoreboard players set #gc bm.rng 1',
                          'execute if score #gc bm.rng matches 0 run return run tag @e[type=minecraft:item,tag=bm.gfresh] remove bm.gfresh',
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          'execute align xyz positioned ~0.5 ~ ~0.5 run function bm:p50/grave/dig'])
    fn('p50/grave/age', ['execute store result score #a bm.rng run data get entity @s Age', 'execute if score #a bm.rng matches ..4 run tag @s add bm.gfresh'])
    stone = snbt({'Tags': ['bm.gravev', 'bm.gnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:grave3d'}},
                  'item_display': 'fixed', 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                                'translation': [F(0), F(0.5), F(0)], 'scale': [F(1)] * 3}})
    label = snbt({'Tags': ['bm.gravet', 'bm.gnew'], 'billboard': 'center', 'text': T('Grave', '#c8ccd0'), 'background': Int(0x50000000),
                  'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                     'translation': [F(0), F(1.25), F(0)], 'scale': [F(0.6)] * 3}})
    fn('p50/grave/dig', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.grave","bm.gnew"],data:{items:[]}}',
                         f'summon minecraft:item_display ~ ~ ~ {stone}', f'summon minecraft:text_display ~ ~ ~ {label}',
                         'summon minecraft:interaction ~ ~ ~ {Tags:["bm.gravehit","bm.gnew"],width:0.8f,height:1.1f,response:1b}',
                         'scoreboard players operation @e[tag=bm.gnew,distance=..1] bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:item,tag=bm.gfresh,distance=..5] run data modify entity @e[type=minecraft:marker,tag=bm.gnew,limit=1] data.items append from entity @s Item',
                         'kill @e[type=minecraft:item,tag=bm.gfresh,distance=..5]',
                         'tp @e[tag=bm.gnew,distance=..1] ~ ~ ~ ~ 0', 'tag @e[tag=bm.gnew,distance=..1] remove bm.gnew',
                         'execute store result score #gx bm.rng run data get entity @s Pos[0]', 'execute store result score #gy bm.rng run data get entity @s Pos[1]',
                         'execute store result score #gz bm.rng run data get entity @s Pos[2]',
                         'particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.02 12', 'playsound minecraft:block.gravel.place player @a[distance=..16] ~ ~ ~ 1 0.7',
                         tellraw('@s', PREFIX + [T('Your Grave Charm caught your things. ', '#a8b0b8'), T('They rest in a grave at ', 'gray'),
                                                 {'score': {'name': '#gx', 'objective': 'bm.rng'}, 'color': 'white'}, T(' ', 'gray'),
                                                 {'score': {'name': '#gy', 'objective': 'bm.rng'}, 'color': 'white'}, T(' ', 'gray'),
                                                 {'score': {'name': '#gz', 'objective': 'bm.rng'}, 'color': 'white'},
                                                 T(' - right-click it to take them back.', 'gray')])])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gravehit] if data entity @s interaction at @s run function bm:p50/grave/click')
    fn('p50/grave/click', ['scoreboard players operation #gp bm.pid = @s bm.pid', 'tag @s add bm.gme',
                           'execute on target if score @s bm.pid = #gp bm.pid run function bm:p50/grave/claim',
                           'execute on target unless score @s bm.pid = #gp bm.pid run ' + say("This grave isn't yours."),
                           'tag @s remove bm.gme', 'data remove entity @s interaction'])
    fn('p50/grave/claim', ['tag @s add bm.gowner',
                           'execute as @e[type=minecraft:interaction,tag=bm.gme,limit=1] at @s as @e[type=minecraft:marker,tag=bm.grave,distance=..0.5,limit=1] at @s run function bm:p50/grave/spill',
                           'execute as @e[type=minecraft:interaction,tag=bm.gme,limit=1] at @s run function bm:p50/grave/gone',
                           'tag @s remove bm.gowner', 'advancement grant @s only bm:story/grave', say('You take back what was yours.', '#a8b0b8'),
                           'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 0.8'])
    fn('p50/grave/spill', ['execute unless data entity @s data.items[0] run return 0',
                           'execute at @a[tag=bm.gowner,limit=1] run summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.gback"]}',
                           'data modify entity @e[type=minecraft:item,tag=bm.gback,limit=1] Item set from entity @s data.items[0]',
                           'tag @e[type=minecraft:item,tag=bm.gback] remove bm.gback', 'data remove entity @s data.items[0]', 'function bm:p50/grave/spill'])
    fn('p50/grave/gone', ['kill @e[type=minecraft:marker,tag=bm.grave,distance=..0.5]', 'kill @e[type=minecraft:item_display,tag=bm.gravev,distance=..0.5]',
                          'kill @e[type=minecraft:text_display,tag=bm.gravet,distance=..0.5]', 'particle minecraft:soul ~ ~0.8 ~ 0.3 0.4 0.3 0.02 10', 'kill @s'])

    # ================================================================ 6) admin/help: every admin command
    DESC = {'settings': 'server settings (Blood Moon interval, breaker, skiff bombs, magic PvP)', 'place_market': 'builds a Black Market at your feet',
            'place_graveyard': 'builds a graveyard + crypt at your feet', 'place_frog_hut': "builds the Frog with Mustache's swamp hut",
            'place_mothership': 'puts a Vorn mothership overhead', 'place_crash_site': 'a crashed saucer at your feet', 'place_dreadnought': 'a Vorn dreadnought',
            'invasion_now': 'starts an Invasion Night', 'invasion_stop': 'ends it', 'lucky_night': 'starts a Lucky Night', 'auction_now': 'opens the Dark Auction',
            'auction_stop': 'closes it', 'bank_interest_on': 'bank interest on', 'bank_interest_off': 'bank interest off', 'horseman': 'summons the Headless Horseman',
            'spawn_monstrosity': 'the Blood Moon Monstrosity', 'uninstall': 'stops every loop before you remove the pack', 'bounty_test': 'posts a test bounty',
            'shrine': 'places a shrine', 'void_rat': 'summons the Void Rat', 'ember_rat': 'summons the Ember Rat', 'horseman_heads': "gives the Horseman's Heads"}
    def make_help():
        names = sorted(k[6:] for k in G.FUNCS if k.startswith('admin/') and '/' not in k[6:] and k not in ('admin/help',))
        cats = sorted({k.split('/')[2] for k in G.FUNCS if k.startswith('admin/give/') and k.count('/') == 2})
        lines = [tellraw('@s', PREFIX + [T('Admin commands', 'gold', bold=True), T('  (click to fill in)', 'gray')]),
                 tellraw('@s', [T('/function bm:admin/give/<category>', 'yellow'), T('  ' + ', '.join(cats), 'gray')])]
        for n in names:
            lines.append(tellraw('@s', [T(f'/function bm:admin/{n}', 'yellow', click_event={'action': 'suggest_command', 'command': f'/function bm:admin/{n}'}),
                                        T(('  ' + DESC[n]) if n in DESC else '', 'gray')]))
        for sub in ('p2', 'rare'):
            subs = sorted(k[len(f'admin/{sub}/'):] for k in G.FUNCS if k.startswith(f'admin/{sub}/') and k.count('/') == 2)
            if subs: lines.append(tellraw('@s', [T(f'/function bm:admin/{sub}/...', 'yellow'), T('  ' + ', '.join(subs), 'gray')]))
        lines.append(tellraw('@s', [T('/locate structure bm:black_market', 'yellow'), T('  (also bm:graveyard, bm:frog_hut)', 'gray')]))
        return lines
    G.HELP_BUILDER = make_help                      # (built last, once every phase has added its commands - see gen_dp)

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the charm icon and the gravestone
def icons():
    import vanilla as v
    from PIL import Image

    def charm():
        im = Image.new('RGBA', (16, 16)); s = v.ramp('#9aa2aa', 5, 2); k = v._hex('#2a2e34'); ch = v.ramp('#c9b26a', 3, 1)
        rows = ['................', '.......cc.......', '......c..c......', '......c..c......', '.......cc.......', '.....KKKKKK.....',
                '....KsssssLK....', '....KssXssLK....', '....KsXXXsLK....', '....KssXssLK....', '....KssXssdK....', '....KssssddK....',
                '....KsssdddK....', '....KKKKKKKK....', '................', '................']
        pal = {'K': k, 's': s[2], 'L': s[3], 'X': s[0], 'd': s[1], 'c': ch[1]}
        for y, r in enumerate(rows):
            for x, c in enumerate(r):
                if c != '.': im.putpixel((x, y), pal[c])
        return im
    return {'grave_charm': charm}


def rp(R):
    import vanilla
    from PIL import Image
    for k, f in icons().items():
        R.ICONS[k] = Image.new('RGBA', (16, 16))
        vanilla.OVERRIDES[k] = f
    c = R.cube
    t = {'s': 'minecraft:block/stone_bricks', 'm': 'minecraft:block/mossy_stone_bricks', 'd': 'minecraft:block/coarse_dirt', 'c': 'minecraft:block/chiseled_stone_bricks'}
    R.HATS['grave3d'] = (t, [c((2, 0, 2), (14, 1, 14), 'd'), c((4, 1, 6.5), (12, 11, 9.5), 's'), c((5, 11, 6.5), (11, 12.5, 9.5), 'm'),
                             c((7.3, 5, 6.3), (8.7, 10, 6.5), 'c'), c((6, 7.6, 6.3), (10, 9, 6.5), 'c')])
    R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + ('grave3d',)
