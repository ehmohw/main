"""Logic lints: mistakes that are valid 26.2 syntax (so check262 passes them) but break behaviour in game.
Run as: BM_OUT=out python3 check_logic.py   (0 errors expected)

1. Interaction clicks. `execute on target` from an interaction entity selects the player stored in its `interaction`
   (or `attack`) field. Clearing that field first means `on target` finds nobody and the click silently does nothing
   (the 2.5-2.8 Wilfrey tomb bug and the 1.14-1.15 Xenite Altar bug).
2. Trade prices may only test components that survive in every copy of an item: custom_data, item_model, item_name,
   max_stack_size (1.16: enchantment_glint_override was dropped from prices after Xenite trades refused real shards).
3. (1.18) Menus: every dialog button runs `/trigger <objective>` on an objective the tick function enables for all
   players every tick, and every bm.act code a button sends has a handler range in p28/act.
4. (1.18) Escrow: a currency `clear` with a count only follows a count check (`clear ... 0`) in the same function, or
   lives in a payment helper only reachable through one; escrow is only zeroed where it is paid back or spent on a
   delivered lot; the refund loop, the reload abort and the pending-win delivery all exist.
5. (1.18) Standing: every trade advancement's reward revokes the trade tree so it can fire again.
"""
import glob, os, re, sys
import check262 as C

errs = []
ROOT = C.ROOT_DP + '/bm/function/'
for f in sorted(glob.glob(ROOT + '**/*.mcfunction', recursive=True)):
    rel = f[len(ROOT):-len('.mcfunction')]
    lines = open(f, encoding='utf-8').read().splitlines()
    for field in ('interaction', 'attack'):
        cleared = None
        for i, l in enumerate(lines):
            if re.match(rf'^data remove entity @s {field}\b', l):
                cleared = i
            elif cleared is not None and (' on target' in l if field == 'interaction' else ' on attacker' in l):
                errs.append(f'{rel}:{i + 1}: `on target` after the {field} data was cleared on line {cleared + 1} - the click is lost')
                break

SAFE = {'minecraft:custom_data', 'minecraft:item_model', 'minecraft:item_name', 'minecraft:max_stack_size'}
for f in sorted(glob.glob(ROOT + 'p17/npc/*.mcfunction') + glob.glob(ROOT + 'npc/*.mcfunction')):
    s = open(f, encoding='utf-8').read()
    for m in re.finditer(r'(buy|buyB):\{id:"minecraft:totem_of_undying",count:\d+,components:\{(.*?)\}\},', s):
        keys = set(re.findall(r'"(minecraft:[a-z_]+)":', m.group(2)))
        bad = keys - SAFE
        if bad: errs.append(f'{f[len(ROOT):]}: a currency price tests {sorted(bad)} - only {sorted(SAFE)} are safe')


# ---------------------------------------------------------------- 3. menus
import json
DP = C.ROOT_DP
src = {f[len(ROOT):-len('.mcfunction')]: open(f, encoding='utf-8').read() for f in glob.glob(ROOT + '**/*.mcfunction', recursive=True)}
tick = src.get('tick', '')
enabled = set(re.findall(r'scoreboard players enable @a (\S+)', tick))
cmds = []
for f in glob.glob(DP + '/bm/dialog/**/*.json', recursive=True):
    cmds += [(f.split('/data/')[1], c) for c in re.findall(r'"command":\s*"([^"]+)"', open(f, encoding='utf-8').read())]
for rel, body in src.items():
    for ln in body.split('\n'):
        if 'dialog show' in ln: cmds += [(rel, c) for c in re.findall(r'command:"([^"]+)"', ln)]
act_body = src.get('p28/act', '')
ranges = [(int(a), int(b or a)) for a, b in re.findall(r'#act bm\.pay matches (\d+)(?:\.\.(\d+))?', act_body)]
for rel, c in cmds:
    m = re.match(r'/?trigger (\S+)(?: set (-?\d+))?$', c)
    if not m: errs.append(f'{rel}: menu button runs {c!r} - buttons may only run /trigger (no operator rights needed)'); continue
    if m.group(1) not in enabled: errs.append(f'{rel}: button trigger {m.group(1)} is not enabled for players every tick')
    if m.group(1) == 'bm.act':
        v = int(m.group(2))
        if not any(a <= v <= b for a, b in ranges): errs.append(f'{rel}: bm.act code {v} has no handler range in p28/act')
if not cmds: errs.append('no menu buttons found (lint broken?)')

# ---------------------------------------------------------------- 4. escrow + payments
CUR = ('token', 'medallion', 'trophy', 'lucky_token', 'blood_crystal')
PAY_HELPERS = {'p28/pay/clear_med', 'p28/pay/clear_tro', 'p28/pay/any'}
for rel, body in src.items():
    lines = body.split('\n')
    for i, ln in enumerate(lines):
        m = re.search(r'clear @s \*\[minecraft:custom_data~\{bm:"(\$\(cur\)|' + '|'.join(CUR) + r')"\}\] (\S+)', ln)
        if not m or m.group(2) == '0': continue
        if rel in PAY_HELPERS: continue
        if re.match(r'execute store result score \S+ \S+ run clear ', ln): continue    # takes what's there and checks how many it got
        if rel.startswith('p31/bank/dep_'): continue            # deposits clear exactly what they counted
        cur = m.group(1)
        if not any(re.search(r'clear @s \*\[minecraft:custom_data~\{bm:"' + re.escape(cur) + r'"\}\] 0', l) for l in lines[:i]):
            errs.append(f'{rel}:{i + 1}: takes {cur} without counting it first')
callers = {h: [r for r, b in src.items() if f'function bm:{h}' in b] for h in PAY_HELPERS}
for h, cs in callers.items():
    ok = {'p28/pay/clear_med': {'p28/pay/med_s'}, 'p28/pay/clear_tro': {'p28/pay/break'}}.get(h)
    if ok is not None and set(cs) - ok: errs.append(f'{h} is called from {sorted(set(cs) - ok)} (only the checked payment path may)')
ZERO_OK = {'p30/refund', 'p30/win_here', 'p30/pending', 'p30/act'}
for rel, body in src.items():
    if re.search(r'scoreboard players set @s bm\.escrow 0', body) and rel not in ZERO_OK:
        errs.append(f'{rel}: zeroes escrow without paying it back or delivering a lot')
for need, where in (('function bm:p30/settle', 'loop/second'), ('function bm:p30/abort', 'load'), ('function bm:p30/pending', 'p30/settle'),
                    ('give_med_n', 'p30/refund')):
    if need not in src.get(where, ''): errs.append(f'escrow safety: {where} no longer runs {need}')

# ---------------------------------------------------------------- 5. repeatable Standing
n_adv = 0
for f in glob.glob(DP + '/bm/advancement/p28/trade/**/*.json', recursive=True):
    d = C.jload(f)
    if 'rewards' not in d: continue
    n_adv += 1
    fnn = d['rewards']['function'].split(':', 1)[1]
    if 'advancement revoke @s from bm:p28/trade/root' not in src.get(fnn, ''): errs.append(f'{f.split("/data/")[1]}: reward {fnn} never revokes the trade tree')
if n_adv < 100: errs.append(f'only {n_adv} Standing trade advancements (expected one per trader offer group)')

for e in errs: print('✗', e)
print(f'logic lints: {len(errs)} errors')
sys.exit(1 if errs else 0)
