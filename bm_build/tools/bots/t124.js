// 2.75: the bank's exchange both ways; chatter in follower menus; modifiers at BEGIN
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const fs = require('fs'); const OUT = BMB + 'out_p2/BlackMarket_DP/data/bm/function/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const A = await bot('TestRat'); await sleep(2500);
  const num = H.num;
  const items = async (pred) => { const s = await run(`clear TestRat ${pred} 0`); const m = s.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const sc = async o => num(`scoreboard players get TestRat ${o}`);
  const act = async code => { await run('scoreboard players set TestRat bm.menu 7802'); await run(`scoreboard players set #act bm.pay ${code}`); await run('execute as TestRat at @s run function bm:p80/act'); await sleep(250); };
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/fixers_ledger');
  for (const o of ['bm.gbc', 'bm.gbm', 'bm.gbt']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.gbc 300');
  await act(7875); ok('16 coins -> a Medallion (kept in the account)', (await sc('bm.gbm')) === 1 && (await sc('bm.gbc')) === 300);
  await act(7876); ok('128 coins -> a Trophy', (await sc('bm.gbt')) === 1);
  await act(7877); ok('A Medallion -> 16 coins (loose again)', (await sc('bm.gbm')) === 0 && (await sc('bm.gbc')) === 300);
  await act(7883); ok('A Trophy -> 8 Medallions', (await sc('bm.gbt')) === 0 && (await sc('bm.gbm')) === 8);
  await act(7879); ok('8 Medallions -> a Trophy', (await sc('bm.gbt')) === 1 && (await sc('bm.gbm')) === 0);
  await act(7878); ok('A Trophy -> 128 coins', (await sc('bm.gbt')) === 0 && (await sc('bm.gbc')) === 300);
  // bought by mistake: one in your pocket changes back
  await run('loot give TestRat loot bm:items/gutter_trophy'); await run('loot give TestRat loot bm:items/gutter_medallion');
  await act(7878); ok('A Trophy in your pocket -> 128 coins', (await items('*[minecraft:custom_data~{bm:"gutter_trophy"}]')) === 0 && (await sc('bm.gbc')) === 428);
  await act(7877); ok('A Medallion in your pocket -> 16 coins', (await items('*[minecraft:custom_data~{bm:"gutter_medallion"}]')) === 0 && (await sc('bm.gbc')) === 444);
  await run('scoreboard players set TestRat bm.gbc 10'); A.chats.length = 0;
  await act(7875); ok('Not enough loose coins: it says so, nothing changes', (await sc('bm.gbm')) === 0 && A.chats.some(c => /16 loose coins/.test(c)));
  const cd = fs.existsSync(OUT + 'p80/bank_cdlg.mcfunction') ? fs.readFileSync(OUT + 'p80/bank_cdlg.mcfunction', 'utf8') : '',   // (2.80: the coins page went with the Rat Bank's rework)
    bk = fs.readFileSync(OUT + 'p120/bk_dlg.mcfunction', 'utf8');
  ok('"Take out coins" is coins only; the exchange lives on the Medallions & Trophies page', !/set 7857/.test(cd) && !/set 7858/.test(cd) && /set 7875/.test(bk) && /set 7883/.test(bk));
  // chatter from a follower's menu
  await run('tag TestRat remove bm.hush'); await run('scoreboard players set TestRat bm.menu 9920');
  A.cmd('trigger bm.act set 7735'); await sleep(700);
  ok('Chatter from Leo\'s menu: off for all followers', /bm.hush/.test(await run('tag TestRat list')));
  A.cmd('trigger bm.act set 7735'); await sleep(700);
  ok('...and on again', !/bm.hush\b/.test(await run('tag TestRat list')));
  ok('Every follower\'s menu has the switch', ['emma', 'celi', 'zib', 'cecil', 'kw', 'leo', 'demo'].every(w => /set 7735/.test(fs.readFileSync(OUT + `p99/dlg/${w}.mcfunction`, 'utf8'))));
  // modifiers at BEGIN
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  await H.heist('levers', 'a', 1); await sleep(500);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  await run(`execute in bm:gutter run scoreboard players set @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1] bm.gvmod 17`);
  A.chats.length = 0; await run(`scoreboard players set #gi bm.rng ${GI}`); await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},limit=1] at @s run function bm:p70/begin`); await sleep(1000);
  ok('BEGIN reads out the modifiers', A.chats.some(c => /Tonight's modifiers/.test(c)) && A.chats.some(c => /Glass Cannon/.test(c)) && A.chats.some(c => /Lights Out/.test(c)), A.chats.slice(-4).join(' | ').slice(0, 200));
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
