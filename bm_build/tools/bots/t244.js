// 2.88: BENDER, the goodest boy, as a regular (non-op) player - the owner's checklist (rigpet_t): round a village he trots out
// from between the houses; asked empty-handed, he wants a bone; given one, he joins (his ball). His fight: BITE, TACKLE, GUARD BARK,
// GOOD BOY!; then his menu: DIG! (something comes up out of the dirt; again - "Dig again in...") and SNIFF OUT TREASURE. Then the
// shared list.
const runT = require('./rigpet_t');
runT({ W: 'bender', NAME: 'Bender', ab: 'bv', q: 'dq', pfx: 'p195', prefix: 'bd_', item: 'bv_ball', parts: 7, hp: 50, X: 17060, Z: 16000, pron: 'him',
  called: /skidding round the corner|a bark from far off/, home: /trots off home/, sit: /Very good sit/, stand: /springs up/,
  ways: ['Dig!', 'Sniff out Treasure', 'Bite', 'Tackle', 'Guard Bark', 'Good Boy!', 'Happy to See You'],
  plain: 'His own fawn', looks: ['Midnight Black', 'Snow White', 'Sable'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    // (the stage: a village - three villagers - and the roll come up; he trots out as he would)
    for (const dx of [-6, 0, 6]) await run(`${O}summon minecraft:villager ${X + dx} ${Y + 1} ${Z + 8} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.trpz","bm.seen"]}`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s run function bm:p195/enc/trot`);
    ok('round a village: a dog trots out from between the houses (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.bvencp]')) === 7 && A.chats.some(c => /trots out from between the houses/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: he sniffs your hand for a bone', A.bars.some(b => /A bone, maybe/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:bone'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding a bone: the bone taken, his ball given', (await has('bv_ball')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:bone 0')) &&
       A.chats.some(c => /He has decided/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.trpz]`);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.dq${o} ${v}`);
    for (const o of ['gc', 'bc', 'rc', 'mc']) await cd(o, 900);
    await run(`scoreboard players set ${PET} bm.bvrg 9000`);          // (2.93b: his Rage held back - t255 plays it)
    await zom(2.5, 0, 'bm.trpr'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~1.5 ~ ~`); await cd('mc', 0);
    ok('BITE - the foe hurt', await wait(5000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('mc', 900);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(8, 0, 'bm.trpt'); await cd('rc', 0);
    ok('TACKLE - a foe 8 off: he bounds in and bowls it over (hurt, slowed)', await wait(6000, async () => (await num('@e[tag=bm.trpt,limit=1]', 'Health')) < 300 &&
       /slowness/.test(await nbt('@e[tag=bm.trpt,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run('effect clear TestRat minecraft:resistance');
    await zom(3, 2, 'bm.trpb'); await zom(3, -2, 'bm.trpb'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpb] ~4 ~ ~1`); await cd('bc', 0);
    ok('GUARD BARK - two foes near: they falter (weakened, slowed, lit up)', await wait(6000, async () => (await cnt('@e[tag=bm.trpb,nbt={active_effects:[{id:"minecraft:weakness"}]}]')) >= 1));
    ok('...Resistance for you', await wait(2000, async () => /resistance/.test(await fx())));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await zom(5, 0, 'bm.trpg'); await zom(-4, 3, 'bm.trpg'); await cd('gc', 0);
    ok('GOOD BOY! - he darts from foe to foe (both bitten), Regeneration II for you', await wait(8000, async () => (await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')) === 0) &&
       /regeneration/.test(await fx()), `untouched ${await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')}`);
    await sleep(3000); await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    // ---- DIG! from his menu, on dirt
    await run(`${O}fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} minecraft:dirt`);
    await run('scoreboard players set TestRat bm.bvdg 0'); await run('scoreboard players set TestRat bm.bvsn 0');
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`);
    await sneakMenu(0); A.bars.length = 0; await A.press(/^Dig!/); await sleep(500);
    ok('his menu -> Dig!: he digs (state 13)', A.bars.some(b => /and DIGS/.test(b)) && (await score('bm.dqa', PET)) === 13, A.bars.slice(-1).join(''));
    ok('...and something comes up out of the dirt', await wait(5000, async () => (await cnt(`@e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..6]`)) >= 1));
    ok('...five minutes before the next dig', (await score('bm.bvdg')) > 280, `bm.bvdg ${await score('bm.bvdg')}`);
    await sleep(2500); await sneakMenu(0); A.bars.length = 0; await A.press(/^Dig!/); await sleep(600);
    ok('...pressed again: "Dig again in 4m ..s"', A.bars.some(b => /Dig again in/.test(b)), A.bars.slice(-1).join(''));
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`);
    // ---- SNIFF OUT TREASURE
    await sleep(2500); await sneakMenu(0); A.bars.length = 0; A.chats.length = 0; await A.press(/Sniff out treasure/); await sleep(500);
    ok('his menu -> Sniff out treasure: nose down (state 9)', A.bars.some(b => /he's got something/.test(b)) && (await score('bm.dqa', PET)) === 9, A.bars.slice(-1).join(''));
    ok('...he finds the scent and says which way (or that there is nothing near)', await wait(5000, async () =>
      A.chats.some(c => /points his nose .* about \d+ blocks/.test(c)) || A.bars.some(b => /RIGHT HERE|Nothing worth digging/.test(b))),
       (A.chats.slice(-1).join('') + ' / ' + A.bars.slice(-1).join('')).slice(0, 200));
    await run(`${O}fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} minecraft:sandstone`);
  } });
