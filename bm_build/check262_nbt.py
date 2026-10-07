"""Field-level check of entity NBT in summon/data merge commands, from SpyglassMC vanilla-mcdoc (26.x) schemas."""
import glob, re, sys
import check262 as C
ENTITY = {'Air', 'CustomName', 'CustomNameVisible', 'FallDistance', 'Fire', 'Glowing', 'HasVisualFire', 'Invulnerable', 'Motion', 'NoGravity',
          'OnGround', 'Passengers', 'PortalCooldown', 'Pos', 'Rotation', 'Silent', 'Tags', 'TicksFrozen', 'UUID', 'data'}
LIVING = {'Health', 'Brain', 'attributes', 'active_effects', 'AbsorptionAmount', 'equipment'}
MOB = {'drop_chances', 'DeathLootTable', 'DeathLootTableSeed', 'CanPickUpLoot', 'PersistenceRequired', 'LeftHanded', 'NoAI', 'leash',
       'home_radius', 'home_pos'}
VILLAGER = {'Inventory', 'Offers', 'VillagerData', 'VillagerDataFinalized', 'FoodLevel', 'Gossips', 'LastGossipDecay', 'LastRestock',
            'RestocksToday', 'Xp', 'Age', 'ForcedAge', 'InLove', 'LoveCause', 'AgeLocked'}
TRADER = {'Inventory', 'Offers', 'DespawnDelay', 'wander_target', 'Age', 'ForcedAge'}
DISPLAY = {'transformation', 'interpolation_duration', 'start_interpolation', 'teleport_duration', 'billboard', 'brightness', 'view_range',
           'width', 'height', 'shadow_radius', 'shadow_strength', 'glow_color_override', 'item', 'item_display'}
ALLOWED = {'villager': ENTITY | LIVING | MOB | VILLAGER, 'wandering_trader': ENTITY | LIVING | MOB | TRADER,
           'item_display': ENTITY | DISPLAY, 'block_display': ENTITY | DISPLAY | {'block_state'},   # display.mcdoc BlockDisplay
           'warden': ENTITY | LIVING | MOB | {'anger'},
           'creeper': ENTITY | LIVING | MOB | {'powered', 'ExplosionRadius', 'Fuse', 'ignored'}, 'mob': ENTITY | LIVING | MOB}
BREEDABLE = {'Age', 'ForcedAge', 'AgeLocked', 'InLove', 'LoveCause'}
HORSE = BREEDABLE | {'Bred', 'EatingHaystack', 'Tame', 'Temper', 'Owner'}          # mcdoc HorseBase (26.x)
ALLOWED.update({'zombie_horse': ENTITY | LIVING | MOB | HORSE, 'horse': ENTITY | LIVING | MOB | HORSE | {'Variant'},
                'skeleton_horse': ENTITY | LIVING | MOB | HORSE | {'SkeletonTrap', 'SkeletonTrapTime'},
                'camel_husk': ENTITY | LIVING | MOB | HORSE | {'IsSitting', 'LastPoseTick'},      # dispatches to Camel
                'zombie_nautilus': ENTITY | LIVING | MOB | BREEDABLE | {'Owner', 'Sitting'}})  # Tamable: no Tame field
PROJ = {'HasBeenShot', 'Owner', 'LeftOwner'}
ARROW = PROJ | {'shake', 'pickup', 'life', 'damage', 'inGround', 'inBlockState', 'crit', 'weapon', 'PierceLevel', 'SoundEvent', 'item'}
ZOMBIE = {'IsBaby', 'CanBreakDoors', 'DrownedConversionTime', 'InWaterTime'}
ALLOWED.update({'chicken': ENTITY | LIVING | MOB | BREEDABLE | {'IsChickenJockey', 'EggLayTime', 'variant', 'sound_variant'},
                'zombie': ENTITY | LIVING | MOB | ZOMBIE, 'husk': ENTITY | LIVING | MOB | ZOMBIE, 'drowned': ENTITY | LIVING | MOB | ZOMBIE,
                'arrow': ENTITY | ARROW, 'spectral_arrow': ENTITY | ARROW | {'Duration'},
                'snowball': ENTITY | PROJ | {'Item'}, 'egg': ENTITY | PROJ | {'Item'},
                'evoker_fangs': ENTITY | {'Warmup', 'Owner'}, 'marker': ENTITY,
                'pufferfish': ENTITY | LIVING | MOB | {'FromBucket', 'PuffState'},   # vanilla-mcdoc mob/fish.mcdoc
                'wither': ENTITY | LIVING | MOB | {'Invul'},
                'rabbit': ENTITY | LIVING | MOB | BREEDABLE | {'RabbitType', 'MoreCarrotTicks'},     # mob/rabbit.mcdoc (2.18: the Mimic)
                'phantom': ENTITY | LIVING | MOB | {'size', 'anchor_pos'},
                'endermite': ENTITY | LIVING | MOB | {'Lifetime'},                                          # (2.32: verified on 26.3)                                   # mob/phantom.mcdoc (1.21.5+)
                'piglin': ENTITY | LIVING | MOB | {'IsImmuneToZombification', 'TimeInOverworld', 'IsBaby', 'CannotHunt', 'Inventory'},
                'item': ENTITY | {'Age', 'Health', 'PickupDelay', 'Owner', 'Thrower', 'Item'},                 # entity/item.mcdoc
                'text_display': ENTITY | DISPLAY | {'text', 'line_width', 'text_opacity', 'background', 'default_background', 'shadow',
                                                    'see_through', 'alignment'},                                  # display.mcdoc TextDisplay
                'armor_stand': ENTITY | LIVING | {'Invisible', 'Marker', 'NoBasePlate', 'ShowArms', 'Small', 'DisabledSlots', 'Pose'},  # mob/armor_stand.mcdoc
                'interaction': ENTITY | {'width', 'height', 'response', 'attack', 'interaction'},          # entity/interaction.mcdoc
                'magma_cube': ENTITY | LIVING | MOB | {'Size', 'wasOnGround'},                        # mob/slime.mcdoc CubeMob
                'slime': ENTITY | LIVING | MOB | {'Size', 'wasOnGround'},                             # (2.13: same CubeMob fields; 'Size' verified on 26.3)
                'cushion': ENTITY | {'color', 'block_pos'},
                'experience_orb': ENTITY | {'Value', 'Count', 'Age', 'Health'},          # (2.20: field names read from the 26.3 ExperienceOrb class)
                'tnt': ENTITY | {'fuse', 'explosion_power', 'block_state', 'owner'},                     # (2.14: verified on 26.3)                                            # (2.13: verified on 26.3 - a seat that needs a block under it)
                'piglin_brute': ENTITY | LIVING | MOB | {'IsImmuneToZombification', 'TimeInOverworld'},  # mob/piglin.mcdoc PiglinBase
                'hoglin': ENTITY | LIVING | MOB | BREEDABLE | {'IsImmuneToZombification', 'CannotBeHunted', 'TimeInOverworld'}})
RECIPE = {'rewardExp', 'maxUses', 'uses', 'buy', 'buyB', 'sell', 'xp', 'priceMultiplier', 'specialPrice', 'demand'}
EFFECT = {'id', 'amplifier', 'duration', 'ambient', 'show_particles', 'show_icon', 'hidden_effect'}
SLOTS = {'mainhand', 'offhand', 'head', 'chest', 'legs', 'feet', 'body', 'saddle'}
errs = []

def stack(st, where, cost=False):
    if set(st) - {'id', 'count', 'components'}: errs.append(f'{where}: item stack keys {set(st)}')
    C.check_item_id(st['id'], where)
    if not (1 <= st.get('count', 1) <= 99): errs.append(f'{where}: count')
    for k, v in st.get('components', {}).items():
        if k.startswith('!'):
            if cost: errs.append(f'{where}: removal in ItemCost')
            continue
        try: C.check_component(k, v, where)
        except C.PErr as e: errs.append(str(e))

def entity(kind, nbt, where):
    allowed = ALLOWED.get(kind, ALLOWED['mob'])
    for k in nbt:
        if k not in allowed: errs.append(f'{where}: {kind} has no field {k!r}')
    if 'CustomName' in nbt: C.check_text(nbt['CustomName'], where)
    for e in nbt.get('active_effects', []):
        if set(e) - EFFECT: errs.append(f'{where}: effect keys {set(e)}')
        if C.strip_ns(e['id']) not in C.REG['mob_effect']: errs.append(f'{where}: effect {e["id"]}')
    for a in nbt.get('attributes', []):
        if set(a) - {'id', 'base', 'modifiers'}: errs.append(f'{where}: attribute keys')
        if C.strip_ns(a['id']) not in C.REG['attribute']: errs.append(f'{where}: attribute {a["id"]}')
    for s in nbt.get('drop_chances', {}):
        if s not in SLOTS: errs.append(f'{where}: drop slot {s}')
    for m, v in nbt.get('Brain', {}).get('memories', {}).items():
        if C.strip_ns(m) not in C.REG['memory_module_type']: errs.append(f'{where}: memory {m}')
        if set(v) - {'value', 'ttl'}: errs.append(f'{where}: memory keys')
    if 'variant' in nbt and kind == 'chicken' and C.strip_ns(nbt['variant']) not in C.REG['chicken_variant']: errs.append(f'{where}: chicken variant {nbt["variant"]}')
    if kind in ('arrow', 'spectral_arrow') and 'pickup' in nbt and nbt['pickup'] not in (0, 1, 2): errs.append(f'{where}: arrow pickup')
    if 'Item' in nbt and isinstance(nbt['Item'], dict): stack(nbt['Item'], where + ' Item')
    if 'VillagerData' in nbt:
        vd = nbt['VillagerData']
        if set(vd) - {'level', 'profession', 'type'}: errs.append(f'{where}: VillagerData keys')
    for r in nbt.get('Offers', {}).get('Recipes', []):
        if set(r) - RECIPE: errs.append(f'{where}: recipe keys {set(r) - RECIPE}')
        stack(r['buy'], where + ' buy', True); stack(r['sell'], where + ' sell')
        if 'buyB' in r: stack(r['buyB'], where + ' buyB', True)
    if 'item' in nbt: stack(nbt['item'], where + ' display item')
    if 'item_display' in nbt and nbt['item_display'] not in ('none', 'thirdperson_lefthand', 'thirdperson_righthand', 'firstperson_lefthand',
                                                             'firstperson_righthand', 'head', 'gui', 'ground', 'fixed', 'on_shelf'):
        errs.append(f'{where}: item_display {nbt["item_display"]}')
    if 'billboard' in nbt and nbt['billboard'] not in ('fixed', 'vertical', 'horizontal', 'center'): errs.append(f'{where}: billboard')
    if 'brightness' in nbt and set(nbt['brightness']) != {'block', 'sky'}: errs.append(f'{where}: brightness')
    if 'transformation' in nbt and set(nbt['transformation']) - {'translation', 'left_rotation', 'right_rotation', 'scale'}: errs.append(f'{where}: transformation')  # partial is fine (defaults / merge)

def main():
    n = 0
    for f in glob.glob(C.ROOT_DP + '/bm/function/**/*.mcfunction', recursive=True):
        rel = f[len(C.ROOT_DP) + 13:]
        for ln, line in enumerate(open(f), 1):
            if line.startswith('$'): line = re.sub(r'\$\((\w+)\)', '0', line[1:])      # macro line: placeholders -> a number
            m = re.search(r'summon minecraft:(\w+) [~^\d.\- ]+? (\{.*)$', line)
            if m:
                _, nbt = C.parse_snbt(m.group(2), 0); entity(m.group(1), nbt, f'{rel}:{ln}'); n += 1
            m = re.search(r'data merge entity @s(?:\[type=minecraft:(\w+)\])? (\{.*)$', line)
            if m:
                kind = m.group(1) or ('creeper' if 'ExplosionRadius' in line else 'item_display' if ('transformation' in line or 'interpolation' in line) else 'mob')
                _, nbt = C.parse_snbt(m.group(2), 0); entity(kind, nbt, f'{rel}:{ln}'); n += 1
    for e in errs: print('✗', e)
    print(f'{n} summon/data-merge NBT blobs checked field-by-field: {len(errs)} errors')
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
