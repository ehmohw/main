// v2.65: kit abilities, hirelings, the Endless Vault, the Pit
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  const ist = async o => num(`execute in bm:gutter as ${inst} run scoreboard players get @s ${o}`);
  const heist = async (act, lives = 7613) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/heist_plans'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${act}`);
    await run(act <= 7605 ? 'execute as TestRat at @s run function bm:p70/pick_tier' : 'execute as TestRat at @s run function bm:p77/pick_mode');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('scoreboard players reset TestRat bm.gvhr');
  // ---- kits: each comes with its ability
  await heist(7603);
  const kitHas = async (r, iid) => { await run(`execute as TestRat at @s run function bm:p72/kit/pick_${r}`);
    return (await num(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}",bm_kit:1b}] 0`)) === 1; };
  ok('The Tank kit carries the Bulwark Horn', await kitHas(1, 'kit_horn'));
  ok('The Offense kit carries the Shadowstep Charm', await kitHas(2, 'kit_step'));
  ok('The Ranged kit carries the Volley Quiver', await kitHas(3, 'kit_volley'));
  ok('The Support kit carries the Tidal Ward', await kitHas(4, 'kit_tidal'));
  // abilities (run as if used)
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~ ~ ~ -90 0'); await sleep(300);
  await run('effect clear TestRat'); await run('execute as TestRat at @s run function bm:p77/kit/kit_horn_go');
  ok('Bulwark Horn: absorption and resistance', /absorption/.test(await run('data get entity TestRat active_effects')) && /resistance/.test(await run('data get entity TestRat active_effects')));
  const p0 = await run('data get entity TestRat Pos');
  await run('execute as TestRat at @s run function bm:p77/kit/kit_step_go'); await sleep(200);
  const p1 = await run('data get entity TestRat Pos');
  const x0 = +p0.match(/\[([-\d.]+)d/)[1], x1 = +p1.match(/\[([-\d.]+)d/)[1];
  ok('Shadowstep: a blink forward (east, a few blocks), unseen', x1 - x0 >= 3 && x1 - x0 <= 7.6 && /invisibility/.test(await run('data get entity TestRat active_effects')), `${x0} -> ${x1}`);
  await run('execute as TestRat at @s run tp @s ~ ~ ~ 90 0'); await sleep(150);
  const before = await run('data get entity TestRat Pos');
  await run('execute as TestRat at @s run function bm:p77/kit/kit_step_go'); await sleep(200);
  const after = await run('data get entity TestRat Pos'); const bx = +before.match(/\[([-\d.]+)d/)[1], ax = +after.match(/\[([-\d.]+)d/)[1];
  ok('...never through the den\'s west wall', ax >= 0.9, `${bx} -> ${ax}`);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~ ~ ~ -90 -5'); await sleep(200);
  await run('execute as TestRat at @s run function bm:p77/kit/kit_volley_go'); await sleep(150);
  const arrows = await cnt('@e[type=arrow,x=0,y=60,z=0,dx=40,dy=20,dz=30]');
  const mo = await run('execute in bm:gutter run data get entity @e[type=arrow,limit=1,sort=nearest,x=12,y=68,z=12] Motion');
  ok('Volley Quiver: five arrows, flying', arrows === 5 && /\[[1-3]\.\d+d/.test(mo), `${arrows} ${mo.replace(/.*data: /, '')}`);
  await run('execute in bm:gutter run kill @e[type=arrow]');
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:poison 20 0'); await run('execute as TestRat at @s run function bm:p77/kit/kit_tidal_go');
  const ef = await run('data get entity TestRat active_effects');
  ok('Tidal Ward: heals, shields, washes off poison', /absorption/.test(ef) && /regeneration/.test(ef) && !/poison/.test(ef));
  // the consumed ability comes straight back to your hand
  await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p72/kit/pick_1');
  await run('clear TestRat *[minecraft:custom_data~{bm:"kit_horn"}]'); await run('item replace entity TestRat weapon.mainhand with air');
  await run('advancement grant TestRat only bm:consume/kit_horn'); await sleep(200);
  ok('...a used ability is handed straight back (in your hand)', /kit_horn/.test(await run('data get entity TestRat SelectedItem')), (await run('data get entity TestRat SelectedItem')).slice(-120));
  // ---- hirelings
  await run('loot give TestRat loot bm:items/contract_turret');
  await run('execute as TestRat at @s run function bm:p77/hire/use4'); await sleep(400);
  ok('A contract in the vault: the hireling joins (a wolf with a rat on it)', (await cnt('@e[type=wolf,tag=bm.hire_turret]')) === 1 && (await cnt('@e[tag=bm.hired]')) === 2);
  ok('...and is remembered for every heist', (await num('scoreboard players get TestRat bm.gvhr')) === 4);
  await run('scoreboard players set #gt bm.rng 3'); await run('scoreboard players set #gn bm.rng 0'); await run('scoreboard players set #gm bm.rng 0');
  await run('scoreboard players operation #gi bm.rng = TestRat bm.gvi');
  await run('execute in bm:gutter at @e[type=wolf,tag=bm.hire_turret,limit=1] positioned ~3 ~ ~ run function bm:p70/guard'); await sleep(2600);
  const ghp = await run('execute in bm:gutter run data get entity @e[tag=bm.gvg,limit=1,sort=nearest,x=3,y=68,z=12] Health');
  // (2.67: the rogues' gallery makes guards of many sizes - hurt is below its own max)
  const gmx = await run('execute in bm:gutter run attribute @e[tag=bm.gvg,limit=1,sort=nearest,x=3,y=68,z=12] minecraft:max_health get');
  ok('Tick-Tock shoots the guard', /\d/.test(ghp) && +ghp.match(/([\d.]+)f/)[1] < +(gmx.match(/([\d.]+)\s*$/) || [0, 0])[1], ghp.replace(/.*data: /, '') + ' of ' + gmx.replace(/.*is /, ''));
  await run('execute in bm:gutter run kill @e[tag=bm.gvg]');
  await run('execute in bm:gutter run kill @e[type=wolf,tag=bm.hire]'); await sleep(2500);
  ok('Knocked out: back in 45 seconds', (await num('scoreboard players get TestRat bm.gvhd')) >= 40);
  await run('scoreboard players set TestRat bm.gvhd 1'); await sleep(2500);
  ok('...and back again after', (await cnt('@e[type=wolf,tag=bm.hire_turret]')) === 1);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1800);
  ok('Hirelings never leave the vault (gone when you do)', (await cnt('@e[type=wolf,tag=bm.hire]')) === 0);
  // ---- the next heist: the hireling comes along by itself
  await heist(7601); await sleep(2000);
  ok('Next heist: your hireling meets you in the den', (await cnt('@e[type=wolf,tag=bm.hire_turret]')) === 1);
  await run('execute as TestRat at @s run function bm:p77/hire/send_off'); await sleep(300);
  ok('Sneak + use: sent off duty', (await cnt('@e[type=wolf,tag=bm.hire]')) === 0 && (await num('scoreboard players get TestRat bm.gvhr')) === 0);
  // ---- THE ENDLESS VAULT
  await heist(7606);
  ok('The Endless Vault: mode set, no vault at the end, three rooms ahead', (await ist('bm.gvmd')) === 2 && (await cnt('@e[type=marker,tag=bm.gvr_vault]')) === 0 &&
     (await cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache]')) === 3, `rooms ${await cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache]')}`);
  ok('...a cursor kept to build on', (await cnt('@e[type=marker,tag=bm.gvcurk]')) === 1);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin');
  for (let q = 1; q <= 3; q++) { await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},limit=1] at @s run function bm:p70/solved`); await sleep(3200); }
  const nr = await cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache]');
  ok('Three rooms beaten: the vault builds on ahead (two more each time)', nr >= 5, `rooms ${nr}, cleared ${await ist('bm.gvxw')}`);
  ok('...rooms cleared are counted', (await ist('bm.gvxw')) === 3);
  // the fifth room is a Rats' Rest with the cash-out
  for (let q = 4; q <= 5; q++) { await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},limit=1] at @s run function bm:p70/solved`); await sleep(3200); }
  ok('Room five is a Rats\' Rest', (await cnt('@e[type=marker,tag=bm.gvr_rest,scores={bm.gvq=5}]')) === 1, await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,scores={bm.gvq=5},limit=1] Tags'));
  ok('...and the vault has gone deeper: tier II now', (await ist('bm.gvt')) >= 2, 'tier ' + await ist('bm.gvt'));
  await run('clear TestRat');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_rest,scores={bm.gvq=5},limit=1] at @s run tp TestRat ~ ~ ~9'); await sleep(1500);
  const haul = async () => { for (let i = 0; i < 12; i++) { if ((+(((await run('execute store result score #t bm.rng run clear TestRat minecraft:barrel[minecraft:custom_data~{bm_haul:1b}] 0')).match(/Found (\d+)/) || [0, 0])[1])) >= 1) return true; await sleep(500); } return false; };   // (counted, not read: the Haul's listing is longer than an RCON reply)
  const inv = await haul();
  ok('Cash out on the Rest\'s plate: paid (The Haul)', (await ist('bm.gvst')) === 4 && inv, `st ${await ist('bm.gvst')}`);
  await sleep(10500);
  ok('...and the Fixer pulls you out', !/bm:gutter/.test(await run('data get entity TestRat Dimension')));
  // ---- THE PIT
  await heist(7607);
  ok('The Pit: an arena after the den', (await ist('bm.gvmd')) === 1 && (await cnt('@e[type=marker,tag=bm.gvr_arena]')) === 1);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_arena,limit=1] at @s run tp TestRat ~-10 ~ ~'); await sleep(6500);
  const g1 = await cnt('@e[tag=bm.gvg]');
  ok('Wave 1 pours in', g1 >= 3, 'guards ' + g1);
  await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(1600);
  ok('...cleared: a wave survived (one share)', (await ist('bm.gvxw')) === 1);
  for (let w = 2; w <= 5; w++) { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_arena,limit=1] run scoreboard players set @s bm.gvtm 239'); await sleep(1500);
    if (w === 5) { const b = await cnt('@e[tag=bm.gvboss]'); ok('Wave 5: a guardian (no golden shell in the Pit)', b === 1); }
    await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await run('execute in bm:gutter run kill @e[tag=bm.gvboss]'); await sleep(1600); }
  ok('Five waves survived', (await ist('bm.gvxw')) === 5);
  await run('clear TestRat');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_arena,limit=1] at @s run tp TestRat ~-15 ~ ~4'); await sleep(1200);
  ok('The emerald plate between waves cashes out', (await ist('bm.gvst')) === 4 && await haul(), 'st ' + await ist('bm.gvst'));
  await sleep(10500);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0); })();
