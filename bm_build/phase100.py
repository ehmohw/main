"""2.67: THREE TOGETHER - the follower trios (the three-follower limit, made the most of).

With three particular followers at your side at once (within 24 blocks), something more than the pairs:
THE SERPENT'S BANE - Emma, Leo and Cecil, who fought the serpent king Apophiss together: you regenerate and shrug off blows
  (Regeneration, Resistance) and a shield of absorption comes back every half minute; the three of them hit harder and heal.
THE STORM COURT - Cecil, Democratus and KillerWatt: you hit far harder and move quicker (Strength II, Speed); the three are
  tougher, and their charged attacks build faster (another charge every four seconds).
THE PRINCESS'S GUARD - Emma, Leo and Celi: two more hearts (Health Boost) and Regeneration for you; the three are tougher.
THE ODD ONES - Emma, Cecil and KillerWatt: quick on your feet and quick with your hands (Speed II, Jump Boost, Haste); the
  three heal, and Emma's charge fills faster.
Each has a hidden achievement and its own banter. (No trio in the vault: a raid allows two followers at most.)
"""
from items import T

TRIOS = {   # key: (name, colour, members, advancement title, description)
    'bane': ("The Serpent's Bane", '#e8c070', ('emma', 'leo', 'cecil'), "The Serpent's Bane", 'Walk with Emma, Leo and Cecil at once - together again'),
    'storm': ('The Storm Court', '#9ad06a', ('cecil', 'demo', 'kw'), 'The Storm Court', 'Walk with Cecil, Democratus and KillerWatt at once'),
    'guard': ("The Princess's Guard", '#9ad8ff', ('emma', 'leo', 'celi'), "The Princess's Guard", 'Walk with Emma, Leo and Celi at once'),
    'odd': ('The Odd Ones', '#ff9ad0', ('emma', 'cecil', 'kw'), 'The Odd Ones', 'Walk with Emma, Cecil and KillerWatt at once'),
}
WHO = {'emma': ('cat', 'bm.emmapet'), 'leo': ('wolf', 'bm.leopet'), 'cecil': ('wolf', 'bm.cecilpet'), 'celi': ('wolf', 'bm.celipet'),
       'kw': ('wolf', 'bm.kxpet'), 'demo': ('wolf', 'bm.dmpet')}
VOICE = {'Emma': ('#ff8ad8', '#ffd0ec'), 'Leo': ('#5ab8e0', '#d8f0ff'), 'Cecil': ('#b48cff', '#e8d8ff'), 'Celi': ('#9ad8ff', '#e0f6ff'),
         'KillerWatt': ('#74d462', '#c8f0c0'), 'Democratus': ('#7ad06a', '#e0f8d8')}
BANTER = {
    'bane': [('Emma', 'Just like old times! Sir Leo, Cecil - remember the serpent\'s den?', 'Leo', 'I remember you charging in before either of us, Princess.'),
             ('Cecil', 'Apophiss had more teeth than sense.', 'Emma', 'And you had more sparks than sense! We made a good team.'),
             ('Leo', 'Stay close, both of you. Last time I nearly lost you.', 'Cecil', 'Last time you nearly lost your helmet, knight.')],
    'storm': [('Democratus', 'A mage, a beast and a reaper. The storm keeps strange company.', 'Cecil', 'Speak for yourself, old man.'),
              ('KillerWatt', '*thunder rolls in his chest*', 'Democratus', 'Quiet. You are not the storm. You are what it left behind.'),
              ('Cecil', 'If either of you steals my kill again...', 'Democratus', 'Then be faster, boy.')],
    'guard': [('Leo', 'A princess, a knight and... whatever Celi is.', 'Celi', 'The one who actually gets things done.'),
              ('Emma', 'My two favourite grumps!', 'Celi', 'I am NOT a grump. Leo is the grump.'),
              ('Celi', 'Why do I have to guard the princess?', 'Leo', 'Because she likes you. Heaven knows why.')],
    'odd': [('Emma', "Cecil, walk on my other side. I don't want him behind me.", 'Cecil', 'Hehe... sensible. I\'d hex him myself if someone weren\'t holding his leash.'),
            ('KillerWatt', '*sparks crawl along the ground toward the hem of Cecil\'s robe*', 'Cecil', 'Touch the robe and I turn your lightning into lukewarm bathwater.'),
            ('Cecil', 'How did I end up with a princess and that... thing?', 'Emma', 'Same as me. Somebody has to keep an eye on him.')],
}


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    second = []
    objs = ['bm.trio', 'bm.triob', 'bm.trioc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pred = lambda name, eff, mn: wjson(f'bm/predicate/p100/{name}.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                          'predicate': {'minecraft:effects': {f'minecraft:{eff}': {'duration': {'min': mn}}}}})
    pred('hb', 'health_boost', 100); pred('abs', 'absorption', 1); pred('regen', 'regeneration', 1)
    # (as each player, every second) who's here?
    second.append('execute as @a[gamemode=!spectator] at @s run function bm:p100/check')
    # (whose: by the Owner link, as the follower limit counts them)
    fn('p100/is_mine', ['execute on owner if entity @s[tag=bm.trme] run return 1', 'return 0'])
    chk = ['tag @s add bm.trme']
    for k, (host, tag) in WHO.items():
        chk += [f'scoreboard players set #t_{k} bm.rng 0',
                f'execute as @e[type=minecraft:{host},tag={tag},distance=..24] if function bm:p100/is_mine run scoreboard players set #t_{k} bm.rng 1']
    chk.append('scoreboard players set #tr bm.rng 0')
    for i, (k, (nm, col, mem, at, desc)) in enumerate(TRIOS.items(), 1):
        chk.append('execute ' + ' '.join(f'if score #t_{m} bm.rng matches 1' for m in mem) + f' run scoreboard players set #tr bm.rng {i}')
    chk += ['execute unless score #tr bm.rng = @s bm.trio if score #tr bm.rng matches 1.. run function bm:p100/formed',
            'scoreboard players operation @s bm.trio = #tr bm.rng'] + \
           [f'execute if score #tr bm.rng matches {i} run function bm:p100/{k}' for i, k in enumerate(TRIOS, 1)] + ['tag @s remove bm.trme']
    fn('p100/check', chk)
    # the followers of a trio, tagged for the buffs (as the player)
    mine = lambda k: f'@e[type=minecraft:{WHO[k][0]},tag={WHO[k][1]},distance=..24]'
    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    regen = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    tick4 = ['scoreboard players add @s bm.trioc 1', 'execute if score @s bm.trioc matches 4.. run scoreboard players set @s bm.trioc 0']
    fn('p100/bane', ['effect give @s minecraft:resistance 3 0 true', regen,
                     'execute unless predicate bm:p100/abs run scoreboard players add @s bm.trioc 1',
                     'execute unless predicate bm:p100/abs if score @s bm.trioc matches 30.. run function bm:p100/bane_shield'] +
       each(TRIOS['bane'][2], 'effect give @s minecraft:strength 3 0 true') + each(TRIOS['bane'][2], regen) + ['function bm:p100/banter_tick'])
    fn('p100/bane_shield', ['scoreboard players set @s bm.trioc 0', 'effect give @s minecraft:absorption 30 1 true',
                            'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.2 20'])
    fn('p100/storm', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:speed 3 0 true'] + tick4 +
       each(TRIOS['storm'][2], 'effect give @s minecraft:resistance 3 0 true') +
       ['execute if score @s bm.trioc matches 0 as ' + mine('kw') + ' if function bm:p100/is_mine run scoreboard players add @s bm.kxch 1',
        'execute if score @s bm.trioc matches 0 as ' + mine('demo') + ' if function bm:p100/is_mine run scoreboard players add @s bm.dmch 1',
        'execute if score @s bm.trioc matches 0 as ' + mine('cecil') + ' if function bm:p100/is_mine run scoreboard players add @s bm.cpch 1',
        'execute if score @s bm.trioc matches 0 run particle minecraft:electric_spark ~ ~1 ~ 1.2 0.8 1.2 0.2 16', 'function bm:p100/banter_tick'])
    fn('p100/guard', ['execute unless predicate bm:p100/hb run effect give @s minecraft:health_boost 15 0 true', regen] +
       each(TRIOS['guard'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    fn('p100/odd', ['effect give @s minecraft:speed 3 1 true', 'effect give @s minecraft:jump_boost 3 0 true', 'effect give @s minecraft:haste 3 0 true'] +
       each(TRIOS['odd'][2], regen) + each(('emma',), 'scoreboard players add @s bm.emc 1') + ['function bm:p100/banter_tick'])
    # formed: the first time, an achievement and the story of it; every time, a flash of the trio's colour
    fm = ['playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 0.8 1.2']
    for i, (k, (nm, col, mem, at, desc)) in enumerate(TRIOS.items(), 1):
        fm.append(f'execute if score #tr bm.rng matches {i} run function bm:p100/formed_{k}')
        fn(f'p100/formed_{k}', [title('@s', 'actionbar', [T('Three together: ', 'gray'), T(nm, col, bold=True)]),
                                f'execute unless entity @s[advancements={{bm:story/trio_{k}=true}}] run function bm:p100/first_{k}'])
        fn(f'p100/first_{k}', [f'advancement grant @s only bm:story/trio_{k}',
                               tellraw('@s', PREFIX + [T(f'{nm}! ', col, bold=True), T(desc.replace('Walk with', 'With') + ' - see the README for what it gives.', 'gray')])])
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:demo_seal' if k == 'storm' else 'bm:leo_crest' if k in ('bane', 'guard') else 'bm:kw_spark'}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal', 'show_toast': True,
                                                                 'announce_to_chat': True, 'hidden': True}})
    fn('p100/formed', fm)
    # banter: every couple of minutes, one of the trio's exchanges
    line = lambda n, txt: tellraw('@s', [T(f'{n}: ', VOICE[n][0], bold=True), T(txt if n != 'KillerWatt' else txt, VOICE[n][1], italic=n == 'KillerWatt')])
    bt = ['scoreboard players add @s bm.triob 1', 'execute if score @s bm.triob matches ..120 run return 0', 'scoreboard players set @s bm.triob 0']
    # (each trio draws from its own pool - some have more to say than others)
    bt += [f'execute if score #tr bm.rng matches {i} store result score #r bm.rng run random value 1..{len(BANTER[k])}' for i, k in enumerate(TRIOS, 1)]
    for i, k in enumerate(TRIOS, 1):
        for j, (a, ta, b, tb) in enumerate(BANTER[k], 1):
            fn(f'p100/say_{k}{j}', [line(a, ta if a == 'KillerWatt' else f'"{ta}"'), line(b, tb if b == 'KillerWatt' else f'"{tb}"')])
            bt.append(f'execute if score #tr bm.rng matches {i} if score #r bm.rng matches {j} run function bm:p100/say_{k}{j}')
    fn('p100/banter_tick', bt)
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
