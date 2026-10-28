// 2.98: THE COUNT of the Gutter Gentry, reformed, as a regular (non-op) player (gentry_t): the third win over the Gentry leaves his
// Calling Token. CANE, BLOBLINGS (two foes close: bounced off, weakened), A GENTLEMAN'S DUEL (charged: weakened), NOBLESSE OBLIGE
// (Resistance and Absorption for you).
require('./gentry_t')({ W: 'count', NAME: 'The Count', ab: 'kn', q: 'kz', pfx: 'p232c', pre: 'gc_', item: 'gentry_count', n: 3, others: ['gentry_batty', 'gentry_eggbert'],
  parts: 6, figParts: 6, hp: 36, X: 17700, Z: 17600,
  called: /At your service\. Reluctantly/, home: /retire to my parlour/, sit: /tips his hat down over his eyes/, stand: /Onwards, then/,
  ways: ['Cane', 'Bloblings', "A Gentleman's Duel", 'Noblesse Oblige'], plain: 'His red-banded topper', looks: ['Emerald Topper', 'Royal Topper', 'Crimson Topper'], lookPart: 'hat',
  crowd: ['BLOBLINGS', 'weakness'], charge: ["A GENTLEMAN'S DUEL", 'weakness'], kind: ['NOBLESSE OBLIGE', 'resistance', 'absorption'] });
