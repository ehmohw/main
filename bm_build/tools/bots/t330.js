// 3.0b: THE PIXEL CREEPER (phase256), as a regular (non-op) player. Hard mode on (rcon - the test server keeps it off): bought
// from the Pixel Villager in the Arcade (t162's market) for Dread Tokens, a real trade. Then on a pad: the companion pops out
// beside the player (one, theirs), hops about them (it moves; its frames squat and stand; its display rises in a hop), turns to
// look at them between hops, keeps up when they move off (a leap), hisses now and then (the hiss heard - and nothing hurt);
// two carried: still one; the item in the off hand only: still there; dropped (Q): it's gone; picked up again: back;
// spectator: gone; survival: back. Hung in an item frame with a right-click: the frame holds it (and the item's 'fixed' model
// is the hopping strip - what a frame shows), and the framed one hisses now and then; set in a display case: the hopping
// figurine on the cushion. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const num = async (sel, p) => +(((await run(`${O}data get entity ${sel} ${p}`)).match(/(-?[\d.]+)[dfbsL]?$/) || [0, NaN])[1]);
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); A.stand(); };
  const trade = async (sel, iid) => {
    let idx = -1;
    for (let i = 0; i < 40 && idx < 0; i++) if (new RegExp(`"${iid}"`).test(await run(`${O}data get entity ${sel} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`))) idx = i;
    const price = idx >= 0 ? await num(sel, `Offers.Recipes[${idx}].buy.count`) : NaN;
    return { idx, price, go: async () => {
      const eid = await uuidEnt(sel); A.windows.length = 0; A.interact(eid); await sleep(1200);
      const w = A.windows[A.windows.length - 1];
      if (w && idx >= 0) {
        A.write('select_trade', { slot: idx }); await sleep(400);
        A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
        A.close(w.windowId); await sleep(500);
      }
      return !!w; } };
  };
  const CR = '@e[type=minecraft:item_display,tag=bm.pcr]';
  const crCount = () => cnt(CR);
  const pid = async () => +(((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, -9])[1]);
  const dist = (a, b) => Math.hypot(a[0] - b[0], a[2] - b[2]);

  // (t162's market: template (x, y, z) is the world's (CX + x, CY + y, CZ + z))
  const CX = 24000, CY = 30, CZ = 24000, W = 10;
  const VIL = `@e[type=minecraft:villager,tag=bm.arcvil,x=${CX + 26.5},y=${CY + W},z=${CZ + 51.6},distance=..2,limit=1]`;
  const X = 17900, Y = 100, Z = 16100;                                  // (the pad)

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run(`${O}kill ${CR}`);
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');

  // ================================================================== 1. bought from the Pixel Villager
  await run(`${O}forceload add ${CX} ${CZ} ${CX + 76} ${CZ + 84}`);   // (the whole town: the market's patch runs only with it loaded)
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await cnt(MK))) { let pl = ''; for (let i = 0; i < 30; i++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
  await run('scoreboard players set #hardoff bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1');
  await run(`${O}tp TestRat ${CX + 25.5} ${CY + W} ${CZ + 54.5} 180 0`); await sleep(1500); A.stand();
  ok('Hard mode on: the Pixel Villager behind the Arcade\'s counter', await wait(25000, async () => (await cnt(VIL)) === 1, 500));
  let t = await trade(VIL, 'px_creeper');                             // (a villager standing from before the build: the market's patch hands him the new stock, every 10 s)
  for (let i = 0; i < 12 && t.idx < 0; i++) { await sleep(1500); t = await trade(VIL, 'px_creeper'); }
  ok('...he sells a Pixel Creeper (Dread Tokens, priced like the Arcade\'s other display pieces)', t.idx >= 0 && t.price >= 1 && t.price <= 4, JSON.stringify(t));
  await run('clear TestRat *[minecraft:custom_data~{bm:"dread_token"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_token');
  await run(`item modify entity TestRat hotbar.0 {type:"minecraft:set_count",count:${t.price || 3}}`); A.slot(0); await sleep(300);
  const opened = await t.go();
  ok('Right-click him: the Pixel Creeper bought, the tokens paid', opened && (await has('px_creeper')) === 1 && (await has('dread_token')) === 0,
     `opened ${opened} creeper ${await has('px_creeper')} tokens ${await has('dread_token')}`);
  ok('...its lore: it hops along beside you while it\'s in your inventory', /hops/.test(await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"px_creeper"}}}].components."minecraft:lore"')));
  // (in the shop, with the item: a creeper out already - fine; the pad's the stage)
  await run('scoreboard players set #hard bm.cfg 0'); await run('scoreboard players set #hardoff bm.cfg 1');

  // ================================================================== 2. on the pad: it comes out and hops about you
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(1500);
  await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} minecraft:grass_block`); await run(`${O}fill ${X - 14} ${Y + 1} ${Z - 14} ${X + 14} ${Y + 8} ${Z + 14} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('time set noon'); await run('weather clear');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const NEARME = `${CR.slice(0, -1)},x=${X + 0.5},y=${Y + 1},z=${Z + 0.5},distance=..3]`;    // (the one from the shop pops away: too far)
  ok('the Pixel Creeper pops out beside you (one)', await wait(5000, async () => (await crCount()) === 1 && (await cnt(NEARME)) === 1), `${await crCount()} near ${await cnt(NEARME)}`);
  ok('...yours (your player id)', (await cnt(`${CR.slice(0, -1)},scores={bm.pid=${await pid()}}]`)) === 1);
  const scale = await num(`${CR.slice(0, -1)},limit=1]`, 'transformation.scale[0]');
  const t0y = await num(`${CR.slice(0, -1)},limit=1]`, 'transformation.translation[1]');
  ok('...little (about half a block tall)', scale > 0.4 && scale < 0.8, `scale ${scale}`);
  ok('...never glowing', !/Glowing: 1b/.test(await run(`${O}data get entity ${CR.slice(0, -1)},limit=1]`)));
  const me = [X + 0.5, Y + 1, Z + 0.5];
  const seen = new Set(); let moved = 0, maxUp = 0, maxD = 0, last = null, facing = [];
  for (let k = 0; k < 60; k++) {                                      // (12 seconds, a look every 200 ms)
    const s = `${CR.slice(0, -1)},limit=1]`;
    const cmd = (await run(`${O}data get entity ${s} item.components."minecraft:custom_model_data".strings[0]`)).match(/"(\w+)"$/);
    if (cmd) seen.add(cmd[1]);
    const up = await num(s, 'transformation.translation[1]'); maxUp = Math.max(maxUp, up - t0y);
    const p = await epos(s); if (p) { if (last && dist(p, last) > 0.2) moved++; last = p; maxD = Math.max(maxD, dist(p, me)); }
    if (p && /has 0\b/.test(await run(`scoreboard players get ${s} bm.pcrs`)) && /has [1-9]/.test(await run(`scoreboard players get ${s} bm.pcrt`))) {
      const yaw = await num(s, 'Rotation[0]'); const want = Math.atan2(-(me[0] - p[0]), me[2] - p[2]) * 180 / Math.PI;
      facing.push(Math.abs(((yaw - want) % 360 + 540) % 360 - 180));
    }
    await sleep(200);
  }
  ok('it hops about you: it moves (hop by hop)', moved >= 2, `moves ${moved}`);
  ok('...squatting and landing (its frames: crouch, stand - and half, a tick at a time, seen or not)', seen.has('crouch') && seen.has('stand'), [...seen].join(','));
  ok('...rising in each hop (its display lifted)', maxUp > 0.3, `up ${maxUp.toFixed(2)}`);
  ok('...staying near you', maxD > 0 && maxD < 4.5, `farthest ${maxD.toFixed(2)}`);
  ok('...and between hops it turns to look at you', facing.length > 0 && Math.min(...facing) < 40, facing.map(f => f.toFixed(0)).join(','));
  // (it keeps up: you move off 8 blocks - it leaps after you)
  await at(X + 8.5, Y + 1, Z + 0.5, 0, 0); const me2 = [X + 8.5, Y + 1, Z + 0.5];
  ok('you move off 8 blocks: it hops after you and is by your side again', await wait(6000, async () => { const p = await epos(`${CR.slice(0, -1)},limit=1]`); return p && dist(p, me2) < 3; }),
     JSON.stringify(await epos(`${CR.slice(0, -1)},limit=1]`)));
  ok('...still just the one', (await crCount()) === 1);
  // (the hiss: heard, and nothing hurt)
  A.sounds.length = 0; const hp0 = await num('@a[name=TestRat,limit=1]', 'Health');
  ok('now and then it hisses (heard) - and goes white-hot', await wait(90000, async () => A.sounds.some(s => /creeper\.primed/.test(s.name)), 500),
     A.sounds.slice(-3).map(s => s.name).join(','));
  await sleep(1500);
  ok('...and nothing happens: no damage, the ground whole, the creeper still there', (await num('@a[name=TestRat,limit=1]', 'Health')) >= hp0 &&
     !/Successfully filled [1-9]/i.test(await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} minecraft:grass_block replace minecraft:air`)) && (await crCount()) === 1);

  // ================================================================== 3. one per player; the off hand; dropped; spectator
  await run('loot give TestRat loot bm:items/px_creeper'); await sleep(2500);
  ok('two carried: still one creeper', (await crCount()) === 1, `${await crCount()}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"px_creeper"}] 1'); await sleep(300);
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/px_creeper'); A.slot(0); await sleep(300);
  A.swap(); await sleep(600);                                         // (F: into the off hand)
  ok('the item swapped into the off hand (F)', /px_creeper/.test(await run('data get entity TestRat equipment.offhand')));
  await sleep(2500);
  ok('...the creeper\'s still out', (await crCount()) === 1);
  A.swap(); await sleep(600); A.slot(0); await sleep(300);
  A.drop(); await sleep(500);                                         // (Q)
  ok('the item dropped (Q)', (await has('px_creeper')) === 0);
  ok('...and the creeper is gone (a puff)', await wait(3000, async () => (await crCount()) === 0));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/px_creeper');
  ok('given back: it pops out again', await wait(4000, async () => (await crCount()) === 1));
  await run('gamemode spectator TestRat');
  ok('spectator: gone', await wait(3000, async () => (await crCount()) === 0));
  await run('gamemode survival TestRat'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  ok('survival again: back', await wait(4000, async () => (await crCount()) === 1));
  await run('loot replace entity TestRat hotbar.0 loot minecraft:empty'); await run('clear TestRat');
  ok('stashed away (out of the inventory): gone', await wait(3000, async () => (await crCount()) === 0));

  // ================================================================== 4. in an item frame
  await run(`${O}fill ${X - 4} ${Y + 1} ${Z + 5} ${X + 4} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t330f"]}`); await sleep(400);
  const FR = `@e[type=minecraft:item_frame,tag=bm.t330f,x=${X},y=${Y + 2},z=${Z + 4},distance=..2,limit=1]`;
  await run('loot replace entity TestRat hotbar.0 loot bm:items/px_creeper');
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10); A.slot(0); await sleep(300);
  let fr = null; await wait(4000, async () => (fr = await uuidEnt(FR)) != null, 250);
  if (fr) A.interact(fr); await sleep(1200);
  ok('hung in an item frame (a right-click): the frame holds it', /px_creeper/.test(await run(`${O}data get entity ${FR} Item`)) && (await has('px_creeper')) === 0);
  ok('...and no creeper hops about you (it\'s on the wall)', await wait(3000, async () => (await crCount()) === 0));
  const RP = path.join(__dirname, '..', '..', 'out_p2', 'BlackMarket_RP', 'assets', 'bm');
  let def = {}; try { def = JSON.parse(fs.readFileSync(path.join(RP, 'items', 'px_creeper.json'))); } catch (e) {}
  const fixed = ((def.model || {}).cases || []).find(c => c.when === 'fixed');
  ok('...what a frame shows (the item\'s \'fixed\' model): the hopping creeper, an animated strip', fixed && /pxcr_framed/.test(fixed.model.model) &&
     fs.existsSync(path.join(RP, 'textures', 'block', 'pxcr_hop.png.mcmeta')), JSON.stringify(fixed));
  A.sounds.length = 0;
  ok('...and now and then the framed one hisses', await wait(90000, async () => A.sounds.some(s => /creeper\.primed/.test(s.name)), 500));
  ok('...still no creeper of yours about (you don\'t carry it)', (await crCount()) === 0);
  A.attack(fr); await sleep(800);
  await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t330f]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`);

  // ================================================================== 5. in a display case: the hopping figurine
  await run('clear TestRat'); await at(X + 0.5, Y + 1, Z - 3.5, 0, 70);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/display_case_oak'); await run('loot replace entity TestRat hotbar.1 loot bm:items/px_creeper');
  A.slot(0); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(500);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z - 2.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const box = await uuidEnt(caseSel); A.slot(1); await sleep(300);
  if (box) A.interact(box); await sleep(900);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X + 0.5},y=${Y + 1},z=${Z - 2.5},distance=..1.5]`;
  ok('the Pixel Creeper set in it: its figurine on the cushion - the hopping one', (await cnt(FIG)) === 1 &&
     /pxcr_framed/.test(await run(`${O}data get entity ${FIG.slice(0, -1)},limit=1] item.components`)));
  const fy = await num(`${FIG.slice(0, -1)},limit=1]`, 'transformation.translation[1]'), fs_ = await num(`${FIG.slice(0, -1)},limit=1]`, 'transformation.scale[0]');
  ok('...its feet on the cushion, sized to the glass (hop and all)', Math.abs(fy - 0.4375 * fs_) < 0.01 && fs_ * 1.11 <= 0.61, `y ${fy} scale ${fs_}`);
  ok('...and no creeper hops about you (the item\'s in the case)', await wait(3000, async () => (await crCount()) === 0));
  await run(`${O}kill @e[tag=bm.dchit,x=${X},y=${Y},z=${Z},distance=..12]`); await run(`${O}kill @e[tag=bm.dcase,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}kill @e[tag=bm.dcitem,x=${X},y=${Y},z=${Z},distance=..12]`); await run(`${O}kill @e[tag=bm.dcfg,x=${X},y=${Y},z=${Z},distance=..12]`);

  // ---------------------------------------------------------------- clean up
  await run('clear TestRat'); await run(`${O}kill ${CR}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
