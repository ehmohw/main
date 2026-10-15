// 2.78: more weapons on the wall, as a regular (non-op) player: Cecil's staff, Leo's trident (his own model now, both forms),
// Apophiss's mace, the Frisbee Shield, a ray gun and the Sepulchre each hung with a sneak + drop (Q, as a client sends it) while
// facing a wall - the very weapon, its name kept, on its plaque, facing out. A drop without sneaking is just a drop; a sneak +
// drop with no wall in reach is just a drop too. Taken down again with a sneak + punch. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)(?:[dfbsL])?\s*$/) || [0, NaN])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const drop = async (C, slot, sneak) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(250); }
    C.write('block_dig', { status: 4, location: { x: 0, y: 0, z: 0 }, face: 0, sequence: C.seq++ }); await sleep(500); if (sneak) { C.input({}); await sleep(150); } };
  const X = 16300, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  for (const [x1, z1, x2, z2] of [[X - 3, Z - 3, X + 3, Z - 3], [X - 3, Z + 3, X + 3, Z + 3], [X - 3, Z - 3, X - 3, Z + 3], [X + 3, Z - 3, X + 3, Z + 3]])
    await run(`${O}fill ${x1} ${Y + 1} ${z1} ${x2} ${Y + 4} ${z2} minecraft:stone_bricks`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const W = (x, y, z) => `@e[type=minecraft:item_display,tag=bm.mtw,x=${x},y=${y},z=${z},distance=..0.3,limit=1]`;
  const Xs = (x, y, z) => `@e[type=minecraft:interaction,tag=bm.mtx,x=${x},y=${y - 0.45},z=${z},distance=..0.3,limit=1]`;
  const P = (x, y, z) => `@e[type=minecraft:block_display,tag=bm.mtp,x=${x},y=${y},z=${z},distance=..0.3]`;
  const loose = async (iid) => cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12,nbt={Item:{components:{"minecraft:custom_data":{bm:"${iid}"}}}}]`);
  const yawOf = async (sel) => num(`${O}data get entity ${sel} Rotation[0]`);
  // (each on a wall of its own: north, east, south, west, and two more along the north wall)
  const walls = [['cecil_staff', 180, [X + 0.5, Y + 2.5, Z - 2], 0, 'north', X + 0.5],
                 ['leo_trident', -90, [X + 3, Y + 2.5, Z + 0.5], 90, 'east', X + 0.5],
                 ['apo_mace', 0, [X + 0.5, Y + 2.5, Z + 3], 180, 'south', X + 0.5],
                 ['frisbee_shield', 90, [X - 2, Y + 2.5, Z + 0.5], -90, 'west', X + 0.5],
                 ['ray_gun', 180, [X - 1.5, Y + 2.5, Z - 2], 0, 'north (left)', X - 1.5],
                 ['sepulchre', 180, [X + 2.5, Y + 2.5, Z - 2], 0, 'north (right)', X + 2.5]];
  for (const [iid, lookYaw, [mx, my, mz], faceYaw, side, sx] of walls) {
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`);
    await run(`item modify entity TestRat hotbar.0 {type:"minecraft:set_name",target:"custom_name",name:{text:"Mine on the wall",color:"gold"}}`);
    ok(`[${iid}] its lore says how: "Sneak + drop (Q) facing a wall: hang it there."`, /Sneak \+ drop \(Q\) facing a wall/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components')));
    await at(sx, Y + 1, Z + 0.5, lookYaw, -2);
    A.bars.length = 0; await drop(A, 0, true); await sleep(300);
    ok(`[${iid}] sneak + drop at the ${side} wall: it hangs there`, (await cnt(W(mx, my, mz))) === 1 && (await cnt(Xs(mx, my, mz))) === 1, A.bars.slice(-1).join('').slice(0, 100));
    ok(`[${iid}] ...on a plaque, facing out from the wall`, (await cnt(P(mx, my, mz))) === 2 && Math.abs(((await yawOf(W(mx, my, mz))) - faceYaw + 540) % 360 - 180) < 1,
       `yaw ${await yawOf(W(mx, my, mz))}`);
    ok(`[${iid}] ...the very weapon (its name kept), nothing left lying about`, /Mine on the wall/.test(await nbt(W(mx, my, mz), 'item')) && (await has('TestRat', iid)) === 0 && (await loose(iid)) === 0);
  }
  ok("Leo's trident wears his own model (both forms)", /bm:leo_trident/.test(await nbt(W(X + 3, Y + 2.5, Z + 0.5), 'item.components')) &&
     /bm:leo_trident/.test(JSON.stringify(require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/loot_table/items/leo_spear.json', 'utf8'))));
  // (a drop without sneaking: just a drop; a sneak + drop at nothing: just a drop)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/shrink_ray');
  await at(X + 0.5, Y + 1, Z + 1.5, 0, -2);
  await drop(A, 0, false);
  ok('a plain drop facing a wall: it just drops', (await loose('shrink_ray')) === 1 && (await cnt(W(X + 0.5, Y + 2.5, Z + 3))) === 1);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/shrink_ray');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, -80);
  await drop(A, 0, true);
  ok('a sneak + drop looking at the floor (no wall): it just drops', (await loose('shrink_ray')) === 1);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  // (down again: Cecil's staff, sneak + punch)
  await at(X + 0.5, Y + 1, Z + 0.5, 180, -2);
  const cx = [X + 0.5, Y + 2.5, Z - 2];
  const box = await entOf(A, Xs(...cx)); A.input({ shift: true }); await sleep(250); if (box) A.attack(box.entityId); await sleep(800); A.input({}); await sleep(300);
  ok("sneak + punch Cecil's staff: it comes down into the inventory, name and all", await wait(2000, async () => (await has('TestRat', 'cecil_staff')) === 1) &&
     /Mine on the wall/.test(await run('data get entity TestRat Inventory')), `box ${box ? 'yes' : 'no'}`);
  ok('...and nothing is left on the wall', (await cnt(W(...cx))) === 0 && (await cnt(Xs(...cx))) === 0 && (await cnt(P(...cx))) === 0);
  await run(`${O}kill @e[tag=bm.mtw,x=${X},y=${Y},z=${Z},distance=..12]`); await run(`${O}kill @e[tag=bm.mtp,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}kill @e[tag=bm.mtx,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
