// The Hollow King's Regalia + Sepulchre: names, wither immunity, waking by tier (trims, buffs), Wither Nova, Grave Quake.
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
let R, A, B; const run = (c) => R.run(c);
const results = []; const ok = (n, p, d = '') => { results.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const k = s.indexOf(`id: "minecraft:${id}"`); if (k < 0) return null;
                                     const st = s.lastIndexOf('{', k); const seg = s.slice(st, k + 40); const tail = s.slice(k, s.indexOf('}', k) + 1);
                                     const a = (s.slice(st, k) + tail).match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const tp = async (who, x, y, z, yaw = 0, pitch = 0) => { await run(`tp ${who} ${x} ${y} ${z} ${yaw} ${pitch}`); await sleep(250); const b = who === 'TestRat' ? A : B; if (b.pos) { b.pos.yaw = yaw; b.pos.pitch = pitch; } };
const mob = (x, y, z, tag, hp = 60, type = 'husk') => run(`summon minecraft:${type} ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],NoAI:1b,PersistenceRequired:1b,Silent:1b,Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}d}]}`);
(async () => {
  R = await rcon(); A = await bot('TestRat'); B = await bot('TestRat2'); await sleep(800);
  for (const w of ['TestRat', 'TestRat2']) { await run(`data modify entity ${w} Health set value 20f`).catch(() => {}); await run(`clear ${w}`); await run(`effect clear ${w}`); await run(`gamemode survival ${w}`); await run(`effect give ${w} minecraft:saturation infinite 0 true`); }
  await run('weather clear'); await run('time set 6000'); await run('scoreboard players set #forced bm.bm 0'); await run('function bm:admin/invasion_stop').catch(() => {});
  await run('kill @e[tag=t_r]'); await tp('TestRat2', X + 40.5, Y, Z + 0.5); await tp('TestRat', X + 0.5, Y, Z + 0.5);
  await run('execute as TestRat run function bm:admin/p2/regalia'); await sleep(300);
  for (const [sl, p] of [['armor.head', 'helmet'], ['armor.chest', 'chestplate'], ['armor.legs', 'leggings'], ['armor.feet', 'boots']])
    await run(`item replace entity TestRat ${sl} from entity TestRat container.${['helmet', 'chestplate', 'leggings', 'boots'].indexOf(p)}`);
  for (let i = 0; i < 4; i++) await run(`item replace entity TestRat container.${i} with minecraft:air`);
  await run('item replace entity TestRat hotbar.0 from entity TestRat container.4'); await run('item replace entity TestRat container.4 with minecraft:air').catch(() => {});
  A.slot(0); await sleep(1500);
  const nm = await run('data get entity TestRat equipment.chest.components."minecraft:item_name"');
  ok('evil names (the Ribcage of the Hollow King)', nm.includes('Ribcage of the Hollow King') && nm.includes('☠'), nm.slice(40, 200));
  const held = await run('data get entity TestRat SelectedItem.id');
  ok('Sepulchre in hand (a mace)', held.includes('mace'), held);
  // wither immunity
  await run('effect give TestRat minecraft:wither 6 2'); const h0 = A.health; await sleep(3000);
  ok('the Ribcage: Withering does no harm', A.health >= h0, `health ${h0} -> ${A.health} under Wither III`);
  await run('effect clear TestRat minecraft:wither');
  // day: asleep (quartz); night: amethyst and +15%
  const trim = async () => (await run('data get entity TestRat equipment.head.components."minecraft:trim".material')).replace(/.*: /, '');
  const atk = () => num('attribute TestRat minecraft:attack_damage get');
  const a0 = await atk(); const t0 = await trim();
  await run('time set 14000'); await sleep(2300);
  const ph = await num('scoreboard players get #mph bm.bm'); const a1 = await atk(); const t1 = await trim();
  ok('night/moon: the Regalia wakes (trim changes, damage up)', a1 > a0 && t1 !== t0, `attack ${a0} -> ${a1} (moon phase ${ph}), trim ${t0} -> ${t1}`);
  await run('scoreboard players set #forced bm.bm 1'); await run('time set 15000'); await sleep(2300);
  const a3 = await atk(); const t3 = await trim(); const st = await effect('TestRat', 'strength'); const reach = await num('attribute TestRat minecraft:entity_interaction_range get');
  ok('Blood Moon: redstone trim, +50%, Strength II, reach', t3.includes('redstone') && a3 > a1 && st === 1 && reach > 3, `trim ${t3}, attack ${a3}, strength ${st}, reach ${reach}`);
  await run('scoreboard players set #forced bm.bm 0'); await run(`kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..120]`);
  await run('time set 6000'); await sleep(1500); await run('time set 14000'); await run('function bm:admin/invasion_now'); await run('time set 15000'); await sleep(2500);
  const inv = await num('scoreboard players get #inv bm.bm'); const t4 = await trim(); const arm = await num('attribute TestRat minecraft:armor get'); const rs = await effect('TestRat', 'resistance');
  ok('Invasion Night: emerald trim, Resistance II, +6 armour', t4.includes('emerald') && rs === 1, `#inv ${inv}, trim ${t4}, armour ${arm}, resistance ${rs}`);
  await run('function bm:admin/invasion_stop'); await run(`kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..120]`); await run(`kill @e[tag=bm.vorn]`).catch(() => {});
  await run('time set 6000'); await sleep(2300);
  ok('dawn: it settles back to quartz', (await trim()).includes('quartz'), await trim());
  // Wither Nova: crouch + look up for a second
  await mob(X + 5.5, Y, Z + 0.5, 't_r'); await mob(X + 12.5, Y, Z + 0.5, 't_rf');
  await run('scoreboard players set TestRat bm.rgc 0'); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, -80);
  A.input({ shift: true }); await sleep(1600); A.input({}); await sleep(300);
  const w1 = await effect('@e[tag=t_r,limit=1]', 'wither'); const wf = await effect('@e[tag=t_rf,limit=1]', 'wither'); const selfw = await effect('TestRat', 'wither');
  ok('crouch + look up: Wither Nova (8 blocks, not you)', w1 === 1 && wf === null && selfw === null, `near husk wither ${w1}, husk at 12 blocks ${wf}, you ${selfw}, cooldown ${await num('scoreboard players get TestRat bm.rgc')}`);
  await run('kill @e[tag=t_r]'); await run('kill @e[tag=t_rf]');
  // Grave Quake: right-click with Sepulchre
  await run(`summon minecraft:husk ${X + 4.5} ${Y} ${Z + 0.5} {Tags:["bm.seen","t_r"],PersistenceRequired:1b,Silent:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60d},{id:"minecraft:movement_speed",base:0d}]}`); await sleep(300); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0);
  await run('scoreboard players set TestRat bm.mqc 0'); A.use(); await sleep(200); A.release(); await sleep(250);
  const vy = await run('data get entity @e[tag=t_r,limit=1] Pos[1]'); const qw = await effect('@e[tag=t_r,limit=1]', 'wither'); const qh = await num('data get entity @e[tag=t_r,limit=1] Health');
  ok('right-click Sepulchre: Grave Quake throws monsters up and withers them', parseFloat(vy.replace(/.*: /, '')) > Y + 1 && qw !== null && qh < 60, `husk y ${vy.replace(/.*: /, '')}, wither ${qw}, health ${qh}, cooldown ${await num('scoreboard players get TestRat bm.mqc')}`);
  await run('kill @e[tag=t_r]');
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
