const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const R = await rcon(); const run = c => R.run(c);
  const O = 'execute in minecraft:overworld run ';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  await run('gamemode survival TestRat'); await run('clear TestRat');
  for (const p of ['p252', 'p227', 'p195', 'p229']) await run(`execute as TestRat at @s run function bm:${p}/home`);
  for (const cd of ['bm.mlcd', 'bm.ktcd', 'bm.bvcd']) await run(`scoreboard players set TestRat ${cd} 0`);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/kettle_plane'); await sleep(500);
  A.slot(5); await sleep(300); A.chats.length = 0; A.bars.length = 0; A.use(); await sleep(400); A.release(); await sleep(2500);
  console.log('bars', A.bars, 'chats', A.chats);
  console.log(await run('execute if entity @e[type=minecraft:wolf,tag=bm.ktpet,tag=!bm.ffpet]'));
  console.log(await run('scoreboard players get TestRat bm.ktcd'));
  console.log(await run('data get entity TestRat SelectedItem'));
  for (const p of ['p227']) await run(`execute as TestRat at @s run function bm:${p}/home`);
  A.end(); R.end(); process.exit(0);
})();
