// 3.1w: RAID CONTRACTS AND THE COAT CHECK, as a regular (non-op) player TestRat (replaces t89's function-driven vault steps; rcon
// sets the stage only: Cecil and Emma met, no contracts yet, the contract and the summoning items handed over, Tokens and the Ledger).
//  - Cecil's Raid Contract, used as a real item (held, right-click): his bit signed, the contract used up; a second one isn't wasted;
//  - a job planned through the Ledger's buttons carrying Cecil's gem and Emma's ribbon: both stay at the coat check;
//  - under contract, Cecil comes into the vault by himself; Emma (no contract) stays home;
//  - out through the den door (before BEGIN: at once, no question): the gem and the ribbon are handed back.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const has = async iid => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async sel => +(((await run(`execute in bm:gutter if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const iget = async (obj) => +(((await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${obj}`)).match(/has (-?\d+)/) || [0, -99])[1]);
  const KILL = async () => { for (const t of ['bm.cecilpet', 'bm.emmapet']) { await run(`execute in minecraft:overworld run kill @e[tag=${t}]`); await run(`execute in bm:gutter run kill @e[tag=${t},distance=0..]`); } };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_anywhere', 'heist_hard_never', 'heist_variants_never']) await run(`function bm:admin/${f}`);
  await KILL();
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  for (const o of ['bm.crew', 'bm.crewoff', 'bm.crewoff2', 'bm.crewoff3', 'bm.gvhr']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('execute as TestRat run function bm:admin/contracts_none');
  for (const k of ['cecil', 'emma']) await run(`advancement grant TestRat only bm:met/${k}`);
  await run('scoreboard players set TestRat bm.cpcd 0'); await run('scoreboard players set TestRat bm.emcd 0');
  await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await sleep(2000);

  // ---- signing: the contract used as a real item
  await run('loot replace entity TestRat hotbar.2 loot bm:items/fcontract_cecil'); await run('loot give TestRat loot bm:items/fcontract_cecil');
  A.slot(2); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(800);
  ok('Cecil\'s Raid Contract, used: his bit signed', ((await num('scoreboard players get TestRat bm.fcon')) & 1) === 1, `fcon ${await num('scoreboard players get TestRat bm.fcon')}`);
  ok('...and that contract used up', (await has('fcontract_cecil')) === 1, `${await has('fcontract_cecil')}`);
  await run('scoreboard players set TestRat bm.gvhc 0'); await sleep(300);
  A.slot(2); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(800);
  ok('A second contract for Cecil isn\'t wasted', (await has('fcontract_cecil')) === 1 && (await num('scoreboard players get TestRat bm.fcon')) === 1, `${await has('fcontract_cecil')}`);
  await run('clear TestRat');

  // ---- into the vault with the summoning items
  await run('loot replace entity TestRat hotbar.4 loot bm:items/cecil_gem'); await run('loot replace entity TestRat hotbar.5 loot bm:items/emma_ribbon');
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 0');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
  if (!ok('a job planned through the Ledger', await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500))) return done();
  await sleep(2000);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  ok('The summoning items stay at the coat check', (await has('cecil_gem')) === 0 && (await has('emma_ribbon')) === 0, `gem ${await has('cecil_gem')}, ribbon ${await has('emma_ribbon')}`);
  ok('Under contract, Cecil comes along by himself', await wait(8000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.cecilpet,distance=0..]')) === 1, 400));
  ok('Without one, Emma stays home', (await cnt('@e[type=minecraft:cat,tag=bm.emmapet,distance=0..]')) === 0);

  // ---- out through the den door: the items handed back
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(1000);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.exitm] at @s if entity @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},distance=..60] run tp TestRat ~ ~ ~`);
  ok('the den door before BEGIN: out at once (it only asks once the job is under way)', await wait(6000, async () => !(await passes('execute if entity @a[name=TestRat,tag=bm.gvp]')), 300));
  ok('...and the gem and the ribbon are handed back', await wait(6000, async () => (await has('cecil_gem')) === 1 && (await has('emma_ribbon')) === 1, 400),
     `gem ${await has('cecil_gem')}, ribbon ${await has('emma_ribbon')}`);
  return done();

  async function done() {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    for (const f of ['plan_safe', 'heist_hard_any', 'heist_variants_off']) await run(`function bm:admin/${f}`);
    await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home');
    await run('execute as TestRat run function bm:admin/contracts_none'); await KILL();
    await run('clear TestRat'); await run('effect clear TestRat'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
    A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
  }
})().catch(e => { console.error(e); process.exit(1); });
