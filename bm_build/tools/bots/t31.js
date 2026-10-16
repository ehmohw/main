const { bot, rcon, sleep } = require('./lib');
const X = 5700, Y = 100, Z = 5700;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[^\d]*$/); return m ? parseFloat(m[1]) : null; };
  const score = async (h, o = 'bm.bm') => { const r = await run(`scoreboard players get ${h} ${o}`); const m = r.match(/has (-?\d+)/); return m ? +m[1] : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const blk = async (x, y, z, b) => (await run(`execute if block ${x} ${y} ${z} ${b}`)).includes('passed');
  // what's in a container: {key: count}, key = bm id or vanilla id (+ "*" when marked as bought)
  const contents = async (x, y, z) => { const out = {};
    for (let i = 0; i < 27; i++) { const r = await run(`data get block ${x} ${y} ${z} Items[${i}]`); if (!r.includes('has the following')) break;
      const id = (r.match(/id: "minecraft:(\w+)"/) || [])[1]; const bm = (r.match(/bm: "(\w+)"/) || [])[1]; const c = +((r.match(/count: (\d+)/) || [0, 1])[1]);
      const k = bm || (id + (r.includes('bm_from') ? '*' : '')); out[k] = (out[k] || 0) + c; } return out; };
  const A = await bot('TestRat'); await sleep(1500);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2500);
  await run(`fill ${X - 10} ${Y - 1} ${Z - 10} ${X + 10} ${Y} ${Z + 10} stone`); await run(`fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} air`);
  await run(`fill ${X - 10} ${Y + 5} ${Z - 10} ${X + 10} ${Y + 5} ${Z + 10} sea_lantern`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('scoreboard players set #forced bm.bm 0');
  // ---- DAYS
  await run('scoreboard players set #bmday bm.bm 9'); await run('time set 234000'); await sleep(1200);
  const d0 = await score('#day');
  await run('time set 1000'); await sleep(1200); const d1 = await score('#day');
  ok('raw `time set 1000` no longer sends the count back to day 0', d0 >= 9 && d1 === d0 + 1, `${d0} -> ${d1}`);
  await run('time set day'); await sleep(1200); const d2 = await score('#day');
  await run('time set midnight'); await sleep(1200); const d3 = await score('#day');
  ok('`time set day` (already morning) and `midnight` keep the count; nothing goes backwards', d2 >= 10 && d3 === d2, `${d2} ${d3}`);
  await run('scoreboard players set #bmday bm.bm 29'); await sleep(2500);
  ok('the Blood Moon follows the new count (day 29, night)', (await score('#active')) === 1, 'cyc ' + await score('#cyc'));
  await run('scoreboard players set #bmday bm.bm 30'); await run('time set day'); await sleep(2500);
  ok('...and dawn ends it', (await score('#active')) === 0, 'day ' + await score('#day'));
  // ---- the market's own bin, by Barnaby
  await run(`summon marker ${X - 8.5} ${Y + 1} ${Z - 8.5} {Tags:["bm.t31mkt"],Rotation:[0f,0f]}`);
  const mk = await run(`execute as @e[tag=bm.t31mkt] at @s rotated as @s run function bm:p51/market`);
  const mb = await cnt(`@e[type=marker,tag=bm.mktbin]`), lab = await cnt('@e[type=text_display,tag=bm.scraplabel]');
  ok('market patch: a Scrap Bin (barrel + label) at the end of Barnaby\'s counter', mb >= 1 && lab >= 1, mk.slice(0, 60));
  await run('kill @e[tag=bm.mktbin]'); await run('kill @e[tag=bm.scraplabel]'); await run('kill @e[tag=bm.t31mkt]');
  // ---- place a Scrap Bin like a player
  const bx = X, bz = Z - 3;
  await run(`tp TestRat ${bx + 0.5} ${Y + 1} ${bz + 2.5} 180 42`); A.pos.yaw = 180; A.pos.pitch = 42; await sleep(400);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/scrap_bin'); await sleep(150); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('Scrap Bin placed (a barrel, named)', await blk(bx, Y + 1, bz, 'barrel') && (await cnt('@e[type=marker,tag=bm.rs_scrap_bin]')) === 1 && (await run(`data get block ${bx} ${Y + 1} ${bz} CustomName`)).includes('Scrap Bin'));
  // fill it
  const B = `${bx} ${Y + 1} ${bz}`;
  await run(`loot insert ${B} loot bm:items/lava_lamp`); await run(`loot insert ${B} loot bm:items/lava_lamp`);
  await run(`loot insert ${B} loot bm:items/lucky_seven`); await run(`loot insert ${B} loot bm:items/heros_bow`); await run(`loot insert ${B} loot bm:items/skiff_paint_crimson`);
  await run(`loot insert ${B} loot bm:items/grave_charm`); await run(`loot insert ${B} loot bm:items/tinker_wrench`);
  await run(`item replace block ${B} container.20 with minecraft:spectral_arrow[minecraft:custom_data={bm_from:1b}] 33`);
  await run(`item replace block ${B} container.21 with minecraft:spectral_arrow 10`);
  await run(`item replace block ${B} container.22 with minecraft:dirt 5`);
  await run(`loot insert ${B} loot bm:items/token`);
  await sleep(2200);
  const c = await contents(bx, Y + 1, bz);
  console.log('  bin now:', JSON.stringify(c));
  // expected: lava 2x3=6, wrench 1, grave charm 5 -> tokens 12 + the 1 token already there; arrows 33* -> 2 tokens + 1 arrow* left
  ok('scrapped for half (2.65 prices): Lava Lamps (4 -> 2 each), Grave Charm (10 -> 5), arrows by the 16, Wrench', c.token === 11, 'tokens ' + c.token);   // (1 there + 4 + 5 + the rest)
  ok('Lucky 7 -> 3 Trophies (Barnaby\'s old buy-back); Hero\'s Bow -> half its whole upgrade chain', c.trophy === 3 && c.medallion >= 1, `trophy ${c.trophy} medallion ${c.medallion}`);
  ok('Zorp\'s goods refund in Xenite: paint (6 green + 2 violet) -> 3 + 1', c.xenite_green === 3 && c.xenite_violet === 1);
  ok('leftovers and things never bought stay: 1 marked arrow, 10 plain arrows, dirt', c['spectral_arrow*'] === 1 && c.spectral_arrow === 10 && c.dirt === 5);
  ok('the scrapped goods are gone', !c.lava_lamp && !c.lucky_seven && !c.heros_bow && !c.skiff_paint_crimson && !c.grave_charm && !c.tinker_wrench);
  await sleep(1500);
  const c2 = await contents(bx, Y + 1, bz);
  ok('money is never scrapped (a second later nothing changes)', JSON.stringify(c2) === JSON.stringify(c));
  // full bin: refunds that don't fit pop out on top
  await run(`data modify block ${B} Items set value []`);
  for (let i = 0; i < 27; i++) await run(`item replace block ${B} container.${i} with minecraft:cobblestone 64`);
  await run(`item replace block ${B} container.0 with minecraft:spectral_arrow[minecraft:custom_data={bm_from:1b}] 16`); await sleep(2200);
  ok('a full bin: the refund pops out on top', (await cnt(`@e[type=item,x=${bx + 0.5},y=${Y + 2},z=${bz + 0.5},distance=..1.5,nbt={Item:{components:{"minecraft:custom_data":{bm:"token"}}}}]`)) === 1 ||
     (await contents(bx, Y + 1, bz)).token === 1);
  await run(`data modify block ${B} Items set value []`); await run(`kill @e[type=item,x=${bx},y=${Y},z=${bz},distance=..4]`);
  // break it: you get the Scrap Bin back
  await run(`setblock ${B} air destroy`); await sleep(600); console.log('  near:', (await run(`execute as @e[type=item,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..4] run data get entity @s Item.id`)).slice(0, 200), await cnt(`@e[type=item,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..4]`), await cnt('@e[type=marker,tag=bm.rs_scrap_bin]'));
  ok('broken: drops the Scrap Bin item, not a barrel', (await cnt(`@e[type=item,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..2,nbt={Item:{components:{"minecraft:custom_data":{bm:"scrap_bin"}}}}]`)) === 1 &&
     !(await cnt(`@e[type=item,x=${bx + 0.5},y=${Y + 1},z=${bz + 0.5},distance=..2,nbt={Item:{id:"minecraft:barrel"}}]`)));
  // lore
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/lava_lamp');
  const lore = await run('data get entity TestRat SelectedItem.components."minecraft:lore"');
  ok('no "no refunds" line on Black Market goods', !lore.includes('no refunds') && lore.includes('no questions asked'));
  await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..30]`);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });
