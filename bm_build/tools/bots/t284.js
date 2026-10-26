// 2.94y, as a regular (non-op) player:
//   THE DARK AUCTION'S RELICS SCRAP FOR MORE - a Scrap Bin set down as you would (its item, used); the six relics put in
//   (rcon: the stage, as t31 does) - each comes back as a Trophy and 2 Medallions (they paid 3 Medallions);
//   A DREAD TOKEN FROM A DREAD MOB, ONE IN TWENTY, LOOTING OR NOT - a hundred Dread zombies (rcon: the stage - stood still, at
//   a heartbeat) struck down by you with a Looting III sword: about five Tokens (1..14 - Looting's bonus would show well past it).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const X = 18220, Y = 100, Z = 16400;
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const contents = async (x, y, z) => { const out = {};
    for (let i = 0; i < 27; i++) { const r = await run(`${O}data get block ${x} ${y} ${z} Items[${i}]`); if (!r.includes('has the following')) break;
      const id = (r.match(/id: "minecraft:(\w+)"/) || [])[1]; const bm = (r.match(/bm: "(\w+)"/) || [])[1]; const c = +((r.match(/count: (\d+)/) || [0, 1])[1]);
      const k = bm || id; out[k] = (out[k] || 0) + c; } return out; };
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y - 1} ${Z - 10} ${X + 10} ${Y - 1} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y + 5} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);

  // ---- the relics, scrapped
  const bx = X, bz = Z - 3;
  await run(`${O}tp TestRat ${bx + 0.5} ${Y} ${bz + 2.5} 180 42`); A.pos && (A.pos.yaw = 180, A.pos.pitch = 42); await sleep(1500);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/scrap_bin'); await sleep(200); A.use(); await sleep(300); A.release(); await sleep(500);
  ok('a Scrap Bin set down', (await run(`${O}data get block ${bx} ${Y} ${bz} CustomName`)).includes('Scrap Bin'));
  const B = `${bx} ${Y} ${bz}`;
  for (const r of ['auroral_crown', 'brass_wing_scroll', 'rat_familiar', 'bloomwalker_boots', 'showstopper_charm', 'market_crest_scroll']) await run(`${O}loot insert ${B} loot bm:items/${r}`);
  await sleep(2500);
  const c = await contents(bx, Y, bz);
  ok('the six Dark Auction relics scrapped: a Trophy and 2 Medallions each (6 Trophies, 12 Medallions)', c.trophy === 6 && c.medallion === 12 && !c.auroral_crown && !c.rat_familiar, JSON.stringify(c));
  await run(`${O}setblock ${B} minecraft:air`); await run(`${O}kill @e[type=minecraft:marker,tag=bm.rs_scrap_bin,x=${bx},y=${Y},z=${bz},distance=..2]`);

  // ---- a hundred Dread zombies, struck down with a Looting III sword
  await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword[enchantments={"minecraft:looting":3,"minecraft:sharpness":5}]');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500);
  let kills = 0;
  for (let wave = 0; wave < 20; wave++) {
    for (let i = 0; i < 5; i++) await run(`${O}summon minecraft:zombie ${X - 2 + i + 0.5} ${Y} ${Z + 2.5} {Tags:["bm.seen","bm.dnew","t284"],NoAI:1b,Silent:1b}`);
    await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.dnew] run function bm:p176/mk/zombie`); await run(`${O}tag @e[tag=bm.dnew] remove bm.dnew`);
    await run(`${O}execute as @e[type=minecraft:zombie,tag=t284] run data merge entity @s {Health:1f,NoAI:1b}`); await run(`${O}effect clear @e[type=minecraft:zombie,tag=t284]`);
    await sleep(500);
    for (let i = 0; i < 5; i++) {
      const sel = `@e[type=minecraft:zombie,tag=t284,x=${X - 2 + i + 0.5},y=${Y},z=${Z + 2.5},distance=..0.8,limit=1]`;
      const e = await uuidEnt(sel); if (!e) continue;
      for (let k = 0; k < 4 && (await cnt(sel)); k++) { A.attack(e); await sleep(650); }
      if (!(await cnt(sel))) kills++;
    }
  }
  await sleep(1500);
  let tokens = 0;
  // (the drops counted by stack: every Dread Token item on the floor)
  for (let i = 0; i < 60; i++) { const r = await run(`${O}data get entity @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12,nbt={Item:{components:{"minecraft:custom_data":{bm:"dread_token"}}}},limit=1,sort=nearest] Item.count`);
    const m = r.match(/(\d+)$/); if (!m) break; tokens += +m[1]; await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12,nbt={Item:{components:{"minecraft:custom_data":{bm:"dread_token"}}}},limit=1,sort=nearest]`); }
  ok(`a hundred Dread zombies struck down (${kills})`, kills >= 95, `${kills}`);
  ok('...with Looting III: about one Dread Token in twenty (1..14 of them - Looting doesn\'t add)', tokens >= 1 && tokens <= 14, `${tokens} Dread Tokens from ${kills}`);
  await run(`${O}kill @e[tag=t284]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..14]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
