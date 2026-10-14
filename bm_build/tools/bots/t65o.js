// v2.65: the 2.60 rooms still work in their new tiers (levers, plates, guards at I; tiles, lasers, dial at III), on a bench
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  const pot = async () => num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvpot`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const benchClean = async () => { for (let x0 = 1590; x0 < 1990; x0 += 60) { await run(`execute in bm:gutter run forceload add ${x0} -10 ${x0 + 59} 40`); }
    await sleep(2500); await run('execute in bm:gutter run kill @e[type=!player,x=1590,y=40,z=-10,dx=400,dy=60,dz=50]');
    for (let x0 = 1590; x0 < 1990; x0 += 20) await run(`execute in bm:gutter run fill ${x0} 60 -5 ${x0 + 19} 95 30 air strict`);
    for (let x0 = 1590; x0 < 1990; x0 += 60) await run(`execute in bm:gutter run forceload remove ${x0} -10 ${x0 + 59} 40`); };
  await benchClean();
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await sleep(1500);
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000);
  ok('In a heist', /bm:gutter/.test(await run('data get entity TestRat Dimension')));
  await run('effect give TestRat resistance 600 4 true'); await run('effect give TestRat regeneration 600 2 true');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(500);
  const gi = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvi`);
  const alarm = async () => num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gva`);
  for (let x0 = 1590; x0 < 1990; x0 += 60) await run(`execute in bm:gutter run forceload add ${x0} -10 ${x0 + 59} 40`); await sleep(2500);
  const bench = async (kind, x, tier) => {
    await run(`scoreboard players set #gt bm.rng ${tier}`); await run(`scoreboard players set #gi bm.rng ${gi}`); await run('scoreboard players set #gn bm.rng 0'); await run('scoreboard players set #gm bm.rng 0');
    await run(`execute in bm:gutter run place template bm:gv_${kind}_t${tier} ${x} 64 0`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvnew] run function bm:p75/claim`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${kind},x=${x},y=60,z=0,dx=25,dy=30,dz=25] at @s run function bm:p70/r/init`); await sleep(300);
    return `@e[type=marker,tag=bm.gvr_${kind},x=${x},y=60,z=0,dx=25,dy=30,dz=25,limit=1]`;
  };
  const rel = (x, y, z) => `~${x - 12} ~${y - 4} ~${z - 12}`;
  const atm = (m, cmd) => run(`execute in bm:gutter as ${m} at @s run ${cmd}`);
  const gvs = async m => num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvs`);
  const solved = async m => (await gvs(m)) === 3 && /passed/.test(await atm(m, `execute if block ${rel(24, 5, 12)} minecraft:air`));
  const enter = async m => { await atm(m, `tp TestRat ${rel(3, 4, 12)} -90 0`); await sleep(500); };
  // ---- COMBINATION ROOM (tier I)
  let m = await bench('levers', 1600, 1); await enter(m);
  const a0 = await alarm(); const code = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvc`);
  await atm(m, `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(300);
  await atm(m, `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=false]`); await sleep(200);
  ok('Combination Room: a wrong combination rings the alarm', (await alarm()) > a0 && (await gvs(m)) !== 3, `${a0} -> ${await alarm()}`);
  const LV = [8, 10, 12, 14, 16];
  for (let i = 0; i < 5; i++) await atm(m, `setblock ${rel(LV[i], 5, 23)} minecraft:lever[face=wall,facing=north,powered=${(code >> i) & 1 ? 'true' : 'false'}]`);
  await atm(m, `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(500);
  ok('...the ledger\'s combination opens it', await solved(m), 'code ' + code);
  // ---- WEIGHING ROOM (tier I): you on one scale, a dropped item on the other
  m = await bench('plates', 1650, 1); await enter(m);
  await atm(m, `tp TestRat ${rel(5, 4, 5)}`); await atm(m, `summon item ${rel(19, 4, 5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(1600);
  ok('Weighing Room: two scales at once', await solved(m));
  // ---- COUNTING HOUSE (tier I): two waves, a captain, then the way opens
  m = await bench('guards', 1700, 1); await enter(m); await atm(m, `tp TestRat ${rel(12, 4, 12)}`); await sleep(1800);
  const G = '@e[tag=bm.gvg,x=1700,y=60,z=0,dx=25,dy=30,dz=25]';
  const g1 = await cnt(G); const t1 = (await run(`execute in bm:gutter run data get entity ${G.replace(']', ',limit=1]')} id`)).replace(/.*data: /, '');
  await run(`execute in bm:gutter run kill ${G}`); await sleep(2600);
  const g2 = await cnt(G); const cap = await cnt('@e[tag=bm.gvcap,x=1700,y=60,z=0,dx=25,dy=30,dz=25]');
  await run(`execute in bm:gutter run kill ${G}`); await sleep(2600);
  ok('Counting House: a wave, then a bigger one with a captain, then the way opens', g1 >= 2 && g2 > g1 && cap === 1 && await solved(m), `${g1} then ${g2} (+captain ${cap}), guards: ${t1}`);
  // ---- TILE FLOOR (tier III)
  m = await bench('tiles', 1750, 3); await enter(m); const at0 = await alarm();
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvtile,scores={bm.gvsafe=0},x=1750,y=60,z=0,dx=25,dy=30,dz=25,limit=1] run tag @s add t65t');
  await run('execute in bm:gutter as @e[type=marker,tag=t65t,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(500);
  const gone = /passed/.test(await run('execute in bm:gutter as @e[type=marker,tag=t65t,limit=1] at @s if block ~ ~-1 ~ minecraft:air'));
  await run('execute in bm:gutter as @e[type=marker,tag=t65t,limit=1] at @s run tp TestRat ~ ~-3 ~'); await sleep(700);
  ok('Tile Floor: a false tile gives way - into the pit, hauled back, alarm', gone && (await alarm()) > at0, `gone ${gone}, alarm ${at0} -> ${await alarm()}`);
  await sleep(3500);
  ok('...the fallen tile comes back', /passed/.test(await run('execute in bm:gutter as @e[type=marker,tag=t65t,limit=1] at @s unless block ~ ~-1 ~ minecraft:air')));
  await run('tag @e remove t65t');
  await atm(m, `tp TestRat ${rel(22, 4, 12)}`); await sleep(500);
  ok('...the far side beats it', await solved(m));
  // ---- GAUNTLET (tier III)
  m = await bench('lasers', 1800, 3); await enter(m); let zapped = false; const az = await alarm();
  for (let i = 0; i < 40 && !zapped; i++) { await atm(m, `tp TestRat ${rel(5, 4, 12)}`); await sleep(150); zapped = (await alarm()) > az; }
  ok('Gauntlet: a laser zaps you back and rings the alarm', zapped, `${az} -> ${await alarm()}`);
  await sleep(1600); await atm(m, `tp TestRat ${rel(22, 4, 12)}`); await sleep(500);
  ok('...reaching the far plate beats it', await solved(m));
  // ---- DIAL LOCK (tier III): set the dials, then press TRY THE DIALS
  m = await bench('dial', 1850, 3); await enter(m);
  const dc = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvc`);
  ok('Dial Lock: the TRY THE DIALS button is there', /passed/.test(await atm(m, `execute if block ${rel(16, 5, 22)} minecraft:pale_oak_button`)));
  await atm(m, `setblock ${rel(16, 5, 22)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(600);
  ok('...pressed with the dials wrong: still locked', (await gvs(m)) !== 3);
  await atm(m, `setblock ${rel(16, 5, 22)} minecraft:pale_oak_button[face=wall,facing=north,powered=false]`); await sleep(1600);
  for (let i = 0; i < 3; i++) await run(`execute in bm:gutter run data modify entity @e[type=item_frame,tag=bm.gvdial${i},x=1850,y=60,z=0,dx=25,dy=30,dz=25,limit=1] ItemRotation set value ${(dc >> (3 * i)) & 7}b`);
  await atm(m, `setblock ${rel(16, 5, 22)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(800);
  ok('...set to the blueprint\'s arrows and pressed: it opens', await solved(m), `code ${dc}`);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  for (let x0 = 1590; x0 < 1990; x0 += 60) await run(`execute in bm:gutter run forceload remove ${x0} -10 ${x0 + 59} 40`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
