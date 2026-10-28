// 2.97: HENRY, the owner's black cat, as a regular (non-op) player - the owner's checklist (rigpet_t). In a village at night
// (rcon: the night, a villager, and the roll come up) a black cat with a red collar sits watching; right-clicked empty-handed he
// sniffs your hand; given a cod he eats it and leaves his tag (Henry's Collar Tag). His ways: SWIPE, POUNCE (a leap onto a foe 6
// off), HISS (two foes close: slowed and weakened), BLACK CAT'S LUCK (three swipes; Luck II for you), PURR (out of a fight:
// Regeneration and Absorption), NIGHT PROWLER (by night, Night Vision beside him). Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'henry', NAME: 'Henry', ab: 'hy', q: 'hq', pfx: 'p229', prefix: 'hy_', item: 'henry_tag', parts: 7, figParts: 7, hp: 30, X: 17400, Z: 16000, pron: 'him',
  called: /headbutts your leg|out of nowhere/, home: /saunters off home/, sit: /folds himself into a loaf/, stand: /stretches front and back/,
  ways: ['Swipe', 'Pounce', 'Hiss', "Black Cat's Luck", 'Purr', 'Night Prowler'],
  plain: 'His red collar', looks: ['Navy Collar', 'Emerald Collar', 'Gold Collar'], lookPart: 'body',
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    await run('time set midnight'); await run('weather clear');
    await run(`${O}summon minecraft:villager ${X + 6} ${Y + 1} ${Z + 6} {NoAI:1b,Tags:["bm.t294v","bm.seen"],PersistenceRequired:1b}`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^5 run function bm:p229/enc/place`);
    // (the chat line can land a moment after the cat; and the night's own roll may have set one down too - only ours is counted)
    ok('in a village at night: a black cat with a red collar, watching (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) >= 1 &&
       A.chats.some(c => /black cat with a red collar/.test(c))), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 1.8, 0, 25);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: he sniffs your hand, unimpressed', A.bars.some(b => /sniffs your empty hand/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:cod'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding a cod: the fish eaten, his tag left for you', (await has('henry_tag')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:cod 0')) &&
       A.chats.some(c => /HENRY, it says/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}kill @e[tag=bm.t294v]`);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, X, Y, Z, sleep, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.hq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
    await run(`${O}time set noon`); await calm();
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await cd('mc', 0);
    ok('SWIPE - a foe beside him: clawed', await wait(5000, async () => (await hp('bm.trps')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(6, 0, 'bm.trpp'); await cd('rc', 0);
    ok('POUNCE - a foe 6 off: he leaps onto it', await wait(6000, async () => (await hp('bm.trpp')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    for (const [dx, dz] of [[1.5, 1], [1.5, -1]]) await zom(dx, dz, 'bm.trph');
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trph] ~1.5 ~ ~1`); await cd('k2', 0);
    ok('HISS - two foes close: slowed and weakened', await wait(6000, async () => /weakness/.test(await fxOf('bm.trph'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(2, 0, 'bm.trpc'); await cd('gc', 0);
    ok("BLACK CAT'S LUCK - swipes, and Luck II for you", await wait(8000, async () => (await hp('bm.trpc')) < 290 && /luck/.test(await fx())));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(3000);   // (the charged flurry plays out first)
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await cd('k', 0);
    ok('PURR - out of a fight beside you: Regeneration and Absorption', await wait(7000, async () => /regeneration/.test(await fx()) && /absorption/.test(await fx())));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run(`${O}time set midnight`);
    ok('NIGHT PROWLER - by night, Night Vision beside him', await wait(4000, async () => /night_vision/.test(await fx())));
    await run(`${O}time set noon`); await calm();
  } });
