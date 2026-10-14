// 2.20 fixes: XP flask (main hand), triple-jump boots logic, Ender Pouch, Hoard Sack, Golden Cheese Wheel, orphan Vorn models.
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
let R, A; const run = (c) => R.run(c);
const res = []; const ok = (n, p, d = '') => { res.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const tp = async (x, y, z, yaw = 0, pitch = 0) => { await run(`tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await sleep(250); if (A.pos) { A.pos.yaw = yaw; A.pos.pitch = pitch; } };
(async () => {
  R = await rcon(); A = await bot('TestRat'); await sleep(1000);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat'); await run('weather clear'); await run('time set 6000');
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y + 3} ${Z + 6} minecraft:air`); await run(`fill ${X - 6} ${Y - 1} ${Z - 6} ${X + 6} ${Y - 1} ${Z + 6} minecraft:stone`);
  await tp(X + 0.5, Y, Z + 0.5);
  // ---- XP flask in the MAIN hand: pour, then sneak-drink
  await run('loot give TestRat loot bm:items/xp_flask'); A.slot(0); await sleep(300);
  await run('experience set TestRat 30 levels'); A.use(); await sleep(250); A.release(); await sleep(400);
  const stored = await num('data get entity TestRat SelectedItem.components."minecraft:custom_data".bm_xp'); const lv0 = await num('experience query TestRat levels');
  A.input({ shift: true }); await sleep(200); A.use(); await sleep(250); A.release(); A.input({}); await sleep(400);
  const lv1 = await num('experience query TestRat levels');
  ok('XP flask in the main hand: pours in, drinks back out', stored > 1000 && lv0 === 0 && lv1 === 30, `stored ${stored}, levels after pour ${lv0}, after drink ${lv1}`);
  await run('clear TestRat');
  // ---- triple jump boots (logic: each take-off raises the next jump; the third is the big one; 0.8 s on the ground resets)
  await run('loot replace entity TestRat armor.feet loot bm:items/triple_boots'); await sleep(300);
  const js = () => num('attribute TestRat minecraft:jump_strength get');
  const j0 = await js(); await run('scoreboard players set TestRat bm.jumps 1'); await sleep(150); const j1 = await js();
  await run('scoreboard players set TestRat bm.jumps 1'); await sleep(150); const j2 = await js();
  await run('scoreboard players set TestRat bm.jumps 1'); await sleep(150); const j3 = await js();
  await run('scoreboard players set TestRat bm.jumps 1'); await sleep(1300); const j4 = await js();
  ok('triple-jump boots: 2nd and 3rd jumps higher, then back; a pause resets', j0 < j1 && j1 < j2 && Math.abs(j3 - j0) < 0.01 && Math.abs(j4 - j0) < 0.01,
     `jump strength ${j0} -> ${j1} -> ${j2} -> ${j3} (after the 3rd), after a pause ${j4}`);
  await run('clear TestRat');
  // ---- Ender Pouch: an ender chest in front of you, gone when you walk off
  let wins = 0; A.on('open_window', () => wins++);
  await run('loot give TestRat loot bm:items/ender_pouch'); A.slot(0); await sleep(300); await tp(X + 0.5, Y, Z + 0.5, 0, 0);
  A.use(); await sleep(250); A.release(); await sleep(400);
  const ec = (await run(`execute if block ${X} ${Y} ${Z + 2} minecraft:ender_chest`)).includes('passed') || (await run(`execute if block ${X} ${Y} ${Z + 3} minecraft:ender_chest`)).includes('passed');
  const zc = (await run(`execute if block ${X} ${Y} ${Z + 2} minecraft:ender_chest`)).includes('passed') ? Z + 2 : Z + 3;
  A.useOn(X, Y, zc, 1); await sleep(500);
  const opened = wins > 0; await run('execute as TestRat run function bm:p33/pouch/use').catch(() => {});
  await tp(X + 0.5, Y, Z - 8.5); await sleep(1500);
  const gone = !(await run(`execute if block ${X} ${Y} ${zc} minecraft:ender_chest`)).includes('passed');
  ok('Ender Pouch: an ender chest appears, opens, folds away when you leave', ec && opened && gone, `placed ${ec}, opened ${opened}, gone ${gone}`);
  await run('clear TestRat'); await tp(X + 0.5, Y, Z + 0.5);
  // ---- Hoard Sack: a locked barrel only this sack opens; contents kept across folds
  await run('loot give TestRat loot bm:items/hoard_sack'); A.slot(0); await sleep(300);
  A.use(); await sleep(250); A.release(); await sleep(400);
  const bz = (await run(`execute if block ${X} ${Y} ${Z + 2} minecraft:barrel`)).includes('passed') ? Z + 2 : Z + 3;
  const bar = (await run(`execute if block ${X} ${Y} ${bz} minecraft:barrel`)).includes('passed');
  await run(`item replace block ${X} ${Y} ${bz} container.4 with minecraft:diamond 7`);
  wins = 0; A.slot(1); await sleep(200); A.useOn(X, Y, bz, 1); await sleep(400); const openNoSack = wins;
  A.slot(0); await sleep(200); A.useOn(X, Y, bz, 1); await sleep(400); const openSack = wins - openNoSack;
  await tp(X + 0.5, Y, Z - 9.5); await sleep(1500);
  const folded = !(await run(`execute if block ${X} ${Y} ${bz} minecraft:barrel`)).includes('passed');
  await tp(X + 0.5, Y, Z + 0.5, 0, 0); A.use(); await sleep(250); A.release(); await sleep(400);
  const bz2 = (await run(`execute if block ${X} ${Y} ${Z + 2} minecraft:barrel`)).includes('passed') ? Z + 2 : Z + 3;
  const kept = await run(`data get block ${X} ${Y} ${bz2} Items`);
  ok('Hoard Sack: locked to its sack, folds away, keeps its contents', bar && openNoSack === 0 && openSack === 1 && folded && kept.includes('diamond'),
     `barrel ${bar}, opened without sack ${openNoSack}, with ${openSack}, folded ${folded}, kept ${kept.slice(-60)}`);
  A.use(); await sleep(250); A.release(); await sleep(400); await run('clear TestRat');
  // ---- Golden Cheese Wheel: set it down, everyone near is fed; sneak-punch picks it up
  await run('loot give TestRat loot bm:items/golden_cheese_wheel'); A.slot(0); await tp(X + 0.5, Y, Z + 0.5, 0, 45); await sleep(300);
  A.use(); await sleep(900); A.release(); await sleep(500);
  const wheel = (await run('execute if entity @e[type=minecraft:item_display,tag=bm.gcheese]')).includes('passed');
  await run('effect give TestRat minecraft:hunger 2 255 true'); await sleep(2200); await run('effect clear TestRat');
  const f0 = await num('data get entity TestRat foodSaturationLevel'); const h0 = await num('data get entity TestRat foodLevel'); let sat = false, f1 = f0, h1 = h0;
  for (let i = 0; i < 25 && !sat; i++) { await sleep(250); f1 = await num('data get entity TestRat foodSaturationLevel'); h1 = await num('data get entity TestRat foodLevel'); sat = f1 > f0 || h1 > h0; }
  const hit = Object.values(A.ents).find(e => e.type === 70 && Math.abs(e.x - (X + 0.5)) < 1 && Math.abs(e.z - (Z + 2.5)) < 2);
  if (hit) { A.input({ shift: true }); await sleep(200); A.attack(hit.entityId); await sleep(500); A.input({}); }
  const back = (await run('clear TestRat *[minecraft:custom_data~{bm:"golden_cheese_wheel"}] 0')).match(/Found (\d+)/);
  const pickup = !(await run('execute if entity @e[type=minecraft:item_display,tag=bm.gcheese]')).includes('passed');
  ok('Golden Cheese Wheel: placed, feeds you, sneak-punch picks it up', wheel && sat && pickup, `placed ${wheel}, fed ${sat} (food ${h0}->${h1}, saturation ${f0}->${f1}), click box seen ${!!hit}, picked up ${pickup}`);
  await run(`kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`);
  // ---- orphan Vorn models vanish
  await run(`summon minecraft:item_display ${X} ${Y + 1} ${Z} {Tags:["bm.vdisp","t_orphan"]}`); await sleep(1300);
  ok('a Vorn model without its body vanishes', !(await run('execute if entity @e[tag=t_orphan]')).includes('passed'), '');
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
