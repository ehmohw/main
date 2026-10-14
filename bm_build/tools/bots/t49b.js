// v2.49: Pearlman's trade window stays open while he turns to face you
const { bot, rcon, sleep } = require('./lib');
const X = 11000, Y = 200, Z = 11000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); await sleep(300);
  await run(`execute as TestRat at @s positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} run function bm:p60/pm/spawn`); await sleep(1000);
  const pid = Object.values(A.ents).filter(e => Math.abs(e.x - X - 0.5) < 0.6 && Math.abs(e.z - Z - 3.5) < 0.6).map(e => e.entityId);
  let closed = 0; A.on('close_window', () => closed++);
  const w0 = A.windows.length; for (const id of pid) A.interact(id); await sleep(600);
  const opened = A.windows.length > w0;
  // walk round him while the screen is open (he turns his model to follow)
  for (let i = 0; i < 4; i++) { await run(`tp TestRat ${X + 0.5 + (i % 2 ? 2 : -2)} ${Y + 1} ${Z + 1.5}`); await sleep(1100); }
  console.log((opened && closed === 0 ? 'PASS' : 'FAIL') + ` Pearlman's trade window stays open for 4+ s while he turns to face you  -- opened ${opened}, closed ${closed}, clicked ${pid.length}`);
  await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); process.exit(0);
})();
