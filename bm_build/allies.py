"""2.67: one list of everyone on the player's side.

Every weapon and spell that hits "anything but the player's friends" spelled its own exclusion list, and each new follower was
added to a few of them: the 2.67 audit found KillerWatt, Zib, the raid hirelings and escorts missing from all 43 lists, Celi and
Leo from 26, and the Mercenary excluded under a tag he never carried (bm.merc - he is bm.mercpet), so a stray bolt could fell
your own companion. This pass runs last: any selector that already skips a follower now skips all of them. A new follower only
needs adding to ALLIES.
"""
import re

ALLIES = ['bm.wilfrey', 'bm.wil_body', 'bm.frogpet', 'bm.mercpet', 'bm.cecilpet', 'bm.emmapet', 'bm.celipet', 'bm.donado',
          'bm.kxpet', 'bm.leopet', 'bm.zibpet', 'bm.hire', 'bm.eskhost', 'bm.skiff']
_MARK = ('tag=!bm.frogpet', 'tag=!bm.emmapet', 'tag=!bm.cecilpet', 'tag=!bm.merc,', 'tag=!bm.merc]')
_SEL = re.compile(r'@e\[(?:[^\[\]{}]|\{[^{}]*\}|\[[^\[\]]*\])*\]')


def _fix(sel):
    if not any(m in sel for m in _MARK): return sel
    sel = re.sub(r'tag=!bm\.merc(?=[,\]])', 'tag=!bm.mercpet', sel)
    have = set(re.findall(r'tag=!([A-Za-z0-9_.\-+]+)', sel))
    add = ''.join(f',tag=!{t}' for t in ALLIES if t not in have)
    return sel[:-1] + add + ']'


def finalize(G):
    n = 0
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            if '@e[' not in l or not any(m in l for m in _MARK): continue
            new = _SEL.sub(lambda m: _fix(m.group(0)), l)
            if new != l: lines[i] = new; n += 1
    return n
