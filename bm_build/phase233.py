"""2.98: THE CREATIVE FORMS - a pair with the Gem of Creativity (phase231) for every Buddy, and five more: when one walks beside the Gem
it takes on a CREATIVE FORM - it sparkles with the Gem's colours, and the two of them give you something nobody else does.
The Buddies (the Gem made them all): Fishy, the Gutter Gentry (Batty, Eggbert, the Count), Mr. Capshun, the Sky Buddies, Kettle.
And the owner's five: Emma, Queen Ava, Democratus, KillerWatt and Queen Pearl.
(phase188 runs the pairs: the Gem's host leads every one.)
2.96a: and the form is an OUTFIT, not only a sparkle - each of them puts on their creative outfit (creative.py: a beret, a smock,
a rainbow cape, a crown of crayons...) the moment the pair forms, and takes it off again (back to whatever they wore) a few seconds after they part.
It's a flag on their parts beside whatever they wear, so it goes over every look, pose and face, and a part that stops being dressed
(the pair parted, the Gem sent home, a logout) is itself again a second later.)"""
import phase188 as P188
_O = P188.O
_SP = '{B} at @s run particle minecraft:end_rod ~ ~1 ~ 0.4 0.5 0.4 0.02 3'
_RB = lambda c: '{B} at @s run particle minecraft:dust{color:[' + c + '],scale:1.1} ~ ~1 ~ 0.5 0.6 0.5 0 4'
# who: (form name, its colours (r,g,b for the sparkle), the buff [as the Gem, the player tagged], intro (who, line) x2)
FORMS = {
    'fishy': ('Creative Form: Rainbow Fin', '1.0,0.6,0.2', [f'effect give {_O} minecraft:dolphins_grace 3 0 true', f'effect give {_O} minecraft:conduit_power 3 0 true', f'effect give {_O} minecraft:luck 3 0 true'],
              [('fishy', '"Good heavens - my scales! They\'re every colour at once!"'), ('gem', '(the Gem sparkles: ^-^)')]),
    'batty': ('Creative Form: Prism Wings', '0.6,0.5,1.0', [f'effect give {_O} minecraft:night_vision 15 0 true', f'effect give {_O} minecraft:slow_falling 3 0 true', f'effect give {_O} minecraft:speed 3 1 true'],
              [('gem', '(the Gem looks at Batty a long time: :c ... then: c:)'), ('batty', '"...You\'re not mad? Even after everything? ...Thanks, Gem."')]),
    'eggbert': ('Creative Form: Golden Yolk', '1.0,0.85,0.3', [f'effect give {_O} minecraft:absorption 3 1 true', f'effect give {_O} minecraft:resistance 3 0 true'],
                [('eggbert', '"My shell - it\'s shining. Gold. Like when I was new."'), ('gem', '(the Gem glows warmly: <3)')]),
    'count': ('Creative Form: Starlit Gentleman', '0.6,0.8,1.0', [f'effect give {_O} minecraft:strength 3 1 true', f'effect give {_O} minecraft:luck 3 0 true'],
              [('count', '"Ah. Our maker. I... owe you an apology, I think."'), ('gem', '(the Gem dips, like a bow: :) )')]),
    'capshun': ('Creative Form: Full Colour', '1.0,0.4,0.7', [f'effect give {_O} minecraft:haste 3 1 true', f'effect give {_O} minecraft:strength 3 0 true'],
                [('capshun', '"[Mr. Capshun narrates: \'And for the first time, he was drawn in FULL COLOUR.\'] ...Is this canon?"'), ('gem', '(the Gem: :D)')]),
    'sky': ('Creative Form: Aurora', '0.5,1.0,0.8', [f'effect give {_O} minecraft:slow_falling 3 0 true', f'effect give {_O} minecraft:jump_boost 3 1 true', f'effect give {_O} minecraft:regeneration 3 0 true'],
            [('sky', 'Sunny: "We\'re an AURORA!" Nimbus: ":3" Twinkle: "Ooooh."'), ('gem', '(the Gem: :3)')]),
    'kettle': ('Creative Form: First Sketch', '0.55,0.85,1.0', [f'effect give {_O} minecraft:speed 3 1 true', f'effect give {_O} minecraft:jump_boost 3 1 true', f'effect give {_O} minecraft:luck 3 0 true'],
               [('kettle', '"GEM! Look! I\'m all sparkly! Like when you first drew me!"'), ('gem', '(the Gem spins round and round: ^-^)')]),
    'emma': ('Creative Form: Dream Petals', '1.0,0.6,0.85', [f'effect give {_O} minecraft:regeneration 3 1 true', f'effect give {_O} minecraft:speed 3 0 true'],
             [('emma', '"My petals are glittering! Gem, did you do that?"'), ('gem', '(the Gem: c:)')]),
    'ava': ('Creative Form: Living Tide', '0.4,0.85,0.95', [f'effect give {_O} minecraft:water_breathing 3 0 true', f'effect give {_O} minecraft:dolphins_grace 3 0 true', f'effect give {_O} minecraft:regeneration 3 0 true'],
            [('ava', '"The water remembers colour, little gem. Thank you."'), ('gem', '(the Gem: o3o)')]),
    'demo': ('Creative Form: Painted Reaper', '0.5,0.9,0.4', [f'effect give {_O} minecraft:strength 3 1 true', f'effect give {_O} minecraft:night_vision 15 0 true'],
             [('demo', '"...I am sparkling. The Reaper does not sparkle. ...Leave it on."'), ('gem', '(the Gem: :3)')]),
    'kw': ('Creative Form: Rainbow Current', '1.0,0.9,0.25', [f'effect give {_O} minecraft:speed 3 2 true', f'effect give {_O} minecraft:haste 3 0 true'],
           [('kw', '"...Colour, running through my current. Bright. Fragile. I want all of it."'), ('gem', '(the Gem flickers, uneasy: o.o)')]),   # (3.0e: in character - the parasite, not a cheerful spark)
    'pearlq': ('Creative Form: Pearlescent', '0.9,0.95,1.0', [f'effect give {_O} minecraft:luck 3 1 true', f'effect give {_O} minecraft:absorption 3 0 true'],
               [('pearlq', '"Pearlescent! Oh, it suits me. It REALLY suits me."'), ('gem', '(the Gem: ^-^)')]),
}


def add_pairs():
    """(after every follower is imported)"""
    import phase100 as P100
    for w, (nm, col, buff, intro) in FORMS.items():
        if w not in P100.WHO: continue
        P188.PAIRS[f'cf_{w}'] = ('gem', w, nm, '#5ae0a0', f'The Gem of Creativity and {P188.VNAME.get(w, w)} - a creative form', buff + [_SP, _RB(col)], intro,
                                 [('gem', '(the Gem sparkles at them: :D)', w, '"Gem! Look at me go!"' if w in ('kettle', 'emma') else
                                  '"Keep shining, little stone. I\'ll take everything you give."' if w == 'kw' else '"...Thank you."')])
        P188.ICON[f'cf_{w}'] = 'bm:creativity_gem'
        P188.PAIRS[f'cf_{w}'][5].append(f'execute as {_O} at @s run function bm:p233/on/{w}')
    P188.PAIRS['cf_bender'] = ('gem', 'bender', 'Fetch the Rainbow', '#e0a860', 'The Gem of Creativity and Bender - he chases its sparkles, forever',
                               [f'effect give {_O} minecraft:speed 3 1 true', f'effect give {_O} minecraft:luck 3 0 true', _SP],
                               [('bender', '(chases the Gem\'s sparkles round and round)'), ('gem', '(the Gem makes more sparkles: :3)')],
                               [('bender', '(catches a sparkle; it tickles)', 'gem', '(the Gem: ^-^)')])
    P188.ICON['cf_bender'] = 'bm:creativity_gem'


def generate(G):
    """(2.96a) the creative outfit: while the pair runs, the outfit flag raised on every part of the partner (creative.py: each part's
    item definition then shows its outfitted twin), kept up a few times a second; lowered (their own look) when they part"""
    import phase100 as P100
    import creative
    fn = G.fn
    assert set(FORMS) == set(creative.FORMS), set(FORMS) ^ set(creative.FORMS)
    objs = [f'bm.cf{w}' for w in FORMS] + ['bm.cfu']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    fast, sec = G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    for w in FORMS:
        host, tag = P100.WHO[w]
        # (the pair, each second, as you: in form for three seconds more)
        fn(f'p233/on/{w}', [f'execute unless score @s bm.cf{w} matches 1.. run playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 1.4',
                            f'scoreboard players set @s bm.cf{w} 3'])
        sec.append(f'execute as @a[scores={{bm.cf{w}=1..}}] run scoreboard players remove @s bm.cf{w} 1')
        # (a few times a second: your partner's parts - every display about them - wear the outfit)
        fast.append(f'execute as @a[scores={{bm.cf{w}=1..}}] at @s run function bm:p233/paint/{w}')
        fn(f'p233/paint/{w}', ['scoreboard players operation #me bm.pid = @s bm.pid',
                               f'execute as @e[type=minecraft:{host},tag={tag},distance=..32] if score @s bm.pid = #me bm.pid at @s '
                               f'as @e[type=minecraft:item_display,distance=..3.5,tag=!bm.cgp] run function bm:p233/part'])
    fn('p233/part', ['tag @s add bm.cft', 'execute store result score @s bm.cfu run time query gametime',
                     'data modify entity @s item.components."minecraft:custom_model_data".flags set value [1b]'])
    # (and a part not dressed for a second - the pair parted, or it wandered off - is itself again)
    sec.append('execute store result score #now bm.rng run time query gametime')
    sec.append('execute as @e[type=minecraft:item_display,tag=bm.cft] run function bm:p233/fade')
    fn('p233/fade', ['scoreboard players operation #age bm.rng = #now bm.rng', 'scoreboard players operation #age bm.rng -= @s bm.cfu',
                     'execute if score #age bm.rng matches ..20 run return 0',
                     'data remove entity @s item.components."minecraft:custom_model_data".flags', 'tag @s remove bm.cft'])
