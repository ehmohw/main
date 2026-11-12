// 3.1w: THE ENDLESS VAULT AND THE PIT, as a regular (non-op) player TestRat (replaces t65k's function-driven pass; rcon sets the
// stage only: Tokens, the Ledger, BEGIN pressed, rooms marked solved as a room's own finish would, a wave's monsters cleared, the
// wave clock run forward, standing on the cash-out plate).
//   The Endless Vault, planned through the Ledger's buttons: mode 2, no vault at the end, three rooms ahead, a cursor to build on;
//   three rooms beaten: two more built on (five or more), three counted; the fifth a Rats' Rest, the vault gone deeper (tier II);
//   on the Rest's plate: paid (a Haul Crate), and the Fixer pulls you out.
//   The Pit, planned the same way: mode 1, an arena; wave 1 pours in; cleared, a wave survived; wave 5 a guardian; five survived;
//   the emerald plate between waves cashes out.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, NaN])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const G = 'execute in bm:gutter run ';
  const cnt = async sel => +(((await run(`execute in bm:gutter if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const ist = async o => +(((await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const haul = async () => wait(12000, async () => /Found [1-9]/.test(await run('clear TestRat minecraft:barrel[minecraft:custom_data~{bm_haul:1b}] 0')), 400);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // (a clean slate: no Raid Crew coming in, no hard-mode guardian swapped in, safe ground anywhere)
  for (const o of ['bm.crew', 'bm.crewoff', 'bm.crewoff2', 'bm.crewoff3', 'bm.fcon', 'bm.fcon2', 'bm.gvhr']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const f of ['plan_anywhere', 'heist_hard_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);

  const plan = async (mode) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
    await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    await sleep(2000);
    for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
    A.cmd(`trigger bm.act set ${mode}`); await sleep(1500); A.cmd('trigger bm.act set 7613');
    return wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500);
  };
  const begin = async () => {
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(600);
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
    await sleep(1500);
    if ((await ist('bm.gvst')) < 2) await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);   // (the ready check: again to go anyway)
    return wait(8000, async () => (await ist('bm.gvst')) >= 2, 300);
  };
  const ROOMS = () => `@e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,scores={bm.gvi=${GI}}]`;
  const solve = async (q) => {
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvi=${GI},bm.gvq=${q}},limit=1] run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvi=${GI},bm.gvq=${q}},limit=1] at @s run function bm:p70/solved`); await sleep(3200);
  };
  let GI = 0;

  // ================================================================== THE ENDLESS VAULT
  if (ok('The Endless Vault planned through the Ledger (Plan a Heist -> THE ENDLESS VAULT -> 7 tries)', await plan(7606))) {
    await sleep(2000); GI = await num('scoreboard players get TestRat bm.gvi');
    ok('...mode 2, no vault at the end, three rooms ahead', (await ist('bm.gvmd')) === 2 && (await cnt(`@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}}]`)) === 0 &&
       (await cnt(ROOMS())) === 3, `mode ${await ist('bm.gvmd')}, rooms ${await cnt(ROOMS())}`);
    ok('...a cursor kept to build on', (await cnt(`@e[type=minecraft:marker,tag=bm.gvcurk]`)) >= 1);
    ok('...BEGIN: under way', await begin(), `state ${await ist('bm.gvst')}`);
    for (let q = 1; q <= 3; q++) await solve(q);
    const nr = await cnt(ROOMS());
    ok('three rooms beaten: the vault builds on ahead (five or more)', nr >= 5, `rooms ${nr}`);
    ok('...three rooms counted', (await ist('bm.gvxw')) === 3, `${await ist('bm.gvxw')}`);
    for (let q = 4; q <= 5; q++) await solve(q);
    ok('the fifth room is a Rats\' Rest', (await cnt(`@e[type=minecraft:marker,tag=bm.gvr_rest,scores={bm.gvi=${GI},bm.gvq=5}]`)) === 1,
       await run(`execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvi=${GI},bm.gvq=5},limit=1] Tags`));
    ok('...and the vault has gone deeper: tier II or more', (await ist('bm.gvt')) >= 2, `tier ${await ist('bm.gvt')}`);
    await run('clear TestRat');
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_rest,scores={bm.gvi=${GI},bm.gvq=5},limit=1] at @s run tp TestRat ~ ~ ~9`); await sleep(1500); A.stand();
    ok('on the Rest\'s plate: cashed out - a Haul Crate', await haul(), `state ${await ist('bm.gvst')}`);
    ok('...and the Fixer pulls you out', await wait(15000, async () => !/bm:gutter/.test(await run('data get entity TestRat Dimension')), 500));
  }

  // ================================================================== THE PIT
  if (ok('The Pit planned through the Ledger (Plan a Heist -> THE PIT -> 7 tries)', await plan(7607))) {
    await sleep(2000); GI = await num('scoreboard players get TestRat bm.gvi');
    const AR = `@e[type=minecraft:marker,tag=bm.gvr_arena,scores={bm.gvi=${GI}},limit=1]`;
    ok('...mode 1, an arena after the den', (await ist('bm.gvmd')) === 1 && (await cnt(AR)) === 1, `mode ${await ist('bm.gvmd')}`);
    ok('...BEGIN: under way', await begin());
    await run(`execute in bm:gutter as ${AR} at @s run tp TestRat ~-10 ~ ~`); await sleep(6500); A.stand();
    const g1 = await cnt(`@e[tag=bm.gvg,scores={bm.gvi=${GI}}]`) || await cnt('@e[tag=bm.gvg]');
    ok('wave 1 pours in', g1 >= 3, `guards ${g1}`);
    await run(`${G}kill @e[tag=bm.gvg]`); await sleep(1600);
    ok('...cleared: a wave survived', (await ist('bm.gvxw')) === 1, `${await ist('bm.gvxw')}`);
    let boss = false;
    for (let w = 2; w <= 5; w++) {
      await run(`execute in bm:gutter as ${AR} run scoreboard players set @s bm.gvtm 239`); await sleep(1800);
      if (w === 5) boss = await wait(4000, async () => (await cnt('@e[tag=bm.gvboss]')) >= 1);
      await run(`${G}kill @e[tag=bm.gvg]`); await run(`${G}kill @e[tag=bm.gvboss]`); await sleep(1600);
    }
    ok('wave 5: a guardian', boss);
    ok('...five waves survived', (await ist('bm.gvxw')) === 5, `${await ist('bm.gvxw')}`);
    await run('clear TestRat');
    await run(`execute in bm:gutter as ${AR} at @s run tp TestRat ~-15 ~ ~4`); await sleep(1200); A.stand();
    ok('the emerald plate between waves cashes out: a Haul Crate', await haul(), `state ${await ist('bm.gvst')}`);
    await wait(15000, async () => !/bm:gutter/.test(await run('data get entity TestRat Dimension')), 500);
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_safe', 'heist_hard_any', 'prime_chance', 'fork_chance', 'traps_chance', 'curse_chance']) await run(`function bm:admin/${f}`);
  await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home'); await run('clear TestRat'); await run('effect clear TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
