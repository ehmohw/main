// v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh,
// the Storm Roc (rigs follow + fade on death/retreat, ambience, attacks), WANTED bounties, spawns.
const { bot, rcon, sleep } = require('./lib');
const X = 6400, Y = 100, Z = 6400;
const results = [];
let R, A, B; const run = (c) => R.run(c);
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const score = (who, obj) => num(`scoreboard players get ${who} ${obj}`);
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const re = new RegExp(`\\{[^{}]*id: "minecraft:${id}"[^{}]*\\}`); const m = s.match(re);
                                     if (!m) return null; const a = m[0].match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const ok = (n, p, d = '') => { results.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const tp = async (who, x, y, z, yaw = 0, pitch = 0) => { await run(`tp ${who} ${x} ${y} ${z} ${yaw} ${pitch}`); const b = who === 'TestRat' ? A : B; await sleep(250); if (b.pos) { b.pos.yaw = yaw; b.pos.pitch = pitch; } };
const mob = (x, y, z, tag, hp = 60, type = 'pillager') => run(`summon minecraft:${type} ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],NoAI:1b,PersistenceRequired:1b,Silent:1b,Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}d}]}`);
const hp = (sel) => num(`data get entity ${sel} Health`);
const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
const inv = async (it) => { const r = await run(`clear TestRat ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
const holding = async (iid) => (await run(`execute if items entity TestRat weapon.mainhand *[minecraft:custom_data~{bm:"${iid}"}]`)).includes('passed');
const give0 = async (iid) => { await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); A.slot(0); await sleep(300); };
const click = async (ms = 250) => { A.use(); await sleep(ms); A.release(); await sleep(250); };
const sneakClick = async (ms = 250) => { A.input({ shift: true }); await sleep(200); A.use(); await sleep(ms); A.release(); A.input({}); await sleep(300); };
const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
const at = (sel) => `x=${X},y=${Y},z=${Z},distance=..80`;
const clean = () => run(`kill @e[type=!player,${at()}]`);
const heal = async () => { await run('effect give TestRat instant_health 1 4 true'); await run('effect give TestRat2 instant_health 1 4 true'); };
const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
(async () => {
  R = await rcon(); A = await bot('TestRat'); B = await bot('TestRat2'); await sleep(1500);
  for (const [b, n] of [[A, 'TestRat'], [B, 'TestRat2']]) b.on('update_health', (p) => { if (p.health <= 0) console.log('   !! ' + n + ' died'); });
  let parts = 0; A.on('world_particles', () => parts++);
  for (const w of ['TestRat', 'TestRat2']) { await run(`clear ${w}`); await run(`effect clear ${w}`); await run(`gamemode survival ${w}`);
    await run(`effect give ${w} saturation 9999 1 true`); await run(`effect give ${w} regeneration 9999 1 true`); }
  await run('weather clear'); await run('scoreboard players set #forced bm.bm 0'); await run('scoreboard players set #active bm.bm 0');
  await run('time set day'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 20'); await sleep(1300);
  await tp('TestRat', X + 0.5, Y + 1, Z + 0.5); await tp('TestRat2', X + 30.5, Y + 1, Z + 0.5); await sleep(2000);
  await run(`fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y} ${Z + 40} stone`); await run(`fill ${X - 40} ${Y + 1} ${Z - 40} ${X + 40} ${Y + 20} ${Z + 40} air`);
  await clean(); await sleep(300);
  const P0 = [X + 0.5, Y + 1, Z + 0.5];
  const reset = async () => { for (const o of ['bm.hfu', 'bm.hcd', 'bm.hkl', 'bm.hbc', 'bm.hzc', 'bm.hch', 'bm.rcd']) await run(`scoreboard players set TestRat ${o} 0`);
                              await run('scoreboard players set TestRat bm.hfu 200'); };
  await run('effect give TestRat resistance 9999 3 true');

  // ================================================================ THE SAND PHARAOH
  await run('effect give TestRat resistance 9999 2 true'); await heal();
  const tok0 = await inv('*[custom_data~{bm:"token"}]'), med0 = await inv('*[custom_data~{bm:"medallion"}]');
  await run(`summon text_display ${X - 5} ${Y + 3} ${Z} {Tags:["bm.bboard","bm.npc"]}`);
  await tp('TestRat', ...P0, 0, 0); parts = 0; await sleep(2000); const calm = parts;
  await run('execute as TestRat at @s run function bm:admin/pharaoh'); await sleep(400);
  ok('the Sand Pharaoh rises (a husk host + his model)', (await cnt('@e[type=husk,tag=bm.sph]')) === 1 && (await cnt('@e[type=item_display,tag=bm.sphrig]')) === 1);
  ok('...you sense him: his song plays, a sense message', (await cnt('@a[name=TestRat,tag=bm.sphsensed]')) === 1);
  parts = 0; await sleep(2000);
  ok('...the sandstorm blows around you', parts > calm + 20, `${calm} -> ${parts} particle packets in 2 s`);
  ok('...his bossbar', (await run('bossbar get bm:sph visible')).includes('visible'));
  await run(`tp @e[type=husk,tag=bm.sph] ${X + 6.5} ${Y + 1} ${Z + 6.5}`); await sleep(400);
  let hpz = await pos('@e[type=husk,tag=bm.sph,limit=1]'), rpz = await pos('@e[type=item_display,tag=bm.sphrig,limit=1]');
  ok('...the model follows him', dist(hpz, rpz) < 1.2, `${dist(hpz, rpz).toFixed(2)} blocks apart`);
  const ry = await num('data get entity @e[type=item_display,tag=bm.sphrig,limit=1] Rotation[0]'), hy = await num('data get entity @e[type=husk,tag=bm.sph,limit=1] Rotation[0]');
  ok('...and turns with him', Math.abs(((ry - hy) % 360 + 540) % 360 - 180) < 2, `model ${ry.toFixed(1)}, husk ${hy.toFixed(1)}`);
  await run('data merge entity @e[type=husk,tag=bm.sph,limit=1] {NoAI:1b}');
  const at_ = async (t) => { await run(`scoreboard players set @e[type=husk,tag=bm.sph] bm.r53t ${t - 1}`); for (let i = 0; i < 11; i++) { await sleep(100); if (t === 3 && await cnt('@e[type=endermite]')) { console.log('   endermites at', i); break; } } };
  console.log('   direct:', await run('execute as @e[type=husk,tag=bm.sph] at @s run function bm:p53/sph/scarabs'));
  for (let i = 0; i < 10; i++) { console.log('   t', i, await cnt('@e[type=endermite]'), (await run('data get entity @e[type=endermite,limit=1] Health')).slice(-20)); await sleep(150); }
  await at_(3); ok('attack: scarab swarm (endermites)', (await cnt('@e[type=endermite,tag=bm.scarab]')) >= 2, `${await cnt('@e[type=endermite,tag=bm.scarab]')} scarabs, ${await cnt('@e[type=endermite]')} endermites, timer ${await score('@e[type=husk,tag=bm.sph,limit=1]', 'bm.r53t')}`);
  await at_(6); ok('attack: sand in your eyes (blindness)', (await effect('TestRat', 'blindness')) !== null);
  await at_(9); ok('attack: Tomb Guards rise', (await cnt('@e[type=husk,tag=bm.sphmin]')) >= 1);
  let d_ = await score('TestRat', 'bm.pdmg'); await at_(12);
  ok('attack: a beam of the sun burns you', (await score('TestRat', 'bm.pdmg')) > d_, `damage taken ${d_} -> ${await score('TestRat', 'bm.pdmg')}`);
  await run(`kill @e[type=endermite,tag=bm.scarab]`);
  await run(`data merge entity @e[type=husk,tag=bm.sph,limit=1] {Health:150f}`); await sleep(1200);
  ok('half health: he enrages', (await cnt('@e[type=husk,tag=bm.sph_rage]')) === 1);
  d_ = await score('TestRat', 'bm.pdmg'); await at_(14);
  ok('attack (enraged): the sand erupts under you', (await score('TestRat', 'bm.pdmg')) > d_ && (await effect('TestRat', 'levitation')) !== null, `damage taken ${d_} -> ${await score('TestRat', 'bm.pdmg')}`);
  await heal();
  await run('damage @e[type=husk,tag=bm.sph,limit=1] 999 minecraft:player_attack by TestRat'); await sleep(250);
  const fading = await cnt('@e[type=item_display,tag=bm.sphrig,tag=bm.rfade]');
  const tr = await run('data get entity @e[type=item_display,tag=bm.sphrig,limit=1] transformation.scale');
  ok('he falls: his model fades (shrinks away)', fading === 1 && tr.includes('0.0f'), tr.slice(-40));
  await sleep(2000);
  ok('...and is gone; his guards crumble; the bossbar goes', (await cnt('@e[type=item_display,tag=bm.sphrig]')) === 0 && (await cnt('@e[type=husk,tag=bm.sphmin]')) === 0 &&
     !(await run('bossbar get bm:sph visible')).includes('is visible') && (await cnt('@a[tag=bm.sphsensed]')) === 0);
  const tok1 = await inv('*[custom_data~{bm:"token"}]'), med1 = await inv('*[custom_data~{bm:"medallion"}]');
  ok('WANTED bounty collected: 8 Tokens + 2 Medallions', tok1 === tok0 + 8 && med1 === med0 + 2, `tokens ${tok0} -> ${tok1}, medallions ${med0} -> ${med1}`);
  ok('Curse of the Pharaoh', await adv('pharaoh'));
  const loot = await cnt(`@e[type=item,${at()}]`);
  ok('...his loot drops', loot >= 3, `${loot} item stacks`);
  await run(`kill @e[type=item,${at()}]`); await run(`kill @e[type=experience_orb,${at()}]`);
  const board = await run('data get entity @e[type=text_display,tag=bm.bboard,limit=1] text');
  ok('the Bounty Board lists the WANTED bosses', board.includes('WANTED') && board.includes('Sand Pharaoh') && board.includes('Storm Roc'), board.slice(0, 80));
  // he sinks away at dusk (and his model fades)
  await run('execute as TestRat at @s run function bm:admin/pharaoh'); await sleep(800);
  await run('time set 13000'); await sleep(1600);
  ok('at dusk he sinks back into the dunes; the model fades away', (await cnt('@e[type=husk,tag=bm.sph]')) === 0 && (await cnt('@e[type=item_display,tag=bm.sphrig,tag=!bm.rfade]')) === 0);
  await sleep(1600); ok('...and is gone', (await cnt('@e[type=item_display,tag=bm.sphrig]')) === 0);
  await run('time set day'); await sleep(1200);
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
