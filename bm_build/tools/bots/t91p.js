// v2.67: game night in the vault - the seven game rooms
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const o = await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const tokens = async () => num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"token"}] 0');
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const heist = async (tier = 3, ntok = 8) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
    for (let i = 0; i < ntok; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    const p0 = await num('scoreboard players get #lpool bm.gvlp');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
    const paid = (await num('scoreboard players get #lpool bm.gvlp')) - p0, left = await tokens();
    await sleep(4500); return { paid, left }; };
  const gi = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvi');
  const rooms = async () => cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,tag=!bm.gvr_vault]');
  const goRoom = async (k, dx = 0, dz = 0) => { await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] run tp TestRat ~${dx} ~ ~${dz}`); await sleep(800); };
  const rstate = async (k) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s bm.gvs`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('function bm:admin/heist_variants_never');
  const U = await uuid(); const pid = await sc('bm.pid');


  const base = k => `execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] positioned ~-12.5 ~-4 ~-12.5`;
  const ms = async (k, o) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s ${o}`);
  const setms = (k, o, v) => run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players set @s ${o} ${v}`);
  const lives = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvlv');
  const isb = async (k, x, y, z, b) => /passed/i.test(await run(`${base(k)} if block ~${x} ~${y} ~${z} ${b}`));
  const items = async (sel) => { const v = await num(`execute store result score #t bm.rng run clear TestRat ${sel} 0`); return isNaN(v) ? 0 : v; };
  const hp = async () => num('data get entity TestRat Health 1');

  // ---- PIPE PLAZA
  await run('function bm:admin/room_plaza'); await heist(1, 8);
  await goRoom('plaza', -8, 0); await sleep(600);
  ok('Pipe Plaza: Grumbas (3 + tier), five ? blocks with their marks', (await rstate('plaza')) === 1 && (await cnt('@e[type=husk,tag=bm.gvgrum]')) === 4 &&
     (await cnt('@e[type=interaction,tag=bm.gvq]')) === 5 && (await cnt('@e[type=text_display,tag=bm.gvql]')) === 10,
     `${await cnt('@e[type=husk,tag=bm.gvgrum]')} grumbas, ${await cnt('@e[type=text_display,tag=bm.gvql]')} marks`);
  ok('...and 8 coins needed solo', (await ms('plaza', 'bm.gvc')) === 8);
  const c0 = await cnt('@e[type=item,tag=bm.gvpzc]');
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvq,limit=1,sort=arbitrary] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('Bonk! The ? block goes brown and pops two coins', (await cnt('@e[type=item,tag=bm.gvpzc]')) === c0 + 2 && (await cnt('@e[type=text_display,tag=bm.gvql]')) === 8 &&
     (await isb('plaza', 6, 6, 9, 'minecraft:brown_terracotta') || await isb('plaza', 9, 6, 9, 'minecraft:brown_terracotta') || await isb('plaza', 12, 7, 9, 'minecraft:brown_terracotta') ||
      await isb('plaza', 15, 6, 9, 'minecraft:brown_terracotta') || await isb('plaza', 18, 6, 9, 'minecraft:brown_terracotta')));
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvflag,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(300);
  ok('The flagpole without enough coins: not yet', (await rstate('plaza')) === 1);
  const g0 = await cnt('@e[type=husk,tag=bm.gvgrum]');
  await run('execute in bm:gutter as @e[type=husk,tag=bm.gvgrum,limit=1] run data merge entity @s {NoAI:1b}');
  await run('execute in bm:gutter at @e[type=husk,tag=bm.gvgrum,nbt={NoAI:1b},limit=1] run tp TestRat ~ ~1.3 ~'); await sleep(700);
  ok('Stomp a Grumba from above: squashed (and it leaves a coin)', (await cnt('@e[type=husk,tag=bm.gvgrum]')) === g0 - 1, `${g0} -> ${await cnt('@e[type=husk,tag=bm.gvgrum]')}`);
  await goRoom('plaza', -8, 0);
  await run('execute in bm:gutter as @e[type=item,tag=bm.gvpzc] run data merge entity @s {NoGravity:0b}');
  await run('execute in bm:gutter as @e[type=item,tag=bm.gvpzc] run tp @s TestRat'); await sleep(1500);
  ok('Coins picked up count for the crew (and leave the inventory)', (await ms('plaza', 'bm.gvw')) >= 8 && (await items('minecraft:raw_gold')) === 0, `${await ms('plaza', 'bm.gvw')} coins, ${await items('minecraft:raw_gold')} raw gold held, gvpz ${await sc('bm.gvpz')}, ${(await run('data get entity TestRat Inventory')).slice(0, 400)}`);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvflag,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('Touch the flagpole: course clear', (await rstate('plaza')) === 3 && (await cnt('@e[type=husk,tag=bm.gvgrum]')) === 0);

  // ---- they're drawn in a heist
  await run('function bm:admin/heist_variants_never');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('function bm:admin/heist_variants_off');
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();
