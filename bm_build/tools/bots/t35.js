// v2.34: every roaming boss always drops its relic to a player's kill (3 kills each)
const { bot, rcon, sleep } = require('./lib');
const X = 6800, Y = 100, Z = 6800;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`tp TestRat ${X+0.5} ${Y+1} ${Z+0.5} 0 0`); await sleep(2500); await run('gamemode creative TestRat');
  await run(`fill ${X-20} ${Y} ${Z-20} ${X+20} ${Y} ${Z+20} stone`); await run(`fill ${X-20} ${Y+1} ${Z-20} ${X+20} ${Y+15} ${Z+20} air`);
  const res = [];
  for (const [adm, ent, tag, relic, time, w] of [['horseman', 'wither_skeleton', 'bm.hhm', 'horseman_head', 'night', 'clear'], ['pharaoh', 'husk', 'bm.sph', 'pharaoh_crook', 'day', 'clear'],
      ['storm_roc', 'phantom', 'bm.roc', 'storm_talon', 'day', 'thunder'], ['treant', 'creaking', 'bm.trt', 'heartwood_branch', 'night', 'clear'],
      ['colossus', 'magma_cube', 'bm.mcol', 'molten_gauntlet', 'day', 'clear'], ['voidwalker', 'enderman', 'bm.vwk', 'void_scepter', 'day', 'clear']]) {
    await run(`time set ${time}`); await run(`weather ${w}`); await sleep(w === 'thunder' ? 8000 : 1500);
    let got = 0;
    for (let i = 0; i < 3; i++) {
      await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..40]`);
      await run('execute as TestRat at @s run function bm:admin/' + adm); await sleep(500);
      await run(`damage @e[type=${ent},tag=${tag},limit=1] 9999 minecraft:player_attack by TestRat`); await sleep(1500);
      got += await cnt(`@e[type=item,x=${X},y=${Y},z=${Z},distance=..40,nbt={Item:{components:{"minecraft:custom_data":{bm:"${relic}"}}}}]`) > 0 ? 1 : 0;
    }
    console.log((got === 3 ? 'PASS ' : 'FAIL ') + `${adm}: relic dropped ${got}/3 kills`); res.push(got === 3);
    await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`);
  }
  await run('weather clear'); await run('time set day');
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
