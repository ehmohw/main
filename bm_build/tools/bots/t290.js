// 2.95d: KETTLE, the first Buddy, as a regular (non-op) player - the owner's checklist (rigpet_t): on a sunny day in a meadow a
// stick figure comes skipping by (rcon: the sun, the grass, and the roll come up - he steps in as he would); asked empty-handed he
// wants paper; given a sheet he folds it into a plane and joins (Kettle's Paper Plane). His play: TAG ("you're it": slowed,
// weakened), PAPER PLANES, KICKBALL (and the bounce on to the next foe), CARTWHEEL, JUMP ROPE (three foes tripped), RECESS! (foes
// tossed up; Speed and Jump Boost for you), LET'S PLAY! (out of a fight: tagged - Speed and Jump Boost); SKETCH & PLAY with Mr.
// Capshun (called with his own pencil): a toy sketched over a foe, and Kettle plays with it. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'kettle', NAME: 'Kettle', ab: 'kt', q: 'kq', pfx: 'p227', prefix: 'kt_', item: 'kettle_plane', parts: 11, figParts: 10, hp: 40, X: 17200, Z: 16000, pron: 'him',
  called: /Wait for me|What are we playing/, home: /Same time tomorrow/, sit: /Look at the clouds/, stand: /I'm rested/,
  ways: ["Let's Play!", 'Tag', 'Paper Planes', 'Kickball', 'Cartwheel', 'Jump Rope', 'Recess!', 'Sketch & Play'],
  plain: 'Plain pencil', looks: ['Red Crayon', 'Blue Crayon', 'Green Crayon'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep }) => {
    // (the stage: a grass field at noon, clear skies - and the roll come up; he skips in as he would)
    await run('time set noon'); await run('weather clear');
    await run(`${O}fill ${X - 8} ${Y} ${Z - 2} ${X + 8} ${Y} ${Z + 12} minecraft:grass_block`);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^6 run function bm:p227/enc/place`);
    ok('on a sunny meadow: a stick figure comes skipping by, bouncing a ball (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.ktencp]')) >= 10 && A.chats.some(c => /comes skipping across the grass/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: he asks for a sheet of paper', A.bars.some(b => /any paper/.test(b)), A.bars.slice(-1).join(''));
    await run('item replace entity TestRat hotbar.8 with minecraft:paper'); await sleep(600);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding paper: the paper taken, folded into his paper plane - given', (await has('kettle_plane')) === 1 && !/Found [1-9]/.test(await run('clear TestRat minecraft:paper 0')) &&
       A.chats.some(c => /perfect paper plane/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}fill ${X - 8} ${Y} ${Z - 2} ${X + 8} ${Y} ${Z + 12} minecraft:stone`);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.kq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    await calm();
    await zom(2.5, 0, 'bm.trpt'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpt] ~1.5 ~ ~`); await cd('mc', 0);
    ok('TAG - a poke: the foe hurt, and "it" (slowed, weakened)', await wait(5000, async () => (await hp('bm.trpt')) < 300 && /slowness/.test(await fxOf('bm.trpt')) && /weakness/.test(await fxOf('bm.trpt'))));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(9, 0, 'bm.trpp'); await cd('rc', 0);
    ok('PAPER PLANES - a foe 9 off: his planes hit it', await wait(7000, async () => (await hp('bm.trpp')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(7, 0, 'bm.trpk'); await zom(9, 2, 'bm.trpb'); await cd('bc', 0);
    ok('KICKBALL - a foe 7 off: the ball hits it - and bounces on to the next foe near it', await wait(7000, async () => (await hp('bm.trpk')) < 300 && (await hp('bm.trpb')) < 300),
       `first ${await hp('bm.trpk')}, next ${await hp('bm.trpb')}`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(6, 0, 'bm.trpc'); await cd('sc', 0);
    ok('CARTWHEEL - a foe 6 off: he cartwheels into it', await wait(6000, async () => (await hp('bm.trpc')) < 300));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    for (const [dx, dz] of [[2, 1], [2, -1], [-2, 1]]) await zom(dx, dz, 'bm.trpr');
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~2 ~ ~1`); await cd('k2', 0);
    ok('JUMP ROPE - three foes near: tripped up as the rope comes round (Slowness III)', await wait(6000, async () => (await cnt('@e[tag=bm.trpr,nbt={active_effects:[{id:"minecraft:slowness",amplifier:2b}]}]')) >= 2),
       `${await cnt('@e[tag=bm.trpr,nbt={active_effects:[{id:"minecraft:slowness"}]}]')} slowed`);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await sleep(300);
    await zom(5, 0, 'bm.trpg'); await zom(-4, 3, 'bm.trpg'); await cd('gc', 0); A.bars.length = 0;
    ok('RECESS! - every foe near tossed into the air and hurt; Speed and Jump Boost for you', await wait(8000, async () => (await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')) === 0) &&
       /speed/.test(await fx()) && /jump_boost/.test(await fx()), `untouched ${await cnt('@e[tag=bm.trpg,nbt={Health:300.0f}]')}; ${A.bars.slice(-1).join('')}`);
    await sleep(2500); await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    // ---- LET'S PLAY!: out of a fight, beside you - he tags you
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); A.bars.length = 0; await cd('k', 0);
    ok("LET'S PLAY! - out of a fight he tags you: Speed and Jump Boost", await wait(6000, async () => /speed/.test(await fx()) && /jump_boost/.test(await fx())) &&
       A.bars.some(b => /You're it/.test(b)), A.bars.slice(-1).join(''));
    // ---- SKETCH & PLAY: Mr. Capshun called with his own pencil; a foe near - a toy sketched over it, and Kettle plays with it
    await run('tag TestRat add bm.mzmet'); await run('scoreboard players set TestRat bm.mzcd 0');
    await run('loot replace entity TestRat hotbar.6 loot bm:items/capshun_pencil'); await use(6);
    const CAP = '@e[type=minecraft:wolf,tag=bm.mzpet,limit=1]';
    if (ok('Mr. Capshun called with his pencil', await wait(6000, async () => (await cnt(CAP)) === 1))) {
      await run(`scoreboard players set ${CAP} bm.zqk2 900`); for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k']) await run(`scoreboard players set ${CAP} bm.zq${o} 900`);
      await calm(); await run(`${O}tp ${CAP} ${X - 1} ${Y + 1} ${Z}`); await run(`${O}tp ${PET} ${X + 1} ${Y + 1} ${Z}`);
      await zom(0, 8, 'bm.trpy'); await run(`scoreboard players set ${PET} bm.ktty 0`);
      let toy = false;
      const played = await wait(8000, async () => { if ((await cnt('@e[type=minecraft:item_display,tag=bm.kttoy]')) >= 1) toy = true; return (await hp('bm.trpy')) < 300; }, 100);
      ok('SKETCH & PLAY - Capshun sketches a toy over the foe, and Kettle plays with it (it\'s hurt)', toy && played, `toy ${toy}, foe ${await hp('bm.trpy')}`);
      await run(`${O}kill @e[tag=bm.trpz]`); await use(6, true); await sleep(800); await A.press(/Send him home/); await sleep(1500);
      await run('clear TestRat *[minecraft:custom_data~{bm:"capshun_pencil"}]');
    }
    await calm();
  } });
