// 2.97: NIA, the owner's tortoiseshell (in loving memory), as a regular (non-op) player - the owner's checklist (rigpet_t). Henry
// called with his tag; on a clear night under the open sky (rcon: the night, the clear sky, and the roll come up) a bell rings in the
// grass and Henry runs to her - she was always waiting for him; stroked (right-click), she stays, and leaves her bell (Nia's
// Bell) - "In loving memory of Nia". Her ways (2.96c: a gentle support follower - she almost never scratches): COMFORT (you hurt,
// in a fight: Regeneration), GUARDIAN CURL (you at a third of your health: Resistance II, Absorption), BELL CHIME (Regeneration II
// for you; the monsters round her glow - unhurt), SHOO (two foes close: pushed back and slowed, unhurt), GENTLE PAWS (a monster
// beside her that hasn't hurt her isn't scratched), KNEAD (out of a fight: Regeneration and a bite), STARLIGHT. Her special pairs: with Emma, every 30 s she
// curls up in Emma's lap - petals heal you all (Absorption II); with Queen Ava, a glowing tide (Water Breathing). Then the list.
const runT = require('./rigpet_t');
runT({ W: 'nia', NAME: 'Nia', ab: 'ni', q: 'nq', pfx: 'p230', prefix: 'ni_', item: 'nia_bell', parts: 7, figParts: 7, hp: 30, X: 17500, Z: 16000, pron: 'her',
  called: /winds round your legs|a bell jingles/, home: /pads off under the stars/, sit: /tucks her paws in/, stand: /uncurls, stretches/,
  ways: ['Comfort', 'Guardian Curl', 'Bell Chime', 'Shoo', 'Gentle Paws', 'Knead', 'Starlight'],
  plain: 'Her lilac collar', looks: ['Rose Collar', 'Sky Collar', 'Mint Collar'], lookPart: 'body',
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, X, Y, Z, ENC, sleep, use }) => {
    await run('tag TestRat add bm.hymet'); await run('scoreboard players set TestRat bm.hycd 0');
    await run('time set midnight'); await run('weather clear');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/henry_tag'); await use(7); await sleep(1500);
    const HY = '@e[type=minecraft:wolf,tag=bm.hypet,limit=1]';
    ok('Henry called with his tag', await wait(4000, async () => (await cnt(HY)) === 1));
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^5 run function bm:p230/enc/place`);
    ok('a clear night, Henry beside you: a bell in the grass - and there she is, waiting for him', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       A.chats.some(c => /She was always waiting for him/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 1.8, 0, 25);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('stroked: she stays - and her bell is yours ("In loving memory of Nia")', (await has('nia_bell')) === 1 && A.chats.some(c => /In loving memory of Nia/.test(c)),
       A.chats.slice(-2).join(' | ').slice(0, 200));
    await run(`${O}execute as TestRat at @s run function bm:p98/home/henry`); await run('clear TestRat *[minecraft:custom_data~{bm:"henry_tag"}]');
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, X, Y, Z, sleep, at, use }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.nq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'bc', 'sc', 'rc', 'mc', 'k', 'k2']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const fxOf = async (t) => nbt(`@e[tag=${t},limit=1]`, 'active_effects');
    await run(`${O}time set noon`); await calm();
    const hurtMe = async (n) => { await run('effect clear TestRat'); await run(`damage TestRat ${n} minecraft:generic`); };
    const healMe = async () => { await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); };
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await run(`${O}data merge entity @e[tag=bm.trps,limit=1] {NoAI:1b}`); await cd('mc', 0);
    await sleep(3000);
    ok('GENTLE PAWS - a monster beside her that hasn\'t hurt her: not a scratch', (await hp('bm.trps')) >= 300, String(await hp('bm.trps')));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(8, 0, 'bm.trpf'); await run(`${O}data merge entity @e[tag=bm.trpf,limit=1] {NoAI:1b}`);
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await hurtMe(4); await cd('sc', 0);
    ok('COMFORT - you hurt, in a fight: she purrs against you - Regeneration', await wait(6000, async () => /regeneration/.test(await fx())));
    await healMe(); await calm();
    await hurtMe(15); await cd('bc', 0);
    ok('GUARDIAN CURL - you at a third of your health: she curls round your feet - Resistance and Absorption',
       await wait(7000, async () => /resistance/.test(await fx()) && /absorption/.test(await fx())));
    await healMe(); await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(2500);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(3, 0, 'bm.trpc'); await run(`${O}data merge entity @e[tag=bm.trpc,limit=1] {NoAI:1b}`); await cd('gc', 0);
    ok('BELL CHIME - her bell: Regeneration II for you; the monster round her glows - and is not hurt',
       await wait(8000, async () => /regeneration/.test(await fx()) && /glowing/.test(await fxOf('bm.trpc'))) && (await hp('bm.trpc')) >= 300);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(1500);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`);
    for (const [dx, dz] of [[1.5, 1], [1.5, -1]]) await zom(dx, dz, 'bm.trph');
    await run(`${O}execute at ${PET} run tp @e[tag=bm.trph] ~1.5 ~ ~1`); await run(`${O}execute as @e[tag=bm.trph] run data merge entity @s {NoAI:1b}`); await cd('k2', 0);
    ok('SHOO - two foes close: a soft hiss - slowed, and not hurt', await wait(6000, async () => /slowness/.test(await fxOf('bm.trph'))) && (await hp('bm.trph')) >= 300);
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(1500);
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await cd('k', 0);
    ok('KNEAD - out of a fight beside you: Regeneration and a bite to eat', await wait(7000, async () => /regeneration/.test(await fx())));
    // ---- her special pair with Emma: every 30 s she curls up in Emma's lap - petals heal you all
    await run('tag TestRat add bm.emmet'); await run('scoreboard players set TestRat bm.emcd 0'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run('loot replace entity TestRat hotbar.6 loot bm:items/emma_ribbon'); await use(6); await sleep(1500);
    const EM = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]';
    if (ok('Emma called with her ribbon', await wait(4000, async () => (await cnt(EM)) === 1))) {
      await run(`${O}tp ${EM} ${X + 1.5} ${Y + 1} ${Z + 0.5}`); await run(`execute as @e[type=minecraft:wolf,tag=bm.nipet] run scoreboard players set @s bm.p8ni_emma 29`); A.bars.length = 0;
      ok('NIA AND EMMA - every 30 s she curls up in Emma\'s lap: petals heal you (Absorption II)', await wait(6000, async () => /absorption/.test(await fx()) && A.bars.some(b => /fell asleep in my lap/.test(b))),
         A.bars.slice(-1).join(''));
      await run(`${O}execute as TestRat at @s run function bm:p98/home/emma`); await run('clear TestRat *[minecraft:custom_data~{bm:"emma_ribbon"}]');
    }
    await calm();
  } });
