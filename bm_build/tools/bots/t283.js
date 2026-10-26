// 2.94x: THE SMUGGLER'S WAYTOKEN (phase225), as a regular (non-op) player, in t162's market (placed if a last run hasn't):
//   bought from the Fence (3 Medallions - 4 in your pack, rcon: the stage; one left over); unstamped, used out in the world: "Unstamped"; used inside the market:
//   stamped for it (its lore says where); carried off far away (rcon: the stage - a journey) to x and z below 0, facing west:
//   used - at the market's doorstep; used there again - back where you were (the very block: below 0 too), facing west;
//   used at the market with no way back: "at its market already"; in the pack's own worlds (the Hollow Throne): "cold here".
//   And (2.94x) a Blood Moon or Lucky Night heist's guard, struck down: it drops nothing. A heist's hidden passage, opened (its crack right-clicked): the wall crumbles, and no bricks drop.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1, 4).map(Number) : null; };
  const yaw = async () => +(((await run('data get entity TestRat Rotation[0]')).match(/(-?[\d.]+)f$/) || [0, NaN])[1]);
  const has = async (iid) => { const m = (await run(`execute store result score #h bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)) && (await run('scoreboard players get #h bm.rng')).match(/has (\d+)/); return m ? +m[1] : 0; };
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const trade = async (sel, iid) => {
    let idx = -1;
    for (let i = 0; i < 40 && idx < 0; i++) if (new RegExp(`"${iid}"`).test(await run(`${O}data get entity ${sel} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`))) idx = i;
    const eid = await uuidEnt(sel); A.windows.length = 0; A.interact(eid); await sleep(1200);
    const w = A.windows[A.windows.length - 1];
    if (w && idx >= 0) {
      A.write('select_trade', { slot: idx }); await sleep(400);
      A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
      A.close(w.windowId); await sleep(500);
    }
    return idx;
  };
  const use = async () => { A.slot(0); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(1200); };
  const CX = 24000, CY = 30, CZ = 24000;
  const EXIT = [CX + 38.5, CY + 18, CZ + 88.5];
  const FX = -18300, FY = 100, FZ = -16300;                // (far off, below 0: the way back must find the very block)
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${CX} ${CZ} ${CX + 76} ${CZ + 96}`);
  await run(`${O}forceload add ${FX - 8} ${FZ - 8} ${FX + 8} ${FZ + 8}`);
  await run(`${O}fill ${FX - 6} ${FY - 1} ${FZ - 6} ${FX + 6} ${FY - 1} ${FZ + 6} minecraft:stone`); await run(`${O}fill ${FX - 6} ${FY} ${FZ - 6} ${FX + 6} ${FY + 4} ${FZ + 6} minecraft:air`);
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) { let pl = ''; for (let i = 0; i < 30; i++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
  const FENCE = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${CX + 38},y=${CY},z=${CZ + 46},distance=..80,limit=1]`;
  ok('the market has its Fence', await wait(30000, async () => (await cnt(FENCE)) === 1, 1000));

  // ---- bought from the Fence
  await run(`${O}execute at ${FENCE} run tp TestRat ^ ^ ^1.5 facing entity ${FENCE} eyes`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.1 loot bm:items/medallion'); await run('item modify entity TestRat hotbar.1 {type:"minecraft:set_count",count:4}'); await sleep(300);
  const idx = await trade(FENCE, 'waytoken');
  ok('the Fence sells the Smuggler\'s Waytoken - bought for 3 Medallions', idx >= 0 && (await has('waytoken')) === 1 && (await has('medallion')) === 1, `offer ${idx} token ${await has('waytoken')} medallions left ${await has('medallion')}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"waytoken"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/waytoken');   // (into the hand)

  // ---- unstamped, out in the world
  await run(`${O}tp TestRat ${FX + 0.5} ${FY} ${FZ + 0.5} 90 0`); await sleep(1500); A.stand(); A.bars.length = 0;
  await use();
  ok('used unstamped, out in the world: "Unstamped - use it inside a Black Market"', A.bars.some(b => /Unstamped/.test(b)), A.bars.slice(-2).join(' | '));
  // ---- stamped in the market
  await run(`${O}tp TestRat ${CX + 38.5} ${CY + 12} ${CZ + 46.5} 0 0`); await sleep(2500); A.stand(); A.chats.length = 0; await sleep(2000);
  await use();
  const item = await run('data get entity TestRat SelectedItem.components');
  ok('used inside the market: stamped for it ("Waytoken stamped"), its doorstep in the token', A.chats.some(c => /Waytoken stamped/.test(c)) && /bm_way/.test(item), item.slice(0, 200));
  ok('...its lore says which market', new RegExp(`Black Market at ${Math.floor(EXIT[0])}, ${Math.floor(EXIT[2])}`).test(item), (item.match(/Stamped[^"]*/) || [''])[0]);
  A.bars.length = 0; await sleep(2500); await use();
  ok('used there again with nowhere to go back to: "at its market already"', A.bars.some(b => /market already/.test(b)), A.bars.slice(-2).join(' | '));

  // ---- the journey: far off (below 0), facing west; there and back
  await run(`${O}tp TestRat ${FX + 2.5} ${FY} ${FZ - 3.5} 90 0`); await sleep(2000); A.stand(); await sleep(2500);
  const p0 = await pos('TestRat');
  await use();
  const p1 = await pos('TestRat');
  ok('used out in the world: at the market\'s doorstep', p1 && Math.hypot(p1[0] - EXIT[0], p1[2] - EXIT[2]) <= 1.5 && Math.abs(p1[1] - EXIT[1]) <= 2, JSON.stringify(p1));
  await sleep(3500); await use();
  const p2 = await pos('TestRat');
  ok('used there again: back where you were - the very block (below 0)', p2 && Math.floor(p2[0]) === Math.floor(p0[0]) && Math.floor(p2[2]) === Math.floor(p0[2]) && Math.abs(p2[1] - p0[1]) < 1.1,
     `${JSON.stringify(p0)} -> ${JSON.stringify(p2)}`);
  ok('...facing the way you were (west)', Math.abs(((await yaw()) - 90 + 540) % 360 - 180) <= 5, `${await yaw()}`);
  await sleep(3500); A.bars.length = 0; await use();
  ok('...and the way back spent: used again, it\'s off to the market once more', (await pos('TestRat')) && Math.hypot((await pos('TestRat'))[0] - EXIT[0], (await pos('TestRat'))[2] - EXIT[2]) <= 1.5);
  await sleep(3500); await use();

  // ---- not in the pack's own worlds
  await run('execute in bm:hollow_throne run tp TestRat 0.5 200 0.5'); await run('effect give TestRat minecraft:slow_falling 20 0 true'); await sleep(1500); A.bars.length = 0; await sleep(3200); await use();
  ok('in the pack\'s own worlds (the Hollow Throne): "The token is cold here"', A.bars.some(b => /cold here/.test(b)), A.bars.slice(-2).join(' | '));
  await run(`${O}tp TestRat ${FX + 0.5} ${FY} ${FZ + 0.5} 90 0`); await sleep(1500);

  // ---- (2.94x) a heist's hidden passage: right-clicked, it crumbles - nothing drops
  await run(`${O}fill ${FX + 3} ${FY} ${FZ} ${FX + 3} ${FY + 1} ${FZ} minecraft:cracked_stone_bricks`);
  await run(`${O}summon minecraft:interaction ${FX + 3.5} ${FY} ${FZ + 0.5} {width:1.1f,height:2.1f,Tags:["bm.gvhvi","t283"]}`); await sleep(800);
  await run(`${O}tp TestRat ${FX + 1.5} ${FY} ${FZ + 0.5} -90 10`); await sleep(1200); A.stand();
  const ie = await uuidEnt(`@e[type=minecraft:interaction,tag=t283,limit=1]`);
  if (ie) A.interact(ie); await sleep(1500);
  ok('a hidden passage right-clicked: the wall crumbles', await passes(`${O}execute if block ${FX + 3} ${FY} ${FZ} minecraft:air if block ${FX + 3} ${FY + 1} ${FZ} minecraft:air`), `bot saw it: ${!!ie}`);
  ok('...and no cracked bricks drop (none on the floor, none in your pack)', (await cnt(`@e[type=minecraft:item,x=${FX + 3},y=${FY},z=${FZ},distance=..6]`)) === 0 &&
     !/cracked_stone_bricks/.test(await run('data get entity TestRat Inventory')));

  // ---- (2.94x) a Blood Moon heist's guard, and a Lucky Night's (rcon: the night set and one stood up, as the heist does): you
  //      strike it down - and it drops nothing (a guard's loot: no emeralds, charms or Tokens)
  for (const [gn, night] of [[1, 'Blood Moon'], [2, 'Lucky Night']]) {
    await run(`${O}kill @e[type=minecraft:item,x=${FX},y=${FY},z=${FZ},distance=..12]`);
    await run(`scoreboard players set #gn bm.rng ${gn}`); await run('scoreboard players set #gt bm.rng 1'); await run('scoreboard players set #gi bm.rng 0'); await run('scoreboard players set #gm bm.rng 0');
    await run(`${O}execute positioned ${FX - 2.5} ${FY} ${FZ + 0.5} run function bm:p70/guard`); await sleep(600);
    const G = `@e[tag=bm.gvg,x=${FX - 2.5},y=${FY},z=${FZ + 0.5},distance=..3,limit=1]`;
    await run(`${O}data merge entity ${G} {NoAI:1b,Tags:["bm.gvg","t283","bm.seen","bm.tiered"]}`); await run(`${O}effect clear ${G}`); await run(`${O}data modify entity ${G} Health set value 1f`);
    await run(`${O}tp TestRat ${FX - 0.5} ${FY} ${FZ + 0.5} 90 10`); await sleep(1200); A.stand();
    const ge = await uuidEnt(G); for (let i = 0; i < 6 && (await cnt(G)); i++) { if (ge) A.attack(ge); await sleep(700); }
    await sleep(800);
    const drops = await run(`${O}data get entity @e[type=minecraft:item,x=${FX},y=${FY},z=${FZ},distance=..10,limit=1] Item`);
    ok(`a ${night} heist's guard struck down: it drops nothing (no emeralds, charms or Tokens)`, (await cnt(G)) === 0 && (await cnt(`@e[type=minecraft:item,x=${FX},y=${FY},z=${FZ},distance=..10]`)) === 0,
       `${await cnt(G)} left; ${drops.slice(0, 160)}`);
  }
  await run('scoreboard players set #gn bm.rng 0');

  await run(`${O}kill @e[tag=t283]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${FX - 8} ${FZ - 8} ${FX + 8} ${FZ + 8}`); await run(`${O}forceload remove ${CX} ${CZ} ${CX + 76} ${CZ + 96}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
