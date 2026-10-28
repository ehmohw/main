// 2.98: EGGBERT of the Gutter Gentry, reformed, as a regular (non-op) player (gentry_t): the second win over the Gentry leaves his
// Calling Token. CLAW, GOO (a foe 4-14 off: a glob of ooze, slowed), OOZE SPILL (charged: the ground goes sticky), YOLK (a bite to eat - over in a moment - and Regeneration).
require('./gentry_t')({ W: 'eggbert', NAME: 'Eggbert', ab: 'eb', q: 'ey', pfx: 'p232e', pre: 'ge_', item: 'gentry_eggbert', n: 2, others: ['gentry_batty', 'gentry_count'],
  parts: 6, figParts: 6, hp: 40, X: 17600, Z: 17600,
  called: /Here, here\. Coming/, home: /Off to my nest/, sit: /settles down like he's being kept warm/, stand: /Up I get/,
  ways: ['Claw', 'Goo', 'Ooze Spill', 'Yolk'], plain: 'His own black ooze', looks: ['Royal Ooze', 'Slime Ooze', 'Magma Ooze'], lookPart: 'body',
  ranged: 'GOO', charge: ['OOZE SPILL', 'slowness'], kind: ['YOLK', 'regeneration'] });
