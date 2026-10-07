"""1.10 price rebalance, applied inside gen_dp.offer() so every shop (base game, Phase 1.5-1.9, Phase 2) uses it.

Currency ladder (unchanged): 1 Medallion = 9 Tokens, 1 Trophy = 6 Medallions (54 Tokens). The pawn shop pays half.
Rules:
- UNBREAKABLE gear is the most expensive thing in the market: it never has to be replaced, so it is priced in Trophies.
- Tier upgrades cost the same at every armourer: tier II = +10 Medallions (armour) / +12 (weapons, tools), tier III = +5 Trophies.
- 1.11: utility and cosmetic boots went back to Medallions; the OP tiers, the elytras and the Bloodforge Sigil carry the price.
- No loops: buying a currency anywhere costs the same as at the Fence, and the Bloodbroker's Trophy is no longer half price.
"""
CUR = {'token', 'medallion', 'trophy', 'lucky_token', 'blood_crystal'}

# item sold -> (cost A, cost B or None). Final prices: these are NOT run through the 1.5x price scale.
DIRECT = {
    'grave_charm': (('token', 10), None),                 # 2.29: an early-game purchase, exactly 10 Tokens
    'golden_wings': (('trophy', 10), None),               # unbreakable elytra, +4 armour
    'dragon_wings': (('trophy', 12), ('dragon_head', 1)),  # unbreakable elytra, +5 armour, fire immunity (1.10)
    'bloodforge_sigil': (('blood_crystal', 48), ('trophy', 1)),   # makes anything unbreakable (and costs a heart, 1.11)
    # 1.11: utility/cosmetic boots are not OP - back to Medallions
    'pegasus_boots': (('medallion', 4), None),
    'bouncy_boots': (('medallion', 3), None),
    'flame_boots': (('medallion', 2), None),
    'heart_boots': (('medallion', 2), None),
    'soul_boots': (('medallion', 2), None),
    # 2.20: full Protection VI netherite sets with set bonuses are Trophy goods, not gold-and-Medallion goods
    'solar_helmet': (('trophy', 2), ('medallion', 10)), 'solar_chestplate': (('trophy', 3), ('medallion', 14)),
    'solar_leggings': (('trophy', 3), ('medallion', 12)), 'solar_boots': (('trophy', 2), ('medallion', 10)),
    'vampire_helmet': (('blood_crystal', 12), ('trophy', 2)), 'vampire_chestplate': (('blood_crystal', 16), ('trophy', 3)),
    'vampire_leggings': (('blood_crystal', 14), ('trophy', 3)), 'vampire_boots': (('blood_crystal', 12), ('trophy', 2)),
    'crimson_helmet': (('blood_crystal', 10), ('trophy', 1)), 'crimson_chestplate': (('blood_crystal', 14), ('trophy', 2)),
    'crimson_leggings': (('blood_crystal', 12), ('trophy', 2)), 'crimson_boots': (('blood_crystal', 10), ('trophy', 1)),
}
# (item sold, currency paid) -> cost: currency exchanges
EXCHANGE = {('medallion', 'token'): ('token', 9),            # the Captain sold them for 8 (Fence: 9)
            ('trophy', 'blood_crystal'): ('blood_crystal', 48)}   # was 24 (= 3 Medallions' worth for a 6-Medallion Trophy)
SPECIALTY = ('shadowstep_', 'juggernaut_', 'architect_helmet', 'architect_chestplate', 'architect_leggings', 'architect_boots',
             'tidecaller_')


def apply(buy, sell, buyB):
    """-> (buy, buyB, scale_buy, scale_buyB)"""
    s = sell[0]
    if s in DIRECT and buy[0] in CUR:
        a, b = DIRECT[s]
        return a, b, False, False
    if s in CUR and (s, buy[0]) in EXCHANGE:
        return EXCHANGE[(s, buy[0])], buyB, False, True
    if buyB and buy[0] not in CUR and buyB[0] in ('medallion', 'trophy') and is_upgrade(s):   # every tier upgrade (1.11)
        return buy, upgrade_cost(s, buyB[0]), True, False
    if s.startswith(('crimson_', 'vampire_')) and buyB and buyB[0] == 'medallion':   # Blood Moon armour sets
        return buy, ('medallion', 8 if s.startswith('crimson_') else 10), True, False
    return buy, buyB, True, True


def is_upgrade(iid):
    import items as I
    return any(to == iid for _, _, _, to in I.UPGRADES)


ARMOR = ('_helmet', '_chestplate', '_leggings', '_boots', '_helmet_2', '_chestplate_2', '_leggings_2', '_boots_2',
         '_helmet_3', '_chestplate_3', '_leggings_3', '_boots_3')


def upgrade_cost(iid, cur):
    """Tier II: +10 Medallions (armour) / +12 (weapons, tools). Tier III: +5 Trophies (+6 for Biggoron's Sword)."""
    if cur == 'trophy': return ('trophy', 6 if iid == 'biggoron_sword' else 5)
    return ('medallion', 10 if iid.endswith(ARMOR) else 12)


def pawn(iid, price):
    """What the pawn shop pays: half the purchase price, never a whole Trophy for a one-Trophy item."""
    cur, n = DIRECT[iid][0] if iid in DIRECT else price
    import items as I
    if any(to == iid for _, _, _, to in I.UPGRADES): cur, n = upgrade_cost(iid, cur)
    if cur == 'trophy' and n // 2 < 1: return ('medallion', 3)
    return (cur, max(1, n // 2))
