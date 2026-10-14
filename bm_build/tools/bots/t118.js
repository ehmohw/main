// 2.73: a raid boss's minions fall with it
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, qs, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');

  // ================================================================== THE VAULT'S GUARDIAN
  await heist('levers', 'a', 2); await begin();
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
  const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
  await run(`execute in bm:gutter as ${V} at @s run tp TestRat ${rel(10, 4, 12)} -90 0`); await sleep(3000);
  ok('Walk into the vault: the guardian wakes', (await cnt(B)) === 1);
  await run(`scoreboard players set #gi bm.rng ${GI}`);
  await run(`execute in bm:gutter as ${B} at @s run function bm:p70/boss/call`); await sleep(300);
  await run(`execute in bm:gutter as ${B} at @s run summon minecraft:vex ~ ~2 ~ {Tags:["bm.t118"]}`);
  const q1 = (await qs('levers'))[0];
  await at('levers', q1, 'function bm:p70/ctx'); await run(`scoreboard players set #gi bm.rng ${GI}`);
  await at('levers', q1, 'function bm:p70/guard'); await sleep(500);
  const near = () => cnt(`@e[tag=bm.gvg,tag=!bm.gvboss,scores={bm.gvi=${GI}},distance=..48]`.replace('@e[', `@e[`));
  const nearV = async () => +(((await run(`execute in bm:gutter as ${V} at @s store result score #t bm.rng if entity @e[tag=bm.gvg,tag=!bm.gvboss,scores={bm.gvi=${GI}},distance=..48]`)).match(/(\d+)/) || [0, 0])[1]);
  const farG = async () => +(((await run(`execute in bm:gutter as ${room('levers', q1)} at @s store result score #t bm.rng if entity @e[tag=bm.gvg,scores={bm.gvi=${GI}},distance=..14]`)).match(/(\d+)/) || [0, 0])[1]);
  const n0 = await nearV(), f0 = await farG(), v0 = await cnt('@e[type=minecraft:vex,tag=bm.t118]');
  ok(`The guardian calls its guards (${n0} at its side, plus a vex); a guard stands in room ${q1}, far off`, n0 >= 2 && v0 === 1 && f0 >= 1);
  await sleep(1500);
  A.chats.length = 0;
  await run(`execute in bm:gutter as ${B} run data modify entity @s DeathLootTable set value "minecraft:empty"`);
  await run(`execute in bm:gutter run kill ${B}`); await sleep(2200);
  const items = +(((await run(`execute in bm:gutter as ${V} at @s store result score #t bm.rng if entity @e[type=minecraft:item,distance=..40]`)).match(/(\d+)/) || [0, 0])[1]);
  ok('The guardian falls: every guard at its side falls with it (dropping nothing), and the vex too', (await nearV()) === 0 && (await cnt('@e[type=minecraft:vex,tag=bm.t118]')) === 0 && items === 0, `items ${items}`);
  ok('...the crew is told', A.chats.some(c => /master has fallen/.test(c)));
  ok('...a guard elsewhere in the heist is left alone', (await farG()) === f0);
  ok('...and the vault opens as before', (await num(`execute in bm:gutter run scoreboard players get ${V} bm.gvs`)) === 2);

  // ================================================================== THE GUTTER GENTRY: the Count's Bloblings
  await heist('levers', 'a', 3); await begin();
  const q = (await qs('levers'))[0];
  await at('levers', q, `tp TestRat ${rel(12, 4, 12)}`); await sleep(500);
  await run('execute in bm:gutter run kill @e[tag=bm.gnt]'); await run('execute in bm:gutter run kill @e[type=minecraft:slime,tag=bm.gntl]'); await sleep(2500);
  const g0 = await cnt('@e[tag=bm.gnt]');
  await run('execute as TestRat at TestRat run function bm:admin/gentry_here'); await sleep(2500);
  const g1 = await cnt('@e[tag=bm.gnt]');
  ok('The Gutter Gentry: all three in the parlour', (await cnt('@e[tag=bm.gnt_bat]')) >= 1 && (await cnt('@e[tag=bm.gnt_egg]')) >= 1 && (await cnt('@e[tag=bm.gnt_blob]')) >= 1, `${g0} -> ${g1}`);
  await run('execute in bm:gutter as @e[tag=bm.gnt_blob,limit=1] at @s run function bm:p88/blob/call'); await sleep(500);
  await run('execute in bm:gutter as @e[tag=bm.gnt_blob,limit=1] at @s run function bm:p88/blob/call'); await sleep(500);
  const bl0 = await cnt('@e[type=minecraft:slime,tag=bm.gntl]');
  ok(`The Count tips his hat: ${bl0} Bloblings`, bl0 >= 2);
  await run('execute in bm:gutter run kill @e[tag=bm.gnt_blob]'); await sleep(2500);
  ok('The Count falls: his Bloblings pop with him (Batty and Eggbert fight on)', (await cnt('@e[type=minecraft:slime,tag=bm.gntl]')) === 0 && (await cnt('@e[tag=bm.gnt_blob]')) === 0 && (await cnt('@e[tag=bm.gnt_bat]')) >= 1 && (await cnt('@e[tag=bm.gnt_egg]')) >= 1, `bloblings ${await cnt('@e[type=minecraft:slime,tag=bm.gntl]')}`);
  await run('execute in bm:gutter run kill @e[tag=bm.gnt]'); await sleep(2500);

  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
