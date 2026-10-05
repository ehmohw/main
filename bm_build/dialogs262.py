"""1.18: structural check of 26.2 dialogs (data/<ns>/dialog/*.json and inline `dialog show` SNBT), from the
SpyglassMC vanilla-mcdoc java/data/dialog schema (mod.mcdoc, action.mcdoc, body.mcdoc, input.mcdoc)."""

TYPES = {'notice', 'confirmation', 'multi_action', 'server_links', 'dialog_list'}
BASE = {'type', 'title', 'external_title', 'body', 'inputs', 'can_close_with_escape', 'after_action', 'pause'}
EXTRA = {'notice': {'action'}, 'confirmation': {'yes', 'no'}, 'multi_action': {'actions', 'exit_action', 'columns'},
         'server_links': {'exit_action', 'columns', 'button_width'}, 'dialog_list': {'exit_action', 'columns', 'button_width', 'dialogs'}}
ACTIONS = {'change_page': {'page'}, 'copy_to_clipboard': {'value'}, 'custom': {'id', 'payload'}, 'open_url': {'url'},
           'run_command': {'command'}, 'show_dialog': {'dialog'}, 'suggest_command': {'command'},
           'dynamic/run_command': {'template'}, 'dynamic/custom': {'id', 'additions'}}
TEXT_KEYS = {'text', 'translate', 'with', 'fallback', 'score', 'selector', 'separator', 'keybind', 'nbt', 'block', 'entity', 'storage', 'interpret',
             'source', 'object', 'player', 'atlas', 'sprite', 'type', 'extra', 'color', 'font', 'bold', 'italic', 'underlined', 'strikethrough',
             'obfuscated', 'shadow_color', 'insertion', 'click_event', 'hover_event'}


def strip(i):
    return i.split(':', 1)[1] if isinstance(i, str) and i.startswith('minecraft:') else i


def check_text(t, where, E):
    if isinstance(t, str): return
    if isinstance(t, list):
        if not t: E(f'{where}: empty text list')
        for k, x in enumerate(t): check_text(x, f'{where}[{k}]', E)
        return
    if not isinstance(t, dict): E(f'{where}: text must be a string, list or compound'); return
    bad = set(t) - TEXT_KEYS
    if bad: E(f'{where}: unknown text keys {sorted(bad)}')
    if not ({'text', 'translate', 'score', 'selector', 'keybind', 'nbt', 'sprite', 'object'} & set(t)): E(f'{where}: text component has no content')
    for k in ('bold', 'italic', 'underlined', 'strikethrough', 'obfuscated', 'interpret'):
        if k in t and t[k] not in (True, False, 0, 1): E(f'{where}.{k}: not a boolean ({t[k]!r})')
    if 'extra' in t: check_text(t['extra'], where + '.extra', E)


def check_int(v, lo, hi, where, E):
    if not isinstance(v, int) or isinstance(v, bool) or not (lo <= v <= hi): E(f'{where}: {v!r} is not an int in {lo}..{hi}')


def check_button(b, where, E, check_cmd):
    if not isinstance(b, dict): E(f'{where}: a button is a compound'); return
    bad = set(b) - {'label', 'tooltip', 'width', 'action'}
    if bad: E(f'{where}: unknown button keys {sorted(bad)}')
    if 'label' not in b: E(f'{where}: button without a label')
    else: check_text(b['label'], where + '.label', E)
    if 'tooltip' in b: check_text(b['tooltip'], where + '.tooltip', E)
    if 'width' in b: check_int(b['width'], 1, 1024, where + '.width', E)
    if 'action' in b:
        a = b['action']
        if not isinstance(a, dict) or 'type' not in a: E(f'{where}.action: needs a type'); return
        t = strip(a['type'])
        if t not in ACTIONS: E(f'{where}.action: unknown type {a["type"]}'); return
        bad = set(a) - {'type'} - ACTIONS[t]
        if bad: E(f'{where}.action: unknown keys {sorted(bad)} for {t}')
        miss = {'run_command': ['command'], 'suggest_command': ['command'], 'open_url': ['url'], 'show_dialog': ['dialog'],
                'change_page': ['page'], 'copy_to_clipboard': ['value'], 'dynamic/run_command': ['template'], 'custom': ['id'], 'dynamic/custom': ['id']}[t]
        for m in miss:
            if m not in a: E(f'{where}.action: {t} needs {m}')
        if t == 'run_command' and check_cmd and isinstance(a.get('command'), str):
            err = check_cmd(a['command'].lstrip('/'))
            if err: E(f'{where}.action.command {a["command"]!r}: {err}')


def check_body(b, where, E):
    if not isinstance(b, dict) or 'type' not in b: E(f'{where}: a body needs a type'); return
    t = strip(b['type'])
    if t == 'plain_message':
        bad = set(b) - {'type', 'contents', 'width'}
        if bad: E(f'{where}: unknown plain_message keys {sorted(bad)}')
        if 'contents' not in b: E(f'{where}: plain_message needs contents')
        else: check_text(b['contents'], where + '.contents', E)
        if 'width' in b: check_int(b['width'], 1, 1024, where + '.width', E)
    elif t == 'item':
        bad = set(b) - {'type', 'item', 'description', 'show_decorations', 'show_tooltip', 'width', 'height'}
        if bad: E(f'{where}: unknown item-body keys {sorted(bad)}')
        if 'item' not in b: E(f'{where}: item body needs an item')
    else:
        E(f'{where}: unknown body type {b["type"]}')


def check_dialog(d, where, E, check_cmd=None):
    if not isinstance(d, dict) or 'type' not in d: E(f'{where}: a dialog needs a type'); return
    t = strip(d['type'])
    if t not in TYPES: E(f'{where}: unknown dialog type {d["type"]}'); return
    bad = set(d) - BASE - EXTRA[t]
    if bad: E(f'{where}: unknown keys {sorted(bad)} for {t}')
    if 'title' not in d: E(f'{where}: dialog without a title')
    else: check_text(d['title'], where + '.title', E)
    if 'body' in d:
        bodies = d['body'] if isinstance(d['body'], list) else [d['body']]
        for k, b in enumerate(bodies): check_body(b, f'{where}.body[{k}]', E)
    aa = d.get('after_action', 'close')
    if aa not in ('close', 'none', 'wait_for_response'): E(f'{where}: after_action {aa!r}')
    if aa == 'none' and d.get('pause', True) not in (False, 0): E(f'{where}: after_action none needs pause:false')
    for k in ('pause', 'can_close_with_escape'):
        if k in d and d[k] not in (True, False, 0, 1): E(f'{where}.{k}: not a boolean')
    if t == 'notice' and 'action' in d: check_button(d['action'], where + '.action', E, check_cmd)
    if t == 'confirmation':
        for k in ('yes', 'no'):
            if k not in d: E(f'{where}: confirmation needs {k}')
            else: check_button(d[k], f'{where}.{k}', E, check_cmd)
    if t == 'multi_action':
        acts = d.get('actions')
        if not isinstance(acts, list) or not acts: E(f'{where}: multi_action needs at least one action')
        else:
            for k, b in enumerate(acts): check_button(b, f'{where}.actions[{k}]', E, check_cmd)
    if t in ('multi_action', 'server_links', 'dialog_list'):
        if 'exit_action' in d: check_button(d['exit_action'], where + '.exit_action', E, check_cmd)
        if 'columns' in d: check_int(d['columns'], 1, 1 << 30, where + '.columns', E)
    if 'inputs' in d: E(f'{where}: inputs are not used by this pack (unchecked)')
