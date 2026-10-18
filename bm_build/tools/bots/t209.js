// 2.82f: KIT GOLDEN APPLES BACK FOR ANOTHER JOB, AND LIGHTS OUT ON THE BAR - as a regular (non-op) player TestRat, every step a real
// packet (rcon sets the stage: TestRat's tank kit at rank 2, the Ledger and Tokens, the next heist's modifiers).
//   THE APPLES: TestRat eats one of the kit's golden apples (a real right-click), plans another Tier III heist through the Ledger's
//   buttons as sent, and walks into its den with the kit's apples topped back up - the kit rank's own count, no more.
//   LIGHTS OUT: a Lights Out heist's bar (as the client receives it) says LIGHTS OUT; without it, it doesn't.
//   (The roll itself - about 1 Tier III heist in 20 now - is measured from the built function in the checks, not here.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const GAP = 'minecraft:golden_apple[minecraft:custom_data~{bm_kit:1b}]';
  const apples = async () => { const o = await run(`clear TestRat ${GAP} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  const bars = []; A.on('boss_bar', p => { try { bars.push(Buffer.from(p.data && p.data.data ? p.data.data : p.data).toString('latin1')); } catch (e) { bars.push(String(p)); } });   // (the title's text, raw)
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  // ---- the stage: no heist running, the tank kit at rank 2, the Ledger, Tokens
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await sleep(2000);
  const menu = async () => num('scoreboard players get TestRat bm.menu');
  const slot = async () => num('scoreboard players get TestRat bm.gvi');
  const plan = async (from = -99) => {                                                  // the Ledger's buttons, as sent: Tier III, 7 tries
    A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    return wait(40000, async () => /passed/.test(await run('execute if entity @a[name=TestRat,tag=bm.gvp]')) && (await slot()) !== from, 500); };
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  const in1 = await plan(); await sleep(2000);
  const GI1 = await num('scoreboard players get TestRat bm.gvi');
  ok('a Tier III heist planned through the Ledger: TestRat is in its den', in1, `gvi ${GI1}`);

  // ---- the tank kit (rank 2) - the stage - and TestRat eats one of its golden apples
  await run('scoreboard players set TestRat bm.gvrole 2'); await run('scoreboard players set TestRat bm.kr2 2'); await run('execute as TestRat run function bm:p72/kit/give_2');
  const full = await apples();
  ok('the tank kit (rank 2) carries its golden apples', full >= 1, `${full}`);
  let src = -1; for (let i = 0; i < 36 && src < 0; i++) if (/passed/.test(await run(`execute if items entity TestRat container.${i} ${GAP}`))) src = i;
  if (src !== 8) { await run(`item replace entity TestRat hotbar.8 from entity TestRat container.${src}`); await run(`item replace entity TestRat container.${src} with minecraft:air`); }
  A.slot(8); await sleep(300); A.use(); await sleep(2200); A.release(); await sleep(500);
  const ate = await apples();
  ok('...TestRat eats one (a real right-click)', ate === full - 1, `${full} -> ${ate}`);

  // ---- the heist ends (the stage: its own "home, or another job?"), and TestRat presses Start a new raid
  A.chats.length = 0;
  for (let i = 0; i < 8; i++) await run('loot give TestRat loot bm:items/token');           // (the stage: the heist's winnings)
  await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI1}}] run scoreboard players set @s bm.gvst 4`);   // (paid out)
  await run(`execute as TestRat at @s run function bm:p101/s${GI1 - 1}/ask`); await sleep(1000);
  const sn = await A.press(/Start a new raid/); await sleep(1500);
  ok('the heist-over dialog offers Start a new raid, and TestRat presses it', !!sn);
  A.chats.length = 0; const in2 = await plan(GI1); await sleep(2500);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const after = await apples();
  ok('Start a new raid: into the new den with the kit\'s golden apples topped back up (the rank\'s own count, no more)', in2 && GI !== GI1 && after === full,
     `in den ${in2}, heist ${GI1} -> ${GI}, apples ${ate} -> ${after} (kit gives ${full}) ${A.chats.slice(-3).join(' / ').slice(0, 300)}`);

  // ---- Lights Out on the bar
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players set @s bm.gvmod 1`);
  bars.length = 0;                                                                      // (a heist's modifiers are rolled as it's made, and its bar named then:
  await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} at @s run function bm:p70/bar`);   //  the stage swaps them in, so the bar is named again)
  await wait(4000, async () => bars.some(b => /LIGHTS OUT/.test(b)), 300);
  const st = await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s bm.gvst`);
  ok('a Lights Out heist: its bar (as the client receives it) says LIGHTS OUT', bars.some(b => /LIGHTS OUT/.test(b)), `${st.slice(-40)} | ${bars.length} bar packets ${(bars.slice(-1)[0] || '').replace(/[^ -~]/g, '.').slice(0, 160)}`);
  await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players set @s bm.gvmod 0`); bars.length = 0;
  await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} at @s run function bm:p70/bar`); await sleep(1200);
  ok('...and without it, the bar doesn\'t', bars.length > 0 && !bars.some(b => /LIGHTS OUT/.test(b)), `${bars.length} bar packets`);

  // ---- clean up
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
