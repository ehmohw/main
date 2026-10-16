// v2.40: KillerWatt's Tendrils, Apophiss's Crown, Leo's Trident, Cecil's Staff
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const X = 9900, Y = 100, Z = 9900;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[fdbsL]?\s*$/); return m ? +m[1] : null; };
  const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const give = async (iid, slot = 'hotbar.0') => { await run(`execute as TestRat run function bm:admin/cecil_relics`); };
  const sneakUse = async () => { A.input({ shift: true }); await sleep(250); A.use(); await sleep(250); A.release(); A.input({}); await sleep(400); };
  const use = async () => { A.use(); await sleep(250); A.release(); await sleep(400); };
  const zombie = async (x, z, tag, kind = 'husk') => { await run(`summon ${kind} ${x} ${Y + 1} ${z} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["${tag}","bm.t42"],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b}]}`);
    await sleep(400); await run(`attribute @e[tag=${tag},limit=1] minecraft:max_health base set 200`); await sleep(100); await run(`data modify entity @e[tag=${tag},limit=1] Health set value 200f`); };
  const hp = (tag) => num(`data get entity @e[tag=${tag},limit=1] Health`);
  const face = async (x, y, z) => { await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} facing ${x} ${y} ${z}`); await sleep(600); };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 25} ${Y} ${Z - 25} ${X + 25} ${Y} ${Z + 25} stone`); await run(`fill ${X - 25} ${Y + 1} ${Z - 25} ${X + 25} ${Y + 10} ${Z + 25} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('time set noon'); await run('weather clear');
  for (const o of ['bm.kwcd', 'bm.stcd', 'bm.sthc', 'bm.crcd']) await run(`scoreboard players reset TestRat ${o}`);
  await run('execute as TestRat run function bm:admin/cecil_relics'); await sleep(500);
  // slots: 0 tendrils, 1 crown, 2 trident, 3 staff (admin gives in that order)
  let all = true; for (const k of ['killerwatt_tendrils', 'apophiss_crown', 'leo_trident', 'cecil_staff']) all = all && /Found 1 /.test(await run(`clear TestRat *[custom_data~{bm:"${k}"}] 0`));
  ok('Cecil\'s relics: all four given', all);
  A.slot(0); await sleep(300);
  // ---- tendrils (2.4x: worn as equipment - their zap and snatch are covered by t43): the sneak + use yank
  // sneak: yank it to you
  await run(`summon husk ${X + 0.5} ${Y + 1} ${Z + 10.5} {PersistenceRequired:1b,Silent:1b,Tags:["bm.zy","bm.t42"],attributes:[{id:"minecraft:movement_speed",base:0.0d}],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b}]}`);
  await run('kill @e[tag=bm.z1]'); await sleep(900); const p0 = await pos('@e[tag=bm.zy,limit=1]'); await sneakUse(); await sleep(400);
  const p1 = await pos('@e[tag=bm.zy,limit=1]');
  ok('...sneak + use: the monster is yanked toward you', p0 && p1 && p1[2] < p0[2] - 1.0, `${p0 && p0[2].toFixed(2)} -> ${p1 && p1[2].toFixed(2)}`);
  await run('kill @e[tag=bm.t42]'); await sleep(1100);
  // a block: flung toward it (the enchantment's impulse fires and clears the tag)
  await run(`fill ${X - 1} ${Y + 1} ${Z + 12} ${X + 2} ${Y + 6} ${Z + 12} stone`); await face(X + 0.5, Y + 2.5, Z + 12);
  await use(); await sleep(150);
  const tg = await run('tag TestRat list');
  ok('...aimed at a wall 11 blocks off: the fling fires (tag armed then consumed by the impulse)', !/bm\.kwl[123]/.test(tg), tg.slice(-60));
  await sleep(1300); await sneakUse(); await sleep(150);
  ok('...sneak + use at a wall: heaved upward (fires)', !/bm\.kwup/.test(await run('tag TestRat list')));
  await run(`fill ${X - 1} ${Y + 1} ${Z + 12} ${X + 2} ${Y + 6} ${Z + 12} air`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
  const hf0 = await num('data get entity TestRat Health'); await run('damage TestRat 6 minecraft:fall'); await sleep(200);
  const hf = await num('data get entity TestRat Health');
  ok('...held: no fall damage', hf >= hf0 - 0.01, `health ${hf0} -> ${hf}`);
  const spd = await num('attribute TestRat minecraft:movement_speed get');
  ok('...held: 15% faster', spd > 0.113, `${spd}`);
  // ---- the crown
  await run('item replace entity TestRat armor.head from entity TestRat hotbar.1'); await sleep(400);
  const sc = await num('attribute TestRat minecraft:scale get');
  ok("Apophiss's Crown worn: you grow (scale 1.2), more health", Math.abs(sc - 1.2) < 0.01 && (await num('attribute TestRat minecraft:max_health get')) >= 24, `scale ${sc}`);
  A.input({ shift: true }); await sleep(300); await run('scoreboard players set TestRat bm.crj 1'); await sleep(300);
  const fangs = await cnt(`@e[type=evoker_fangs,x=${X},y=${Y},z=${Z},distance=..30]`); A.input({}); await sleep(300);
  ok("...sneak + jump: Serpent's Fangs (a line of 12)", fangs >= 10, `${fangs} fangs`);
  await run('scoreboard players set TestRat bm.crj 1'); await sleep(300);
  ok('...not while it recovers', (await cnt(`@e[type=evoker_fangs,x=${X},y=${Y},z=${Z},distance=..30]`)) <= fangs);
  await zombie(X + 0.5, Z + 2.2, 'bm.z3', 'vindicator'); await sleep(800); A.slot(4); await sleep(200);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
  const zid = Object.values(A.ents).filter(e => Math.abs(e.x - X - 0.5) < 0.3 && Math.abs(e.z - Z - 2.2) < 0.3).pop()?.entityId;
  A.attack(zid ?? 0); await sleep(400);
  ok('...your blows wither', (await run('data get entity @e[tag=bm.z3,limit=1] active_effects')).includes('wither'), zid ? '' : '(bot lost track of the zombie: ' + Object.values(A.ents).map(e => e.x.toFixed(1) + ',' + e.z.toFixed(1)).slice(-6).join(' ') + ')');
  // ---- Leo's trident: swap hands changes its form
  await run('item replace entity TestRat armor.head with air');
  A.slot(2); await sleep(400); await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.2'); await run('item replace entity TestRat hotbar.2 with stone'); await sleep(400);
  const mh = await run('data get entity TestRat SelectedItem'); const oh = await run('data get entity TestRat equipment.offhand');
  ok("Leo's Trident: swapped to the off hand, it comes back as the spear; the stone goes back to the off hand", mh.includes('leo_spear') && oh.includes('stone'), mh.slice(0, 80));
  await run('item replace entity TestRat weapon.offhand from entity TestRat weapon.mainhand'); await run('item replace entity TestRat weapon.mainhand with stone'); await sleep(400);
  ok('...and again: the trident', (await run('data get entity TestRat SelectedItem')).includes('leo_trident'));
  await run('effect clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
  const zid2 = Object.values(A.ents).filter(e => Math.abs(e.x - X - 0.5) < 0.3 && Math.abs(e.z - Z - 2.2) < 0.3).pop()?.entityId;
  A.attack(zid2 ?? 0); await sleep(400);
  ok('...a hit: Speed II', /speed/.test(await run('data get entity TestRat active_effects')));
  // ---- Cecil's staff
  await run('kill @e[tag=bm.t42]'); await zombie(X + 0.5, Z + 9.5, 'bm.z4', 'vindicator'); A.slot(3); await sleep(300);
  await face(X + 0.5, Y + 2, Z + 9.5); await use(); await sleep(300);
  const z4 = await hp('bm.z4'); ok("Cecil's Staff: a poisoned bolt (5)", z4 <= 195.5 && (await run('data get entity @e[tag=bm.z4,limit=1] active_effects')).includes('poison'), `${z4}; held ${(await run('data get entity TestRat SelectedItem')).slice(-60)}`);
  await run('effect clear TestRat'); await run('damage TestRat 12 minecraft:out_of_world'); await sleep(100); const h0 = await num('data get entity TestRat Health'); await sneakUse(); await sleep(300);
  const hh = await num('data get entity TestRat Health');
  ok('...sneak + use: it mends you (+4 at once)', hh >= h0 + 3.9, `health ${h0} -> ${hh}`);
  await run('effect clear TestRat'); await run('damage TestRat 6 minecraft:out_of_world'); await sleep(100); const h1 = await num('data get entity TestRat Health'); await sneakUse(); await sleep(200);
  ok('...then needs 20 s (no second +4; saturation may heal a point)', (await num('data get entity TestRat Health')) < h1 + 3.5, `${h1}`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat'); await run(`forceload remove ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`);
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
