const { bot, rcon, sleep } = require('./lib');
const X = 9600, Y = 100, Z = 9600;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('gamemode survival TestRat');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2000);
  await run(`execute positioned ${X + 0.5} ${Y + 1} ${Z + 2.5} rotated 180 0 run function bm:npc/chef`); await sleep(2000);
  const id = Object.values(A.ents).filter(e => Math.hypot(e.x - X - 0.5, e.z - Z - 2.5) < 0.4).map(e => [e.entityId, e.type]);
  console.log('candidates', JSON.stringify(id), 'ents', Object.keys(A.ents).length);
  let closed = 0; A.on('close_window', () => closed++); A.on('open_window', p => console.log('open', p.windowId, p.inventoryType));
  for (const [i] of id) { A.interact(i); await sleep(300); }
  await sleep(3000); console.log("before tp: closed", closed); await run(`execute as @e[tag=bm.npc_chef,x=${X},y=${Y},z=${Z},distance=..6] at @s run tp @s ~ ~ ~`); await sleep(1000); console.log('windows', A.windows.length, 'closed by server', closed);
  await run(`kill @e[tag=bm.npc_chef,x=${X},y=${Y},z=${Z},distance=..6]`); await run(`kill @e[type=text_display,x=${X},y=${Y},z=${Z},distance=..6]`);
  A.end(); R.end(); process.exit(0);
})();
