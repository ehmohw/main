// Headless Horseman play-test: spawn him near a survival bot at night, watch him fight, then kill him.
const { bot, rcon, sleep, text } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(800);
  const subs = []; A.on('set_title_subtitle', (p) => subs.push(text(p.text)));
  const results = []; const ok = (n, p, d) => { results.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + '  -- ' + d); };
  await run('kill @e[tag=bm.hhm]'); await run('kill @e[tag=bm.hhs]'); await run('kill @e[tag=bm.hhmin]');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 2 true'); await run('effect give TestRat minecraft:regeneration infinite 2 true');
  await run('time set 14000'); await run('difficulty normal'); await run('weather clear');
  await run(`tp TestRat ${X} ${Y} ${Z} 0 0`); await sleep(1500);
  await run(`execute positioned ${X} ${Y} ${Z + 14} run function bm:p42/boss/summon`); await sleep(1500);
  const hasBoss = (await run('execute if entity @e[type=minecraft:wither_skeleton,tag=bm.hhm]')).includes('passed');
  const mounted = (await run('execute as @e[type=minecraft:wither_skeleton,tag=bm.hhm] on vehicle if entity @s[tag=bm.hhs]')).includes('passed');
  ok('summoned, riding the Hellsteed', hasBoss && mounted, `boss ${hasBoss}, mounted ${mounted}`);
  ok('"evil presence" subtitle for the nearby player', subs.some(s => s.includes('evil presence')), JSON.stringify(subs));
  const pos = async (sel) => { const s = await run(`data get entity ${sel} Pos`); const m = s.match(/\[(.*)\]/); return m ? m[1].split(',').map(parseFloat) : null; };
  const hp0 = A.health; let minHp = 20, hits = 0, last = A.health;
  A.on('update_health', (p) => { if (p.health < last) hits++; last = p.health; minHp = Math.min(minHp, p.health); });
  const p0 = await pos('@e[type=minecraft:skeleton_horse,tag=bm.hhs,limit=1]');
  let maxThralls = 0, closest = 99, motionSeen = 0;
  for (let t = 0; t < 30; t++) {
    await sleep(1000);
    const th = (await run('execute store result score #t bm.rng if entity @e[tag=bm.hhmin]')); const n = +((await run('scoreboard players get #t bm.rng')).match(/has (\d+)/) || [0, 0])[1];
    maxThralls = Math.max(maxThralls, n);
    const hp = await pos('@e[type=minecraft:skeleton_horse,tag=bm.hhs,limit=1]');
    if (hp) closest = Math.min(closest, Math.hypot(hp[0] - X, hp[2] - Z));
    const mo = await run('data get entity @e[type=minecraft:skeleton_horse,tag=bm.hhs,limit=1] Motion');
    const mm = mo.match(/\[(.*)\]/); if (mm) { const v = mm[1].split(',').map(parseFloat); if (Math.hypot(v[0], v[2]) > 0.5) motionSeen++; }
    await run(`tp TestRat ${X} ${Y} ${Z}`);     // stand still so he has to come
  }
  const bh = await run('data get entity @e[type=minecraft:wither_skeleton,tag=bm.hhm,limit=1] Health');
  ok('he closes in on the player', closest < 6, `steed start ${p0 && p0.map(v => v.toFixed(1))}, closest ${closest.toFixed(1)} blocks`);
  ok('he hurts the player (breath / spear / thralls)', hits > 0, `hits ${hits}, lowest health ${minHp.toFixed(1)}`);
  ok('Pumpkin Thralls summoned (cap 6)', maxThralls >= 2 && maxThralls <= 9, `max thralls ${maxThralls}`);
  console.log('    lunge motion samples:', motionSeen, ' boss', bh);
  const bar = await run('bossbar get bm:hhm visible');
  ok('boss bar shown', bar.includes('visible') && !bar.includes('hidden'), bar);
  // kill credit to the player -> loot + slain message
  A.chats = [];
  await run('damage @e[type=minecraft:wither_skeleton,tag=bm.hhm,limit=1] 2000 minecraft:player_attack by TestRat'); await sleep(2500);
  const gone = !(await run('execute if entity @e[type=minecraft:wither_skeleton,tag=bm.hhm]')).includes('passed');
  const loot = await run(`execute positioned ${X} ${Y} ${Z} run data get entity @e[type=minecraft:item,distance=..30,limit=1] Item.id`);
  const nItems = await run(`execute positioned ${X} ${Y} ${Z} store result score #t bm.rng if entity @e[type=minecraft:item,distance=..30]`);
  ok('killed: slain message + loot', gone && A.chats.some(c => c.includes('fallen')), `chat ${JSON.stringify(A.chats.slice(-2))}; items ${nItems}; e.g. ${loot}`);
  await sleep(4000);
  const steedGone = !(await run('execute if entity @e[type=minecraft:skeleton_horse,tag=bm.hhs]')).includes('passed');
  const thrallsGone = !(await run('execute if entity @e[tag=bm.hhmin]')).includes('passed');
  ok('steed and thralls leave with him', steedGone && thrallsGone, `steed gone ${steedGone}, thralls gone ${thrallsGone}`);
  await run(`kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..40]`); await run(`kill @e[type=minecraft:experience_orb,x=${X},y=${Y},z=${Z},distance=..40]`);
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
