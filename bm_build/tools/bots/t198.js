// 2.82: BLOOD MOON DROPS - as a regular (non-op) player striking real blows (rcon sets the stage: a floor, Blood Moon horrors made
// from zombies the way the moon makes them, worn down to a sliver of health). Every horror slain drops 1 to 3 Blood Moon Crystals
// (never none) and its Tokens. A horror that drowns into a Drowned keeps its loot: Crystals and Tokens all the same.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const X = 5400, Y = 120, Z = 5400;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z}.5`); await sleep(3000);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 200 4 true');
  await run('time set day');
  await run('item replace entity TestRat hotbar.0 with minecraft:diamond_sword'); A.slot(0);
  const cnt = async i => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${i}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const eidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const slay = async (sel) => {          // (a sliver of health, then the player's own blow; then walk over the drops)
    await run(`${O}data merge entity ${sel} {Health:1f}`);
    await run(`${O}effect clear ${sel} minecraft:resistance`);
    const eid = await eidOf(sel); if (eid == null) return false;
    for (let k = 0; k < 6 && /passed/.test(await run(`${O}execute if entity ${sel}`)); k++) { A.attack(eid); await sleep(700); }
    await sleep(600);
    await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z + 2}.5`); await sleep(1500);
    await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z}.5`); await sleep(600);
    return !/passed/.test(await run(`${O}execute if entity ${sel}`));
  };

  // ---- five horrors: 1 to 3 Crystals each, every time
  const per = [];
  let tokOk = true;
  for (let k = 0; k < 5; k++) {
    await run('clear TestRat *[minecraft:custom_data~{bm:"blood_crystal"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
    await run(`${O}summon minecraft:zombie ${X}.5 ${Y + 1} ${Z + 2}.5 {Tags:["bm.t198"],NoAI:1b}`);
    await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t198,limit=1] at @s run function bm:mobs/blood/zombie`);
    const dead = await slay('@e[type=minecraft:zombie,tag=bm.t198,limit=1]');
    const c = await cnt('blood_crystal'), t = await cnt('token');
    per.push(dead ? c : -1); if (t < 1) tokOk = false;
  }
  ok('every Blood Moon horror slain drops 1 to 3 Crystals (never none) - five of them', per.every(c => c >= 1 && c <= 3), `crystals: ${per.join(', ')}`);
  ok('...and its Tokens', tokOk);

  // ---- a horror that drowns: still a horror's loot
  await run(`${O}fill ${X - 2} ${Y + 1} ${Z + 4} ${X + 2} ${Y + 3} ${Z + 6} minecraft:water`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"blood_crystal"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
  await run(`${O}summon minecraft:zombie ${X}.5 ${Y + 1} ${Z + 5}.5 {Tags:["bm.t198d"],NoAI:1b}`);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t198d,limit=1] at @s run function bm:mobs/blood/zombie`);
  await run(`${O}data merge entity @e[type=minecraft:zombie,tag=bm.t198d,limit=1] {InWaterTime:900,DrownedConversionTime:2}`);
  await sleep(3500);                                              // (it drowns - and a second later the moon's loot is back on it)
  const dsel = '@e[type=minecraft:drowned,tag=bm.t198d,limit=1]';
  const drowned = /passed/.test(await run(`${O}execute if entity ${dsel}`));
  await run(`${O}fill ${X - 2} ${Y + 1} ${Z + 4} ${X + 2} ${Y + 3} ${Z + 6} minecraft:air`);
  await run(`${O}tp ${dsel} ${X}.5 ${Y + 1} ${Z + 2}.5`); await sleep(400);
  const dead = drowned && await slay(dsel);
  const c = await cnt('blood_crystal'), t = await cnt('token');
  ok('a Blood Moon zombie that drowned into a Drowned, slain: Crystals and Tokens all the same', drowned && dead && c >= 1 && c <= 3 && t >= 1, `drowned ${drowned}, slain ${dead}, crystals ${c}, tokens ${t}`);

  await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}kill @e[type=#minecraft:zombies,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
