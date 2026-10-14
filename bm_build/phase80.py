"""2.66: THE FIXER'S OFFICE - the vault's spoils, the Gutter Bank, and loaner kits that grow with you.

SPOILS: the vault's guards carry spoils now - about one in three drops its tier's spoil, captains and the guardian more
  (for the whole crew), champions too. COPPER COGS (Tier I), SILVER SEALS (II), GILDED LEAVES (III), DEEP PEARLS (IV),
  HOARD EMBERS (V), and CAPTAIN'S INSIGNIA from captains, champions and guardians. Like the pot, they're only yours if
  the crew gets out: at the payout they go straight into your Gutter Bank.
THE GUTTER BANK: your coins and spoils, kept against your name. Deposit everything in one click, take coins or spoils
  back out, and 32 coins (2.67: was 16) buy a Black Market Token. The Armory and the bank pay from it first, then from your pockets.
THE ARMORY: every loaner kit has six ranks, and each leans further into its job. Clear a tier to unlock the next rank
  (Tier I: rank II ... Tier V: rank VI), then pay in coins, that tier's spoil and Captain's Insignia. Ranks are yours for
  good and come with every kit you take.
  TANK      II Reinforced (Juggernaut II, +12 health)   III Spiked Guard (sneaking: attackers take 3 back; Horn every 24 s)
            IV Bastion (Juggernaut III; the Horn shields the crew)   V Last Stand (+16 health; once a heist at 4 hearts:
            Resistance IV + Absorption IV)   VI Colossus (no knockback; the Horn hurls guards back)
  OFFENSE   II Keen Edge (Shadowstep II; Bloodrush heals more)   III Executioner (+5 on foes under a third of their
            health; Charm every 14 s)   IV Ambush (Shadowstep III; the blink strikes for 8)   V Bloodlust (Strength II;
            every fourth hit a sure critical)   VI Phantom (the blink: unseen 4 s, next hit +10)
  RANGED    II Fletcher (64 spectral arrows + 8 harming arrows)   III Wide Volley (7 arrows, every 10 s)   IV Searing
            Shots (Flame)   V Hawkeye (Speed II; bow hits heal you)   VI Storm of Arrows (volley arrows hit twice as hard
            and pierce two foes)
  SUPPORT   II Tidewater (Tidecaller II; the aura reaches 12 and mends faster)   III Spring Tide (Ward every 16 s, and it
            speeds the crew)   IV Undertow (Tidecaller III; Lifeline catches crewmates)   V High Tide (the Ward gives the
            crew Resistance and Strength; 5 potions)   VI Tidal Wave (the Ward hurls guards back, heals twice as much)
YOUR SECONDARY and YOUR SIGNATURE: whatever kit you take, add one weapon and one effect of your own (more open up as you
  clear tiers): a crossbow (an axe for the Ranged kit), slowness potions, wind charges, a trident, spears, harming potions, a mace; fleet feet, iron skin,
  cat's eyes, featherfall, leech, spring heels, fortune's favour, second skin, adrenaline. Change them as often as you like.
THE FIXER'S LEDGER opens the office anywhere (everyone gets one on their first heist; Goldtooth keeps spares). In the den:
  the Armory bench and the Bank vault, beside the kit racks.
GOLDTOOTH: 2 Gutter Medallions (32 coins) for a Token, goods for coins and spoils (pearls, golden apples, diamonds, a totem...).
NETHERITE SCRAP (2.67): no longer for coins - a rare find in a won heist's haul instead, likelier the higher the tier."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import copy
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72

GOLD = '#ffcf40'
OFFICE = '#e8c070'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI']
MAXR = 6
MATS = [  # (iid, name, plural, colour, the tier whose guards carry it - 0: captains, champions, guardians)
    ('copper_cog', 'Copper Cog', 'Copper Cogs', '#d9824a', 1, 'A cog off a Copper Thug\'s gear.'),
    ('silver_seal', 'Silver Seal', 'Silver Seals', '#c8d0d8', 2, 'A silver wax-seal, stamped with a rat.'),
    ('gilded_leaf', 'Gilded Leaf', 'Gilded Leaves', GOLD, 3, 'Gold leaf, peeled off the Gutter Guard\'s armour.'),
    ('deep_pearl', 'Deep Pearl', 'Deep Pearls', '#4ad0c0', 4, 'A pearl from the drowned vault, still wet.'),
    ('hoard_ember', 'Hoard Ember', 'Hoard Embers', '#ff8a30', 5, 'A coal from the Hoard that never goes out.'),
    ('captains_insignia', "Captain's Insignia", "Captain's Insignia", '#c060ff', 0, 'Torn from a captain\'s collar.')]
NM = len(MATS)
COST = {2: (32, 10, 0), 3: (64, 12, 1), 4: (112, 12, 2), 5: (176, 12, 3), 6: (256, 12, 5)}     # rank: (coins, the tier's spoil, insignia)
ROLE_NAME = {r: v[0] for r, v in P72.ROLES.items()}
ROLE_COL = {r: v[1] for r, v in P72.ROLES.items()}
PERKS = {  # role: rank -> (name, what it does)
    1: {1: ('Loaner', 'Juggernaut I, +8 health, half knockback, sneak for Resistance, the Bulwark Horn.'),
        2: ('Reinforced', 'Juggernaut II plate; +12 health.'),
        3: ('Spiked Guard', 'While you sneak, whatever hits you takes 3 back. The Horn every 24 s.'),
        4: ('Bastion', 'Juggernaut III plate; the Horn shields the crew too.'),
        5: ('Last Stand', '+16 health. Once a heist, at 4 hearts: Resistance IV and Absorption IV.'),
        6: ('Colossus', 'No knockback at all. The Horn hurls the guards near you back.')},
    2: {1: ('Loaner', 'Shadowstep I, Strength, Bloodrush, the Cutlass, the Shadowstep Charm.'),
        2: ('Keen Edge', 'Shadowstep II; Bloodrush heals more.'),
        3: ('Executioner', '+5 damage to foes under a third of their health. The Charm every 14 s.'),
        4: ('Ambush', 'Shadowstep III; the blink strikes the nearest foe where you land (8).'),
        5: ('Bloodlust', 'Strength II. Every fourth hit is a sure critical (+6).'),
        6: ('Phantom', 'The blink leaves you unseen for 4 s - and your next hit deals +10.')},
    3: {1: ('Loaner', "Smuggler's set, the Fairy Bow (no Infinity), 64 arrows + 32 spectral, Speed, the Volley Quiver."),
        2: ('Fletcher', '64 spectral arrows, and 8 arrows of Harming.'),
        3: ('Wide Volley', 'Seven arrows a volley, every 10 s.'),
        4: ('Searing Shots', 'The Fairy Bow sets what it hits alight (Flame).'),
        5: ('Hawkeye', 'Speed II. Every Fairy Bow hit heals you a little.'),
        6: ('Storm of Arrows', 'Volley arrows hit twice as hard and pierce through two foes.')},
    4: {1: ('Loaner', 'Tidecaller I, the Staff of Sparks, healing potions, a mending aura, Lifeline, the Tidal Ward.'),
        2: ('Tidewater', 'Tidecaller II; your aura reaches 12 blocks and mends faster.'),
        3: ('Spring Tide', 'The Tidal Ward every 16 s - and it speeds the crew.'),
        4: ('Undertow', 'Tidecaller III; Lifeline catches crewmates near you too.'),
        5: ('High Tide', 'The Ward gives the crew Resistance and Strength. 5 healing potions.'),
        6: ('Tidal Wave', 'The Ward hurls guards back and heals twice as much.')}}
ARMOR_SET = {1: 'juggernaut', 2: 'shadowstep', 4: 'tidecaller'}
ABIL_IID = {1: 'kit_horn', 2: 'kit_step', 3: 'kit_volley', 4: 'kit_tidal'}
ABIL_CD = {1: (30, 24), 2: (18, 14), 3: (14, 10), 4: (24, 16)}          # (ranks I-II, rank III+)
SECONDARY = [  # (name, what, tiers cleared to unlock, [(item, count, extra components)])
    ('Crossbow', 'a crossbow (Quick Charge) and 16 arrows', 0, [('minecraft:crossbow', 1, {'minecraft:enchantments': {'minecraft:quick_charge': 1}}),
                                                               ('minecraft:arrow', 16, None)]),
    ('Slowness Potions', '3 splash potions of Slowness II - pin a crowd down', 0, [('minecraft:splash_potion', 3, {'minecraft:potion_contents': {'potion': 'minecraft:strong_slowness'}})]),   # (2.68b: was the Shield - the Tank has one)
    ('Wind Charges', '12 wind charges - launch yourself, scatter them', 1, [('minecraft:wind_charge', 12, None)]),
    ('Trident', 'a trident that comes back (Loyalty)', 2, [('minecraft:trident', 1, {'minecraft:enchantments': {'minecraft:loyalty': 2}})]),
    ('Iron Spear', 'an iron spear - charge in with it', 2, [('minecraft:iron_spear', 1, None)]),
    ('Harming Potions', '3 splash potions of Harming II', 3, [('minecraft:splash_potion', 3, {'minecraft:potion_contents': {'potion': 'minecraft:strong_harming'}})]),
    ('Diamond Spear', 'a diamond spear (Sharpness II)', 4, [('minecraft:diamond_spear', 1, {'minecraft:enchantments': {'minecraft:sharpness': 2}})]),
    ('Mace', 'a mace (Wind Burst) - fall on them', 5, [('minecraft:mace', 1, {'minecraft:enchantments': {'minecraft:wind_burst': 1}})])]
SIGNATURE = [  # (name, what, tiers cleared to unlock)
    ('Fleet-Footed', 'Speed I', 0), ('Iron Skin', '+4 max health', 0), ("Cat's Eyes", 'Night Vision', 0),
    ('Featherfall', 'falls of up to 8 blocks hurt nothing', 1), ('Leech', 'every guard you drop heals you', 2),
    ('Spring-Heeled', 'Jump Boost I', 2), ("Fortune's Favour", 'every guard you drop: +1 coin into the pot', 3),
    ('Second Skin', 'Absorption I every 30 s', 4), ('Adrenaline', 'under half health: Strength and Speed', 5)]
MENU_CODE = 7800
SEC_NONE, SIG_NONE = MENU_CODE + 29, MENU_CODE + 19    # (2.76: the ninth signature, Adrenaline, had 'none''s code 7839 - it could never be picked)
GUT_M = '#e0a040'           # (the Gutter Medallion's colour - phase86)
LUCKY = '#7dff6a'
TOKEN_COINS = 32          # (2.67: was 16) coins for a Black Market Token at the bank

for _iid, _nm, _pl, _col, _t, _lore in MATS:
    item(_iid, TOTEM, _nm, _col, [_lore, ('A spoil of the Gilded Gutter Vault.', 'gray'),
                                  ('Pays for kit ranks at the Armory, and', 'blue'), ('Goldtooth takes it for his best goods.', 'blue'),
                                  ('Keep it safe in the Gutter Bank.', 'dark_gray')],
         model=f'bm:{_iid}', stack=64, cat='currency')
item('fixers_ledger', TOTEM, "The Fixer's Ledger", OFFICE, ['A battered book with your name in it.', ('Use: plan a heist (or join your party\'s),', 'blue'),
                                                           ('the Armory, the Gutter Bank, your lockers,', 'blue'), ('the lounge, trophies and Bond Sigils.', 'blue'),
                                                           ('Your party within 24 blocks comes along.', 'gray')],
     model='bm:fixers_ledger', stack=1, cat='magic', comps=hold('none'), custom_extra={'bmlv': 276})     # (2.76: every older Ledger is re-issued - phase129)
HOLD['fixers_ledger'] = 'bm:p80/ledger'
P72.KEEP += [m[0] for m in MATS] + ['fixers_ledger']
P70.GOLDTOOTH_STOCK.append((1, 'fixers_ledger', 1))
ITEMS['gutter_coin']['comps']['minecraft:lore'] = [T('A heavy coin stamped with a grinning rat.', 'gray'), T('Goldtooth takes them in the Fixer\'s Den.', 'gray'),
                                                   T('16 buy a Token at the Gutter Bank;', 'blue'), T('the Armory takes them for kit ranks.', 'blue')] + ITEMS['gutter_coin']['comps']['minecraft:lore'][-1:]

# Goldtooth's new goods: a Token, and the better things for coins and spoils
_orig_goldtooth = P70.goldtooth


def _goldtooth():
    from gen_dp import offer
    d = _orig_goldtooth()
    d['Offers']['Recipes'] += [offer(('gutter_medallion', 2), ('token', 1)),        # (2.67: was 16 coins)
                               offer(('gutter_coin', 12), ('minecraft:ender_pearl', 1)),
                               offer(('gutter_coin', 10), ('minecraft:golden_carrot', 4)),
                               offer(('gutter_coin', 24), ('minecraft:golden_apple', 1)),
                               offer(('gutter_coin', 16), ('minecraft:experience_bottle', 8), ('copper_cog', 6)),
                               offer(('gutter_coin', 48), ('minecraft:diamond', 1), ('silver_seal', 4)),
                               offer(('gutter_coin', 40), ('minecraft:enchanted_golden_apple', 1), ('gilded_leaf', 10)),
                               offer(('gutter_coin', 64), ('minecraft:totem_of_undying', 1), ('hoard_ember', 8))]
    return d


P70.goldtooth = _goldtooth


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Office] ', OFFICE, bold=True)]
    rel = RM.rel
    tick, fast, second = [], [], []
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    ident = [F(0), F(0), F(0), F(1)]
    bank = ['bm.gbc'] + [f'bm.gb{i}' for i in range(1, NM + 1)]                  # banked: coins, then each spoil
    found = [f'bm.gf{i}' for i in range(1, NM + 1)]                                # found this heist (lost if it fails)
    objs = bank + found + [f'bm.kr{r}' for r in range(1, 5)] + ['bm.ksec', 'bm.ksig', 'bm.kls', 'bm.khc', 'bm.ksgt', 'bm.gvled']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 3, 4, 10, 16, 64)]
    G.OBJECTIVES += objs
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    raw = lambda k: f'@@RAW:{k}@@'

    # ================================================================== bookkeeping
    fn('p80/init_me', [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0' for o in bank] +
       [f'execute unless score @s bm.kr{r} matches 1.. run scoreboard players set @s bm.kr{r} 1' for r in range(1, 5)] +
       ['execute unless score @s bm.ksec matches 0.. run scoreboard players set @s bm.ksec 0', 'execute unless score @s bm.ksig matches 0.. run scoreboard players set @s bm.ksig 0'])
    # (as a player) #tc = coins on you + banked; #t1.. each spoil, the same
    fn('p80/tot', ['function bm:p80/init_me', f'execute store result score #tc bm.rng run clear @s {holds("gutter_coin")} 0', 'scoreboard players operation #tc bm.rng += @s bm.gbc'] +
       sum(([f'execute store result score #t{i} bm.rng run clear @s {holds(m[0])} 0', f'scoreboard players operation #t{i} bm.rng += @s bm.gb{i}'] for i, m in enumerate(MATS, 1)), []))
    # (as a player) take $(n) of $(iid): the bank first (bm.gb$(o): c coins, 1.. a spoil), then the pockets - the caller has checked there's enough
    fn('p80/pay', ['$scoreboard players set #need bm.rng $(n)', '$scoreboard players operation #fromb bm.rng = @s bm.gb$(o)',
                   'scoreboard players operation #fromb bm.rng < #need bm.rng', '$scoreboard players operation @s bm.gb$(o) -= #fromb bm.rng',
                   'scoreboard players operation #need bm.rng -= #fromb bm.rng',
                   'execute store result storage bm:tmp pay.k int 1 run scoreboard players get #need bm.rng', '$data modify storage bm:tmp pay.iid set value "$(iid)"',
                   'execute if score #need bm.rng matches 1.. run function bm:p80/pay_inv with storage bm:tmp pay'])
    fn('p80/pay_inv', ['$clear @s *[minecraft:custom_data~{bm:"$(iid)"}] $(k)'])
    # (#c = how many, as a player) hand out $(iid) in stacks of 64
    fn('p80/hand', ['scoreboard players set #k bm.rng 64', 'scoreboard players operation #k bm.rng < #c bm.rng',
                    'execute store result storage bm:tmp hd.k int 1 run scoreboard players get #k bm.rng', '$data modify storage bm:tmp hd.iid set value "$(iid)"',
                    'function bm:p80/hand1 with storage bm:tmp hd', 'scoreboard players operation #c bm.rng -= #k bm.rng',
                    '$execute if score #c bm.rng matches 1.. run function bm:p80/hand {iid:"$(iid)"}'])
    fn('p80/hand1', ['$loot give @s loot bm:p80/n/$(iid)'])           # (each item's loot table gives #k of it)
    for iid in ['gutter_coin', 'token'] + [m[0] for m in MATS]:
        wjson(f'bm/loot_table/p80/n/{iid}.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry(iid, {'type': 'minecraft:score', 'target': {'type': 'minecraft:fixed', 'name': '#k'},
                                                                                                        'score': 'bm.rng'})]}]})
    # (#clr = the highest tier you've cleared, from your first-clear marks)
    fn('p80/clr', ['scoreboard players set #clr bm.rng 0'] +
       [x for t in range(1, 6) for x in (f'scoreboard players operation #q bm.rng = @s bm.gvcl', f'scoreboard players set #bit bm.rng {2 ** t}',
                                          'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                                          f'execute if score #q bm.rng matches 1 run scoreboard players set #clr bm.rng {t}')])

    # ================================================================== SPOILS: dropped as guards fall, banked at the payout
    mat_name = lambda i, n: [f'execute if score #mi bm.rng matches {i} run return run ' + title('@s', 'actionbar', [
        T('+', GOLD), {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True}, T(' coins into the pot   ', GOLD),
        T('+', MATS[i - 1][3]), {'score': {'name': '#md', 'objective': 'bm.rng'}, 'color': MATS[i - 1][3], 'bold': True}, T(' ' + MATS[i - 1][2], MATS[i - 1][3]),
        T('  (yours if the crew gets out)', 'dark_gray')])]
    fn('p80/kbar', ['execute if score #md bm.rng matches 0 run return run ' + title('@s', 'actionbar', [T('+', GOLD), {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True},
                                                                                                       T(' coins into the pot', GOLD)])] +
       sum((mat_name(i, None) for i in range(1, NM + 1)), []))
    # (as the killer; #gi set) #mt = the heist's tier
    fn('p80/tier', ['scoreboard players set #mt bm.rng 1', inst('bm:p80/tier2')])
    fn('p80/tier2', ['scoreboard players operation #mt bm.rng = @s bm.gvt', 'execute if score #mt bm.rng matches ..0 run scoreboard players set #mt bm.rng 1',
                     'execute if score #mt bm.rng matches 6.. run scoreboard players set #mt bm.rng 5'])
    # (#mi = which spoil, #md = how many) into this heist's finds
    fn('p80/find', [f'execute if score #mi bm.rng matches {i} run scoreboard players operation @s {o} += #md bm.rng' for i, o in enumerate(found, 1)])
    fn('p80/drop_guard', ['scoreboard players set #md bm.rng 0', 'function bm:p80/tier', 'execute store result score #r bm.rng run random value 1..100',
                          'execute if score #r bm.rng matches 34.. run return 0', 'scoreboard players operation #mi bm.rng = #mt bm.rng', 'scoreboard players set #md bm.rng 1',
                          'function bm:p80/find'])
    # captains and guardians: for the whole crew
    for key, nmat, nins in (('captain', 2, 1), ('boss', 4, 2), ('champ', 3, 1)):
        fn(f'p80/drop_{key}', ['function bm:p80/tier', f'execute as @a[tag=bm.gvp] if score @s bm.gvi = #gi bm.rng run function bm:p80/drop_{key}_p'])
        fn(f'p80/drop_{key}_p', ['scoreboard players operation #mi bm.rng = #mt bm.rng', f'scoreboard players set #md bm.rng {nmat}', 'function bm:p80/find',
                                 f'scoreboard players add @s bm.gf{NM} {nins}',
                                 tellraw('@s', P + [T('Spoils! ', GOLD, bold=True), T(f'+{nmat} of this tier\'s spoil and +{nins} Captain\'s Insignia', 'gray'),
                                                    T(' - yours if the crew gets out.', 'dark_gray')])])
    kg = G.FUNCS['p75/kill_guard']
    k = next(i for i, l in enumerate(kg) if l.startswith('title @s actionbar'))
    kg[k:k + 1] = ['function bm:p80/drop_guard', 'function bm:p80/kbar']
    for key in ('captain', 'boss'):
        L = G.FUNCS[f'p75/kill_{key}']
        L.append(f'function bm:p80/drop_{key}')
    killed = lambda tag: {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}}
    wjson('bm/advancement/p80/kill_champ.json', {'criteria': killed('bm.gvchamp'), 'rewards': {'function': 'bm:p80/kill_champ'}})
    fn('p80/kill_champ', ['advancement revoke @s only bm:p80/kill_champ', 'execute unless entity @s[tag=bm.gvp] run return 0',
                          'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p80/drop_champ'])
    # the payout: your finds into your bank (as the player, in p70/haul)
    fn('p80/bank_finds', ['function bm:p80/init_me'] +
       sum(([f'scoreboard players operation @s bm.gb{i} += @s {found[i - 1]}',
             f'execute if score @s {found[i - 1]} matches 1.. run ' + tellraw('@s', P + [T('+', m[3]), {'score': {'name': '@s', 'objective': found[i - 1]}, 'color': m[3], 'bold': True},
                                                                                      T(f' {m[2]}', m[3]), T(' into your Gutter Bank.', 'gray')]),
             f'scoreboard players set @s {found[i - 1]} 0'] for i, m in enumerate(MATS, 1)), []))
    G.FUNCS['p70/haul'].append('function bm:p80/bank_finds')
    # (2.67) NETHERITE SCRAP: a rare find in a won heist - Tier I 3%, II 6%, III 10%, IV 15%, V 22% (+3 with nobody knocked out);
    #        at Tier V sometimes two
    SCRAP = {1: 3, 2: 6, 3: 10, 4: 15, 5: 22}
    G.FUNCS['p70/haul'].append('function bm:p80/scrap')
    fn('p80/scrap', ['scoreboard players set #sc bm.rng 0'] + [f'execute if score #gt bm.rng matches {t} run scoreboard players set #sc bm.rng {c}' for t, c in SCRAP.items()] +
       [inst('bm:p80/scrap_clean'), 'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng > #sc bm.rng run return 0',
        'loot give @s loot bm:p80/scrap1', 'execute if score #gt bm.rng matches 5 if score #r bm.rng matches ..7 run loot give @s loot bm:p80/scrap1',     # (into The Haul - phase81)
        'playsound minecraft:block.ancient_debris.break player @s ~ ~ ~ 1 0.8',
        tellraw('@s', P + [T('Rare find! ', '#a08090', bold=True), T('A scrap of netherite in your share of the haul.', 'gray')])])
    wjson('bm/loot_table/p80/scrap1.json', {'pools': [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:netherite_scrap'}]}]})
    fn('p80/scrap_clean', ['execute if score @s bm.gvdc matches 0 run scoreboard players add #sc bm.rng 3'])
    # a fresh heist, a failed one, or walking out: the finds are lost; once-a-heist perks reset
    fn('p80/run_reset', [f'scoreboard players set @s {o} 0' for o in found] + ['scoreboard players set @s bm.kls 0', 'scoreboard players set @s bm.khc 0',
                                                                              'tag @s remove bm.kphantom'])
    for s in range(P70.SLOTS):
        for f in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            G.FUNCS[f] += ['function bm:p80/run_reset', 'function bm:p80/first_ledger']
    G.FUNCS['p75/after_fail'].append('function bm:p80/run_reset')
    G.FUNCS['p70/unraid'].append('function bm:p80/run_reset')
    fn('p80/first_ledger', ['execute if score @s bm.gvled matches 1 run return 0', 'scoreboard players set @s bm.gvled 1',
                            'execute if items entity @s container.* *[minecraft:custom_data~{bm:"fixers_ledger"}] run return 0', give('fixers_ledger'),
                            tellraw('@s', P + [T('The Fixer slides you a ledger with your name in it. ', OFFICE), T('Use it any time: your kits, your bank, your trophies.', 'gray')])])

    # ================================================================== THE OFFICE (the hub)
    def menu_open(code):
        return [f'scoreboard players set @s bm.menu {code}']
    can = ['execute if items entity @s container.* *[minecraft:custom_data~{bm:"fixers_ledger"}] run return 1',
           'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"fixers_ledger"}] run return 1',
           'execute if entity @s[tag=bm.gvp] run return 1', 'return 0']
    fn('p80/can', can)
    fn('p80/ledger', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2', 'function bm:p80/office'])
    hub_lines = ['function bm:p80/tot', 'function bm:p80/clr', 'data remove storage bm:ui of'] + menu_open(MENU_CODE) + \
        ['execute store result storage bm:ui of.c int 1 run scoreboard players get @s bm.gbc', 'execute store result storage bm:ui of.clr int 1 run scoreboard players get #clr bm.rng'] + \
        [f'execute store result storage bm:ui of.r{r} int 1 run scoreboard players get @s bm.kr{r}' for r in range(1, 5)] + \
        ['function bm:p81/count_all', 'execute store result storage bm:ui of.tro int 1 run scoreboard players get #tro bm.rng',
         'function bm:p80/office_dlg with storage bm:ui of']
    fn('p80/office', hub_lines)
    hub = P28.multi([T("THE FIXER'S OFFICE", OFFICE, bold=True), T('  ·  everything the vault owes you', 'gray')],
                    [P28.body([T('"Sit. Here\'s where you stand."\n', '#d8c8a8', italic=True),
                               T('⛃ ', GOLD), T('In the Gutter Bank   ', 'white'), T('$(c)', GOLD, bold=True), T(' coins', 'gray'),
                               T('\n⚑ ', '#9ad0ff'), T('Tiers cleared   ', 'white'), T('$(clr)', 'white', bold=True), T(' of 5', 'gray'),
                               T('\n★ ', GOLD), T('Trophies on your shelf   ', 'white'), T('$(tro)', GOLD, bold=True),
                               T('\n⚒ ', ROLE_COL[1]), T('Kit ranks ', 'white'), T('(of 6)', 'dark_gray'),
                               T('\n     Tank ', ROLE_COL[1]), T('$(r1)', 'white', bold=True), T('    Offense ', ROLE_COL[2]), T('$(r2)', 'white', bold=True),
                               T('    Ranged ', ROLE_COL[3]), T('$(r3)', 'white', bold=True), T('    Support ', ROLE_COL[4]), T('$(r4)', 'white', bold=True)], 300)],
                    [P28.btn([T('⚒ ', ROLE_COL[1]), T('The Armory', 'white', bold=True)], MENU_CODE + 1, tooltip=T('Rank up your kits; pick your secondary and signature.'), width=150),
                     P28.btn([T('⛃ ', GOLD), T('The Gutter Bank', 'white', bold=True)], MENU_CODE + 2, tooltip=T('Coins and spoils; 32 coins buy a Token.'), width=150),
                     P28.btn([T('🏆 ', GOLD), T('Trophy Case', 'white', bold=True)], MENU_CODE + 3, tooltip=T('Six metals of trophies, and how to earn them.'), width=150),
                     P28.btn([T('✦ ', '#e8b8ff'), T('Bond Sigils', 'white', bold=True)], MENU_CODE + 4, tooltip=T('Which sigils do what - two at most each heist.'), width=150),
                     P28.btn([T('▣ ', '#c89a5a'), T('The Locker Hall', 'white', bold=True)], MENU_CODE + 5, tooltip=T('Claim double-chest lockers for your raiding things. From safe ground: hold still for 3 seconds.'), width=150),
                     P28.btn([T('⛁ ', '#9ad0ff'), T('The Crate Desk', 'white', bold=True)], MENU_CODE + 6, tooltip=T('Crates of vanilla goods, and tip-offs for your next heist - for Gutter Coins.'), width=150),
                     P28.btn([T('☺ ', '#9ad0ff'), T('Raid Crew', 'white', bold=True)], MENU_CODE + 7, tooltip=T('Followers and hirelings: who comes into the vault with you.'), width=150)],
                    columns=2)
    globals()['HUB'] = copy.deepcopy(hub)                    # (2.68: on a heist the Office adds 'Leave the heist' - phase104)
    # (2.75: the Heist Plans folded into the Ledger - planning heads the Office, off a heist)
    globals()['PLAN_BTN'] = P28.btn([T('⚑ ', GOLD), T('Plan a Heist', GOLD, bold=True), T('  or join your party\'s', 'gray')], MENU_CODE + 9, width=304,
                                    tooltip=T('Pick a tier (or the Endless Vault, or the Pit) and your tries; your party within 24 blocks comes along. From safe ground.'))
    hub['actions'].insert(0, copy.deepcopy(PLAN_BTN))       # (later phases that rebuild the Office from HUB put this back on top - see phase117)
    fn('p80/office_dlg', [f'$dialog show @s {P28.inline(hub)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU_CODE}..{MENU_CODE + 199} run return run function bm:p80/act')
    act = ['execute unless function bm:p80/can run return run function bm:p28/stale',
           f'execute unless score @s bm.menu matches {MENU_CODE}..{MENU_CODE + 199} run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {MENU_CODE} run return run function bm:p80/office',
           f'execute if score #act bm.pay matches {MENU_CODE + 1} run return run function bm:p80/armory',
           f'execute if score #act bm.pay matches {MENU_CODE + 2} run return run function bm:p80/bank',
           f'execute if score #act bm.pay matches {MENU_CODE + 3} run return run function bm:p81/case',
           f'execute if score #act bm.pay matches {MENU_CODE + 4} run return run function bm:p81/sigils',
           f'execute if score #act bm.pay matches {MENU_CODE + 5} run return run function bm:p84/lk/from_ledger',
           f'execute if score #act bm.pay matches {MENU_CODE + 6} run return run function bm:p86/theme/menu',
           f'execute if score #act bm.pay matches {MENU_CODE + 9} run return run function bm:p70/plans'] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 10 + r} run return run function bm:p80/up{r}' for r in range(1, 5)] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 20} run return run function bm:p80/sec_menu',
         f'execute if score #act bm.pay matches {MENU_CODE + 30} run return run function bm:p80/sig_menu'] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 21 + i} run return run function bm:p80/sec_pick {{i:{i + 1}}}' for i in range(len(SECONDARY))] + \
        [f'execute if score #act bm.pay matches {SEC_NONE} run return run function bm:p80/sec_pick {{i:0}}',
         f'execute if score #act bm.pay matches {SIG_NONE} run return run function bm:p80/sig_pick {{i:0}}'] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 31 + i} run return run function bm:p80/sig_pick {{i:{i + 1}}}' for i in range(len(SIGNATURE))] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 40 + j} run return run function bm:p80/bank_{a}' for j, a in
         enumerate(('deposit', 'take16', 'take64', 'takeall', 'buy1', 'buy10'))] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 50 + i} run return run function bm:p80/bank_mat {{i:{i}}}' for i in range(1, NM + 1)] + \
        [f'execute if score #act bm.pay matches {MENU_CODE + 46} run return run function bm:p80/bank_coins',
         f'execute if score #act bm.pay matches {MENU_CODE + 47} run return run function bm:p80/bank_spoils',
         f'execute if score #act bm.pay matches {MENU_CODE + 48} run return run function bm:p80/bank_tokens',
         f'execute if score #act bm.pay matches {MENU_CODE + 57} run return run function bm:p80/bank_takegm',
         f'execute if score #act bm.pay matches {MENU_CODE + 58} run return run function bm:p80/bank_takegt']
    fn('p80/act', act)

    # ================================================================== THE GUTTER BANK
    # (2.67: one clear account page - what you hold, then four plain choices; taking coins, taking spoils and buying Tokens
    #  each get their own small page, and every action brings you back to the page you were on)
    bank_lines = ['function bm:p80/tot', 'data remove storage bm:ui bk2'] + menu_open(MENU_CODE + 2) + \
        ['execute store result storage bm:ui bk2.c int 1 run scoreboard players get @s bm.gbc',
         f'execute store result storage bm:ui bk2.ci int 1 run clear @s {holds("gutter_coin")} 0'] + \
        [f'execute store result storage bm:ui bk2.m{i} int 1 run scoreboard players get @s bm.gb{i}' for i in range(1, NM + 1)]
    fn('p80/bank', bank_lines + ['function bm:p80/bank_dlg with storage bm:ui bk2'])
    fn('p80/bank_coins', bank_lines + ['function bm:p80/bank_cdlg with storage bm:ui bk2'])
    fn('p80/bank_spoils', bank_lines + ['function bm:p80/bank_sdlg with storage bm:ui bk2'])
    fn('p80/bank_tokens', bank_lines + ['function bm:p80/bank_tdlg with storage bm:ui bk2'])
    btitle = lambda sub: [T('THE GUTTER BANK', GOLD, bold=True), T('  ·  ' + sub, 'gray')]
    coins_line = [T('◆ ', GOLD), T('Gutter Coins   ', 'white'), T('$(c)', GOLD, bold=True), T('   (on you: $(ci))', 'dark_gray')]
    acct = [T('YOUR ACCOUNT\n', 'white', bold=True)] + coins_line + \
        sum(([T('\n◆ ', m[3]), T(m[2] + '   ', 'white'), T(f'$(m{i})', m[3], bold=True)] for i, m in enumerate(MATS, 1)), [])
    back = P28.btn(T('« Back', 'gray'), MENU_CODE + 2, width=150)
    bdlg = P28.multi(btitle('your coins and spoils'),
                     [P28.body(acct, 260),
                      P28.body([T('Deposit puts every coin, spoil and Gutter Medallion you carry into your account. ', 'gray'),
                                T('The Armory pays from here first, then from your pockets.', 'dark_gray')], 300)],
                     [P28.btn([T('⬇ ', LUCKY), T('Deposit everything', 'white', bold=True)], MENU_CODE + 40, tooltip=T('All the coins, spoils and Gutter Medallions you carry.'), width=150),
                      P28.btn([T('⬆ ', GOLD), T('Take out coins', 'white')], MENU_CODE + 46, tooltip=T('16, 64, all - or a Gutter Medallion.'), width=150),
                      P28.btn([T('⬆ ', '#c060ff'), T('Take out spoils', 'white')], MENU_CODE + 47, tooltip=T('Cogs, seals, leaves, pearls, embers, insignia.'), width=150),
                      P28.btn([T('✦ ', GOLD), T('Buy Tokens', 'white')], MENU_CODE + 48, tooltip=T(f'{TOKEN_COINS} coins a Black Market Token.'), width=150),
                      P28.btn(T('« The Office', 'gray'), MENU_CODE, width=150)],
                     columns=2)
    fn('p80/bank_dlg', [f'$dialog show @s {P28.inline(bdlg)}'])
    cdlg = P28.multi(btitle('take out coins'),
                     [P28.body(coins_line, 260), P28.body([T('A Gutter Medallion is 16 coins in one piece (a Gutter Trophy, 128).', 'dark_gray')], 300)],
                     [P28.btn(T('Take 16 coins', 'white'), MENU_CODE + 41, width=150), P28.btn(T('Take 64 coins', 'white'), MENU_CODE + 42, width=150),
                      P28.btn(T('Take all my coins', 'white'), MENU_CODE + 43, width=150),
                      P28.btn([T('A Gutter Medallion ', GUT_M), T('(16)', 'gray')], MENU_CODE + 57, width=150),
                      P28.btn([T('A Gutter Trophy ', '#ffd870'), T('(128)', 'gray')], MENU_CODE + 58, width=150), back],
                     columns=2)
    fn('p80/bank_cdlg', [f'$dialog show @s {P28.inline(cdlg)}'])
    sdlg = P28.multi(btitle('take out spoils'),
                     [P28.body([T('Take a spoil out and you get every one you have of it.', 'gray')], 300)],
                     [P28.btn([T(m[2] + '  ', m[3]), T(f'($(m{i}))', 'white')], MENU_CODE + 50 + i, width=150) for i, m in enumerate(MATS, 1)] + [back],
                     columns=2)
    fn('p80/bank_sdlg', [f'$dialog show @s {P28.inline(sdlg)}'])
    tdlg = P28.multi(btitle('Black Market Tokens'),
                     [P28.body([T(f'A Token costs {TOKEN_COINS} coins - from your account first, then your pockets.\n', 'gray')] + coins_line, 300)],
                     [P28.btn([T('Buy 1 Token ', GOLD), T(f'({TOKEN_COINS})', 'gray')], MENU_CODE + 44, width=150),
                      P28.btn([T('Buy 10 Tokens ', GOLD), T(f'({TOKEN_COINS * 10})', 'gray')], MENU_CODE + 45, width=150), back],
                     columns=2)
    fn('p80/bank_tdlg', [f'$dialog show @s {P28.inline(tdlg)}'])
    for nm, worth, iid in (('takegm', 16, 'gutter_medallion'), ('takegt', 128, 'gutter_trophy')):
        fn(f'p80/bank_{nm}', ['function bm:p80/init_me', f'execute unless score @s bm.gbc matches {worth}.. run return run ' + say(f'That takes {worth} coins in your account.', 'red'),
                              f'scoreboard players remove @s bm.gbc {worth}', f'loot give @s loot bm:items/{iid}', 'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.4',
                              'function bm:p80/bank_coins'])
    dep = ['function bm:p80/init_me', 'scoreboard players set #any bm.rng 0']
    for iid, obj in [('gutter_coin', 'bm.gbc')] + [(m[0], f'bm.gb{i}') for i, m in enumerate(MATS, 1)]:
        dep += [f'execute store result score #n bm.rng run clear @s {holds(iid)} 0', f'scoreboard players operation @s {obj} += #n bm.rng',
                f'execute if score #n bm.rng matches 1.. run scoreboard players set #any bm.rng 1', f'clear @s {holds(iid)}']
    for iid, worth in (('gutter_medallion', 16), ('gutter_trophy', 128)):          # (2.67) the big pieces count as coins in your account
        dep += [f'execute store result score #n bm.rng run clear @s {holds(iid)} 0', f'scoreboard players set #w bm.rng {worth}', 'scoreboard players operation #n bm.rng *= #w bm.rng',
                'scoreboard players operation @s bm.gbc += #n bm.rng', f'execute if score #n bm.rng matches 1.. run scoreboard players set #any bm.rng 1', f'clear @s {holds(iid)}']
    dep += ['execute if score #any bm.rng matches 0 run ' + say('Nothing on you to deposit.'), 'execute if score #any bm.rng matches 1 run playsound minecraft:block.chain.place player @s ~ ~ ~ 0.8 1.4',
            'execute if score #any bm.rng matches 1 run ' + say('Deposited. The rats count it twice.', GOLD), 'function bm:p80/bank']
    fn('p80/bank_deposit', dep)
    for nm, n in (('take16', 16), ('take64', 64)):
        fn(f'p80/bank_{nm}', ['function bm:p80/init_me', f'scoreboard players set #c bm.rng {n}', 'scoreboard players operation #c bm.rng < @s bm.gbc',
                              'execute if score #c bm.rng matches ..0 run return run ' + say('No coins in your account.'),
                              'scoreboard players operation @s bm.gbc -= #c bm.rng', 'function bm:p80/hand {iid:"gutter_coin"}',
                              'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.4', 'function bm:p80/bank_coins'])
    fn('p80/bank_takeall', ['function bm:p80/init_me', 'scoreboard players operation #c bm.rng = @s bm.gbc',
                            'execute if score #c bm.rng matches ..0 run return run ' + say('No coins in your account.'),
                            'scoreboard players set @s bm.gbc 0', 'function bm:p80/hand {iid:"gutter_coin"}', 'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.2',
                            'function bm:p80/bank_coins'])
    for nm, n in (('buy1', 1), ('buy10', 10)):
        fn(f'p80/bank_{nm}', ['function bm:p80/tot', f'execute unless score #tc bm.rng matches {TOKEN_COINS * n}.. run return run ' + say(f'That takes {TOKEN_COINS * n} coins (bank and pockets).', 'red'),
                              f'function bm:p80/pay {{o:"c",iid:"gutter_coin",n:{TOKEN_COINS * n}}}', f'loot give @s loot bm:p80/tokens{n}',
                              'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1', say(f'{TOKEN_COINS * n} coins for {n} Token{"s" if n > 1 else ""}.', GOLD), 'function bm:p80/bank_tokens'])
        wjson(f'bm/loot_table/p80/tokens{n}.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('token', n)]}]})
    fn('p80/bank_mat', ['function bm:p80/init_me', '$scoreboard players operation #c bm.rng = @s bm.gb$(i)',
                        'execute if score #c bm.rng matches ..0 run return run ' + say('None of those in your account.'),
                        '$scoreboard players set @s bm.gb$(i) 0', '$function bm:p80/bank_mat2 {i:$(i)}', 'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.2', 'function bm:p80/bank_spoils'])
    fn('p80/bank_mat2', ['$function bm:p80/bank_mat_$(i)'])
    for i, m in enumerate(MATS, 1):
        fn(f'p80/bank_mat_{i}', [f'function bm:p80/hand {{iid:"{m[0]}"}}'])

    # ================================================================== THE ARMORY
    def status_cmds(r):
        """(as a player, after p80/tot and p80/clr) ar.s{r} = the next rank's status, as a coloured component"""
        out = []
        for n in range(2, MAXR + 1):
            coins, mats, ins = COST[n]
            mat = MATS[n - 2]
            need = f'{coins} coins · {mats} {mat[2]}' + (f' · {ins} Insignia' if ins else '')
            cond = f'if score @s bm.kr{r} matches {n - 1}'
            out += [f'execute {cond} run data modify storage bm:ui ar.n{r} set value "{ROMAN[n]} {PERKS[r][n][0]}"',
                    f'execute {cond} run data modify storage bm:ui ar.d{r} set value "{PERKS[r][n][1]}"',
                    f'execute {cond} run data modify storage bm:ui ar.r_s{r} set value {snbt(T("✘ Needs: " + need, GOLD))}',
                    f'execute {cond} if score #tc bm.rng matches {coins}.. if score #t{n - 1} bm.rng matches {mats}.. if score #t{NM} bm.rng matches {ins}.. run '
                    f'data modify storage bm:ui ar.r_s{r} set value {snbt(T("✔ Ready: " + need, "green"))}',
                    f'execute {cond} unless score #clr bm.rng matches {n - 1}.. run data modify storage bm:ui ar.r_s{r} set value {snbt(T(f"✘ Clear Tier {ROMAN[n - 1]} to unlock rank {ROMAN[n]}", "red"))}']
        out += [f'execute if score @s bm.kr{r} matches {MAXR}.. run data modify storage bm:ui ar.n{r} set value "-"',
                f'execute if score @s bm.kr{r} matches {MAXR}.. run data modify storage bm:ui ar.d{r} set value "Every rank earned."',
                f'execute if score @s bm.kr{r} matches {MAXR}.. run data modify storage bm:ui ar.r_s{r} set value {snbt(T("✦ MASTERED", GOLD, bold=True))}']
        out += [f'execute if score @s bm.kr{r} matches {n} run data modify storage bm:ui ar.r{r} set value "{ROMAN[n]} {PERKS[r][n][0]}"' for n in range(1, MAXR + 1)]
        return out
    ar = ['function bm:p80/tot', 'function bm:p80/clr', 'data remove storage bm:ui ar'] + menu_open(MENU_CODE + 1)
    for r in range(1, 5):
        ar += status_cmds(r)
    ar += ['data modify storage bm:ui ar.sec set value "none"', 'data modify storage bm:ui ar.sig set value "none"']
    ar += [f'execute if score @s bm.ksec matches {i + 1} run data modify storage bm:ui ar.sec set value "{s[0]}"' for i, s in enumerate(SECONDARY)]
    ar += [f'execute if score @s bm.ksig matches {i + 1} run data modify storage bm:ui ar.sig set value "{s[0]}"' for i, s in enumerate(SIGNATURE)]
    ar += ['execute store result storage bm:ui ar.c int 1 run scoreboard players get #tc bm.rng', 'function bm:p80/armory_dlg with storage bm:ui ar']
    fn('p80/armory', ar)
    rbody = lambda r: P28.body([T(ROLE_NAME[r].upper(), ROLE_COL[r], bold=True), T('   rank ', 'gray'), T(f'$(r{r})', 'white', bold=True), T('\n'),
                                T('next: ', 'dark_gray'), T(f'$(n{r})', 'white'), T(f' - $(d{r})', 'gray'), T('\n'), raw(f'r_s{r}')], 360)
    ladder = lambda r: [T(f'{ROLE_NAME[r]} ranks', ROLE_COL[r], bold=True)] + sum(([T(f'\n{ROMAN[n]} {PERKS[r][n][0]}: ', 'white'), T(PERKS[r][n][1], 'gray')]
                                                                                for n in range(1, MAXR + 1)), [])
    adlg = P28.multi([T('THE ARMORY', ROLE_COL[1], bold=True), T('  ·  your kits, for good', 'gray')],
                     [P28.body([T('Clear a tier to unlock the next rank, then pay in coins, that tier\'s spoil and insignia ', 'dark_gray'),
                                T('(bank first, then your pockets: ', 'dark_gray'), T('$(c)', GOLD), T(' coins to hand).', 'dark_gray')], 360)] +
                     [rbody(r) for r in range(1, 5)] +
                     [P28.body([T('Secondary: ', 'gray'), T('$(sec)', 'white', bold=True), T('      Signature: ', 'gray'), T('$(sig)', 'white', bold=True),
                                T('  (with every kit)', 'dark_gray')], 360)],
                     [P28.btn([T('⬆ ', ROLE_COL[r]), T(ROLE_NAME[r], 'white', bold=True)], MENU_CODE + 10 + r, tooltip=ladder(r), width=110) for r in range(1, 5)] +
                     [P28.btn([T('Secondary weapon', 'white')], MENU_CODE + 20, tooltip=T('One weapon of your own, with any kit.'), width=110),
                      P28.btn([T('Signature effect', 'white')], MENU_CODE + 30, tooltip=T('One effect of your own, with any kit.'), width=110),
                      P28.btn(T('Gutter Bank', 'gray'), MENU_CODE + 2, width=110), P28.btn(T('« Office', 'gray'), MENU_CODE, width=110)],
                     columns=4)
    fn('p80/armory_dlg', [f'$dialog show @s {P28.inline(adlg)}'])
    # buying a rank
    for r in range(1, 5):
        up = ['function bm:p80/tot', 'function bm:p80/clr',
              f'execute if score @s bm.kr{r} matches {MAXR}.. run return run ' + say(f'Your {ROLE_NAME[r]} kit has every rank already.', GOLD)]
        for n in range(2, MAXR + 1):
            coins, mats, ins = COST[n]
            mat = MATS[n - 2]
            up += [f'execute if score @s bm.kr{r} matches {n - 1} unless score #clr bm.rng matches {n - 1}.. run return run ' + say(f'Clear Tier {ROMAN[n - 1]} first.', 'red'),
                   f'execute if score @s bm.kr{r} matches {n - 1} unless score #tc bm.rng matches {coins}.. run return run ' + say(f'That rank costs {coins} coins.', 'red'),
                   f'execute if score @s bm.kr{r} matches {n - 1} unless score #t{n - 1} bm.rng matches {mats}.. run return run ' + say(f'That rank needs {mats} {mat[2]}.', 'red'),
                   f'execute if score @s bm.kr{r} matches {n - 1} unless score #t{NM} bm.rng matches {ins}.. run return run ' + say(f'That rank needs {ins} Captain\'s Insignia.', 'red'),
                   f'execute if score @s bm.kr{r} matches {n - 1} run return run function bm:p80/buy{r}_{n}']
        fn(f'p80/up{r}', up)
        for n in range(2, MAXR + 1):
            coins, mats, ins = COST[n]
            mat = MATS[n - 2]
            fn(f'p80/buy{r}_{n}', [f'function bm:p80/pay {{o:"c",iid:"gutter_coin",n:{coins}}}', f'function bm:p80/pay {{o:"{n - 1}",iid:"{mat[0]}",n:{mats}}}'] +
               ([f'function bm:p80/pay {{o:"{NM}",iid:"{MATS[-1][0]}",n:{ins}}}'] if ins else []) +
               [f'scoreboard players set @s bm.kr{r} {n}',
                'execute at @s run playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 0.9', 'execute at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1.2',
                'execute at @s run particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.3 40',
                'title @s times 5 40 10', title('@s', 'title', T(f'{ROLE_NAME[r]} {ROMAN[n]}', ROLE_COL[r], bold=True)),
                title('@s', 'subtitle', T(PERKS[r][n][0], 'white')),
                tellraw('@s', P + [T(f'{ROLE_NAME[r]} kit, rank {ROMAN[n]}: ', ROLE_COL[r], bold=True), T(PERKS[r][n][0] + '. ', 'white'), T(PERKS[r][n][1], 'gray'),
                                   T(' (From your next kit on.)', 'dark_gray')]),
                'function bm:p80/armory'])
    # secondary and signature pickers
    def picker(kind, opts, base_code, obj):
        lines = ['function bm:p80/clr', f'data remove storage bm:ui p{kind}'] + menu_open(MENU_CODE + (20 if kind == 'sec' else 30))
        btns = []
        for i, o in enumerate(opts):
            nm, what, need = o[0], o[1], o[2]
            lines += [f'data modify storage bm:ui p{kind}.r_l{i} set value {snbt(T(nm, "white", bold=True))}',
                      f'execute unless score #clr bm.rng matches {need}.. run data modify storage bm:ui p{kind}.r_l{i} set value {snbt([T("🔒 " + nm, "dark_gray")])}',
                      f'execute if score @s {obj} matches {i + 1} run data modify storage bm:ui p{kind}.r_l{i} set value {snbt([T("✔ " + nm, "green", bold=True)])}']
            btns.append(P28.btn(raw(f'r_l{i}'), base_code + 1 + i, tooltip=[T(nm, 'white', bold=True), T('\n' + what, 'gray')] +
                                ([T(f'\nOpens with a Tier {ROMAN[need]} clear.', 'dark_gray')] if need else []), width=110))
        none_code = SEC_NONE if kind == 'sec' else SIG_NONE
        assert none_code not in range(base_code + 1, base_code + 1 + len(opts)), f'{kind}: "none" shares a code with an option'
        btns += [P28.btn(T('none', 'gray'), none_code, width=110), P28.btn(T('« Armory', 'gray'), MENU_CODE + 1, width=110)]
        dlg = P28.multi([T('YOUR SECONDARY' if kind == 'sec' else 'YOUR SIGNATURE', OFFICE, bold=True),
                         T('  ·  a weapon of your own' if kind == 'sec' else '  ·  an effect of your own', 'gray')],
                        [P28.body([T('Comes with whichever kit you take. More open up as you clear tiers. Change it whenever you like.', 'gray')], 340)],
                        btns, columns=3)
        lines.append(f'function bm:p80/{kind}_dlg with storage bm:ui p{kind}')
        fn(f'p80/{kind}_menu', lines)
        fn(f'p80/{kind}_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
        pick = ['function bm:p80/clr', '$scoreboard players set #i bm.rng $(i)']
        for i, o in enumerate(opts):
            pick += [f'execute if score #i bm.rng matches {i + 1} unless score #clr bm.rng matches {o[2]}.. run return run ' + say(f'{o[0]} opens with a Tier {ROMAN[o[2]] if o[2] else "I"} clear.', 'red')]
        pick += [f'scoreboard players operation @s {obj} = #i bm.rng', 'execute at @s run playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 1 1.2']
        pick += [f'execute if score #i bm.rng matches {i + 1} run ' + say(f'{"Secondary" if kind == "sec" else "Signature"}: {o[0]} - {o[1]}. (From your next kit on.)', OFFICE)
                 for i, o in enumerate(opts)]
        pick += ['execute if score #i bm.rng matches 0 run ' + say('None, then.'), 'function bm:p80/armory']
        fn(f'p80/{kind}_pick', pick)
    picker('sec', SECONDARY, MENU_CODE + 20, 'bm.ksec')
    picker('sig', SIGNATURE, MENU_CODE + 30, 'bm.ksig')

    # ================================================================== THE KITS BY RANK
    kit_arg = P72.kit_arg

    def kit_arg_x(iid, role=None, over=None):
        """like phase72's loaner argument, with some components replaced"""
        if not over: return kit_arg(iid, role)
        it = ITEMS[iid]
        saved = it['comps']
        it['comps'] = dict(saved, **over)
        try:
            return kit_arg(iid, role)
        finally:
            it['comps'] = saved
    keep_any = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{t}"}}' for t in P72.KEEP) + ']'
    for r, (nm, col, desc, armor, hand) in P72.ROLES.items():
        for n in range(1, MAXR + 1):
            tier = 3 if n >= 4 else 2 if n >= 2 else 1
            lines = []
            for slot, iid in armor.items():
                if r in ARMOR_SET and iid.startswith(ARMOR_SET[r]) and iid.endswith('_1'):
                    iid = iid[:-2] + f'_{tier}'
                sl = P72.SLOT_OF[slot]
                lines += [f'execute unless items entity @s {sl} * run item replace entity @s {sl} with {kit_arg(iid, r)}',
                          f'execute if items entity @s {sl} {keep_any} run give @s {kit_arg(iid, r)}']
            for h in hand:
                iid, cnt, extra = (h, 1, None) if isinstance(h, str) else (h + (None,))[:3]
                if iid == ABIL_IID[r]:
                    sec = ABIL_CD[r][1 if n >= 3 else 0]
                    lines.append(f'give @s {kit_arg_x(iid, over={"minecraft:use_cooldown": {"seconds": float(sec), "cooldown_group": f"bm:{iid}"}})} 1')
                    continue
                if r == 3 and iid == 'fairy_bow':          # (2.67) the loaner has no Infinity, so the spectral arrows get shot; Flame from Searing Shots
                    en = {k: v for k, v in ITEMS[iid]['comps'].get('minecraft:enchantments', {}).items() if k != 'minecraft:infinity'}
                    if n >= 4: en['minecraft:flame'] = 1
                    lines.append(f'give @s {kit_arg_x(iid, over={"minecraft:enchantments": en})} 1')
                    continue
                if r == 3 and iid == 'minecraft:spectral_arrow' and n >= 2:
                    cnt = 64
                if r == 4 and iid == 'minecraft:splash_potion' and n >= 5:
                    cnt = 5
                lines.append(f'give @s {kit_arg(iid, extra=extra)} {cnt}')
            if r == 3 and n >= 2:
                lines.append(f'give @s {kit_arg("minecraft:tipped_arrow", extra={"minecraft:potion_contents": {"potion": "minecraft:harming"}})} 8')
            lines.append(f'give @s {kit_arg(P72.KIT_FOOD[0])} {P72.KIT_FOOD[1]}')
            if r == 1:
                hp = 16 if n >= 5 else 12 if n >= 2 else 8
                kb = 1.0 if n >= 6 else 0.5
                lines += [f'attribute @s minecraft:max_health modifier add bm:gv_role_tank {hp} add_value',
                          f'attribute @s minecraft:knockback_resistance modifier add bm:gv_role_tank {kb} add_value']
            lines += ['function bm:p80/kit/extras']
            fn(f'p80/kit/give_{r}_{n}', lines)
        G.FUNCS[f'p72/kit/give_{r}'] = [f'execute if score @s bm.kr{r} matches {n} run return run function bm:p80/kit/give_{r}_{n}' for n in range(2, MAXR + 1)] + \
            [f'function bm:p80/kit/give_{r}_1']
    # your secondary and your signature's lasting parts, with every kit
    ext = ['function bm:p80/init_me', 'attribute @s minecraft:max_health modifier remove bm:gv_sig_hp', 'attribute @s minecraft:safe_fall_distance modifier remove bm:gv_sig_fall',
           'execute if score @s bm.ksig matches 2 run attribute @s minecraft:max_health modifier add bm:gv_sig_hp 4 add_value',
           'execute if score @s bm.ksig matches 4 run attribute @s minecraft:safe_fall_distance modifier add bm:gv_sig_fall 5 add_value']
    for i, (snm, what, need, its) in enumerate(SECONDARY, 1):
        ext += [f'execute if score @s bm.ksec matches {i} run give @s {kit_arg(iid, extra=extra)} {cnt}' for iid, cnt, extra in its]
    fn('p80/kit/extras', ext)
    G.FUNCS['p72/kit/strip'] += ['attribute @s minecraft:max_health modifier remove bm:gv_sig_hp', 'attribute @s minecraft:safe_fall_distance modifier remove bm:gv_sig_fall']

        # ---- the ranks' extra blows land even straight after a sword's (their own damage type skips the hurt cooldown)
    wjson('bm/damage_type/kit_strike.json', {'exhaustion': 0.1, 'message_id': 'player', 'scaling': 'when_caused_by_living_non_player'})
    G.wjson('minecraft/tags/damage_type/bypasses_cooldown.json', {'replace': False, 'values': ['bm:kit_strike']})
    G.wjson('minecraft/tags/damage_type/is_player_attack.json', {'replace': False, 'values': ['bm:kit_strike']})
    gap = G.FUNCS['p77/kit/gap']
    gap[0] = gap[0].replace('minecraft:player_attack', 'bm:kit_strike')
    # ---- a used ability comes back with its rank's cooldown
    #      (2.78: handed back a tick later - see useitem.give_back - in the rank's cooldown)
    from useitem import give_back
    for r, iid in ABIL_IID.items():
        L = G.FUNCS[f'p77/kit/{iid}']
        plain = give_back(kit_arg(iid))
        k = L.index(plain[0])
        assert L[k + 1] == plain[1], (iid, L[k:k + 2])
        gbs = [give_back(kit_arg_x(iid, over={'minecraft:use_cooldown': {'seconds': float(ABIL_CD[r][fast_]), 'cooldown_group': f'bm:{iid}'}}))
               for fast_ in (0, 1)]
        L[k:k + 2] = [f'execute if score @s bm.kr{r} matches 3.. run {gbs[1][0]}', f'execute unless score @s bm.kr{r} matches 3.. run {gbs[0][0]}', 'tag @s add bm.gb']
    # ---- the ranks at work
    rk = lambda r, n: f'scores={{bm.gvrole={r},bm.kr{r}={n}..}}'
    # TANK III: spikes while you sneak
    wjson('bm/advancement/p80/hurt.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {}}}, 'rewards': {'function': 'bm:p80/hurt'}})
    fn('p80/hurt', ['advancement revoke @s only bm:p80/hurt', 'execute unless entity @s[tag=bm.gvp] run return 0',
                    'execute if entity @s[scores={bm.gvrole=1,bm.kr1=3..,bm.sneak=1..}] run function bm:p80/kit/spikes'])
    fn('p80/kit/spikes', ['tag @s add bm.kme', 'execute on attacker unless entity @s[type=minecraft:player] run damage @s 3 minecraft:thorns by @a[tag=bm.kme,limit=1]',
                          'execute on attacker at @s run particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 8', 'tag @s remove bm.kme'])
    # TANK IV: the Horn shields the crew; VI: and hurls the guards back
    G.FUNCS['p77/kit/kit_horn_go'] += [f'execute if entity @s[{rk(1, 4)}] run effect give @a[tag=bm.gvp,distance=..8] minecraft:absorption 10 1 true',
                                       f'execute if entity @s[{rk(1, 6)}] run function bm:p80/kit/hurl']
    fn('p80/kit/hurl', ['tag @s add bm.kme', 'execute as @e[tag=bm.gvg,distance=..7] run damage @s 4 bm:kit_strike by @a[tag=bm.kme,limit=1]',
                        'execute as @e[tag=bm.gvg,distance=..7] at @s facing entity @a[tag=bm.kme,limit=1] feet run tp @s ^ ^0.3 ^-1.5',
                        'particle minecraft:gust_emitter_large ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.breeze.wind_burst player @a[distance=..20] ~ ~ ~ 1 0.8', 'tag @s remove bm.kme'])
    # TANK V: Last Stand, once a heist
    second.append(f'execute as @a[tag=bm.gvp,{rk(1, 5)}] unless score @s bm.kls matches 1 if score @s bm.hp matches 1..8 at @s run function bm:p80/kit/last_stand')
    fn('p80/kit/last_stand', ['scoreboard players set @s bm.kls 1', 'effect give @s minecraft:resistance 5 3 true', 'effect give @s minecraft:absorption 10 3 true',
                              'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.4 50', 'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.7 1.2',
                              say('LAST STAND - the Juggernaut will not fall.', ROLE_COL[1])])
    # OFFENSE II: Bloodrush heals more
    G.FUNCS['p77/kit/bloodrush'].append(f'execute if entity @s[{rk(2, 2)}] run effect give @s minecraft:regeneration 4 1 true')
    # OFFENSE III / V / VI: each melee blow (a guard on reentry is ignored)
    wjson('bm/advancement/p80/ohit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'damage': {'type': {'is_direct': True, 'tags': [{'id': '#minecraft:is_projectile', 'expected': False}]}}}}}, 'rewards': {'function': 'bm:p80/ohit'}})
    fn('p80/ohit', ['advancement revoke @s only bm:p80/ohit', 'execute unless entity @s[tag=bm.gvp] run return 0', 'execute if entity @s[tag=bm.kbusy] run return 0', 'execute if entity @s[tag=bm.katk] run return 0',
                    f'execute unless entity @s[{rk(2, 3)}] run return 0', 'tag @s add bm.kbusy', 'tag @s add bm.kme',
                    'execute at @s as @e[type=#bm:hostile,tag=!bm.npc,distance=..6,nbt={HurtTime:10s},sort=nearest,limit=1] at @s run function bm:p80/kit/ohit_t',
                    'tag @s remove bm.kme', 'tag @s remove bm.kbusy', 'advancement revoke @s only bm:p80/ohit'])
    fn('p80/kit/ohit_t', ['execute store result score #h bm.rng run data get entity @s Health 3', 'execute store result score #m bm.rng run attribute @s minecraft:max_health get',
                          'execute if score #h bm.rng < #m bm.rng run function bm:p80/kit/execute',
                          f'execute if entity @a[tag=bm.kme,{rk(2, 5)}] run function bm:p80/kit/count',
                          'execute if entity @a[tag=bm.kme,tag=bm.kphantom] run function bm:p80/kit/phantom_hit'])
    fn('p80/kit/execute', ['damage @s 5 bm:kit_strike by @a[tag=bm.kme,limit=1]', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 6'])
    fn('p80/kit/count', ['scoreboard players add @a[tag=bm.kme] bm.khc 1', 'execute unless score @a[tag=bm.kme,limit=1] bm.khc matches 4.. run return 0',
                         'scoreboard players set @a[tag=bm.kme] bm.khc 0', 'damage @s 6 bm:kit_strike by @a[tag=bm.kme,limit=1]',
                         'particle minecraft:crit ~ ~1 ~ 0.4 0.5 0.4 0.4 24', 'playsound minecraft:entity.player.attack.crit player @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p80/kit/phantom_hit', ['tag @a[tag=bm.kme] remove bm.kphantom', 'damage @s 10 bm:kit_strike by @a[tag=bm.kme,limit=1]',
                               'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.05 20', 'playsound minecraft:entity.phantom.bite player @a[distance=..16] ~ ~ ~ 1 0.8'])
    # OFFENSE IV / VI: the blink
    G.FUNCS['p77/kit/kit_step_go'] += [f'execute if entity @s[{rk(2, 4)}] run function bm:p80/kit/ambush', f'execute if entity @s[{rk(2, 6)}] run function bm:p80/kit/phantom']
    fn('p80/kit/ambush', ['tag @s add bm.kme', 'tag @s add bm.kbusy',
                          'execute at @s as @e[type=#bm:hostile,tag=!bm.npc,distance=..3.5,sort=nearest,limit=1] run damage @s 8 bm:kit_strike by @a[tag=bm.kme,limit=1]',
                          'execute at @s run particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.3 0.6 0 3', 'tag @s remove bm.kbusy', 'tag @s remove bm.kme'])
    fn('p80/kit/phantom', ['effect give @s minecraft:invisibility 4 0 true', 'tag @s add bm.kphantom', say('PHANTOM - your next blow lands for +10.', ROLE_COL[2])])
    # RANGED III: seven arrows; VI: harder, piercing
    G.FUNCS['p77/kit/kit_volley_go'] += [f'execute if entity @s[{rk(3, 3)}] run function bm:p77/kit/arrow {{a:-24}}',
                                         f'execute if entity @s[{rk(3, 3)}] run function bm:p77/kit/arrow {{a:24}}']
    arw = G.FUNCS['p77/kit/arrow']
    arw.insert(len(arw) - 1, f'execute if entity @s[{rk(3, 6)}] run data merge entity @e[type=minecraft:arrow,tag=bm.kva,limit=1,sort=nearest] {{damage:6.0d,PierceLevel:2b}}')
    # RANGED V: Speed II, and bow hits heal
    second.append(f'effect give @a[tag=bm.gvp,{rk(3, 5)}] minecraft:speed 3 1 true')
    G.FUNCS['p77/kit/pin'].append(f'execute if entity @s[{rk(3, 5)}] run effect give @s minecraft:regeneration 2 2 true')
    # SUPPORT II: a wider, stronger aura
    G.FUNCS['p72/kit/mend'][1:1] = [f'execute if entity @s[{rk(4, 2)}] run effect give @a[tag=bm.gvp,tag=!bm.gvself,distance=..12] minecraft:regeneration 3 1 true']
    # SUPPORT III / V / VI: the Ward
    G.FUNCS['p77/kit/kit_tidal_go'] += [f'execute if entity @s[{rk(4, 3)}] run effect give @a[tag=bm.gvp,distance=..8] minecraft:speed 8 0 true',
                                        f'execute if entity @s[{rk(4, 5)}] run effect give @a[tag=bm.gvp,distance=..8] minecraft:resistance 8 0 true',
                                        f'execute if entity @s[{rk(4, 5)}] run effect give @a[tag=bm.gvp,distance=..8] minecraft:strength 8 0 true',
                                        f'execute if entity @s[{rk(4, 6)}] run effect give @a[tag=bm.gvp,distance=..8] minecraft:instant_health 1 1 true',
                                        f'execute if entity @s[{rk(4, 6)}] run function bm:p80/kit/hurl']
    # SUPPORT IV: Lifeline for the crew near you
    second.append(f'execute as @a[tag=bm.gvp,{rk(4, 4)}] at @s as @a[tag=bm.gvp,distance=..12,scores={{bm.hp=1..6}}] unless score @s bm.gvll matches 1.. at @s run function bm:p77/kit/lifeline')
    # signatures, each second in a heist
    sg = lambda i: f'scores={{bm.ksig={i}}}'
    second += [f'effect give @a[tag=bm.gvp,{sg(1)}] minecraft:speed 3 0 true', f'effect give @a[tag=bm.gvp,{sg(3)}] minecraft:night_vision 15 0 true',
               f'effect give @a[tag=bm.gvp,{sg(6)}] minecraft:jump_boost 3 0 true',
               f'scoreboard players add @a[tag=bm.gvp,{sg(8)}] bm.ksgt 1',
               f'execute as @a[tag=bm.gvp,{sg(8)}] if score @s bm.ksgt matches 30.. run function bm:p80/kit/second_skin',
               'execute as @a[tag=bm.gvp,scores={bm.ksig=9,bm.hp=1..10}] run function bm:p80/kit/adrenaline']
    fn('p80/kit/second_skin', ['scoreboard players set @s bm.ksgt 0', 'effect give @s minecraft:absorption 30 0 true'])
    fn('p80/kit/adrenaline', ['effect give @s minecraft:strength 2 0 true', 'effect give @s minecraft:speed 2 0 true'])
    k = next(i for i, l in enumerate(kg) if 'bm:p75/pot_add' in l)
    kg.insert(k, 'execute if score @s bm.ksig matches 7 run scoreboard players add #c bm.rng 1')
    kg.append('execute if score @s bm.ksig matches 5 run effect give @s minecraft:regeneration 2 2 true')

    # ================================================================== THE DEN: the Armory bench and the Bank vault, by the racks
    # (rel() is already a block's centre for a summon - 2.67: the boxes and signs sat half a block off)
    stations = [('arm', 7, 'minecraft:smithing_table', 'THE ARMORY', 'your kits, for good', ROLE_COL[1]),
                ('bank', 5, 'minecraft:vault[facing=north]', 'THE GUTTER BANK', 'coins and spoils', GOLD)]
    den = []
    for key, x, block, label, sub, col in stations:
        den += [f'setblock {rel(x, 4, 21)} {block}',
                f'summon minecraft:interaction {rel(x, 4, 21)} {snbt({"Tags": ["bm.gvprop", "bm.ofhit", "bm.of_" + key], "width": F(1.02), "height": F(1.02), "response": B(1)})}',
                f'summon minecraft:text_display {rel(x, 5.3, 21)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(1879048192),
                                                                                  'text': [T(label + '\n', col, bold=True), T(sub, 'gray')],
                                                                                  'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                     'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})]
    G.FUNCS['p70/r/lobby/init'] += den
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.ofhit] if data entity @s interaction at @s run function bm:p80/den_click')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.ofhit] if data entity @s attack run data remove entity @s attack')
    fn('p80/den_click', ['tag @s add bm.ofme', 'execute on target run function bm:p80/den_who', 'tag @s remove bm.ofme', 'data remove entity @s interaction'])
    fn('p80/den_who', ['execute if entity @e[type=minecraft:interaction,tag=bm.ofme,tag=bm.of_arm] run return run function bm:p80/armory',
                       'execute if entity @e[type=minecraft:interaction,tag=bm.ofme,tag=bm.of_bank] run return run function bm:p80/bank'])

    # ================================================================== admin
    fn('admin/office_items', [give('fixers_ledger')] + [give(m[0], 32) for m in MATS] + [give('gutter_coin', 64)])
    fn('admin/kits_max', [f'scoreboard players set @s bm.kr{r} {MAXR}' for r in range(1, 5)] + ['scoreboard players set @s bm.gvcl 62',
                                                                                              tellraw('@s', PREFIX + [T('Every kit at rank VI; every tier cleared.', 'gray')])])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    g = R.grid
    R.ICONS['copper_cog'] = g(['................', '......oo........', '...o.oCCo.o.....', '..oCoCCCCoCo....', '...oCCddCCo.....', '..oCCd..dCCo....', '.oCCd....dCCo...',
                               '..oCCd..dCCo....', '...oCCddCCo.....', '..oCoCCCCoCo....', '...o.oCCo.o.....', '......oo........', '................', '................',
                               '................', '................'], dict(o='#7a3a18', C='#d9824a', d='#a85a2a'))
    R.ICONS['silver_seal'] = g(['................', '.....ssssss.....', '...ssSSSSSSss...', '..sSSwSSSSSSSs..', '..sSSSkkkkSSSs..', '.sSSSkSSSSkSSSs.', '.sSSSkSkkSkSSSs.',
                                '.sSSSkSkkSkSSSs.', '.sSSSkSSSSkSSSs.', '..sSSSkkkkSSSs..', '..sSSSSSSSSSSs..', '...ssSSSSSSss...', '.....ssssss.....', '................',
                                '................', '................'], dict(s='#6a7078', S='#c8d0d8', w='#ffffff', k='#7a8088'))
    R.ICONS['gilded_leaf'] = g(['................', '..........yy....', '........yYYy....', '.......yYYYy....', '......yYYwYy....', '.....yYYYYy.....', '....yYYdYYy.....',
                                '....yYdYYy......', '...yYdYYy.......', '...yYYYy........', '..yydyy.........', '..d.............', '.d..............', '................',
                                '................', '................'], dict(y='#b88a18', Y='#ffd84a', w='#fff6c0', d='#8a6410'))
    R.ICONS['deep_pearl'] = g(['................', '................', '.....tttttt.....', '....tTTTTTTt....', '...tTwwTTTTTt...', '...tTwTTTTTTt...', '...tTTTTTTTTt...',
                               '...tTTTTTTdTt...', '...tTTTTTddTt...', '....tTTTddTt....', '.....tttttt.....', '................', '................', '................',
                               '................', '................'], dict(t='#1e7a70', T='#4ad0c0', w='#d8fff8', d='#2e9a8e'))
    R.ICONS['hoard_ember'] = g(['................', '.......r........', '......rOr.......', '.....rOYOr......', '....rOYwYOr.....', '....rOYYYOr.....', '...rkOOYOOkr....',
                                '...kkrOOOrkk....', '..kkkkrrrkkkk...', '..kKkkkkkkKkk...', '...kkkKkkkkk....', '....kkkkkkk.....', '................', '................',
                                '................', '................'], dict(r='#c03010', O='#ff8a30', Y='#ffd040', w='#fff8c0', k='#2a1a14', K='#4a2a1a'))
    R.ICONS['captains_insignia'] = g(['................', '..pp........pp..', '..pPp......pPp..', '...pPp....pPp...', '....pPpppPPp....', '.....pPPPPp.....', '....yyyyyyyy....',
                                      '...yYYYYYYYYy...', '...yYwYYYYYYy...', '...yYYYrrYYYy...', '...yYYrrrrYYy...', '...yYYYrrYYYy...', '....yYYYYYYy....', '.....yyyyyy.....',
                                      '................', '................'], dict(p='#5a2a8a', P='#c060ff', y='#b88a18', Y='#ffd84a', w='#fff6c0', r='#c03030'))
    R.ICONS['fixers_ledger'] = g(['................', '..kkkkkkkkkkk...', '..kBBBBBBBBBkw..', '..kBYYYYYYYBkw..', '..kBYBBBBBYBkw..', '..kBBBBBBBBBkw..', '..kBBYYYYYBBkw..',
                                  '..kBBBBBBBBBkw..', '..kBBBYrYBBBkw..', '..kBBBBrBBBBkw..', '..kBBBBBBBBBkw..', '..kBBBBBBBBBkw..', '..kkkkkkkkkkkw..', '...wwwwwwwwwww..',
                                  '................', '................'], dict(k='#2a1a10', B='#6a3a1a', Y='#e8c070', r='#c03030', w='#e8dcc0'))
