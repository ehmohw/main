"""26.3 data format layer (applied by gen_dp.wjson to every JSON file the pack writes).

26.3 reworked loot/predicate data (SpyglassMC vanilla-mcdoc, checked against the 26.3 server):
- a loot condition's `condition` key is now `type`; lists of conditions (`conditions`) became one `condition`
  (several are wrapped in minecraft:all_of); predicate files are one condition (no top-level list);
- a loot function's `function` key is now `type`; `functions` lists on tables, pools and entries became `modifier`;
  an item modifier FILE is one function (several are wrapped in minecraft:sequence);
- advancement trigger entity/location predicates are one condition (or a predicate id), not a list;
  player_generates_container_loot takes `loot_tables`;
- exploration_map `destination` needs `#` for a structure tag; tag loot entries use `items: "#tag"`;
  set_loot_table's `name` is `loot_table_id`.
The generators keep writing the 26.2 shapes; this layer translates. It is idempotent on 26.3 data (vanilla copies)."""
import copy
from nbt import snbt


def _s(i):
    return i.split(':', 1)[1] if isinstance(i, str) and ':' in i else i


def cond(c):
    """One loot condition (26.2 or 26.3 shape) -> 26.3."""
    if isinstance(c, list): return conds(c)
    if isinstance(c, str): return c                      # a predicate id reference
    c = dict(c)
    if 'condition' in c and isinstance(c['condition'], str): c['type'] = c.pop('condition')
    t = _s(c.get('type'))
    if t in ('all_of', 'any_of'): c['terms'] = [cond(x) for x in c['terms']]
    elif t == 'inverted': c['term'] = cond(c['term'])
    elif t in ('reference', 'value_check', 'block_state_property', 'alternative'):
        raise ValueError(f'26.3: loot condition {t} no longer exists - rewrite it')
    return c


def conds(lst):
    lst = [cond(x) for x in lst]
    if len(lst) == 1: return lst[0]
    return {'type': 'minecraft:all_of', 'terms': lst}


def func(f):
    """One loot function -> 26.3."""
    f = dict(f)
    if 'function' in f and isinstance(f['function'], str): f['type'] = f.pop('function')
    if 'conditions' in f: f['condition'] = conds(f.pop('conditions'))
    elif 'condition' in f and not isinstance(f['condition'], str): f['condition'] = cond(f['condition'])
    t = _s(f.get('type'))
    if t == 'exploration_map':
        d = f.get('destination')
        if isinstance(d, str) and not d.startswith('#'): f['destination'] = '#' + d     # every destination we use is a structure tag
    elif t == 'sequence':
        f['functions'] = [func(x) for x in f['functions']] if isinstance(f['functions'], list) else func(f['functions'])
    elif t == 'set_loot_table' and 'name' in f:
        f['loot_table_id'] = f.pop('name'); f.pop('type_', None)
    elif t == 'filtered':
        for k in ('modifier', 'on_pass', 'on_fail'):
            if k in f: f[k] = modifier(f[k])
    return f


def modifier(m):
    """An item modifier in a non-root position (a list is allowed)."""
    if isinstance(m, list): return [func(x) for x in m] if len(m) != 1 else func(m[0])
    if isinstance(m, str): return m
    return func(m)


def item_modifier_file(m):
    if isinstance(m, list):
        if len(m) == 1: return func(m[0])
        return {'type': 'minecraft:sequence', 'functions': [func(x) for x in m]}
    return func(m)


def entry(e):
    e = dict(e)
    if 'conditions' in e: e['condition'] = conds(e.pop('conditions'))
    elif isinstance(e.get('condition'), (dict, list)): e['condition'] = cond(e['condition'])
    if 'functions' in e: e['modifier'] = modifier(e.pop('functions'))
    t = _s(e.get('type'))
    if e.get('name') == 'minecraft:map' and 'exploration_map' in str(e.get('modifier')):
        raise ValueError('26.3: exploration_map keeps the input item - start from minecraft:filled_map or an explorer-map item, not minecraft:map')
    if t == 'tag' and 'name' in e:
        n = e.pop('name'); e['items'] = n if n.startswith('#') else '#' + n
    if 'children' in e: e['children'] = [entry(x) for x in e['children']]
    if t == 'loot_table' and isinstance(e.get('value'), dict): e['value'] = loot_table(e['value'])
    return e


def pool(p):
    p = dict(p)
    if 'conditions' in p: p['condition'] = conds(p.pop('conditions'))
    elif isinstance(p.get('condition'), (dict, list)): p['condition'] = cond(p['condition'])
    if 'functions' in p: p['modifier'] = modifier(p.pop('functions'))
    p['entries'] = [entry(x) for x in p.get('entries', [])]
    return p


def loot_table(t):
    t = dict(t)
    if 'functions' in t: t['modifier'] = modifier(t.pop('functions'))
    if 'pools' in t: t['pools'] = [pool(x) for x in t['pools']]
    return t


ENTITY_KEYS = ('player', 'entity', 'villager', 'projectile', 'shooter', 'parent', 'partner', 'child', 'zombie', 'lightning',
               'source', 'bystander', 'killing_blow', 'direct_entity', 'source_entity')


def advancement(a):
    a = copy.deepcopy(a)
    for crit in a.get('criteria', {}).values():
        c = crit.get('conditions')
        if not isinstance(c, dict): continue
        for k in ENTITY_KEYS + ('location',):
            if isinstance(c.get(k), list): c[k] = conds(c[k])
            elif isinstance(c.get(k), dict) and ('condition' in c[k] or 'type' in c[k]): c[k] = cond(c[k])
        if 'victims' in c and isinstance(c['victims'], list):
            c['victims'] = [conds(v) if isinstance(v, list) else v for v in c['victims']]
        if 'loot_table' in c: c['loot_tables'] = c.pop('loot_table')
    return a


def enchantment(e):
    e = copy.deepcopy(e)

    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if k == 'requirements': o[k] = cond(v)
                else: walk(v)
        elif isinstance(o, list):
            for x in o: walk(x)
    walk(e.get('effects', {}))
    return e


def convert(rel, obj):
    """rel: 'bm/loot_table/x.json' etc. (relative to data/)."""
    parts = rel.split('/')
    kind = parts[1] if len(parts) > 1 else ''
    if kind == 'loot_table': return loot_table(obj)
    if kind == 'item_modifier': return item_modifier_file(obj)
    if kind == 'predicate': return cond(obj)
    if kind == 'advancement': return advancement(obj)
    if kind == 'enchantment': return enchantment(obj)
    return obj


def inline_modifier(snbt_text):
    """For inline item modifiers / predicates written as SNBT inside commands: the same key renames, textually."""
    for bad, why in (('block_state:{Name:', 'block states are "minecraft:x" or {id:..,properties:{..}} in 26.3'),
                     ('BlockState:{Name:', 'block states are "minecraft:x" or {id:..,properties:{..}} in 26.3'),
                     ('swing_animation', 'swing_animation became attack_animation/interact_animation in 26.3'),
                     ('map_color', 'the map_color component was removed in 26.3')):
        if bad in snbt_text: raise ValueError(f'26.3: {why}: {snbt_text[:160]}')
    return snbt_text.replace('{function:"minecraft:', '{type:"minecraft:').replace('{condition:"minecraft:', '{type:"minecraft:')


def custom_data_snbt(o, parent=None):
    """custom_data inside JSON `components` maps is written as SNBT text, not a JSON object.

    A JSON object is converted to NBT with numbers narrowed to the smallest type ("bmv": 20 becomes 20b), while the same
    item written in a command (trades, gives) keeps 20 as an int. custom_data is compared tag-for-tag (byte != int), so a
    loot-table token would never satisfy a trade asking for {bm:"token",bmv:20} and the re-sync would fire forever.
    Written as SNBT text (CustomData accepts both), loot tables, item modifiers and commands produce identical tags.
    Runs on the generator's typed objects (before to_json), so Byte/Float wrappers keep their suffixes."""
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if k == 'minecraft:custom_data' and parent == 'components' and isinstance(v, dict): out[k] = snbt(v)
            else: out[k] = custom_data_snbt(v, k)
        return out
    if isinstance(o, list): return [custom_data_snbt(x, parent) for x in o]
    return o
