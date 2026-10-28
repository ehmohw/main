// 2.98: BATTY of the Gutter Gentry, reformed, as a regular (non-op) player (gentry_t): the first win over the Gentry leaves his Calling
// Token. BITE, SCREECH (two foes close: dizzy and slowed), WING GUST (charged: blown back), NIGHT FLIGHT (Night Vision, Slow Falling).
require('./gentry_t')({ W: 'batty', NAME: 'Batty', ab: 'yt', q: 'yk', pfx: 'p232b', pre: 'gb_', item: 'gentry_batty', n: 1, others: ['gentry_eggbert', 'gentry_count'],
  parts: 4, figParts: 4, hp: 30, X: 17500, Z: 17600,
  called: /Yeah, yeah, I'm here/, home: /Back to the rafters/, sit: /folds his wings round himself/, stand: /Up and at 'em/,
  ways: ['Bite', 'Screech', 'Wing Gust', 'Night Flight'], plain: 'His own navy fur', looks: ['Crimson Fur', 'Ash Fur', 'Moss Fur'], lookPart: 'body',
  crowd: ['SCREECH', 'nausea'], charge: ['WING GUST', null], kind: ['NIGHT FLIGHT', 'night_vision', 'slow_falling'] });
