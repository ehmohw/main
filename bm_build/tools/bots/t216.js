// 2.82n: NO WAY BACK, THE CREW FLARE, ADVENTURE IN THE LOCKER HALL - two regular (non-op) players TestRat (leader) and TestMouse,
// every step a real packet (rcon sets the stage: a party, Tokens, the Ledger, a room solved, the heist won, a raider put where
// they shouldn't be).
//   LOCKER HALL: both raiders go through to it; a raider found in survival in there is in adventure within a second.
//   FLARE: every kit carries one; before BEGIN it won't burn. Once the heist is on: TestMouse's flare takes them to TestRat;
//   sneak + flare, to the hall before the room ahead (the checkpoint).
//   NO WAY BACK: a solved room's entrance is barred as its exit opens.
//   THE WON VAULT: its entrance is barred; a raider who gets out into the old rooms is put back in the treasury.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const G = 'execute in bm:gutter run ';
  const passes = async c => /passed/i.test(await run(c));
  const have = async (who, item) => { const o = await run(`clear ${who} ${item} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const WC = 'minecraft:wind_charge[minecraft:custom_data~{bm_kit:1b}]';
  const POT = 'minecraft:splash_potion[minecraft:custom_data~{bm_kit:1b}]';
  const NAMES = ['TestRat', 'TestMouse'];

  const A = await bot('TestRat'); await sleep(1500); const M = await bot('TestMouse'); await sleep(2000);
  A.stand(); M.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); M.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player (and so is TestMouse)', /unknown|incomplete|permission/i.test(A.chats.join(' ')));

  // ---- the stage: no heist running, a party of two led by TestRat
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_anywhere', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never', 'rooms_only_levers']) await run(`function bm:admin/${f}`);
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone');
  for (const [i, n] of NAMES.entries()) {
    await run(`clear ${n}`); await run(`gamemode survival ${n}`); await run(`effect give ${n} resistance 900 4 true`); await run(`effect give ${n} saturation 900 0 true`);
    await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`);
    await run(`execute as ${n} unless score @s bm.pid matches 1.. run function bm:p21/pid`);
    await run(`execute in minecraft:overworld run tp ${n} ${13000.5 + i} 120 13000.5`);
    for (let k = 0; k < 16; k++) await run(`loot give ${n} loot bm:items/token`);
    await run(`scoreboard players set ${n} bm.gvu 5`); await run(`scoreboard players set ${n} bm.gval 1`);
  }
  for (const n of NAMES) await run(`scoreboard players operation ${n} bm.pty = TestRat bm.pid`);
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger');
  await sleep(2000);
  const gvi = n => num(`scoreboard players get ${n} bm.gvi`);
  const mode = async (n, m) => passes(`execute if entity @a[name=${n},gamemode=${m}]`);
  const pos = async n => (await run(`data get entity ${n} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  const FL = '*[minecraft:custom_data~{bm:"crew_flare"}]';
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7601'); await sleep(1500); A.cmd('trigger bm.act set 7613'); await sleep(1500);
  if (M.buttons().length) await M.press(/I'm in|Join|opt in|Count me in/i);
  const in1 = await wait(40000, async () => (await gvi('TestRat')) >= 1 && (await gvi('TestMouse')) === (await gvi('TestRat')), 500);
  const GI = await gvi('TestRat');
  ok('a heist planned through the Ledger: both raiders in its den', in1, `gvi ${GI}`);

  // ---- the Locker Hall
  for (const n of NAMES) await run(`execute as ${n} at @s run function bm:p84/lk/from_den`);
  await sleep(1500);
  const both = (await mode('TestRat', 'adventure')) && (await mode('TestMouse', 'adventure'));
  await run('gamemode survival TestMouse');                                   // (the stage: the slip as reported)
  const back = await wait(1500, () => mode('TestMouse', 'adventure'), 100);
  ok('Locker Hall: both raiders in adventure; one found in survival in there is in adventure again within a second', both && back);
  const LB = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},limit=1]`;
  for (const n of NAMES) await run(`execute in bm:gutter as ${LB} at @s run tp ${n} ~8 ~ ~3 -90 0`);
  await sleep(1500);

  // ---- the flare: in every kit, and dead before BEGIN
  for (const [n, r] of [['TestRat', 2], ['TestMouse', 4]]) { await run(`scoreboard players set ${n} bm.gvrole ${r}`); await run(`execute as ${n} run function bm:p72/kit/give_${r}`); }
  await sleep(500);
  const toHand = async (who, item, sl) => {
    let src = -1; for (let i = 0; i < 36 && src < 0; i++) if (await passes(`execute if items entity ${who} container.${i} ${item}`)) src = i;
    if (src >= 0 && src !== sl) { await run(`item replace entity ${who} hotbar.${sl} from entity ${who} container.${src}`); await run(`item replace entity ${who} container.${src} with minecraft:air`); }
  };
  const has = (await have('TestRat', FL)) === 1 && (await have('TestMouse', FL)) === 1;
  await toHand('TestMouse', FL, 8); M.slot(8); await sleep(300);
  const p0 = await pos('TestMouse'); M.bars.length = 0;
  M.use(); await sleep(300); M.release(); await sleep(800);
  const p1 = await pos('TestMouse');
  ok('every kit carries a Crew Flare; before BEGIN it won\'t burn', has && Math.hypot(p1[0] - p0[0], p1[2] - p0[2]) < 1 && M.bars.some(b => /under way/.test(b)), M.bars.slice(-1).join(''));
  // BEGIN, by TestRat's own press
  const lp = (await run(`${G}data get entity ${LB} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [bx, by, bz] = [Math.floor(+lp[1]) + 11, Math.floor(+lp[2]) + 1, Math.floor(+lp[3]) + 3];
  await run(`execute in bm:gutter as ${LB} at @s run tp TestRat ~10 ~ ~3 -90 0`); await sleep(1500);
  const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
  for (let k = 0; k < 3 && (await num(`${G}scoreboard players get ${inst} bm.gvst`)) < 2; k++) { A.useOn(bx, by, bz, 4); await sleep(2600); }
  const begun = (await num(`${G}scoreboard players get ${inst} bm.gvst`)) >= 2;
  // TestRat goes on ahead (the stage), TestMouse flares
  const room = `@e[type=minecraft:marker,tag=bm.gvr_levers,scores={bm.gvi=${GI}},sort=nearest,limit=1]`;
  await run(`${G}execute as ${room} at @s run tp TestRat ~ ~ ~ -90 0`); await sleep(21000);  // (the flare's cooldown since the dud)
  M.use(); await sleep(300); M.release(); await sleep(1000);
  const [rx, , rz] = await pos('TestRat'); const [mx, , mz] = await pos('TestMouse');
  ok('BEGIN pressed; TestRat on ahead: TestMouse\'s flare takes them to TestRat', begun && Math.hypot(rx - mx, rz - mz) < 2, `rat ${rx},${rz} mouse ${mx},${mz}`);
  await run(`${G}execute as ${inst.replace('gvinst', 'gvinst')} run tp @e[type=minecraft:marker,tag=bm.gvcp,scores={bm.gvi=${GI}}] @s`.replace(inst, inst) ) ;
  const cp = (await run(`${G}data get entity @e[type=minecraft:marker,tag=bm.gvcp,scores={bm.gvi=${GI}},limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  await sleep(20500);
  M.input({ shift: true }); await sleep(300); M.use(); await sleep(300); M.release(); await sleep(300); M.input({}); await sleep(900);
  const [cx, , cz] = await pos('TestMouse');
  ok('...sneak + flare: to the hall before the room ahead (the checkpoint)', Math.hypot(cx - cp[0], cz - cp[2]) < 2, `mouse ${cx},${cz} checkpoint ${cp[0]},${cp[2]}`);

  // ---- no way back: the room is solved (the stage) - exit open, entrance barred
  await run(`${G}execute as ${room} at @s run function bm:p70/solved`); await sleep(500);
  const exitOpen = await passes(`${G}execute as ${room} at @s unless block ~12 ~ ~ minecraft:iron_bars`);
  const entBar = await passes(`${G}execute as ${room} at @s if block ~-12 ~ ~ minecraft:iron_bars`);
  ok('a solved room: its exit opens and its entrance is barred behind the crew', exitOpen && entBar);

  // ---- the won vault (the stage: the heist won and paid)
  const VM = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
  for (const n of NAMES) await run(`${G}execute as ${VM} at @s run tp ${n} ~18 ~ ~ -90 0`);
  await sleep(1000);
  await run(`${G}execute as ${inst} at @s run function bm:p70/payout_inst`); await sleep(1500);
  const vBar = await passes(`${G}execute as ${VM} at @s if block ~-12 ~ ~ minecraft:iron_bars`);
  await run(`${G}execute as ${room} at @s run tp TestMouse ~ ~ ~`);           // (the stage: TestMouse slips out into an old room)
  const home = await wait(3000, async () => passes(`${G}execute as ${VM} at @s positioned ~-12.5 ~-2 ~-12.5 if entity @a[name=TestMouse,dx=37,dy=20,dz=25]`), 250);
  ok('the heist won: the vault\'s entrance barred, and a raider out in the old rooms is put back in the treasury', vBar && home, `bars ${vBar} back ${home}`);

  // ---- clean up
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'rooms_any', 'plan_safe']) await run(`function bm:admin/${f}`);
  for (const n of NAMES) { await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`); await run(`scoreboard players reset ${n} bm.pty`);
    await run(`scoreboard players set ${n} bm.ksec 0`); await run(`clear ${n}`); await run(`effect clear ${n}`); await run(`gamemode survival ${n}`);
    await run(`execute in minecraft:overworld run tp ${n} 13000.5 120 13000.5`); }
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); M.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
