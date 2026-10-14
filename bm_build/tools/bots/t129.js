// 2.76: a vault beside each trial spawner - placed in a new dungeon, patched into an old one, opened with the dungeon's key once per player
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const A = await bot('TestRat'); await sleep(2500);
  const O = 'execute in minecraft:overworld run ';
  const X = 20000, Y = 60, Z = 20000;              // the dungeon's corner
  const VAULTS = [[9, 3, 35], [19, 3, 33]];         // brood's stash vaults (template coords)
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 80} ${Z + 80}`);
  await run(`${O}tp TestRat ${X + 30} ${Y + 40} ${Z + 30}`); await sleep(2500);
  await run(`${O}fill ${X - 2} ${Y - 2} ${Z - 2} ${X + 66} ${Y + 28} ${Z + 66} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},dx=66,dy=30,dz=66]`);
  console.log(await run(`execute in minecraft:overworld positioned ${X} ${Y} ${Z} run place template bm:p2_brood`));
  await sleep(1500);
  // 1. the new template: one vault beside each spawner, the dungeon's key, the stash loot
  let good = 0;
  for (const [x, y, z] of VAULTS) {
    const b = await run(`${O}data get block ${X + x} ${Y + y} ${Z + z} config`);
    if (/vkey_brood/.test(b) && /p2\/brood\/stash/.test(b)) good++;
    else console.log('vault?', x, y, z, b.slice(0, 200));
  }
  ok('The Broodmother\'s Nest: a vault beside each of its 2 trial spawners (the dungeon\'s Vault Key, the stash loot)', good === 2, `${good}/2`);
  // 2. open one with the key: it pays out, and won't for the same player twice
  const [vx, vy, vz] = VAULTS[0].map((v, i) => v + [X, Y, Z][i]);
  await run(`${O}tp TestRat ${vx - 1.5} ${vy} ${vz + 0.5} -90 20`); await sleep(1500);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/vkey_brood'); A.slot(0); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${vx},y=${vy},z=${vz},distance=..6]`);
  A.useOn(vx, vy, vz, 4); await sleep(4500);
  const items = (await run(`${O}execute if entity @e[type=minecraft:item,x=${vx},y=${vy},z=${vz},distance=..6]`)).match(/Count: (\d+)/i);
  const keyGone = !/Found [1-9]/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"vkey_brood"}] 0'));
  const rp = await run(`${O}data get block ${vx} ${vy} ${vz} server_data.rewarded_players`);
  ok('The Vault Key opens it: the key is used, it pays out, and you\'re on its list', keyGone && items && +items[1] > 0 && /I;/.test(rp), `items ${items && items[1]} key gone ${keyGone} ${rp.slice(-60)}`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/vkey_brood'); A.slot(0); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${vx},y=${vy},z=${vz},distance=..6]`);
  A.useOn(vx, vy, vz, 4); await sleep(2500);
  const again = /Found [1-9]/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"vkey_brood"}] 0'));
  ok('...but not twice for the same player (the second key is kept)', again);
  // 3. an old dungeon (built before 2.76): take its stash vaults away, untag it - the visit puts them back
  for (const [x, y, z] of VAULTS) await run(`${O}setblock ${X + x} ${Y + y} ${Z + z} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:marker,tag=bm.vaultm,x=${X},y=${Y},z=${Z},dx=66,dy=30,dz=66]`);
  const tags = await run(`${O}execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_brood,x=${X},y=${Y},z=${Z},dx=66,dy=30,dz=66] run tag @s remove bm.stash76`);
  console.log('untag:', tags.slice(0, 80));
  await run(`${O}tp TestRat ${X + 12} ${Y + 4} ${Z + 34}`); await sleep(4000);
  let back = 0;
  for (const [x, y, z] of VAULTS) { const b = await run(`${O}data get block ${X + x} ${Y + y} ${Z + z} config`); if (/vkey_brood/.test(b) && /stash/.test(b)) back++; }
  ok('An older Nest gets its spawner vaults the first time someone comes near', back === 2, `${back}/2`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 80} ${Z + 80}`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
