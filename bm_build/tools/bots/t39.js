// v2.36 fixes: trades stay open (no re-teleport), nameplates follow, Cecil's spawn on a step, admin/blood_moon
const { bot, rcon, sleep } = require('./lib');
const X = -27000, Y = 100, Z = 15000;               // (2.81: 384 blocks from the nearest natural market)
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 600 4 true');
  await run(`forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} grass_block`); await run(`fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 6} ${Z + 20} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await sleep(500);
  // ---- Cecil in front of a step: not inside it
  await run(`setblock ${X} ${Y + 1} ${Z + 1} grass_block`); await run(`setblock ${X} ${Y + 1} ${Z + 2} grass_block`);
  await run('scoreboard players reset TestRat bm.cpcd'); await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1200);
  const cp = await pos('@e[type=wolf,tag=bm.cecilpet,limit=1]');
  ok('Cecil, summoned facing a step, stands ON it (not inside)', cp && cp[1] >= Y + 2 - 0.01, cp && cp.map(v => v.toFixed(2)).join(' '));
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run(`fill ${X} ${Y + 1} ${Z + 1} ${X} ${Y + 1} ${Z + 2} air`); await sleep(1500);
  await run('scoreboard players reset TestRat bm.cpcd'); await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1200);
  const cp2 = await pos('@e[type=wolf,tag=bm.cecilpet,limit=1]');
  ok('...and on flat ground, 1.2 blocks ahead at your level', cp2 && Math.abs(cp2[1] - Y - 1) < 0.01 && Math.abs(cp2[2] - Z - 1.7) < 0.05, cp2 && cp2.map(v => v.toFixed(2)).join(' '));
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(1500);
  // ---- nameplates follow: a trader moved 3 blocks gets its plate back
  await run(`execute positioned ${X + 6.5} ${Y + 1} ${Z + 6.5} rotated 180 0 run function bm:npc/chef`); await run(`execute positioned ${X + 8.5} ${Y + 1} ${Z + 6.5} rotated 180 0 run function bm:npc/professor`); await sleep(2500);
  ok('traders get their nameplates', (await cnt(`@e[type=text_display,tag=bm.plate,x=${X + 7},y=${Y + 1},z=${Z + 6},distance=..4]`)) === 2);
  await run(`tp @e[tag=bm.npc_chef,x=${X + 6.5},y=${Y + 1},z=${Z + 6.5},distance=..1] ${X + 6.5} ${Y + 1} ${Z + 3.5}`); await sleep(2500);
  const near = async (nx, nz) => cnt(`@e[type=text_display,tag=bm.plate,x=${nx},y=${Y + 1},z=${nz},distance=..0.7]`);
  ok('...a moved trader\'s plate follows it; the neighbour keeps its own', (await near(X + 6.5, Z + 3.5)) === 1 && (await near(X + 8.5, Z + 6.5)) === 1 && (await near(X + 6.5, Z + 6.5)) === 0 &&
     (await cnt(`@e[type=text_display,tag=bm.plate,x=${X + 7},y=${Y + 1},z=${Z + 5},distance=..6]`)) === 2);
  await sleep(3000); ok('...and it stays settled (no plate swapping)', (await near(X + 6.5, Z + 3.5)) === 1 && (await near(X + 8.5, Z + 6.5)) === 1);
  // ---- a trade stays open (nothing re-teleports the trader)
  await run(`tp TestRat ${X + 8.5} ${Y + 1} ${Z + 4.5} 0 0`); await sleep(1500);
  const id = Object.values(A.ents).filter(e => Math.abs(e.x - X - 8.5) < 0.3 && Math.abs(e.z - Z - 6.5) < 0.3 && Math.abs(e.y - Y - 1) < 0.3).map(e => e.entityId);
  let closed = 0; A.on('close_window', () => closed++); const w0 = A.windows.length;
  for (const i of id) A.interact(i); await sleep(1000);
  const opened = A.windows.length > w0; await sleep(12000);
  ok('a trade screen stays open for 12 s', opened && closed === 0, `opened ${opened}, closed by server ${closed}`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  // ---- admin/blood_moon by day
  await run('scoreboard players set #active bm.bm 0'); await run('time set day'); await sleep(1500);
  await run('execute as TestRat at @s run function bm:admin/blood_moon'); await sleep(2500);
  const act = await run('scoreboard players get #active bm.bm'), tod = await run('scoreboard players get #tod bm.bm');
  ok('admin/blood_moon (by day): night falls and the Blood Moon rises', act.includes('has 1 '), `${act} / ${tod}`);
  await sleep(3000); ok('...and stays up', (await run('scoreboard players get #active bm.bm')).includes('has 1 '));
  // and bloodmoon/start by hand
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day'); await sleep(1500);
  await run('function bm:bloodmoon/start'); await sleep(3000);
  ok('bloodmoon/start by hand sticks too', (await run('scoreboard players get #active bm.bm')).includes('has 1 '));
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day');
  await run(`forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
