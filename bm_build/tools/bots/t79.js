// v2.65: KillerWatt - the Storm Effigy, the boss (rig, animation, attacks, roar, reward), the Spark follower, Cecil's shop
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 17000, Y = 120, Z = 17000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '') + (process.env.BARS ? '  [bars ' + JSON.stringify(A.bars.splice(0)) + ']' : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async (sel) => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed|No entity/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const has = async iid => { const n = await num(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`); return isNaN(n) ? 0 : n; };
  const hp = async () => { const o = await run('data get entity TestRat Health'); const m = o.match(/([\d.]+)f/); return m ? +m[1] : NaN; };
  const press = async (sneak) => { await run('scoreboard players set TestRat bm.gvhc 0'); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.use(); await sleep(300); A.release(); if (sneak) A.input({}); await sleep(500); };
  const hold = async iid => { await run(`item replace entity TestRat weapon.mainhand with air`); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${iid}`); await sleep(150); };
  const heal = async () => { await run('effect give TestRat minecraft:instant_health 1 10 true'); await run('effect give TestRat minecraft:saturation 1 10 true'); await sleep(300); };
  const BOSS = '@e[type=husk,tag=bm.kxboss,limit=1]';
  // (the server eases into and out of a storm over a few seconds: wait until it really is / isn't thundering)
  const weather = async thunder => { await run(thunder ? 'weather thunder 6000' : 'weather clear');
    for (let i = 0; i < 40; i++) { const o = await run('execute if predicate bm:p79/thunder'); if (/passed/.test(o) === thunder) break; await sleep(300); } await sleep(200); };
  const part = p => `@e[type=item_display,tag=bm.kxp_${p},tag=bm.kxp_boss,tag=!bm.kxdying,limit=1]`;
  // an open field, high up: stone floor, nothing over it
  await run(`forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`fill ${X - 30} ${Y - 1} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:stone`);
  await run(`fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 12} ${Z + 30} minecraft:air`);
  await run('kill @e[type=husk,tag=bm.kxboss]'); await run('kill @e[type=item_display,tag=bm.kxp]'); await run('kill @e[type=wolf,tag=bm.kxpet]');
  await run('kill @e[type=marker,tag=bm.kxcall]'); await run('kill @e[type=marker,tag=bm.kxstrike]'); await run('kill @e[type=vex,tag=bm.kxwisp]');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('scoreboard players reset TestRat bm.kxk');
  await run('scoreboard players reset TestRat bm.kxcd'); await sleep(1500);

  // ---- the Effigy: only in a thunderstorm, only under the open sky
  await weather(false);
  await hold('kw_effigy'); await press(false);
  ok('Clear sky: the Effigy does nothing (and is not used up)', (await cnt('@e[type=marker,tag=bm.kxcall]')) === 0 && (await has('kw_effigy')) === 1);
  await weather(true);
  await run(`setblock ${X} ${Y + 3} ${Z} minecraft:stone`);
  await press(false);
  ok('Under a roof: nothing', (await cnt('@e[type=marker,tag=bm.kxcall]')) === 0 && (await has('kw_effigy')) === 1);
  await run(`setblock ${X} ${Y + 3} ${Z} minecraft:air`);
  // (a little hill where he'll land: the spot rises out of it)
  await run(`fill ${X - 1} ${Y} ${Z + 8} ${X + 1} ${Y + 1} ${Z + 10} minecraft:dirt`);
  await press(false);
  const mk = await run('data get entity @e[type=marker,tag=bm.kxcall,limit=1] Pos');
  ok('Thunderstorm + open sky: the storm gathers (Effigy used)', (await cnt('@e[type=marker,tag=bm.kxcall]')) === 1 && (await has('kw_effigy')) === 0, mk.replace(/.*data: /, ''));
  const mp = (mk.match(/[-\d.]+(?=d)/g) || []).map(Number);
  ok('...nine blocks ahead, standing on the ground (up out of the hill)', Math.abs(mp[1] - (Y + 2)) < 0.01 && Math.abs(mp[2] - (Z + 9.5)) < 0.01, mk.replace(/.*data: /, ''));
  await run(`fill ${X - 1} ${Y} ${Z + 8} ${X + 1} ${Y + 1} ${Z + 10} minecraft:air`);
  await run('execute as @e[type=marker,tag=bm.kxcall] at @s run tp @s ~ ' + Y + ' ~');
  await hold('kw_effigy'); await press(false);
  ok('A second Effigy while the storm gathers: refused', (await cnt('@e[type=marker,tag=bm.kxcall]')) === 1 && (await has('kw_effigy')) === 1);
  await sleep(5200);
  ok('Five seconds later KillerWatt crashes down', (await cnt('@e[type=husk,tag=bm.kxboss]')) === 1 && (await cnt('@e[type=marker,tag=bm.kxcall]')) === 0);
  const kid = await num(`scoreboard players get ${BOSS} bm.kxid`);
  const parts = await num(`execute store result score #t bm.rng if entity @e[type=item_display,tag=bm.kxp_boss,scores={bm.kxid=${kid}}]`);
  ok('...an eight-part rig, linked to him', parts === 8, `kid ${kid}, parts ${parts}`);
  const sc = await run(`data get entity ${BOSS} attributes`);
  const bbp = await run('bossbar get bm:kwb players');
  ok('...big (scale 2.4), 500 health, the bossbar shows', /scale.*?2\.4/.test(sc) && /max_health.*?500/.test(sc) && /TestRat/.test(bbp), sc.slice(0, 260) + ' | ' + bbp);
  await hold('kw_effigy'); await press(false);
  ok('Another Effigy while he is here: refused', (await cnt('@e[type=husk,tag=bm.kxboss]')) === 1 && (await has('kw_effigy')) === 1);
  // (hold him still from here: we drive his attacks ourselves)
  await run(`data merge entity ${BOSS} {NoAI:1b}`); await run(`tp ${BOSS} ${X + 0.5} ${Y} ${Z + 8.5} 180 0`); await sleep(400);
  const bpos = await run(`data get entity ${BOSS} Pos`); const hpos = await run(`data get entity ${part('head')} Pos`);
  const by = +bpos.match(/,\s*([-\d.]+)d,/)[1], hy = +hpos.match(/,\s*([-\d.]+)d,/)[1];
  ok('The rig stands on him: head joint about 2.8 blocks up', Math.abs(hy - by - 29 * 1.55 / 16) < 0.15, `${by} / ${hy}`);
  // smooth idle: the pose changes, and every change interpolates
  const r0 = await run(`data get entity ${part('body')} transformation.left_rotation`); await sleep(1700);
  const r1 = await run(`data get entity ${part('body')} transformation.left_rotation`);
  const idur = await num(`data get entity ${part('body')} interpolation_duration`);
  ok('He breathes and sways standing (idle poses, 30-tick blends)', r0 !== r1 && idur === 30, `${r0.replace(/.*: /, '')} -> ${r1.replace(/.*: /, '')}`);

  // ---- THUNDER SLAM
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 5.5} 0 0`); await heal(); await run(`scoreboard players set ${BOSS} bm.kxc 999`);
  await run(`execute as ${BOSS} run function bm:p79/boss/go {a:1}`); await sleep(250);
  const flex = await run(`data get entity ${part('armr')} item.components."minecraft:item_model"`);
  ok('Thunder Slam: arms up - the bent-elbow arms', /kw_armr_flex/.test(flex), flex.replace(/.*: /, ''));
  const h0 = await hp(); await sleep(1300);
  const h1 = await hp(); const unflex = await run(`data get entity ${part('armr')} item.components."minecraft:item_model"`);
  ok('...then down: the quake hurts you (and the arms straighten)', h1 < h0 - 3 && /"bm:kw_armr"/.test(unflex), `${h0} -> ${h1}`);
  await sleep(300);
  ok('...and he goes back to standing', (await num(`scoreboard players get ${BOSS} bm.kxatk`)) === 0);
  // ---- TENDRIL SWEEP (wider: 6 blocks off still gets it)
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 2.5} 0 0`); await heal();
  const s0 = await hp(); await run(`execute as ${BOSS} run function bm:p79/boss/go {a:2}`); await sleep(900);
  ok('Tendril Sweep: hits six blocks out', (await hp()) < s0 - 3, `${s0} -> ${await hp()}`);
  await sleep(800);
  // ---- CALL LIGHTNING: dodge it...
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 6.5} 0 0`); await heal(); await sleep(300);
  await run(`execute as ${BOSS} run function bm:p79/boss/go {a:3}`); await sleep(650);
  const strikes = await cnt('@e[type=marker,tag=bm.kxstrike]');
  ok('Call Lightning: sparks gather under you', strikes === 1 && (await cnt(`@e[type=marker,tag=bm.kxstrike,x=${X + 0.5},y=${Y},z=${Z - 6.5},distance=..1.5]`)) === 1, `${strikes}`);
  await run(`kill @e[type=#bm:hostile,tag=!bm.kxboss,tag=!bm.kxwisp,x=${X},y=${Y},z=${Z},distance=..48]`);
  await run(`tp TestRat ${X + 6.5} ${Y} ${Z - 6.5}`); const d0 = await hp(); await sleep(1600);
  ok('...step away and the bolt misses', (await cnt('@e[type=marker,tag=bm.kxstrike]')) === 0 && (await hp()) >= d0, `${d0} -> ${await hp()}`);
  await sleep(800);
  // ...or don't
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 6.5}`); await heal(); await sleep(300); const c0 = await hp();
  await run(`execute as ${BOSS} run function bm:p79/boss/go {a:3}`); await sleep(2200);
  ok('...stay put and it lands on you', (await hp()) < c0 - 3, `${c0} -> ${await hp()}`);
  await sleep(600);
  // ---- THE ROAR at half health: thrown up, three Static Wisps, enraged
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 4.5} 0 0`); await heal();
  await run(`data merge entity ${BOSS} {Health:240f}`); await run(`scoreboard players set ${BOSS} bm.kxc 1`); await sleep(750);
  const lev = await run('data get entity TestRat active_effects');
  ok('At half health he roars (enraged from now on)', (await num(`scoreboard players get ${BOSS} bm.kxr`)) === 1, `atk ${await num(`scoreboard players get ${BOSS} bm.kxatk`)}`);
  ok('...three Static Wisps, and you are thrown up', (await cnt('@e[type=vex,tag=bm.kxwisp]')) === 3 && /levitation/.test(lev), `${await cnt('@e[type=vex,tag=bm.kxwisp]')} ${lev.slice(-120)}`);
  await sleep(1500); await run(`scoreboard players set ${BOSS} bm.kxc 999`);
  // enraged slam: bolts come down round him too
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 2.5} 0 0`); await heal(); await sleep(200);
  await run(`execute as ${BOSS} run function bm:p79/boss/go {a:1}`); await sleep(1000);
  ok('Enraged, his slam calls four bolts round him', (await cnt('@e[type=marker,tag=bm.kxstrike]')) === 4);
  await sleep(1800);
  // ---- he falls: the reward
  await run('clear TestRat'); await heal();
  await run(`damage ${BOSS} 9999 minecraft:player_attack by TestRat`); await sleep(600);
  ok('Brought down: his Tendrils and his Spark (certain, the first time)', (await has('killerwatt_tendrils')) === 1 && (await has('kw_spark')) === 1);
  ok('...and Medallions, a Trophy, Tokens', (await has('medallion')) >= 3 && (await has('trophy')) >= 1 && (await has('token')) >= 4);
  ok('...his rig crumples (the fall pose) and fades', (await cnt('@e[type=item_display,tag=bm.kxdying]')) === 8);
  await sleep(2600);
  ok('...gone in a couple of seconds; the wisps too', (await cnt('@e[type=item_display,tag=bm.kxp]')) === 0 && (await cnt('@e[type=vex,tag=bm.kxwisp]')) === 0 &&
     (await num('scoreboard players get TestRat bm.kxk')) === 1);
  // ---- he leaves if nobody's near for a minute
  await run('execute as TestRat at @s run function bm:admin/killerwatt'); await sleep(800);
  await run(`scoreboard players set ${BOSS} bm.kxlone 59`); await run(`data merge entity ${BOSS} {NoAI:1b}`);
  await run(`tp TestRat ${X + 110.5} ${Y + 20} ${Z + 0.5}`); await sleep(2200);
  ok('Alone for a minute: he leaves (quietly - no fall)', (await cnt('@e[type=husk,tag=bm.kxboss]')) === 0 && (await cnt('@e[type=item_display,tag=bm.kxp]')) === 0);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1000);

  // ---- THE SPARK: a follower (clear skies now - a dark stormy platform grows its own monsters, which he'd go for first)
  await weather(false); await run(`kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..48]`);
  await run('scoreboard players set TestRat bm.kxcd 0'); await hold('kw_spark'); await press(false); await sleep(400);
  const own = await run('data get entity @e[type=wolf,tag=bm.kxpet,limit=1] Owner');
  const pk = await num('scoreboard players get @e[type=wolf,tag=bm.kxpet,limit=1] bm.kxid');
  ok('The Spark: KillerWatt comes as a follower (yours, with his own rig)', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 1 && /\[I;/.test(own) &&
     (await num(`execute store result score #t bm.rng if entity @e[type=item_display,tag=bm.kxp_pet,scores={bm.kxid=${pk}}]`)) === 8);
  const php = await run('data get entity @e[type=wolf,tag=bm.kxpet,limit=1] Health');
  ok('...with 80 health (a tamed wolf would reset to 8)', +((php.match(/([\d.]+)f/) || [0, 0])[1]) >= 70, php.replace(/.*data: /, ''));
  const ps = await num(`data get entity @e[type=item_display,tag=bm.kxp_pet,tag=bm.kxp_body,limit=1] transformation.scale[0] 100`);
  ok('...smaller than the boss', ps >= 104 && ps <= 105, `${ps}`);
  await run('scoreboard players set #fc bm.rng 0'); await run('tag TestRat add bm.fcme'); await run('function bm:p58/count'); await run('tag TestRat remove bm.fcme');
  ok('...he counts toward the three-follower limit', (await num('scoreboard players get #fc bm.rng')) >= 1);
  await run(`tp @e[type=wolf,tag=bm.kxpet] ${X + 14.5} ${Y} ${Z + 0.5}`); await sleep(300); await press(false); await sleep(300);
  ok('Use again: he comes to you', (await cnt('@e[type=wolf,tag=bm.kxpet,distance=..3]'.replace('@e[', `@e[x=${X + 0.5},y=${Y},z=${Z + 0.5},`))) === 1);
  // fights: a slam on what's close
  await run('data merge entity @e[type=wolf,tag=bm.kxpet,limit=1] {Sitting:1b}');
  await run(`summon minecraft:zombie ${X + 2.5} ${Y} ${Z + 0.5} {Tags:["bm.kxtz","bm.seen"],NoAI:1b,PersistenceRequired:1b}`);
  await run(`tp @e[type=wolf,tag=bm.kxpet] ${X + 0.5} ${Y} ${Z + 0.5}`); await run('data merge entity @e[type=wolf,tag=bm.kxpet,limit=1] {Sitting:0b}');
  await run('scoreboard players set @e[type=wolf,tag=bm.kxpet] bm.kxc 1'); await sleep(1500);
  const zh = await run('data get entity @e[type=zombie,tag=bm.kxtz,limit=1] Health');
  ok('He slams a monster that comes close', /No entity/.test(zh) || +((zh.match(/([\d.]+)f/) || [0, 20])[1]) <= 13, zh.replace(/.*data: /, ''));
  await run('execute as @e[type=zombie,tag=bm.kxtz] run tp @s ~ -400 ~'); await run('kill @e[type=zombie,tag=bm.kxtz]'); await sleep(1200);
  // ...and calls lightning onto one further off
  await run(`kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..48]`);
  await run(`summon minecraft:zombie ${X + 11.5} ${Y} ${Z + 0.5} {Tags:["bm.kxtz","bm.seen"],NoAI:1b,PersistenceRequired:1b}`);
  await run('scoreboard players set @e[type=wolf,tag=bm.kxpet] bm.kxc 1'); await run('scoreboard players set @e[type=wolf,tag=bm.kxpet] bm.kxatk 0'); await sleep(2400);
  const zh2 = await run('data get entity @e[type=zombie,tag=bm.kxtz,limit=1] Health');
  ok('...and calls lightning onto one further off', /No entity/.test(zh2) || +((zh2.match(/([\d.]+)f/) || [0, 20])[1]) <= 13, zh2.replace(/.*data: /, ''));
  await run('kill @e[type=zombie,tag=bm.kxtz]');
  // home, quietly
  await press(true); await sleep(400);
  ok('Sneak + use: his wardrobe opens (2.67)', /has 9900/.test(await run('scoreboard players get TestRat bm.menu')));
  await run('scoreboard players set TestRat bm.act 9900'); await sleep(600);
  ok('...Send him home: he goes (no fall, no cooldown)', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 0 && (await cnt('@e[type=item_display,tag=bm.kxp]')) === 0 &&
     !((await num('scoreboard players get TestRat bm.kxcd')) > 0));
  // put the Spark away: he heads home
  await press(false); await sleep(400);
  await run('clear TestRat *[minecraft:custom_data~{bm:"kw_spark"}]'); await sleep(4500);
  ok('Put the Spark away: he heads home', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 0);
  // he falls: five minutes
  await hold('kw_spark'); await press(false); await sleep(400);
  await run('kill @e[type=wolf,tag=bm.kxpet]'); await sleep(1000);
  ok('If he falls: his rig crumples, and the Spark rests five minutes', (await cnt('@e[type=item_display,tag=bm.kxdying]')) === 8 && (await num('scoreboard players get TestRat bm.kxcd')) >= 295);
  await press(false); await sleep(300);
  ok('...he will not come while it recharges', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 0);
  // never into the vault
  await run('scoreboard players set TestRat bm.kxcd 0');
  // (the vault sends a player who isn't on a heist straight back out, so check the gate from inside it directly)
  await run('execute in bm:gutter positioned 5000 100 5000 as TestRat run function bm:p79/pet/try'); await sleep(300);
  ok('The Spark will not answer in the vault', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 0);
  await run('execute in bm:hollow_throne positioned 0 100 0 as TestRat run function bm:p79/pet/try'); await sleep(300);
  ok('...nor in the Hollow Throne', (await cnt('@e[type=wolf,tag=bm.kxpet]')) === 0);
  // ---- Cecil: no Tendrils for sale any more; the Effigy instead
  const fs = require('fs'); const path = require('path');
  const root = BMB + 'out_p2/BlackMarket_DP/data/bm/function';
  const all = []; const walk = d => { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); fs.statSync(p).isDirectory() ? walk(p) : all.push(p); } }; walk(root);
  const wiz = all.filter(p => /wizard/.test(p)).map(p => fs.readFileSync(p, 'utf8')).join('\n');
  ok("Cecil's shop: no Tendrils, the Storm Effigy instead", wiz.length > 0 && !/bm:"killerwatt_tendrils"/.test(wiz) && /bm:"kw_effigy"/.test(wiz), `${wiz.length} chars`);
  await run('weather clear'); await run(`forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
