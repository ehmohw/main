// 2.94: 8-BIT LEO (phase213), a hidden follower, as a regular (non-op) player - the owner's checklist (rigpet_t): met through a GLITCHED
// CARTRIDGE used beside your own Leo; then his retro ways - SWORD BEAM (only at full health: a projectile), SLASH (everything within
// 3), SHIELD BLOCK (you hurt: Resistance II, the foes shoved back), COIN BLOCK (no fight near: experience and Luck), SPIN ATTACK (three
// foes: every one hurt); the palettes; the shared list.
const runT = require('./rigpet_t');
runT({ W: 'pxleo', NAME: '8-Bit Leo', ab: 'xl', q: 'xo', pfx: 'p213l', prefix: 'xl_', item: 'cart_leo', parts: 2, hp: 50, X: 17520, Z: 16000, pron: 'him',
  lookPart: 'head', sprite: true,
  called: /Hyaah/, home: /Saving your game/, sit: /save point/, stand: /Back to the quest/,
  ways: ['Sword Beam', 'Slash', 'Shield Block', 'Coin Block', 'Spin Attack'], plain: 'Sixteen colours', looks: ['Game Boy', 'Virtual Boy', 'Sepia Print'],
  encounter: require('./px_enc')('leo', 'leo_crest', 'bm.xlmet', 'cart_leo'),
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, sleep }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.xo${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'mc', 'rc', 'k', 'k2']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    await calm(); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(300);
    await zom(9, 0, 'bm.trpb'); await cd('rc', 0);
    ok('SWORD BEAM - at full health, a foe 9 off: hit by the beam', await wait(6000, async () => (await hp('bm.trpb')) < 300), `hp ${await hp('bm.trpb')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(2.5, 0, 'bm.trps'); await cd('mc', 0);
    ok('SLASH - a foe beside him: slashed', await wait(5000, async () => (await hp('bm.trps')) < 300));
    await calm(); await run('effect clear TestRat'); await run('damage TestRat 8 minecraft:generic'); A.bars.length = 0; await cd('k', 0);
    ok('SHIELD BLOCK - you hurt, a foe near: Resistance II behind his shield', await wait(5000, async () => /resistance/.test(await fx())) && A.bars.some(b => /shield/.test(b)), A.bars.slice(-1).join(''));
    await run(`${O}kill @e[tag=bm.trpz]`); await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect clear TestRat');
    await run('effect give TestRat minecraft:resistance 900 4 true'); await calm(); await sleep(500);
    A.bars.length = 0; await cd('k2', 0);
    ok('COIN BLOCK - no fight near: a ? block (Luck)', await wait(6000, async () => /luck/.test(await fx())) && A.bars.some(b => /\? block/.test(b)), A.bars.slice(-1).join(''));
    await calm();
    for (const [dx, dz] of [[3, 2], [3, -2], [-2, 3]]) await zom(dx, dz, 'bm.trpl');
    await cd('gc', 0);
    ok('SPIN ATTACK - three foes near: every one hurt', await wait(6000, async () => (await cnt('@e[tag=bm.trpl,nbt={Health:300.0f}]')) === 0), `untouched ${await cnt('@e[tag=bm.trpl,nbt={Health:300.0f}]')}`);
    await sleep(1500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
  } });
