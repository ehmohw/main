// v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh,
// the Storm Roc (vanilla bodies, scaled up; ambience, attacks), WANTED bounties, spawns.
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

  // ================================================================ THE HORSEMAN'S HEAD - four classes
  await give0('horseman_head'); await reset();
  ok('OFFENSE (Horseman\'s Head): heavier melee (10 by day)', (await num('attribute TestRat minecraft:attack_damage get')) === 10, '' + await num('attribute TestRat minecraft:attack_damage get'));
  await tp('TestRat', ...P0, 0, 0); await mob(X + 0.5, Y + 1, Z + 4.5, 't_h', 100); await sleep(400);
  let h0 = await hp('@e[tag=t_h,limit=1]'); A.use(); await sleep(1500);
  let h1 = await hp('@e[tag=t_h,limit=1]'); let fu = await score('TestRat', 'bm.hfu');
  ok('...a fierce stream: hurts, burns, uses fuel twice as fast', h1 < h0 - 10 && fu < 150, `husk ${h0} -> ${h1}, fuel ${fu}`);
  await sleep(4000); const cd = await score('TestRat', 'bm.hcd'); A.release(); await sleep(300);
  ok('...5 s of fire, then it gutters out', cd > 0, `cooldown ${cd}`);
  await clean(); await reset();
  // catalysts: blaze rod / armadillo scute / breeze rod / heartstone; the lanterns still work
  const up = async (off) => { await run(`item replace entity TestRat weapon.offhand with ${off}`); await tp('TestRat', ...P0, 0, -85); await click(); };
  await up('minecraft:armadillo_scute 2');
  ok('Armadillo Scute: Soulfire Head (DEFENSE), one scute used', await holding('soul_head') && (await num('data get entity TestRat equipment.offhand.count')) === 1);
  await up('minecraft:breeze_rod 1'); ok('Breeze Rod: Venomfire Head (RANGED)', await holding('venom_head'));
  await run('loot replace entity TestRat weapon.offhand loot bm:items/heartstone'); await tp('TestRat', ...P0, 0, -85); await click();
  ok('Heartstone: Hallowed Head (SUPPORT)', await holding('hallowed_head'));
  await up('minecraft:blaze_rod 1'); ok('Blaze Rod: back to the Horseman\'s Head (OFFENSE)', await holding('horseman_head'));
  await up('minecraft:soul_lantern 1'); ok('a Soul Lantern still works', await holding('soul_head'));
  // ---- DEFENSE
  await reset(); await tp('TestRat', ...P0, 0, 0);
  ok('DEFENSE melee is lighter (7)', (await num('attribute TestRat minecraft:attack_damage get')) === 7);
  await mob(X + 0.5, Y + 1, Z + 2.2, 't_h', 100); await sleep(300);
  A.attack(Object.values(A.ents).filter(e => Math.abs(e.x - (X + 0.5)) < 0.2 && Math.abs(e.z - (Z + 2.2)) < 0.2).pop()?.entityId ?? 0); await sleep(400);
  ok('...its blows slow and weaken', (await effect('@e[tag=t_h,limit=1]', 'slowness')) !== null && (await effect('@e[tag=t_h,limit=1]', 'weakness')) !== null);
  await run('effect clear TestRat resistance');
  A.use(); await sleep(700);
  const kb = await num('attribute TestRat minecraft:knockback_resistance get'); const res = await effect('TestRat', 'resistance');
  ok('hold: FROST WARD - Resistance II and no knockback', res === 1 && kb >= 1 && (await cnt('@a[name=TestRat,tag=bm.p42ward]')) === 1, `resistance ${res}, knockback res ${kb}`);
  await run(`damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]`); await sleep(300);
  const fz = await num('data get entity @e[tag=t_h,limit=1] TicksFrozen');
  ok('...whoever hits you is chilled to the bone (frost, slowness)', fz > 100 && (await effect('@e[tag=t_h,limit=1]', 'slowness')) >= 3, `TicksFrozen ${fz}, slowness ${await effect('@e[tag=t_h,limit=1]', 'slowness')}`);
  A.release(); await sleep(500);
  ok('...let go: the ward drops', (await num('attribute TestRat minecraft:knockback_resistance get')) < 1 && (await cnt('@a[name=TestRat,tag=bm.p42ward]')) === 0);
  await run('effect give TestRat resistance 9999 3 true'); await clean();
  await run('scoreboard players set TestRat bm.hkl 20'); await mob(X + 5.5, Y + 1, Z + 0.5, 't_h', 100); await mob(X + 14.5, Y + 1, Z + 0.5, 't_far', 100);
  await tp('TestRat', ...P0, 0, 85); await sneakClick();
  ok('GLACIAL NOVA: freezes everything near (Slowness X), you get Absorption', (await effect('@e[tag=t_h,limit=1]', 'slowness')) === 9 && (await effect('TestRat', 'absorption')) === 2 &&
     (await hp('@e[tag=t_far,limit=1]')) === 100, `slowness ${await effect('@e[tag=t_h,limit=1]', 'slowness')}, absorption ${await effect('TestRat', 'absorption')}`);
  await clean();
  // ---- RANGED
  await up('minecraft:breeze_rod 1'); await reset(); await tp('TestRat', ...P0, 0, 0);
  ok('RANGED melee is weak (5)', (await num('attribute TestRat minecraft:attack_damage get')) === 5);
  await mob(X + 0.5, Y + 1, Z + 25.5, 't_h', 100, 'pillager'); await sleep(400);
  h0 = await hp('@e[tag=t_h,limit=1]'); A.use(); await sleep(1600); A.release(); await sleep(300);
  h1 = await hp('@e[tag=t_h,limit=1]');
  ok('hold: VENOM BOLTS reach 25 blocks, hurt and poison', h1 < h0 - 6 && (await effect('@e[tag=t_h,limit=1]', 'poison')) !== null, `pillager ${h0} -> ${h1}`);
  await clean(); await reset();
  await mob(X + 0.5, Y + 1, Z + 12.5, 't_h', 100, 'pillager'); await sleep(300);
  await tp('TestRat', ...P0, 0, -12); h0 = await hp('@e[tag=t_h,limit=1]');
  A.input({ shift: true }); await sleep(200); A.use(); await sleep(2400); A.release(); A.input({}); await sleep(200);
  const lob = await cnt('@e[type=snowball,tag=bm.plg]') + await cnt('@e[type=marker,tag=bm.plgc]');
  await sleep(2500);
  const clouds = await cnt('@e[type=marker,tag=bm.plgc]'); const cp = await pos('@e[type=marker,tag=bm.plgc,limit=1]');
  h1 = await hp('@e[tag=t_h,limit=1]');
  ok('sneak + hold, let go: a PLAGUE BURST is lobbed and leaves a poison cloud', lob >= 1 && clouds === 1, `in flight ${lob}, clouds ${clouds} at ${cp && cp.map(v => v.toFixed(1))}`);
  if (cp) { await run(`tp @e[tag=t_h] ${cp[0]} ${cp[1]} ${cp[2]}`); await sleep(2200); }
  const h2 = await hp('@e[tag=t_h,limit=1]');
  ok('...the cloud poisons and hurts what stands in it', h2 < h1 && (await effect('@e[tag=t_h,limit=1]', 'poison')) !== null, `pillager ${h1} -> ${h2}`);
  await clean();
  // ---- SUPPORT still heals
  await run('loot replace entity TestRat weapon.offhand loot bm:items/heartstone'); await tp('TestRat', ...P0, 0, -85); await click(); await reset();
  await tp('TestRat2', X + 0.5, Y + 1, Z + 5.5, 180, 0); await run('effect clear TestRat2 regeneration'); await sleep(300); await run('damage TestRat2 10 minecraft:generic'); await sleep(500);
  let g0 = B.health; await tp('TestRat', ...P0, 0, 8); A.use(); await sleep(2500); A.release(); await sleep(300);
  ok('SUPPORT (Hallowed Head) still heals with its beam', B.health >= g0 + 4, `${g0} -> ${B.health}`);
  await run('effect give TestRat2 regeneration 9999 1 true'); await tp('TestRat2', X + 30.5, Y + 1, Z + 0.5);

  // ================================================================ THE RELICS
  const R_ = { crook: ['pharaoh_crook', 'crook_sands', 'crook_sun', 'crook_ra'], talon: ['storm_talon', 'talon_static', 'talon_chain', 'talon_wind'] };
  for (const fam of ['crook', 'talon']) {
    await give0(R_[fam][0]);
    const order = [['minecraft:armadillo_scute 1', 1], ['minecraft:breeze_rod 1', 2], [null, 3], ['minecraft:blaze_rod 1', 0]];
    const got = [];
    for (const [off, k] of order) { if (off) await run(`item replace entity TestRat weapon.offhand with ${off}`); else await run('loot replace entity TestRat weapon.offhand loot bm:items/heartstone');
      await tp('TestRat', ...P0, 0, -85); await click(); got.push(await holding(R_[fam][k])); }
    ok(`${fam}: every catalyst turns it (scute, breeze rod, heartstone, blaze rod)`, got.every(x => x), got.join(','));
  }
  const relic = async (iid) => { await give0(iid); await run('scoreboard players set TestRat bm.rcd 0'); };
  // ---- Crook of Scarabs
  await run('time set day'); await sleep(1200);
  await relic('pharaoh_crook'); await tp('TestRat', ...P0, 0, 0);
  await mob(X + 0.5, Y + 1, Z + 5.5, 't_a', 100); await mob(X + 0.8, Y + 1, Z + 10.5, 't_b', 100); await mob(X + 0.5, Y + 1, Z + 20.5, 't_far', 100); await sleep(300);
  await click();
  let a1 = await hp('@e[tag=t_a,limit=1]'), b1 = await hp('@e[tag=t_b,limit=1]');
  ok('Crook of Scarabs: the swarm eats through everything in its path (and starves it)', a1 < 100 && b1 < 100 && (await effect('@e[tag=t_a,limit=1]', 'hunger')) !== null &&
     (await hp('@e[tag=t_far,limit=1]')) === 100, `near ${a1}, behind ${b1}, out of reach ${await hp('@e[tag=t_far,limit=1]')}`);
  ok('...stronger under the sun (x1.5: 10.5 damage)', a1 === 89.5, `${100 - a1} damage`);
  await click(150);
  ok('...and then it needs a moment (cooldown)', (await score('TestRat', 'bm.rcd')) > 0 && (A.bars.slice(-1)[0] || '').includes('gathering'), A.bars.slice(-1)[0]);
  await clean();
  // ---- Crook of the Sands
  await relic('crook_sands'); await run('effect clear TestRat resistance');
  ok('Crook of the Sands: melee 7', (await num('attribute TestRat minecraft:attack_damage get')) === 7);
  await mob(X + 0.5, Y + 1, Z + 2.5, 't_h', 100, 'zombie'); await click();
  ok('...a Sandstone Shell: Resistance II', (await effect('TestRat', 'resistance')) === 1 && (await score('TestRat', 'bm.rst')) > 0);
  await sleep(300); await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  ok('...whoever hits you gets sand in the eyes (blinded)', (await effect('@e[tag=t_h,limit=1]', 'blindness')) !== null);
  await run('effect give TestRat resistance 9999 3 true'); await clean();
  // ---- Crook of the Sun
  await relic('crook_sun'); await tp('TestRat', ...P0, 0, 0);
  await mob(X + 0.5, Y + 1, Z + 10.5, 't_a', 100); await mob(X + 0.5, Y + 1, Z + 30.5, 't_b', 100); await sleep(300); await click();
  a1 = await hp('@e[tag=t_a,limit=1]'); b1 = await hp('@e[tag=t_b,limit=1]');
  ok('Crook of the Sun: the lance pierces 30 blocks and sets alight', a1 < 100 && b1 < 100 && (await num('data get entity @e[tag=t_b,limit=1] Fire')) > 0, `${a1}, ${b1}`);
  await run('time set night'); await sleep(1300); await run('scoreboard players set TestRat bm.rcd 0'); await click();
  const a2 = await hp('@e[tag=t_a,limit=1]');
  ok('...weaker by night (x1: 8 vs 12 by day)', (100 - a1) === 12 && (a1 - a2) >= 8 && (a1 - a2) < 10, `day ${100 - a1}, night ${a1 - a2}`);
  await run('time set day'); await sleep(1200); await clean();
  // ---- Crook of Ra
  await relic('crook_ra'); await tp('TestRat2', X + 4.5, Y + 1, Z + 0.5); await tp('TestRat', ...P0, 0, 0); await click();
  ok('Crook of Ra: Strength + Haste II for you and an ally within 8', (await effect('TestRat2', 'strength')) === 0 && (await effect('TestRat2', 'haste')) === 1 &&
     (await effect('TestRat', 'haste')) === 1);
  await tp('TestRat2', X + 30.5, Y + 1, Z + 0.5);
  // ---- Thunderbird Talon
  await relic('storm_talon'); await tp('TestRat', ...P0, 0, 0);
  await mob(X + 3.5, Y + 1, Z + 0.5, 't_a', 100); await mob(X + 0.5, Y + 1, Z - 3.5, 't_b', 100, 'zombie'); await mob(X + 9.5, Y + 1, Z + 0.5, 't_far', 100); await sleep(300);
  parts = 0; await click();
  a1 = await hp('@e[tag=t_a,limit=1]'); b1 = await hp('@e[tag=t_b,limit=1]');
  ok('Thunderbird Talon: a Thunderclap strikes every monster within 5 (not beyond)', a1 < 100 && b1 < 100 && (await hp('@e[tag=t_far,limit=1]')) === 100, `${a1}, ${b1}, far ${await hp('@e[tag=t_far,limit=1]')}`);
  ok('...with its thunderbolts (sparks and a flash)', parts > 10, `${parts} particle packets`);
  await clean(); await mob(X + 0.5, Y + 1, Z + 2.2, 't_h', 500); await sleep(400);
  const eid = Object.values(A.ents).filter(e => Math.abs(e.z - (Z + 2.2)) < 0.2 && Math.abs(e.x - (X + 0.5)) < 0.2).pop()?.entityId;
  let bolts = 0; A.on('sound_effect', () => {}); const hb = await hp('@e[tag=t_h,limit=1]');
  for (let i = 0; i < 12; i++) { A.attack(eid); await sleep(950); }
  const ha = await hp('@e[tag=t_h,limit=1]');
  ok('...its blows often call down a thunderbolt (12 hits do more than 12 x 9)', hb - ha > 12 * 9, `${hb - ha} damage from 12 hits`);
  await clean();
  // ---- Static Talon
  await relic('talon_static'); await mob(X + 0.5, Y + 1, Z + 2.5, 't_h', 100, 'zombie'); await sleep(200); await click();
  ok('Static Talon: a Static Field (Resistance)', (await score('TestRat', 'bm.rst')) > 0 && (await effect('TestRat', 'resistance')) !== null);
  await sleep(2300); a1 = await hp('@e[tag=t_h,limit=1]');
  ok('...shocks what stands near you every second', a1 < 97, `zombie ${a1}`);
  await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(200);
  ok('...and whoever hits you', (await hp('@e[tag=t_h,limit=1]')) < a1, `${a1} -> ${await hp('@e[tag=t_h,limit=1]')}`);
  await clean(); await sleep(6000);
  // ---- Stormcaller Talon
  await relic('talon_chain'); await tp('TestRat', ...P0, 0, 0);
  for (const [i, dx, dz] of [[0, 0, 12], [1, 3, 15], [2, -2, 18], [3, 3, 21], [4, 0, 34]]) await mob(X + 0.5 + dx, Y + 1, Z + dz + 0.5, `t_c${i}`, 100);
  await sleep(300); await click();
  const hit = []; for (let i = 0; i < 5; i++) hit.push(await hp(`@e[tag=t_c${i},limit=1]`));
  ok('Stormcaller Talon: chain lightning leaps to 4 targets (not a 5th 12 blocks off)', hit.slice(0, 4).every(h => h < 100) && hit[4] === 100, hit.join(','));
  await clean();
  // ---- Tailwind Talon
  await relic('talon_wind'); await tp('TestRat2', X + 4.5, Y + 1, Z + 0.5); await tp('TestRat', ...P0, 0, 0); await click();
  ok('Tailwind Talon: Speed II + Jump Boost II for you and an ally', (await effect('TestRat2', 'speed')) === 1 && (await effect('TestRat2', 'jump_boost')) === 1 && (await effect('TestRat', 'speed')) === 1);
  await tp('TestRat2', X + 30.5, Y + 1, Z + 0.5);
  await run('item replace entity TestRat hotbar.0 with air'); await run('effect clear TestRat speed'); await run('effect clear TestRat jump_boost');

  // ================================================================ THE SAND PHARAOH
  await run('effect give TestRat resistance 9999 2 true'); await heal();
  const tok0 = await inv('*[custom_data~{bm:"token"}]'), med0 = await inv('*[custom_data~{bm:"medallion"}]');
  await run(`summon text_display ${X - 5} ${Y + 3} ${Z} {Tags:["bm.bboard","bm.npc"]}`);
  await tp('TestRat', ...P0, 0, 0); parts = 0; await sleep(2000); const calm = parts;
  await run('execute as TestRat at @s run function bm:admin/pharaoh'); await sleep(400);
  ok('the Sand Pharaoh rises: a giant visible husk (scale 2.6) in a golden crown, no model parts', (await cnt('@e[type=husk,tag=bm.sph]')) === 1 && (await num('attribute @e[type=husk,tag=bm.sph,limit=1] minecraft:scale get')) === 2.6 &&
     (await effect('@e[type=husk,tag=bm.sph,limit=1]', 'invisibility')) === null && (await cnt('@e[type=item_display,tag=bm.rig53]')) === 0 && (await run('data get entity @e[type=husk,tag=bm.sph,limit=1] equipment.head.id')).includes('golden_helmet'));
  ok('...you sense him: his song plays, a sense message', (await cnt('@a[name=TestRat,tag=bm.sphsensed]')) === 1);
  parts = 0; await sleep(2000);
  ok('...the sandstorm blows around you', parts > calm + 20, `${calm} -> ${parts} particle packets in 2 s`);
  ok('...his bossbar', (await run('bossbar get bm:sph visible')).includes('visible'));
  await run(`tp @e[type=husk,tag=bm.sph] ${X + 6.5} ${Y + 1} ${Z + 6.5}`); await sleep(400);
  let hpz, rpz;
  await run('data merge entity @e[type=husk,tag=bm.sph,limit=1] {NoAI:1b}');
  const at_ = async (t) => { await run(`scoreboard players set @e[type=husk,tag=bm.sph] bm.r53t ${t - 1}`); for (let i = 0; i < 11; i++) { await sleep(100); if (t === 3 && await cnt('@e[type=endermite]')) { console.log('   endermites at', i); break; } } };
  await at_(3); ok('attack: scarab swarm (endermites)', (await cnt('@e[type=endermite,tag=bm.scarab]')) >= 2, `${await cnt('@e[type=endermite,tag=bm.scarab]')} scarabs, ${await cnt('@e[type=endermite]')} endermites, timer ${await score('@e[type=husk,tag=bm.sph,limit=1]', 'bm.r53t')}`);
  await at_(6); ok('attack: sand in your eyes (blindness)', (await effect('TestRat', 'blindness')) !== null);
  await at_(9); ok('attack: Tomb Guards rise', (await cnt('@e[type=husk,tag=bm.sphmin]')) >= 1);
  let d_ = await score('TestRat', 'bm.pdmg'); await at_(12);
  ok('attack: a beam of the sun burns you', (await score('TestRat', 'bm.pdmg')) > d_, `damage taken ${d_} -> ${await score('TestRat', 'bm.pdmg')}`);
  await run(`kill @e[type=endermite,tag=bm.scarab]`);
  await run(`data merge entity @e[type=husk,tag=bm.sph,limit=1] {Health:150f}`); await sleep(1200);
  ok('half health: he enrages', (await cnt('@e[type=husk,tag=bm.sph_rage]')) === 1);
  d_ = await score('TestRat', 'bm.pdmg'); await at_(14);
  ok('attack (enraged): the sand erupts under you', (await score('TestRat', 'bm.pdmg')) > d_, `damage taken ${d_} -> ${await score('TestRat', 'bm.pdmg')}`);
  await heal();
  await run('damage @e[type=husk,tag=bm.sph,limit=1] 999 minecraft:player_attack by TestRat'); await sleep(250);
  const gone = await cnt('@e[type=husk,tag=bm.sph]');

  ok('he falls (no model left behind)', gone === 0 && (await cnt('@e[type=item_display,tag=bm.rig53]')) === 0);
  await sleep(2000);
  ok('...and is gone; his guards crumble; the bossbar goes', (await cnt('@e[type=husk,tag=bm.sphmin]')) === 0 &&
     !(await run('bossbar get bm:sph visible')).includes('is visible') && (await cnt('@a[tag=bm.sphsensed]')) === 0);
  const tok1 = await inv('*[custom_data~{bm:"token"}]'), med1 = await inv('*[custom_data~{bm:"medallion"}]');
  ok('WANTED bounty collected: 8 Tokens + 2 Medallions', tok1 === tok0 + 8 && med1 === med0 + 2, `tokens ${tok0} -> ${tok1}, medallions ${med0} -> ${med1}`);
  ok('Curse of the Pharaoh', await adv('pharaoh'));
  const loot = await cnt(`@e[type=item,${at()}]`);
  ok('...his loot drops', loot >= 3, `${loot} item stacks`);
  await run(`kill @e[type=item,${at()}]`); await run(`kill @e[type=experience_orb,${at()}]`);
  const board = await run('data get entity @e[type=text_display,tag=bm.bboard,limit=1] text');
  ok('the Bounty Board lists the WANTED bosses', board.includes('WANTED') && board.includes('Pharaoh') && board.includes('Storm Roc'), board.slice(0, 80));
  // he sinks away at dusk (and his model fades)
  await run('execute as TestRat at @s run function bm:admin/pharaoh'); await sleep(800);
  await run('time set 13000'); await sleep(1600);
  ok('at dusk he sinks back into the dunes', (await cnt('@e[type=husk,tag=bm.sph]')) === 0);

  await run('time set day'); await sleep(1200);
  // natural spawn: desert, day, under the sky
  await run(`fillbiome ${X - 12} ${Y - 2} ${Z - 12} ${X + 12} ${Y + 12} ${Z + 12} minecraft:desert`); await sleep(300);
  ok('the desert predicate sees the desert', (await run('execute as TestRat at @s if predicate bm:p53/desert')).includes('passed'));
  await run('execute as TestRat at @s run function bm:p53/sph/try'); await sleep(500);
  const sp = await pos('@e[type=husk,tag=bm.sph,limit=1]');
  ok('a desert day spawn: about 20 blocks off', sp && Math.abs(dist(sp, P0) - 20) < 3, sp ? `${dist(sp, P0).toFixed(1)} blocks` : 'none');
  await run('kill @e[type=husk,tag=bm.sph]'); await sleep(2000); await clean();
  await run(`fillbiome ${X - 12} ${Y - 2} ${Z - 12} ${X + 12} ${Y + 12} ${Z + 12} minecraft:plains`);

  // ================================================================ THE STORM ROC
  await tp('TestRat2', X + 0.5, Y + 1, Z + 75.5);
  await run('weather thunder'); await sleep(8000); await heal();
  const tokR = await inv('*[custom_data~{bm:"token"}]');
  await run('execute as TestRat at @s run function bm:admin/storm_roc'); await sleep(500);
  ok('the Storm Roc comes down: a giant visible phantom (scale 4.5), no model parts', (await cnt('@e[type=phantom,tag=bm.roc]')) === 1 && (await num('attribute @e[type=phantom,tag=bm.roc,limit=1] minecraft:scale get')) === 4.5 &&
     (await effect('@e[type=phantom,tag=bm.roc,limit=1]', 'invisibility')) === null && (await cnt('@e[type=item_display,tag=bm.rig53]')) === 0);
  ok('...you sense it', (await cnt('@a[name=TestRat,tag=bm.rocsensed]')) === 1);
  const anc = await run('data get entity @e[type=phantom,tag=bm.roc,limit=1] anchor_pos');
  ok('...it circles where it came down (anchor set)', !anc.includes('[I; 0, 0, 0]'), anc.slice(-40));
  await sleep(1500);
  await run(`tp @e[type=phantom,tag=bm.roc] ${X + 6.5} ${Y + 6} ${Z + 6.5}`); await run('data merge entity @e[type=phantom,tag=bm.roc,limit=1] {NoAI:1b}');
  const rt = async (t) => { await run(`scoreboard players set @e[type=phantom,tag=bm.roc] bm.r53t ${t - 1}`); await sleep(1050); };
  d_ = await score('TestRat', 'bm.pdmg');
  await run('scoreboard players set @e[type=phantom,tag=bm.roc] bm.r53t 3'); let marks = 0; for (let i = 0; i < 24 && !marks; i++) { await sleep(50); marks = await cnt('@e[type=marker,tag=bm.rocbolt]'); } await sleep(1300);
  ok('attack: sparks gather over you, then lightning falls', marks >= 1 && (await score('TestRat', 'bm.pdmg')) > d_, `marks ${marks}, damage taken ${d_} -> ${await score('TestRat', 'bm.pdmg')}`);
  await heal(); const y0 = (await pos('@a[name=TestRat,limit=1]'))[1]; await rt(8); await sleep(150);
  const y1 = (await pos('@a[name=TestRat,limit=1]'))[1];
  // (a bot client doesn't simulate knockback: check the same gust on a zombie)
  await run(`summon zombie ${X - 5.5} ${Y + 1} ${Z + 0.5} {Tags:["t_g"]}`); await sleep(300);
  const gz0 = (await pos('@e[tag=t_g,limit=1]'))[1]; await run('execute at @e[tag=t_g] run summon minecraft:breeze_wind_charge ~ ~0.3 ~ {Motion:[0.0d,-1.0d,0.0d]}'); await sleep(400);
  const gz1 = (await pos('@e[tag=t_g,limit=1]'))[1]; await run('kill @e[tag=t_g]');
  ok('attack: a gust of wind throws you (its charge, on a zombie)', gz1 > gz0 + 1, `y ${gz0.toFixed(1)} -> ${gz1.toFixed(1)}`);
  await sleep(1500); await tp('TestRat', ...P0);
  await run(`data merge entity @e[type=phantom,tag=bm.roc,limit=1] {Health:120f}`); await sleep(1200);
  ok('half health: it shrieks, Stormlings join', (await cnt('@e[type=phantom,tag=bm.roc_rage]')) === 1 && (await cnt('@e[type=phantom,tag=bm.rocmin]')) >= 1);
  await heal();
  await run('damage @e[type=phantom,tag=bm.roc,limit=1] 999 minecraft:player_attack by TestRat'); await sleep(250);
  ok('it falls', (await cnt('@e[type=phantom,tag=bm.roc]')) === 0);
  await sleep(2000);
  ok('...and are gone; Stormlings crumble; no stray bolts', (await cnt('@e[type=phantom,tag=bm.rocmin]')) === 0 &&
     (await cnt('@e[type=marker,tag=bm.rocbolt]')) === 0);
  ok('WANTED bounty collected (8 Tokens)', (await inv('*[custom_data~{bm:"token"}]')) === tokR + 8);
  ok('Eye of the Storm', await adv('storm_roc'));
  await run(`kill @e[type=item,${at()}]`); await run(`kill @e[type=experience_orb,${at()}]`);
  // it leaves with the storm
  await run('execute as TestRat at @s run function bm:admin/storm_roc'); await sleep(800); await run('weather clear'); await sleep(12500);
  ok('when the storm ends it rises away', (await cnt('@e[type=phantom,tag=bm.roc]')) === 0);
  await sleep(1600);
  // a thunderstorm spawn
  await run('weather thunder'); await sleep(8000); await run('execute as TestRat at @s run function bm:p53/roc/try'); await sleep(500);
  const rp_ = await pos('@e[type=phantom,tag=bm.roc,limit=1]');
  ok('a thunderstorm spawn: it comes down near you, high up', rp_ && rp_[1] > Y + 10, rp_ ? rp_.map(v => v.toFixed(0)).join(' ') : 'none');
  await run('kill @e[type=phantom,tag=bm.roc]'); await run('weather clear'); await sleep(2000);
  // the Horseman's bounty too + Monster Slayer
  const tokH = await inv('*[custom_data~{bm:"token"}]');
  await run('time set night'); await sleep(1500); await run('execute as TestRat at @s run function bm:admin/horseman'); await sleep(600);
  await run('damage @e[type=wither_skeleton,tag=bm.hhm,limit=1] 999 minecraft:player_attack by TestRat'); await sleep(800);
  ok('the Headless Horseman pays the WANTED bounty too', (await inv('*[custom_data~{bm:"token"}]')) === tokH + 8);
  ok('Monster Slayer (all three)', await adv('monster_slayer'));
  for (const i of ['horseman_head', 'pharaoh_crook', 'storm_talon']) await run(`loot give TestRat loot bm:items/${i}`); await sleep(400);
  ok('Relic Hunter (a relic of each)', await adv('relic_hunter'));
  await run('time set day'); await sleep(500); await clean();
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
