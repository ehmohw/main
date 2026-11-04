// 3.0j: STAY HERE (phase260's anchor), as a regular player, with Bender (a rigpet follower) - called with his ball; his menu (sneak +
// use) shows "Stay here" beside "Send him home"; pressed: he's tied to the spot (bm.anc, a leash, a marker), the menu now says "Come
// with me"; we go 130 blocks off (past "couldn't keep up") with Keep up on: after 6 s he's still there, within 7 blocks of the spot;
// a husk set down by him is attacked; we log off and on: still there, still anchored; his ball used (call): he comes to us, free,
// no marker, no lead dropped; anchored again, then "Come with me" from the Settings page: back at our side, free.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 16820, Y = 100, Z = 16120, FAR = 130;
  let A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run('scoreboard players set TestRat bm.bvcd 0');
  for (const x of [X, X + FAR]) {
    await run(`${O}forceload add ${x - 16} ${Z - 16} ${x + 16} ${Z + 16}`);
    await run(`${O}fill ${x - 12} ${Y} ${Z - 12} ${x + 12} ${Y} ${Z + 12} minecraft:grass_block`); await run(`${O}fill ${x - 12} ${Y + 1} ${Z - 12} ${x + 12} ${Y + 6} ${Z + 12} minecraft:air`);
  }
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.bvpet]`); await run(`${O}kill @e[type=minecraft:marker,tag=bm.ancm]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bv_ball'); A.slot(0); await sleep(300);
  const mine = `@e[type=minecraft:wolf,tag=bm.bvpet]`;
  const there = async (extra = '') => /passed/i.test(await run(`${O}execute as ${mine.slice(0, -1)}${extra}] if score @s bm.pid = TestRat bm.pid`));
  const useB = async (sneak = false) => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length; A.slot(0); await sleep(200);
    if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(350); A.release(); A.input({}); await sleep(200);
    if (sneak) await wait(3000, async () => A.dialogN.length > n0, 50); };
  await useB();
  ok('his ball: Bender comes', await wait(6000, async () => there()));
  await useB(true);
  ok('his menu: "Stay here" beside "Send him home"', A.buttons().some(b => /Stay here/.test(b.label)) && A.buttons().some(b => /Send him home/.test(b.label)));
  A.chats.length = 0; await A.press(/Stay here/); await sleep(800);
  const anc = await there(',tag=bm.anc');
  const leash = /leash/.test(await run(`${O}data get entity ${mine.slice(0, -1)},limit=1] leash`)) && !/Found no elements/.test(await run(`${O}data get entity ${mine.slice(0, -1)},limit=1] leash`));
  const marker = /Count: 1/i.test(await run(`${O}execute if entity @e[type=minecraft:marker,tag=bm.ancm]`));
  ok('Stay here: told so, anchored, leashed to a marker, and the menu says "Come with me"', anc && leash && marker && A.chats.some(c => /stays here/.test(c)) && A.buttons().some(b => /Come with me/.test(b.label)),
     `anc ${anc} leash ${leash} marker ${marker}`);
  const near = async () => /passed/i.test(await run(`${O}execute positioned ${X} ${Y + 1} ${Z} as ${mine.slice(0, -1)},distance=..7] if score @s bm.pid = TestRat bm.pid`));
  await run('tag TestRat add bm.pwkeep');
  await run(`${O}tp TestRat ${X + FAR + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(6500);
  ok(`${FAR} blocks off, Keep up on, 6 s: still guarding (within 7 of the spot), anchored`, await near() && await there(',tag=bm.anc'));
  await run(`${O}summon minecraft:husk ${X + 3} ${Y + 1} ${Z} {Tags:["bm.seen","bm.t382"],PersistenceRequired:1b}`);
  const hurt = await wait(10000, async () => { const h = await run(`${O}data get entity @e[type=minecraft:husk,tag=bm.t382,limit=1] Health`); return /Found no|has the following/.test(h) && !/: 20\.0f/.test(h); }, 400);
  ok('a husk by him: attacked (hurt or dead)', hurt);
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t382]`);
  A.end(); await sleep(3000); A = await bot('TestRat'); await sleep(3000); A.stand(); await sleep(3000);
  ok('logged off and on: still there, still anchored', await near() && await there(',tag=bm.anc'));
  await run(`${O}tp TestRat ${X + FAR + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(500);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bv_ball'); A.slot(0); await sleep(300);
  await useB();
  const back = await wait(6000, async () => /passed/i.test(await run(`${O}execute positioned ${X + FAR} ${Y + 1} ${Z} as ${mine.slice(0, -1)},distance=..8] if score @s bm.pid = TestRat bm.pid`)));
  await sleep(1000);
  const lead = /Count: [1-9]/i.test(await run(`${O}execute if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:lead"}}]`));
  const mk = /Count: [1-9]/i.test(await run(`${O}execute if entity @e[type=minecraft:marker,tag=bm.ancm]`));
  ok('his ball used: he comes to us, free - no marker, no lead dropped', back && !(await there(',tag=bm.anc')) && !mk && !lead, `back ${back} marker ${mk} lead ${lead}`);
  await useB(true); await A.press(/Stay here/); await sleep(800);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 40.5}`); await sleep(1500);
  await useB(true); const ps = await A.press(/Settings$/);
  const ce = await A.press(/Come with me/);
  const back2 = await wait(8000, async () => /passed/i.test(await run(`${O}execute positioned ${X} ${Y + 1} ${Z + 40} as ${mine.slice(0, -1)},distance=..8] if score @s bm.pid = TestRat bm.pid`)));
  ok('anchored again, then Settings -> "Come with me": back at our side, free, and the page says "Stay here" again', ps && ce && back2 && !(await there(',tag=bm.anc')) && A.buttons().some(b => /Stay here/.test(b.label)));
  await run('tag TestRat remove bm.pwkeep'); await run('function bm:p195/home'.replace('function', 'execute as TestRat run function'));
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
