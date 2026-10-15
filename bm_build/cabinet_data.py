"""2.79: FISHY'S CABINET OF CURIOSITIES - the catalogue. Six wings of twenty exhibits each.

An exhibit is (key, [item ids that count as it], riddle). Shown one of the ids, Fishy makes a replica for his cabinet - the
thing itself stays with whoever showed it. The riddle stands on a veiled plinth until someone does: a hint at where the
thing is found, in his flowery hand. (Each id belongs to one exhibit only; the build checks it.)"""

WINGS = [
    ('hollow', 'The Hollow', '#a89ad8', 'The Hollow Throne, the five conquests and the serpent beneath them.'),
    ('gutter', 'The Gutter', '#ffcf40', 'What the Gilded Gutter Vault gives up to a crew that wins.'),
    ('skies', 'The Skies', '#7ae0ff', 'The Vorn, the Donadians and the storms.'),
    ('deep', 'The Deep', '#3ab0c8', 'The sea, the drowned and the sunken kingdom.'),
    ('wilds', 'The Wilds', '#7ad06a', 'The roaming bosses, the Blood Moon and the luck of the open world.'),
    ('court', 'The Court', '#ff8ad8', 'The tokens of every follower, and the gifts of their friendship.'),
]

EXHIBITS = {
    'hollow': [
        ('trophy_hollow', ['trophy_hollow'], 'The trophy of a king who fell on his own throne.'),
        ('emblem_hollow', ['emblem_hollow'], 'Every seal broken, every throne empty - and this to prove it.'),
        ('trophy_keep', ['trophy_keep'], "Proof of a keep conquered - its lord's old friend, Bobbery, made a trophy."),
        ('trophy_brood', ['trophy_brood'], 'Taken from the mother of a nest of silk and bone.'),
        ('trophy_frost', ['trophy_frost'], 'A huntsman of the frozen spire, never to draw again.'),
        ('trophy_hex', ['trophy_hex'], 'The archmage of a hexbound cathedral, bested.'),
        ('trophy_tide', ['trophy_tide'], 'A tyrant who ruled a throne beneath the waves.'),
        ('wilfrey_aegis', ['wilfrey_aegis'], 'It held the line against the Hollow King.'),
        ('oathblade', ['oathblade'], '"I chose the world," says the blade.'),
        ('blink_tome', ['blink_tome'], 'Hidden in the Hollow: a book that skips you forward.'),
        ('horseshoe_charm', ['horseshoe_charm'], 'Hidden in the Hollow: luck for your off hand.'),
        ('hollow_warpstone', ['hollow_warpstone'], "The King's own key, taken from his throne."),
        ('hollow_wings', ['hollow_wings'], "Torn from the Hollow King's back."),
        ('sepulchre', ['sepulchre'], 'A maul; every grave it struck stayed open.'),
        ('hollow_crown', ['hollow_crown'], 'A crown lighter than it ought to be.'),
        ('music_disc_hollow', ['music_disc_hollow'], 'A record hidden somewhere in the Hollow Throne.'),
        ('apophiss_crown', ['apophiss_crown'], "A serpent's black crown. Its emerald watches."),
        ('apo_true_crown', ['apo_true_crown'], 'The crown the Hollow King only ever wore the shadow of.'),
        ('apo_mace', ['apo_mace', 'apo_mace_sword', 'apo_mace_axe', 'apo_mace_pickaxe', 'apo_mace_shovel', 'apo_mace_hoe', 'apo_mace_trident'],
         'The end of a serpent king\'s tail, black spikes and white crescents.'),
        ('conq_helmet', ['conq_helmet'], 'The face the Hollow King wore to battle.'),
    ],
    'gutter': [
        ('the_alibi', ['the_alibi'], '"I was never there." A legendary find from a won heist.'),
        ('counterfeiters_press', ['counterfeiters_press'], 'A little iron press, still inky. Mythical.'),
        ('forgeheart', ['forgeheart'], 'A coal heart from the Hoard. It never cools.'),
        ('merchants_bell', ['merchants_bell'], 'Ring it and the villages restock. Tier I, mythical.'),
        ('tinkers_thimble', ['tinkers_thimble'], 'What you wear slowly mends. Tier II, mythical.'),
        ('fizzle_stone', ['fizzle_stone'], 'Creepers fizzle out near it. Tier III, mythical.'),
        ('wayfarers_lodestar', ['wayfarers_lodestar'], 'Mark a spot; come back to it. Tier IV, mythical.'),
        ('phoenix_plume', ['phoenix_plume'], 'It smoulders and never burns away. Tier V, mythical.'),
        ('songbird', ['songbird'], 'Music notes dance about your head. Tier I, legendary.'),
        ('firefly_jar', ['firefly_jar'], 'Fireflies drift and blink about you. Tier II, legendary.'),
        ('honeycomb_brooch', ['honeycomb_brooch'], 'Honey drips from your shoulders. Tier III, legendary.'),
        ('trial_key_fob', ['trial_key_fob'], 'Streams of light spiral in. Tier IV, legendary.'),
        ('gale_locket', ['gale_locket'], 'Little gusts whirl about your feet. Tier V, legendary.'),
        ('echo_bell', ['echo_bell'], "A bat's collar bell, from the Gutter Gentry."),
        ('blob_cane', ['blob_cane'], "A Count's cane, black lacquer and a silver tip."),
        ('yolkshell_helm', ['yolkshell_helm'], 'A cap of cracked egg shell, still sticky.'),
        ('frisbee_shield', ['frisbee_shield'], 'Shield, plate, frisbee - found only in the Gutter.'),
        ('music_disc_big_score', ['music_disc_big_score'], 'A record in a heist haul, once in a long while.'),
        ('pearl_bell', ['pearl_bell'], 'One ring and a penguin waddles over.'),
        ('laurel_t5', ['laurel_t5'], 'Worn by those who first won the deepest tier.'),
    ],
    'skies': [
        ('donadian_medal', ['donadian_medal'], 'For defending a Donadian mothership from the Vorn.'),
        ('ray_gun', ['ray_gun'], 'Pew. It runs on green crystals.'),
        ('shrink_ray', ['shrink_ray'], 'Makes big things small.'),
        ('growth_ray', ['growth_ray'], 'Makes small things big.'),
        ('plasma_blaster', ['plasma_blaster'], 'Taken from a Vorn trooper, twice as quick as a ray gun.'),
        ('quake_maul', ['quake_maul'], "The Dreadnought's war hammer."),
        ('vorn_drill', ['vorn_drill'], 'Vorn mining, the hard way.'),
        ('dimension_shifter', ['dimension_shifter'], 'Donadian travel tech. Fragile. Loud.'),
        ('gravitic_core', ['gravitic_core'], "The Overseer's anti-gravity heart."),
        ('overcharged_beacon', ['overcharged_beacon'], 'A distress beacon, wired wrong on purpose.'),
        ('xeno_visor', ['xeno_visor'], 'Vorn targeting optics.'),
        ('xenite_altar', ['xenite_altar'], 'Lifted from a crash site, shards and all.'),
        ('skiff_key', ['skiff_key'], 'A saucer that answers to you.'),
        ('skiff_reactor', ['skiff_reactor'], 'Part six of six, salvaged from mothership stores.'),
        ('tractor_beam', ['tractor_beam'], 'Pulls what you look at.'),
        ('cloaking_device', ['cloaking_device'], 'Forty-five seconds of nobody.'),
        ('music_disc_invasion', ['music_disc_invasion'], 'Pried off a Vorn on invasion night.'),
        ('killerwatt_tendrils', ['killerwatt_tendrils'], 'Torn from a storm that walks on many legs.'),
        ('ethereal_tendrils', ['ethereal_tendrils'], 'The same storm, gone ghostly.'),
        ('demo_scythe', ['demo_scythe'], 'Won from the storm reaper himself, in a fair fight.'),
    ],
    'deep': [
        ('tul_blunderbuss', ['tul_blunderbuss'], "A drowned captain's gun, rimed with frost."),
        ('tul_harpoon', ['tul_harpoon'], 'A barbed harpoon on a frozen rope.'),
        ('leo_trident', ['leo_trident', 'leo_spear'], "A knight's trident of blue steel and sea-glass."),
        ('tidal_tear', ['tidal_tear'], 'A drop of the deep sea, holding a garnet.'),
        ('blue_marlin', ['blue_marlin'], "A marlin's bill, honed to a razor."),
        ('kraken_conch', ['kraken_conch'], 'Blow it in the water and something BIG answers.'),
        ('abyssal_helm', ['abyssal_helm'], 'Salvaged from a drowned captain.'),
        ('tyrant_trident', ['tyrant_trident'], 'It returns. It always returns.'),
        ('pearl_sigil_1', ['pearl_sigil_1'], 'The first of three sigils a tyrant demands.'),
        ('pearl_sigil_2', ['pearl_sigil_2'], 'The second of three sigils a tyrant demands.'),
        ('pearl_sigil_3', ['pearl_sigil_3'], 'The last of three sigils a tyrant demands.'),
        ('key_tide', ['key_tide'], 'Still dripping, somehow. It opens a coral throne.'),
        ('emblem_tide', ['emblem_tide'], 'An emblem won from the drowned tyrant.'),
        ('gold_doubloon', ['gold_doubloon'], 'Pirate gold. Cursed? Lucky? Both.'),
        ('water_walking_boots', ['water_walking_boots'], 'A treasure of the wide world: stride across the sea.'),
        ('message_bottle', ['message_bottle'], 'A scroll in a bottle, washed up.'),
        ('zora_trident', ['zora_trident'], 'Returns faster than a boomerang.'),
        ('pirate_cutlass', ['pirate_cutlass'], 'Curved, notched and very well loved.'),
        ('rat_banner_pirate', ['rat_banner_pirate'], 'The colours of Captain Cheddarbeard.'),
        ('rat_shield_pirate', ['rat_shield_pirate'], "Captain Cheddarbeard's shield. Mostly dent-free."),
    ],
    'wilds': [
        ('horseman_head', ['horseman_head', 'soul_head', 'venom_head', 'hallowed_head'], 'A grinning head, taken from a rider who had none.'),
        ('pharaoh_crook', ['pharaoh_crook', 'crook_ra', 'crook_sands', 'crook_sun'], 'Gold and lapis, from a king of the sands.'),
        ('storm_talon', ['storm_talon', 'talon_chain', 'talon_static', 'talon_wind'], 'A talon of a great bird of storms, crackling still.'),
        ('heartwood_branch', ['heartwood_branch', 'branch_bark', 'branch_bloom', 'branch_seed'], "A living branch from an elder tree's heart."),
        ('molten_gauntlet', ['molten_gauntlet', 'gauntlet_hearth', 'gauntlet_magma', 'gauntlet_obsidian'], "A colossus's molten core, made a fist."),
        ('void_scepter', ['void_scepter', 'scepter_phase', 'scepter_rift', 'scepter_star'], "A walker of the void's eye, set on a rod."),
        ('scorching_heart', ['scorching_heart'], 'The heart of a lantern on eight legs. It never stops burning.'),
        ('ravenous_heart', ['ravenous_heart'], 'Torn from the Blood Moon Monstrosity. Still hungry.'),
        ('sanguine_fang', ['sanguine_fang'], 'A tooth from a Blood Moon horror.'),
        ('specter_charm', ['specter_charm'], 'Nine shrouds, stitched into one.'),
        ('crimson_effigy', ['crimson_effigy'], 'Use it and the moon turns red tonight.'),
        ('moon_pact', ['moon_pact'], 'A contract signed in something red.'),
        ('vampire_mirror', ['vampire_mirror'], 'It shows the room, but never you.'),
        ('music_disc_blood_moon', ['music_disc_blood_moon'], 'Dropped by the riders of Blood Moon steeds.'),
        ('music_disc_lucky', ['music_disc_lucky'], 'Dropped by something lucky on a Lucky Night.'),
        ('fallen_star', ['fallen_star'], 'Still warm from the sky.'),
        ('pot_of_gold', ['pot_of_gold'], 'Dropped by a rat in green.'),
        ('lucky_trophy', ['lucky_trophy'], 'Taken from the Golden Goose itself.'),
        ('trophy_lucky', ['trophy_lucky'], 'Proof you conquered the Gilded Roost.'),
        ('golden_cheese_wheel', ['golden_cheese_wheel'], "The Rat King's prize. Nobody goes hungry near it."),
    ],
    'court': [
        ('cecil_gem', ['cecil_gem'], "A wizard's summoning gem."),
        ('emma_ribbon', ['emma_ribbon'], "A girl's pink ribbon. She comes when you use it."),
        ('celi_charm', ['celi_charm'], 'A moon charm, from a fierce friend in the snow.'),
        ('leo_crest', ['leo_crest'], 'A blue badge: a crescent, a drop of sea, a pink gem.'),
        ('demo_seal', ['demo_seal'], "The green crystal of a reaper's scythe, in golden claws."),
        ('kw_spark', ['kw_spark'], 'A spark from a storm that chose to follow you.'),
        ('apo_oath', ['apo_oath'], 'An oath sworn by a serpent king.'),
        ('tul_coin', ['tul_coin'], 'A gold coin of the sunken kingdom, iced over.'),
        ('frog_signet', ['frog_signet'], 'The signet of a frog knight. Distinguished.'),
        ('donado_tag', ['donado_tag'], 'A bent tin tag: SPECIMEN 042, scratched out.'),
        ('pearl_card', ['pearl_card'], 'Embossed. Smells faintly of fish. (Not mine.)'),
        ('wilfrey_locket', ['wilfrey_locket'], 'A silver locket from a quiet grave.'),
        ('pearl_statue', ['pearl_statue'], 'Solid gold, tipping his hat - for buying all nine gems.'),
        ('ethereal_gem', ['ethereal_gem'], 'Nine made one. It is warm, and it sings.'),
        ('wraithfire_heart', ['wraithfire_heart'], 'A burning heart, quenched in a gem\'s light.'),
        ('bloomheart_gem', ['bloomheart_gem'], 'A gem that grew in a flower instead of a mine.'),
        ('emma_doll', ['emma_doll'], 'A chibi doll, mid-twirl.'),
        ('golden_donado', ['golden_donado'], 'Solid gold. Monsters cannot stand to look at it.'),
        ('rat_king_signet', ['rat_king_signet'], 'The seal on every deal that matters.'),
        ('music_disc_market', ['music_disc_market'], "From Old Barnaby's crate of records."),
    ],
}

# Fishy's powers, one per wing finished (the world's cabinet, so every Fishy learns them) - and the capstone
POWERS = {
    'hollow': ('Hollow Grip', 'his claws wither what they strike, and hit harder'),
    'gutter': ('Coin Toss', 'he flings gold coins at foes up to 10 blocks off'),
    'skies': ('Ray Zap', 'a Vorn ray from his bowl at foes up to 16 blocks off'),
    'deep': ('Bowl Splash', 'a jet of water shoves foes back and slows them; in water he is quick, and you breathe'),
    'wilds': ('Thunder Exhibit', 'every sixth blow, a thunderclap round him'),
    'court': ('Grand Company', 'you and your followers near him mend (Regeneration) and stand firm (Resistance)'),
}
GRAND = ('The Grand Exhibition', 'now and then spectral replicas of the cabinet\'s pieces wheel round him and burst on every foe near')
CAPSTONE = ('The Golden Bowl', 'his bowl and limbs turn gold, and he is far tougher')


def keys():
    return [k for w, *_ in WINGS for k, _ids, _r in EXHIBITS[w]]


def check(ITEMS):
    seen = {}
    for w, *_ in WINGS:
        assert len(EXHIBITS[w]) == 20, (w, len(EXHIBITS[w]))
        for k, ids, _r in EXHIBITS[w]:
            for i in ids:
                assert i in ITEMS, (w, k, i)
                assert i not in seen, (i, seen.get(i), k)
                seen[i] = k
    assert len(set(keys())) == len(keys())
    return seen
