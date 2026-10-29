"""2.99a: HOLY BANE - the Dread is weak against the light. A blow from a HOLY weapon (anything holy: bm_angel - the Holy-forged
Regalia's blade, axe, bow and Sepulchre, the Undercrown's holy relics, whatever a Golden Cross has made holy) on a thing of the
Dread hurts it more: BONUS more (magic, past its armour) and a flare of gleaming light. The Dread: its monsters (bm.dread, the
Undercrown's own), its three bosses and their echoes, the Dread Sovereign and its eyes, the Dread Sentinels, the Dread Mire."""
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
