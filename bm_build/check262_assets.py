"""26.2 verification for everything that isn't a command: structure templates, JSON data, resource pack.
Reference data: misode/mcmeta 26.2-summary (generated from the vanilla 26.2 jar)."""
import json, glob, re, sys, os
sys.path.insert(0, '/home/claude/bm_build')
from nbt import read_nbt_gz
import check262 as C

REG, BLOCKS = C.REG, C.BLOCKS
DP = os.environ.get('BM_OUT', '/home/claude/bm_build/out') + '/BlackMarket_DP'
RP = os.environ.get('BM_OUT', '/home/claude/bm_build/out') + '/BlackMarket_RP'
errs = []


def E(msg): errs.append(msg)


# ---------------- pack.mcmeta

dpm = json.load(open(f'{DP}/pack.mcmeta'))['pack']; rpm = json.load(open(f'{RP}/pack.mcmeta'))['pack']
if dpm['min_format'] != [121, 0] or dpm["max_format"] not in (121, [121, 0]): E(f'data pack format {dpm}')
if rpm['min_format'] != [97, 1] or rpm["max_format"] not in (97, [97, 1]): E(f'resource pack format {rpm}')

# ---------------- structures: block states + block entities + entities
BE_OK = {'lectern', 'sign', 'hanging_sign', 'chest', 'barrel', 'vault', 'trial_spawner'}
def loot_exists(ref):
    ns_, path_ = ref.split(':', 1)
    if ns_ == 'minecraft': return path_ in REG['loot_table']
    return os.path.exists(f'{DP}/data/{ns_}/loot_table/{path_}.json')
BOOLK = ('bold', 'italic', 'underlined', 'strikethrough', 'obfuscated', 'minecraft:enchantment_glint_override', 'has_glowing_text')
def nbt_bools(o):
    # NBT has no booleans: text flags are stored as 0b/1b, which the game reads as false/true
    if isinstance(o, dict): return {k: (bool(v) if k in BOOLK and v in (0, 1) else nbt_bools(v)) for k, v in o.items()}
    if isinstance(o, list): return [nbt_bools(x) for x in o]
    return o
def check_stack(st, where):
    st = nbt_bools(st)
    try:
        C.check_item_id(st['id'], where)
        for k, val in st.get('components', {}).items():
            if not k.startswith('!'): C.check_component(k, val, where)
    except C.PErr as ex: E(str(ex))
for f in glob.glob(f'{DP}/data/bm/structure/*.nbt'):
    d = read_nbt_gz(f); name = os.path.basename(f)
    if d['DataVersion'] != 4903: E(f'{name}: DataVersion {d["DataVersion"]} != 4903')
    for p in d['palette']:
        bn = p['Name'].split(':')[1]
        if bn not in BLOCKS: E(f'{name}: unknown block {bn}'); continue
        props = BLOCKS[bn][0]
        for k, val in p.get('Properties', {}).items():
            if k not in props: E(f'{name}: {bn} has no property {k}')
            elif val not in props[k]: E(f'{name}: {bn}[{k}={val}] invalid, allowed {props[k]}')
    for b in d['blocks']:
        if 'nbt' in b:
            be = b['nbt'].get('id', '').split(':')[-1]
            if be not in BE_OK: E(f'{name}: unexpected block entity {be}')
            if be in ('chest', 'barrel'):
                if 'LootTable' in b['nbt'] and not loot_exists(b['nbt']['LootTable']): E(f'{name}: chest loot table {b["nbt"]["LootTable"]} missing')
                for it in b['nbt'].get('Items', []): check_stack(it, f'{name} chest item')
            if be == 'vault':
                cf = b['nbt']['config']
                if set(cf) - {'key_item', 'loot_table', 'override_loot_table_to_display', 'activation_range', 'deactivation_range'}: E(f'{name}: vault config keys {set(cf)}')
                check_stack(cf['key_item'], f'{name} vault key')
                if not loot_exists(cf['loot_table']): E(f'{name}: vault loot table {cf["loot_table"]} missing')
            if be == 'trial_spawner':
                t = b['nbt']
                if set(t) - {'id', 'normal_config', 'ominous_config', 'required_player_range', 'target_cooldown_length'}: E(f'{name}: trial spawner keys {set(t)}')
                for kc in ('normal_config', 'ominous_config'):
                    ns_, path_ = t[kc].split(':', 1)
                    if not os.path.exists(f'{DP}/data/{ns_}/trial_spawner/{path_}.json'): E(f'{name}: trial spawner config {t[kc]} missing')
            if be == 'lectern':
                bk = b['nbt']['Book']
                C.check_item_id(bk['id'], 'lectern book')
                for k, val in bk['components'].items(): C.check_component(k, val, 'lectern book')
            if be in ('sign', 'hanging_sign'):
                for side in ('front_text', 'back_text'):
                    t = b['nbt'][side]
                    if len(t['messages']) != 4: E(f'{name}: sign needs 4 lines')
                    for m in t['messages']: C.check_text(m, 'sign')
                    if t['color'] not in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray',
                                          'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black'): E(f'{name}: sign color {t["color"]}')
    for e in d['entities']:
        if e['nbt']['id'] not in ('minecraft:marker', 'minecraft:item_display'): E(f'{name}: unexpected entity {e["nbt"]["id"]}')
        if e['nbt']['id'] == 'minecraft:item_display':                    # decorative displays in templates (2.4: Wilfrey's sword)
            import check262_nbt as N
            N.entity('item_display', {k: v for k, v in e['nbt'].items() if k != 'id'}, name)
            for er in N.errs: E(er)
            N.errs.clear()
        if len(e['blockPos']) != 3 or len(e['pos']) != 3: E(f'{name}: bad entity pos')

# ---------------- JSON data
for f in glob.glob(f'{DP}/data/**/*.json', recursive=True):
    rel = f[len(DP) + 6:]
    d = C.jload(f)
    s = json.dumps(d)
    # every component patch in loot tables / item modifiers
    def walk(o):
        if isinstance(o, dict):
            if o.get('function') == 'minecraft:set_components':
                for k, val in o['components'].items():
                    try:
                        if k.startswith('!'):
                            if C.strip_ns(C.ns(k[1:])) not in REG['data_component_type']: E(f'{rel}: bad removal {k}')
                        else: C.check_component(k, val, rel)
                    except C.PErr as ex: E(str(ex))
            if o.get('type') == 'minecraft:item' and 'name' in o:
                try: C.check_item_id(o['name'], rel)
                except C.PErr as ex: E(str(ex))
            for x in o.values(): walk(x)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(d)
    for fn_ in re.findall(r'"function": "minecraft:(\w+)"', s):
        if fn_ not in REG['loot_function_type']: E(f'{rel}: loot function {fn_}')
    for c in re.findall(r'"condition": "minecraft:(\w+)"', s):
        if c not in REG['loot_condition_type']: E(f'{rel}: loot condition {c}')
    for t in re.findall(r'"trigger": "minecraft:(\w+)"', s):
        if t not in REG['trigger_type']: E(f'{rel}: trigger {t}')
    for t in re.findall(r'"loot_table": "minecraft:([\w/]+)"', s) + re.findall(r'"value": "minecraft:([\w/]+)"', s):
        if t not in REG['loot_table']: E(f'{rel}: vanilla loot table {t}')
    if '/trial_spawner/' in rel:
        okk = {'spawn_range', 'total_mobs', 'total_mobs_added_per_player', 'simultaneous_mobs', 'simultaneous_mobs_added_per_player',
               'ticks_between_spawn', 'spawn_potentials', 'loot_tables_to_eject', 'items_to_drop_when_ominous'}
        if set(d) - okk: E(f'{rel}: trial spawner keys {set(d) - okk}')
        for sp in d['spawn_potentials']:
            if set(sp) != {'data', 'weight'} or set(sp['data']) - {'entity', 'equipment', 'custom_spawn_rules'}: E(f'{rel}: spawn potential shape')
            if sp['data']['entity']['id'].split(':')[1] not in REG['entity_type']: E(f'{rel}: entity {sp["data"]["entity"]["id"]}')
            if 'equipment' in sp['data'] and not loot_exists(sp['data']['equipment']['loot_table']): E(f'{rel}: equipment table missing')
        for lt in d.get('loot_tables_to_eject', []):
            if not loot_exists(lt['data']): E(f'{rel}: eject table {lt["data"]} missing')
    if '/dimension_type/' in rel:
        req = {'has_skylight', 'has_ceiling', 'has_ender_dragon_fight', 'coordinate_scale', 'ambient_light', 'logical_height', 'infiniburn',
               'min_y', 'height', 'monster_spawn_light_level', 'monster_spawn_block_light_limit'}
        opt = {'attributes', 'default_clock', 'timelines', 'has_fixed_time', 'skybox', 'cardinal_light'}
        if req - set(d): E(f'{rel}: dimension type missing {req - set(d)}')
        if set(d) - req - opt: E(f'{rel}: dimension type unknown keys {set(d) - req - opt}')
        if d.get('skybox', 'overworld') not in ('none', 'overworld', 'end'): E(f'{rel}: skybox')
        if d['min_y'] % 16 or d['height'] % 16: E(f'{rel}: min_y/height must be multiples of 16')
        if d.get('default_clock') and d['default_clock'].split(':')[1] not in REG['world_clock']: E(f'{rel}: clock')
        for k, v in d.get('attributes', {}).items():          # 2.2: environment attributes vs the 26.2 registry
            if k.split(':', 1)[1] not in REG['environment_attribute']: E(f'{rel}: attribute {k}')
            if k.endswith('/ambient_particles'):
                for ap in v:
                    if set(ap) != {'particle', 'probability'} or ap['particle']['type'].split(':')[1] not in REG['particle_type']: E(f'{rel}: ambient particle {ap}')
            if k.endswith(('_color',)) and not re.fullmatch(r'#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?', v): E(f'{rel}: colour {k}={v}')
    if rel.startswith('bm/dimension/'):
        tp = d['type'].split(':', 1)
        if not os.path.exists(f'{DP}/data/{tp[0]}/dimension_type/{tp[1]}.json'): E(f'{rel}: dimension type missing')
        if d['generator']['settings']['biome'].split(':')[1] not in REG['worldgen/biome']: E(f'{rel}: biome')
    for dest in re.findall(r'"destination": "bm:([\w/]+)"', s):
        if not os.path.exists(f'{DP}/data/bm/tags/worldgen/structure/{dest}.json'): E(f'{rel}: map destination tag bm:{dest} missing')
    for ref in re.findall(r'"value": "(bm:[\w/]+)"', s) + re.findall(r'"loot_table": "(bm:[\w/]+)"', s):
        if not loot_exists(ref): E(f'{rel}: loot table {ref} missing')
    if '/worldgen/structure/' in rel and '/tags/' not in rel:
        sp_ = d['start_pool'].split(':', 1)
        if not os.path.exists(f'{DP}/data/{sp_[0]}/worldgen/template_pool/{sp_[1]}.json'): E(f'{rel}: start pool missing')
        bt = d['biomes'].lstrip('#').split(':', 1)
        if not os.path.exists(f'{DP}/data/{bt[0]}/tags/worldgen/biome/{bt[1]}.json'): E(f'{rel}: biome tag missing')
    if '/template_pool/' in rel:
        for el in d['elements']:
            loc = el['element']['location'].split(':', 1)
            if not os.path.exists(f'{DP}/data/{loc[0]}/structure/{loc[1]}.nbt'): E(f'{rel}: template {el["element"]["location"]} missing')
    if '/tags/block/' in rel:
        for vv in d['values']:
            if vv.startswith('#'):
                if vv.split(':')[1] not in REG['tag/block'] and not os.path.exists(f'{DP}/data/{vv[1:].split(":")[0]}/tags/block/{vv.split(":")[1]}.json'): E(f'{rel}: block tag {vv}')
            elif vv.split(':')[1] not in BLOCKS: E(f'{rel}: block {vv}')
    if '/tags/entity_type/' in rel:
        for vv in d['values']:
            i = vv['id'] if isinstance(vv, dict) else vv
            if i.startswith('#'): continue
            if i.split(':')[1] not in REG['entity_type']: E(f'{rel}: entity {i}' + (' (optional entry, would be skipped)' if isinstance(vv, dict) else ''))
    if '/tags/worldgen/biome/' in rel:
        for vv in d['values']:
            i = vv['id'] if isinstance(vv, dict) else vv
            if i.startswith('#'):
                if i[11:] not in REG['tag/worldgen/biome']: E(f'{rel}: biome tag {i}')
            elif i.split(':')[1] not in REG['worldgen/biome']: E(f'{rel}: biome {i}')
    if '/worldgen/structure/' in rel and '/tags/' not in rel:
        if d['terrain_adaptation'] not in ('none', 'beard_thin', 'beard_box', 'bury', 'encapsulate'): E(f'{rel}: terrain_adaptation')
        if d['step'] not in ('underground_structures', 'surface_structures'): E(f'{rel}: step')
        if d.get('project_start_to_heightmap', 'WORLD_SURFACE_WG') not in ('WORLD_SURFACE_WG', 'WORLD_SURFACE', 'OCEAN_FLOOR_WG', 'OCEAN_FLOOR', 'MOTION_BLOCKING', 'MOTION_BLOCKING_NO_LEAVES'): E(f'{rel}: heightmap')
        if not (1 <= d['size'] <= 20): E(f'{rel}: size')
    if '/predicate/' in rel and isinstance(d, dict) and d.get('condition', '').endswith('entity_properties'):   # 26.2 sub-predicate map
        for k in d.get('predicate', {}):
            if not k.startswith('minecraft:') or C.strip_ns(k) not in REG['entity_sub_predicate_type']: E(f'{rel}: entity sub-predicate {k}')
    if '/dialog/' in rel:                      # 1.18: menus, against the 26.2 dialog schema
        import dialogs262
        dialogs262.check_dialog(d, rel, E, C.check_line)
    if '/painting_variant/' in rel:
        if set(d) - {'asset_id', 'width', 'height', 'title', 'author'}: E(f'{rel}: unknown painting keys')
        if not (1 <= d.get('width', 0) <= 16 and 1 <= d.get('height', 0) <= 16): E(f'{rel}: painting size')
        ns_, pth = d['asset_id'].split(':')
        png = f'{RP}/assets/{ns_}/textures/painting/{pth}.png'
        if not os.path.exists(png): E(f'{rel}: missing texture {png}')
        else:
            from PIL import Image
            sz = Image.open(png).size          # 16 px a block, or an HD multiple of it (x2, x4, x8) - same aspect
            if not any(sz == (16 * k * d['width'], 16 * k * d['height']) for k in (1, 2, 4, 8)): E(f'{rel}: texture size {sz}')
    if '/banner_pattern/' in rel:
        if set(d) != {'asset_id', 'translation_key'}: E(f'{rel}: banner pattern keys {sorted(d)}')
        ns_, pth = d['asset_id'].split(':')
        for kind in ('banner', 'shield'):
            if not os.path.exists(f'{RP}/assets/{ns_}/textures/entity/{kind}/{pth}.png'): E(f'{rel}: missing {kind} texture')
    if '/advancement/' in rel:
        for crit in d['criteria'].values():
            if C.strip_ns(crit['trigger']) not in REG['trigger_type']: E(f'{rel}: trigger {crit["trigger"]}')
            for cond in crit.get('conditions', {}).get('entity', []):
                if C.strip_ns(cond['condition']) not in REG['loot_condition_type']: E(f'{rel}: condition {cond["condition"]}')
                for k, val in cond.get('predicate', {}).items():
                    # 26.2: entity predicates are a map of namespaced sub-predicates
                    if not k.startswith('minecraft:') or C.strip_ns(k) not in REG['entity_sub_predicate_type']: E(f'{rel}: entity sub-predicate {k}')
                    if k == 'minecraft:nbt': C.parse_snbt(val, 0)
            item = crit.get('conditions', {}).get('item')
            if item:
                if item['items'].startswith('#'):                       # 2.13: an item tag
                    if C.strip_ns(item['items'][1:]) not in REG['tag/item']: E(f'{rel}: unknown item tag {item["items"]}')
                else:
                    C.check_item_id(item['items'], rel)
                for k, val in item.get('predicates', {}).items():
                    if C.strip_ns(k) not in REG['data_component_predicate_type']: E(f'{rel}: predicate {k}')
                    C.parse_snbt(val, 0)

# ---------------- custom enchantments / damage types / predicates
ALL_LINES = [ln.strip() for g in glob.glob(f'{DP}/data/bm/function/**/*.mcfunction', recursive=True) for ln in open(g)]
VAN_ENCH_KEYS = {'anvil_cost', 'description', 'effects', 'exclusive_set', 'max_cost', 'max_level', 'min_cost', 'primary_items', 'slots', 'supported_items', 'weight'}
for f in glob.glob(f'{DP}/data/bm/enchantment/*.json'):
    d = C.jload(f)
    if set(d) - VAN_ENCH_KEYS: E(f'{f}: unknown keys {set(d) - VAN_ENCH_KEYS}')
    for k in ('anvil_cost', 'description', 'max_cost', 'max_level', 'min_cost', 'slots', 'supported_items', 'weight'):
        if k not in d: E(f'{f}: missing required {k}')
    si = d['supported_items']
    if isinstance(si, list) or not si.startswith('#'):       # (2.35: an item or a list of items)
        for i in (si if isinstance(si, list) else [si]):
            if C.strip_ns(i) not in REG['item']: E(f'{f}: supported item {i}')
    elif si.startswith('#bm:'):
        if not os.path.exists(f'{DP}/data/bm/tags/item/{si[4:]}.json'): E(f'{f}: supported_items tag')
    elif si.lstrip('#').split(':')[1] not in REG['tag/item']: E(f'{f}: supported_items tag')
    for comp, effs in d['effects'].items():
        if C.strip_ns(comp) not in REG['enchantment_effect_component_type']: E(f'{f}: effect component {comp}')
        for e in effs:
            if C.strip_ns(comp) == 'tick':          # 2.16: conditional effects (no targets); requirements are a plain loot condition
                if set(e) - {'effect', 'requirements'}: E(f'{f}: tick effect keys')
                if C.strip_ns(e['effect']['type']) not in REG['enchantment_entity_effect_type']: E(f'{f}: entity effect {e["effect"]["type"]}')
                if e['effect']['type'] == 'minecraft:ignite' and not isinstance(e['effect'].get('duration'), (int, float)): E(f'{f}: ignite duration')
                rq = e.get('requirements', {'condition': 'minecraft:entity_scores', 'scores': {}})
                if C.strip_ns(rq.get('type', rq.get('condition', ''))) not in REG['loot_condition_type']: E(f'{f}: requirement condition')
                for ob in rq.get('scores', {}):
                    if not any(ln.startswith(f'scoreboard objectives add {ob} ') for ln in ALL_LINES): E(f'{f}: objective {ob} never created')
                continue
            if C.strip_ns(comp) == 'damage':                                     # 2.35: a value effect (the Pharaoh's daylight bonus)
                if set(e) - {'effect', 'requirements'} or C.strip_ns(e['effect'].get('type', '')) not in REG['enchantment_value_effect_type']: E(f'{f}: damage value effect')
                rq = e.get('requirements', {})
                if rq and C.strip_ns(rq.get('condition', rq.get('type', ''))) not in REG['loot_condition_type']: E(f'{f}: damage requirement')
                continue
            if C.strip_ns(comp) in ('damage_immunity', 'damage_protection'):     # 2.20: conditional (damage context) effects
                if set(e) - {'effect', 'requirements'}: E(f'{f}: {comp} keys')
                if C.strip_ns(comp) == 'damage_protection' and C.strip_ns(e['effect'].get('type', '')) not in REG['enchantment_value_effect_type']: E(f'{f}: value effect')
                if C.strip_ns(comp) == 'damage_immunity' and e['effect'] != {}: E(f'{f}: damage_immunity effect must be empty')
                continue
            if C.strip_ns(comp) in ('post_attack', 'post_piercing_attack') and e['affected'] not in ('attacker', 'damaging_entity', 'victim') or C.strip_ns(comp) in ('post_attack', 'post_piercing_attack') and e['enchanted'] not in ('attacker', 'damaging_entity', 'victim'): E(f'{f}: target')
            def ee(x):
                if C.strip_ns(x['type']) not in REG['enchantment_entity_effect_type']: E(f'{f}: entity effect {x["type"]}')
                for y in x.get('effects', []): ee(y)
                if x['type'] == 'minecraft:run_function' and x['function'][3:] not in C.MY_FUNCS: E(f'{f}: missing function')
                if x['type'] == 'minecraft:damage_entity':
                    dt = x['damage_type']
                    if dt.startswith('bm:') and not os.path.exists(f'{DP}/data/bm/damage_type/{dt[3:]}.json'): E(f'{f}: damage type {dt}')
                    if dt.startswith('minecraft:') and dt[10:] not in REG['damage_type']: E(f'{f}: damage type {dt}')
                if x['type'] == 'minecraft:apply_mob_effect' and C.strip_ns(x['to_apply']) not in REG['mob_effect']: E(f'{f}: mob effect')
            ee(e['effect'])
            rq = e.get('requirements')
            if rq is None: continue
            if rq.get('type', rq.get('condition')) == 'minecraft:inverted': rq = rq['term']
            if rq.get('type', rq.get('condition')) == 'minecraft:random_chance':     # (2.32: the Thunderbird's blows)
                if not 0 < rq['chance'] <= 1: E(f'{f}: random_chance')
                continue
            pr = rq['predicate']
            if set(pr) - {'minecraft:entity_type', 'minecraft:flags', 'minecraft:movement'}: E(f'{f}: predicate keys')     # (2.20: as vanilla wind_burst)
for f in glob.glob(f'{DP}/data/bm/damage_type/*.json'):
    d = C.jload(f)
    if set(d) - {'exhaustion', 'message_id', 'scaling', 'effects', 'death_message_type'} or d['scaling'] not in ('never', 'always', 'when_caused_by_living_non_player'): E(f'{f}: damage type format')
for f in glob.glob(f'{DP}/data/minecraft/tags/damage_type/*.json'):
    if os.path.basename(f)[:-5] not in REG['tag/damage_type']: E(f'{f}: not a vanilla damage type tag')
for f in glob.glob(f'{DP}/data/bm/predicate/*.json'):
    d = C.jload(f)
    if C.strip_ns(d['condition']) not in REG['loot_condition_type']: E(f'{f}: condition')
    if d['condition'] == 'minecraft:entity_properties':
        for k, v in d['predicate'].items():
            if C.strip_ns(k) not in REG['entity_sub_predicate_type'] and k not in ('minecraft:flags', 'minecraft:entity_type'): E(f'{f}: entity predicate key {k}')
        for fl in d['predicate'].get('minecraft:flags', {}):
            if fl not in ('is_on_fire', 'is_sneaking', 'is_sprinting', 'is_swimming', 'is_on_ground', 'is_baby', 'is_flying', 'is_fall_flying', 'is_in_water'): E(f'{f}: flag {fl}')
    if d['condition'] == 'minecraft:location_check' and set(d['predicate']) - {'position', 'biomes', 'structures', 'dimension', 'light', 'block', 'fluid', 'smokey', 'can_see_sky'}: E(f'{f}: location keys')

# ---------------- resource pack
def walk_item_model(f, m):
    # 26.2 item definitions (vanilla-mcdoc assets/item_definition.mcdoc): model / select / condition / composite / range_dispatch
    t = m.get('type')
    if t == 'minecraft:model':
        mp = m['model'].split(':')
        if mp[0] == 'bm' and not os.path.exists(f'{RP}/assets/bm/models/{mp[1]}.json'): E(f'{f}: missing model {m["model"]}')
        if mp[0] == 'minecraft' and mp[1] not in REG['model']: E(f'{f}: vanilla model {m["model"]} not in 26.3')
    elif t == 'minecraft:select':
        if m.get('property') != 'minecraft:custom_model_data': E(f'{f}: select property {m.get("property")} (only custom_model_data used/checked)')
        if not isinstance(m.get('index', 0), int) or m.get('index', 0) < 0: E(f'{f}: select index')
        for c in m.get('cases', []):
            if set(c) != {'when', 'model'} or not isinstance(c['when'], (str, list)): E(f'{f}: select case keys {set(c)}')
            walk_item_model(f, c['model'])
        if 'fallback' in m: walk_item_model(f, m['fallback'])
        if set(m) - {'type', 'property', 'index', 'cases', 'fallback', 'transformation'}: E(f'{f}: select keys {set(m)}')
    else: E(f'{f}: item model type {t}')


for f in glob.glob(f'{RP}/assets/bm/items/*.json'):
    d = C.jload(f)
    walk_item_model(f, d['model'])
for f in glob.glob(f'{RP}/assets/bm/models/item/*.json'):
    d = C.jload(f)
    if 'parent' in d and d['parent'].split(':')[1] not in REG['model']: E(f'{f}: parent model {d["parent"]} not in 26.3')
    for k, t in d.get('textures', {}).items():
        ns_, path = t.split(':')
        if ns_ == 'minecraft':
            if path not in REG['texture']: E(f'{f}: vanilla texture {t} not in 26.3')
        elif not os.path.exists(f'{RP}/assets/{ns_}/textures/{path}.png'): E(f'{f}: missing texture {t}')
    for el in d.get('elements', []):
        for a in el['from'] + el['to']:
            if not -16 <= a <= 32: E(f'{f}: element coord {a} outside -16..32')
        for face in el['faces'].values():
            if face['texture'][1:] not in d['textures']: E(f'{f}: face texture {face["texture"]}')
            if any(not 0 <= u <= 16 for u in face['uv']): E(f'{f}: uv out of range')
    for ctx in d.get('display', {}):
        if ctx not in ('none', 'firstperson_righthand', 'firstperson_lefthand', 'thirdperson_righthand', 'thirdperson_lefthand', 'gui', 'head', 'ground', 'fixed', 'on_shelf'):
            E(f'{f}: display ctx {ctx}')
# every bm:* item_model used by the data pack must exist in the RP
txt = ''.join(open(f).read() for f in glob.glob(f'{DP}/data/**/*', recursive=True) if f.endswith(('.json', '.mcfunction')))
for m in sorted(set(re.findall(r'"?minecraft:item_model"?[=:] ?"(bm:[a-z_]+)"', txt))):
    if not os.path.exists(f'{RP}/assets/bm/items/{m[3:]}.json'): E(f'item_model {m} has no RP item definition')
for f in glob.glob(f'{RP}/assets/bm/equipment/*.json'):
    for layer, entries in json.load(open(f))['layers'].items():
        if layer not in ('humanoid', 'humanoid_leggings', 'wings', 'wolf_body', 'horse_body', 'llama_body', 'pig_saddle', 'strider_saddle', 'camel_saddle', 'horse_saddle', 'donkey_saddle', 'mule_saddle', 'skeleton_horse_saddle', 'zombie_horse_saddle', 'happy_ghast_body', 'nautilus_saddle', 'nautilus_body'): E(f'{f}: layer {layer}')
        for en in entries:
            t = en['texture'].split(':')
            if not os.path.exists(f'{RP}/assets/{t[0]}/textures/entity/equipment/{layer}/{t[1]}.png'): E(f'{f}: missing texture {en["texture"]}')
for png in glob.glob(f'{RP}/assets/bm/textures/**/*.png', recursive=True):
    from PIL import Image
    im = Image.open(png)
    if '/equipment/' in png: continue
    if im.mode != 'RGBA' or im.size[0] != im.size[1] or im.size[0] & (im.size[0] - 1): E(f'{png}: texture should be square power-of-two RGBA')

for e in errs: print('✗', e)
print(f'structures + JSON + resource pack vs 26.3: {len(errs)} errors')
sys.exit(1 if errs else 0)
