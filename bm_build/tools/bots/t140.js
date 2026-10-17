// 2.77c: weapons on the wall, as a regular (non-op) player: Tullius's blunderbuss and harpoon, Democratus' scythe and both of
// KillerWatt's tendril sets, each hung on a wall with a sneak + use (the very weapon, its name kept, on a little wooden plaque,
// facing out from the wall it hangs on - all four walls), taken down again with a sneak + punch. The blunderbuss with a monster
// close fires instead; the scythe used without sneaking says how; the tendrils' plain use still puts them on (swapping with
// the chestplate on). A broken wall drops the weapon - never lost. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)(?:[dfbsL])?\s*$/) || [0, NaN])[1]);
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  const X = 16200, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  // (a room: walls 3 blocks out on every side, 4 high)
  for (const [x1, z1, x2, z2] of [[X - 3, Z - 3, X + 3, Z - 3], [X - 3, Z + 3, X + 3, Z + 3], [X - 3, Z - 3, X - 3, Z + 3], [X + 3, Z - 3, X + 3, Z + 3]])
    await run(`${O}fill ${x1} ${Y + 1} ${z1} ${x2} ${Y + 4} ${z2} minecraft:stone_bricks`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const W = (x, y, z) => `@e[type=minecraft:item_display,tag=bm.mtw,x=${x},y=${y},z=${z},distance=..0.3,limit=1]`;
  const Xs = (x, y, z) => `@e[type=minecraft:interaction,tag=bm.mtx,x=${x},y=${y - 0.45},z=${z},distance=..0.3,limit=1]`;
  const P = (x, y, z) => `@e[type=minecraft:block_display,tag=bm.mtp,x=${x},y=${y},z=${z},distance=..0.3]`;
  const yawOf = async (sel) => num(`${O}data get entity ${sel} Rotation[0]`);
  const take = async (C, sel) => { const box = await entOf(C, sel); C.input({ shift: true }); await sleep(250); if (box) C.attack(box.entityId); await sleep(800); C.input({}); await sleep(300); return !!box; };

  // ---------------------------------------------------------------- each weapon on its own wall (north, east, south, west, and north again)
  // (looking north at the north wall's face: the face is z = Z - 2, the mount sits on it at y + 0.5 of the block looked at)
  // (looking north you see the north wall's south face, and the weapon faces back out, south - and so on round)
  const walls = [['tul_blunderbuss', 180, [X + 0.5, Y + 2.5, Z - 2], 0, 'north'],
                 ['tul_harpoon', -90, [X + 3, Y + 2.5, Z + 0.5], 90, 'east'],
                 ['demo_scythe', 0, [X + 0.5, Y + 2.5, Z + 3], 180, 'south'],
                 ['killerwatt_tendrils', 90, [X - 2, Y + 2.5, Z + 0.5], -90, 'west'],
                 ['ethereal_tendrils', 180, [X - 0.5, Y + 2.5, Z - 2], 0, 'north again']];
  // (the look: from the room's middle, eyes at Y + 2.62, at the block one up on that wall - a little up: pitch about -2)
  for (const [iid, lookYaw, [mx, my, mz], faceYaw, side] of walls) {
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`);
    await run(`item modify entity TestRat hotbar.0 {type:"minecraft:set_name",target:"custom_name",name:{text:"Mine on the wall",color:"gold"}}`);
    ok(`[${iid}] its lore says how: "Sneak + use on a wall: hang it there."`, /Sneak \+ use on a wall: hang it there/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components')));
    const sx = iid === 'ethereal_tendrils' ? X - 0.5 : X + 0.5;
    await at(sx, Y + 1, Z + 0.5, lookYaw, -2);
    A.bars.length = 0; await use(A, 0, true); await sleep(300);
    ok(`[${iid}] sneak + use at the ${side} wall: it hangs there`, (await cnt(W(mx, my, mz))) === 1 && (await cnt(Xs(mx, my, mz))) === 1, A.bars.slice(-1).join('').slice(0, 100));
    ok(`[${iid}] ...on a plaque (two boards), facing out from the wall`, (await cnt(P(mx, my, mz))) === 2 && Math.abs(((await yawOf(W(mx, my, mz))) - faceYaw + 540) % 360 - 180) < 1,
       `yaw ${await yawOf(W(mx, my, mz))}`);
    const lit = await run(`execute as ${W(mx, my, mz)} at @s if block ~ ~ ~ minecraft:air`), plit = await run(`execute as ${P(mx, my, mz).replace(']', ',limit=1]')} at @s if block ~ ~ ~ minecraft:air`);
    ok(`[${iid}] (2.82) ...weapon and plaque stand in the room's air, not in the wall (lit by the room, not black)`, /passed/i.test(lit) && /passed/i.test(plit), `${lit} | ${plit}`);
    ok(`[${iid}] ...the very weapon (its name kept), out of the hand`, /Mine on the wall/.test(await nbt(W(mx, my, mz), 'item')) && (await has('TestRat', iid)) === 0);
    ok(`[${iid}] ..."It hangs on the wall. (Sneak + punch it to take it down.)"`, /Sneak \+ punch it to take it down/.test(A.bars.join(' ')));
  }
  // (take one down: the harpoon, from the east wall)
  await at(X + 0.5, Y + 1, Z + 0.5, -90, -2);
  const hx = [X + 3, Y + 2.5, Z + 0.5];
  const hit = await take(A, Xs(...hx));
  ok('sneak + punch the harpoon: it comes down into the inventory, name and all', await wait(2000, async () => (await has('TestRat', 'tul_harpoon')) === 1) &&
     /Mine on the wall/.test(await run('data get entity TestRat Inventory')), `box ${hit ? 'yes' : 'no'}`);
  ok('...and nothing is left on the wall', (await cnt(W(...hx))) === 0 && (await cnt(Xs(...hx))) === 0 && (await cnt(P(...hx))) === 0);
  // (a plain punch does nothing: only sneak + punch takes it down)
  const bx = [X + 0.5, Y + 2.5, Z - 2];
  await at(X + 0.5, Y + 1, Z + 0.5, 180, -2);
  let box = await entOf(A, Xs(...bx)); if (box) A.attack(box.entityId); await sleep(800);
  ok('a plain punch at the blunderbuss: it stays up', (await cnt(W(...bx))) === 1 && (await has('TestRat', 'tul_blunderbuss')) === 0);
  // (its wall broken: the scythe drops - never lost)
  const scx = [X + 0.5, Y + 2.5, Z + 3];
  await run(`${O}setblock ${X} ${Y + 2} ${Z + 3} minecraft:air`);
  ok('the scythe\'s wall broken: it drops as an item, plaque and all gone', await wait(2500, async () => (await cnt(W(...scx))) === 0 && (await cnt(P(...scx))) === 0 &&
     /passed/i.test(await run(`${O}execute if entity @e[type=minecraft:item,x=${scx[0]},y=${scx[1]},z=${scx[2]},distance=..2,nbt={Item:{components:{"minecraft:custom_data":{bm:"demo_scythe"}}}}]`))));
  await run(`${O}setblock ${X} ${Y + 2} ${Z + 3} minecraft:stone_bricks`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);

  // ---------------------------------------------------------------- uses that aren't a hanging
  // (the blunderbuss with a monster close: it fires - it doesn't hang)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/tul_blunderbuss'); await run('scoreboard players set TestRat bm.tugc 0');
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z - 1.5} {NoAI:1b,Tags:["bm.t140"],PersistenceRequired:1b,Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}`);
  await at(X + 1.5, Y + 1, Z + 0.5, 180, -2);
  await use(A, 0, true); await sleep(300);
  ok('a monster close: sneak + use at the wall fires the blunderbuss instead (reloading, the gun still in hand, no new mount)',
     (await sc('TestRat', 'bm.tugc')) > 0 && (await has('TestRat', 'tul_blunderbuss')) === 1 && (await cnt(W(X + 1.5, Y + 2.5, Z - 2))) === 0,
     `reload ${await sc('TestRat', 'bm.tugc')}`);
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t140]`);
  // (the scythe without sneaking: it says how)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/demo_scythe');
  A.bars.length = 0; await use(A, 0, false);
  ok('the scythe used without sneaking: "Sneak + use on a wall: hang it there."', /Sneak \+ use on a wall/.test(A.bars.join(' ')) && (await has('TestRat', 'demo_scythe')) === 1);
  // (the scythe, sneaking, looking at the floor: no wall - it says so)
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 80); A.bars.length = 0; await use(A, 0, true);
  ok('...sneak + use at the floor: "Look at a wall within 3 blocks..."', /Look at a wall/.test(A.bars.join(' ')) && (await has('TestRat', 'demo_scythe')) === 1);
  // (the tendrils' plain use: on they go, the chestplate that was on to the hand)
  await run('clear TestRat'); await run('item replace entity TestRat armor.chest with minecraft:iron_chestplate'); await run('loot replace entity TestRat hotbar.0 loot bm:items/killerwatt_tendrils');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0); await use(A, 0, false);
  ok('the tendrils used (not sneaking): worn - and the iron chestplate comes to the hand', /killerwatt_tendrils/.test(await run('data get entity TestRat equipment.chest')) &&
     /iron_chestplate/.test(await run('data get entity TestRat Inventory[{Slot:0b}]')));
  // (and sneaking, but at no wall: still worn - the old way)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ethereal_tendrils'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 80);
  await use(A, 0, true);
  ok('...sneak + use at no wall: worn all the same', /ethereal_tendrils/.test(await run('data get entity TestRat equipment.chest')));
  await run('clear TestRat');

  // ---------------------------------------------------------------- the rest come down too
  for (const [iid, lookYaw, mpos, , side] of walls.filter(w => !['tul_harpoon', 'demo_scythe'].includes(w[0]))) {
    const sx = iid === 'ethereal_tendrils' ? X - 0.5 : X + 0.5;
    await at(sx, Y + 1, Z + 0.5, lookYaw, -2);
    await take(A, Xs(...mpos));
    ok(`[${iid}] taken down from the ${side} wall`, await wait(2000, async () => (await has('TestRat', iid)) === 1) && (await cnt(W(...mpos))) === 0);
  }
  ok('the room is clean: no plaques, no weapons, no boxes left', (await cnt(`@e[type=minecraft:block_display,tag=bm.mtp]`)) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.mtw]')) === 0 &&
     (await cnt('@e[type=minecraft:interaction,tag=bm.mtx]')) === 0);
  await run('clear TestRat'); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
