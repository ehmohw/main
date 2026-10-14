// v2.67 (code pass): friendly fire spares every follower; KillerWatt's held reaction poses (arrival roar, flinch, tendril swipe,
// hover), the rider's leap pose kept to the landing, the boss's flinch and jab
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 19000, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async sel => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const hpOf = async sel => { const m = (await run(`data get entity ${sel} Health`)).match(/([\d.]+)f/); return m ? +m[1] : NaN; };
  const rot = async sel => (await run(`data get entity ${sel} transformation.left_rotation`)).replace(/.*data: /, '');
  const W = '@e[type=wolf,tag=bm.kxpet,limit=1]';
  const BODY = '@e[type=item_display,tag=bm.kxp_body,tag=bm.kxp_pet,tag=!bm.kxdying,limit=1]';
  const riding = async () => /passed/i.test(await run(`execute as TestRat on vehicle if entity @s[tag=bm.kxpet]`));
  await run(`forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`fill ${X - 24} ${Y - 1} ${Z - 24} ${X + 24} ${Y - 1} ${Z + 24} minecraft:stone`); await run(`fill ${X - 24} ${Y} ${Z - 24} ${X + 24} ${Y + 16} ${Z + 24} minecraft:air`);
  await run('weather clear'); await run('time set day'); await run('gamerule doMobSpawning false');
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.cecilpet', 'husk,tag=bm.kxboss'])
    await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run(`kill @e[type=#bm:hostile,x=${X - 40},y=${Y - 20},z=${Z - 40},dx=80,dy=60,dz=80,tag=!bm.npc]`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('scoreboard players set TestRat bm.kxcd 0'); await run('scoreboard players set TestRat bm.kxel 0');
  await run('loot replace entity TestRat container.9 loot bm:items/kw_spark'); await sleep(800);

  // ---- he arrives: the roar, held, then back to his breath
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(250);
  const HEAD = '@e[type=item_display,tag=bm.kxp_head,tag=bm.kxp_pet,tag=!bm.kxdying,limit=1]';
  const maw = async () => (await run(`data get entity ${HEAD} item.components."minecraft:custom_model_data".strings[0]`)).replace(/^.*data: /, '').trim();
  const mw0 = await maw();
  const ho0 = await sc(W, 'bm.kxho');
  ok('Called, KillerWatt arrives with a roar (a held pose)', ho0 >= 5, `kxho ${ho0}`);
  ok('...his maw gapes as he roars', /roar/.test(mw0), mw0);
  const roarRot = await rot(BODY);
  await sleep(1300);
  ok('...and the hold runs out: back to his idle cycle', (await sc(W, 'bm.kxho')) === 0 && (await rot(BODY)) !== roarRot, `${roarRot} -> ${await rot(BODY)}`);
  await run(`execute as ${W} run data merge entity @s {Sitting:1b}`); await sleep(200);

  // ---- a blow: the flinch, with a cooldown
  await run(`damage ${W} 1 minecraft:generic`); await sleep(200);
  const fc = await sc(W, 'bm.kxfc'), fho = await sc(W, 'bm.kxho');
  ok('Hurt: he flinches (held, then a 2 s cooldown)', fc >= 30 && fho >= 1, `kxfc ${fc} kxho ${fho}`);
  const mh = await maw(); ok('...and clenches his jaws', /hurt/.test(mh), mh);
  await sleep(500);
  await run(`damage ${W} 1 minecraft:generic`); await sleep(150);
  ok('...a second blow inside the cooldown: no second flinch', (await sc(W, 'bm.kxho')) === 0, `kxho ${await sc(W, 'bm.kxho')}`);
  await run(`execute as ${W} run data merge entity @s {Sitting:0b,Health:60f}`);

  // ---- a monster in bite reach (his bigger attacks on cooldown): the tendril swipe, for show
  await run(`execute as ${W} run scoreboard players set @s bm.kxc 400`); await run(`tp ${W} ${X + 4.5} ${Y} ${Z + 0.5} 90 0`);
  await run(`summon minecraft:zombie ${X + 3} ${Y} ${Z + 0.5} {Tags:["bm.t99z","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:20f}`);
  let sw = false; for (let i = 0; i < 20 && !sw; i++) { await sleep(100); sw = (await cnt('@e[type=wolf,tag=bm.kxpet,tag=bm.kxsw]')) === 1; }
  ok('A monster in reach: his tendrils swipe at it (sweep, held)', sw);
  await sleep(300); const ms = await maw(); ok('...snarling', /snarl/.test(ms), ms);
  await run('kill @e[type=zombie,tag=bm.t99z]'); await run(`execute as ${W} run scoreboard players set @s bm.kxc 20`); await sleep(1000);

  // ---- friendly fire: the Prism's nova hurts the monster beside him, never him
  await run(`tp ${W} ${X + 3} ${Y} ${Z + 0.5}`); await run(`execute as ${W} run data merge entity @s {Health:60f,Sitting:1b}`);
  await run(`summon minecraft:zombie ${X + 3} ${Y} ${Z + 1.5} {Tags:["bm.t99z","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:20f}`);
  await run(`summon minecraft:arrow ${X + 3} ${Y + 0.5} ${Z + 1} {Tags:["bm.t99a"],NoGravity:1b}`);
  await run('data modify entity @e[type=arrow,tag=bm.t99a,limit=1] Owner set from entity TestRat UUID');
  const w0 = await hpOf(W), z0 = await hpOf('@e[type=zombie,tag=bm.t99z,limit=1]');
  await run(`execute as @e[type=arrow,tag=bm.t99a] at @s run function bm:p45/prism_shot/nova`); await sleep(200);
  const w1 = await hpOf(W), z1 = await hpOf('@e[type=zombie,tag=bm.t99z,limit=1]');
  ok('A Prism nova beside KillerWatt: the zombie is hurt, he is not', z1 < z0 && w1 >= w0, `zombie ${z0}->${z1}, KillerWatt ${w0}->${w1}`);
  await run('kill @e[type=arrow,tag=bm.t99a]'); await run('kill @e[type=zombie,tag=bm.t99z]');
  // the Mercenary too (he was excluded as bm.merc, but wears bm.mercpet)
  await run(`summon minecraft:husk ${X + 3} ${Y} ${Z - 1.5} {Tags:["bm.mercpet","bm.t99m"],NoAI:1b,PersistenceRequired:1b,Health:20f}`);
  await run(`summon minecraft:arrow ${X + 3} ${Y + 0.5} ${Z - 1} {Tags:["bm.t99a"],NoGravity:1b}`);
  await run('data modify entity @e[type=arrow,tag=bm.t99a,limit=1] Owner set from entity TestRat UUID'); await sleep(300);
  const m0 = await hpOf('@e[type=husk,tag=bm.t99m,limit=1]');
  await run(`execute as @e[type=arrow,tag=bm.t99a] at @s run function bm:p45/prism_shot/nova`); await sleep(200);
  const m1 = await hpOf('@e[type=husk,tag=bm.t99m,limit=1]');
  ok('...and anything wearing the Mercenary\'s tag (bm.mercpet) is spared as well', m1 === m0, `${m0}->${m1}`);
  await run('kill @e[type=arrow,tag=bm.t99a]'); await run('kill @e[type=husk,tag=bm.t99m]');

  // ---- ridden: the Thunder Leap keeps its pose in mid-air
  await run(`execute as ${W} run data merge entity @s {Sitting:0b}`);
  await run(`tp ${W} ${X + 1.5} ${Y} ${Z + 0.5} -90 0`); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await sleep(400);
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(800);
  ok('On his back', await riding());
  await run(`execute as ${W} run scoreboard players set @s bm.kxho 0`); await sleep(300);
  await run(`execute as ${W} at @s run function bm:p79/pet/rleap`); await sleep(120);
  const l0 = await rot(BODY); await sleep(400); const l1 = await rot(BODY);
  const air = /\d/.test(await run(`execute as ${W} unless predicate bm:p39/on_ground run say x`));
  ok('Thunder Leap: the leap pose holds in mid-air (no walk cycle over it)', l0 === l1 && /-0\.05/.test(l0), `${l0} / ${l1} airborne:${air}`);
  let landed = false; for (let i = 0; i < 40 && !landed; i++) { await sleep(150); landed = (await cnt('@e[type=wolf,tag=bm.kxpet,tag=bm.kxleap]')) === 0; }
  ok('...and he lands (the slam), back to his stride', landed);
  A.input({ shift: true }); await sleep(400); A.input({}); await sleep(500);

  // ---- the followers' new faces: Emma startled when a monster first shows; Cecil drowsy, sitting at night
  const cmdOf = async sel => (await run(`data get entity @e[${sel},limit=1] item.components."minecraft:custom_model_data".strings[0]`)).replace(/^.*data: /, '').trim();
  await run(`kill @e[type=#bm:hostile,x=${X - 40},y=${Y - 20},z=${Z - 40},dx=80,dy=60,dz=80,tag=!bm.npc]`);
  for (const o of ['bm.emcd', 'bm.cpcd', 'bm.cpel']) await run(`scoreboard players reset TestRat ${o}`);
  await run('loot replace entity TestRat container.10 loot bm:items/emma_ribbon'); await run('loot replace entity TestRat container.11 loot bm:items/cecil_gem');
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(2500);
  await run(`summon minecraft:zombie ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["bm.t99z","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:20f}`);
  let st = ''; for (let i = 0; i < 16 && !/surprised/.test(st); i++) { await sleep(100); st = await cmdOf('type=item_display,tag=bm.ep_head'); }
  ok('A monster appears: Emma looks startled', /surprised/.test(st), st);
  await sleep(1200); const se = await cmdOf('type=item_display,tag=bm.ep_head');
  ok('...then settles into her fighting face', /serious|blink/.test(se), se);
  await run('kill @e[type=zombie,tag=bm.t99z]'); await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(500);
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1800);
  await run('time set 14000'); await run('execute as @e[type=wolf,tag=bm.cecilpet] run data merge entity @s {Sitting:1b}'); await sleep(1500);
  const sl = new Set(); for (let i = 0; i < 24; i++) { sl.add(await cmdOf('type=item_display,tag=bm.cp_eyes')); await sleep(150); }
  ok('Sitting at night: Cecil grows drowsy', [...sl].some(x => /sleepy/.test(x)), [...sl].join(' | '));
  await run('time set day'); await sleep(1500);
  const sd = new Set(); for (let i = 0; i < 16; i++) { sd.add(await cmdOf('type=item_display,tag=bm.cp_eyes')); await sleep(150); }
  ok('...by day, sitting, his usual deadpan', ![...sd].some(x => /sleepy/.test(x)), [...sd].join(' | '));
  await run('execute as @e[type=wolf,tag=bm.cecilpet] at @s run function bm:p62/cecil_go'); await sleep(400);

  // ---- the boss: flinches when struck (idle), and the jab
  await run('weather thunder 6000'); await sleep(500);
  await run(`execute positioned ${X - 8} ${Y} ${Z + 0.5} run function bm:admin/killerwatt`);
  let boss = false; for (let i = 0; i < 60 && !boss; i++) { await sleep(250); boss = (await cnt('@e[type=husk,tag=bm.kxboss]')) === 1; }
  ok('The boss crashes down', boss);
  const B = '@e[type=husk,tag=bm.kxboss,limit=1]';
  await run(`execute as ${B} run data merge entity @s {NoAI:1b}`); await sleep(2500);
  await run(`execute as ${B} run scoreboard players set @s bm.kxatk 0`); await run(`execute as ${B} run scoreboard players set @s bm.kxc 400`);
  await run(`execute as ${B} run scoreboard players set @s bm.kxfc 0`); await sleep(200);
  await run(`execute as ${B} at @s run function bm:p79/boss/ouch`); await sleep(150);
  ok('Struck while idle: the boss flinches (held, cooldown)', (await sc(B, 'bm.kxho')) >= 1 && (await sc(B, 'bm.kxfc')) >= 30, `kxho ${await sc(B, 'bm.kxho')} kxfc ${await sc(B, 'bm.kxfc')}`);
  await sleep(600);
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 10 1 true');
  await run(`execute as ${B} at @s run tp TestRat ^ ^ ^2.5`); await sleep(200);
  const p0 = await hpOf('TestRat');
  const ARM = '@e[type=item_display,tag=bm.kxp_armr,tag=bm.kxp_boss,tag=!bm.kxdying,limit=1]';
  const a0 = await rot(ARM);
  await run(`execute as ${B} run scoreboard players set @s bm.kxatk 6`); await run(`execute as ${B} run scoreboard players set @s bm.kxt 0`); await sleep(350);
  const a1 = await rot(ARM); await sleep(700);
  const p1 = await hpOf('TestRat');
  ok('The jab: a right then a left (the fists swing) and they land', a1 !== a0 && p1 < p0, `arm ${a0} -> ${a1}; hp ${p0} -> ${p1}`);
  await sleep(600);
  ok('...and he is done (back to the mind)', (await sc(B, 'bm.kxatk')) === 0);
  await run(`execute as ${B} run tp @s ~ -400 ~`); await run('weather clear'); await run(`execute as ${W} run tp @s ~ -400 ~`);
  await run('effect clear TestRat');

  const n = res.filter(Boolean).length;
  console.log(`${n}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
