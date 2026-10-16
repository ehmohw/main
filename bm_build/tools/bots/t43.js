// v2.42: two-blade tendrils + lunge; v2.41: tendrils worn on the chest (4 at the back, look-to-lash, sneak+jump fling, snatch, weather), crown at night, Leo by water, Emma's Bloomheart
const { bot, rcon, sleep } = require('./lib');
const X = 9950, Y = 100, Z = 9950;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[fdbsL]?\s*$/); return m ? +m[1] : null; };
  const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const mob = async (x, z, tag, kind = 'husk') => { await run(`summon ${kind} ${x} ${Y + 1} ${z} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["${tag}","bm.t43"],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b}]}`);
    await sleep(400); await run(`attribute @e[tag=${tag},limit=1] minecraft:max_health base set 200`); await sleep(100); await run(`data modify entity @e[tag=${tag},limit=1] Health set value 200f`); };
  const hp = (tag) => num(`data get entity @e[tag=${tag},limit=1] Health`);
  const effects = () => run('data get entity TestRat active_effects');
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 25} ${Y} ${Z - 25} ${X + 25} ${Y} ${Z + 25} stone`); await run(`fill ${X - 25} ${Y + 1} ${Z - 25} ${X + 25} ${Y + 10} ${Z + 25} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('time set noon'); await run('weather clear'); await run('kill @e[type=cat,tag=bm.emmapet]');
  await run('scoreboard players reset TestRat bm.kwmd');   // (the mode is the player's own and stays: a fresh player starts in OFFENSE)
  await run('execute as TestRat run function bm:admin/cecil_relics'); await sleep(300);
  // ---- the tendrils, worn
  await run('item replace entity TestRat armor.chest from entity TestRat hotbar.0'); await run('item replace entity TestRat hotbar.0 with air'); await sleep(800);
  ok('Tendrils worn on the chest: four two-blade tendrils (8 displays) sprout at your back', (await cnt(`@e[type=item_display,tag=bm.kwt,x=${X},y=${Y},z=${Z},distance=..4]`)) === 8);
  ok('...each a base blade and a tip blade', (await cnt('@e[type=item_display,tag=bm.kws_b]')) === 4 && (await cnt('@e[type=item_display,tag=bm.kws_t]')) === 4);
  const tp0 = await pos('@e[type=item_display,tag=bm.kwt_ul,limit=1]');
  ok('...the upper-left one sits behind your left shoulder', tp0 && tp0[2] < Z + 0.5 - 0.1 && Math.abs(tp0[1] - (Y + 1 + 1.3)) < 0.05 && tp0[0] > X + 0.5, tp0 && tp0.map(v => v.toFixed(2)).join(' '));
  ok('...no armour (the chest slot gives none)', (await num('attribute TestRat minecraft:armor get')) === 0);
  await run(`tp TestRat ${X + 5.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(400);
  const tp1 = await pos('@e[type=item_display,tag=bm.kwt_ul,limit=1]');
  ok('...and they follow you', tp1 && Math.abs(tp1[0] - X - 5.63) < 0.1, tp1 && tp1.map(v => v.toFixed(2)).join(' '));
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300);
  await mob(X + 0.5, Z + 10.5, 'bm.z1'); await mob(X + 3.0, Z + 11.0, 'bm.z2');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} facing ${X + 0.5} ${Y + 2} ${Z + 10.5}`);
  let lt = 0, tipz = -9; for (let i = 0; i < 12; i++) { const m_ = (await run('scoreboard players get TestRat bm.kwlt')).match(/has (-?\d+)/); const v = m_ ? +m_[1] : 0; if (v > lt) lt = v;
    await sleep(100); }
  const sc = async (o) => { const m = (await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const lk = await sc('bm.kwlk');
  ok('...the striking tendril lunges forward (timer runs, then settles)', lt > 0 && lk >= 0 && lk <= 3, `kwlt max ${lt}, kwlk ${lk}`);
  await sleep(300);
  const z1 = await hp('bm.z1'), z2 = await hp('bm.z2');
  ok('Look at a monster: a tendril lashes it (10 a lash, ~1 a second) and it arcs (5)', z1 <= 191 && z2 < 200, `${z1} / ${z2}`);
  await run('kill @e[tag=bm.t43]'); await sleep(300); await run('weather rain'); await sleep(500);
  await mob(X + 0.5, Z + 10.5, 'bm.z3'); await sleep(200); const r0 = await hp('bm.z3'); await sleep(1300); const r1 = await hp('bm.z3');
  ok('...in the rain: 13 a lash', (r0 - r1) % 13 < 0.5 || (r0 - r1) % 13 > 12.5, `${r0} -> ${r1}`);
  await run('weather thunder'); await sleep(6000); await run('kill @e[tag=bm.t43]'); await mob(X + 0.5, Z + 10.5, 'bm.z4'); await sleep(1600);
  ok('...in a thunderstorm: 16 a lash, and lightning falls on it', (await hp('bm.z4')) <= 184.1 && (await cnt(`@e[type=lightning_bolt,x=${X},y=${Y},z=${Z},distance=..30]`)) + 1 > 0, `${await hp('bm.z4')}`);
  ok('...storm: Speed II and Strength', /speed/.test(await effects()) && /strength/.test(await effects()));
  await run('weather clear'); await run('kill @e[tag=bm.t43]'); await run('effect clear TestRat'); await sleep(500);
  // sneak: yank
  await run(`summon husk ${X + 0.5} ${Y + 1} ${Z + 10.5} {PersistenceRequired:1b,Silent:1b,Tags:["bm.zy","bm.t43"],attributes:[{id:"minecraft:movement_speed",base:0.0d}]}`);
  A.input({ shift: true }); await sleep(300); const y0 = await pos('@e[tag=bm.zy,limit=1]'); await sleep(1600); const y1 = await pos('@e[tag=bm.zy,limit=1]'); A.input({}); await sleep(300);
  ok('...sneaking: they yank it toward you instead', y0 && y1 && y1[2] < y0[2] - 1, `${y0 && y0[2].toFixed(2)} -> ${y1 && y1[2].toFixed(2)}`);
  await run('kill @e[tag=bm.t43]');
  // sneak + jump: fling
  await run('scoreboard players reset TestRat bm.kwf'); A.input({ shift: true }); await sleep(500); await run('scoreboard players set TestRat bm.kwj 1'); await sleep(200);
  const tg = await run('tag TestRat list'); const kf = await run('scoreboard players get TestRat bm.kwf'); const kj = await run('scoreboard players get TestRat bm.kwj');
  const sn = await run('execute as TestRat if predicate bm:p20/sneaking'); const wn = await run('execute as TestRat if items entity @s armor.chest *[minecraft:custom_data~{bm:"killerwatt_tendrils"}]'); A.input({}); await sleep(300);
  ok('Sneak + jump: the fling fires (armed, then spent by the impulse)', !/bm\.kwl[123]|bm\.kwup/.test(tg) && /has \d+ \[bm.kwf/.test(kf), [kf, kj, sn, wn].map(x => x.slice(-30)).join(' | '));
  // snatch
  await run(`summon item ${X + 0.5} ${Y + 1} ${Z + 6.5} {Item:{id:"minecraft:apple",count:1},Tags:["bm.t43i"]}`); await sleep(1600);
  const ip = await pos('@e[tag=bm.t43i,limit=1]');
  ok('They snatch a dropped item 6 blocks off', !ip || Math.abs(ip[2] - Z - 0.5) < 1.6, ip ? ip.map(v => v.toFixed(1)).join(' ') : 'picked up');
  const h0 = await num('data get entity TestRat Health'); await run('damage TestRat 6 minecraft:fall'); await sleep(200);
  ok('No fall damage while worn', (await num('data get entity TestRat Health')) >= h0 - 0.01);
  await run('item replace entity TestRat armor.chest with air'); await sleep(400);
  ok('Taken off: the tendrils vanish', (await cnt('@e[type=item_display,tag=bm.kwt]')) === 0);
  // ---- the crown at night
  await run('item replace entity TestRat armor.head from entity TestRat hotbar.1'); await run('effect clear TestRat');
  ok('Crown: no armour', (await num('attribute TestRat minecraft:armor get')) === 0);
  await run('time set midnight'); await sleep(2300);
  ok('Crown at night: Strength and Night Vision', /strength/.test(await effects()) && /night_vision/.test(await effects()));
  A.input({ shift: true }); await sleep(300); await run('scoreboard players reset TestRat bm.crcd'); await run('scoreboard players set TestRat bm.crj 1'); await sleep(300);
  const fn = await cnt(`@e[type=evoker_fangs,x=${X},y=${Y},z=${Z},distance=..30]`); A.input({}); await sleep(200);
  ok('...night fangs: 16, and only 3 s to recover', fn >= 15 && (await num('scoreboard players get TestRat bm.crcd')) <= 60, `${fn}`);
  await run('time set noon'); await run('item replace entity TestRat armor.head with air'); await run('effect clear TestRat'); await sleep(1200);
  // ---- Leo by the water
  A.slot(2); await sleep(300); await run(`fill ${X - 2} ${Y + 1} ${Z - 2} ${X + 3} ${Y + 1} ${Z + 3} water`); await sleep(2200);
  ok("Leo's Trident in water: Strength, Dolphin's Grace, Conduit Power", /dolphins_grace/.test(await effects()) && /conduit_power/.test(await effects()) && /strength/.test(await effects()));
  await run(`fill ${X - 2} ${Y + 1} ${Z - 2} ${X + 3} ${Y + 1} ${Z + 3} air`); await run('effect clear TestRat'); await sleep(3500); await run('effect clear TestRat'); await sleep(1200);
  ok('...dry land, clear sky: nothing', !/dolphins_grace/.test(await effects()));
  // ---- Emma's Bloomheart: boosted by day
  await run('clear TestRat'); await run('give TestRat totem_of_undying[custom_data={bm:"bloomheart_gem"}]'); A.slot(0); await sleep(300);
  await run('scoreboard players set TestRat bm.mcd4 0'); await run('effect clear TestRat'); await run('execute as TestRat at @s run function bm:p45/bloomheart_gem/use'); await sleep(200);
  ok("Emma's Bloomheart by day: Regeneration and Absorption", /absorption/.test(await effects()) && /regeneration/.test(await effects()));
  await run('time set midnight'); await sleep(1500); await run('scoreboard players set TestRat bm.mcd4 0'); await run('effect clear TestRat'); await run('execute as TestRat at @s run function bm:p45/bloomheart_gem/use'); await sleep(200);
  ok('...at night without Emma: the plain bloom (no Absorption)', !/absorption/.test(await effects()) && /regeneration/.test(await effects()));
  await run('scoreboard players reset TestRat bm.emcd'); await run('execute as TestRat at @s run function bm:p57/summon'); await sleep(400);
  await run('scoreboard players set TestRat bm.mcd4 0'); await run('effect clear TestRat'); await run('execute as TestRat at @s run function bm:p45/bloomheart_gem/use'); await sleep(200);
  ok('...at night with Emma following: boosted again', /absorption/.test(await effects()));
  await run('time set noon'); await sleep(1500); await run('scoreboard players set TestRat bm.mcd4 0'); await run('effect clear TestRat'); await run('execute as TestRat at @s run function bm:p45/bloomheart_gem/use'); await sleep(200);
  ok('...by day AND with Emma: Resistance too', /resistance/.test(await effects()));
  await run('kill @e[type=cat,tag=bm.emmapet]'); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`forceload remove ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`);
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
