"""2.94t: SHINY FOLLOWERS - finding them (the looks themselves: shiny.py).

NOW AND THEN, CALLED: one summon in shiny.SHINY_ODDS, a follower turns up TRYING SOMETHING NEW TODAY - in their shiny colours,
  with a burst of sparkles and a word about it ("I'm trying something new today - what do you think?"). The look goes in
  their wardrobe for good (as a cosmetic used would), and they're wearing it now; change back any time from their menu.
  A follower whose shiny look you already have rolls no more. Never sold: the Tailor and Goldtooth don't stock them.
WEARING IT: a shiny follower glitters - a few gold motes about them, now and then a star - whatever else they wear.
THE GALLERY: a follower whose shiny look you have shows a gold star by their name.
(/function bm:admin/shiny_next: your next summon is a shiny one, for whichever follower you call.)"""
from items import T
import shiny

GOLD = '#ffd84a'
# what each says, turning up in it (one line, in their own voice)
SAY = {
    'emma': "I'm trying something new today! Lilac! Do you love it? You love it.",
    'celi': "Don't stare. I'm trying something new today. ...It's pink. Say one word and I'll freeze you.",
    'zib': 'Trying something new today, Earthling. Magenta is very fashionable on my planet.',
    'cecil': "I'm trying something new today. Orange. Apparently wizards are allowed to have fun.",
    'kw': '*crackles in a colour he has never been before - he is trying something new today*',
    'leo': "I'm trying something new today, my liege. Rose-gold. A knight may be dashing, may he not?",
    'demo': 'I am trying something new today. Do not make it a thing.',
    'apo': 'I am trying something new today. White scales. KNEEL before my elegance.',
    'tul': "Tryin' something new today. Sea glass. The ocean's colour, the way I remember her.",
    'frog': 'Trying something new today. Pink. A professional can pull off anything.',
    'don': "I am trying something new today! Strawberry! Zib says it's 'a lot'.",
    'pearl': 'Trying something new today, my friend! Magenta - and for you, a discount on compliments!',
    'fishy': '(he tips a silver hat - he is trying something new today, and he is delighted with it)',
    'wil': "I'm trying something new today - a new device on my shield. Do you like the flowers?",
    'dennis': 'Tryin\' somethin\' new today. Blue. Don\'t tell the lads at the mine.',
    'pistachio': 'I am trying something new today, sir. Rose. One mustn\'t haunt in the same coat for three centuries.',
    'omega': 'I am trying something new today! Ember! The dead adore a bold colour!',
    'ashur': "Trying something new today! PINK fire! Hotter, right? It's hotter.",
    'chef': "I am trying something new today! Mint! Fresh, like my soup!",
    'neighbor': "Trying something new today! A sunshine suit - every song sounds happier in yellow!",
    'ava': "I'm trying something new today, darling. Rose. It's been a thousand years - I'm allowed.",
    'pearlq': "I'm trying something new today! Mint! It goes with cake. Everything goes with cake.",
    'bloo': '...I am trying something new today. It is pink. If you laugh, I will eat you.',
    'stalker': '(it is trying something new today. It is very green. It stands very still, waiting to see if you noticed.)',
    'lantern': '(its rind glows moon-blue - it is trying something new today, and it scuttles a proud little circle)',
    'bender': '(he is trying something new today - blue merle - and he will NOT stop showing you)',
    'bones': '(he is trying something new today: tiger stripes. The grin is even bigger.)',
    'capshun': '"[He was trying something new today. Purple. A bold choice, for a stick.]"',
    'gem': '(the Gem is trying something new today: every colour at once, twice as bright. ^-^)',
    'batty': '"New look, who dis. ...Golden wings. Don\'t make it weird."',
    'eggbert': '"Ooze of a different colour today. Fancy, eh?"',
    'count': '"A gentleman refreshes his wardrobe. Silver, today. Do try to keep up."',
    'dragon': '"I\'m trying something new today! Kettle used ALL the crayons on me! ALL OF THEM!"',
    'eraser': '"I\'m... trying something new today. Glitter. Is it too much? It\'s too much. Sorry."',
    'cursor': '"Trying something new today: GOLD pointer! Like a high score!"',
    'inkblot': "(it's trying something new today: it's full of stars, and very pleased about it)",
    'speech': '"TRYING SOMETHING NEW TODAY! In FULL COLOUR! KA-POW!"',
    'lightbringer': '"I am trying something new today - starlight. The Divine One said it suits me."',
    'dryad': '"I\'m trying something new today! My cap glows like the moon!"',
    'henry': '(he is trying something new today: a sparkly starlit collar. He is very handsome and he knows it.)',
    'nia': '(she is trying something new today: a shimmering rainbow collar, and her bell sounds like starlight)',
    'rufus': '"Gold bandana today. Don\'t look at me like that - a rat can treat himself."',
    'kettle': '"Look! I\'m PINK today! Pink is the best colour. Until tomorrow."',
    'sky': 'Sunny: "We\'re trying something new today! Sherbet! Nimbus picked it." Nimbus: ":3"',
    'pxemma': "I'm trying something new today! NEON! Like the arcade at night!",
    'pxleo': 'Trying something new today! The arcade palette - for honour, and for style!',
    'pxcecil': 'I am trying something new today. Neon. Sixteen colours, and every one of them loud.',
}


def generate(G):
    import phase99 as P99, phase125 as P125, phase138 as P138, phase179 as P179
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.shnext dummy']
    G.OBJECTIVES.append('bm.shnext')
    assert set(SAY) == set(shiny.KEY), set(SAY) ^ set(shiny.KEY)
    # each follower's shiny look in the wardrobe's own terms: (group, current-look score, unlocked bits, apply)
    look = {}
    for who, g, cur, un, ks, iid, off, apply in P99.groups():
        if who in shiny.KEY and shiny.KEY[who] in ks and iid.format(shiny.KEY[who]) == shiny.item_of(who):
            look[who] = (g, cur, un, apply)
    assert set(look) == set(shiny.KEY), set(shiny.KEY) - set(look)
    # (each follower's "here they are" - run as you, where they appear)
    kind = {P125.WHO[w][4].split(',')[0]: w for w in P125.WHO}
    summon = {kind[tag]: e[7] for tag, e in P179.FOLLOW.items() if tag in kind}
    summon['wil'] = 'p2/wil/summon'
    assert set(summon) >= set(shiny.KEY), set(shiny.KEY) - set(summon)
    owns = lambda w: ['scoreboard players set #q bm.rng 0', f'scoreboard players operation #q bm.rng = @s {look[w][2]}', f'scoreboard players set #bit bm.rng {2 ** shiny.KEY[w]}',
                      'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    for w, k in shiny.KEY.items():
        g, cur, un, apply = look[w]
        nm, col = P125.WHO[w][0], P125.WHO[w][2]
        cap = nm[0].upper() + nm[1:]
        lname = shiny.LOOKS[w][0] if w in shiny.LOOKS else {'kw': shiny.KW, 'emma': shiny.EMMA, 'celi': shiny.CELI, 'zib': shiny.ZIB}[w][0]
        G.FUNCS[summon[w]].append(f'function bm:p221/roll/{w}')
        fn(f'p221/roll/{w}', [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0'] + owns(w) +
           ['execute if score #q bm.rng matches 1 run return 0',
            f'execute if score @s bm.shnext matches 1.. run return run function bm:p221/hit/{w}',
            f'execute store result score #sh bm.rng run random value 1..{shiny.SHINY_ODDS}',
            f'execute if score #sh bm.rng matches 1 run function bm:p221/hit/{w}'])
        fn(f'p221/hit/{w}', ['scoreboard players reset @s bm.shnext',
                             f'function bm:p99/unlock/{g}{k}', f'scoreboard players set @s {cur} {k}', f'function bm:{apply}',
                             'particle minecraft:end_rod ~ ~1.2 ~ 0.7 0.9 0.7 0.06 50', 'particle minecraft:firework ~ ~1.2 ~ 0.5 0.8 0.5 0.12 40',
                             'particle minecraft:wax_on ~ ~1.2 ~ 0.8 1 0.8 0 30',
                             'playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.6',
                             'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.8',
                             'title @s times 5 50 15', title('@s', 'subtitle', T(f'{cap} is trying something new today', col)),
                             title('@s', 'title', T('✦ Shiny! ✦', GOLD, bold=True)),
                             tellraw('@s', [T(f'{cap}: ', col, bold=True), T(SAY[w], 'white')]),
                             tellraw('@s', PREFIX + [T('✦ ', GOLD), T(lname, GOLD, bold=True),
                                                     T(' - a shiny look, found only like this. It\'s in their wardrobe for good.', 'gray')])])
    # ---- wearing it: they glitter (as phase147's metal looks sparkle: every 5 ticks, at the host, for its owner's look)
    fast = G.FUNCS['loop/fast']
    for w, k in shiny.KEY.items():
        if w not in P138.HOST: continue
        host_t, host_tag = P138.HOST[w]
        _n, _c, h, r = P138.AURA[w][:4]
        cur = look[w][1]
        fast.append(f'execute as @e[type=minecraft:{host_t},tag={host_tag}] at @s on owner if score @s {cur} matches {k} run function bm:p221/sp/{w}')
        fn(f'p221/sp/{w}', [f'particle minecraft:dust{{color:[1.0,0.86,0.3],scale:0.6}} ~ ~{h:.2f} ~ {r:.2f} {h * 0.55:.2f} {r:.2f} 0 1',
                            f'execute if predicate bm:p147/third run particle minecraft:end_rod ~ ~{h + 0.2:.2f} ~ {r * 0.8:.2f} {h * 0.4:.2f} {r * 0.8:.2f} 0.01 1'])
    # ---- the Gallery: a gold star by a name whose shiny look you have
    op = G.FUNCS['p220/open']
    for w, k in shiny.KEY.items():
        j = next(i for i, l in enumerate(op) if l.startswith('execute if entity @s[advancements=') and 'gal.r_gal append' in l and f'#{list(P125.WHO).index(w) + 1:02d} ' in l)
        op[j + 1:j + 1] = owns(w) + ['execute if score #q bm.rng matches 1 run data modify storage bm:tmp gal.r_gal append value {text:"✦  ",color:"#ffd84a"}']
    fn('admin/shiny_next', ['scoreboard players set @s bm.shnext 1', tellraw('@s', PREFIX + [T('Your next summon is a shiny one.', GOLD)])])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/shiny_next', 'yellow'), T('  your next summon turns up shiny (trying something new today)', 'gray')])]
