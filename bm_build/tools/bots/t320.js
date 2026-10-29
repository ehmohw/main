// 2.99a: THE BACKPACK (phase248) as a regular (non-op) player, every step a real packet. rcon sets the stage only: a floor, the
// Fence at his stall, the Tokens to pay with, the things to pack, the Undercrown placed, a block set where the barrel stands.
//   buy      the Fence sells the Backpack: his window opened, the trade picked, the backpack taken out, the Tokens gone
//   store    used, it unfolds into a barrel in front of you (out of your hand); opened, three stacks shift-clicked in; sneak:
//            it folds back into your hand, the barrel gone - and the stacks ride in the item (its minecraft:container)
//   two      a second backpack, its own load; using it while the first is out folds the first; each keeps its own
//   dungeon  in the Undercrown (Adventure mode): it unfolds on open floor, takes a stack, folds back - the dungeon's blocks
//            just as they were (compared with a copy taken before); out again, a block set where its barrel stood (as a
//            dungeon's door or rebuild would) - it folds back with all it held, the block left alone, nothing on the ground
//   nest     one backpack shift-clicked into another's barrel is handed straight back; the first folds without it
//   node t320.js [buy|store|two|dungeon|nest]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const O = 'execute in minecraft:overworld run ', N = 'execute in minecraft:the_nether run ';
const X = 20800, Y = 100, Z = 16800;                       // (the field: the bot stands at X+.5 Y+1 Z+.5 facing south; the barrel is X Y+1 Z+2)
const UO = [2560, 6, -2560];                               // (p2/undercfg.ORIGIN)
const BP = '{components:{"minecraft:custom_data":{bm:"backpack"}}}';
const HB = (n) => 54 + n;                                  // (a 9x3 container window: hotbar slot n)

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (D, sel) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (D, sel, path) => (await run(`${D}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const passes = async (c) => /passed/i.test(await run(c));
  const pos = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const uuidOf = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (D, sel) => { const u = await uuidOf(D, sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  // (a backpack's load, read from the item: the one in a hotbar slot, or any backpack holding a given item)
  const load = async (slot) => nbt(O, 'TestRat', `Inventory[{Slot:${slot}b}].components."minecraft:container"`);
  const holding = async (id) => nbt(O, 'TestRat', `Inventory[{components:{"minecraft:custom_data":{bm:"backpack"},"minecraft:container":[{item:{id:"${id}"}}]}}].components."minecraft:container"`);
  const barrel = async (D, p) => passes(`${D}execute if block ${p[0]} ${p[1]} ${p[2]} minecraft:barrel`);
  // (use the held backpack: right-click into the air, let go)
  const use = async () => { A.use(); await sleep(350); A.release(); await sleep(400); };
  // (open the barrel at p as a player - a right-click on its top - and shift-click the given hotbar slots into it)
  const fill = async (p, slots) => {
    A.windows.length = 0; A.useOn(p[0], p[1], p[2], 1); await wait(2000, async () => A.windows.length > 0, 100);
    const w = A.windows[A.windows.length - 1];
    if (w) { for (const n of slots) { A.write('window_click', { windowId: w.windowId, stateId: 0, slot: HB(n), mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(450); } }
    return w;
  };
  const shut = async (w) => { if (w) { A.close(w.windowId); await sleep(400); } };
  // (sneak: the open bag packs itself up)
  const sneak = async () => { A.input({ shift: true }); await sleep(900); A.input({}); await sleep(500); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (2.99a: phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await sleep(300);
  const B = [X, Y + 1, Z + 2];
  const field = async () => { await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await at(O, X + 0.5, Y + 1, Z + 0.5, 0, 0); };

  // ---------------------------------------------------------------- the Fence sells it: a real trade
  if (on('buy')) {
    await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z - 4.5} rotated 0 0 run function bm:npc/fence`); await sleep(1200);
    const FEN = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 0.5},y=${Y + 1},z=${Z - 4.5},distance=..2,limit=1]`;
    let idx = -1;
    for (let i = 0; i < 60 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(O, FEN, `Offers.Recipes[${i}].sell.count`))) break; const s = await nbt(O, FEN, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/"backpack"/.test(s)) idx = i; }
    ok('the Fence sells the Backpack', idx >= 0, `trade #${idx}`);
    const price = idx < 0 ? 0 : +(((await nbt(O, FEN, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
    const buyId = idx < 0 ? '' : (await nbt(O, FEN, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
    ok('...cheap, an early-game price: 5 Tokens', buyId === 'token' && price === 5, `${price} ${buyId}`);
    await run('clear TestRat'); for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
    await at(O, X + 0.5, Y + 1, Z - 2.5, 180, 0);
    const fen = await entOf(O, FEN); A.windows.length = 0; if (fen) A.interact(fen.entityId); await sleep(900);
    const w = A.windows[A.windows.length - 1];
    ok('right-clicking the Fence opens his trades', !!w);
    if (w && idx >= 0) {
      A.write('select_trade', { slot: idx }); await sleep(300);
      A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
      A.close(w.windowId); await sleep(400);
    }
    ok(`...bought in his window: a backpack in the pack, the ${price} ${buyId}s gone`, (await has('backpack')) === 1 && (await has(buyId)) === 0);
    ok('...an empty bag that holds one to a slot (stack size 1, its own empty container)',
       /max_stack_size": 1|max_stack_size":1/.test(await nbt(O, 'TestRat', `Inventory[${BP}].components`)) && /^\[\]$/.test((await nbt(O, 'TestRat', `Inventory[${BP}].components."minecraft:container"`)).trim()),
       (await nbt(O, 'TestRat', `Inventory[${BP}].components."minecraft:container"`)).slice(0, 80));
    // (the one bought: into hotbar slot 0 for what follows)
    const slot = +(((await nbt(O, 'TestRat', `Inventory[${BP}].Slot`)).match(/(-?\d+)/) || [0, -1])[1]);
    if (slot !== 0 && slot >= 0) { await run(`item replace entity TestRat hotbar.0 from entity TestRat ${slot < 9 ? 'hotbar.' + slot : 'inventory.' + (slot - 9)}`);
      await run(`item replace entity TestRat ${slot < 9 ? 'hotbar.' + slot : 'inventory.' + (slot - 9)} with minecraft:air`); }
    await run(`${O}kill ${FEN}`);
  }

  // ---------------------------------------------------------------- storing: open, three stacks in, folded - they ride in the item
  if (on('store') || on('two') || on('nest')) {
    if ((await has('backpack')) !== 1 || !/backpack/.test(await nbt(O, 'TestRat', 'Inventory[{Slot:0b}]'))) { await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/backpack'); }
  }
  if (on('store') || on('two')) {
    await field();
    await run('item replace entity TestRat hotbar.1 with minecraft:cobblestone 32'); await run('item replace entity TestRat hotbar.2 with minecraft:iron_ingot 5');
    await run('loot replace entity TestRat hotbar.3 loot bm:items/token'); await run('item modify entity TestRat hotbar.3 {type:"minecraft:set_count",count:3}');
    A.slot(0); await sleep(250); A.bars.length = 0; await use();
    ok('used: it unfolds into a barrel in front of you', await wait(2000, async () => barrel(O, B)));
    ok('...out of your hand while it\'s out (held for you)', (await has('backpack')) === 0);
    ok('...named for it', /Backpack/.test(await run(`${O}data get block ${B[0]} ${B[1]} ${B[2]} CustomName`)));
    const w = await fill(B, [1, 2, 3]);
    ok('opened as a player: its window', !!w);
    ok('...three stacks shift-clicked in', await wait(2000, async () => /cobblestone/.test(await run(`${O}data get block ${B[0]} ${B[1]} ${B[2]} Items`)) &&
       /iron_ingot/.test(await run(`${O}data get block ${B[0]} ${B[1]} ${B[2]} Items`)) && (await has('token')) === 0));
    await shut(w);
    await sneak();
    ok('sneak: it folds back - the barrel gone, the backpack back in your hand', await wait(3000, async () => !(await barrel(O, B))) &&
       /backpack/.test(await nbt(O, 'TestRat', 'Inventory[{Slot:0b}]')));
    ok('...the barrel\'s spot is air again', await passes(`${O}execute if block ${B[0]} ${B[1]} ${B[2]} minecraft:air`));
    const c = await load(0);
    ok('...and the stacks ride in the item (its container: 32 cobblestone, 5 iron, 3 Tokens)', /cobblestone/.test(c) && /count: 32/.test(c) && /iron_ingot/.test(c) &&
       /count: 5/.test(c) && /bm: "token"|bm:"token"/.test(c), c.slice(0, 300));
    ok('...nothing left on the ground', (await cnt(O, `@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8]`)) === 0);
  }

  // ---------------------------------------------------------------- two backpacks: each its own load
  if (on('two')) {
    await field();
    await run('loot replace entity TestRat hotbar.4 loot bm:items/backpack'); await run('item replace entity TestRat hotbar.5 with minecraft:gold_ingot 7');
    A.slot(0); await sleep(250); await use();
    ok('the first one out', await wait(2000, async () => barrel(O, B)));
    A.slot(4); await sleep(300); await use(); await sleep(400);
    ok('the second one used: the first folds (back in the pack, its load kept), the second is out in its place',
       await wait(3000, async () => (await has('backpack')) === 1 && (await barrel(O, B)) && (await cnt(O, `@e[type=minecraft:marker,tag=bm.bxm,x=${X},y=${Y},z=${Z},distance=..8]`)) === 1) &&
       /cobblestone/.test(await holding('minecraft:cobblestone')));
    const w = await fill(B, [5]);
    ok('...gold put in the second', await wait(2000, async () => /gold_ingot/.test(await run(`${O}data get block ${B[0]} ${B[1]} ${B[2]} Items`))));
    await shut(w); await sneak();
    ok('...folded: two backpacks in the pack', await wait(3000, async () => (await has('backpack')) === 2 && !(await barrel(O, B))));
    const g = await holding('minecraft:gold_ingot'), cb = await holding('minecraft:cobblestone');
    ok('each keeps its own: one holds the gold (and no cobblestone)', /gold_ingot/.test(g) && !/cobblestone/.test(g), g.slice(0, 200));
    ok('...the other the cobblestone, iron and Tokens (and no gold)', /cobblestone/.test(cb) && /iron_ingot/.test(cb) && !/gold_ingot/.test(cb), cb.slice(0, 200));
  }

  // ---------------------------------------------------------------- no bag inside a bag
  if (on('nest')) {
    await field();
    await run('clear TestRat *[minecraft:custom_data~{bm:"backpack"}]');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/backpack'); await run('loot replace entity TestRat hotbar.4 loot bm:items/backpack');
    A.slot(0); await sleep(250); await use();
    ok('a backpack out', await wait(2000, async () => barrel(O, B)));
    A.bars.length = 0;
    const w = await fill(B, [4]);
    await sleep(1200);
    ok('the other shift-clicked into its barrel: handed straight back', !(await passes(`${O}execute if items block ${B[0]} ${B[1]} ${B[2]} container.* *[minecraft:custom_data~{bm:"backpack"}]`)) &&
       (await wait(3000, async () => (await has('backpack')) === 1)));
    ok('...and told so', A.bars.some(b => /No bags inside bags/i.test(b)), A.bars.slice(-2).join(' / '));
    await shut(w); await sneak();
    ok('folded: two backpacks in the pack, neither inside the other', await wait(3000, async () => (await has('backpack')) === 2) &&
       !(await passes(`execute if data entity TestRat Inventory[{components:{"minecraft:container":[{item:{components:{"minecraft:custom_data":{bm:"backpack"}}}}]}}]`)));
  }

  // ---------------------------------------------------------------- in a dungeon: the Undercrown, in Adventure mode
  if (on('dungeon')) {
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/backpack');
    await run('item replace entity TestRat hotbar.1 with minecraft:cobblestone 20'); await run('item replace entity TestRat hotbar.2 with minecraft:torch 4');
    if ((await sc('#uver', 'bm.p2')) < 1) await run('function bm:admin/under/place');
    ok('the stage: the Undercrown placed', await wait(900000, async () => (await sc('#uver', 'bm.p2')) >= 1, 2000));
    await run(`${N}forceload add ${UO[0]} ${UO[2]} ${UO[0] + 223} ${UO[2] + 223}`); await sleep(4000);
    const hub = await pos(N, `@e[type=minecraft:marker,tag=bm.pz1,x=${UO[0]},y=-64,z=${UO[2]},dx=223,dy=380,dz=223,limit=1]`);      // (the first trial room: floor all round)
    // (a spot on open floor: the bot's cell and the two ahead clear, the floor under the barrel solid, no dungeon marker by it)
    let S = null;
    if (!hub) ok('the Undercrown\'s first trial room found', false);
    for (let r = 3; r <= 14 && !S && hub; r++) {
      for (const [dx, dz] of [[r, 0], [-r, 0], [0, r], [0, -r], [r, r], [-r, -r], [r, -r], [-r, r]]) {
        for (const dy of [0, 1, -1, 2, -2, 3]) {
          const x = Math.floor(hub[0]) + dx, y = Math.floor(hub[1]) + dy, z = Math.floor(hub[2]) + dz;
          if (await passes(`${N}execute if block ${x} ${y} ${z} minecraft:air if block ${x} ${y + 1} ${z} minecraft:air unless block ${x} ${y - 1} ${z} #minecraft:replaceable ` +
            `if block ${x} ${y} ${z + 1} minecraft:air if block ${x} ${y + 1} ${z + 1} minecraft:air if block ${x} ${y} ${z + 2} #bm:p248_air ` +
            `unless block ${x} ${y - 1} ${z + 2} #minecraft:replaceable unless block ${x} ${y - 1} ${z + 2} #bm:p248_nofloor ` +
            `positioned ${x + 0.5} ${y} ${z + 2.5} unless entity @e[type=minecraft:marker,distance=..2.5]`)) { S = [x, y, z]; break; }
        }
        if (S) break;
      }
    }
    ok('a spot on the Undercrown\'s open floor', !!S, S ? S.join(' ') : `hub ${hub}`);
    if (S) {
      const DB = [S[0], S[1], S[2] + 2];
      const lo = [S[0] - 2, S[1] - 1, S[2]], hi = [S[0] + 2, S[1] + 2, S[2] + 4], cp = [S[0] - 2, 200, S[2]];
      await run(`${N}clone ${lo.join(' ')} ${hi.join(' ')} ${cp.join(' ')}`);           // (the dungeon's blocks there, copied up past the roof)
      await run('gamemode survival TestRat'); await run('tag TestRat remove bm.uadv');
      await at(N, S[0] + 0.5, S[1], S[2] + 0.5, 0, 0);
      ok('inside: Adventure mode', await wait(6000, async () => /: 2$/.test(await run('data get entity TestRat playerGameType'))));
      A.slot(0); await sleep(250); A.bars.length = 0; await use();
      ok('used in the dungeon: it unfolds on the open floor', await wait(2000, async () => barrel(N, DB)), A.bars.slice(-1).join(''));
      const w = await fill(DB, [2]);
      ok('...opened in Adventure mode: the torches in', await wait(2000, async () => /torch/.test(await run(`${N}data get block ${DB[0]} ${DB[1]} ${DB[2]} Items`))));
      await shut(w); await sneak();
      ok('...folded back into your hand', await wait(3000, async () => !(await barrel(N, DB))) && /torch/.test(await load(0)));
      ok('...and the dungeon\'s blocks are just as they were', await passes(`${N}execute if blocks ${lo.join(' ')} ${hi.join(' ')} ${cp.join(' ')} all`));
      // (out again - and a block set where the barrel stands, as a dungeon's door, reset or rebuild would set its own)
      await use();
      ok('out again', await wait(2000, async () => barrel(N, DB)));
      const w2 = await fill(DB, [1]); await sleep(300); await shut(w2);
      ok('...the cobblestone in', /cobblestone/.test(await run(`${N}data get block ${DB[0]} ${DB[1]} ${DB[2]} Items`)));
      await run(`${N}setblock ${DB[0]} ${DB[1]} ${DB[2]} minecraft:polished_blackstone_bricks`);
      ok('a dungeon block set over its barrel: it folds back with all it held (torches and cobblestone)',
         await wait(3000, async () => /backpack/.test(await nbt(O, 'TestRat', 'Inventory[{Slot:0b}]')) && /torch/.test(await load(0)) && /cobblestone/.test(await load(0))), (await load(0)).slice(0, 200));
      ok('...the dungeon\'s block left as it set it', await passes(`${N}execute if block ${DB[0]} ${DB[1]} ${DB[2]} minecraft:polished_blackstone_bricks`));
      ok('...and nothing spilled or doubled on the ground', (await cnt(N, `@e[type=minecraft:item,x=${DB[0]},y=${DB[1]},z=${DB[2]},distance=..6]`)) === 0 &&
         !/cobblestone/.test(await nbt(O, 'TestRat', 'Inventory[{id:"minecraft:cobblestone"}]')));
      await run(`${N}clone ${cp.join(' ')} ${cp[0] + 4} ${cp[1] + 3} ${cp[2] + 4} ${lo.join(' ')}`);       // (the stage put back, and the copy cleared)
      await run(`${N}fill ${cp.join(' ')} ${cp[0] + 4} ${cp[1] + 3} ${cp[2] + 4} minecraft:air`);
    }
    await run('execute in minecraft:overworld run tp TestRat 0 200 0');
    await wait(7000, async () => /: 0$/.test(await run('data get entity TestRat playerGameType')));
  }

  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('clear TestRat');
  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
