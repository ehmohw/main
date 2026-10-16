// v2.67d: the vault smoothed out - the way out asks first mid-run (instant otherwise); the crew needn't wait on the leader
// (head home now / I'm in if we go again); a leader who doesn't choose passes the choice on (not when solo); the Ledger reopens it
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16200, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2000); const B = await bot('TestMouse'); await sleep(2000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (who, pred) => { const o = await run(`clear ${who} ${pred} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const setToks = async (who, n) => { await run(`clear ${who} *[minecraft:custom_data~{bm:"token"}]`); for (let i = 0; i < n; i++) await run(`loot give ${who} loot bm:items/token`); };
  const tags = async who => await run(`data get entity ${who} Tags`);
  const has = async (who, t) => new RegExp(`"${t.replace('.', '\\.')}"`).test(await tags(who));
  const dim = async who => (await run(`data get entity ${who} Dimension`)).replace(/.*data: /, '');
  const act = async (who, code) => { await run(`scoreboard players set ${who} bm.act ${code}`); await sleep(500); };
  const until = async (f, ms = 6000) => { for (let t = 0; t < ms; t += 250) { if (await f()) return true; await sleep(250); } return !!(await f()); };
  const inst = async who => `@e[type=marker,tag=bm.gvinst,scores={bm.gvi=${await sc('bm.gvi', who)}},limit=1]`;
  const setSt = async (who, st) => run(`execute in bm:gutter as ${await inst(who)} run scoreboard players set @s bm.gvst ${st}`);
  const win = async who => { const gi = await sc('bm.gvi', who);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run function bm:p70/payout`); };
  const toExit = async who => { await run(`execute as ${who} at @s run tp @s @e[type=marker,tag=bm.exitm,limit=1,sort=nearest]`); await sleep(400); };
  const offExit = async who => { await run(`execute as ${who} at @s run tp @s ~3 ~ ~3`); await sleep(400); };
  const home = async () => { for (const p of ['TestRat', 'TestMouse']) { if (await has(p, 'bm.gvp')) await run(`execute as ${p} at @s run function bm:p70/leave`); }
    await sleep(2500);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await sleep(800); };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
  for (const p of ['TestRat', 'TestMouse']) {
    await run(`gamemode survival ${p}`); await run(`clear ${p}`); await run(`effect clear ${p}`);
    await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); await run(`execute as ${p} run function bm:p80/init_me`);
    for (const o of ['bm.crew', 'bm.crewoff', 'bm.fcon', 'bm.gvhc']) await run(`scoreboard players set ${p} ${o} 0`);
    for (const t of ['bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvin', 'bm.gvwait', 'bm.gvp', 'bm.gvwaitd', 'bm.gvpre', 'bm.exon', 'bm.exask']) await run(`tag ${p} remove ${t}`);
  }
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await sleep(1200);
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestMouse bm.pty = TestRat bm.pid');
  await setToks('TestRat', 40); await setToks('TestMouse', 20);
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  const plan = async (tier = 1, lives = 7613) => {
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };

  // ---- 1. the way out asks first while the heist is on
  await plan(1);
  ok('In: both', (await has('TestRat', 'bm.gvp')) && (await has('TestMouse', 'bm.gvp')));
  await setSt('TestMouse', 2);
  await toExit('TestMouse');
  ok('Mid-heist, stepping into the way out: the Fixer asks first (still in)', (await has('TestMouse', 'bm.exask')) && /gutter/.test(await dim('TestMouse')) && (await has('TestMouse', 'bm.gvp')));
  await act('TestMouse', 7725);
  ok('"Stay": still in the heist', !(await has('TestMouse', 'bm.exask')) && (await has('TestMouse', 'bm.gvp')));
  await sleep(1000);
  ok('...standing there, it doesn\'t ask again', !(await has('TestMouse', 'bm.exask')) && (await has('TestMouse', 'bm.exon')));
  await offExit('TestMouse'); await toExit('TestMouse');
  ok('Step out and back in: it asks again', await has('TestMouse', 'bm.exask'));
  await act('TestMouse', 7724); await sleep(500);
  ok('"Leave now": home, out of the heist', /overworld/.test(await dim('TestMouse')) && !(await has('TestMouse', 'bm.gvp')));
  await act('TestMouse', 7724);
  ok('...a stale "Leave now" does nothing', /overworld/.test(await dim('TestMouse')));
  await setSt('TestRat', 1);
  await toExit('TestRat');
  ok('Before the heist begins: the way out is instant', /overworld/.test(await dim('TestRat')) && !(await has('TestRat', 'bm.gvp')));
  await home();

  // ---- 2. won: the crew needn't wait - "I'm in" ahead of time
  await plan(1); await win('TestRat');
  ok('Won: the leader is asked', await until(async () => has('TestRat', 'bm.gvask'), 8000));
  ok('...the member gets their own card - head home now, or in if we go again', (await has('TestMouse', 'bm.gvwaitd')) && B.chats.some(c => /Head home now/.test(c) && /I'm in if we go again/.test(c)));
  A.chats.length = 0;
  await act('TestMouse', 7727);
  ok('"I\'m in if we go again": the leader hears it', (await has('TestMouse', 'bm.gvpre')) && A.chats.some(c => /TestMouse is in if you go again/.test(c)));
  B.chats.length = 0;
  await act('TestRat', 7721);
  ok('The leader starts a new raid: the member is in already (not asked again)', (await has('TestMouse', 'bm.gvin')) && !(await has('TestMouse', 'bm.gvoffer')) &&
     !B.chats.some(c => /Count me in/.test(c)));
  const gi1 = await sc('bm.gvi');
  await plan(1);
  ok('...and both go into the new heist', (await sc('bm.gvi')) !== gi1 && (await sc('bm.gvi', 'TestMouse')) === (await sc('bm.gvi')) &&
     !(await has('TestMouse', 'bm.gvwaitd')) && !(await has('TestMouse', 'bm.gvpre')));

  // ---- 3. won: the member heads home at once (the leader still choosing)
  await win('TestRat');
  await until(async () => has('TestRat', 'bm.gvask'), 8000);
  A.chats.length = 0;
  await act('TestMouse', 7726); await sleep(500);
  ok('"Head home now": the member goes at once', /overworld/.test(await dim('TestMouse')) && !(await has('TestMouse', 'bm.gvp')) && (await has('TestRat', 'bm.gvask')));
  ok('...and the leader is told', A.chats.some(c => /TestMouse heads home/.test(c)));

  // ---- 4. the Ledger reopens the choice
  B.chats.length = 0; A.chats.length = 0;
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('scoreboard players set TestRat bm.menu 0');
  await run('execute as TestRat at @s run function bm:p80/ledger'); await sleep(300);
  ok('Closed the card? The Ledger opens the leader\'s choice again (not the Office)', A.chats.some(c => /Back to the Overworld/.test(c)) && (await sc('bm.menu')) !== 7800,
     `menu ${await sc('bm.menu')}`);

  // ---- 5. a solo leader takes as long as they like
  const s0 = (await sc('bm.gvi')) - 1;
  await run(`scoreboard players set #dt${s0} bm.gvdt 2`); await sleep(3500);
  ok('Solo: no time limit (still the leader\'s call)', (await has('TestRat', 'bm.gvask')));
  await act('TestRat', 7720); await sleep(500);
  await home();

  // ---- 6. a leader who doesn't choose: the choice passes on
  await plan(1); await win('TestRat');
  await until(async () => has('TestRat', 'bm.gvask'), 8000);
  const s1 = (await sc('bm.gvi')) - 1;
  ok('The leader\'s clock starts (75 s)', (await num(`scoreboard players get #dt${s1} bm.gvdt`)) > 60);
  A.chats.length = 0;
  await run(`scoreboard players set #dt${s1} bm.gvdt 2`);
  ok('Time\'s up: the choice passes to the crew', await until(async () => (await has('TestMouse', 'bm.gvask')) && !(await has('TestRat', 'bm.gvask')), 5000));
  ok('...the old leader is told, and gets the crew\'s card', A.chats.some(c => /Time's up/.test(c)) && (await has('TestRat', 'bm.gvwaitd')));
  B.chats.length = 0;
  await run('scoreboard players set TestMouse bm.gvhc 0'); await run('execute as TestMouse at @s run function bm:p80/ledger'); await sleep(300);
  ok('...and the new one can reopen it from the Ledger', B.chats.some(c => /Back to the Overworld/.test(c)));
  await act('TestMouse', 7720); await sleep(500);
  ok('The new leader calls it a night: both home', /overworld/.test(await dim('TestMouse')) && /overworld/.test(await dim('TestRat')));

  // ---- 7. the den, laid out by job
  const eidOf = async sel => { const m = (await run(`data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  await home(); await plan(1);
  const gi7 = await sc('bm.gvi');
  const lm = `@e[type=marker,tag=bm.gvr_lobby,scores={bm.gvi=${gi7}},limit=1]`;
  const mpos = []; for (let i = 0; i < 3; i++) mpos.push(+(await run(`execute in bm:gutter run data get entity ${lm} Pos[${i}]`)).replace(/.*data: /, '').replace('d', ''));
  const at = (x, y, z) => `${Math.floor(mpos[0] + x - 12)} ${Math.floor(mpos[1] + y - 4)} ${Math.floor(mpos[2] + z - 12)}`;
  const eidAt = async (tag, x, y, z) => { const [bx, by, bz] = at(x, y, z).split(' ');
    const m = (await run(`execute in bm:gutter run data get entity @e[type=interaction,tag=${tag},x=${+bx + 0.5},y=${by},z=${+bz + 0.5},distance=..2,limit=1] UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const isb = async (x, y, z, b) => !/failed/i.test(await run(`execute in bm:gutter if block ${at(x, y, z)} ${b}`));
  ok('Office counter: the Bank, the Armory, the haul lectern and the Raid Crew board side by side on the north wall',
     (await isb(16, 4, 2, 'minecraft:vault')) && (await isb(18, 4, 2, 'minecraft:smithing_table')) && (await isb(20, 4, 2, 'minecraft:lectern')) &&
     (await isb(22, 4, 2, 'minecraft:chiseled_bookshelf')));
  ok('...nothing left behind Goldtooth (the old Bank and Armory spots empty)', (await isb(5, 4, 21, 'minecraft:air')) && (await isb(7, 4, 21, 'minecraft:air')));
  const gt = await run(`execute in bm:gutter positioned ${mpos.join(' ')} run data get entity @e[type=villager,tag=bm.gvgt,sort=nearest,limit=1] Pos`);
  const gtr = await run(`execute in bm:gutter positioned ${mpos.join(' ')} run data get entity @e[type=villager,tag=bm.gvgt,sort=nearest,limit=1] Rotation[0]`);
  const gp = (gt.match(/-?[\d.]+d/g) || []).map(v => parseFloat(v));
  ok('Goldtooth stands behind his counter, facing the room', gp.length === 3 && Math.abs(gp[0] - (mpos[0] - 9)) < 0.6 && Math.abs(gp[2] - (mpos[2] + 8)) < 0.6 && /180/.test(gtr) &&
     (await isb(3, 4, 19, 'minecraft:dark_oak_planks')), `${gt} ${gtr}`);
  ok('The Lockers: a copper door on the north wall; the plate by the way out is gone', (await isb(8, 4, 1, 'minecraft:waxed_copper_door')) && (await isb(2, 4, 7, 'minecraft:air')));
  ok('"Back to the crew": a plate you can see, by the far door', (await isb(21, 3, 17, 'minecraft:emerald_block')) && (await isb(21, 4, 17, 'minecraft:polished_blackstone_pressure_plate')));
  // click the Raid Crew board, then the Lockers' door
  await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${at(22, 4, 4).split(' ').map((v, i) => +v + (i === 1 ? 0 : 0.5)).join(' ')} 180 20`); await sleep(1500);
  await run('scoreboard players set TestRat bm.menu 0');
  A.interact(await eidAt('bm.ofcrew', 22, 4, 2));
  await sleep(600);
  ok('Right-click the Raid Crew board: the Raid Crew page', (await sc('bm.menu')) === 7807, `${await sc('bm.menu')}`);
  await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${at(8, 4, 3).split(' ').map((v, i) => +v + (i === 1 ? 0 : 0.5)).join(' ')} 180 10`); await sleep(1500);
  A.interact(await eidAt('bm.lkdoor', 8, 4, 1));
  await sleep(900);
  const lx = +(await run('data get entity TestRat Pos[0]')).replace(/.*data: /, '').replace('d', '');
  ok('Right-click the Lockers\' door (before the heist begins): into the Locker Hall', lx > -256 && lx < -241, `${lx}`);
  await run('execute as TestRat at @s run function bm:p84/lk/to_den'); await sleep(600);

  // ---- 8. three shopkeepers
  const near = async (tag, path) => run(`execute in bm:gutter positioned ${mpos.join(' ')} run data get entity @e[type=villager,tag=${tag},sort=nearest,limit=1] ${path}`);
  const nOff = async tag => { await run(`execute in bm:gutter positioned ${mpos.join(' ')} store result score #t bm.rng run data get entity @e[type=villager,tag=${tag},sort=nearest,limit=1] Offers.Recipes`); return num('scoreboard players get #t bm.rng'); };
  const sells = async (tag, iid) => !/failed/i.test(await run(`execute in bm:gutter positioned ${mpos.join(' ')} if data entity @e[type=villager,tag=${tag},sort=nearest,limit=1] Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${iid}"}}}}]`));
  const ngt = await nOff('bm.gvgt');
  ok('Goldtooth: heist supplies only (no contracts, outfits, gems or coin-changing)', ngt >= 25 && ngt <= 40 && !(await sells('bm.gvgt', 'fcontract_cecil')) &&
     !(await sells('bm.gvgt', 'cos_ribbon_1')) && !(await sells('bm.gvgt', 'gem_fire')) && !(await sells('bm.gvgt', 'gutter_medallion')) && (await sells('bm.gvgt', 'smoke_bomb')), `${ngt} trades`);
  const nrc = await nOff('bm.gvrec');
  const RCD = require('path').join(__dirname, '..', '..', 'out_p2/BlackMarket_DP/data/bm/function/p137/rc');     // (2.78: his book - t145 plays it)
  const rcAll = require('fs').readdirSync(RCD).map(f => require('fs').readFileSync(`${RCD}/${f}`, 'utf8')).join('\n');
  ok('The Recruiter: no trades - his book sells the contracts and the vault gems', nrc === 0 && ['fcontract_cecil', 'contract_medic', 'gem_fire'].every(i => rcAll.includes(`bm:"${i}"`)), `${nrc} trades`);
  ok('The Tailor stands at the counter', /The Tailor/.test(await near('bm.gvtail', 'CustomName')));
  await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${at(7, 4, 17).split(' ').map((v, i) => +v + (i === 1 ? 0 : 0.5)).join(' ')} 180 0`); await sleep(1500);
  await run('scoreboard players set TestRat bm.menu 0');
  let te = null; for (let i = 0; i < 20 && !te; i++) { te = await eidAt('bm.tailhit', 7, 4, 20); if (!te) await sleep(250); }
  if (te) A.interact(te);
  else { const u = (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim(); const [bx, by, bz] = at(7, 4, 20).split(' ');   // (the bot's client lost sight of it: click it server-side, as TestRat)
    await run(`execute in bm:gutter run data merge entity @e[type=interaction,tag=bm.tailhit,x=${+bx + 0.5},y=${by},z=${+bz + 0.5},distance=..2,limit=1] {interaction:{player:${u},timestamp:1L}}`); }
  await sleep(600);
  ok('Right-click the Tailor: the Tailor\'s menu', (await sc('bm.menu')) === 7740, `${await sc('bm.menu')}`);
  for (const o of ['bm.wur', 'bm.wuc', 'bm.wuz', 'bm.wuleo']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"gutter_coin"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"gutter_medallion"}]');
  await run('scoreboard players set TestRat bm.gbc 200');
  B.chats.length = 0; A.chats.length = 0;
  await act('TestRat', 7750);
  ok('Buy Emma\'s first ribbon (48 coins from the bank): in her wardrobe for good', ((await sc('bm.wur')) & 2) === 2 && (await sc('bm.gbc')) === 152 &&
     A.chats.some(c => /wardrobe for good/.test(c)), `${await sc('bm.wur')} / ${await sc('bm.gbc')}`);
  await act('TestRat', 7750);
  ok('...again: it says it\'s owned, and charges nothing', (await sc('bm.gbc')) === 152 && A.chats.some(c => /wardrobe already/.test(c)));
  // pay with pocket coins and a Gutter Medallion, the change to the bank
  await run('scoreboard players set TestRat bm.gbc 0');
  for (let i = 0; i < 50; i++) await run('loot give TestRat loot bm:items/gutter_coin');
  await run('loot give TestRat loot bm:items/gutter_medallion');
  const zj = 7750 + 6 + 6 + 2 + 5;                // (Emma: 6 ribbons, 6 dresses (2.79a: the Gilded Gown), 2 outfits; Celi: 5 (her Gilded) - then Zib's first)
  await run('scoreboard players set TestRat bm.menu 7740'); await act('TestRat', zj);
  ok('Pockets pay too: 50 coins and a Medallion for 64 - the 2 change goes to the bank', ((await sc('bm.wuz')) & 2) === 2 &&
     (await cnt('TestRat', '*[minecraft:custom_data~{bm:"gutter_coin"}]')) === 0 && (await cnt('TestRat', '*[minecraft:custom_data~{bm:"gutter_medallion"}]')) === 0 &&
     (await sc('bm.gbc')) === 2, `zib ${await sc('bm.wuz')} bank ${await sc('bm.gbc')}`);
  await run('scoreboard players set TestRat bm.menu 7740'); await act('TestRat', 7750 + 14);
  ok('Not enough: "That\'s 64 coins - you have 2", nothing taken', ((await sc('bm.wuc')) & 2) === 0 && (await sc('bm.gbc')) === 2 && A.chats.some(c => /That's 64 coins - you have 2/.test(c)));
  await run('scoreboard players set TestRat bm.gbc 500'); await run('loot give TestRat loot bm:items/cos_leo_1');
  const lj = zj + 3;                              // (... Zib 3 - then Leo's first)
  await run('scoreboard players set TestRat bm.menu 7740'); await act('TestRat', lj);
  ok('Holding that outfit already: "use it", not sold again', ((await sc('bm.wuleo')) & 2) === 0 && (await sc('bm.gbc')) === 500 && A.chats.some(c => /You have that one/.test(c)));
  await run('scoreboard players set TestRat bm.menu 7740'); await act('TestRat', 7790);
  ok('Display cases at the Tailor: an oak case for 3 coins', (await cnt('TestRat', '*[minecraft:custom_data~{bm:"display_case_oak"}]')) === 1 && (await sc('bm.gbc')) === 497);
  const tcec = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p98/t/cecil.mcfunction', 'utf8');
  ok('Messages point to the Recruiter for contracts now', /The Recruiter in the den sells Raid Contracts/.test(tcec) && !/Goldtooth/.test(tcec));
  await run('clear TestRat'); await setToks('TestRat', 30); await run('loot give TestRat loot bm:items/fixers_ledger');
  await home();

  // ---- 9. the Raid Crew page: who's where, and who comes first
  await run('scoreboard players reset TestMouse bm.pty'); await run('scoreboard players reset TestRat bm.pty');
  for (const o of ['bm.cpcd', 'bm.emcd', 'bm.cecd', 'bm.zbcd', 'bm.kxcd', 'bm.lecd', 'bm.dmcd', 'bm.crewoff', 'bm.coq', 'bm.gvhr']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const k of ['cecil', 'emma', 'celi', 'zib', 'killerw', 'leo', 'demo', 'escort', 'frog', 'donado']) await run(`scoreboard players reset TestRat bm.co_${k}`);
  await run('scoreboard players reset TestRat bm.coq');
  await run('execute as TestRat run function bm:admin/contracts_all');
  await plan(1);
  const fcnt = async tag => num(`execute in bm:gutter store result score #t bm.rng if entity @e[tag=${tag},distance=0..]`).then(() => num('scoreboard players get #t bm.rng'));
  await until(async () => (await fcnt('bm.cecilpet')) + (await fcnt('bm.emmapet')) === 2, 8000);
  ok('Solo: the first two in line come (Cecil and Emma)', (await fcnt('bm.cecilpet')) === 1 && (await fcnt('bm.emmapet')) === 1);
  await run('scoreboard players set TestRat bm.menu 7807'); await act('TestRat', 7900); await sleep(3500);
  await run('scoreboard players set TestRat bm.menu 7807'); await act('TestRat', 7900); await sleep(2500);
  ok('Cecil off and on again: he goes to the back of the line - Celi comes, Cecil waits', (await fcnt('bm.cecilpet')) === 0 && (await fcnt('bm.emmapet')) === 1 && (await fcnt('bm.celipet')) === 1);
  const lbl = async (i, j) => (await run(`data get storage bm:ui crew.acts[${i}].label[${j}].text`)).replace(/^.*(data|contents): /, '').replace(/"/g, '');
  await run('execute as TestRat at @s run function bm:p98/crew'); await sleep(200);
  const r0 = [await lbl(0, 0), await lbl(0, 2)], r1 = [await lbl(1, 0), await lbl(1, 2)];
  // (every follower has a row now: Cecil, at the back, is far down)
  let cecilSt = ''; for (let i = 2; i < 24; i++) { if ((await lbl(i, 0)) === 'Cecil') { cecilSt = await lbl(i, 2); break; } }
  ok('The page: the ones in the vault first, in line order, each saying so', r0[0] === 'Emma' && r0[1] === 'IN THE VAULT' && r1[0] === 'Celi' && r1[1] === 'IN THE VAULT', `${r0} | ${r1}`);
  ok('...Cecil, at the back, says he\'s waiting (crew full)', /WAITING/.test(cecilSt), cecilSt);
  // (2.74: alone, THREE come along - Zib, next in line, took the third place when Cecil went to the back)
  ok('...and the header counts the crew (3/3 - alone, three come)', /: 3$/.test(await run('data get storage bm:ui crew.fc')) && /: 3$/.test(await run('data get storage bm:ui crew.lim')) && (await fcnt('bm.zibpet')) === 1,
     `${(await run('data get storage bm:ui crew.fc')).replace(/.*data: /, '')}/${(await run('data get storage bm:ui crew.lim')).replace(/.*data: /, '')}`);
  await run('execute in bm:gutter run kill @e[type=cat,tag=bm.emmapet,distance=0..]'); await sleep(2500);
  await run('execute as TestRat at @s run function bm:p98/crew'); await sleep(200);
  let emSt = ''; for (let i = 0; i < 24; i++) { if ((await lbl(i, 0)) === 'Emma') { emSt = await lbl(i, 2); break; } }
  ok('Emma faints: her row says RESTING, with the seconds left', /RESTING 4\ds/.test(emSt), emSt);
  await until(async () => (await fcnt('bm.kxpet')) === 1, 6000);
  ok('...and the next in line steps in (KillerWatt - before Cecil, who went to the back)', (await fcnt('bm.kxpet')) === 1 && (await fcnt('bm.cecilpet')) === 0);
  // (over the limit - a raider joining makes it one each - the bench sends home the one last in line)
  await run('execute as TestRat at @s run function bm:p103/crew/bench'); await sleep(500);
  ok('The bench sends home the one last in line (KillerWatt, not Celi or Zib)', (await fcnt('bm.kxpet')) === 0 && (await fcnt('bm.celipet')) === 1 && (await fcnt('bm.zibpet')) === 1,
     `kx ${await fcnt('bm.kxpet')} celi ${await fcnt('bm.celipet')} zib ${await fcnt('bm.zibpet')}`);
  await run('execute as TestRat run function bm:admin/contracts_none');
  for (const k of ['cecil', 'emma', 'celi', 'zib', 'killerw', 'leo', 'demo', 'escort', 'frog', 'donado']) await run(`scoreboard players reset TestRat bm.co_${k}`);
  await run('scoreboard players reset TestRat bm.coq');
  await home();

  // ---- 10. one card at the end
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestMouse bm.pty = TestRat bm.pid');
  await setToks('TestRat', 30); await setToks('TestMouse', 20);
  await plan(1);
  A.chats.length = 0; B.chats.length = 0;
  await win('TestRat');
  ok('Won: one line sums it up (no run of shares/pot/prize/crate lines)', A.chats.some(c => /Heist won! The Haul: \d+ Tokens, \d+ coins/.test(c)) &&
     !A.chats.some(c => /Your haul: |The pot: |The Fixer's prize|hands you The Haul/.test(c)), A.chats.filter(c => /Heist|haul|Haul/.test(c)).join(' | ').slice(0, 300));
  ok('...for the crew too', B.chats.some(c => /Heist won! The Haul:/.test(c)));
  const resOf = async who => { await run(`execute as ${who} run function bm:p103/res_load`); return run('data get storage bm:ui res.r_res'); };
  const rr = await resOf('TestRat');
  ok('The leader\'s card opens with how it went (won, the tier, shares, Tokens, coins)', /HEIST WON/.test(rr) && /Tier 1/.test(rr) && /shares/.test(rr) && /Tokens/.test(rr), rr.slice(0, 200));
  ok('...and the crew\'s card too', /HEIST WON/.test(await resOf('TestMouse')));
  ok('The end-of-heist card comes up three seconds after the payout', await until(async () => has('TestRat', 'bm.gvask'), 4500));
  await act('TestRat', 7721); await act('TestMouse', 7722); await plan(1);
  const I10 = await inst('TestRat');
  await run(`execute in bm:gutter as ${I10} run function bm:p70/tag_mine`); await run(`execute in bm:gutter as ${I10} run function bm:p75/fail`);
  await until(async () => has('TestRat', 'bm.gvask'), 9000);
  ok('Failed: the card says so', /HEIST FAILED/.test(await resOf('TestRat')) && /HEIST FAILED/.test(await resOf('TestMouse')));
  await act('TestRat', 7720); await sleep(800);
  const pidR = await sc('bm.pid');
  ok('...and it\'s cleared once you\'re home', /failed|not found|No /i.test(await run(`data get storage bm:gv res.p${pidR}`)) || !/HEIST/.test(await run(`data get storage bm:gv res.p${pidR}`)));
  await home();

  // ---- 11. followers wait outside the vault, and come back after; BEGIN's ready check
  await run('scoreboard players reset TestMouse bm.pty'); await run('scoreboard players reset TestRat bm.pty');
  await run('execute as TestRat run function bm:admin/contracts_none'); await run('scoreboard players set TestRat bm.cpcd 0'); await run('tag TestRat remove bm.ow_cecil');
  await run('loot give TestRat loot bm:items/cecil_gem'); await run('execute as TestRat at @s run function bm:p46/pet/try_summon'); await sleep(1200);
  const owc = async () => { await run('execute in minecraft:overworld store result score #t bm.rng if entity @e[type=wolf,tag=bm.cecilpet,distance=0..]'); return num('scoreboard players get #t bm.rng'); };
  ok('(Cecil out with TestRat in the Overworld)', (await owc()) === 1);
  A.chats.length = 0;
  await plan(1);
  await until(async () => has('TestRat', 'bm.ow_cecil'), 5000);
  ok('Into a heist: Cecil "waits outside the vault" (and is remembered)', (await has('TestRat', 'bm.ow_cecil')) && A.chats.some(c => /Cecil waits outside the vault/.test(c)) && (await owc()) === 0,
     A.chats.filter(c => /Cecil/.test(c)).join(' | '));
  await run('execute as TestRat at @s run function bm:p70/leave');
  ok('Home again: Cecil comes back to you', await until(async () => (await owc()) === 1, 7000) && !(await has('TestRat', 'bm.ow_cecil')));
  await run('execute as @e[type=wolf,tag=bm.cecilpet] at @s run function bm:p62/cecil_go'); await run('clear TestRat *[minecraft:custom_data~{bm:"cecil_gem"}]');
  await home();
  // BEGIN
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestMouse bm.pty = TestRat bm.pid');
  await plan(1);
  const giB = await sc('bm.gvi');
  const bm_ = `@e[type=marker,tag=bm.gvr_lobby,scores={bm.gvi=${giB}},limit=1]`;
  const press = async on => run(`execute in bm:gutter positioned as ${bm_} run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=${on}]`);
  const st = async () => num(`execute in bm:gutter run scoreboard players get ${await inst('TestRat')} bm.gvst`);
  await run('scoreboard players set TestRat bm.gvrole 1'); await run('scoreboard players reset TestMouse bm.gvrole');
  A.chats.length = 0;
  await press(true); await sleep(600);
  ok('BEGIN with TestMouse kitless: it names who isn\'t ready, and waits', (await st()) === 1 && A.chats.some(c => /Not everyone's ready: TestMouse/.test(c)), A.chats.slice(-1)[0]);
  await press(false); await sleep(2300); await press(true); await sleep(600);
  ok('...press again within ten seconds: off we go (TestMouse in the Offense kit)', (await st()) === 2 && (await sc('bm.gvrole', 'TestMouse')) === 2, `st ${await st()} role ${await sc('bm.gvrole', 'TestMouse')}`);
  await home();
  await plan(1);
  const giC = await sc('bm.gvi');
  await run('scoreboard players set TestRat bm.gvrole 1'); await run('scoreboard players set TestMouse bm.gvrole 3');
  await run(`execute in bm:gutter positioned as @e[type=marker,tag=bm.gvr_lobby,scores={bm.gvi=${giC}},limit=1] run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`); await sleep(600);
  ok('Everyone kitted: BEGIN starts it at once', (await st()) === 2);
  await home();

  // ---- 12. the Fixer's Door
  await run('scoreboard players reset TestMouse bm.pty'); await run('scoreboard players reset TestRat bm.pty');
  await plan(1);
  const gD = await sc('bm.gvi');
  const lmD = `@e[type=marker,tag=bm.gvr_lobby,scores={bm.gvi=${gD}},limit=1]`;
  const pD = []; for (let i = 0; i < 3; i++) pD.push(+(await run(`execute in bm:gutter run data get entity ${lmD} Pos[${i}]`)).replace(/.*data: /, '').replace('d', ''));
  const atD = (x, y, z) => `${Math.floor(pD[0] + x - 12)} ${Math.floor(pD[1] + y - 4)} ${Math.floor(pD[2] + z - 12)}`;
  const isD = async (x, y, z, b) => !/failed/i.test(await run(`execute in bm:gutter if block ${atD(x, y, z)} ${b}`));
  const METAL = '#bm:t105_metal';
  const metal = async (isf, x, y, z) => { for (const m of ['gold_block', 'waxed_copper_block', 'iron_block', 'diamond_block']) if (await isf(x, y, z, 'minecraft:' + m)) return true; return false; };
  ok('The den\'s Fixer\'s Door: an arch (in the tier\'s metal) in the west doorway, the old plate gone', (await metal(isD, 0, 4, 10)) && (await metal(isD, 0, 8, 12)) &&
     (await metal(isD, 0, 8, 11)) && (await isD(0, 5, 12, "minecraft:air")) && (await isD(1, 4, 12, "minecraft:air")));
  const swirlN = async () => { await run(`execute in bm:gutter positioned ${atD(0, 4, 12)} store result score #t bm.rng if entity @e[type=block_display,tag=bm.exdoor,distance=..2]`); return num('scoreboard players get #t bm.rng'); };
  ok('...with the swirl in it', (await swirlN()) === 1);
  await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${atD(0, 4, 12).split(' ').map((v, i) => +v + (i === 1 ? 0 : 0.5)).join(' ')}`); await sleep(600);
  ok('Walk into it (before the heist begins): home', /overworld/.test(await dim('TestRat')) && !(await has('TestRat', 'bm.gvp')));
  await home(); await plan(1);
  const gV = await sc('bm.gvi');
  const vm = `@e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gV}},limit=1]`;
  const pV = []; for (let i = 0; i < 3; i++) pV.push(+(await run(`execute in bm:gutter run data get entity ${vm} Pos[${i}]`)).replace(/.*data: /, '').replace('d', ''));
  const atV = (x, y, z) => `${Math.floor(pV[0] + x - 12)} ${Math.floor(pV[1] + y - 4)} ${Math.floor(pV[2] + z - 12)}`;
  const doorV = async () => { await run(`execute in bm:gutter positioned ${atV(35, 4, 12)} store result score #t bm.rng if entity @e[type=marker,tag=bm.exitm,distance=..1.5]`); return num('scoreboard players get #t bm.rng'); };
  const isV = async (x, y, z, bl) => !/failed/i.test(await run(`execute in bm:gutter if block ${atV(x, y, z)} ${bl}`));
  ok('The treasury\'s door: an arch against the far wall, shut till the vault opens', (await metal(isV, 35, 7, 12)) &&
     (await doorV()) === 0 && !/failed/i.test(await run(`execute in bm:gutter if block ${atV(34, 4, 12)} minecraft:air`)));
  await run(`execute in bm:gutter as ${vm} at @s run function bm:p70/r/vault/open`); await sleep(300);
  ok('...the vault opens (2.80: its great door parting, a second or two): the door swirls', await wait(4000, async () => (await doorV()) === 1));
  await win('TestRat'); await sleep(800);
  await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${atV(35, 4, 12).split(' ').map((v, i) => +v + (i === 1 ? 0 : 0.5)).join(' ')}`); await sleep(700);
  ok('Won: through the door, home - the haul with you', /overworld/.test(await dim('TestRat')) && !(await has('TestRat', 'bm.gvp')));
  await sleep(2500);
  await home();

  for (const p of ['TestRat', 'TestMouse']) await run(`scoreboard players reset ${p} bm.pty`);
  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });
