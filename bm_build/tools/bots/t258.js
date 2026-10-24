// 2.94: 8-BIT EMMA (phase213), a hidden follower, as a regular (non-op) player - the owner's checklist (rigpet_t): met through a GLITCHED
// CARTRIDGE used beside your own Emma; then her retro ways - FIREBALL (a projectile, burning), STOMP (everything within 3, dazed),
// EXTRA LIFE (you low: a 1-UP - Absorption), POWER STAR (three foes: every one hurt; you, Resistance and Speed); her palettes on the
// sprite's every frame; the shared list (sitting: the frame changes as she breathes).
const runT = require('./rigpet_t');
runT({ W: 'pxemma', NAME: '8-Bit Emma', ab: 'xm', q: 'xn', pfx: 'p213e', prefix: 'xm_', item: 'cart_emma', parts: 2, hp: 50, X: 17460, Z: 16000, pron: 'her',
  lookPart: 'head', sprite: true,
  called: /Player Two/, home: /Saving/, sit: /PAUSE/, stand: /Unpaused/,
  ways: ['Fireball', 'Stomp', 'Extra Life', 'Power Star'], plain: 'Sixteen colours', looks: ['Game Boy', 'Virtual Boy', 'Sepia Print'],
  encounter: require('./px_enc')('emma', 'emma_ribbon', 'bm.xmmet', 'cart_emma'),
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, sleep }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.xn${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'sc', 'rc', 'k']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    await calm();
    await zom(8, 0, 'bm.trpb'); await cd('rc', 0);
    ok('FIREBALL - a foe 8 off: hit by the fireball, burning', await wait(6000, async () => (await hp('bm.trpb')) < 300 && (await num('@e[tag=bm.trpb,limit=1]', 'Fire')) > 0), `hp ${await hp('bm.trpb')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(2.5, 0, 'bm.trps'); await cd('sc', 0);
    ok('STOMP - a foe beside her: stomped (hurt, dazed)', await wait(5000, async () => (await hp('bm.trps')) < 300 && /slowness/.test(await nbt('@e[tag=bm.trps,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run('effect clear TestRat'); await run('damage TestRat 14 minecraft:generic'); A.bars.length = 0; await cd('k', 0);
    ok('EXTRA LIFE - you down to 3 hearts: a 1-UP (Absorption)', await wait(5000, async () => /absorption/.test(await fx())) && A.bars.some(b => /1-UP/.test(b)), A.bars.slice(-1).join(''));
    await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await calm();
    for (const [dx, dz] of [[4, 2], [4, -2], [-3, 3]]) await zom(dx, dz, 'bm.trpl');
    await cd('gc', 0);
    ok('POWER STAR - three foes near: every one hurt', await wait(6000, async () => (await cnt('@e[tag=bm.trpl,nbt={Health:300.0f}]')) === 0), `untouched ${await cnt('@e[tag=bm.trpl,nbt={Health:300.0f}]')}`);
    await sleep(1500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
  } });
