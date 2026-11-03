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


def _hosts():
    # (3.0g: every follower since 2.67 too - their hosts, from the Partner Wheel's list - wear one shared tag, bm.ally, given each second)
    import phase125
    return {**{w[4].split(',')[0]: w[3] for w in phase125.WHO.values()}, 'bm.wil_body': 'wither_skeleton'}


def _fix(sel):
    if not any(m in sel for m in _MARK): return sel
    sel = re.sub(r'tag=!bm\.merc(?=[,\]])', 'tag=!bm.mercpet', sel)
    have = set(re.findall(r'tag=!([A-Za-z0-9_.\-+]+)', sel))
    add = ''.join(f',tag=!{t}' for t in ALLIES + ['bm.ally'] if t not in have)
    return sel[:-1] + add + ']'


# 3.0g: Wilfrey's body is a wither skeleton (bm.wil_body) - and "the nearest monster" in ~1200 selectors (every follower's strike,
# splash and charge-up: Emma's crescent axe went for him) is any #bm:hostile. Every selector picking by a monster tag skips him.
# (Every other follower host and every tamed animal is a wolf, cat or bat - in none of these tags.)
_FOE_TYPES = ('#bm:hostile', '#bm:gv_hostile', '#bm:p42_foe', '#bm:frz_target', '#bm:p255_wild', '#minecraft:undead', '#minecraft:skeletons')
_FOE = re.compile(r'type=(' + '|'.join(re.escape(t) for t in _FOE_TYPES) + r')(?=[,\]])')


def _skip_wil(sel):
    if not _FOE.search(sel) or 'bm.wil_body' in sel: return sel
    return sel[:-1] + ',tag=!bm.wil_body]'


def finalize(G):
    n = 0
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            if '@e[' not in l: continue
            new = _SEL.sub(lambda m: _skip_wil(m.group(0)), l) if '#' in l else l
            if any(m in new for m in _MARK): new = _SEL.sub(lambda m: _fix(m.group(0)), new)
            if new != l: lines[i] = new; n += 1
    G.FUNCS['allies/tag'] = [f'tag @e[type=minecraft:{ty},tag={t},tag=!bm.ally] add bm.ally' for t, ty in _hosts().items()]
    G.FUNCS['loop/second'].append('function bm:allies/tag')
    return n
