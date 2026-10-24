// 2.88: BONES, Emma's shark, as a regular (non-op) player - the owner's checklist (rigpet_t): out on the ocean a fin cuts the water;
// asked empty-handed, he wants fish; given a cod, he joins (his whistle). His fight: BITE, THRASH, TORPEDO, FEEDING FRENZY; Dolphin's
// Grace for you in water near him; then RIDING him from his menu - he floats along where you look, and from his back the whistle is
// CHOMP; sneak to get off. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'bones', NAME: 'Bones', ab: 'bj', q: 'bz', pfx: 'p196', prefix: 'bn_', item: 'bn_whistle', parts: 8, hp: 70, X: 17260, Z: 16000, pron: 'him',
  called: /a whole grinning shark|his bubble wobbles in/, home: /swims off home/, sit: /settles to the bottom of his bubble/, stand: /perks up, all teeth/,
  ways: ['Ride', 'Bite', 'Thrash', 'Torpedo', 'Feeding Frenzy', 'Guardian of the Kingdom'],
  plain: 'His own shark grey', looks: ['Great White', 'Hammerhead Bronze', 'Abyss Black'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    // (the stage: out on the ocean, and the roll come up - a fin beside you)
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s positioned ~ ~ ~4 run function bm:p196/enc/fin`);
    ok('out on the ocean: a fin cuts the water - a grinning grey shark (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.bjencp]')) === 8) && A.chats.some(c => /A fin cuts the water/.test(c)), `enc ${await cnt(ENC.replace(',limit=1', ''))} parts ${await cnt('@e[type=minecraft:item_display,tag=bm.bjencp]')} | ` + A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: he wants to know if your hands have fish in them', A.bars.some(b => /fish in them/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:cod'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding a cod: CHOMP - the fish gone, his whistle given', (await has('bn_whistle')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:cod 0')) &&
       A.chats.some(c => /You have a shark now/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.bz${o} ${v}`);
    for (const o of ['gc', 'bc', 'rc', 'mc']) await cd(o, 900);
    await zom(2.5, 0, 'bm.trpr'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~1.8 ~ ~`); await cd('mc', 0);
    ok('BITE - the foe hurt', await wait(5000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300));
    await cd('mc', 900); await run(`${O}data merge entity @e[tag=bm.trpr,limit=1] {Health:300f}`); await cd('rc', 0);
    ok('THRASH - he shakes it: torn, and slowed', await wait(6000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300 &&
       /slowness/.test(await nbt('@e[tag=bm.trpr,limit=1]', 'active_effects'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z} -90 0`); await zom(8, 0, 'bm.trpt'); await cd('bc', 0);
    ok('TORPEDO - a foe 8 off: he rams through it', await wait(6000, async () => (await num('@e[tag=bm.trpt,limit=1]', 'Health')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`);
    await zom(5, 0, 'bm.trpf'); await zom(-4, 3, 'bm.trpf'); await cd('gc', 0); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    ok('FEEDING FRENZY - foe after foe bitten, and you healed (Regeneration)', await wait(9000, async () => (await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')) === 0) &&
       /regeneration/.test(await fx()), `untouched ${await cnt('@e[tag=bm.trpf,nbt={Health:300.0f}]')}`);
    await sleep(3000); await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    // ---- the Guardian of the Kingdom: in water near him, Dolphin's Grace
    await run(`${O}setblock ${X + 4} ${Y + 1} ${Z + 4} minecraft:water`); await run(`${O}setblock ${X + 4} ${Y + 2} ${Z + 4} minecraft:water`);
    await at(X + 4.5, Y + 1, Z + 4.5, 0, 0); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    ok('in the water near him: Dolphin\'s Grace', await wait(5000, async () => /dolphins_grace/.test(await fx())),
       `me ${await run('data get entity TestRat Pos')} | him ${await run(`data get entity ${PET} Pos`)} ${await run(`data get entity ${PET} Tags`)}`);
    await run(`${O}fill ${X + 4} ${Y + 1} ${Z + 4} ${X + 4} ${Y + 2} ${Z + 4} minecraft:air`);
    // ---- RIDING: from his menu; he floats along where you look; the whistle from his back - CHOMP; sneak - off
    await at(X + 0.5, Y + 1, Z - 7.5, 0, 0); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z - 6.5} 0 0`); await sleep(500);
    await sneakMenu(0); const pr = await A.press(/^Ride/);
    const riding = async () => /bjpet/.test(await run('execute as TestRat on vehicle run tag @s list'));
    ok('his menu -> Ride: on his back', !!pr && await wait(3000, riding));
    A.ride(0, 0, {}); await sleep(600);
    const z0 = await num(PET, 'Pos[2]');
    A.ride(0, 0, { forward: true }); await sleep(1200); A.ride(0, 0, {}); await sleep(400);
    const z1 = await num(PET, 'Pos[2]');
    ok('on land: he floats along where you look (south)', z1 - z0 > 2.0, `z ${z0.toFixed(1)} -> ${z1.toFixed(1)}`);
    ok('...Water Breathing for his rider', /water_breathing/.test(await fx()));
    await sleep(1000);
    const px = await num('TestRat', 'Pos[0]'), pz = await num('TestRat', 'Pos[2]');
    await run(`${O}summon minecraft:husk ${px.toFixed(1)} ${Y + 1} ${(pz + 2.4).toFixed(1)} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.trpz","bm.trpc","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
    A.ride(0, 0, {}); await sleep(500); await use(0); await sleep(800);
    ok('the whistle from his back: CHOMP - the foe ahead bitten', (await num('@e[tag=bm.trpc,limit=1]', 'Health')) < 300, `health ${await num('@e[tag=bm.trpc,limit=1]', 'Health')}`);
    A.ride(0, 0, { shift: true }); await sleep(800); A.ride(0, 0, {}); await sleep(300);
    ok('sneak: off his back', await wait(3000, async () => !(await riding())));
    A.unride(); A.stand(); await sleep(300);          // (on foot again: the riding loop's inputs would swallow every sneak after this)
    await run(`${O}kill @e[tag=bm.trpz]`);
  } });
