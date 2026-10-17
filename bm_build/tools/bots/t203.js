// 2.82b: THE PRESSES - the Counterfeiter's Press's lucky plates, and the three mythical presses - as a regular (non-op) player
// TestRat, every step a real packet (rcon sets the stage: the presses in hand, a floor, and the days gone by).
//   THE COUNTERFEITER'S PRESS: used on the floor - set down, the item spent; right-clicked the same day - "the ink's still wet";
//   a week on - seven days of printing. Four hundred and twenty days of printing later: mostly Tokens, now and then a Medallion
//   (about 1 day in 25), a Trophy only rarely (about 1 in 200) - and never more than one thing a day.
//   THE BLOOD PRESS, THE XENITE PRESS, THE LUCKY PRESS: each set down beside the first (one of each per crook - a second Blood Press
//   is refused); a week on, right-clicked: 14 Blood Crystals; 14 Green Xenite (and maybe a rarer shard); 7 Lucky Tokens.
//   Sneak + punch: folded up and back in the pack.
//   Where they come from: a won Blood Moon heist rolls for the Blood Press, an Invasion heist for the Xenite Press, a Lucky
//   heist for the Lucky Press - 6% each, every raider (higher than the 1% Counterfeiter's, as those heists come round seldom).
const fs = require('fs');
const { bot, rcon, sleep } = require('./lib_resp');
const OUT = (process.env.BM_OUT || __dirname + '/../../out_p2') + '/BlackMarket_DP/data/bm/function/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const sc = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1];
  const ecnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const cnt = async (id) => { const o = await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const said = re => A.chats.some(x => re.test(x));
  const X = 26000, Y = 100, Z = 26000;
  const at = async (x, z, pitch = 60) => { await run(`${O}tp TestRat ${x + 0.5} ${Y + 1} ${z + 0.5} 0 ${pitch}`);
    await wait(2500, async () => A.pos && Math.abs(A.pos.x - x - 0.5) < 0.1 && Math.abs(A.pos.z - z - 0.5) < 0.1, 100); await sleep(400); };
  const press = (k) => `@e[type=minecraft:interaction,tag=bm.presshit,scores={bm.prk=${k}},x=${X},y=${Y},z=${Z},distance=..12,limit=1]`;
  const ago = async (k, d) => { await run(`${O}execute as ${press(k)} run scoreboard players operation @s bm.prsd = #day bm.bm`);
    await run(`${O}scoreboard players remove ${press(k)} bm.prsd ${d}`); };
  const click = async (k, ms = 700) => { const e = await entOf(press(k)); if (!e) return false; A.interact(e.entityId); await sleep(ms); return true; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} minecraft:stone`); await run(`${O}fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 6} ${Z + 6} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.presshit,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.press,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  for (const o of ['bm.prs', 'bm.prsb', 'bm.prsx', 'bm.prsl']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');

  // ---- the Counterfeiter's Press
  await run('loot replace entity TestRat hotbar.0 loot bm:items/counterfeiters_press'); A.slot(0);
  await at(X, Z - 2); A.chats.length = 0; A.use(); await sleep(250); A.release(); await sleep(900);
  ok('the Counterfeiter\'s Press, used on the floor: set down, the item spent', (await ecnt(press(0))) === 1 && (await cnt('counterfeiters_press')) === 0 && said(/press is set up/),
     A.chats.slice(-1).join(''));
  A.bars.length = 0; const c0 = await click(0, 1000);
  ok('...right-clicked the same day: the ink\'s still wet', A.bars.some(b => /ink's still wet/.test(JSON.stringify(b))) && (await cnt('token')) === 0, `clicked ${c0} bars ${A.bars.slice(-3).join(' / ')}`);
  await ago(0, 7); A.chats.length = 0; await click(0);
  const wk = (await cnt('token')) + (await cnt('medallion')) + (await cnt('trophy'));
  ok('...a week on: seven days of printing, one thing a day', said(/clacks out 7 day/) && wk === 7, `${wk} prints`);
  for (let i = 0; i < 59; i++) { await ago(0, 7); await click(0, 300); }
  await sleep(600);
  const [tk, md, tr] = [await cnt('token'), await cnt('medallion'), await cnt('trophy')];
  ok('...420 days of printing: mostly Tokens, a Medallion now and then (~1 in 25), a Trophy rarely (~1 in 200)',
     tk + md + tr === 420 && md >= 5 && md <= 35 && tr <= 8 && tk > 370, `Tokens ${tk}, Medallions ${md}, Trophies ${tr}`);
  await run('clear TestRat');

  // ---- the mythical presses, side by side
  const KINDS = [[1, 'blood_press', 'Blood Press', 'bm.prsb'], [2, 'xenite_press', 'Xenite Press', 'bm.prsx'], [3, 'lucky_press', 'Lucky Press', 'bm.prsl']];
  for (const [k, iid, nm, own] of KINDS) {
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); A.slot(0);
    await at(X - 4 + 3 * k, Z + 1); A.chats.length = 0; A.use(); await sleep(250); A.release(); await sleep(900);
    ok(`the ${nm}: set down, the item spent, yours`, (await ecnt(press(k))) === 1 && (await cnt(iid)) === 0 && (await sc(own)) === 1, A.chats.slice(-1).join(''));
  }
  await run('loot replace entity TestRat hotbar.0 loot bm:items/blood_press'); A.slot(0);
  await at(X - 3, Z - 4); A.chats.length = 0; A.use(); await sleep(250); A.release(); await sleep(900);
  ok('...a second Blood Press: no - one of each per crook', said(/one of each per crook/) && (await cnt('blood_press')) === 1 && (await ecnt(press(1))) === 1);
  await run('clear TestRat');
  await ago(1, 7); await at(X, Z + 3, 30); await click(1);
  ok('the Blood Press, a week on: 14 Blood Crystals', (await cnt('blood_crystal')) === 14, `${await cnt('blood_crystal')}`);
  await ago(2, 7); await click(2);
  const xg = await cnt('xenite_green'), xr = (await cnt('xenite_violet')) + (await cnt('xenite_cyan')) + (await cnt('xenite_red'));
  ok('the Xenite Press, a week on: 14 Green Xenite (and maybe a rarer shard or two)', xg === 14 && xr <= 7, `green ${xg}, rarer ${xr}`);
  await ago(3, 7); await click(3);
  ok('the Lucky Press, a week on: 7 Lucky Tokens', (await cnt('lucky_token')) === 7, `${await cnt('lucky_token')}`);

  // ---- sneak + punch: folded up
  A.input({ shift: true }); await sleep(300);
  const e1 = await entOf(press(1)); if (e1) A.attack(e1.entityId); await sleep(800); A.input({}); await sleep(300);
  ok('sneak + punch the Blood Press: folded up and back in the pack', (await cnt('blood_press')) === 1 && (await sc('bm.prsb')) === 0 && (await ecnt(press(1))) === 0);

  // ---- where they come from (the win rolls)
  const finds = fs.readFileSync(OUT + 'p105/finds.mcfunction', 'utf8');
  const roll = (k, cond) => new RegExp(`${cond}[^\\n]*matches \\.\\.6 run function bm:p105/find_press_${k}`).test(finds);
  ok('a won Blood Moon heist rolls 6% for the Blood Press, an Invasion heist for the Xenite Press, a Lucky heist for the Lucky Press',
     roll('blood', '#gn bm.rng matches 1') && roll('xen', '#gn bm.rng matches 3') && roll('luck', '#gn bm.rng matches 2') && roll('luck', '#plu bm.rng matches 1') &&
     /matches \.\.1 run function bm:p105\/find_myth/.test(finds));

  // ---- clean up
  for (const k of [0, 1, 2, 3]) { await run(`${O}kill @e[type=minecraft:interaction,tag=bm.presshit,scores={bm.prk=${k}},x=${X},y=${Y},z=${Z},distance=..12]`); }
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.press,x=${X},y=${Y},z=${Z},distance=..12]`);
  for (const o of ['bm.prs', 'bm.prsb', 'bm.prsx', 'bm.prsl']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
