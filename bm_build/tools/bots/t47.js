// v2.47: carrying the Ethereal Gem anywhere in your inventory: a shimmer of the nine follows you
const { bot, rcon, sleep } = require('./lib');
const X = 10600, Y = 200, Z = 10600;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  let parts = 0, sample = null; const near = (p) => { if (!sample) sample = JSON.stringify(p).slice(0, 200); let x = p.x, y = p.y, z = p.z; if (x === undefined && p.data) { const b = Buffer.from(p.data.data || p.data); try { x = b.readDoubleBE(11); y = b.readDoubleBE(19); z = b.readDoubleBE(27); } catch (e) { return false; } }
    return Math.abs(x - X - 0.5) < 1.6 && Math.abs(z - Z - 0.5) < 1.6 && y > Y + 0.5 && y < Y + 3; };
  A.on('world_particles', (p) => { if (near(p)) parts++; }); A.on('level_particles', (p) => { if (near(p)) parts++; });
  const window = async (ms) => { parts = 0; await sleep(ms); return parts; };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 10} ${Z - 10} ${X + 10} ${Z + 10}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} stone`); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await sleep(1500);
  const base = await window(2000);
  await run('loot replace entity TestRat inventory.20 loot bm:items/ethereal_gem'); await sleep(300);
  const deep = await window(2000);
  ok('Carried deep in the inventory (not held): the shimmer follows you', deep >= base + 10 && deep >= 3 * Math.max(base, 1), `particles in 2 s: ${base} without, ${deep} with`);
  await run('item replace entity TestRat inventory.20 with air'); await run('loot replace entity TestRat weapon.offhand loot bm:items/ethereal_gem'); await sleep(300);
  const off = await window(2000);
  ok('...in the off-hand too', off >= base + 10, `${off}`);
  await run('item replace entity TestRat weapon.offhand with air'); await sleep(400);
  console.log('  gems left:', await run('clear TestRat *[custom_data~{bm:"ethereal_gem"}] 0'), '| tags:', await run('tag TestRat list'));
  const none = await window(2000);
  ok('...and it stops when the gem is gone', none <= base + 3, `${none}`);
  console.log('  packet:', sample);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
