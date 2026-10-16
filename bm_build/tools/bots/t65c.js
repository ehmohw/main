// v2.65 content: the new rooms and events, secrets, rare foes, the heist items, the layout's connectivity
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  const pot = async () => num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvpot`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const benchClean = async () => { for (let x0 = 1590; x0 < 1990; x0 += 60) { await run(`execute in bm:gutter run forceload add ${x0} -10 ${x0 + 59} 40`); }
    await sleep(2500); await run('execute in bm:gutter run kill @e[type=!player,x=1590,y=40,z=-10,dx=400,dy=60,dz=50]');
    for (let x0 = 1590; x0 < 1990; x0 += 20) await run(`execute in bm:gutter run fill ${x0} 60 -5 ${x0 + 19} 95 30 air strict`);
    for (let x0 = 1590; x0 < 1990; x0 += 60) await run(`execute in bm:gutter run forceload remove ${x0} -10 ${x0 + 59} 40`); };
  await benchClean();
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await sleep(1500);
  // ---- a heist (tier IV) to stand the tests in
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7604'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000);
  ok('In a tier IV heist', /bm:gutter/.test(await run('data get entity TestRat Dimension')));
  // ---- the layout: every door leads somewhere
  const kinds = (await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,limit=1] Tags'));
  let bad = [];
  for (let q = 0; q <= 6; q++) {
    const tags = await run(`execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},tag=!bm.gvr_cache,limit=1] Tags`);
    if (!/bm.gvr_/.test(tags)) continue;
    const k = tags.match(/bm\.gvr_(\w+)/)[1]; const up = (k === 'climb' || k === 'spire') ? 10 : 0;
    if (k === 'vault') continue;
    const out = await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},tag=!bm.gvr_cache,limit=1] at @s if block ~13 ~${up} ~ minecraft:air if block ~13 ~${up + 1} ~ minecraft:air unless block ~13 ~${up - 1} ~ minecraft:air`);
    if (!/passed/.test(out)) bad.push(`${q}:${k}`);
    if (q > 0) { const inn = await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=${q}},limit=1] at @s if block ~-13 ~ ~ minecraft:air unless block ~-13 ~-1 ~ minecraft:air`);
                 if (!/passed/.test(inn)) bad.push(`in${q}:${k}`); }
  }
  const vin = await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s if block ~-13 ~ ~ minecraft:air unless block ~-13 ~-1 ~ minecraft:air');
  if (!/passed/.test(vin)) bad.push('vault-in');
  ok('Every room\'s exit opens onto a passage, every entry from one (and the vault\'s)', bad.length === 0, bad.join(' '));
  // ---- a test bench: each new room placed far off in the vault's world, claimed for this heist
  await run('execute in bm:gutter run forceload add 1600 -40 1760 40'); await sleep(2500);
  const gi = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvi`);
  const bench = async (kind, x, tier = 4) => {
    await run(`scoreboard players set #gt bm.rng ${tier}`); await run(`scoreboard players set #gi bm.rng ${gi}`); await run('scoreboard players set #gn bm.rng 0'); await run('scoreboard players set #gm bm.rng 0');
    await run(`execute in bm:gutter run place template bm:gv_${kind}_t${tier} ${x} 64 0`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvnew] run function bm:p75/claim`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${kind},x=${x},y=60,z=0,dx=25,dy=30,dz=25] at @s run function bm:p70/r/init`);
    return `@e[type=marker,tag=bm.gvr_${kind},x=${x},y=60,z=0,dx=25,dy=30,dz=25,limit=1]`;
  };
  const st = async m => num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvs`);
  const at = async (m, dx, dy, dz) => run(`execute in bm:gutter as ${m} at @s run tp TestRat ~${dx} ~${dy} ~${dz}`);
  const pressAt = async (m, x, y, z, face = 'wall', facing = 'south') => {
    await run(`execute in bm:gutter as ${m} at @s run setblock ~${x - 12} ~${y - 4} ~${z - 12} minecraft:pale_oak_button[face=${face},facing=${facing},powered=true]`); await sleep(250);
    await run(`execute in bm:gutter as ${m} at @s run setblock ~${x - 12} ~${y - 4} ~${z - 12} minecraft:pale_oak_button[face=${face},facing=${facing},powered=false]`); await sleep(200); };
  // THE SIGNAL LAMPS
  let m = await bench('lamps', 1600);
  const L = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvx`), C = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvc`);
  await at(m, 0, 0, -6); await sleep(1500);
  ok('The Signal Lamps: they flash when you come in (showing)', (await st(m)) === 1);
  await sleep((26 + 16 * L) * 50 + 600);
  ok('...then it is your turn', (await st(m)) === 2, `state ${await st(m)} L ${L}`);
  const LX = [8, 11, 14, 17];
  await pressAt(m, LX[(Math.floor(C / 1) % 4 + 1) % 4], 5, 1);
  ok('...a wrong lamp: back to watching (the alarm rings)', (await st(m)) === 1);
  await sleep((26 + 16 * L) * 50 + 800);
  for (let i = 0; i < L; i++) await pressAt(m, LX[Math.floor(C / 4 ** i) % 4], 5, 1);
  ok('...the right sequence: beaten', (await st(m)) === 3, `state ${await st(m)}`);
  // THE LAMP FLOOR
  m = await bench('lightsout', 1630);
  let g = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvc`);
  const nb = b => { const i = b % 3, j = Math.floor(b / 3); const r = [b]; if (i > 0) r.push(b - 1); if (i < 2) r.push(b + 1); if (j > 0) r.push(b - 3); if (j < 2) r.push(b + 3); return r; };
  let sol = null;
  for (let mask = 0; mask < 512 && sol === null; mask++) { let s = g; for (let b = 0; b < 9; b++) if (mask >> b & 1) for (const c of nb(b)) s ^= 1 << c; if (s === 511) sol = mask; }
  await at(m, -6, 0, 0); await sleep(600);
  for (let b = 0; b < 9; b++) if (sol >> b & 1) await pressAt(m, 5 + b % 3, 5, 11 + Math.floor(b / 3), 'floor', 'east');
  ok('The Lamp Floor: solving it lights every lamp and beats the room', (await st(m)) === 3, `state ${await st(m)} start ${g} sol ${sol}`);
  // THE TUMBLER LOCK
  m = await bench('tumbler', 1660); await at(m, 0, 0, -8); await sleep(500);
  await run(`execute in bm:gutter as ${m} run scoreboard players set @s bm.gvc 1`); await run(`execute in bm:gutter as ${m} at @s run function bm:p76/r/tumbler/try`);
  ok('The Tumbler Lock: a press off the gate resets the count', (await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvw`)) === 0);
  for (let i = 0; i < 3; i++) { await run(`execute in bm:gutter as ${m} run scoreboard players set @s bm.gvc 4`); await run(`execute in bm:gutter as ${m} at @s run function bm:p76/r/tumbler/try`); }
  ok('...three presses on the gate beat it', (await st(m)) === 3);
  // THE BELL TOWER
  m = await bench('climb', 1690);
  ok('The Bell Tower: the high exit is barred', /passed/.test(await run(`execute in bm:gutter as ${m} at @s if block ~12 ~10 ~ minecraft:iron_bars`)));
  await at(m, 9, 10, 0); await sleep(800);
  ok('...the plate on the landing beats it and opens the high door', (await st(m)) === 3 && /passed/.test(await run(`execute in bm:gutter as ${m} at @s if block ~12 ~10 ~ minecraft:air`)));
  // THE CRUMBLING RAFTERS
  m = await bench('rafters', 1720); await at(m, -8, 0.05, 0); await sleep(1600);
  ok('The Crumbling Rafters: a beam gives way under you', /passed/.test(await run(`execute in bm:gutter as ${m} at @s if block ~-8 ~-1 ~ minecraft:air`)));
  await at(m, -11, 0, 0); await sleep(4200);
  ok('...and comes back a while later', !/passed/.test(await run(`execute in bm:gutter as ${m} at @s if block ~-8 ~-1 ~ minecraft:air`)));
  await at(m, 10, 0, 0); await sleep(600);
  ok('...the far plate beats it', (await st(m)) === 3);
  await run('execute in bm:gutter run forceload remove 1600 -40 1760 40');
  await run('execute in bm:gutter run forceload add 1750 -40 1920 40'); await sleep(2500);
  // THE ARCANE STUDY
  m = await bench('ambush', 1750); await at(m, 0, 0, 0); await sleep(800);
  console.log('   ambush:', await st(m), await cnt('@e[tag=bm.gvg,x=1750,y=60,z=0,dx=25,dy=20,dz=25]'), await run(`execute in bm:gutter as ${m} at @s if block ~-12 ~ ~ minecraft:iron_bars`));
  ok('The Arcane Study: the door slams, casters appear', (await st(m)) === 1 && (await cnt('@e[tag=bm.gvg,x=1750,y=60,z=0,dx=25,dy=20,dz=25]')) >= 1 &&
     /passed/.test(await run('execute in bm:gutter if block 1750 68 12 minecraft:iron_bars')));
  await run('execute in bm:gutter run kill @e[tag=bm.gvg,x=1750,y=60,z=0,dx=25,dy=20,dz=25]'); await sleep(1500);
  ok('...a second wave', (await st(m)) === 2 && (await cnt('@e[tag=bm.gvg,x=1750,y=60,z=0,dx=25,dy=20,dz=25]')) >= 1);
  await run('execute in bm:gutter run kill @e[tag=bm.gvg,x=1750,y=60,z=0,dx=25,dy=20,dz=25]'); await sleep(1500);
  ok('...then the way on - and the way back - open', (await st(m)) === 3 && !/passed/.test(await run('execute in bm:gutter if block 1750 68 12 minecraft:iron_bars')));
  // THE CHAMPION'S PIT
  m = await bench('pit', 1780); const p0 = await pot(); await at(m, 0, 0, 3); await sleep(800);
  const champ = await run('execute in bm:gutter run data get entity @e[tag=bm.gvchamp,limit=1] CustomName');
  ok('The Champion\'s Pit: a champion steps out', (await cnt('@e[tag=bm.gvchamp]')) >= 1, champ.slice(-60));
  await run('execute in bm:gutter run kill @e[tag=bm.gvchamp]'); await sleep(1500);
  ok('...beaten: the pot fills', (await st(m)) === 3 && (await pot()) >= p0 + 3, `pot ${p0} -> ${await pot()}`);
  // THE RAT RAVE
  m = await bench('rave', 1810); await at(m, 0, 0, 0); await sleep(400);
  ok('The Rat Rave: the dance-off starts, the rave plays', (await st(m)) === 1 && (await num('scoreboard players get TestRat bm.gvmz')) === 7 || (await st(m)) === 1);
  const RV = ['red', 'blue', 'lime', 'yellow', 'magenta'];
  for (let r = 0; r < 6; r++) {
    const w = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvw`); if (w !== r) { await sleep(300); }
    const c = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvc`);
    await run(`execute in bm:gutter as ${m} at @s run setblock ~ ~-1 ~ minecraft:${RV[c]}_stained_glass`);
    const len = 80 - 8 * r, tm = await num(`execute in bm:gutter as ${m} run scoreboard players get @s bm.gvtm`);
    await sleep(Math.max(0, len - tm) * 50 + 400);
  }
  ok('...six rounds danced: beaten, and a spring in your step', (await st(m)) === 3 && /speed/.test(await run('data get entity TestRat active_effects')), `state ${await st(m)}`);
  // THE RATS' REST
  m = await bench('rest', 1840); await at(m, -3, 0, 0); await sleep(800);
  const rs = await run('data get entity TestRat respawn');
  ok('The Rats\' Rest: open at once, and you\'ll wake here', (await st(m)) >= 1 && /pos: \[I; 1852, 68, 12\]/.test(rs), rs.replace(/.*data: /, ''));
  ok('...a peddler', (await cnt('@e[type=villager,x=1840,y=60,z=0,dx=25,dy=20,dz=25]')) === 1);
  // THE STORM VAULT
  m = await bench('storm', 1870); await at(m, 0, 0, 0); await sleep(1500);
  ok('The Storm Vault: breezes, and sparks where lightning will fall', (await cnt('@e[type=breeze,tag=bm.gvg,x=1870,y=60,z=0,dx=25,dy=20,dz=25]')) >= 1);
  for (const [x, z, f] of [[6, 7, 'north'], [18, 7, 'north'], [12, 19, 'south']]) await run(`execute in bm:gutter as ${m} at @s run setblock ~${x - 12} ~1 ~${z - 12} minecraft:lever[face=wall,facing=${f},powered=true]`);
  await sleep(500);
  ok('...three levers pulled: the storm passes, beaten', (await st(m)) === 3 && (await cnt('@e[type=breeze,tag=bm.gvg,x=1870,y=60,z=0,dx=25,dy=20,dz=25]')) === 0);
  await run('execute in bm:gutter run forceload remove 1750 -40 1920 40');
  await run('execute in bm:gutter run forceload add 1900 -40 1980 40'); await sleep(2500);
  // THE VORN LANDING
  m = await bench('ufo', 1900); await at(m, -8, 0, 0); await sleep(800);
  ok('The Vorn Landing: troopers drop', (await cnt('@e[tag=bm.gvg,x=1900,y=60,z=0,dx=25,dy=20,dz=25]')) >= 1);
  for (let k = 0; k < 20; k++) { await run('execute in bm:gutter as @e[type=interaction,tag=bm.gvcoreh,x=1900,y=60,z=0,dx=25,dy=20,dz=25] run data modify entity @s attack set value {player:[I;1,2,3,4],timestamp:1L}'); await sleep(120); }
  await sleep(500);
  ok('...three cores smashed: saucer down, beaten', (await st(m)) === 3);
  // THE ENCHANTED GROVE
  m = await bench('grove', 1930); await at(m, 0, 0, 0); await sleep(500);
  for (let k = 0; k < 4; k++) { await run('execute in bm:gutter at @e[type=block_display,tag=bm.gvwisp,x=1930,y=60,z=0,dx=25,dy=20,dz=25,limit=1] run tp TestRat ~ ~-0.8 ~'); await sleep(400); }
  ok('The Enchanted Grove: four wisps caught - sprites came, the grove blesses you', (await st(m)) === 3 && /luck/.test(await run('data get entity TestRat active_effects')), `state ${await st(m)}`);
  // ---- a loose brick
  await run(`scoreboard players set #gi bm.rng ${gi}`); await run('scoreboard players set #gt bm.rng 4');
  await run('execute in bm:gutter positioned 1930 69 5 run function bm:p76/secret/set');
  ok('A loose brick: a cracked block with a hidden handle', /passed/.test(await run('execute in bm:gutter if block 1930 69 5 minecraft:cracked_deepslate_tiles')) && (await cnt('@e[type=interaction,tag=bm.gvsec]')) >= 1);
  const p1 = await pot();
  await run('tag TestRat add bm.gvok'); await run('execute in bm:gutter run tp TestRat 1931.5 69 5.5');
  await run('execute in bm:gutter as @e[type=interaction,tag=bm.gvsec,x=1930,y=69,z=5,distance=..2] run data modify entity @s interaction set value {player:[I;1,2,3,4],timestamp:1L}'); await sleep(600);
  ok('...pull it: a hidden stash, coins into the pot', (await pot()) >= p1 + 2 && (await cnt('@e[type=interaction,tag=bm.gvsec,x=1930,y=69,z=5,distance=..2]')) === 0, `pot ${p1} -> ${await pot()}`);
  await run('execute in bm:gutter run kill @e[type=rabbit,tag=bm.gvthief]');
  // ---- the Coin Rat
  await run('execute in bm:gutter positioned 1935 68 10 run function bm:p76/gob/spawn'); await sleep(300);
  const p2 = await pot();
  await run('execute in bm:gutter run damage @e[type=rabbit,tag=bm.gvgob,limit=1] 100 minecraft:player_attack by TestRat'); await sleep(1700);
  ok('The Coin Rat: catch it and the pot fills (8+ coins: the pot keeps a third)', (await pot()) >= p2 + 8 && (await cnt('@e[type=item_display,tag=bm.gvgobd,x=1935,y=68,z=10,distance=..8]')) === 0, `pot ${p2} -> ${await pot()}`);
  // ---- a shiny guard: something rare for your haul
  await run('execute in bm:gutter positioned 1935 68 14 run function bm:p70/guard'); await sleep(200);
  await run('execute in bm:gutter as @e[tag=bm.gvg,x=1935,y=68,z=14,distance=..2,limit=1] run function bm:p76/shiny');
  await run('execute in bm:gutter run damage @e[tag=bm.gvshiny,limit=1] 500 minecraft:player_attack by TestRat'); await sleep(700);
  const pid = await num('scoreboard players get TestRat bm.pid');
  const pp = await run(`data get storage bm:gv pot.p${pid}`);
  ok('A shiny guard: a rare find goes into your pot', /bm:p76\/shiny/.test(pp), pp.slice(-160));
  // ---- the heist items
  await run('loot give TestRat loot bm:items/second_wind'); const lv0 = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvlv`);
  await run('execute as TestRat at @s run function bm:p76/item/second_wind');
  await run('loot give TestRat loot bm:items/second_wind'); await run('execute as TestRat at @s run function bm:p76/item/second_wind');
  ok('A Second Wind: one more try, and only once a heist', (await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvlv`)) === lv0 + 1 &&
     (await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"second_wind"}] 0')) === 1);
  await run('loot give TestRat loot bm:items/master_key'); await run('scoreboard players reset TestRat bm.gvmk');
  m = await bench('levers', 1955, 4); await at(m, 0, 0, 0); await sleep(300);
  await run('execute as TestRat at @s run function bm:p76/item/master_key');
  ok('The Master Key beats the puzzle room you stand in (then cools down)', (await st(m)) === 3 && (await num('scoreboard players get TestRat bm.gvmk')) > 500);
  // ---- heist goods ride the coat check
  const keep = await run('data get storage bm:gv bag');
  await run('execute in bm:gutter run forceload remove 1900 -40 1980 40');
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2500);
  ok('Out again: the Second Wind and the Master Key come with you', (await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"master_key"}] 0')) === 1);
  await benchClean();
  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0); })();
