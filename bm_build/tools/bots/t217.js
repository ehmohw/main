// 2.82o: THE GRAPPLE ROOM, AND HEISTS FROM ANYWHERE - as a regular (non-op) player TestRat, every step a real packet (rcon sets
// the stage: a solo heist laid with only Grapple rooms - the Swinging Lamps - TestRat stood in it, aimed with a teleport).
//   THE HOOK: the room lends one Fixer's Hook. Dropped (Q), it's gone from the floor and one more comes - no more than one,
//   however long TestRat waits; with the inventory open and the hook on the cursor, no second one is lent.
//   THE SWINGING LAMPS: hooking a lamp's chain (anywhere on its swing) takes - TestRat is hung under the lamp over its island.
//   ANYWHERE: from inside the Black Market (its adventure zone), the Ledger's Plan a Heist goes through.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const G = 'execute in bm:gutter run ';
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const RH = '*[minecraft:custom_data~{bm_rhook:1b}]';
  const hooks = async () => { const o = await run(`clear TestRat ${RH} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_safe', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never', 'rooms_only_grapple', 'variant_b']) await run(`function bm:admin/${f}`);
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty');
  // ---- from inside the Black Market (the stage: TestRat in the market's adventure zone)
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await sleep(1500);
  await run('tag TestRat add bm.adv');                                      // (the stage: in the Black Market's zone - what the old check refused)
  const inMkt = await passes('execute if entity @a[name=TestRat,tag=bm.adv]'); const mp = [];
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7601'); await sleep(1500); A.cmd('trigger bm.act set 7613');
  const went = await wait(40000, async () => (await num('scoreboard players get TestRat bm.gvi')) >= 1, 500);
  ok('from inside the Black Market, the Ledger\'s Plan a Heist goes through', inMkt && went, `in market ${inMkt} (${mp.join(',')}), went ${went}`);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
  await run('tag TestRat remove bm.adv');
  const LB = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},limit=1]`;
  await wait(30000, async () => passes(`${G}execute if entity ${LB}`), 500);
  const lp = (await run(`${G}data get entity ${LB} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [bx, by, bz] = [Math.floor(+lp[1]) + 11, Math.floor(+lp[2]) + 1, Math.floor(+lp[3]) + 3];
  await run(`execute in bm:gutter as ${LB} at @s run tp TestRat ~10 ~ ~3 -90 0`); await sleep(1500);
  for (let k = 0; k < 3 && (await num(`${G}scoreboard players get ${inst} bm.gvst`)) < 2; k++) { A.useOn(bx, by, bz, 4); await sleep(2600); }
  const room = `@e[type=minecraft:marker,tag=bm.gvr_grapple,scores={bm.gvi=${GI}},sort=nearest,limit=1]`;
  await run(`${G}execute as ${room} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(2000);
  const h0 = await hooks();
  // ---- dropped: gone from the floor, one more lent - never a pile
  let src = -1; for (let i = 0; i < 9 && src < 0; i++) if (await passes(`execute if items entity TestRat hotbar.${i} ${RH}`)) src = i;
  A.slot(src); await sleep(300); A.drop(true); await sleep(6000);
  const floor = await passes(`${G}execute as @e[type=minecraft:item] if items entity @s contents ${RH}`);
  const h1 = await hooks();
  ok('the room lends one hook; dropped, it\'s cleared from the floor and exactly one comes back - six seconds later still one', h0 === 1 && !floor && h1 === 1, `${h0} -> ${h1}, on floor ${floor}`);
  // ---- on the cursor (inventory open, picked up): no second one
  A.write('entity_action', { entityId: A.entityId || 0, actionId: 'open_inventory', jumpBoost: 0 }); await sleep(300);
  src = -1; for (let i = 0; i < 9 && src < 0; i++) if (await passes(`execute if items entity TestRat hotbar.${i} ${RH}`)) src = i;
  await run(`item replace entity TestRat player.cursor from entity TestRat hotbar.${src}`); await run(`item replace entity TestRat hotbar.${src} with minecraft:air`);
  await sleep(5000);
  const h2 = await hooks();
  await run(`item replace entity TestRat hotbar.0 from entity TestRat player.cursor`); await run('item replace entity TestRat player.cursor with minecraft:air');
  ok('...with the hook on the cursor, no second hook is lent', h2 === 1 && (await hooks()) === 1, `${h2}`);
  // ---- the swinging lamp: aim at its chain, hook
  await run(`${G}execute as ${room} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(800);
  await run(`${G}execute as TestRat at @s run tag @e[type=minecraft:marker,tag=bm.gvswing,sort=nearest,limit=1] add t217sw`);
  const sw = `@e[type=minecraft:marker,tag=t217sw,limit=1]`;
  const swp = (await run(`${G}data get entity ${sw} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  await run(`${G}execute as ${room} at @s run tp TestRat ~-10 ~ ~ facing ${swp[0]} ${swp[1] + 2.5} ${swp[2]}`); await sleep(800);
  src = -1; for (let i = 0; i < 9 && src < 0; i++) if (await passes(`execute if items entity TestRat hotbar.${i} ${RH}`)) src = i;
  A.slot(src); await sleep(300); A.bars.length = 0;
    for (let d = 1; d < 12; d++) console.log('DBG ray', d, await run(`execute as TestRat at @s anchored eyes positioned ^ ^ ^${d} if block ~ ~ ~ #bm:grap_pass`)); }
  A.use(); await sleep(200); A.release();
  const hung = await wait(10000, async () => passes(`${G}execute as ${sw} at @s if entity @a[name=TestRat,distance=..4]`), 200);
  ok('the Swinging Lamps: TestRat hooks a lamp by its chain and is hung under it over the island', hung, A.bars.slice(-3).join(' | ') + ' ' + (await run('data get entity TestRat Pos')) + ' ' + swp.join(','));
  // ---- clean up
  await run(`${G}tag @e[tag=t217sw] remove t217sw`);
  A.input({ shift: true }); await sleep(400); A.input({});
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['rooms_any', 'variant_random', 'prime_chance', 'fork_chance', 'traps_chance', 'curse_chance']) await run(`function bm:admin/${f}`);
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
