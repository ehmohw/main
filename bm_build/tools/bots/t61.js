const { bot, rcon, sleep } = require('./lib');
const X = 12300, Y = 200, Z = 12300;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(800); const B = await bot('PartyPal'); await sleep(1500);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`tp PartyPal ${X + 3.5} ${Y + 1} ${Z + 0.5}`); await run('gamemode survival PartyPal'); await run('gamemode survival TestRat'); await sleep(1000);
  await run('time set night'); await run(`execute positioned ${X} ${Y + 1} ${Z + 8} run function bm:p54/vwk/summon`); await run('effect give @e[tag=bm.vwk] slowness 60 255 true');
  for (let i = 0; i < 8; i++) { await sleep(1000); console.log(i, (await run('scoreboard players get #bsc bm.bm')).slice(-12), (await run('scoreboard players get @e[tag=bm.vwk,limit=1] bm.bsn')).slice(-14),
     (await run('attribute @e[type=enderman,tag=bm.vwk,limit=1] minecraft:max_health get')).slice(-8), (await run('data get entity @e[tag=bm.vwk,limit=1] Pos')).slice(-50), (await run('data get entity TestRat Pos')).slice(-50)); }
  await run('kill @e[tag=bm.vwk]'); await run('kill @e[tag=bm.vwkmin]'); await run('time set day'); process.exit(0); })();
