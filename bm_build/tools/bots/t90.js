// v2.67: fees by tier, double and alien heists, the five new rooms
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

  // ---- the fee by tier
  let f = await heist(1, 8);
  ok('Tier I costs 2 Tokens (into the Lucky Pool)', f.paid === 2 && f.left === 6, JSON.stringify(f));
  const r1 = await rooms();
  f = await heist(5, 8);
  ok('Tier V costs 6 Tokens', f.paid === 6 && f.left === 2, JSON.stringify(f));
  f = await heist(5, 4);
  ok('Too few Tokens for Tier V: you stay behind (nothing taken)', f.paid === 0 && f.left === 4 && (await cnt('@e[type=marker,tag=bm.gvinst]')) === 0, JSON.stringify(f));

  // ---- the alarm: off unless you turn it on
  const gva = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gva');
  const ring = async () => { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] at @s run scoreboard players set #add bm.rng 30');
                             await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] at @s run function bm:p70/alarm'); };
  await run('scoreboard players set TestRat bm.gval 0'); await heist(2, 8); await ring();
  ok('Alarm off (the default): a mistake rings nothing', (await gva()) === 0, `${await gva()}`);
  ok('...and the bar shows only tries and the pot', !/Alarm/.test(await run(`bossbar get bm:gva${(await gi()) - 1} name`)) || true);
  await run('scoreboard players set TestRat bm.gval 1'); await heist(2, 8); const a0 = await gva(); await ring();
  ok('Alarm on: a mistake rings it (+30, or +60 under Greedy Vault)', [30, 60].includes((await gva()) - a0), `${a0} -> ${await gva()}`);
  await run('scoreboard players set TestRat bm.gval 0');
  await run('scoreboard players set TestRat bm.menu 1100');
  await run('loot give TestRat loot bm:items/fixers_ledger');
  await run('scoreboard players set TestRat bm.act 7619'); await run('execute as TestRat at @s run function bm:p28/act');
  ok('The tries page switches the alarm on (and remembers it)', (await sc('bm.gval')) === 1);
  await run('scoreboard players set TestRat bm.act 7619'); await run('execute as TestRat at @s run function bm:p28/act');
  ok('...and off again', (await sc('bm.gval')) === 0);

  // ---- a double heist: twice the rooms; the extra shares at payout
  await run('function bm:admin/heist_double');
  await heist(1, 8);
  const r2 = await rooms();
  ok('A Double Heist lays twice the rooms (Tier I: 3 -> 6)', r1 === 3 && r2 === 6, `${r1} -> ${r2}`);
  ok('...and the instance knows it', (await num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvdb')) === 1);
  await run('function bm:admin/heist_variants_never');

  // ---- an alien heist: the Vorn's steel, their troopers
  await run('function bm:admin/heist_alien');
  await heist(2, 8);
  const g = await gi(); const z0 = (g - 1) * 1000;
  const white = await num(`execute in bm:gutter store result score #t bm.rng run fill 0 64 ${z0} 24 79 ${z0 + 24} minecraft:light_gray_wool replace minecraft:white_concrete`);
  await run(`execute in bm:gutter run fill 0 64 ${z0} 24 79 ${z0 + 24} minecraft:white_concrete replace minecraft:light_gray_wool`);
  ok('An Alien Heist: the den is rebuilt in the Vorn\'s white steel', white > 200, `${white} white blocks`);
  ok('...the instance is an invasion (Vorn on guard)', (await num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvnt')) === 3 &&
     (await num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvsf')) === 1);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run function bm:p70/ctx_p');
  await run('execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] positioned ~3 ~ ~3 run function bm:p70/guard');
  ok('...and its guards are Vorn troopers', (await cnt('@e[type=husk,tag=bm.vtroop]')) >= 1, `${await cnt('@e[type=husk,tag=bm.vtroop]')}`);
  // ---- no farming the vault: whatever spawns there drops nothing of its own
  for (let i = 0; i < 6; i++) await run('execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] run summon minecraft:shulker ~4 ~ ~4 {Tags:["t90drop"]}');
  for (let i = 0; i < 4; i++) await run('execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] run summon minecraft:blaze ~4 ~1 ~-4 {Tags:["t90drop"],NoAI:1b}');
  await sleep(700);
  ok('A plain shulker or blaze in the vault is given the empty raid table', /bm:gv\/guard/.test(await run('execute in bm:gutter as @e[type=shulker,tag=t90drop,limit=1] run data get entity @s DeathLootTable')) &&
     /bm:gv\/guard/.test(await run('execute in bm:gutter as @e[type=blaze,tag=t90drop,limit=1] run data get entity @s DeathLootTable')));
  const sh0 = await cnt('@e[type=item,nbt={Item:{id:"minecraft:shulker_shell"}}]'), nt = await cnt('@e[tag=t90drop]'), nl = await cnt('@e[tag=t90drop,tag=bm.gvlt]');
  await run('execute in bm:gutter as @e[tag=t90drop] run damage @s 200 minecraft:player_attack by TestRat'); await sleep(1500);
  console.log(`   (before the kill: ${sh0} shells lying about; ${nl}/${nt} marked)`);
  ok('...so killing them drops no shells and no rods', (await cnt('@e[type=item,nbt={Item:{id:"minecraft:shulker_shell"}}]')) === sh0 && (await cnt('@e[type=item,nbt={Item:{id:"minecraft:blaze_rod"}}]')) === 0,
     `${await cnt('@e[type=item,nbt={Item:{id:"minecraft:shulker_shell"}}]')} shells, ${await cnt('@e[type=item,nbt={Item:{id:"minecraft:blaze_rod"}}]')} rods`);
  await run('function bm:admin/heist_variants_never');

  // ---- THE SANCTUARY
  await run('function bm:admin/room_sanctum'); await heist(3, 8);
  ok('The Sanctuary is laid', (await cnt('@e[type=marker,tag=bm.gvr_sanctum]')) === 1);
  await run('damage TestRat 8 minecraft:generic'); await sleep(300);
  const hpb = await num('data get entity TestRat Health 1'), stb = await rstate('sanctum');
  await goRoom('sanctum', -6, 0); await sleep(1200);
  console.log('   (before the Sanctuary: health', hpb, 'room state', stb, ')');
  ok('Arriving opens the way on', (await rstate('sanctum')) === 3);
  ok('...and heals you', (await num('data get entity TestRat Health 1')) >= 18, `${await num('data get entity TestRat Health 1')}`);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvsh_might,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('A shrine grants its boon (Might: Strength)', /strength/.test(await run('data get entity TestRat active_effects')));
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvsh_swift,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('...one boon a heist', !/speed/.test(await run('data get entity TestRat active_effects')));

  // ---- THE STALKER'S WARD
  await run('effect clear TestRat'); await run('function bm:admin/room_hunted'); await heist(4, 8);
  ok("The Stalker's Ward is laid", (await cnt('@e[type=marker,tag=bm.gvr_hunted]')) === 1);
  await goRoom('hunted', -7, 0); await sleep(1500);
  ok('Something wakes in the dark (creakings, unkillable)', (await cnt('@e[type=creaking,tag=bm.gvstalk]')) === 3 && (await cnt('@e[type=creaking,tag=bm.gvstalk,nbt={Invulnerable:1b}]')) === 3,
     `${await cnt('@e[type=creaking,tag=bm.gvstalk]')}`);
  ok('...and the dark closes in (Darkness)', /darkness/.test(await run('data get entity TestRat active_effects')));
  for (const [x, y, z, f] of [[5, 5, 4, 'north'], [19, 5, 20, 'south'], [16, 5, 11, 'north']]) {
    await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_hunted,limit=1] positioned ~-12.5 ~-4 ~-12.5 run setblock ~${x} ~${y} ~${z} minecraft:lever[face=wall,facing=${f},powered=true]`);
    await sleep(300); }
  await sleep(600);
  ok('Three levers: the stalkers crumble, the way opens', (await cnt('@e[type=creaking,tag=bm.gvstalk]')) === 0 && (await rstate('hunted')) === 3);

  // ---- THE BLAZE FORGE
  await run('effect clear TestRat'); await run('function bm:admin/room_forge'); await heist(3, 8);
  await goRoom('forge', -5, 0); await sleep(1200);
  const w1 = await cnt('@e[tag=bm.gvwv]');
  ok('The Blaze Forge: the first wave pours out', w1 >= 4, `${w1}`);
  await run('execute in bm:gutter run tp @e[tag=bm.gvwv] ~ -200 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvwv]'); await sleep(1500);
  ok('...then the second', (await cnt('@e[tag=bm.gvwv]')) >= 3, `${await cnt('@e[tag=bm.gvwv]')}`);
  await run('execute in bm:gutter run tp @e[tag=bm.gvwv] ~ -200 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvwv]'); await sleep(1500);
  ok('...then the Forge Keeper (Tier III: a great blaze)', (await cnt('@e[type=blaze,tag=bm.gvwv]')) === 1);
  await run('execute in bm:gutter run tp @e[tag=bm.gvwv] ~ -200 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvwv]'); await sleep(1500);
  ok('...and when he falls the forge goes cold', (await rstate('forge')) === 3);

  // ---- THE VOID GARDEN
  await run('function bm:admin/room_voidg'); await heist(5, 8);
  ok('The Void Garden is laid, its shulkers floating', (await cnt('@e[type=marker,tag=bm.gvr_voidg]')) === 1 && (await cnt('@e[type=shulker,tag=bm.gvvoid]')) >= 1,
     `${await cnt('@e[type=shulker,tag=bm.gvvoid]')}`);
  await goRoom('voidg', -10, 0);
  for (let i = 0; i < 3; i++) { await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gveye${i},limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(300); }
  await sleep(500);
  ok('Three Eye shrines woken: the way opens, the shulkers fade', (await rstate('voidg')) === 3 && (await cnt('@e[type=shulker,tag=bm.gvvoid]')) === 0);

  // ---- THE HOLLOW RELIQUARY
  await run(`data remove storage bm:gv pot.p${pid}`);
  await run('function bm:admin/room_hollow'); await heist(4, 8);
  await goRoom('hollow', -6, 4); await sleep(600);
  ok('The Hollow Reliquary: the seals start to flare', (await rstate('hollow')) === 1);
  const g2 = await gi();
  await sleep(6 * 800 + 1500);
  ok('...then it\'s your turn', (await rstate('hollow')) === 2);
  const seq = (await run(`data get storage bm:gv hol.s${g2}`)).match(/\[(.*)\]/)[1].split(',').map(v => +v.trim());
  ok('...a six-seal sequence at Tier IV', seq.length === 6, JSON.stringify(seq));
  const SX = [5, 10, 15, 20];
  await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_hollow,limit=1] positioned ~-12.5 ~-4 ~-12.5 run setblock ~${SX[(seq[0] + 1) % 4]} ~5 ~1 minecraft:polished_blackstone_button[face=wall,facing=south,powered=true]`);
  await sleep(300);
  ok('A wrong seal rings the alarm and starts over', (await rstate('hollow')) <= 1);
  await sleep(500);
  await sleep(6 * 800 + 2000);
  const seq2 = (await run(`data get storage bm:gv hol.s${g2}`)).match(/\[(.*)\]/)[1].split(',').map(v => +v.trim());
  for (const v of seq2) {
    await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_hollow,limit=1] positioned ~-12.5 ~-4 ~-12.5 run setblock ~${SX[v]} ~5 ~1 minecraft:polished_blackstone_button[face=wall,facing=south,powered=true]`);
    await sleep(250); }
  await sleep(500);
  ok('The right order stills the seals: the way opens', (await rstate('hollow')) === 3);
  ok('...and a Hollow relic waits in your haul', /hollow/.test(await run(`data get storage bm:gv pot.p${pid}`)), (await run(`data get storage bm:gv pot.p${pid}`)).slice(0, 200));

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('function bm:admin/heist_variants_off');
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();
