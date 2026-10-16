// 2.80g: the vault's guardian, scaled for every crew - as a regular (non-op) player. It grows 50% stronger per raider past the
// first, but no mob holds more than 1024 health: from Tier IV up, a crew of two or more met the same capped guardian, its bar
// opened part-empty and its shell came at the wrong time. rcon sets the stage: a Tier V heist with a second raider (TestMouse,
// another regular player) in its crew, the vault reached, a sword in hand, one heavy blow, the reserve run dry at the end.
//   Walk in, a crew of two: the guardian wakes with its whole health (610 x 1.5 x 1.6 = 1464, or half again under the Armored
//   modifier): 1024 in the mob, the rest a reserve; the bar opens full, out of the whole.
//   Hit it: what the blow took comes back out of the reserve at once; a heavy blow likewise - and the bar falls by it.
//   The second raider leaves: the whole eases to a crew of one's, and what's left of the guardian keeps its share.
//   Under half of the whole (the reserve spent): its shell goes up - as it should, at half.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(1500); let A2 = await bot('TestMouse'); await sleep(2500); A.stand(); A2.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  const G = 'execute in bm:gutter run ';

  await heist('levers', 'a', 5); await begin();
  const GI = await num('scoreboard players get TestRat bm.gvi');
  await H.mouse();                                                                 // (the stage: TestMouse in the crew - a crew of two)
  const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
  const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
  const atV = (cmd) => run(`execute in bm:gutter as ${V} at @s run ${cmd}`);
  const hp = async () => +(((await run(`${G}data get entity ${B} Health`)).match(/(-?[\d.]+)f\s*$/) || [0, NaN])[1]);
  const resv = () => num(`${G}scoreboard players get ${B} bm.gvres`);
  const bar = async (k) => +(((await run(`bossbar get bm:gvb${GI - 1} ${k}`)).match(/(-?\d+)\D*$/)) || [0, -1])[1];
  await run('clear TestRat'); await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword'); await run('gamemode survival TestRat');
  await run('effect give TestRat minecraft:resistance 120 4 true'); await run('effect give TestRat minecraft:regeneration 120 4 true');

  // ---- into the vault: the guardian, whole
  await atV(`tp TestMouse ${rel(4, 4, 10)} -90 0`); await sleep(1500);
  await atV(`tp TestRat ${rel(6, 4, 12)} -90 0`);
  ok('walk into the vault: the guardian wakes', await wait(5000, async () => (await cnt(B)) === 1) &&
     await wait(9000, async () => !/bm\.cfrz/.test(await run(`${G}data get entity ${B} Tags`))));
  const mx = await num(`${G}scoreboard players get ${B} bm.gvmx`);
  ok('...a crew of two at Tier V: its whole health is 1464 (2196 Armored) - past the 1024 a mob can hold', mx === 1464 || mx === 2196, `${mx}`);
  ok('...1024 in the guardian, the rest its reserve', Math.abs((await hp()) - 1024) < 1 && (await resv()) === mx - 1024, `${await hp()} + ${await resv()}`);
  ok('...the bar opens full, out of the whole', await wait(2500, async () => (await bar('max')) === mx && (await bar('value')) >= mx - 10), `${await bar('value')} of ${await bar('max')}`);

  // ---- a hit: the reserve fills it back
  const bp = (await run(`${G}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  await atV(`tp TestRat ${rel(10, 4, 12)} -90 0`); await sleep(400);
  const bpos = bp ? [+bp[1], +bp[2], +bp[3]] : [0, 0, 0];
  const now = (await run(`${G}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); if (now) { bpos[0] = +now[1]; bpos[1] = +now[2]; bpos[2] = +now[3]; }
  await run(`${G}tp TestRat ${bpos[0] - 1.6} ${bpos[1]} ${bpos[2]} -90 0`); await sleep(500);
  const r0 = await resv();
  let e = null, bd = 1e9; for (const x of Object.values(A.ents)) { const d = (x.x - bpos[0]) ** 2 + (x.y - bpos[1]) ** 2 + (x.z - bpos[2]) ** 2; if (d < bd) { bd = d; e = x; } }
  for (let k = 0; k < 3 && (await resv()) === r0; k++) { if (e) A.attack(e.entityId); await sleep(700); }
  const r1 = await resv();
  ok('your sword hits it: what the blow took comes back out of its reserve', r1 < r0 && Math.abs((await hp()) - 1024) < 1, `reserve ${r0} -> ${r1}, health ${await hp()}`);
  await run(`${G}damage ${B} 300 minecraft:out_of_world`);
  await wait(1000, async () => (await resv()) <= r1 - 290);
  const r2 = await resv();
  ok('...a heavy blow (300) likewise: the guardian stays topped up, the reserve pays', r2 <= r1 - 290 && r2 >= r1 - 310 && Math.abs((await hp()) - 1024) < 1, `reserve ${r1} -> ${r2}, health ${await hp()}`);
  ok('...and the bar falls by it', await wait(2500, async () => Math.abs((await bar('value')) - (1024 + r2)) <= 2), `${await bar('value')} (whole ${1024 + r2})`);

  // ---- the second raider leaves: a crew of one's guardian, what's left keeping its share
  const left0 = 1024 + r2;
  A2.end(); A2 = null;
  const eased = await wait(6000, async () => (await num(`${G}scoreboard players get ${B} bm.gvmx`)) === Math.floor(mx * 100 / 150));
  const mx1 = await num(`${G}scoreboard players get ${B} bm.gvmx`);
  const left1 = Math.floor(await hp()) + await resv();
  ok('the second raider leaves: the whole eases to a crew of one\'s (x1/1.5)', eased, `${mx} -> ${mx1}`);
  ok('...and what\'s left of the guardian keeps its share', Math.abs(left1 - Math.floor(left0 * 100 / 150)) <= 3 && (await hp()) <= 1024.5 && (await bar('max')) === mx1,
     `${left0} -> ${left1} (health ${await hp()}, reserve ${await resv()}, bar max ${await bar('max')})`);

  // ---- under half of the whole: the shell goes up
  await run(`${G}scoreboard players set ${B} bm.gvres 0`); await run(`${G}data modify entity ${B} Health set value ${Math.floor(mx1 / 2) - 20}f`);
  ok('under half of the whole (the reserve spent): its shell goes up, as it should at half',
     await wait(3000, async () => /bm\.gvshell/.test(await run(`${G}data get entity ${B} Tags`))), (await run(`${G}data get entity ${B} Tags`)).slice(-160));

  await run(`${G}data modify entity ${B} DeathLootTable set value "minecraft:empty"`); await run(`${G}kill ${B}`);
  await run('effect clear TestRat'); await run('clear TestRat'); await run('tag TestMouse remove bm.gvp');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
