const { bot, rcon, sleep } = require('./lib');
const X = 5200, Y = 100, Z = 5200;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)\D*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const inv = async (id) => num(`execute store result score #t bm.rng run clear TestRat *[custom_data~{bm:"${id}"}] 0`);
  const A = await bot('TestRat'); await sleep(1500);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} stone`); await run(`fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 10} ${Z + 14} air`);
  await run(`fill ${X - 14} ${Y + 4} ${Z - 14} ${X + 14} ${Y + 4} ${Z + 14} sea_lantern`);
  for (const [a, b] of [[`${X - 14} ${Y} ${Z - 14}`, `${X + 14} ${Y + 3} ${Z - 14}`], [`${X - 14} ${Y} ${Z + 14}`, `${X + 14} ${Y + 3} ${Z + 14}`],
                        [`${X - 14} ${Y} ${Z - 14}`, `${X - 14} ${Y + 3} ${Z + 14}`], [`${X + 14} ${Y} ${Z - 14}`, `${X + 14} ${Y + 3} ${Z + 14}`]]) await run(`fill ${a} ${b} sea_lantern`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat'); await run('effect give TestRat instant_health 1 5 true');
  await run('tag TestRat remove bm.pact'); await run('scoreboard players reset TestRat bm.thirst'); await run('scoreboard players reset TestRat bm.mircd');
  await run('time of minecraft:overworld resume'); await run('scoreboard players set #hgt bm.bm 0');
  const clean = async () => { await run(`kill @e[type=#bm:hostile,tag=!t27,tag=!t27s,x=${X},y=${Y},z=${Z},distance=..80]`); await run('effect clear TestRat'); };
  const hp = async () => num('data get entity TestRat Health');
  const useHeld = async (id, ms = 1800) => { await clean(); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${id}`); await sleep(200); A.use(); await sleep(ms); A.release(); await sleep(200); };
  const slay = async (sel) => { await run(`damage @e[${sel},limit=1] 500 minecraft:player_attack by TestRat`); await sleep(250); };
  // no moon: refunds
  await run('scoreboard players set #forced bm.bm 0'); await run('time set noon'); await sleep(1500);
  await useHeld('moon_pact');
  ok('pact refused (and refunded) with no Blood Moon', !(await cnt('@a[tag=bm.pact]')) && (await inv('moon_pact')) === 1);
  await run('clear TestRat');
  // raise a Blood Moon
  await run('scoreboard players set #forced bm.bm 1'); await run('time set midnight'); await sleep(2500);
  ok('Blood Moon active', (await num('scoreboard players get #active bm.bm')) === 1);
  // ---- MOON PACT
  await useHeld('moon_pact');
  ok('pact signed', (await cnt('@a[name=TestRat,tag=bm.pact]')) === 1 && !(await inv('moon_pact')));
  await run('clear TestRat'); await run('effect give TestRat instant_health 1 5 true'); await sleep(600);
  await clean(); await run('scoreboard objectives add tdmg minecraft.custom:minecraft.damage_taken'); await run('scoreboard players set TestRat tdmg 0'); await run('damage TestRat 4 minecraft:generic'); await sleep(1500);
  const dd = await num('scoreboard players get TestRat tdmg'); ok('pact: 4 damage costs 6', dd === 60, 'took ' + dd / 10);
  for (let i = 0; i < 4; i++) { await run(`summon zombie ${X + 3} ${Y} ${Z + 3} {NoAI:1b,Tags:["bm.blood","t27"],PersistenceRequired:1b}`); await slay('tag=t27'); }
  const cr = await inv('blood_crystal');
  ok('pact: slain horrors pay extra Crystals into your pack', cr >= 4 && cr <= 8, cr + ' crystals from 4 kills');
  await run('clear TestRat'); await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..20]`);
  await useHeld('moon_pact');
  ok('second pact refused (refunded)', (await inv('moon_pact')) === 1);
  await run('clear TestRat'); await run('effect give TestRat instant_health 1 5 true');
  // ---- THIRSTING BLADE
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/thirsting_blade'); await sleep(600);
  const d0 = await num('attribute TestRat minecraft:attack_damage get');
  for (let i = 0; i < 3; i++) { await run(`summon zombie ${X + 3} ${Y} ${Z + 3} {NoAI:1b,Tags:["t27"],PersistenceRequired:1b}`); await slay('tag=t27'); }
  await sleep(600);
  const d3 = await num('attribute TestRat minecraft:attack_damage get');
  ok('blade: 3 kills = +3 damage', (await num('scoreboard players get TestRat bm.thirst')) === 3 && d3 === d0 + 3, `${d0} -> ${d3}`);
  await clean(); A.slot(4); await sleep(700);
  ok('blade: bonus gone when not in hand', (await num('attribute TestRat minecraft:attack_damage get')) === 1, '' + await num('attribute TestRat minecraft:attack_damage get'));
  A.slot(0); await sleep(700);
  await run('scoreboard players set TestRat bm.thirst 6');
  await run(`summon zombie ${X + 3} ${Y} ${Z + 3} {NoAI:1b,Tags:["t27"],PersistenceRequired:1b}`); await slay('tag=t27'); await sleep(600);
  ok('blade: capped at +6', (await num('scoreboard players get TestRat bm.thirst')) === 6 && (await num('attribute TestRat minecraft:attack_damage get')) === d0 + 6);
  // ---- CRIMSON HOURGLASS
  await useHeld('crimson_hourglass');
  const t0 = await num('time of minecraft:overworld query time'); await sleep(3000); const t1 = await num('time of minecraft:overworld query time');
  ok('hourglass: the moon stands still', (await num('scoreboard players get #hgt bm.bm')) > 100 && t1 === t0, `${t0} -> ${t1}`);
  await useHeld('crimson_hourglass');
  const hgn = await inv('crimson_hourglass'); ok('hourglass: once a moon (refunded)', hgn >= 1, hgn + ' in pack');
  await run('clear TestRat');
  await run('scoreboard players set #hgt bm.bm 1'); await sleep(2200);
  const t2 = await num('time of minecraft:overworld query time'); await sleep(1500); const t3 = await num('time of minecraft:overworld query time');
  ok('hourglass: time runs again after', t3 > t2 && (await num('scoreboard players get #active bm.bm')) === 1, `${t2} -> ${t3}`);
  // ---- VAMPIRE'S MIRROR
  await clean(); await run(`tp TestRat ${X + 2.5} ${Y} ${Z + 2.5} 90 10`); await sleep(500);
  await useHeld('vampire_mirror', 400);
  ok('mirror: mark set (with a marker)', (await cnt('@a[name=TestRat,tag=bm.mirset]')) === 1 && (await cnt('@e[type=marker,tag=bm.mirmark]')) === 1);
  await run(`tp TestRat ${X - 10.5} ${Y} ${Z - 9.5}`); await sleep(500); A.use(); await sleep(400); A.release(); await sleep(300);
  let px = await num('data get entity TestRat Pos[0]'), pz = await num('data get entity TestRat Pos[2]');
  ok('mirror: steps back to the mark', Math.abs(px - (X + 2.5)) < 0.01 && Math.abs(pz - (Z + 2.5)) < 0.01, `${px} ${pz}`);
  ok('mirror: mark used up, cooldown running', !(await cnt('@a[name=TestRat,tag=bm.mirset]')) && !(await cnt('@e[type=marker,tag=bm.mirmark]')) && (await num('scoreboard players get TestRat bm.mircd')) > 25);
  A.use(); await sleep(400); A.release(); await sleep(300);
  ok('mirror: no new mark during the cooldown', !(await cnt('@a[name=TestRat,tag=bm.mirset]')));
  await run('scoreboard players set TestRat bm.mircd 0');
  A.use(); await sleep(400); A.release(); await sleep(300);
  await run(`execute in minecraft:the_nether run tp TestRat ${X / 8} 120 ${Z / 8}`); await sleep(1500);
  A.use(); await sleep(400); A.release(); await sleep(800);
  const dim = await run('data get entity TestRat Dimension'); px = await num('data get entity TestRat Pos[0]');
  ok('mirror: works across dimensions', dim.includes('overworld') && Math.abs(px - (X + 2.5)) < 0.01, dim.slice(-30) + ' ' + px);
  await run('scoreboard players set TestRat bm.mircd 0'); A.use(); await sleep(400); A.release(); await sleep(300);
  await run('scoreboard players set TestRat bm.mirt 1'); await sleep(2200);
  ok('mirror: an unused mark fades after its window', !(await cnt('@a[name=TestRat,tag=bm.mirset]')) && !(await cnt('@e[type=marker,tag=bm.mirmark]')));
  await run('clear TestRat');
  // ---- MUSIC DISC
  let riders = 0;
  for (let i = 0; i < 12 && riders < 3; i++) {
    await run(`summon skeleton ${X + 40} ${Y + 30} ${Z} {Tags:["t27s"],NoAI:1b,NoGravity:1b,PersistenceRequired:1b}`);
    await run('execute as @e[tag=t27s] at @s run function bm:mounts/blood_skeleton_horse'); await sleep(100);
    riders += await cnt('@e[tag=t27s,tag=bm.bmrider]');
    await run(`kill @e[type=skeleton_horse,x=${X + 40},y=${Y + 30},z=${Z},distance=..10]`); await run('kill @e[tag=t27s]');
  }
  const unmounted = await (async () => { let n = 0; for (let i = 0; i < 6; i++) { await run(`summon skeleton ${X + 6} ${Y + 20} ${Z + 6} {Tags:["t27s"],NoAI:1b,NoGravity:1b}`);
    await run('execute as @e[tag=t27s] at @s run function bm:mounts/blood_skeleton_horse'); n += await cnt('@e[tag=t27s,tag=bm.bmrider,predicate=!bm:sees_sky]'); await run('kill @e[tag=t27s]'); } return n; })();
  await clean();
  ok('riders of blood steeds are marked', riders > 0, riders + ' riders');
  for (let i = 0; i < 16; i++) { await run(`summon skeleton ${X + 3} ${Y} ${Z + 3} {NoAI:1b,Tags:["t27","bm.bmrider","bm.blood"],PersistenceRequired:1b}`); await slay('tag=t27'); }
  const discs = await inv('music_disc_blood_moon');
  ok('riders drop the disc (about 1 in 4)', discs >= 1 && discs <= 10, discs + ' discs from 16 riders');
  await run(`setblock ${X + 4} ${Y} ${Z} jukebox`);
    await run(`loot replace block ${X + 4} ${Y} ${Z} container.0 loot bm:items/music_disc_blood_moon`); await sleep(3000);
  const jb = await run(`data get block ${X + 4} ${Y} ${Z}`);
  ok('jukebox plays it', /ticks_since_song_started: [1-9]\d*L/.test(jb), jb.replace(/.*ticks_since_song_started/, 'ticks').slice(0, 40));
  // ---- dawn
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/thirsting_blade'); await run('scoreboard players set TestRat bm.thirst 4'); await sleep(600);
  await run('scoreboard players set #forced bm.bm 0'); await run('time set day'); await sleep(2500);
  ok('dawn: moon ends, pact lifted', (await num('scoreboard players get #active bm.bm')) === 0 && !(await cnt('@a[tag=bm.pact]')));
  ok('dawn: the blade bonus is gone', (await num('attribute TestRat minecraft:attack_damage get')) === d0, '' + await num('attribute TestRat minecraft:attack_damage get'));
  await clean(); await run('scoreboard players set TestRat tdmg 0'); await run('damage TestRat 4 minecraft:generic'); await sleep(1500);
  ok('dawn: damage back to normal', (await num('scoreboard players get TestRat tdmg')) === 40);
  await run(`setblock ${X + 4} ${Y} ${Z} air`);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });
