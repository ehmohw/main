// 2.82: KILLERWATT PAYS ON ANY DEATH, ONCE - as a regular (non-op) player standing by (rcon sets the stage: a KillerWatt summoned
// beside him on a stone floor, made killable). Brought down by something other than a player (lightning): everyone within 64 is paid when his body
// crumples - a first win gives his Tendrils and his Spark, plus the hoard. Brought down by the player's own blow: paid once (the
// killing-blow advancement pays, and the crumple sees it's been paid and pays nobody twice). And the same for his ETHEREAL form
// (staged by his ascension, as an Ethereal Gem set down nearby does): his Spark and the Ethereal Tendrils - never the plain ones.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // (a floor of his own, far out: an arena over the void lets him walk off and fall, leaving his parts behind)
  await run('execute in minecraft:overworld run tp TestRat 5200 121 5200'); await sleep(3000);
  await run('execute in minecraft:overworld run fill 5176 120 5176 5224 120 5224 minecraft:stone');
  await run('execute in minecraft:overworld run fill 5176 121 5176 5224 140 5224 minecraft:air');
  await run('execute in minecraft:overworld run tp TestRat 5200 121 5200 0 0'); await sleep(1500);
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 120 4 true');
  const cnt = async i => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${i}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const kxk = async () => +(((await run('scoreboard players get TestRat bm.kxk')).match(/has (-?\d+)/) || [0, 0])[1]);
  for (const [label, how] of [['brought down by lightning (no player)', 'damage @e[type=minecraft:husk,tag=bm.kxboss,limit=1] 9999 minecraft:lightning_bolt'],
                              ['brought down by the player\'s own blow', 'damage @e[type=minecraft:husk,tag=bm.kxboss,limit=1] 9999 minecraft:player_attack by TestRat']]) {
    await run('clear TestRat'); await run('execute as TestRat run scoreboard players reset @s bm.kxk'); await run('advancement revoke TestRat only bm:p79/kill');
    await run('execute as TestRat at @s positioned ^ ^ ^6 run function bm:admin/killerwatt'); await sleep(12000);
    await run('execute as @e[type=minecraft:husk,tag=bm.kxboss,limit=1] run data merge entity @s {Invulnerable:0b}');
    A.chats.length = 0;
    await run(how); await sleep(5000);
    const t = await cnt('killerwatt_tendrils'), s = await cnt('kw_spark'), m = await cnt('medallion'), k = await kxk();
    const msgs = A.chats.filter(c => /KILLERWATT/.test(c)).length;
    ok(`${label}: his Tendrils, his Spark and the hoard - paid once`, t === 1 && s === 1 && m >= 3 && k === 1 && msgs === 1,
       `tendrils ${t} spark ${s} medallions ${m} wins ${k}, ${msgs} announcement(s)`);
    await sleep(3000);
  }
  for (const [label, how] of [['ETHEREAL, brought down by lightning (no player)', 'damage @e[type=minecraft:husk,tag=bm.kxboss,limit=1] 9999 minecraft:lightning_bolt'],
                              ['ETHEREAL, brought down by the player\'s own blow', 'damage @e[type=minecraft:husk,tag=bm.kxboss,limit=1] 9999 minecraft:player_attack by TestRat']]) {
    await run('clear TestRat'); for (const o of ['bm.kxk', 'bm.kxek']) await run(`execute as TestRat run scoreboard players reset @s ${o}`);
    for (const a of ['p79/kill', 'p83/killed_eth']) await run(`advancement revoke TestRat only bm:${a}`);
    await run('execute as TestRat at @s positioned ^ ^ ^6 run function bm:admin/killerwatt'); await sleep(12000);
    await run('execute in minecraft:overworld as @e[type=minecraft:husk,tag=bm.kxboss,limit=1] at @s run function bm:p83/ascend'); await sleep(1500);
    const asc = /count: 1/i.test(await run('execute in minecraft:overworld run execute if entity @e[type=minecraft:husk,tag=bm.kxboss,tag=bm.kxeth]'));
    await run('execute as @e[type=minecraft:husk,tag=bm.kxboss,limit=1] run data merge entity @s {Invulnerable:0b}');
    A.chats.length = 0;
    await run(how); await sleep(5000);
    const t = await cnt('killerwatt_tendrils'), e = await cnt('ethereal_tendrils'), s = await cnt('kw_spark'), m = await cnt('medallion'), k = await kxk();
    const msgs = A.chats.filter(c => /KILLERWATT/.test(c)).length;
    ok(`${label}: his Spark, the Ethereal Tendrils (not the plain ones) and the hoard - paid once`, asc && e === 1 && t === 0 && s === 1 && m >= 3 && k === 1 && msgs === 1,
       `ascended ${asc}, ethereal ${e} plain ${t} spark ${s} medallions ${m} wins ${k}, ${msgs} announcement(s)`);
    await sleep(3000);
  }
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run kill @e[type=minecraft:husk,tag=bm.kxboss,x=5200,y=121,z=5200,distance=..64]');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
