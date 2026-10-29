"""2.99a: HOLY BANE - the Dread is weak against the light. A blow from a HOLY weapon (anything holy: bm_angel - the Holy-forged
Regalia's blade, axe, bow and Sepulchre, the Undercrown's holy relics, whatever a Golden Cross has made holy) on a thing of the
Dread hurts it more: BONUS more (magic, past its armour) and a flare of gleaming light. The Dread: its monsters (bm.dread, the
Undercrown's own), its three bosses and their echoes, the Dread Sovereign and its eyes, the Dread Sentinels, the Dread Mire.
HOLY WARD - and holy ARMOUR (any piece worn: bm_angel) turns aside one in four of the blows that go through armour: a Stalker's
rending blow (phase181's p181/stk/hit), a Dread monster's Pulse and Mark (phase176). Light flares, the blow does nothing."""
from items import T
BONUS = 6
DREAD = ('bm.dread', 'bm.udread', 'bm.db', 'bm.dbecho', 'bm.usov', 'bm.sveye', 'bm.kh_dread', 'bm.mire')
ANGEL = '*[minecraft:custom_data~{bm_angel:1b}]'


def generate(G):
    fn = G.fn
    G.wjson('bm/advancement/p247/hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity'}}, 'rewards': {'function': 'bm:p247/hit'}})
    vic = '@e[type=!minecraft:player,distance=..12,nbt={HurtTime:10s},sort=nearest,limit=1]'
    fn('p247/hit', ['advancement revoke @s only bm:p247/hit', 'execute if entity @s[tag=bm.hbme] run return 0',
                    f'execute unless items entity @s weapon.mainhand {ANGEL} run return 0',
                    'tag @s add bm.hbme', f'execute as {vic} at @s run function bm:p247/smite', 'tag @s remove bm.hbme'])
    fn('p247/smite', ['scoreboard players set #d bm.rng 0'] +
       [f'execute if entity @s[tag={t}] run scoreboard players set #d bm.rng 1' for t in DREAD] +
       ['execute if score #d bm.rng matches 0 run return 0',
        f'damage @s {BONUS} minecraft:magic by @a[tag=bm.hbme,limit=1]',
        'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.08 14', 'particle minecraft:flash{color:[1.0,0.93,0.65,1.0]} ~ ~1 ~ 0 0 0 0 1',
        'playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    # ---- the ward: as the player about to take a blow through armour; 1 = turned aside
    fn('p247/ward', [f'execute unless items entity @s armor.* {ANGEL} run return 0',
                     'execute store result score #hw bm.rng run random value 1..4', 'execute unless score #hw bm.rng matches 1 run return 0',
                     'particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.06 24', 'particle minecraft:flash{color:[1.0,0.95,0.7,1.0]} ~ ~1 ~ 0 0 0 0 1',
                     'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.6',
                     G.title('@s', 'actionbar', T('Your holy armour turns the blow aside!', '#ffe08a', bold=True)), 'return 1'])
    for f in ('p181/stk/hit', 'p176/dread/hit_pulse', 'p176/dread/hit_mark'):
        G.FUNCS[f].insert(0, 'execute if function bm:p247/ward run return 0')
