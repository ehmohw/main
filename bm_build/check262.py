"""Validate generated mcfunctions against the official Minecraft 26.2 command tree + registries
(misode/mcmeta 26.2-summary, generated from the vanilla jar)."""
import os, json, re, glob, os, sys

from paths import MC
TREE = json.load(open(MC + 'commands.json'))
REG = {k: set(v) for k, v in json.load(open(MC + 'registries.json')).items()}
BLOCKS = json.load(open(MC + 'blocks.json'))
SOUNDS = set(json.load(open(MC + 'sounds.json')).keys())


def reg(name):
    return REG[name]


class PErr(Exception):
    pass


ROOT_DP = os.environ.get('BM_OUT', '/home/claude/bm_build/out') + '/BlackMarket_DP/data'
MY_FUNCS = {f[len(ROOT_DP) + len('/bm/function/'):-11] for f in glob.glob(ROOT_DP + '/bm/function/**/*.mcfunction', recursive=True)}
MY_LOOT = {f[len(ROOT_DP) + len('/bm/loot_table/'):-5] for f in glob.glob(ROOT_DP + '/bm/loot_table/**/*.json', recursive=True)}
MY_MODS = {f[len(ROOT_DP) + len('/bm/item_modifier/'):-5] for f in glob.glob(ROOT_DP + '/bm/item_modifier/**/*.json', recursive=True)}
MY_ADV = {f[len(ROOT_DP) + len('/bm/advancement/'):-5] for f in glob.glob(ROOT_DP + '/bm/advancement/**/*.json', recursive=True)}
MY_PREDS = {f[len(ROOT_DP) + len('/bm/predicate/'):-5] for f in glob.glob(ROOT_DP + '/bm/predicate/**/*.json', recursive=True)}
MY_ENCH = {f[len(ROOT_DP) + len('/bm/enchantment/'):-5] for f in glob.glob(ROOT_DP + '/bm/enchantment/*.json')}
MY_TEMPLATES = {os.path.basename(f)[:-4] for f in glob.glob(ROOT_DP + '/bm/structure/*.nbt')}
MY_BLOCK_TAGS = {f[len(ROOT_DP) + len('/bm/tags/block/'):-5] for f in glob.glob(ROOT_DP + '/bm/tags/block/*.json')}
MY_ENTITY_TAGS = {f[len(ROOT_DP) + len('/bm/tags/entity_type/'):-5] for f in glob.glob(ROOT_DP + '/bm/tags/entity_type/*.json')}
MY_DIALOGS = {f[len(ROOT_DP) + len('/bm/dialog/'):-5] for f in glob.glob(ROOT_DP + '/bm/dialog/**/*.json', recursive=True)}   # 1.18
OBJECTIVES = set()
WARN = []


def ns(i):
    return i if ':' in i else 'minecraft:' + i


def strip_ns(i):
    return i.split(':', 1)[1] if i.startswith('minecraft:') else i


def in_reg(r, ident):
    return strip_ns(ns(ident)) in REG[r] if ident.startswith('minecraft:') or ':' not in ident else False


# ============================================================ SNBT
class SNBT:
    WS = ' \t\n'

    def __init__(self, s, i):
        self.s, self.i = s, i

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in self.WS: self.i += 1

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else ''

    def value(self):
        self.ws()
        c = self.peek()
        if c == '{': return self.compound()
        if c == '[': return self.list_()
        if c in '"\'': return self.qstr()
        return self.prim()

    def compound(self):
        self.i += 1; out = {}
        self.ws()
        if self.peek() == '}': self.i += 1; return out
        while True:
            self.ws()
            k = self.qstr() if self.peek() in '"\'' else self.word()
            if not k: raise PErr(f'SNBT: expected key at {self.i}')
            self.ws()
            if self.peek() != ':': raise PErr(f'SNBT: expected ":" after key {k!r}')
            self.i += 1
            out[k] = self.value()
            self.ws()
            c = self.peek()
            if c == ',': self.i += 1; continue
            if c == '}': self.i += 1; return out
            raise PErr(f'SNBT: expected , or }} at {self.s[self.i:self.i+20]!r}')

    def list_(self):
        self.i += 1
        if self.s[self.i:self.i + 2] in ('I;', 'B;', 'L;'):
            self.i += 2
        out = []
        self.ws()
        if self.peek() == ']': self.i += 1; return out
        while True:
            out.append(self.value())
            self.ws()
            c = self.peek()
            if c == ',': self.i += 1; continue
            if c == ']': self.i += 1; return out
            raise PErr(f'SNBT: expected , or ] at {self.s[self.i:self.i+20]!r}')

    def qstr(self):
        q = self.peek(); self.i += 1; out = ''
        while True:
            if self.i >= len(self.s): raise PErr('SNBT: unterminated string')
            c = self.s[self.i]
            if c == '\\':                      # SNBT escapes (26.x): \n \t \\ \" \'
                e = self.s[self.i + 1]
                out += {'n': '\n', 't': '\t', 'r': '\r'}.get(e, e); self.i += 2; continue
            if c == q: self.i += 1; return out
            out += c; self.i += 1

    def word(self):
        j = self.i
        while self.i < len(self.s) and (self.s[self.i].isalnum() or self.s[self.i] in '_-.+'): self.i += 1
        return self.s[j:self.i]

    def prim(self):
        w = self.word()
        if not w: raise PErr(f'SNBT: unexpected {self.s[self.i:self.i+20]!r}')
        if w in ('true', 'false'): return w == 'true'
        m = re.fullmatch(r'([+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)([bBsSlLfFdD]?)', w)
        if m:
            v = m.group(1)
            return float(v) if ('.' in v or 'e' in v.lower() or m.group(2).lower() in 'fd' and m.group(2)) else int(v)
        return w   # unquoted string


def plain(v):
    """SNBT parse result -> plain Python (typed numbers stay numbers, 1b/0b stay ints)."""
    if isinstance(v, dict): return {k: plain(x) for k, x in v.items()}
    if isinstance(v, list): return [plain(x) for x in v]
    return v


def parse_snbt(s, i):
    p = SNBT(s, i)
    v = p.value()
    return p.i, v


# ============================================================ semantic checks
COLORS = {'black', 'dark_blue', 'dark_green', 'dark_aqua', 'dark_red', 'dark_purple', 'gold', 'gray', 'dark_gray', 'blue', 'green',
          'aqua', 'red', 'light_purple', 'yellow', 'white'}
TEXT_KEYS = {'text', 'translate', 'with', 'fallback', 'color', 'bold', 'italic', 'underlined', 'strikethrough', 'obfuscated', 'extra',
             'selector', 'separator', 'score', 'keybind', 'nbt', 'insertion', 'click_event', 'hover_event', 'font', 'shadow_color', 'type',
             'source', 'block', 'entity', 'storage', 'interpret', 'object', 'sprite', 'atlas', 'player'}


def check_text(v, where):
    if isinstance(v, str): return
    if isinstance(v, list):
        for x in v: check_text(x, where); return
    if not isinstance(v, dict): raise PErr(f'{where}: text component must be string/compound/list, got {v!r}')
    for k, x in v.items():
        if k not in TEXT_KEYS: raise PErr(f'{where}: unknown text component key {k!r}')
    if 'color' in v:
        c = v['color']
        if not (c in COLORS or re.fullmatch(r'#[0-9a-fA-F]{6}', str(c))): raise PErr(f'{where}: bad color {c!r}')
    for b in ('bold', 'italic', 'underlined', 'strikethrough', 'obfuscated'):
        if b in v and not isinstance(v[b], bool): raise PErr(f'{where}: {b} must be boolean')
    if 'extra' in v:
        for x in v['extra']: check_text(x, where)
    if 'translate' in v and v['translate'].startswith('entity.minecraft.'):
        e = v['translate'][len('entity.minecraft.'):]
        if e not in REG['entity_type']: raise PErr(f'{where}: translate key for unknown entity {e}')
    if not any(k in v for k in ('text', 'translate', 'selector', 'score', 'keybind', 'nbt', 'object')):
        raise PErr(f'{where}: text component has no content key')


SLOTS_EQ = {'any', 'mainhand', 'offhand', 'hand', 'feet', 'legs', 'chest', 'head', 'armor', 'body', 'saddle'}
OPS = {'add_value', 'add_multiplied_base', 'add_multiplied_total'}
ANIMS = {'none', 'eat', 'drink', 'block', 'bow', 'trident', 'spear', 'crossbow', 'spyglass', 'toot_horn', 'brush', 'bundle'}  # 26.2 ItemUseAnimation


def is_num(x): return isinstance(x, (int, float)) and not isinstance(x, bool)


def check_component(key, v, where):
    k = strip_ns(ns(key))
    if k not in REG['data_component_type']: raise PErr(f'{where}: unknown data component {key}')
    w = f'{where} [{k}]'
    if k in ('item_name', 'custom_name'): check_text(v, w)
    elif k == 'lore':
        if not isinstance(v, list): raise PErr(f'{w}: must be list')
        for x in v: check_text(x, w)
    elif k == 'enchantments':
        if not isinstance(v, dict): raise PErr(f'{w}: must be map enchantment->level')
        for e, lv in v.items():
            if e.startswith('bm:'):
                if e[3:] not in MY_ENCH: raise PErr(f'{w}: missing custom enchantment {e}')
            elif strip_ns(ns(e)) not in REG['enchantment']: raise PErr(f'{w}: unknown enchantment {e}')
            if not (isinstance(lv, int) and 1 <= lv <= 255): raise PErr(f'{w}: bad level {lv}')
    elif k == 'attribute_modifiers':
        if not isinstance(v, list): raise PErr(f'{w}: must be list (1.21.5+ format)')
        for m in v:
            if set(m) - {'type', 'id', 'amount', 'operation', 'slot', 'display'}: raise PErr(f'{w}: unknown keys {set(m)}')
            if strip_ns(ns(m['type'])) not in REG['attribute']: raise PErr(f'{w}: unknown attribute {m["type"]}')
            if m['operation'] not in OPS: raise PErr(f'{w}: bad op')
            if m.get('slot', 'any') not in SLOTS_EQ: raise PErr(f'{w}: bad slot {m.get("slot")}')
            if not is_num(m['amount']): raise PErr(f'{w}: amount not number')
    elif k == 'item_model':
        i = ns(v)
        if i.startswith('minecraft:') and strip_ns(i) not in REG['item_definition']: raise PErr(f'{w}: no vanilla item model {v}')
        if i.startswith('bm:'): RP_MODELS_USED.add(i)
    elif k == 'max_stack_size':
        if not (isinstance(v, int) and 1 <= v <= 99): raise PErr(f'{w}: bad stack size')
    elif k == 'enchantment_glint_override':
        if not isinstance(v, bool): raise PErr(f'{w}: must be bool')
    elif k == 'food':
        if set(v) - {'nutrition', 'saturation', 'can_always_eat'}: raise PErr(f'{w}: unknown keys')
    elif k == 'consumable':
        if set(v) - {'consume_seconds', 'animation', 'sound', 'has_consume_particles', 'on_consume_effects'}: raise PErr(f'{w}: unknown keys')
        if 'animation' in v and v['animation'] not in ANIMS: raise PErr(f'{w}: bad animation {v["animation"]}')
        if 'sound' in v and strip_ns(ns(v['sound'])) not in REG['sound_event']: raise PErr(f'{w}: unknown sound {v["sound"]}')
        for e in v.get('on_consume_effects', []):
            if strip_ns(ns(e['type'])) not in REG['consume_effect_type']: raise PErr(f'{w}: bad consume effect type')
            for ef in e.get('effects', []):
                if strip_ns(ns(ef['id'])) not in REG['mob_effect']: raise PErr(f'{w}: bad effect {ef["id"]}')
    elif k == 'equippable':
        if set(v) - {'slot', 'equip_sound', 'asset_id', 'camera_overlay', 'allowed_entities', 'dispensable', 'swappable',
                     'damage_on_hurt', 'equip_on_interact', 'can_be_sheared', 'shearing_sound'}: raise PErr(f'{w}: unknown keys')
        if v['slot'] not in SLOTS_EQ - {'any', 'hand', 'armor'}: raise PErr(f'{w}: bad slot')
        if 'equip_sound' in v and strip_ns(ns(v['equip_sound'])) not in REG['sound_event']: raise PErr(f'{w}: bad sound')
    elif k == 'dyed_color':
        if not isinstance(v, int): raise PErr(f'{w}: must be int (1.21.5+)')
    elif k == 'unbreakable':
        if v != {}: raise PErr(f'{w}: must be empty compound')
    elif k == 'custom_data':
        if not isinstance(v, dict): raise PErr(f'{w}: must be compound')
    elif k == 'written_book_content':
        if set(v) - {'title', 'author', 'pages', 'generation', 'resolved'}: raise PErr(f'{w}: unknown keys')
        if len(v['title']) > 32: raise PErr(f'{w}: title > 32 chars')
        for pg in v['pages']: check_text(pg, w)
    elif k == 'death_protection':
        pass
    elif k == 'use_cooldown':
        if set(v) - {'seconds', 'cooldown_group'} or not is_num(v.get('seconds')) or v['seconds'] <= 0: raise PErr(f'{w}: use_cooldown')
    elif k == 'trim':
        if set(v) != {'material', 'pattern'}: raise PErr(f'{w}: trim needs material + pattern')
        if strip_ns(ns(v['material'])) not in REG['trim_material']: raise PErr(f'{w}: unknown trim material')
        if strip_ns(ns(v['pattern'])) not in REG['trim_pattern']: raise PErr(f'{w}: unknown trim pattern')
    else:
        WARN.append(f'{w}: component not deeply checked')


RP_MODELS_USED = set()


def check_item_id(i, where):
    if strip_ns(ns(i)) not in REG['item'] or not ns(i).startswith('minecraft:'): raise PErr(f'{where}: unknown item {i}')


# ============================================================ argument parsers
def word_end(s, i, chars=None):
    j = i
    while j < len(s) and s[j] != ' ': j += 1
    return j


def p_rl(s, i):
    m = re.compile(r'[a-z0-9_.\-]+(:[a-z0-9_./\-]+)?').match(s, i)
    if not m or m.end() == i: raise PErr(f'expected resource location at {s[i:i+20]!r}')
    return m.end(), m.group(0)


def p_number(s, i, integer=False):
    m = re.compile(r'-?\d+' if integer else r'-?(\d+\.?\d*|\.\d+)').match(s, i)
    if not m: raise PErr(f'expected number at {s[i:i+15]!r}')
    return m.end(), float(m.group(0)) if not integer else int(m.group(0))


def p_coord(s, i, block=False):
    m = re.compile(r'([~^])?(-?(\d+\.?\d*|\.\d+))?').match(s, i)
    if not m or m.end() == i: raise PErr(f'expected coordinate at {s[i:i+15]!r}')
    if block and not m.group(1) and m.group(2) and '.' in m.group(2): raise PErr('block pos needs integers')
    return m.end(), m.group(0)


def p_coords(s, i, n, block=False):
    out = []
    for k in range(n):
        if k:
            if i >= len(s) or s[i] != ' ': raise PErr('expected space between coordinates')
            i += 1
        i, c = p_coord(s, i, block)
        out.append(c)
    locals_ = [c.startswith('^') for c in out]
    if any(locals_) and not all(locals_): raise PErr('cannot mix ^ with other coordinates')
    return i, out


SEL_OPTS = {'type', 'tag', 'distance', 'scores', 'gamemode', 'limit', 'sort', 'nbt', 'x', 'y', 'z', 'dx', 'dy', 'dz', 'predicate',
            'name', 'level', 'team', 'advancements', 'x_rotation', 'y_rotation'}


def p_entity(s, i, props):
    if s.startswith('@', i):
        if i + 1 >= len(s) or s[i + 1] not in 'aeprsn': raise PErr(f'bad selector {s[i:i+3]}')
        kind = s[i + 1]; i += 2
        opts = []
        if i < len(s) and s[i] == '[':
            depth, j, q = 0, i, None
            while j < len(s):
                ch = s[j]
                if q:
                    if ch == '\\': j += 2; continue
                    if ch == q: q = None
                elif ch in '"\'': q = ch
                elif ch in '[{': depth += 1
                elif ch in ']}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            body = s[i + 1:j]; i = j + 1
            opts = split_top(body)
            for o in opts:
                if '=' not in o: raise PErr(f'selector option without = : {o}')
                k, v = o.split('=', 1)
                k = k.strip(); v = v.strip()
                if k not in SEL_OPTS: raise PErr(f'unknown selector option {k}')
                neg = v.startswith('!'); vv = v[1:] if neg else v
                if k == 'type':
                    if vv.startswith('#'):
                        t = vv[1:]
                        if t.startswith('bm:'):
                            if t[3:] not in MY_ENTITY_TAGS: raise PErr(f'unknown entity tag {vv}')
                        elif strip_ns(ns(t)) not in REG['tag/entity_type']: raise PErr(f'unknown entity tag {vv}')
                    elif strip_ns(ns(vv)) not in REG['entity_type']: raise PErr(f'unknown entity type {vv}')
                elif k == 'gamemode':
                    if vv not in ('survival', 'creative', 'adventure', 'spectator'): raise PErr(f'bad gamemode {vv}')
                elif k == 'sort':
                    if vv not in ('nearest', 'furthest', 'random', 'arbitrary'): raise PErr(f'bad sort {vv}')
                elif k in ('limit',):
                    int(vv)
                elif k in ('distance', 'level', 'x_rotation', 'y_rotation'):
                    if not re.fullmatch(r'-?[\d.]*(\.\.)?-?[\d.]*', vv) or vv in ('', '..'): raise PErr(f'bad range {vv}')
                elif k in ('x', 'y', 'z', 'dx', 'dy', 'dz'):
                    float(vv)
                elif k == 'scores':
                    if not re.fullmatch(r'\{([\w.#+-]+=-?\d*(\.\.)?-?\d*)(,[\w.#+-]+=-?\d*(\.\.)?-?\d*)*\}', vv): raise PErr(f'bad scores {vv}')
                    for part in vv[1:-1].split(','):
                        OBJ_REFS.add(part.split('=')[0])
                elif k == 'nbt':
                    e, _ = parse_snbt(vv, 0)
                    if e != len(vv): raise PErr(f'bad nbt option {vv}')
                elif k == 'tag':
                    if not re.fullmatch(r'[\w.+-]*', vv): raise PErr(f'bad tag {vv}')
        if props.get('amount') == 'single' and kind in 'ae' and 'limit=1' not in ' '.join(opts).replace(' ', ''):
            raise PErr('selector must be single (add limit=1)')
        if props.get('type') == 'players' and kind == 'e':
            raise PErr('selector must target players')
        return i, kind
    j = word_end(s, i)
    name = s[i:j]
    if not re.fullmatch(r'[\w-]{1,16}|[0-9a-f-]{36}', name): raise PErr(f'bad player name {name}')
    return j, name


def split_top(body):
    parts, depth, q, cur = [], 0, None, ''
    i = 0
    while i < len(body):
        ch = body[i]
        if q:
            cur += ch
            if ch == '\\': cur += body[i + 1]; i += 2; continue
            if ch == q: q = None
        elif ch in '"\'': q = ch; cur += ch
        elif ch in '[{': depth += 1; cur += ch
        elif ch in ']}': depth -= 1; cur += ch
        elif ch == ',' and depth == 0: parts.append(cur); cur = ''
        else: cur += ch
        i += 1
    if cur.strip(): parts.append(cur)
    return parts


OBJ_REFS = set()


def p_score_holder(s, i, props):
    if s.startswith('@', i): return p_entity(s, i, props)
    j = word_end(s, i)
    if j == i: raise PErr('expected score holder')
    return j, s[i:j]


def p_item_stack(s, i, predicate=False):
    if predicate and s.startswith('*', i):
        j = i + 1; item = '*'
    else:
        tag = s.startswith('#', i)
        j, item = p_rl(s, i + (1 if tag else 0))
        if tag:
            if strip_ns(ns(item)) not in REG['tag/item'] and not (ns(item).startswith('bm:') and os.path.exists(f"{ROOT_DP}/bm/tags/item/{ns(item).split(':')[1]}.json")):
                raise PErr(f'unknown item tag {item}')
        else:
            check_item_id(item, 'item')
    if j < len(s) and s[j] == '[':
        # components
        depth, k, q = 0, j, None
        while k < len(s):
            ch = s[k]
            if q:
                if ch == '\\': k += 2; continue
                if ch == q: q = None
            elif ch in '"\'': q = ch
            elif ch in '[{': depth += 1
            elif ch in ']}':
                depth -= 1
                if depth == 0: break
            k += 1
        body = s[j + 1:k]
        for part in split_top(body):
            part = part.strip()
            for alt in (split_alt(part) if predicate else [part]):
                alt = alt.strip()
                if alt.startswith('!'):
                    key = alt[1:].split('=')[0].split('~')[0]
                    if strip_ns(ns(key)) not in REG['data_component_type']: raise PErr(f'unknown component {key}')
                    continue
                m = re.match(r'([a-z0-9_:./]+)\s*([=~]?)', alt)
                key, op = m.group(1), m.group(2)
                if not op:
                    if not predicate: raise PErr(f'component {key} has no value')
                    if strip_ns(ns(key)) not in REG['data_component_type']: raise PErr(f'unknown component {key}')
                    continue
                e, val = parse_snbt(alt, m.end())
                if e != len(alt): raise PErr(f'trailing junk in component {key}: {alt[e:e+20]!r}')
                if op == '=':
                    check_component(key, val, 'item')
                else:
                    if strip_ns(ns(key)) not in REG['data_component_predicate_type']: raise PErr(f'unknown component predicate {key}')
        j = k + 1
    if not predicate and j < len(s) and s[j] == '{': raise PErr('legacy NBT on item stack is not allowed')
    return j, item


def split_alt(part):
    return [part] if '|' not in part else part.split('|')


def p_block(s, i, predicate=False):
    tag = s.startswith('#', i)
    j, b = p_rl(s, i + (1 if tag else 0))
    if tag:
        if b.startswith('bm:'):
            if b[3:] not in MY_BLOCK_TAGS: raise PErr(f'unknown block tag {b}')
        elif strip_ns(ns(b)) not in REG['tag/block']: raise PErr(f'unknown block tag {b}')
    else:
        bn = strip_ns(ns(b))
        if bn not in BLOCKS: raise PErr(f'unknown block {b}')
    if j < len(s) and s[j] == '[':
        k = s.index(']', j)
        if not tag:
            props = BLOCKS[strip_ns(ns(b))][0]
            for kv in s[j + 1:k].split(','):
                if not kv: continue
                pk, pv = kv.split('=')
                if pk not in props or pv not in props[pk]: raise PErr(f'bad block state {b}[{kv}]')
        j = k + 1
    if j < len(s) and s[j] == '{':
        j, _ = parse_snbt(s, j)
    return j, b


def p_nbt_path(s, i):
    j = word_end(s, i)
    path = s[i:j]
    if path.startswith('{'):
        e, _ = parse_snbt(s, i)
        return e, s[i:e]
    seg = r'([A-Za-z_][\w]*|"[^"]+")(\[[^\]]*\])?'
    if not re.fullmatch(seg + r'(\.' + seg + r')*', path): raise PErr(f'bad nbt path {path}')
    return j, path


def p_particle(s, i):
    j, pid = p_rl(s, i)
    if strip_ns(ns(pid)) not in REG['particle_type']: raise PErr(f'unknown particle {pid}')
    if j < len(s) and s[j] == '{':
        j, _ = parse_snbt(s, j)
    return j, pid


def p_int_range(s, i, integer=True):
    m = re.compile(r'(-?\d+(\.\d+)?)?(\.\.)?(-?\d+(\.\d+)?)?').match(s, i)
    if not m or m.end() == i: raise PErr('bad range')
    return m.end(), m.group(0)


def p_resource(s, i, registry, tag_ok=False):
    tag = s.startswith('#', i)
    if tag and not tag_ok: raise PErr('tag not allowed here')
    j, r = p_rl(s, i + (1 if tag else 0))
    rn = registry.split(':')[-1]
    if not tag:
        if r.startswith('bm:'):
            if not os.path.exists(f"{ROOT_DP}/bm/{rn}/{r.split(':')[1]}.json"):     # 2.13: the pack's own entries (damage types...)
                raise PErr(f'custom id {r} in vanilla registry {rn}')
            return j, r
        if strip_ns(ns(r)) not in REG[rn]: raise PErr(f'unknown {rn}: {r}')
    return j, r


def p_function(s, i):
    j, f = p_rl(s, i + (1 if s.startswith('#', i) else 0))
    if f.startswith('bm:') and f[3:] not in MY_FUNCS: raise PErr(f'missing function {f}')
    return j, f


def p_loot(s, i, kind):
    if s.startswith('{', i):
        return parse_snbt(s, i)
    j, r = p_rl(s, i)
    if r.startswith('bm:'):
        pool = {'loot_table': MY_LOOT, 'loot_modifier': MY_MODS, 'loot_predicate': MY_PREDS}[kind]
        if r[3:] not in pool: raise PErr(f'missing {kind} {r}')
    elif kind == 'loot_table' and strip_ns(ns(r)) not in REG['loot_table']: raise PErr(f'unknown vanilla loot table {r}')
    return j, r


ITEM_SLOT_RE = re.compile(r'(container\.(\d+|\*)|hotbar\.(\d+|\*)|inventory\.(\d+|\*)|enderchest\.(\d+|\*)|mob\.inventory\.(\d+|\*)|horse\.(\d+|\*|saddle|chest)|'
                          r'weapon(\.mainhand|\.offhand|\.\*)?|armor\.(head|chest|legs|feet|body|\*)|player\.(cursor|crafting\.(\d+|\*))|contents|saddle|\*)$')


def parse_arg(node, s, i):
    p = node['parser']; props = node.get('properties', {})
    if p == 'brigadier:string':
        t = props.get('type')
        if t == 'greedy': return len(s), s[i:]
        if t == 'phrase' and s[i:i + 1] in '"\'':
            sn = SNBT(s, i); sn.qstr(); return sn.i, None
        j = word_end(s, i); return j, s[i:j]
    if p in ('brigadier:integer', 'brigadier:long'):
        j, v = p_number(s, i, True)
        if 'min' in props and v < props['min']: raise PErr(f'{v} below min {props["min"]}')
        if 'max' in props and v > props['max']: raise PErr(f'{v} above max {props["max"]}')
        return j, v
    if p in ('brigadier:double', 'brigadier:float'):
        j, v = p_number(s, i)
        if 'min' in props and v < props['min']: raise PErr(f'{v} below min')
        if 'max' in props and v > props['max']: raise PErr(f'{v} above max')
        return j, v
    if p == 'brigadier:bool':
        j = word_end(s, i)
        if s[i:j] not in ('true', 'false'): raise PErr('expected bool')
        return j, s[i:j]
    if p == 'minecraft:entity': return p_entity(s, i, props)
    if p == 'minecraft:score_holder': return p_score_holder(s, i, props)
    if p == 'minecraft:vec3': return p_coords(s, i, 3)
    if p == 'minecraft:vec2': return p_coords(s, i, 2)
    if p == 'minecraft:block_pos': return p_coords(s, i, 3, True)
    if p == 'minecraft:column_pos': return p_coords(s, i, 2, True)
    if p == 'minecraft:rotation': return p_coords(s, i, 2)
    if p == 'minecraft:nbt_compound_tag':
        if not s.startswith('{', i): raise PErr('expected compound')
        return parse_snbt(s, i)
    if p == 'minecraft:nbt_tag': return parse_snbt(s, i)
    if p == 'minecraft:nbt_path': return p_nbt_path(s, i)
    if p in ('minecraft:component', 'minecraft:style'):
        j, v = parse_snbt(s, i)
        check_text(v, 'text')
        return j, v
    if p == 'minecraft:message': return len(s), s[i:]
    if p == 'minecraft:item_stack': return p_item_stack(s, i)
    if p == 'minecraft:item_predicate': return p_item_stack(s, i, True)
    if p == 'minecraft:block_state': return p_block(s, i)
    if p == 'minecraft:block_predicate': return p_block(s, i, True)
    if p == 'minecraft:particle': return p_particle(s, i)
    if p in ('minecraft:int_range', 'minecraft:float_range'): return p_int_range(s, i)
    if p == 'minecraft:resource': return p_resource(s, i, props['registry'])
    if p == 'minecraft:resource_or_tag': return p_resource(s, i, props['registry'], True)
    if p in ('minecraft:resource_key', 'minecraft:resource_or_tag_key'):
        j, r = p_rl(s, i + (1 if s.startswith('#', i) else 0))
        rn = props['registry'].split(':')[-1]
        if r.startswith('bm:'):
            if rn == 'worldgen/structure' and r[3:] not in ('black_market', 'graveyard'): raise PErr(f'unknown structure {r}')
            if rn == 'advancement' and r[3:] not in MY_ADV: raise PErr(f'missing advancement {r}')
            if rn == 'worldgen/template_pool': pass
        elif rn in REG and strip_ns(ns(r)) not in REG[rn]: raise PErr(f'unknown {rn}: {r}')
        return j, r
    if p == 'minecraft:resource_location':
        j, r = p_rl(s, i)
        if node.get('_argname') == 'sound' and strip_ns(ns(r)) not in REG['sound_event']: raise PErr(f'unknown sound event {r}')
        return j, r
    if p == 'minecraft:function': return p_function(s, i)
    if p == 'minecraft:time':
        m = re.compile(r'\d+(\.\d+)?[tsd]?').match(s, i)
        if not m: raise PErr('bad time'); return m.end(), m.group(0)
        return m.end(), m.group(0)
    if p == 'minecraft:gamemode':
        j = word_end(s, i)
        if s[i:j] not in ('survival', 'creative', 'adventure', 'spectator'): raise PErr('bad gamemode')
        return j, s[i:j]
    if p == 'minecraft:objective':
        j = word_end(s, i); OBJ_REFS.add(s[i:j]); return j, s[i:j]
    if p == 'minecraft:objective_criteria':
        j = word_end(s, i); c = s[i:j]
        if c not in ('dummy', 'trigger', 'deathCount', 'playerKillCount', 'totalKillCount', 'health', 'xp', 'level', 'food', 'air', 'armor'):
            m = re.fullmatch(r'minecraft\.(\w+):minecraft\.([\w.]+)', c)
            if not m: raise PErr(f'bad criteria {c}')
            if m.group(1) == 'custom' and m.group(2) not in REG['custom_stat']: raise PErr(f'unknown custom stat {m.group(2)}')
        return j, c
    if p in ('minecraft:item_slot', 'minecraft:item_slots', 'minecraft:slot_source'):     # 26.3: <slots> is a slot_source
        j = word_end(s, i)
        if not ITEM_SLOT_RE.match(s[i:j]): raise PErr(f'bad item slot {s[i:j]}')
        return j, s[i:j]
    if p == 'minecraft:loot_table': return p_loot(s, i, 'loot_table')
    if p == 'minecraft:loot_modifier': return p_loot(s, i, 'loot_modifier')
    if p == 'minecraft:loot_predicate': return p_loot(s, i, 'loot_predicate')
    if p == 'minecraft:entity_anchor':
        j = word_end(s, i)
        if s[i:j] not in ('eyes', 'feet'): raise PErr('bad anchor')
        return j, s[i:j]
    if p == 'minecraft:operation':
        j = word_end(s, i); return j, s[i:j]
    if p == 'minecraft:swizzle':
        j = word_end(s, i); return j, s[i:j]
    if p == 'minecraft:dimension':
        j, r = p_rl(s, i); return j, r
    if p == 'minecraft:dialog':                     # 1.18: a dialog id, or an inline dialog checked against the 26.2 schema
        if s.startswith('{', i):
            j, v = parse_snbt(s, i)
            import dialogs262
            errs = []
            dialogs262.check_dialog(plain(v), 'inline dialog', errs.append, check_line)
            if errs: raise PErr('; '.join(errs[:3]))
            return j, v
        j, r = p_rl(s, i)
        if r.startswith('bm:'):
            if r[3:] not in MY_DIALOGS: raise PErr(f'missing dialog {r}')
        elif strip_ns(ns(r)) not in REG['dialog']: raise PErr(f'unknown vanilla dialog {r}')
        return j, r
    if p in ('minecraft:template_rotation', 'minecraft:template_mirror', 'minecraft:heightmap', 'minecraft:team', 'minecraft:uuid',
             'minecraft:scoreboard_slot', 'minecraft:team_color', 'minecraft:hex_color', 'minecraft:game_profile',
             'minecraft:resource_selector'):
        j = word_end(s, i); return j, s[i:j]
    raise PErr(f'no parser for {p}')


def match(node, s, i, depth=0):
    """node: current node already consumed; s[i:] is the remainder (starting at a space or end)."""
    if i == len(s):
        if node.get('executable'): return True, None
        return False, f'incomplete command (node not executable)'
    if s[i] != ' ': return False, f'expected space at {s[i:i+20]!r}'
    i += 1
    children = node.get('children', {})
    if 'redirect' in node:
        target = TREE
        for part in node['redirect']: target = target['children'][part]
        children = target.get('children', {})
    if node.get('_name') == 'run' or (not children and node.get('type') == 'literal' and node.get('_name') == 'run'):
        children = TREE['children']
    if not children and node.get('_name') == 'run':
        children = TREE['children']
    best = None
    w_end = word_end(s, i)
    word = s[i:w_end]
    for name, ch in children.items():
        if ch['type'] == 'literal':
            if name == word:
                ch['_name'] = name
                ok, err = match(ch, s, w_end, depth + 1)
                if ok: return True, None
                best = best or err
    for name, ch in children.items():
        if ch['type'] == 'argument':
            ch['_argname'] = name
            try:
                j, _ = parse_arg(ch, s, i)
            except PErr as e:
                best = best or f'<{name}>: {e}'
                continue
            except Exception as e:
                best = best or f'<{name}>: parse crash {type(e).__name__} {e}'
                continue
            ch['_name'] = name
            ok, err = match(ch, s, j, depth + 1)
            if ok: return True, None
            best = err or best
    return False, best or f'no matching child for {word!r}'


def check_line(line):
    if line.startswith('$'):
        line = line[1:].replace('$(eid)', 'minecraft:pig').replace('$(data)', '{}').replace('$(dim)', 'minecraft:overworld').replace('$(path)', 'Inventory[{Slot:0b}]').replace('$(slot)', 'container.0').replace('$(iid)', 'token').replace('$(id)', 'minecraft:diamond_sword').replace('$(a)', '30').replace('$(b)', '210')
        line = re.sub(r'\$\(\w+\)', '1', line)      # any other macro argument: a (positive) number is the usual substitution
    first = line.split(' ', 1)[0]
    if first not in TREE['children']: return f'unknown command {first}'
    node = TREE['children'][first]; node['_name'] = first
    ok, err = match(node, line, len(first))
    return None if ok else err


def run():
    errs = 0; n = 0
    for f in sorted(glob.glob(ROOT_DP + '/bm/function/**/*.mcfunction', recursive=True)):
        rel = f[len(ROOT_DP) + 13:]
        for ln, line in enumerate(open(f), 1):
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'): continue
            n += 1
            err = check_line(line)
            if err:
                errs += 1
                print(f'✗ {rel}:{ln}: {err}\n    {line[:160]}')
    # position lint: `execute as <entities> ... run function F` with no `at`/`positioned` runs F at the
    # server's default position (world spawn, overworld). Flag it when F (or anything it calls) is positional.
    src = {f[len(ROOT_DP) + 13:-11]: open(f).read() for f in glob.glob(ROOT_DP + '/bm/function/**/*.mcfunction', recursive=True)}
    memo = {}
    def positional(fn_name, seen=()):
        if fn_name in memo: return memo[fn_name]
        body = src.get(fn_name, '')
        hit = bool(re.search(r'(^|\s)[~^][-\d.]*(\s|$)|distance=|sort=nearest|if dimension|if predicate|if block|unless block', body, re.M))
        if not hit:
            # (a call that sets its own position - `execute at @s ... run function` - doesn't inherit the caller's)
            calls = [c for ln in body.split('\n') if not re.search(r'\b(at|positioned) ', ln.split(' run ')[0]) for c in re.findall(r'function bm:([\w/]+)', ln)]
            for callee in calls:
                if callee not in seen and positional(callee, seen + (fn_name,)): hit = True; break
        memo[fn_name] = hit
        return hit
    for rel, body in src.items():
        for ln, line in enumerate(body.split('\n'), 1):
            m = re.match(r'(\$?)execute (.*?) run function bm:([\w/]+)', line)
            if not m: continue
            sub = ' ' + m.group(2)
            execs = [mm.start() for mm in re.finditer(r'(?<!positioned)(?<!rotated) as @', sub)]
            if not execs: continue
            tail = sub[execs[-1]:]
            if re.search(r'\b(at|positioned|rotated|in) ', tail): continue
            if positional(m.group(3)):
                errs += 1; print(f'✗ {rel}:{ln}: function {m.group(3)} is positional but runs without `at @s`\n    {line[:160]}')
    # objectives referenced must be created in load
    load = open(ROOT_DP + '/bm/function/load.mcfunction').read()
    made = set(re.findall(r'scoreboard objectives add (\S+)', load))
    for o in sorted(OBJ_REFS - made):
        print(f'✗ objective used but never created: {o}'); errs += 1
    print(f'\n{n} command lines checked against the 26.3 command tree: {errs} errors')
    for w in sorted(set(WARN))[:20]: print('  note:', w)
    return errs


if __name__ == '__main__':
    sys.exit(1 if run() else 0)


# ============================================================ 26.3 JSON, viewed in the 26.2 shapes the semantic checks were written for
# (the 26.3 server itself validates the real shapes at load; these checks are about ids, items, trades and wiring)
def _conds262(c):
    if c is None: return []
    if isinstance(c, list): return [_cond262(x) for x in c]
    if isinstance(c, dict) and strip_ns(c.get('type', '')) == 'all_of': return [_cond262(x) for x in c['terms']]
    return [_cond262(c)]


def _cond262(c):
    if not isinstance(c, dict): return c
    c = dict(c)
    if 'type' in c and 'condition' not in c: c['condition'] = c.pop('type')
    if 'terms' in c: c['terms'] = [_cond262(x) for x in c['terms']]
    if 'term' in c: c['term'] = _cond262(c['term'])
    return c


def _cd(comps):
    if isinstance(comps, dict) and isinstance(comps.get('minecraft:custom_data'), str):
        comps = dict(comps); comps['minecraft:custom_data'] = plain(parse_snbt(comps['minecraft:custom_data'], 0)[1])
    return comps


def _func262(f):
    if not isinstance(f, dict): return f
    f = dict(f)
    if 'type' in f and 'function' not in f: f['function'] = f.pop('type')
    if 'condition' in f and not isinstance(f['condition'], str): f['conditions'] = _conds262(f.pop('condition'))
    if 'components' in f: f['components'] = _cd(f['components'])
    if 'functions' in f: f['functions'] = [_func262(x) for x in (f['functions'] if isinstance(f['functions'], list) else [f['functions']])]
    for k in ('modifier', 'on_pass', 'on_fail'):
        if k in f: f[k] = _mods262(f[k])
    return f


def _mods262(m):
    if isinstance(m, str): return m
    m = m if isinstance(m, list) else [m]
    out = []
    for x in m:
        x = _func262(x)
        if isinstance(x, dict) and x.get('function') == 'minecraft:sequence' and 'components' not in x: out += x['functions']
        else: out.append(x)
    return out


def _entry262(e):
    e = dict(e)
    if 'modifier' in e: e['functions'] = _mods262(e.pop('modifier'))
    if 'condition' in e and not isinstance(e['condition'], str): e['conditions'] = _conds262(e.pop('condition'))
    if 'items' in e and strip_ns(e.get('type', '')) == 'tag': e['name'] = e.pop('items').lstrip('#')
    if 'children' in e: e['children'] = [_entry262(x) for x in e['children']]
    return e


def jload(path):
    """json.load for a data pack file, translated to the 26.2 shapes used by the semantic checks."""
    d = json.load(open(path))
    parts = path.replace('\\', '/').split('/')
    if 'data' not in parts: return d
    i = parts.index('data'); kind = parts[i + 2] if len(parts) > i + 2 else ''
    if kind == 'loot_table':
        d = dict(d)
        if 'modifier' in d: d['functions'] = _mods262(d.pop('modifier'))
        pools = []
        for p in d.get('pools', []):
            p = dict(p)
            if 'modifier' in p: p['functions'] = _mods262(p.pop('modifier'))
            if 'condition' in p and not isinstance(p['condition'], str): p['conditions'] = _conds262(p.pop('condition'))
            p['entries'] = [_entry262(x) for x in p.get('entries', [])]
            pools.append(p)
        if 'pools' in d: d['pools'] = pools
        return d
    if kind == 'item_modifier': return _mods262(d)
    if kind == 'predicate': return _cond262(d) if not (isinstance(d, dict) and strip_ns(d.get('type', '')) == 'all_of') else _conds262(d)
    if kind == 'advancement':
        d = json.loads(json.dumps(d))
        for crit in d.get('criteria', {}).values():
            c = crit.get('conditions')
            if not isinstance(c, dict): continue
            for k in ('player', 'entity', 'villager', 'projectile', 'shooter', 'parent', 'partner', 'child', 'zombie', 'lightning',
                      'source', 'bystander', 'killing_blow', 'direct_entity', 'source_entity', 'location'):
                if isinstance(c.get(k), dict) and ('type' in c[k] or 'condition' in c[k]): c[k] = _conds262(c[k])
            if 'loot_tables' in c: c['loot_table'] = c.pop('loot_tables')
        return d
    return d
