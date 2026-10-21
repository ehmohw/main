// 2.87: BLOO, as a regular (non-op) player - the owner's checklist (rigpet_t): HARD MODE ONLY - a sapling planted in a forest at
// night: the beast of the woods steps out; asked, he wants something worth eating; given raw salmon, he joins (his claw). His fight:
// the CLAW RAKE (it bleeds; Frenzy builds), the POUNCE, the FERAL ROAR (cowering foes, Strength for you), the WILD HUNT. Then the
// shared list.
const runT = require('./rigpet_t');
runT({ W: 'bloo', NAME: 'Bloo', ab: 'bo', q: 'bk', pfx: 'p191', prefix: 'bo_', item: 'bo_claw', parts: 11, hp: 70, X: 16660, Z: 16000, pron: 'him',
  called: /^.*What\./, home: /quieter without you/, sit: /Don't touch me/, stand: /Fine\. Moving/, story: /His story/,
  ways: ['Claw Rake', 'Pounce', 'Feral Roar', 'The Wild Hunt', 'Woodland Guardian'],
  plain: 'His own wild blue', looks: ['Shadow Pelt', 'Ember Mane', 'Frost Coat'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    await run(`${O}fillbiome ${X - 16} ${Y - 4} ${Z - 16} ${X + 16} ${Y + 12} ${Z + 16} minecraft:forest`);
    await run(`${O}time set 18000`); await run(`${O}setblock ${X} ${Y} ${Z + 3} minecraft:grass_block`);
    await run('item replace entity TestRat hotbar.1 with minecraft:oak_sapling 4');
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 50); A.chats.length = 0; A.slot(1); await sleep(300); A.useOn(X, Y, Z + 3, 1); await sleep(500);
    ok('a sapling planted in a forest at night: the beast of the woods steps out (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.boencp]')) === 11 && A.chats.some(c => /Something huge and blue/.test(c)), A.chats.slice(-1).join(''));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: "Go away... unless you brought something worth eating"', A.bars.some(b => /worth eating/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:salmon'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding raw salmon: the fish taken, his claw given', (await has('bo_claw')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:salmon 0')) &&
       A.chats.some(c => /not like the others/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.bk${o} ${v}`);
    for (const o of ['gc', 'bc', 'rc', 'mc']) await cd(o, 900);
    await zom(3, 0, 'bm.trpr'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~1.5 ~ ~`); await cd('mc', 0);
    ok('the CLAW RAKE - the foe hurt, and it bleeds (Wither)', await wait(5000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300) &&
       /wither/.test(await nbt('@e[tag=bm.trpr,limit=1]', 'active_effects')));
    ok('...FRENZY builds', await wait(4000, async () => (await score('bm.bkk', PET)) >= 1), `frenzy ${await score('bm.bkk', PET)}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('mc', 900);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(10, 0, 'bm.trpp'); await cd('rc', 0);
    ok('the POUNCE - a foe 10 off: he lands on it (slowed)', await wait(6000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.bopet,x=${X + 10},y=${Y + 1},z=${Z},distance=..3]`)) === 1) &&
       /slowness/.test(await nbt('@e[tag=bm.trpp,limit=1]', 'active_effects')));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await zom(3, 2, 'bm.trpb'); await zom(3, -2, 'bm.trpb'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpb] ~3 ~ ~1`); await cd('bc', 0);
    ok('the FERAL ROAR - two foes near: they cower (Weakness II)', await wait(6000, async () => (await cnt('@e[tag=bm.trpb,nbt={active_effects:[{id:"minecraft:weakness",amplifier:1b}]}]')) >= 1));
    ok('...Strength for you', /strength/.test(await fx()));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900); await zom(5, 0, 'bm.trph'); await cd('gc', 0); A.bars.length = 0;
    ok('the WILD HUNT', await wait(8000, async () => A.bars.some(b => /HUNT IS ON/.test(b))), A.bars.slice(-1).join(''));
    await sleep(3000); await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
  } });
