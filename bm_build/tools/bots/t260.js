// 2.94: 8-BIT CECIL (phase213), a hidden follower, as a regular (non-op) player - the owner's checklist (rigpet_t): met through a GLITCHED
// CARTRIDGE used beside your own Cecil; then his ways - HEX BOLT (a projectile, withering), HEX (three foes: slowed, weakened, lit
// up), GAME OVER (charged: every foe within 9 hurt); the palettes; the shared list.
const runT = require('./rigpet_t');
runT({ W: 'pxcecil', NAME: '8-Bit Cecil', ab: 'xc', q: 'xd', pfx: 'p213c', prefix: 'xc_', item: 'cart_cecil', parts: 2, hp: 50, X: 17580, Z: 16000, pron: 'him',
  lookPart: 'head', sprite: true,
  called: /Not because you called/, home: /sequel/, sit: /meditate/, stand: /Onward/,
  ways: ['Hex Bolt', 'Hex', 'Game Over'], plain: 'Sixteen colours', looks: ['Game Boy', 'Virtual Boy', 'Sepia Print'],
  encounter: require('./px_enc')('cecil', 'cecil_gem', 'bm.xcmet', 'cart_cecil'),
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, sleep, X, Y, Z }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET.replace(',limit=1', '')} bm.xd${o} ${v}`);   // (2.94c: every 8-Bit Cecil there)
    const calm = async () => { for (const o of ['gc', 'bc', 'rc']) await cd(o, 900); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); };   // (2.94c: back to the middle)
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    await calm();
    await zom(9, 0, 'bm.trpb'); await cd('rc', 0);
    ok('HEX BOLT - a foe 9 off: hit, withering', await wait(6000, async () => (await hp('bm.trpb')) < 300 && /wither/.test(await nbt('@e[tag=bm.trpb,limit=1]', 'active_effects'))), `hp ${await hp('bm.trpb')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    for (const [dx, dz] of [[3, 2], [3, -2], [-3, 2]]) await zom(dx, dz, 'bm.trpl');
    await cd('bc', 0);
    ok('HEX - three foes near: slowed and lit up', await wait(7000, async () => (await cnt('@e[tag=bm.trpl,nbt={active_effects:[{id:"minecraft:glowing"}]}]')) >= 2));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await zom(5, 0, 'bm.trpf'); await zom(-4, 3, 'bm.trpf'); await cd('gc', 0);
    ok('GAME OVER - every foe within 9 hurt', await wait(8000, async () => (await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')) === 0), `untouched ${await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')}`);
    await sleep(1500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
  } });
