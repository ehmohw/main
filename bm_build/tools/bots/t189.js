// 2.80g: the heist kit is never lost - as a regular (non-op) player. A loaned weapon dropped with Q came back within a quarter
// second, long enough to burn up in lava or fire. rcon sets the stage: a heist under way, a kit (as the racks give it), a pool
// of lava in front of you, a loose kit weapon left lying in lava.
//   Q over the lava: the main weapon is back in your hands at once - nothing lies in the lava, nothing burned.
//   A kit weapon in lava doesn't burn (the kit is fireproof, like netherite).
//   A paperweight can still be put down, as ever.
const { bot, rcon, sleep } = require('./lib_resp');
const H = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const h = H.mk(run);
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await h.heist('levers', 'a', 1); await h.begin(); await sleep(1500);
  const q = (await h.qs('levers'))[0];
  // ---- a kit, as the racks give it; the main weapon in hand
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.kr2 1'); await run('execute as TestRat at @s run function bm:p72/kit/give_2'); await sleep(400);
  const slot0 = (await run('data get entity TestRat Inventory[{Slot:0b}]')).replace(/.*data: /, '');
  const wid = ((await run('data get entity TestRat Inventory[{Slot:0b}].id')).match(/"([^"]+)"/) || [])[1];
  ok('a kit: the main weapon in the first slot, on loan', /bm_kit: 1b/.test(slot0) && !!wid, wid);
  const kitWeapons = async () => +(((await run(`clear TestRat ${wid}[minecraft:custom_data~{bm_kit:1b}] 0`)).match(/Found (\d+)/)) || [0, 0])[1];
  const n0 = await kitWeapons();
  ok('...counted: one of it on you', n0 >= 1, `${n0}`);
  // ---- the stage: a pool of lava right in front, in the room
  await h.go('levers', q, 4, 12); await sleep(500);
  await h.at('levers', q, `fill ${H.rel(5, 3, 11)} ${H.rel(8, 3, 13)} minecraft:lava`);
  await sleep(300);
  // ---- Q over the lava
  A.slot(0); await sleep(250); A.drop(false); await sleep(150);
  const back = await wait(1000, async () => (await kitWeapons()) === n0);
  ok('Q over the lava: the main weapon is straight back in your hands', back, `${await kitWeapons()} of ${n0}`);
  await sleep(1500);
  ok('...nothing lies in the lava, nothing burned (it\'s still yours a moment later)', (await kitWeapons()) === n0 &&
     (await h.cnt(`@e[type=minecraft:item,nbt={Item:{id:"${wid}"}}]`)) === 0);
  // ---- a loose kit weapon lying in lava: fireproof
  await h.at('levers', q, `summon minecraft:item ${H.relf(6.5, 3.2, 12.5)} {Item:{id:"minecraft:stone",count:1},Tags:["bm.t189"],PickupDelay:32767s}`);
  await h.at('levers', q, `item replace entity @e[type=minecraft:item,tag=bm.t189,limit=1,sort=nearest] contents from entity TestRat container.0`);
  await sleep(3000);
  ok('a kit weapon left lying in lava doesn\'t burn (the kit is fireproof)', (await h.cnt('@e[type=minecraft:item,tag=bm.t189]')) === 1);
  await run('execute in bm:gutter run kill @e[type=minecraft:item,tag=bm.t189]');
  // ---- a paperweight can still be put down
  const pw = async () => +(((await run('clear TestRat *[minecraft:custom_data~{bm:"paperweight"}] 0')).match(/Found (\d+)/)) || [0, 0])[1];
  await h.at('levers', q, `fill ${H.rel(5, 3, 11)} ${H.rel(8, 3, 13)} minecraft:air replace minecraft:lava`);
  const p0 = await pw();
  const ps = await (async () => { for (let s = 0; s < 9; s++) if (/paperweight/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; })();
  if (ps >= 0) { A.slot(ps); await sleep(250); A.drop(false); await sleep(1200); }
  ok('a paperweight can still be put down', ps >= 0 && (await pw()) === p0 - 1, `slot ${ps}: ${p0} -> ${await pw()}`);

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random'); await run('function bm:admin/plan_safe'); await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
