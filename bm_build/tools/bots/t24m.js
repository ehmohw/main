// Cecil in a freshly placed market: spawn, rig, facing, trades, animation
const { bot, rcon, sleep } = require('./lib');
const X = 7000, Y = 90, Z = 7000;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(1000);
  await run('gamemode creative TestRat'); await run(`tp TestRat ${X} ${Y + 20} ${Z}`); await sleep(3000);
  console.log(await run(`execute positioned ${X} ${Y} ${Z} run place template bm:black_market ~-38 ~-18 ~-96`));
  await sleep(1500);
  const mk = await run(`data get entity @e[type=minecraft:marker,tag=bm.mkt,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] Pos`); console.log('market marker', mk);
  const m = mk.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/); const [mx, my, mz] = m.slice(1).map(Number);
  await run(`tp TestRat ${mx} ${my} ${mz + 40}`); await sleep(14000);
  const v = await run(`data get entity @e[type=minecraft:villager,tag=bm.npc_wizard,limit=1] Pos`); console.log('cecil', v);
  console.log('rig parts', await run('execute store result score #t bm.rng if entity @e[tag=bm.cecil]'));
  console.log('offers', await run('data get entity @e[type=minecraft:villager,tag=bm.npc_wizard,limit=1] Offers.Recipes'));
  const c = v.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  console.log('cecil rel to marker', c[0] - mx, c[1] - my, c[2] - mz);
  // stand in front of him (east, +x in template = marker left; marker yaw 0 -> world +x)
  await run(`tp TestRat ${c[0] + 3} ${c[1]} ${c[2]} 90 0`); await sleep(1500);
  console.log('body rot', await run('data get entity @e[tag=bm.cec_body,limit=1] Rotation'), 'head rot', await run('data get entity @e[tag=bm.cec_head,limit=1] Rotation'));
  console.log('arm pos', await run('data get entity @e[tag=bm.cec_arm,limit=1] Pos'));
  await run(`tp TestRat ${c[0] + 2} ${c[1]} ${c[2] + 3}`); await sleep(1500);
  console.log('after moving: body rot', await run('data get entity @e[tag=bm.cec_body,limit=1] Rotation'));
  for (let i = 0; i < 4; i++) { await sleep(2000); console.log('arm tf', (await run('data get entity @e[tag=bm.cec_arm,limit=1] transformation.left_rotation'))); }
  console.log('blocks around', await run(`execute positioned ${c[0]} ${c[1]} ${c[2]} if block ~ ~ ~ #minecraft:air`), await run(`execute positioned ${c[0]} ${c[1] + 1} ${c[2]} if block ~ ~ ~ #minecraft:air`));
  // trade window
  const vid = Object.values(A.ents).find(e => Math.abs(e.x - c[0]) < 0.3 && Math.abs(e.z - c[2]) < 0.3 && Math.abs(e.y - c[1]) < 0.3 && e.type !== undefined);
  await run('gamemode survival TestRat'); await sleep(300);
  if (vid) { A.interact(vid.entityId); await sleep(800); console.log('windows', JSON.stringify(A.windows.slice(-1))); } else console.log('no villager entity seen');
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
