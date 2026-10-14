// v2.49: Shifting arms, followers vanish on death, Tendril modes (toggle / ranged auto-lash / offense grab), Pearlman's trades stay open
const { bot, rcon, sleep } = require('./lib');
const X = 11000, Y = 200, Z = 11000;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (o) => { const m = (await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[fdbsL]?\s*$/); return m ? +m[1] : null; };
  const held = async () => ((await run('data get entity TestRat SelectedItem.components."minecraft:custom_data".bm')).match(/"(\w+)"/) || [])[1];
  const pressF = async (sneak = false) => { if (sneak) { A.input({ shift: true }); await sleep(250); }
    await run('item replace entity TestRat hotbar.8 from entity TestRat weapon.offhand'); await run('item replace entity TestRat weapon.offhand from entity TestRat weapon.mainhand');
    await run('item replace entity TestRat weapon.mainhand from entity TestRat hotbar.8'); await run('item replace entity TestRat hotbar.8 with air'); await sleep(250);
    if (sneak) { A.input({}); await sleep(150); } };
  const mob = async (x, z, tag) => { await run(`summon husk ${x} ${Y + 1} ${z} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["${tag}","bm.t49"]}`);
    await sleep(300); await run(`attribute @e[tag=${tag},limit=1] minecraft:max_health base set 200`); await run(`data modify entity @e[tag=${tag},limit=1] Health set value 200f`); };
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2000);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`);
  await run(`fill ${X - 25} ${Y} ${Z - 25} ${X + 25} ${Y} ${Z + 25} stone`); await run(`fill ${X - 25} ${Y + 1} ${Z - 25} ${X + 25} ${Y + 6} ${Z + 25} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`); await run('time set noon'); await run('weather clear');
  // ---- Shifting arms
  await run('execute as TestRat run function bm:admin/shifting_arms'); A.slot(0); await sleep(300);
  const sh = (await run('data get entity TestRat SelectedItem.components."minecraft:enchantments"'));
  ok('Shifting Blade: a sword with the best enchantments (Sharpness V, Looting III...), unbreakable', /sharpness": 5/.test(sh) && /looting": 3/.test(sh), sh.slice(-120));
  const seen = [await held()];
  for (let i = 0; i < 5; i++) { await pressF(); seen.push(await held()); }
  ok('F cycles sword -> axe -> mace -> spear -> trident -> sword', seen.join(',') === 'shift_blade_sword,shift_blade_axe,shift_blade_mace,shift_blade_spear,shift_blade_trident,shift_blade_sword', seen.join(','));
  await pressF(true);
  ok('Sneak + F goes back (sword -> trident)', (await held()) === 'shift_blade_trident', await held());
  await run('item replace entity TestRat weapon.offhand with minecraft:shield'); await pressF();
  ok('...and whatever was in your off-hand stays there', (await held()) === 'shift_blade_sword' && /shield/.test(await run('data get entity TestRat equipment.offhand.id')), await run('data get entity TestRat equipment.offhand.id'));
  A.slot(1); await sleep(200); const p0 = await held(); const pk = []; for (let i = 0; i < 8; i++) { await pressF(); pk.push((await held() || '').replace('shift_pick_', '')); }
  ok('Shifting Pick: all eight tools', p0 === 'shift_pick_pickaxe' && pk.join(',') === 'axe,shovel,hoe,shears,rod,brush,flint,pickaxe', pk.join(','));
  A.slot(2); await sleep(200); const bw = []; for (let i = 0; i < 3; i++) { await pressF(); bw.push((await held() || '').replace('shift_bow_', '')); }
  ok('Shifting Bow: bow -> crossbow -> trident -> bow', bw.join(',') === 'crossbow,trident,bow', bw.join(','));
  await run('clear TestRat'); await run('item replace entity TestRat weapon.offhand with air');
  // ---- followers vanish when you die
  await run('scoreboard players reset TestRat bm.emcd'); await run('scoreboard players reset TestRat bm.cpcd');
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(400);
  await run('execute as TestRat at @s run function bm:p57/summon'); await sleep(1200);
  const before = [await cnt('@e[type=wolf,tag=bm.cecilpet]'), await cnt('@e[type=cat,tag=bm.emmapet]'), await cnt('@e[type=item_display,tag=bm.emp]'), await cnt('@e[type=item_display,tag=bm.cpet]')];
  await run('kill TestRat'); await sleep(1500);
  const after = [await cnt('@e[type=wolf,tag=bm.cecilpet]'), await cnt('@e[type=cat,tag=bm.emmapet]'), await cnt('@e[type=item_display,tag=bm.emp]'), await cnt('@e[type=item_display,tag=bm.cpet]')];
  ok('Die with Emma and Cecil out: both vanish (hosts and rigs) in a burst', before[0] === 1 && before[1] === 1 && before[2] > 0 && after.every(v => v === 0), `${before} -> ${after}`);
  ok('...and no cooldown: you can call them straight back', !((await sc('bm.emcd')) > 0) && !((await sc('bm.cpcd')) > 0));
  await sleep(1500); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('kill @e[type=item]'); await sleep(800);
  // ---- Tendrils
  await run('execute as TestRat run function bm:admin/cecil_relics'); await sleep(300);
  await run('item replace entity TestRat armor.chest from entity TestRat hotbar.0'); for (let s = 0; s < 9; s++) await run(`item replace entity TestRat hotbar.${s} with air`); await sleep(800);
  ok('Tendrils start in OFFENSE', !((await sc('bm.kwmd')) === 1));
  A.input({ shift: true }); await sleep(120); A.input({}); await sleep(120); A.input({ shift: true }); await sleep(120); A.input({}); await sleep(400);
  ok('Double-tap sneak: RANGED', (await sc('bm.kwmd')) === 1, (A.bars.slice(-1)[0] || '').slice(0, 60));
  // ranged: a monster ahead but off to the side - no aiming needed
  await mob(X + 4.5, Z + 12.5, 'bm.r1'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2200);
  const r1 = await num('data get entity @e[tag=bm.r1,limit=1] Health');
  ok('RANGED: the nearest monster ahead is lashed without aiming at it (10 + lightning)', r1 !== null && r1 <= 191, '' + r1);
  await run('kill @e[tag=bm.t49]'); await sleep(200);
  A.input({ shift: true }); await sleep(120); A.input({}); await sleep(120); A.input({ shift: true }); await sleep(120); A.input({}); await sleep(400);
  ok('Double-tap again: OFFENSE', (await sc('bm.kwmd')) === 0);
  await run('kill @e[tag=bm.g1]'); await run(`summon husk ${X + 0.5} ${Y + 1} ${Z + 9.5} {PersistenceRequired:1b,Silent:1b,Tags:["bm.g1","bm.t49"],attributes:[{id:"minecraft:movement_speed",base:0.0d}]}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  const gz = await num('data get entity @e[tag=bm.g1,limit=1] Pos[2]');
  ok('OFFENSE: a tendril drags a monster 9 blocks ahead in to you', gz !== null && gz < Z + 4.5, '' + gz);
  await run('kill @e[tag=bm.t49]'); await run('item replace entity TestRat armor.chest with air'); await sleep(300);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
