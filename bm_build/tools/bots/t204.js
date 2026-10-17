// 2.82b: CECIL'S TENT, THE CURIO WALK (2.82c: filled in again), AND A CREW PAGE THAT DOESN'T SPOIL - as a regular (non-op) player TestRat, every step a
// real packet (rcon sets the stage: t162's market, rebuilt into the current town if it's older; who TestRat has met).
//   THE MARKET'S HOSTS STAY HIDDEN: Cecil (and the Chef, the Armory) are invisible villagers under their models - a trader's
//   invisibility is no longer cleared for them (they showed as a plain villager on top of the model); one that loses it has it
//   back within a couple of seconds. Cecil's tent is dressed: shelves of books behind him, a counter with candles.
//   THE CURIO WALK (2.82c): rock again - it let you round the Dark Auction's key; the Cabinet's front wall is brown terracotta now
//   (dark oak there caught fire from the forge pit's lava).
//   THE RAID CREW PAGE: met only Cecil (no contracts) - the Ledger's Raid Crew lists Cecil, and no follower TestRat hasn't met;
//   its Outfits page has only Cecil's wardrobe, and nothing of Emma's buff.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const CX = 24000, CY = 30, CZ = 24000, W = 10, BF = 17;
  const T = (x, y, z) => [CX + x, CY + y, CZ + z];
  const at = async (x, y, z, yaw = 0) => { const [a, b, c] = T(x, y, z); await run(`${O}tp TestRat ${a} ${b} ${c} ${yaw} 0`);
    await wait(2500, async () => A.pos && Math.abs(A.pos.x - a) < 0.1 && Math.abs(A.pos.z - c) < 0.1, 100); await sleep(400); };
  const block = async (x, y, z, b) => passes(`${O}execute if block ${T(x, y, z).join(' ')} ${b}`);
  const host = (tag, extra = '') => `@e[type=minecraft:villager,tag=${tag},x=${CX},y=${CY - 4},z=${CZ},dx=80,dy=40,dz=100${extra}]`;
  const hidden = async tag => passes(`${O}execute if entity ${host(tag, ',predicate=bm:p126/invis')}`);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');

  // ---- the stage: the market, rebuilt into the current town on the way in if it's an old one
  await run(`${O}forceload add ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) {
    for (let t = 0; t < 30; t++) { const pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
  }
  await at(38.5, BF + 1, 79.5, 180);
  ok('the market is the current town (bm.m282c)', await wait(60000, async () => passes(`${O}execute if entity ${MK.replace(',limit=1', ',tag=bm.m282c,limit=1')}`), 500));
  await sleep(4000);

  // ---- the hosts under the models stay hidden
  await at(55.5, W, 70.5, 90);
  await wait(15000, async () => passes(`${O}execute if entity ${host('bm.npc_wizard')}`), 500);
  ok('Cecil\'s host is invisible under his model (so are the Chef\'s and the Armory\'s)', await wait(4000, async () =>
     (await hidden('bm.npc_wizard')) && (await hidden('bm.npc_chef')) && (await hidden('bm.npc_armory'))));
  await run(`${O}effect clear ${host('bm.npc_wizard')} minecraft:invisibility`);          // (the stage: it wore off)
  ok('...and if it wears off, it\'s back within a couple of seconds', await wait(3500, async () => hidden('bm.npc_wizard')));
  ok('Cecil\'s tent: shelves of books behind him, a counter with candles and a crystal, a rug, a soul lantern',
     (await block(51, W, 70, 'minecraft:bookshelf')) && (await block(54, W, 70, 'minecraft:polished_blackstone_bricks')) &&
     (await block(54, W + 1, 70, 'minecraft:purple_candle')) && (await block(54, W + 1, 71, 'minecraft:amethyst_cluster')) &&
     (await block(53, W, 71, 'minecraft:purple_carpet')) && (await block(53, W + 3, 71, 'minecraft:soul_lantern')));

  // ---- (2.82c) the Curio Walk filled in again (it led round the Dark Auction's key); the Cabinet's front won't catch from the forge pit
  const solid = async (x, y, z) => !(await block(x, y, z, 'minecraft:air'));
  ok('the Curio Walk is rock again: no way from the Dark Auction\'s plaza round to the Cabinet without the key',
     (await solid(46, W, 11)) && (await solid(48, W, 12)) && (await solid(50, W + 1, 11)) && (await solid(52, W, 12)));
  ok('Fishy\'s Cabinet has its door; its front wall is brown terracotta - three blocks from the forge pit\'s lava, and it won\'t burn',
     await wait(15000, async () => (await block(54, W, 10, 'minecraft:air')) && (await block(53, W + 1, 10, 'minecraft:gold_block')) &&
       (await block(58, W + 1, 10, 'minecraft:brown_terracotta')) && (await block(62, W + 2, 10, 'minecraft:brown_terracotta')), 500));

  // ---- the Raid Crew page: only who you've met
  const fcon = +((await run('scoreboard players get TestRat bm.fcon')).match(/has (-?\d+)/) || [0, 0])[1];
  await run('scoreboard players set TestRat bm.fcon 0');
  for (const k of ['emma', 'leo', 'omega', 'pistachio', 'fishy', 'apo', 'tul', 'demo', 'killerwatt', 'celi', 'zib', 'escort', 'frog', 'donado', 'dennis', 'pearl', 'wil', 'cecil']) await run(`advancement revoke TestRat only bm:met/${k}`);
  await run('advancement grant TestRat only bm:met/cecil');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); A.slot(0); await sleep(400);
  await A.useWait();
  const rc = await A.press(/Raid Crew/); await sleep(600);
  const labels = A.buttons().map(b => b.label);
  ok('met only Cecil: the Ledger\'s Raid Crew lists Cecil - and no follower TestRat hasn\'t met', !!rc && labels.some(l => /Cecil/.test(l)) &&
     !labels.some(l => /Emma|Leo|Omega|Pistachio|Fishy|Apophiss|Tullius|Democratus|KillerWatt|Celi|Dennis/.test(l)), labels.join(' | ').slice(0, 300));
  const op = await A.press(/Outfits/); await sleep(600);
  const ol = A.buttons().map(b => b.label);
  ok('...its Outfits page: only Cecil\'s wardrobe, and nothing of Emma\'s buff', !!op && ol.some(l => /Cecil's wardrobe/.test(l)) &&
     !ol.some(l => /Emma|Leo|Omega|Pistachio|Fishy|Apophiss|Tullius|Democratus|KillerWatt|Celi|Dennis|Zib|Wilfrey|Pearlman|Frog|Donado/.test(l)), ol.join(' | ').slice(0, 300));
  A.cmd('trigger bm.act set 2'); await sleep(300);

  // ---- clean up
  await run(`scoreboard players set TestRat bm.fcon ${fcon}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}tp TestRat ${CX + 38.5} ${CY + BF + 1} ${CZ + 79.5}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
