// v2.65: who guards each tier, the tier guardians, the music, the themed stone
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await sleep(1500);
  // rosters: spawn 30 guards per tier in a test box and list the types
  await run('execute in bm:gutter run forceload add 600 600 660 660'); await sleep(1500);
  await run('execute in bm:gutter run fill 600 63 600 660 63 660 minecraft:stone'); await run('execute in bm:gutter run fill 600 64 600 660 70 660 air');
  const want = { 1: ['zombie', 'pillager', 'husk'], 2: ['skeleton', 'stray', 'vindicator', 'witch'], 3: ['vindicator', 'piglin_brute', 'husk'],
                 4: ['drowned', 'bogged', 'vindicator', 'breeze'], 5: ['wither_skeleton', 'blaze', 'piglin_brute', 'evoker'] };
  await run('scoreboard players set #gn bm.rng 0'); await run('scoreboard players set #gm bm.rng 0'); await run('scoreboard players set #gi bm.rng 1');
  for (let t = 1; t <= 5; t++) {
    await run(`scoreboard players set #gt bm.rng ${t}`);
    for (let i = 0; i < 30; i++) await run(`execute in bm:gutter positioned ${605 + (i % 10) * 4} 64 ${605 + Math.floor(i / 10) * 4} run function bm:p70/guard`);
    const seen = [];
    for (const ty of ['zombie', 'pillager', 'husk', 'skeleton', 'stray', 'vindicator', 'witch', 'piglin_brute', 'drowned', 'bogged', 'breeze', 'wither_skeleton', 'blaze', 'evoker']) {
      const n = await num(`execute in bm:gutter store result score #t bm.rng if entity @e[type=minecraft:${ty},tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]`);
      if (n > 0) seen.push(`${ty}:${n}`); }
    const types = seen.map(s => s.split(':')[0]);
    // (2.67: the rogues' gallery adds more to each tier - its own roster file says which)
    const F = BMB + 'out_p2/BlackMarket_DP/data/bm/function';
    const riders = require('fs').readdirSync(`${F}/p93`).filter(f => f.endsWith('.mcfunction')).map(f => require('fs').readFileSync(`${F}/p93/${f}`, 'utf8')).join('\n');   // (jockeys and riders)
    const own = [...new Set(((require('fs').readFileSync(`${F}/p75/roster${t}.mcfunction`, 'utf8') + riders).match(/(summon |id:")minecraft:(\w+)/g) || []).map(x => x.replace(/^(summon |id:")minecraft:/, '')))];   // (jockeys ride in as passengers)
    ok(`Tier ${t}: its own guards (${want[t].join(', ')} and the gallery's)`, types.length >= 2 && types.every(x => own.includes(x)) && want[t].some(x => types.includes(x)), seen.join(' '));
    const hp = await run(`execute in bm:gutter run data get entity @e[tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60,limit=1] Health`);
    if (t === 1 || t === 5) console.log('   health', hp.replace(/.*data: /, ''));
    await run('execute in bm:gutter run kill @e[tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]');
  }
  // a night keeps its vindicators
  await run('scoreboard players set #gt bm.rng 1'); await run('scoreboard players set #gn bm.rng 1');
  await run('execute in bm:gutter positioned 620 64 620 run function bm:p70/guard');
  ok('A Blood Moon heist keeps its crimson vindicators (even on tier I)', (await num('execute in bm:gutter store result score #t bm.rng if entity @e[type=vindicator,tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]')) === 1);
  await run('execute in bm:gutter run kill @e[tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]'); await run('scoreboard players set #gn bm.rng 0');
  // captains
  for (const [t, ty] of [[1, 'zombie'], [2, 'vindicator'], [4, 'vindicator'], [5, 'piglin_brute']]) {
    await run(`scoreboard players set #gt bm.rng ${t}`); await run('execute in bm:gutter positioned 620 64 620 run function bm:p70/captain');
    const n = await num(`execute in bm:gutter store result score #t bm.rng if entity @e[type=minecraft:${ty},tag=bm.gvcap,tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]`);
    ok(`Tier ${t} captain: a ${ty}`, n === 1); await run('execute in bm:gutter run kill @e[tag=bm.gvg,x=600,y=60,z=600,dx=60,dy=12,dz=60]'); }
  // guardians
  for (const [t, ty, nm] of [[1, 'zombie', 'Copper Foreman'], [2, 'skeleton', 'Silver Marksman'], [3, 'vindicator', 'Gilded Sentinel'], [4, 'drowned', 'Drowned Treasurer'], [5, 'piglin_brute', 'Gutter King']]) {
    await run(`scoreboard players set #gt bm.rng ${t}`);
    await run('execute in bm:gutter positioned 630 64 630 run function bm:p75/boss_tier');
    const n = await num(`execute in bm:gutter store result score #t bm.rng if entity @e[type=minecraft:${ty},tag=bm.gvbnew,x=600,y=60,z=600,dx=60,dy=12,dz=60]`);
    const name = await run('execute in bm:gutter run data get entity @e[tag=bm.gvbnew,limit=1] CustomName');
    ok(`Tier ${t} guardian: ${nm} (${ty})`, n === 1 && name.includes(nm), name.slice(-80));
    await run('execute in bm:gutter run kill @e[tag=bm.gvbnew]'); }
  await run('execute in bm:gutter run fill 600 63 600 660 70 660 air'); await run('execute in bm:gutter run forceload remove 600 600 660 660');
  // a real heist: themed stone, the music
  for (const t of [1, 4]) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(800);
    for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay 760${t}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7612'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4500);
    const wall = t === 1 ? 'tuff_bricks' : 'deepslate_tiles';
    ok(`Tier ${t}: the den is built in its own stone (${wall})`, /passed/.test(await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s if block ~-12 ~1 ~-6 minecraft:${wall}`)),
       await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run data get block ~-12 ~1 ~-6'));
    await sleep(1500);
    ok(`Tier ${t}: its theme plays (track ${t})`, (await num('scoreboard players get TestRat bm.gvmt')) === t);
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
    ok('...and stops when you leave', isNaN(await num('scoreboard players get TestRat bm.gvmt')) || /none|Can't/.test(await run('scoreboard players get TestRat bm.gvmt')));
  }
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0); })();
