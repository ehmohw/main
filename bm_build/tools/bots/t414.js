// 3.1y: FOLLOWERS WAITING OUTSIDE THE VAULT COME BACK AFTER THE LOUNGE - as a regular (non-op) player TestRat (rcon sets the stage
// only: Emma met, no contracts, her ribbon and Tokens handed over, the job won as the vault's own payout would).
//  - Emma called with her ribbon (a real use); a job planned through the Ledger: she waits outside the vault (no contract);
//  - won: "Go to the Lounge" pressed on the end-of-heist card - into the Lounge;
//  - out through the Lounge's door: home, and Emma comes back to TestRat (3.1w: the Lounge used to cancel her return until after
//    the next heist).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const emma = async () => +(((await run('execute in minecraft:overworld if entity @e[type=minecraft:cat,tag=bm.emmapet,distance=0..]')).match(/count: (\d+)/i) || [0, 0])[1]);
  const KILL = async () => { await run('execute in minecraft:overworld run kill @e[tag=bm.emmapet]'); await run('execute in bm:gutter run kill @e[tag=bm.emmapet,distance=0..]'); };
  const O = 'execute in minecraft:overworld run ';

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_anywhere', 'heist_hard_never']) await run(`function bm:admin/${f}`);
  await KILL();
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  for (const t of ['bm.ow_emma', 'bm.lgbag', 'bm.gvask', 'bm.gvnext']) await run(`tag TestRat remove ${t}`);
  for (const o of ['bm.crew', 'bm.crewoff', 'bm.crewoff2', 'bm.crewoff3', 'bm.gvhr', 'bm.emcd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('execute as TestRat run function bm:admin/contracts_none'); await run('advancement grant TestRat only bm:met/emma');
  await run(`${O}fill 12998 119 12998 13002 119 13002 stone`); await run(`${O}tp TestRat 13000.5 120 13000.5`); await sleep(2000);

  // ---- Emma, called with her ribbon
  await run('loot replace entity TestRat hotbar.4 loot bm:items/emma_ribbon'); A.slot(4); await sleep(300); A.use(); await sleep(400); A.release();
  ok('Emma called with her ribbon (a real use)', await wait(6000, async () => (await emma()) === 1, 300));
  // ---- a job through the Ledger
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7601'); await sleep(1500); A.cmd('trigger bm.act set 7613');
  if (!ok('a job planned through the Ledger', await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500))) return done();
  await sleep(3000);
  ok('...Emma waits outside the vault (no contract)', await wait(12000, async () => (await passes('execute if entity @a[name=TestRat,tag=bm.ow_emma]')) && (await emma()) === 0, 400),
     `tag ${await passes('execute if entity @a[name=TestRat,tag=bm.ow_emma]')}, out ${await emma()}`);
  // ---- won: "Go to the Lounge"
  const gi = await num('scoreboard players get TestRat bm.gvi');
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run function bm:p70/payout`);
  await wait(10000, async () => A.buttons().some(b => /Go to the Lounge/.test(b.label)));
  const lg = await A.press(/Go to the Lounge/); await sleep(3000);
  ok('won: "Go to the Lounge" pressed - into the Lounge, off the heist', !!lg && /gutter/.test(await dim()) && !(await passes('execute if entity @a[name=TestRat,tag=bm.gvp]')),
     `${!!lg} ${await dim()}`);
  await sleep(2000);
  ok('...Emma still away while TestRat is in the Lounge', (await emma()) === 0);
  // ---- out through the Lounge's door
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1,distance=0..] at @s run tp TestRat ~ ~ ~');
  ok('out through the Lounge\'s door: home', await wait(8000, async () => /overworld/.test(await dim()), 300), await dim());
  A.stand();
  ok('...and Emma comes back to TestRat', await wait(10000, async () => (await emma()) === 1, 400), `${await emma()}`);
  return done();

  async function done() {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    for (const f of ['plan_safe', 'heist_hard_any']) await run(`function bm:admin/${f}`);
    await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home');
    await KILL(); await run('tag TestRat remove bm.ow_emma');
    await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}tp TestRat 13000.5 120 13000.5`);
    const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
    A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
  }
})().catch(e => { console.error(e); process.exit(1); });
