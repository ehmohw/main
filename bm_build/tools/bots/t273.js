// 2.94q: THE SCORCHING ARACHNO-LANTERN'S SPAWN, on a Blood Moon, with a regular (non-op) player out under the open sky.
// rcon sets the stage: a Blood Moon (admin/blood_moon), a stone field by the player, and monsters set down there in batches
// the way the world spawns them (untagged: the pack's own per-second pass finds each as a fresh spawn and rolls for it).
//   hard mode (conquest 0: no Dread to take a roll first): the great Lantern rises out of one of the first 3000 (1 in 500 each)
//     - whole: its giant host, its rig, its bar; then it's sent off (p82/leave).
//   normal mode, the same 3000: a few at most (1 in 2500 each; an informational count, a loose bound).
//   never under a roof, never with one already out. (The world's own spawning held off meanwhile: only the test's monsters roll.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found |data: )(-?\d+)/) || [0, -1])[1]);
  const O = 'execute in minecraft:overworld run ';
  const cnt = async sel => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const X = 21000, Y = 120, Z = 21000;
  const GIANT = '@e[type=minecraft:giant,tag=bm.salboss]';
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:invisibility 900 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y} ${Z + 16} minecraft:stone`); await run(`${O}fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 20} ${Z + 16} minecraft:air`);
  await run(`${O}fill ${X + 8} ${Y + 4} ${Z + 8} ${X + 14} ${Y + 4} ${Z + 14} minecraft:stone`);          // (a roof, for the under-a-roof check)
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500); A.stand();
  await run(`${O}execute as ${GIANT} at @s run function bm:p82/leave`);
  await run('gamerule spawn_mobs false');                 // (only the test's own spawns roll: none of the world's out past the field)
  const conq = await num('scoreboard players get TestRat bm.conq'); await run('scoreboard players set TestRat bm.conq 0');
  await run('function bm:admin/blood_moon');
  ok('a Blood Moon is up', await wait(20000, async () => (await num('scoreboard players get #active bm.bm')) === 1, 500));
  const mobs = ['zombie', 'skeleton', 'spider', 'creeper'];
  const clear = async () => { for (const t of [...mobs, 'husk', 'stray', 'witch', 'enderman', 'cave_spider', 'ravager', 'item', 'experience_orb'])
    await run(`${O}kill @e[type=minecraft:${t},x=${X},y=${Y},z=${Z},distance=..40]`); };
  // a batch of fresh monsters under the sky, a second for the pack's pass to find them; how many Lanterns rose
  const batch = async (n, x0 = X - 10, z0 = Z - 10) => { for (let i = 0; i < n; i++) await run(`${O}summon minecraft:${mobs[i % 4]} ${x0 + (i % 7) * 0.3} ${Y + 1} ${z0 + ((i / 7) | 0) % 7 * 0.3} {NoAI:0b}`.replace(' {NoAI:0b}', ''));
    await sleep(1300); const g = await cnt(GIANT); await clear(); return g; };
  const roll = async (total) => { let n = 0, hits = 0, first = null;
    while (n < total) { const g = await batch(150); n += 150;
      if (g) { hits++; if (!first) { first = { n, rig: await cnt('@e[type=minecraft:item_display,tag=bm.salp]'), bar: await run('bossbar get bm:salb visible') }; }
        await run(`${O}execute as ${GIANT} at @s run function bm:p82/leave`); await sleep(300); } }
    return { hits, first }; };

  // ---- hard mode
  await run('scoreboard players set #hardoff bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1');
  let h = { hits: 0, first: null }, n = 0;
  while (!h.first && n < 3000) { const r = await roll(300); n += 300; h.hits += r.hits; h.first = h.first || r.first; }
  ok('hard mode, a Blood Moon: the great Lantern rises from a fresh spawn under the sky (1 in 500; within 3000)', !!h.first, `after ${n} spawns`);
  ok('...whole: its rig and its bar', h.first && h.first.rig > 10 && /visible/.test(h.first.bar), JSON.stringify(h.first));
  // ---- normal mode: rarer
  await run('scoreboard players set #hard bm.cfg 0'); await run('scoreboard players set #hardoff bm.cfg 1');
  const nm = await roll(3000);
  console.log(`  (normal mode: ${nm.hits} in 3000; hard mode: ${h.hits} in ${n})`);
  ok('normal mode: rarer (1 in 2500: 0-5 in 3000)', nm.hits <= 5, `${nm.hits}`);
  // ---- under a roof: never (hard mode, 1500 under the roof)
  await run('scoreboard players set #hardoff bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1');
  let roofed = 0, where = ''; for (let k = 0; k < 10; k++) { if (await batch(150, X + 9, Z + 9)) { roofed++; where += await run(`${O}data get entity ${GIANT.slice(0, -1)},limit=1] Pos`); await run(`${O}execute as ${GIANT} at @s run function bm:p82/leave`); await sleep(300); } }
  ok('under a roof: never (1500 spawns)', roofed === 0, `${roofed} ${where}`);
  // ---- one out already: no second
  await run(`${O}execute positioned ${X - 12} ${Y + 1} ${Z - 12} run function bm:p82/summon`); await sleep(500);
  for (let k = 0; k < 10; k++) await batch(150);
  ok('one out already: never a second (1500 spawns)', (await cnt(GIANT)) === 1, `${await cnt(GIANT)}`);

  // ---- clean up
  await run(`${O}execute as ${GIANT} at @s run function bm:p82/leave`); await clear();
  await run('scoreboard players set #hard bm.cfg 0'); await run('scoreboard players set #hardoff bm.cfg 1'); await run(`scoreboard players set TestRat bm.conq ${Math.max(conq, 0)}`);
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day');
  await run('gamerule spawn_mobs true'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const k = res.filter(Boolean).length; console.log(`${k}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(k === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
