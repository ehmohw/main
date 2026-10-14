// 2.74: the Fixer's Lounge; Leo's size
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const A = await bot('TestRat'); await sleep(2500);
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter if entity ${sel}`); return /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0; };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await run('execute in minecraft:overworld run fill 12998 120 12998 13002 120 13002 stone'); await sleep(2500);
  await run('loot give TestRat loot bm:items/fixers_ledger');
  // ---- the Ledger: the Office has the button; the hold, then the lounge
  await run('execute as TestRat at @s run function bm:p80/office'); await sleep(300);
  const od = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p80/office_dlg.mcfunction', 'utf8');
  ok('The Office has a Fixer\'s Lounge button', /Fixer's Lounge/.test(od) && /set 7880/.test(od));
  await run('scoreboard players set TestRat bm.menu 7800'); await run('scoreboard players set #act bm.pay 7880'); await run('execute as TestRat at @s run function bm:p80/act');
  await sleep(4500);
  const p = await pos();
  ok('Hold still 3 seconds: into the Fixer\'s Lounge (bm:gutter)', p && Math.abs(p[0] + 315.5) < 3 && Math.abs(p[2] + 243.5) < 3 && /gutter/.test(await run('data get entity TestRat Dimension')), `${p}`);
  await sleep(1500);
  ok('...adventure mode while there', /adventure/i.test(await run('data get entity TestRat playerGameType')) || /2/.test(await run('data get entity TestRat playerGameType')));
  ok('...nobody sends you home from it (still there after 3 s)', (await pos())[0] < -290);
  const M = '-307.5 68 -243.5';
  for (const [tg, nm] of [['bm.gvgt', 'Goldtooth'], ['bm.gvrec', 'the Recruiter'], ['bm.gvtail', 'the Tailor']])
    ok(`${nm} at the counter`, (await cnt(`@e[type=minecraft:villager,tag=${tg},x=-321,y=60,z=-257,dx=26,dy=20,dz=26]`)) === 1);
  for (const [tg, nm] of [['bm.of_bank', 'the Gutter Bank'], ['bm.of_arm', 'the Armory'], ['bm.ofcrew', 'the Raid Crew board'], ['bm.gvthsel', 'the Crate Desk'], ['bm.tailhit', 'the Tailor\'s counter'], ['bm.lkdoor', 'the Locker Hall door']])
    ok(`${nm} works here`, (await cnt(`@e[type=minecraft:interaction,tag=${tg},x=-321,y=60,z=-257,dx=26,dy=20,dz=26]`)) === 1);
  ok('...the Scrap Box too', (await cnt('@e[type=minecraft:marker,tag=bm.gvscrap,x=-321,y=60,z=-257,dx=26,dy=20,dz=26]')) === 1);
  ok('No loaner racks, no BEGIN buttons', (await cnt('@e[tag=bm.gvkithit,x=-321,y=60,z=-257,dx=26,dy=20,dz=26]')) === 0 && !/passed/.test(await run('execute in bm:gutter if block -296 69 -240 minecraft:pale_oak_button')));
  // the bank, without a Ledger in hand
  await run('clear TestRat *[minecraft:custom_data~{bm:"fixers_ledger"}]');
  await run('execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.of_bank,limit=1] run data modify entity @s interaction set value {player:[I;0,0,0,0],timestamp:0L}');
  await run('execute as TestRat run function bm:p80/bank'); await sleep(300);
  ok('The bank\'s page works without a Ledger in hand (p80/can)', /returned 1/.test(await run('execute as TestRat run function bm:p80/can')));
  // ---- the Fixer's Door: back where you came from
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(1500);
  const p2 = await pos();
  ok('The Fixer\'s Door: back home where you stood', p2 && Math.abs(p2[0] - 13000.5) < 1.5 && /overworld/.test(await run('data get entity TestRat Dimension')), `${p2}`);
  await sleep(1500);
  ok('...survival again', /survival/i.test(await run('data get entity TestRat playerGameType')) || /: 0/.test(await run('data get entity TestRat playerGameType')));
  // ---- the end-of-heist choices
  const ad = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p101/ask_dlg.mcfunction', 'utf8');
  const md = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p103/mem_dlg.mcfunction', 'utf8');
  const of = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p103/offer_show.mcfunction', 'utf8');
  ok('End of a heist: the leader, a waiting member and an asked member can all Go to the Lounge', /Go to the Lounge/.test(ad) && /set 7730/.test(ad) && /set 7731/.test(md) && /set 7732/.test(of));
  // a leader's Go to the Lounge, simulated: send_home then the lounge
  await run('tag TestRat add bm.gvask'); await run('scoreboard players set TestRat bm.gvnx 1'); await run('tag TestRat add bm.gvp'); await run('scoreboard players set TestRat bm.gvi 1');
  await run('scoreboard players set #act bm.pay 7730'); await run('execute as TestRat at @s run function bm:p28/act'); await sleep(1500);
  const p3 = await pos();
  ok('Leader picks Go to the Lounge: the heist ends, into the lounge', p3 && p3[0] < -290 && !/bm.gvp/.test(await run('tag TestRat list')), `${p3}`);
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(1500);
  ok('...and its door takes you home', /overworld/.test(await run('data get entity TestRat Dimension')));
  // ---- Leo: bigger than Emma
  const fs = require('fs'); const art = fs.readFileSync(BMB + 'phase96_art.py', 'utf8'); const em = fs.readFileSync(BMB + 'phase57_art.py', 'utf8');
  const ls = +art.match(/^RIG_SCALE = ([\d.]+)/m)[1], es = +em.match(/^RIG_SCALE = ([\d.]+)/m)[1];
  const lh = (26 + 8 * 0.84) * ls / 16, eh = (24 + 10) * es / 16;
  ok(`Leo now stands ${lh.toFixed(2)} blocks to Emma's ${eh.toFixed(2)}`, lh > eh + 0.1);
  await run('function bm:admin/give/leo').catch(() => {});
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
