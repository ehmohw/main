// 3.1: the new followers in the every-follower tests (t138 figurines, t145 / t158 KINDS, t146 frames, t156 dolls) - only the
// ones fol5flag.py has switched on, in their save-number order. Each: [kind, flag, name, summon item, host tag, figurine parts,
// frame spot on t146's wall].
const FL = require('fs').readFileSync('/home/user/main/bm_build/fol5flag.py', 'utf8');
const on = (k) => new RegExp(`^${k} = True`, 'm').test(FL);
const ALL = [['glitch', 'GLITCH', 'The Glitch', 'glitch_rom', 'bm.gxpet', 9, -16],
             ['cake', 'CAKE', 'The Cake', 'cake_candle', 'bm.czpet', 9, 17],
             ['sapling', 'SAPLING', 'The Sapling', 'golden_pip', 'bm.sxpet', 9, -17],
             ['spawner', 'SPAWNER', 'The Spawner', 'pilot_light', 'bm.nxpet', 7, 18],
             ['cairn', 'CAIRN', 'The Cairn', 'waystone_heart', 'bm.axpet', 23, -18],
             ['knight', 'KNIGHT', 'The Hollow Statue Knight', 'knight_token', 'bm.hxpet', 0, 0],
             ['mimic', 'MIMIC', 'The Mimic', 'mimic_key', 'bm.mxpet', 0, 1]];
const live = ALL.filter(a => on(a[1]));
module.exports = {
  on, live, DOODLEMOB: on('DOODLEMOB'),
  kinds: () => live.map(a => a[0]),                                            // (t145, t158)
  figs: () => live.map(a => [a[3], a[2], a[5]]),                              // (t138: [item, name, parts])
  frames: () => live.map(a => [a[2], a[3], 'wolf', a[4], a[6]]),              // (t146: [name, item, host, tag, dx])
  dolls: () => live.map(a => `doll_${a[0]}`),                                  // (t156)
};
