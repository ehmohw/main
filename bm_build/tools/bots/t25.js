const { bot, rcon, sleep } = require('./lib');
const X = 7400, Y = 90, Z = 7400;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1200);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  await run('gamemode creative TestRat'); await run(`tp TestRat ${X} ${Y + 20} ${Z}`); await sleep(3000);
  await run(`execute positioned ${X} ${Y} ${Z} run place template bm:black_market ~-38 ~-18 ~-96`); await sleep(1000);
  const mk = (await run(`data get entity @e[type=minecraft:marker,tag=bm.mkt,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] Pos`)).match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  // template (38,10,46)=CX,W,CZ ; marker template position from mgeo.MKT
  const [mx, my, mz] = mk;
  await run(`tp TestRat ${mx} ${my} ${mz}`); await sleep(12000);
  const tp = await run('data get entity @e[type=minecraft:text_display,tag=bm.bboard,limit=1,sort=nearest] Pos'); const tr = await run('data get entity @e[type=minecraft:text_display,tag=bm.bboard,limit=1,sort=nearest] Rotation');
  const hp = await run('data get entity @e[type=minecraft:interaction,tag=bm.bbhit,limit=1,sort=nearest] Pos');
  console.log('marker', mk, '\ntext', tp, tr, '\nhit', hp);
  const t = tp.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  const plank = await run(`execute if block ${Math.floor(t[0])} ${Math.floor(t[1])} ${Math.floor(t[2]) - 1} minecraft:dark_oak_planks`);
  const front = await run(`execute if block ${Math.floor(t[0])} ${Math.floor(t[1])} ${Math.floor(t[2])} #minecraft:air`);
  ok('notice text sits on the plank face, open in front', plank.includes('passed') && front.includes('passed'), plank + ' / ' + front);
  ok('no old balcony board/text', (await run(`execute store result score #t bm.rng if entity @e[tag=bm.bboard,x=${mx},y=${my},z=${mz},distance=..120]`)).match(/Count: 1$|\b1$/));   // (this market's own: other tests leave boards elsewhere)
  // old-market simulation: a slab on a counter, a sign on the board, then patch
  const c = [mx + (12 - 38.5) + 0.5, my, mz];
  console.log(await run(`execute as @e[type=minecraft:marker,tag=bm.mkt,limit=1,sort=nearest] at @s rotated as @s positioned ^-26 ^1 ^-22 run setblock ~ ~ ~ minecraft:dark_oak_slab[type=top]`));
  console.log(await run(`execute as @e[type=minecraft:marker,tag=bm.mkt,limit=1,sort=nearest] at @s rotated as @s positioned ^-26 ^1 ^-22 run data get block ~ ~ ~`));
  // Zorp in a mothership
  await run(`tp TestRat ${X + 300} ${Y + 10} ${Z}`); await sleep(2500);
  await run(`execute positioned ${X + 300} ${Y} ${Z} run place template bm:mothership ~-25 ~38 ~-25`); await sleep(9000);
  const zp = await run(`data get entity @e[type=minecraft:wandering_trader,tag=bm.npc_alien,limit=1,sort=nearest,x=${X + 300},y=${Y + 40},z=${Z}] Pos`); console.log('zorp', zp);
  const zz = zp.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  ok('zorp in front of the counter', (await run(`execute if block ${Math.floor(zz[0])} ${Math.floor(zz[1])} ${Math.floor(zz[2]) + 1} minecraft:cyan_terracotta`)).includes('passed'));
  let dsk = false;     // (one trade at a time: the whole list is longer than one RCON reply)
  for (let i = 0; i < 60 && !dsk; i++) { const r = await run(`data get entity @e[type=minecraft:wandering_trader,tag=bm.npc_alien,limit=1,sort=nearest,x=${X + 300},y=${Y + 40},z=${Z}] Offers.Recipes[${i}].sell`);
    if (!r.includes('has the following')) break; dsk = r.includes('display_skiff'); }
  ok('zorp sells the display skiff', dsk);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });
