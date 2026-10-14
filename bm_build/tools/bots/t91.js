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

  // ---- THE SHOOTING GALLERY (timed)
  const SLOTS = []; for (const x of [4, 7, 10, 14, 17, 20]) for (const y of [5, 8]) SLOTS.push([x, y, 1]);
  SLOTS.push([1, 6, 4], [1, 6, 7], [23, 6, 4], [23, 6, 7], [8, 5, 8], [12, 6, 6], [16, 5, 8]);
  const targets = async () => { const out = []; for (const [x, y, z] of SLOTS) if (await isb('gallery', x, y, z, 'minecraft:target')) out.push([x, y, z]); return out; };
  await run('function bm:admin/room_gallery'); await heist(2, 8);
  ok('The Shooting Gallery is laid', (await cnt('@e[type=marker,tag=bm.gvr_gallery]')) === 1);
  await goRoom('gallery', 0, 6); await sleep(600);
  ok('Stepping up: the countdown (and a loaned bow + arrows)', (await rstate('gallery')) === 2 && (await items('minecraft:bow[minecraft:custom_data~{bm_kit:1b}]')) === 1 &&
     (await items('minecraft:arrow')) >= 24, `state ${await rstate('gallery')}`);
  await sleep(3300);
  ok('GO: 8 targets to hit at Tier II solo (6 + tier), two up at a time', (await rstate('gallery')) === 1 && (await ms('gallery', 'bm.gvc')) === 8 && (await targets()).length === 2,
     `state ${await rstate('gallery')}, need ${await ms('gallery', 'bm.gvc')}, up ${(await targets()).length}`);
  let t0 = (await targets())[0]; await run(`${base('gallery')} run setblock ~${t0[0]} ~${t0[1]} ~${t0[2]} minecraft:target[power=9]`); await sleep(300);
  ok('A hit target drops and another pops up', (await ms('gallery', 'bm.gvw')) === 1 && (await targets()).length === 2 && !(await isb('gallery', ...t0, 'minecraft:target[power=9]')));
  const lv0 = await lives();
  await setms('gallery', 'bm.gvz', 1); await sleep(400);
  ok('Out of time: the targets go, and it costs a try', (await rstate('gallery')) === 2 && (await targets()).length === 0 && (await lives()) === lv0 - 1, `lives ${lv0} -> ${await lives()}`);
  await sleep(5200);
  ok('...then the countdown again', (await rstate('gallery')) === 2);
  await sleep(3200);
  ok('...and a fresh round (the count starts over)', (await rstate('gallery')) === 1 && (await ms('gallery', 'bm.gvw')) === 0);
  for (let i = 0; i < 14 && (await rstate('gallery')) !== 3; i++) {
    const up = await targets(); if (up.length) await run(`${base('gallery')} run setblock ~${up[0][0]} ~${up[0][1]} ~${up[0][2]} minecraft:target[power=12]`); await sleep(250); }
  ok('Eight hits in time: the way on is open', (await rstate('gallery')) === 3 && (await targets()).length === 0, `state ${await rstate('gallery')}, hits ${await ms('gallery', 'bm.gvw')}`);

  // ---- THE BUTTON DASH (timed)
  const DASH = [[4, 5, 4], [20, 6, 4], [4, 7, 20], [20, 8, 20], [12, 9, 5], [12, 6, 19]];
  await run('function bm:admin/room_dash'); await heist(3, 8);
  await goRoom('dash', -6, 0); await sleep(600);
  ok('The Button Dash: the countdown', (await rstate('dash')) === 2);
  await sleep(3300);
  ok('GO: 30.5 seconds at Tier III', (await rstate('dash')) === 1 && (await ms('dash', 'bm.gvz')) === 610, `${await ms('dash', 'bm.gvz')}`);
  const press = async ([x, t, z]) => { await run(`${base('dash')} run setblock ~${x} ~${t + 1} ~${z} minecraft:stone_button[face=floor,facing=north,powered=true]`); await sleep(200); };
  await press(DASH[0]); await press(DASH[1]);
  ok('Each button pressed lights its perch', (await ms('dash', 'bm.gvw')) === 2 && (await isb('dash', DASH[0][0], DASH[0][1], DASH[0][2], 'minecraft:redstone_lamp')));
  const lv1 = await lives(); await setms('dash', 'bm.gvz', 1); await sleep(400);
  ok('Out of time: a try lost', (await rstate('dash')) === 2 && (await lives()) === lv1 - 1);
  await sleep(5300);
  ok('...the perches reset for another go', (await rstate('dash')) === 2 && (await isb('dash', DASH[0][0], DASH[0][1] + 1, DASH[0][2], 'minecraft:stone_button')) &&
     (await isb('dash', DASH[0][0], DASH[0][1], DASH[0][2], 'minecraft:polished_deepslate')));
  await sleep(3300);
  for (const d of DASH) await press(d);
  await sleep(300);
  ok('All six in time: the way on is open', (await rstate('dash')) === 3, `state ${await rstate('dash')}, ${await ms('dash', 'bm.gvw')} pressed`);

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

  // ---- THE BLOCK TEMPLE
  await run('function bm:admin/room_temple'); await heist(1, 8);
  await goRoom('temple', -8, 0); await sleep(600);
  ok('The Block Temple (Tier I: the easy layout, two blocks)', (await rstate('temple')) === 1 && (await cnt('@e[type=block_display,tag=bm.gvtb]')) === 2 &&
     (await isb('temple', 11, 4, 3, 'minecraft:barrier')) && (await isb('temple', 12, 4, 5, 'minecraft:barrier')) && (await isb('temple', 13, 3, 3, 'minecraft:gold_block')));
  const push = async (bx, bz, px, pz) => {
    await run(`${base('temple')} run tp TestRat ~${px + 0.5} ~4 ~${pz + 0.5}`); await sleep(150);
    await run(`${base('temple')} positioned ~${bx + 0.5} ~4 ~${bz + 0.5} as @e[type=interaction,tag=bm.gvtbi,distance=..0.6,limit=1] run data modify entity @s attack set value {player:${U},timestamp:0L}`);
    await sleep(300); };
  await push(12, 5, 13, 5);
  ok('Hit a block from the east: it slides one cell west', (await isb('temple', 11, 4, 5, 'minecraft:barrier')) && (await isb('temple', 12, 4, 5, 'minecraft:air')) &&
     (await cnt('@e[type=block_display,tag=bm.gvtb]')) === 2);
  await run(`${base('temple')} run setblock ~5 ~5 ~10 minecraft:stone_button[face=floor,facing=north,powered=true]`); await sleep(400);
  ok('The reset button puts it back', (await isb('temple', 12, 4, 5, 'minecraft:barrier')) && (await isb('temple', 11, 4, 5, 'minecraft:air')) && (await cnt('@e[type=block_display,tag=bm.gvtb]')) === 2);
  await push(12, 5, 12, 6);
  ok('A block won\'t go where there\'s no floor (pushed north it slides; the walls stop it)', await isb('temple', 12, 4, 4, 'minecraft:barrier'));
  await run(`${base('temple')} run setblock ~5 ~5 ~10 minecraft:stone_button[face=floor,facing=north,powered=true]`); await sleep(400);
  await push(12, 5, 13, 5); await push(11, 5, 12, 5); await push(11, 3, 10, 3);
  ok('...three pushes in, not solved yet', (await rstate('temple')) === 1);
  await push(12, 3, 11, 3); await sleep(600);
  ok('Both blocks on their switches: the temple opens', (await rstate('temple')) === 3, `state ${await rstate('temple')}`);
  await run('function bm:admin/room_temple'); await heist(5, 8);
  ok('Tier V lays the hardest layout (three blocks)', (await cnt('@e[type=block_display,tag=bm.gvtb]')) === 3 && (await isb('temple', 9, 4, 4, 'minecraft:barrier')));

  // ---- THE GIRDER CLIMB
  await run('function bm:admin/room_girder'); await heist(2, 8);
  await goRoom('girder', -8, 6); await sleep(600);
  ok('The Girder Climb: the rat at the top', (await rstate('girder')) === 1 && (await cnt('@e[type=item_display,tag=bm.gvgrat]')) === 1);
  await sleep(3500);
  ok('...rolls barrels', (await cnt('@e[type=block_display,tag=bm.gvbar]')) >= 1, `${await cnt('@e[type=block_display,tag=bm.gvbar]')}`);
  await sleep(6000);
  ok('...that drop to the girder below and roll back the other way', (await cnt('@e[type=block_display,tag=bm.gvbar,scores={bm.gvx=2..}]')) >= 1,
     (await run('execute in bm:gutter as @e[type=block_display,tag=bm.gvbar] run scoreboard players get @s bm.gvx')).slice(0, 200));
  await run('effect give TestRat minecraft:resistance 30 0 true');
  await run('effect clear TestRat minecraft:resistance');
  const h0 = await hp();
  await run(`${base('girder')} run tp TestRat ~14.5 ~13 ~3`);
  let hit = false; for (let i = 0; i < 24 && !hit; i++) { await sleep(400); hit = (await hp()) < h0; }
  ok('Stand in a barrel\'s way: BONK', hit, `${h0} -> ${await hp()}`);
  await run('effect give TestRat minecraft:instant_health 1 3 true');
  await run(`${base('girder')} run tp TestRat ~3.5 ~13 ~3`); await sleep(500);
  ok('Reach the gold plate: the rat bolts, the way opens', (await rstate('girder')) === 3 && (await cnt('@e[type=block_display,tag=bm.gvbar]')) === 0 && (await cnt('@e[type=item_display,tag=bm.gvgrat]')) === 0);

  // ---- THE MEAD HALL
  const slay = async () => { await run('execute in bm:gutter run tp @e[tag=bm.gvwv] ~ -200 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvwv]'); await sleep(1500); };
  await run('function bm:admin/room_mead'); await heist(3, 8);
  await goRoom('mead', -6, 0); await sleep(1200);
  ok('The Mead Hall: raiders (five at Tier III)', (await cnt('@e[type=vindicator,tag=bm.gvwv]')) === 5, `${await cnt('@e[tag=bm.gvwv]')}`);
  await slay();
  ok('...then berserkers, shieldmaidens and an axe thrower', (await cnt('@e[type=vindicator,tag=bm.gvwv]')) === 2 && (await cnt('@e[type=zombie,tag=bm.gvwv]')) === 2 &&
     (await cnt('@e[type=pillager,tag=bm.gvwv]')) === 1);
  await slay();
  ok('...then the Jarl himself', (await cnt('@e[type=vindicator,tag=bm.gvwv,tag=bm.gvcap]')) === 1);
  await slay();
  ok('...and when he falls: the way on', (await rstate('mead')) === 3);

  // ---- THE TALL GRASS
  await run('function bm:admin/room_grass'); await heist(1, 8);
  await goRoom('grass', -9, 0); await sleep(700);
  ok('The Tall Grass: six critters, six Rat Balls, 4 to catch solo', (await rstate('grass')) === 1 && (await cnt('@e[tag=bm.gvcrit]')) === 6 &&
     (await items('minecraft:snowball[minecraft:custom_data~{bm_kit:1b}]')) === 6 && (await ms('grass', 'bm.gvc')) === 4,
     `${await cnt('@e[tag=bm.gvcrit]')} critters, ${await items('minecraft:snowball')} balls`);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvctr,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(300);
  ok('The Rat Center hands out three more', (await items('minecraft:snowball')) === 9);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvctr,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(300);
  ok('...but not again straight away', (await items('minecraft:snowball')) === 9);
  await run(`execute in bm:gutter at @e[tag=bm.gvcrit,limit=1] run summon minecraft:snowball ~ ~0.6 ~`); await sleep(300);
  ok('A Rat Ball at a critter: caught', (await ms('grass', 'bm.gvw')) === 1 && (await cnt('@e[tag=bm.gvcrit]')) === 5);
  const gi3 = await gi(); await run(`scoreboard players set #gi bm.rng ${gi3}`);
  const w0 = await cnt('@e[tag=bm.gvg]');
  await run('execute as TestRat at @s run function bm:p91/grass/wild'); await sleep(200);
  ok('Something wild jumps out of the grass', (await cnt('@e[tag=bm.gvg]')) === w0 + 1);
  await run('execute in bm:gutter run tp @e[tag=bm.gvg] ~ -200 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvg]');
  for (let i = 0; i < 3; i++) { await run(`execute in bm:gutter at @e[tag=bm.gvcrit,limit=1,sort=arbitrary] run summon minecraft:snowball ~ ~0.6 ~`); await sleep(400); }
  await sleep(400);
  ok('Four caught: the way on is open', (await rstate('grass')) === 3 && (await cnt('@e[tag=bm.gvcrit]')) === 0, `state ${await rstate('grass')}, caught ${await ms('grass', 'bm.gvw')}`);

  // ---- they're drawn in a heist
  await run('function bm:admin/heist_variants_never');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('function bm:admin/heist_variants_off');
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();
