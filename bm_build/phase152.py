"""Phase 152 (2.80): BOSS THEMES - every boss fight gets music of its own, and the vault opens to a fanfare.

- Twelve synthesised loops (tools/boss_music.py -> vendor/boss_*.ogg), one per kind of fight: the Wild Hunt (Horseman,
  Treant), Sands of the Dead (Pharaoh, Roc), the Abyss (Colossus, Voidwalker), Into the Depths (the dungeon bosses), the
  Hollow King and his Unbound form, Apophiss and the Serpent Risen, Stormborn (KillerWatt, Democratus's duel), the Drowned
  Captain (Tullius), Blood Moon (the Arachno-Lantern) and Mothership (the Vorn bosses).
- Each player hears the theme of the strongest boss within 64 blocks (a second form outranks the first; Apophiss outranks
  everyone). It keeps playing while that boss is within 96 - so a step back doesn't restart it - and stops the moment the
  boss begins to die (a staged death plays in silence) or is gone. Apophiss's transformation is silent too: the Serpent
  Risen comes in with his second form.
- The themes play on the jukebox channel ('record'), so the vanilla soundtrack is held off while one plays and the heist's
  own music is never touched (no theme plays in the vault). They replace the vanilla records the roaming bosses used.
- The vault: the door's opening silences the heist's music for eleven seconds, and the fanfare plays as the last column
  of gold parts.

Importing does nothing; generate(G) runs last of the boss phases (it reads the staged roaming bosses' functions)."""
import re

THEMES = {1: ('hunt', 60), 2: ('sands', 60), 3: ('abyss', 60), 4: ('dungeon', 60), 5: ('hollow', 64), 6: ('hollow2', 60), 7: ('serpent', 64),
          8: ('serpent2', 64), 9: ('storm', 60), 10: ('tide', 60), 11: ('blood', 60), 12: ('vorn', 60)}
ENTER, KEEP = 64, 96
# (theme, boss) - in rising priority: when two are near, the later line wins
WHO = [(1, 'type=minecraft:wither_skeleton,tag=bm.hhm'), (1, 'type=minecraft:creaking,tag=bm.trt'),
       (2, 'type=minecraft:husk,tag=bm.sph'), (2, 'type=minecraft:phantom,tag=bm.roc'),
       (3, 'type=minecraft:magma_cube,tag=bm.mcol'), (3, 'type=minecraft:enderman,tag=bm.vwk')]
WHO_LATE = [(12, 'tag=bm.vboss'), (9, 'type=minecraft:husk,tag=bm.kxboss'), (9, 'type=minecraft:vindicator,tag=bm.dmboss'),
            (10, 'type=minecraft:husk,tag=bm.tuboss'), (11, 'type=minecraft:giant,tag=bm.salboss'),
            (5, 'type=minecraft:wither_skeleton,tag=bm.boss_hollow'), (6, 'type=minecraft:wither,tag=bm.boss_hollow'),
            (7, 'type=minecraft:husk,tag=bm.apboss,scores={bm.apph=..1,bm.apatk=..6}'),       # (not while he transforms: a=7)
            (7, 'type=minecraft:husk,tag=bm.apboss,scores={bm.apph=..1,bm.apatk=8..}'),
            (8, 'type=minecraft:husk,tag=bm.apboss,scores={bm.apph=2}')]
STINGS = []                         # (2.94h: short music laid over a theme - phase197's Dread stings; registered as music.boss_<name>)
OLD_SONGS = ('music_disc.13', 'music_disc.relic', 'music_disc.precipice', 'music_disc.mellohi', 'music_disc.pigstep', 'music_disc.5')


def who(G):
    out = list(WHO)
    if G.PHASE2:
        import phase150
        out += [(4, f'type=minecraft:{ent},tag=bm.boss_{dn}') for dn, (ent, *_r) in phase150.DG.items() if dn != 'hollow']
    return out + WHO_LATE


def sel(body, r):
    return f'@e[{body},tag=!bm.cdie,distance=..{r}]'


def generate(G):
    fn = G.fn
    W = who(G)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.bmt dummy', 'scoreboard objectives add bm.bmu dummy', 'scoreboard objectives add bm.bmf dummy']
    G.OBJECTIVES += ['bm.bmt', 'bm.bmu', 'bm.bmf']

    # ---- the old records out (the roaming bosses' vanilla discs, and the 'stop every record' that went with them)
    pat = re.compile(r'minecraft:(' + '|'.join(re.escape(s) for s in OLD_SONGS) + r')\b')
    hits = 0
    for name, lines in G.FUNCS.items():
        if name.startswith('p45/'):                     # (the boombox plays every disc - it keeps them)
            continue
        keep = []
        for l in lines:
            if pat.search(l) and (l.startswith(('playsound ', 'stopsound ')) or ' run stopsound ' in l):
                hits += 1; continue
            if l == 'stopsound @s record' and (name.endswith('/sense') or name.endswith('/heard')):
                hits += 1; continue
            if re.match(r'execute if score @s bm\.cdt matches 1 run stopsound @a\[tag=bm\.[a-z]+sensed\] record$', l):
                hits += 1; continue
            keep.append(l)
        G.FUNCS[name] = keep
    assert hits >= 20, hits

    # ---- each player, each second: which theme, if any
    G.FUNCS['loop/second'] += ['execute as @a at @s unless dimension bm:gutter run function bm:p152/tick',
                               'execute as @a[scores={bm.bmt=1..}] at @s if dimension bm:gutter run function bm:p152/stop']
    fn('p152/tick', ['scoreboard players set #bt bm.rng 0'] +
       [f'execute if entity {sel(b, ENTER)} run scoreboard players set #bt bm.rng {t}' for t, b in W] +
       ['execute if score #bt bm.rng = @s bm.bmt run return run function bm:p152/keep',
        'execute if score #bt bm.rng matches 0 if function bm:p152/near run return run function bm:p152/keep',
        'function bm:p152/stop',
        'scoreboard players operation @s bm.bmt = #bt bm.rng',
        'execute if score @s bm.bmt matches 1.. run function bm:p152/play'])
    # (its boss still within 96: carry on)
    fn('p152/near', [f'execute if score @s bm.bmt matches {t} if entity {sel(b, KEEP)} run return 1' for t, b in W] + ['return 0'])
    fn('p152/keep', ['execute unless score @s bm.bmt matches 1.. run return 0', 'stopsound @s music', 'scoreboard players remove @s bm.bmu 1',
                     'execute unless score @s bm.bmu matches 1.. run function bm:p152/play'])
    fn('p152/play', ['stopsound @s music'] +
       [f'execute if score @s bm.bmt matches {t} run return run function bm:p152/p{t}' for t in THEMES])
    for t, (nm, ln) in THEMES.items():
        fn(f'p152/p{t}', [f'playsound bm:music.boss_{nm} record @s ~ ~ ~ 1000 1 1', f'scoreboard players set @s bm.bmu {ln}'])
    fn('p152/stop', [f'execute if score @s bm.bmt matches {t} run stopsound @s record bm:music.boss_{nm}' for t, (nm, _l) in THEMES.items()] +
       ['scoreboard players set @s bm.bmt 0', 'scoreboard players set @s bm.bmu 0'])
    G.FUNCS['p104/login'] += ['scoreboard players set @s bm.bmt 0', 'scoreboard players set @s bm.bmu 0']
    G.FUNCS['admin/uninstall'][0:0] = [f'stopsound @a record bm:music.boss_{nm}' for nm, _l in THEMES.values()]

    # ---- the vault's fanfare: the heist's music holds its breath while the door parts, then the fanfare
    if 'cine/vault/door' in G.FUNCS:
        G.FUNCS['p75/mus/tick'][0:0] = ['execute if score @s bm.bmf matches 1.. run scoreboard players set @s bm.gvmz 99',
                                         'execute if score @s bm.bmf matches 1.. run scoreboard players remove @s bm.bmf 1']
        door = G.FUNCS['cine/vault/door']
        door.insert(1, 'execute if score @s bm.cvt matches 1 run stopsound @a[tag=bm.gvp,distance=..64] music')
        door.insert(1, 'execute if score @s bm.cvt matches 1 run scoreboard players set @a[tag=bm.gvp,distance=..64] bm.bmf 11')
        door.insert(1, 'execute if score @s bm.cvt matches 36 run playsound bm:music.boss_vault record @a[tag=bm.gvp,distance=..64] ~ ~ ~ 1000 1 1')
        G.FUNCS['p70/unraid'] += ['stopsound @s record bm:music.boss_vault', 'scoreboard players reset @s bm.bmf']


def rp(R):
    import os, shutil
    here = os.path.dirname(os.path.abspath(__file__))
    def post(R2):
        import json
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'music'), exist_ok=True)
        for nm in [v[0] for v in THEMES.values()] + ['vault'] + STINGS:
            shutil.copy(os.path.join(here, 'vendor', f'boss_{nm}.ogg'), R2.p('assets', 'bm', 'sounds', 'music', f'boss_{nm}.ogg'))
            snd[f'music.boss_{nm}'] = {'sounds': [{'name': f'bm:music/boss_{nm}', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)
