"""Cross-reference lints over the built datapack: names that are read but never set anywhere (valid syntax, so check262
passes them, but in game the check is simply never true). Run as: BM_OUT=out_p2 python3 check_xref.py

1. TAGS: a selector tests tag=X, but nothing ever adds X (no `tag ... add X`, no Tags:[...] in a summon, merge, loot or
   structure template). The 2.67 secret-door cleanup tested bm.eshrhit for bm.eshr_hit, and never matched.
2. SCORES: a command reads objective X, but no `scoreboard objectives add X` exists.
3. STORAGE: `data get/modify ... from storage S P.k` / `if data storage S P.k` reads a key nothing ever writes.
4. ITEMS: a test for custom_data {bm:"x"} names an item that isn't defined.
5. FUNCTIONS: a function is never called from anywhere (not a command, an advancement, a tag, a dialog, an item, a
   macro pattern) - reported as dead code (a warning, not an error).
"""
import glob, gzip, json, os, re, sys
from collections import defaultdict

OUT = os.environ.get('BM_OUT', 'out')
DP = glob.glob(f'{OUT}/*_DP')[0] if glob.glob(f'{OUT}/*_DP') else f'{OUT}/BlackMarket_DP'
DATA = f'{DP}/data'
FN = f'{DATA}/bm/function/'

texts = {}                                      # every text file of the pack: path -> content
for f in glob.glob(f'{DATA}/**/*', recursive=True):
    if os.path.isfile(f) and f.endswith(('.mcfunction', '.json')):
        texts[f] = open(f, encoding='utf-8').read()
structs = {}                                    # structure templates: their strings (tags of the entities inside)
for f in glob.glob(f'{DATA}/**/*.nbt', recursive=True):
    raw = open(f, 'rb').read()
    try: raw = gzip.decompress(raw)
    except OSError: pass
    structs[f] = raw.decode('latin-1')

ALL = '\n'.join(texts.values())
ALLS = '\n'.join(structs.values())
errs, warns = [], []

# ---------------------------------------------------------------- 1. tags
reads = defaultdict(set)
for f, s in texts.items():
    for t, mac in re.findall(r'tag=!?([A-Za-z0-9_.\-+]+)(\$?)', s):
        if not mac: reads[t].add(os.path.relpath(f, DATA))
writes = set()
writes |= set(re.findall(r'\btag @[aesprn](?:\[(?:[^\[\]{}]|\{[^{}]*\}|\[[^\[\]]*\])*\])? add ([A-Za-z0-9_.\-+]+)', ALL))
writes |= set(re.findall(r'\btag [A-Za-z0-9_]+ add ([A-Za-z0-9_.\-+]+)', ALL))
for blob in re.findall(r'Tags\s*:\s*\[([^\]]*)\]', ALL) + re.findall(r'"Tags"\s*:\s*\[([^\]]*)\]', ALL):
    writes |= set(re.findall(r'"([A-Za-z0-9_.\-+]+)"', blob))
for blob in re.findall(r'Tags append value "([^"]+)"', ALL): writes.add(blob)
writes |= set(re.findall(r'\$\(([a-z_]+)\)', ''))                       # (macros: handled below)
writes |= set(re.findall(r'(bm\.[A-Za-z0-9_.\-+]+)', ALLS))               # every string in a template counts as a set tag
macro_tags = re.findall(r'tag [^\n]* add ([A-Za-z0-9_.\-+]*\$\([a-z_]+\)[A-Za-z0-9_.\-+]*)', ALL) + \
    re.findall(r'"([A-Za-z0-9_.\-+]*\$\([a-z_]+\)[A-Za-z0-9_.\-+]*)"', ' '.join(re.findall(r'Tags\s*:\s*\[([^\]]*)\]', ALL)))
macro_res = [re.compile('^' + re.escape(m).replace(r'\$\(', '(').split('(')[0] + '.*$') for m in macro_tags]
def legacy(t):
    # only ever used to sweep away entities older versions left in worlds (kill / send below the world / retire), to skip
    # them, or by a marker dispatcher in npc/ (a spawn marker kind no current template places)
    hits = [(f, l) for f, s in texts.items() for l in s.splitlines() if re.search(rf'tag=!?{re.escape(t)}(?![A-Za-z0-9_.\-+$])', l)]
    return hits and all(re.search(r'\bkill @e|\bkill @s|tp @e\[[^\]]*\] ~ -\d+ ~|tag=!' + re.escape(t) + r'|_retire$', l) or
                        ('/function/npc/' in f and l.startswith(f'execute if entity @s[tag={t}] run ')) for f, l in hits)
for t, where in sorted(reads.items()):
    if t in writes or '$(' in t: continue
    if any(r.match(t) for r in macro_res): continue
    if legacy(t): warns.append(f'LEGACY TAG {t}: only swept away / excluded'); continue
    errs.append(f'TAG {t}: tested in {sorted(where)[:3]}{" ..." if len(where) > 3 else ""} but never added')

# ---------------------------------------------------------------- 2. objectives
added = set(re.findall(r'scoreboard objectives add ([A-Za-z0-9_.\-+]+)', ALL))
used = defaultdict(set)
pat = [r'scoreboard players (?:set|add|remove|reset|get|enable|operation|display \w+) \S+ ([A-Za-z0-9_.\-+]+)',
       r'score \S+ ([A-Za-z0-9_.\-+]+)', r'scores=\{([^}]*)\}', r'operation \S+ \S+ \S+ \S+ ([A-Za-z0-9_.\-+]+)',
       r'"objective"\s*:\s*"([^"]+)"', r'objective:\s*"([^"]+)"', r'trigger ([A-Za-z0-9_.\-+]+)']
for f, s in texts.items():
    for l in s.splitlines():
        if l.startswith('#'): continue
        for p in pat:
            for m in re.findall(p + r'(?![A-Za-z0-9_.\-+$])', l):
                if p.startswith('scores'):
                    for o in re.findall(r'([A-Za-z0-9_.\-+]+)=', m): used[o].add(os.path.relpath(f, DATA))
                else: used[m].add(os.path.relpath(f, DATA))
for o, where in sorted(used.items()):
    if o in added or '$(' in o or o in ('*',) or not re.match(r'^[a-z]', o) or '.' not in o: continue   # (ours are all bm.*; bare words are sound sources)
    errs.append(f'SCORE {o}: used in {sorted(where)[:3]}{" ..." if len(where) > 3 else ""} but never created')

# ---------------------------------------------------------------- 3. storage
def key(path):
    return re.split(r'[.\[{]', path, 1)[0]
swrites, sreads = set(), defaultdict(set)
for f, s in texts.items():
    for l in s.splitlines():
        for st, p in re.findall(r'data (?:modify|merge|remove) storage (\S+) (\S+)', l): swrites.add((st, key(p)))
        for st, p in re.findall(r'store (?:result|success) storage (\S+) (\S+)', l): swrites.add((st, key(p)))
        for st, p in re.findall(r'(?:data get storage|if data storage|unless data storage|from storage|with storage) (\S+) ?(\S*)', l):
            if p and not p.startswith(('run', 'if', 'unless')): sreads[(st, key(p))].add(os.path.relpath(f, DATA))
        for st in re.findall(r'data merge storage (\S+) \{([^}]*)', l):
            pass
    for st, blob in re.findall(r'data merge storage (\S+) (\{.*\})', s):
        for k in re.findall(r'[{,]\s*([A-Za-z0-9_]+)\s*:', blob): swrites.add((st, k))
for (st, k), where in sorted(sreads.items()):
    if (st, k) in swrites or '$(' in k or not k: continue
    errs.append(f'STORAGE {st} {k}: read in {sorted(where)[:3]} but never written')

# ---------------------------------------------------------------- 4. items
defined = {os.path.basename(f)[:-5] for f in glob.glob(f'{DATA}/bm/loot_table/items/*.json')}     # (every item has its give table)
if defined:
    for f, s in texts.items():
        for iid in set(re.findall(r'custom_data[^{]*\{\s*bm\s*:\s*\\?"([a-z0-9_]+)\\?"', s)):
            if iid not in defined and '/retire/' not in f and 'loop/second' not in f: errs.append(f'ITEM {iid}: tested in {os.path.relpath(f, DATA)} but no such item')

# ---------------------------------------------------------------- 5. dead functions
defs = {os.path.relpath(f, FN)[:-len('.mcfunction')] for f in glob.glob(FN + '**/*.mcfunction', recursive=True)}
refs = set(re.findall(r'bm:([a-z0-9_/.\-]+)', ALL)) | set(re.findall(r'bm:([a-z0-9_/.\-]+)', ALLS))
dyn = [re.compile('^' + re.escape(r).replace(r'\$\(', '(').split('(')[0]) for r in re.findall(r'bm:([a-z0-9_/.\-]*\$\([a-z_]+\)[a-z0-9_/.\-]*)', ALL)]
ENTRY = ('admin/', 'load', 'tick', 'uninstall', 'loop/')
dead = sorted(d for d in defs if d not in refs and not d.startswith(ENTRY) and not any(r.match(d) for r in dyn))
for d in dead: warns.append(f'DEAD FUNCTION {d}')

for e in errs: print('ERROR', e)
if '-v' in sys.argv:
    for w in warns: print('warn ', w)
nd = sum(w.startswith('DEAD') for w in warns)
print(f'cross-reference lints: {len(errs)} errors, {nd} dead functions, {len(warns) - nd} legacy tags ({len(texts)} files, {len(structs)} structures)')
