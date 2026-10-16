// v2.66: KillerWatt the follower - riding, wall climbing, the Thunder Leap, the tendril stab, the leap, chain lightning, gems and the Ethereal Form
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 18000, Y = 120, Z = 18000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const W = '@e[type=wolf,tag=bm.kxpet,limit=1]';
  const pos = async (sel) => { const o = await run(`data get entity ${sel} Pos`); const m = o.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const riding = async () => /passed/i.test(await run(`execute as TestRat on vehicle if entity @s[tag=bm.kxpet]`)) || /Test passed/.test(await run(`execute as TestRat on vehicle if entity @s[tag=bm.kxpet]`));
  const models = async () => (await run(`execute as @e[type=item_display,tag=bm.kxp_pet,tag=bm.kxp_body,limit=1] run data get entity @s item.components."minecraft:item_model"`)).replace(/.*data: /, '');
  const zombie = async (dx, dz, tag = 'bm.t79z') => run(`summon minecraft:zombie ${X + dx} ${Y} ${Z + dz} {Tags:["${tag}","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:20f}`);
  const clearMobs = async () => { await run(`kill @e[type=zombie,tag=bm.t79z]`); await run(`kill @e[type=#bm:hostile,x=${X - 40},y=${Y - 20},z=${Z - 40},dx=80,dy=60,dz=80,tag=!bm.npc]`); };
  await run(`forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`fill ${X - 24} ${Y - 1} ${Z - 24} ${X + 24} ${Y - 1} ${Z + 24} minecraft:stone`); await run(`fill ${X - 24} ${Y} ${Z - 24} ${X + 24} ${Y + 12} ${Z + 24} minecraft:air`);
  await run('weather clear'); await run('time set day'); await run('gamerule doMobSpawning false');
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.dmpet']) await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('scoreboard players set TestRat bm.kxcd 0'); await run('scoreboard players set TestRat bm.kxel 0'); await run('scoreboard players set TestRat bm.cosk 0');
  await run('loot replace entity TestRat container.9 loot bm:items/kw_spark'); await clearMobs(); await sleep(2500);
  await run('scoreboard players set TestRat bm.kxcd 0');            // (again: a KillerWatt left fainting by an earlier test lands its cooldown once you're back online)

  // ---- call him, climb on
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(1500);
  ok('The Spark calls KillerWatt', /\d/.test((await pos(W) || []).join()));
  await run(`tp ${W} ${X + 1.5} ${Y} ${Z + 0.5} -90 0`); await sleep(400);
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(600);
  ok('Beside him, the Spark puts you on his back', await riding());
  await sleep(400);
  ok('...he sits tight under you (Sitting) and grows a little (the seat at his shoulders)', /1b/.test(await run(`data get entity ${W} Sitting`)) && /0\.5/.test(await run(`attribute ${W} minecraft:scale modifier value get bm:kx_ride`)));
  // ---- steer: forward, facing east
  await run('rotate TestRat -90 0'); await sleep(300);
  const p0 = await pos(W);
  A.input({ forward: true }); await sleep(1600); A.input({}); await sleep(400);
  const p1 = await pos(W);
  ok('Walk: he strides where you look (east)', p1 && p0 && p1[0] - p0[0] > 4 && Math.abs(p1[2] - p0[2]) < 2, `${p0 && p0.map(v => v.toFixed(1))} -> ${p1 && p1.map(v => v.toFixed(1))}`);
  // ---- a wall: he climbs it
  await run(`execute as TestRat on vehicle run tp @s ${X - 12.5} ${Y} ${Z + 0.5} -90 0`); await sleep(500); await run('rotate TestRat -90 0'); await sleep(200);
  await run(`fill ${X - 6} ${Y} ${Z - 3} ${X - 5} ${Y + 5} ${Z + 3} minecraft:stone`);
  await run(`fill ${X - 6} ${Y + 6} ${Z - 3} ${X + 4} ${Y + 6} ${Z + 3} minecraft:stone`);
  let ymax = 0; A.input({ forward: true });
  for (let i = 0; i < 12; i++) { await sleep(200); const q = await pos(W); if (q) ymax = Math.max(ymax, q[1]); }
  A.input({}); await sleep(500);
  ok('A wall ahead: up it he goes, on his tendrils (and over the top)', ymax >= Y + 6.5, `top y ${ymax.toFixed(1)} (the ledge ${Y + 7})`);
  await run(`fill ${X - 24} ${Y} ${Z - 24} ${X + 24} ${Y + 12} ${Z + 24} minecraft:air`); await sleep(1500);
  await run(`execute as TestRat on vehicle run tp @s ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(800);
  ok('...(still riding after the climb)', await riding());
  // ---- THUNDER LEAP: the Spark, riding
  await zombie(6, 0); await sleep(300);
  const y0 = (await pos(W))[1];
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(350);
  const y1 = (await pos(W))[1];
  ok('Riding, the Spark: THUNDER LEAP - up he goes', y1 - y0 > 1.2, `${y0.toFixed(2)} -> ${y1.toFixed(2)}`);
  await sleep(2500);
  ok('...and lands with a slam (the leap ends)', !/kxleap/.test(await run(`data get entity ${W} Tags`)));
  await clearMobs();
  // ---- off
  A.input({ shift: true }); await sleep(600); A.input({}); await sleep(600);
  ok('Sneak: off his back - he stands up again', !(await riding()) && /0b/.test(await run(`data get entity ${W} Sitting`)) && !/kxrd/.test(await run(`data get entity ${W} Tags`)));

  // ---- the tendril stab: pinned, then two punches
  await run(`tp ${W} ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run(`tp TestRat ${X - 4.5} ${Y} ${Z + 0.5}`); await sleep(500);
  await zombie(2.5, 0.5); await sleep(200);
  await run(`execute as ${W} run scoreboard players set @s bm.kxatk 4`); await run(`execute as ${W} run scoreboard players set @s bm.kxt 0`); await sleep(350);
  const pinned = await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] active_effects');
  const hp1 = await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Health');
  ok('THE TENDRIL STAB: pinned (Slowness X) and stabbed', /slowness/.test(pinned) && /amplifier: 9b/.test(pinned) && +hp1.match(/([\d.]+)f/)[1] < 20, hp1.replace(/.*data: /, ''));
  await sleep(1100);
  const hp2 = await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Health');
  ok('...then a right and a left', !/\d/.test(hp2.replace(/.*data: /, '')) || +hp2.match(/([\d.]+)f/)[1] < +hp1.match(/([\d.]+)f/)[1] - 3, `${hp1.replace(/.*data: /, '')} -> ${hp2.replace(/.*data: /, '')}`);
  await clearMobs(); await sleep(300);
  // ---- chain lightning: three foes at once
  for (const [dx, dz] of [[6, 2], [6, -2], [8, 0]]) await zombie(dx, dz);
  await sleep(200);
  await run(`data modify entity ${W} Sitting set value 1b`);
  await run(`execute as ${W} run scoreboard players set @s bm.kxatk 6`); await run(`execute as ${W} run scoreboard players set @s bm.kxt 0`); await sleep(900);
  await run(`data modify entity ${W} Sitting set value 0b`);
  const hurt = (await run('execute as @e[type=zombie,tag=bm.t79z] run data get entity @s Health')).match(/([\d.]+)f/g) || [];
  ok('CHAIN LIGHTNING: arcs to three foes', hurt.length === 3 && hurt.every(h => parseFloat(h) < 20), hurt.join(' '));
  await clearMobs(); await sleep(300);
  // ---- the leap: up and down on a foe a little way off
  await run(`tp ${W} ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await zombie(7.5, 0.5); await sleep(200);
  await run(`execute as ${W} run scoreboard players set @s bm.kxatk 5`); await run(`execute as ${W} run scoreboard players set @s bm.kxt 0`); await sleep(500);
  const ly = (await pos(W))[1];
  await sleep(2600);
  const lp = await pos(W); const zh = await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Health');
  ok('THE LEAP: up, over, and down on it', ly > Y + 0.8 && lp[0] > X + 3 && (!/\d/.test(zh.replace(/.*data: /, '')) || +zh.match(/([\d.]+)f/)[1] < 20),
     `air y ${ly.toFixed(1)} land x ${lp[0].toFixed(1)} zombie ${zh.replace(/.*data: /, '')}`);
  await clearMobs();

  // ---- gems
  await run(`tp ${W} ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run(`tp TestRat ${X - 1.5} ${Y} ${Z + 0.5} -90 0`); await sleep(400);
  await run('item replace entity TestRat weapon.mainhand with air'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/gem_fire'); await sleep(150);
  await run('advancement grant TestRat only bm:p79/pet_interact'); await sleep(300);
  ok('A Fire Gem: his element is fire (the gem is used up)', (await sc('TestRat', 'bm.kxel')) === 1 && /kw_body_fire/.test(await models()) &&
     !/gem_fire/.test(await run('data get entity TestRat SelectedItem')), await models());
  for (const o of ['bm.kxho', 'bm.kxou', 'bm.kxatk']) await run(`scoreboard players set ${W} ${o} 0`); await run(`tag ${W} remove bm.kxsw`); await sleep(300);
  await zombie(4.0, 0.5); await sleep(200);           // (in stab reach, but out of his own tendril-swipe reach - a swipe would cut the stab short)
  await run(`execute as ${W} run scoreboard players set @s bm.kxatk 4`); await run(`execute as ${W} run scoreboard players set @s bm.kxt 0`); await sleep(450);
  const fire = await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Fire');
  if (process.env.DBG) { console.log('DBG', await run(`data get entity ${W} Tags`), await run(`scoreboard players get ${W} bm.kxatk`), await run(`scoreboard players get ${W} bm.kxt`), await run(`scoreboard players get ${W} bm.kxel`),
    (await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Health')).replace(/.*data: /, ''), await run('execute store result score #t bm.rng if entity @e[type=zombie,tag=bm.t79z]'), await run(`data get entity ${W} Pos`), await run('data get entity @e[type=zombie,tag=bm.t79z,limit=1] Pos')); }
  ok('...and his blows burn', /(\d+)s/.test(fire) && +fire.match(/(-?\d+)s/)[1] > 0, fire.replace(/.*data: /, ''));
  await clearMobs();
  await run('item replace entity TestRat weapon.mainhand with air'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/gem_electric'); await sleep(150);
  await run('advancement grant TestRat only bm:p79/pet_interact'); await sleep(300);
  ok('The Electric Gem: refused - he IS electricity (you keep it)', /gem_electric/.test(await run('data get entity TestRat SelectedItem')) && (await sc('TestRat', 'bm.kxel')) === 1);
  await run('item replace entity TestRat weapon.mainhand with air');
  A.input({ shift: true }); await sleep(300); await run('advancement grant TestRat only bm:p79/pet_interact'); await sleep(300); A.input({}); await sleep(300);
  ok('Sneak + right-click empty-handed: the gem back, green and gold again', (await sc('TestRat', 'bm.kxel')) === 0 && /"bm:kw_body"/.test(await models()) &&
     /Found 1/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"gem_fire"}] 0')), await models());
  // ---- the Ethereal Form
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/ethereal_gem'); await sleep(150);
  await run('advancement grant TestRat only bm:p79/pet_interact'); await sleep(1300);
  ok('The Ethereal Gem: his ETHEREAL FORM (black steel, iridescent, spiked)', (await sc('TestRat', 'bm.kxel')) === 10 && /kw_body_eth/.test(await models()), await models());
  ok('...he floats (no falling)', /slow_falling/.test(await run(`data get entity ${W} active_effects`)));
  await zombie(-21.5, 0.5); await sleep(200);
  await run(`execute as @e[type=zombie,tag=bm.t79z,limit=1] run tag @s add bm.t79h`);
  await run(`execute as ${W} run tag @s add bm.kxme`); await run('scoreboard players set #kel bm.rng 10');
  await run('execute as @e[type=zombie,tag=bm.t79h,limit=1] at @s run function bm:p79/pet/hit8'); await run(`execute as ${W} run tag @s remove bm.kxme`);
  const eh = await run('data get entity @e[type=zombie,tag=bm.t79h,limit=1] Health');
  ok('...half again as strong (an 8 hits for 12)', +eh.match(/([\d.]+)f/)[1] <= 9.5, eh.replace(/.*data: /, ''));
  await clearMobs();
  // ridden, he flies
  await run(`tp ${W} ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run(`tp TestRat ${X - 1.5} ${Y} ${Z + 0.5} -90 -60`); await sleep(500);
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(500);
  await run('rotate TestRat -90 -60'); await sleep(200);
  const fy0 = (await pos(W))[1];
  // (riding as a client does: where it looks and what it presses, every tick - the flight follows the look)
  for (let i = 0; i < 30; i++) { A.write('look', { yaw: -90, pitch: -60, flags: { onGround: false, hasHorizontalCollision: false } }); A.write('player_input', { inputs: { forward: true } }); A.write('tick_end', {}); await sleep(50); }
  A.write('player_input', { inputs: {} }); await sleep(300);
  const fy1 = (await pos(W))[1];
  await run('rotate TestRat -90 0'); await sleep(400);
  const fy1b = (await pos(W))[1]; await sleep(1000);
  const fy2 = (await pos(W))[1];
  ok('...look level: he hovers (no falling)', Math.abs(fy2 - fy1b) < 0.6, `${fy1b.toFixed(2)} -> ${fy2.toFixed(2)}`);
  A.input({ shift: true }); await sleep(600); A.input({}); await sleep(600);
  ok('...off his back: no flying without a rider', !(await riding()) && !/1b/.test(await run(`data get entity ${W} NoGravity`)), (await run(`data get entity ${W} NoGravity`)).replace(/.*data: /, ''));
  // ---- climbing to you
  await run(`fill ${X + 3} ${Y} ${Z - 3} ${X + 4} ${Y + 3} ${Z + 3} minecraft:stone`);
  await run(`execute as TestRat run attribute @s minecraft:fall_damage_multiplier base set 0`);
  await run(`tp TestRat ${X + 4.5} ${Y + 4} ${Z + 0.5}`); await run(`tp ${W} ${X + 2.4} ${Y} ${Z + 0.5} -90 0`); await sleep(400);
  await run(`execute as ${W} run data modify entity @s Sitting set value 0b`);
  const cy0 = (await pos(W))[1]; let cy1 = 0; for (let i = 0; i < 12; i++) { await sleep(250); const q = await pos(W); if (q) cy1 = Math.max(cy1, q[1]); }
  ok("You're up a wall: he climbs it to you (up onto your ledge)", cy1 >= Y + 3.9, `${cy0.toFixed(1)} -> ${cy1.toFixed(1)} (ledge ${Y + 4})`);
  await run(`execute as TestRat run attribute @s minecraft:fall_damage_multiplier base set 1`);
  // ---- tidy
  await run('scoreboard players set TestRat bm.kxel 0');
  await run('scoreboard players set TestRat bm.gvhc 0'); A.input({ shift: true }); await sleep(200); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(300); A.input({});
  await run(`forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
