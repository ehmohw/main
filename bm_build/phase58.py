"""Phase 2.38: at most 3 followers, and Emma's story.

- FOLLOWERS: a player can have at most 3 companions with them at once - the Frog with Mustache, the mercenary rat,
  Cecil and Emma. Calling a fourth is refused ("send one home first"); nothing is paid for a refused call.
- EMMA'S STORY: the orphaned princess of the kingdom under the sea, who once fought the serpent king Apophiss beside
  Cecil and Sir Leo. Her lines, Cecil's hint and their little chats now tell it."""
from items import T

MAX_FOLLOWERS = 3
PINK = '#ff7ad0'


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    emsay = lambda txt: title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(txt, '#ffd0ec')])

    # ------------------------------------------------------------------ the follower cap
    HOSTS = [('wolf', 'bm.frogpet'), ('wolf', 'bm.mercpet'), ('wolf', 'bm.cecilpet'), ('cat', 'bm.emmapet')]
    fn('p58/count', ['tag @s add bm.fcme', 'scoreboard players set #fc bm.rng 0'] +
       [f'execute as @e[type=minecraft:{t},tag={tag}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1' for t, tag in HOSTS] +
       ['tag @s remove bm.fcme'])
    fn('p58/full', ['function bm:p58/count', f'execute if score #fc bm.rng matches ..{MAX_FOLLOWERS - 1} run return 0',
                    title('@s', 'actionbar', [T(f'You already have {MAX_FOLLOWERS} followers with you. ', '#ff9a5a'), T('Send one home first.', 'gray')]),
                    'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.8 0.7', 'return 1'])
    gate = 'execute if function bm:p58/full run return 0'
    G.FUNCS['p46/pet/try_summon'].insert(0, gate)                                  # Cecil
    G.FUNCS['p57/try_summon'].insert(0, gate)                                      # Emma (the ribbon)
    r = G.FUNCS['p57/enc/recruit']                                                 # recruiting her: she joins only if there's room
    k = next(i for i, l in enumerate(r) if 'run function bm:p57/summon' in l)
    r[k] = r[k].replace('run function bm:p57/summon', 'unless function bm:p58/full run function bm:p57/summon')
    h = G.FUNCS['p20/frog/hire']                                                   # the Frog: before the Medallion is taken
    k = next(i for i, l in enumerate(h) if 'clear @s' in l)
    h.insert(k, gate)
    G.FUNCS['p29/merc/first'].insert(0, gate)                                      # the mercenary rat: signing on, being called, patched, paid back
    c = G.FUNCS['p29/merc/call']
    k = next(i for i, l in enumerate(c) if 'run function bm:p29/merc/summon' in l)
    c[k] = c[k].replace('run function bm:p29/merc/summon', 'unless function bm:p58/full run function bm:p29/merc/summon')
    p = G.FUNCS['p29/merc/patch']
    k = next(i for i, l in enumerate(p) if 'bm.pay' in l or 'pay/' in l)
    p.insert(k, gate)
    pay = G.FUNCS['p29/merc/pay']
    for i, l in enumerate(pay):
        if l == 'execute if score @s bm.mstate matches 3 run function bm:p29/merc/summon':
            pay[i] = 'execute if score @s bm.mstate matches 3 unless function bm:p58/full run function bm:p29/merc/summon'

    # ------------------------------------------------------------------ Emma's story
    def swap(fname, old, new):
        L = G.FUNCS[fname]
        k = next(i for i, l in enumerate(L) if old in l)
        L[k] = new
    swap('p57/enc/talk', "I'm Emma.", emsay("Oh! H-hi! I'm Emma. I used to live under the sea, you know... now I just look at flowers. They're my favourite!"))
    r = G.FUNCS['p57/enc/recruit']
    k = next(i for i, l in enumerate(r) if "can I come with you" in l)
    r[k:k + 1] = [tellraw('@s', [T('Emma: ', PINK, bold=True), T('"Um... can I come with you? I\'m not much of a fighter... but I helped Cecil and Sir Leo '
                                                              'beat Apophiss once! I can help you too, I promise!"', '#ffd0ec')]),
                  tellraw('@s', [T('(Emma is the orphaned princess of the kingdom under the sea. Long ago she stood beside Cecil and Sir Leo '
                                   'against Apophiss, the serpent king.)', 'dark_gray', italic=True)])]
    swap('p57/hint', 'Cecil: ', tellraw('@s', [T('Cecil: ', '#b48cff', bold=True),
                                                T('"Hehehe... if you stroll through a cherry grove or a meadow on a sunny day, listen for humming. '
                                                  'The little princess who helped Leo and me against Apophiss adores flowers. She\'d be glad of a friend."', '#d8c8ff')]))
    # their chats: two more, from the old adventure
    hm = G.FUNCS['p57/harmony']
    k = next(i for i, l in enumerate(hm) if l.startswith('execute store result score #r bm.rng run random value 1..'))
    hm[k] = 'execute store result score #r bm.rng run random value 1..8'
    extra = [('Do you think Sir Leo is okay?', 'That knight? Too stubborn to fall. Hehe.'),
             ('I still dream about Apophiss sometimes...', "He's gone, little one. We saw to that."),
             ('I miss the sea, Cecil.', 'And the sea misses its princess, I would wager.')]
    k = max(i for i, l in enumerate(hm) if 'Cecil: ' in l)
    hm[k + 1:k + 1] = [f'execute if score #r bm.rng matches {6 + i} on owner run ' + title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(f'"{e}"  ', '#ffd0ec'),
                                                                                                             T('Cecil: ', '#b48cff', bold=True), T(f'"{c}"', '#d8c8ff')])
                       for i, (e, c) in enumerate(extra)]
