const { bot, rcon, sleep } = require('./lib');
const X = 5200, Y = 100, Z = 5200;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(1000);
  await run('clear TestRat'); await run('loot replace entity TestRat armor.chest loot bm:items/hollow_wings');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 -90`); await sleep(500); A.pos.pitch = -90;
  A.input({ shift: true }); let maxy = 0;
  for (let i = 0; i < 30; i++) { await sleep(100); const p = await run('data get entity TestRat Pos[1]'); const y = parseFloat(p.split(': ')[1]); if (y > maxy) maxy = y; }
  A.input({});
  console.log('max y', maxy, 'ewg', await run('scoreboard players get TestRat bm.ewg'), 'armor', await run('attribute TestRat minecraft:armor get'));
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
