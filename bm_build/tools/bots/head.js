// The Horseman's Head: stream, overheat, charged blast, stoking + Nova, undead XP, lantern/heart variants, night tiers, healing.
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
const results = [];
let R, A, B; const run = (c) => R.run(c);
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const score = (who, obj) => num(`scoreboard players get ${who} ${obj}`);
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const re = new RegExp(`\\{[^{}]*id: "minecraft:${id}"[^{}]*\\}`); const m = s.match(re);
                                     if (!m) return null; const a = m[0].match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const ok = (n, p, d = '') => { results.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const tp = async (who, x, y, z, yaw = 0, pitch = 0) => { const r = await run(`tp ${who} ${x} ${y} ${z} ${yaw} ${pitch}`); const b = who === 'TestRat' ? A : B; await sleep(250); if (b.pos) { b.pos.yaw = yaw; b.pos.pitch = pitch; } try { b.write('look', { yaw, pitch, flags: { onGround: true, hasHorizontalCollision: false } }); } catch (e) {} return r; };
const zombie = (x, y, z, tag, hp = 40, type = 'husk') => run(`summon minecraft:${type} ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],NoAI:1b,PersistenceRequired:1b,Silent:1b,Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}d}]}`);
const hp = (sel) => num(`data get entity ${sel} Health`);
const holding = async (iid) => (await run(`execute if items entity TestRat weapon.mainhand *[minecraft:custom_data~{bm:"${iid}"}]`)).includes('passed');
(async () => {
  R = await rcon(); A = await bot('TestRat'); B = await bot('TestRat2'); await sleep(800);
  for (const [b, n] of [[A, 'TestRat'], [B, 'TestRat2']]) b.on('update_health', (p) => { if (p.health <= 0) console.log('   !! ' + n + ' died'); });
  for (const w of ['TestRat', 'TestRat2']) { await run(`data modify entity ${w} Health set value 20f`).catch(()=>{}); await run(`clear ${w}`); await run(`effect clear ${w}`); await run(`gamemode survival ${w}`); await run(`effect give ${w} minecraft:saturation infinite 0 true`); }
  for (const o of ['bm.hfu', 'bm.hcd', 'bm.hkl', 'bm.hbc', 'bm.hzc', 'bm.hch']) await run(`scoreboard players reset TestRat ${o}`);
  await run('weather clear'); await tp('TestRat2', X + 40.5, Y, Z + 0.5); await run('kill @e[tag=t_h]'); await run('scoreboard players set #forced bm.bm 0'); await run('time set 6000'); await sleep(1200);
  console.log('   give:', await run('loot give TestRat loot bm:items/horseman_head')); A.slot(0); await sleep(600); console.log('   held:', await run('data get entity TestRat SelectedItem.id'), await run('data get entity TestRat Health'));
  // ---- day: plain melee stats; not placeable
  const attr = await num('attribute TestRat minecraft:attack_damage get');
  const spd = await num('attribute TestRat minecraft:attack_speed get');
  ok('melee: netherite-sword damage, slower swing (day)', attr === 8 && spd < 1.6, `attack ${attr}, speed ${spd}`);
  // ---- the stream: zombie 4 blocks ahead takes hellfire and burns
  await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0); await zombie(X + 0.5, Y, Z + 4.5, 't_h'); await sleep(600);
  const h0 = await hp('@e[tag=t_h,limit=1]');
  A.use(); await sleep(1500);
  const h1 = await hp('@e[tag=t_h,limit=1]'); const fire = await num('data get entity @e[tag=t_h,limit=1] Fire');
  const fuel = await score('TestRat', 'bm.hfu');
  ok('hold right-click: a stream of fire that hurts and sets alight', h1 < h0 && fire > 0, `zombie ${h0} -> ${h1}, Fire ${fire}, fuel ${fuel}/200`);
  await sleep(9500);
  const cd = await score('TestRat', 'bm.hcd'); A.release(); await sleep(300);
  ok('10 s of fire, then it gutters out (cooldown)', cd > 100, `cooldown ticks ${cd}, fuel ${await score('TestRat', 'bm.hfu')}`);
  await run('kill @e[tag=t_h]');
  await run('scoreboard players set TestRat bm.hcd 1'); await sleep(600);
  ok('rekindles after the cooldown', (await score('TestRat', 'bm.hfu')) === 200, `fuel ${await score('TestRat', 'bm.hfu')}`);
  // ---- the charged blast at a zombie 16 blocks away
  await zombie(X + 0.5, Y, Z + 16.5, 't_h', 60); await sleep(400);
  const b0 = await hp('@e[tag=t_h,limit=1]');
  A.input({ shift: true }); await sleep(200); A.use(); await sleep(2400); A.release(); await sleep(200); A.input({}); await sleep(600);
  const b1 = await hp('@e[tag=t_h,limit=1]');
  ok('sneak + hold: charge, let go: a Fire Blast (16 blocks)', b1 < b0 - 8, `zombie ${b0} -> ${b1}, blast cooldown ${await score('TestRat', 'bm.hbc')}`);
  const blocks = await run(`execute unless block ${X} ${Y - 1} ${Z + 16} minecraft:air`);
  ok('the blast leaves the ground intact', blocks.includes('passed'), blocks);
  await run('kill @e[tag=t_h]');
  // ---- stoking + undead XP: kill zombies with the stream
  await run('scoreboard players set TestRat bm.hkl 0'); await run('scoreboard players set TestRat bm.hfu 200');
  for (let i = 0; i < 3; i++) await zombie(X - 0.3 + i * 0.8, Y, Z + 3.5 + i, 't_h', 2);
  await sleep(300); A.use(); await sleep(1300); A.release(); await sleep(400);
  const kl = await score('TestRat', 'bm.hkl'); const orbs = await num(`execute positioned ${X} ${Y} ${Z} store result score #t bm.rng if entity @e[type=minecraft:experience_orb,distance=..10]`);
  ok('kills stoke the head; undead drop extra XP', kl >= 3 && orbs >= 1, `stoked ${kl}, xp orbs ${orbs}`);
  await run(`kill @e[type=minecraft:experience_orb,distance=..20,x=${X},y=${Y},z=${Z}]`); await run('kill @e[tag=t_h]');
  // ---- the Nova (forced full), hits everything within 10 but not a pig
  await run('scoreboard players set TestRat bm.hkl 20');
  await zombie(X + 7.5, Y, Z + 0.5, 't_h', 60); await zombie(X - 6.5, Y, Z - 4.5, 't_h', 60); await zombie(X + 14.5, Y, Z + 0.5, 't_far', 60);
  console.log('   nova targets:', await hp('@e[tag=t_far,limit=1]'), await hp('@e[tag=t_h,limit=1]'));
  await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 85); await sleep(400);
  A.input({ shift: true }); await sleep(200); A.use(); await sleep(250); A.release(); A.input({}); await sleep(500);
  const n1 = await hp('@e[tag=t_h,limit=1,sort=nearest,x=' + (X + 7.5) + ',y=' + Y + ',z=' + Z + ']'); const nf = await hp('@e[tag=t_far,limit=1]');
  ok('sneak + look down: Nova hits monsters within 10 (not beyond)', n1 < 60 && nf === 60, `near zombie ${n1}, zombie at 14 blocks ${nf}, stoke now ${await score('TestRat', 'bm.hkl')}`);
  await run('kill @e[tag=t_h]'); await run('kill @e[tag=t_far]');
  // ---- night: night vision, x1.5; full moon x2; blood moon x2.5 + reach + strength/speed
  await run('time set 14000'); await sleep(1300);
  const nv = await effect('TestRat', 'night_vision'); const a1 = await num('attribute TestRat minecraft:attack_damage get');
  const day = await num('scoreboard players get #day bm.bm');
  const ph = await num('scoreboard players get #mph bm.bm');
  ok('night: night vision and x1.5 damage (x2 under a full/new moon)', nv !== null && a1 === ((ph === 0 || ph === 4) ? 16 : 12), `night vision ${nv !== null}, attack ${a1} (day ${day}, moon phase ${await num('scoreboard players get #mph bm.bm')})`);
  await run('effect give TestRat minecraft:resistance 6 4 true'); await run('scoreboard players set #forced bm.bm 1'); await run('time set 15000'); await sleep(2300);
  const a3 = await num('attribute TestRat minecraft:attack_damage get'); const reach = await num('attribute TestRat minecraft:entity_interaction_range get');
  const st = await effect('TestRat', 'strength'); const sp = await effect('TestRat', 'speed');
  ok('Blood Moon: x2.5, Strength II, Speed II, longer reach', a3 >= 34 && reach > 3 && st === 1 && sp === 1, `attack ${a3}, reach ${reach}, strength ${st}, speed ${sp}`);
  await run('scoreboard players set #forced bm.bm 0'); await run('time set 6000'); await sleep(1500);
  await run(`kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..120]`);
  A.slot(1); await sleep(3500);
  const a0 = await num('attribute TestRat minecraft:attack_damage get');
  ok('letting go of it drops the buffs', a0 === 1 && (await effect('TestRat', 'night_vision')) === null, `attack ${a0} (empty hand), night vision ${await effect('TestRat', 'night_vision')}`);
  A.slot(0); await sleep(300);
  // ---- variants: soul lantern -> Soulfire Head (freezing), copper lantern -> Venomfire (poison), lantern back, heartstone -> Hallowed
  const up = async (off) => { await run(`item replace entity TestRat weapon.offhand with ${off}`); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, -85); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(400); };
  console.log('   before variants:', (await run('data get entity TestRat Inventory')).slice(0, 120), await run('data get entity TestRat Health'), await run('data get entity TestRat SelectedItemSlot'));
  await up('minecraft:soul_lantern 2');
  console.log('   after soul:', (await run('data get entity TestRat equipment')).slice(0, 200));
  const soul = await holding('soul_head'); const left = await num('data get entity TestRat equipment.offhand.count');
  ok('Soul Lantern in the off hand + look up: Soulfire Head (one lantern used)', soul && left === 1, `soul head ${soul}, lanterns left ${left}`);
  await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0); await zombie(X + 0.5, Y, Z + 3.5, 't_h', 60); await sleep(300);
  A.use(); await sleep(1200); A.release(); await sleep(200);
  const fr = await num('data get entity @e[tag=t_h,limit=1] TicksFrozen'); const sl = await effect('@e[tag=t_h,limit=1]', 'slowness');
  ok('soul fire freezes (frost + slowness)', fr > 0 && sl !== null, `TicksFrozen ${fr}, slowness ${sl}`);
  await run('kill @e[tag=t_h]'); await run('scoreboard players set TestRat bm.hfu 200');
  await up('minecraft:oxidized_copper_lantern 1');
  ok('Copper Lantern: Venomfire Head', await holding('venom_head'), '');
  await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0); await zombie(X + 0.5, Y, Z + 3.5, 't_h', 60, 'pillager'); await sleep(300);
  A.use(); await sleep(1200); A.release(); await sleep(200);
  ok('venom fire poisons', (await effect('@e[tag=t_h,limit=1]', 'poison')) !== null, `poison ${await effect('@e[tag=t_h,limit=1]', 'poison')}`);
  await run('kill @e[tag=t_h]');
  await up('minecraft:lantern 1');
  ok('a plain Lantern turns it back', await holding('horseman_head'), '');
  await run('loot replace entity TestRat weapon.offhand loot bm:items/heartstone'); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, -85); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(400);
  ok('a Heartstone makes the Hallowed Head', await holding('hallowed_head'), `melee ${await num('attribute TestRat minecraft:attack_damage get')}`);
  // heal beam on the other player
  await run('scoreboard players set TestRat bm.hfu 200'); await run('scoreboard players set TestRat bm.hcd 0');
  await tp('TestRat2', X + 0.5, Y, Z + 5.5, 180, 0); await run('effect clear TestRat2'); await run('effect give TestRat2 minecraft:hunger 30 50 true'); await sleep(1500); await run('damage TestRat2 10 minecraft:generic'); await sleep(600);
  const g0 = B.health; await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 8); await sleep(300);
  A.use(); await sleep(2500); A.release(); await sleep(300);
  ok('Hallowed Head: the beam heals the player in it', B.health >= g0 + 4, `TestRat2 ${g0} -> ${B.health}`);
  // regeneration circle
  await run('scoreboard players set TestRat bm.hzc 0'); A.input({ shift: true }); await sleep(200); A.use(); await sleep(250); A.release(); A.input({}); await sleep(1500);
  const zone = await num(`execute store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.hzone]`);
  ok('sneak + right-click: a circle of Regeneration', zone >= 1 && (await effect('TestRat', 'regeneration')) !== null, `circles ${zone}, regen ${await effect('TestRat', 'regeneration')}`);
  await run('kill @e[tag=bm.hzone]');
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
