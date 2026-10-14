const { bot, rcon, sleep } = require('./lib');
const X = 5500, Y = 100, Z = 5500;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[^\d]*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const blk = async (x, y, z, b) => (await run(`execute if block ${x} ${y} ${z} ${b}`)).includes('passed');
  const items = async (x, y, z) => run(`data get block ${x} ${y} ${z} Items`);
  const A = await bot('TestRat'); await sleep(1500);
  await run('time set noon'); await run('scoreboard players set #forced bm.bm 0'); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 600 4 true');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2500);
  await run(`fill ${X - 16} ${Y - 2} ${Z - 16} ${X + 16} ${Y} ${Z + 16} stone`); await run(`fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 12} ${Z + 16} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  // place: stand 2 south of the cell, look north and down at the floor under it
  const look = async (yw, pt) => { await run(`rotate TestRat ${yw} ${pt}`); A.pos.yaw = yw; A.pos.pitch = pt; await sleep(150); };
  const place = async (id, x, z, name) => {
    await run(`tp TestRat ${x + 0.5} ${Y + 1} ${z + 2.5} 180 42`); await look(180, 42);
    await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${id}`);
    if (name) await run(`item modify entity TestRat weapon.mainhand {type:"minecraft:set_name",name:"${name}",target:"custom_name"}`);
    await sleep(150); A.use(); await sleep(300); A.release(); await sleep(300);
    return cnt(`@e[type=marker,tag=bm.rs_${id},x=${x + 0.5},y=${Y + 1.5},z=${z + 0.5},distance=..0.3]`);
  };
  const drop = (x, y, z, id, n = 1) => run(`summon item ${x} ${y} ${z} {Item:{id:"${id}",count:${n}},PickupDelay:40}`);
  // ---- FILTER HOPPER
  const FX = X - 10, FZ = Z - 10;
  ok('filter hopper placed (pointing down)', (await place('filter_hopper', FX, FZ)) === 1 && await blk(FX, Y + 1, FZ, 'hopper[facing=down]'));
  ok('...and named in its window', (await run(`data get block ${FX} ${Y + 1} ${FZ} CustomName`)).includes('Filter Hopper'));
  await run(`setblock ${FX} ${Y} ${FZ} chest`);                                 // output under it
  await run(`summon glow_item_frame ${FX - 1} ${Y + 1} ${FZ} {Facing:4b,Item:{id:"minecraft:diamond",count:1}}`); await sleep(1300);
  ok('reads the frame on its side', (await run(`data get entity @e[type=marker,tag=bm.rs_filter_hopper,limit=1] data.f`)).includes('diamond'));
  await run(`tp TestRat ${X} ${Y + 1} ${Z}`);
  await drop(FX + 0.5, Y + 2.2, FZ + 0.5, 'minecraft:dirt', 3); await sleep(2500);
  ok('loose dirt above: not taken', (await cnt(`@e[type=item,x=${FX + 0.5},y=${Y + 2},z=${FZ + 0.5},distance=..1.5]`)) === 1 && !(await items(FX, Y, FZ)).includes('dirt'));
  await run(`kill @e[type=item,x=${FX + 0.5},y=${Y + 2},z=${FZ + 0.5},distance=..2]`);
  await drop(FX + 0.5, Y + 2.2, FZ + 0.5, 'minecraft:diamond', 3); await sleep(2500);
  ok('loose diamonds above: taken and passed down', (await items(FX, Y, FZ)).includes('diamond'), (await items(FX, Y, FZ)).slice(-60));
  // a line above it: a chest whose first item is dirt, then diamonds
  await run(`setblock ${FX} ${Y + 2} ${FZ} chest`); await run(`data modify block ${FX} ${Y + 2} ${FZ} Items set value [{Slot:0b,id:"minecraft:diamond",count:2},{Slot:1b,id:"minecraft:dirt",count:5},{Slot:2b,id:"minecraft:diamond",count:4}]`);
  await sleep(3000);
  const src = await items(FX, Y + 2, FZ), below = await items(FX, Y, FZ);
  ok('from a chest: takes the diamonds at the front, stops at the dirt', src.includes('dirt') && !/diamond", count: 2/.test(src) && !(await items(FX, Y + 1, FZ)).includes('dirt') && !below.includes('dirt'), src.slice(-130));
  // ---- breaking gives the machine back, not a plain hopper
  await run(`setblock ${FX} ${Y + 2} ${FZ} air`); await run(`setblock ${FX} ${Y + 1} ${FZ} air destroy`); await sleep(600);
  ok('broken: drops the Filter Hopper item (no plain hopper)', (await cnt(`@e[type=item,x=${FX + 0.5},y=${Y + 1.5},z=${FZ + 0.5},distance=..2,nbt={Item:{components:{"minecraft:custom_data":{bm:"filter_hopper"}}}}]`)) === 1 &&
     !(await cnt(`@e[type=item,x=${FX + 0.5},y=${Y + 1.5},z=${FZ + 0.5},distance=..2,nbt={Item:{id:"minecraft:hopper"}}]`)) && !(await cnt('@e[type=marker,tag=bm.rs_filter_hopper]')));
  // ---- VACUUM HOPPER
  const VX = X - 4, VZ = Z - 10;
  ok('vacuum hopper placed', (await place('vacuum_hopper', VX, VZ)) === 1);
  await run(`tp TestRat ${X} ${Y + 1} ${Z}`);
  await drop(VX + 5.5, Y + 1.2, VZ + 0.5, 'minecraft:iron_ingot', 5); await drop(VX - 3.5, Y + 1.2, VZ + 4.5, 'minecraft:gold_ingot', 2); await sleep(3500);
  const vi = await items(VX, Y + 1, VZ);
  ok('vacuum: pulls loose items within 8 blocks into itself', vi.includes('iron_ingot') && vi.includes('gold_ingot'), vi.slice(-90));
  await run(`setblock ${VX + 1} ${Y + 1} ${VZ} redstone_block`); await sleep(300);
  await drop(VX + 5.5, Y + 1.2, VZ + 0.5, 'minecraft:emerald', 1); await sleep(2500);
  ok('vacuum: off while redstone locks it', (await cnt(`@e[type=item,x=${VX + 5.5},y=${Y + 1},z=${VZ + 0.5},distance=..1.5]`)) === 1);
  await run(`setblock ${VX + 1} ${Y + 1} ${VZ} air`);
  // ---- ITEM COMPACTOR
  const CX = X + 12, CZ = Z - 12;
  ok('item compactor placed', (await place('item_compactor', CX, CZ)) === 1 && await blk(CX, Y + 1, CZ, 'waxed_copper_grate'));
  await run(`tp TestRat ${X} ${Y + 1} ${Z + 12}`);
  for (const [dx, dz] of [[3, 0], [-3, 2], [3, -3], [0, 3], [-4, -3], [-6, 1]]) await drop(CX + 0.5 + dx, Y + 1.2, CZ + 0.5 + dz, 'minecraft:cobblestone', 1);
  for (let i = 0; i < 4; i++) await run(`summon experience_orb ${CX - 4} ${Y + 1.2} ${CZ + i} {Value:3}`);
  const before = await cnt(`@e[type=#bm:p49_loose,x=${CX},y=${Y},z=${CZ},distance=..14]`); await sleep(7500);
  const after = await cnt(`@e[type=#bm:p49_loose,x=${CX},y=${Y},z=${CZ},distance=..14]`);
  const stack = await num(`data get entity @e[type=item,x=${CX + 0.5},y=${Y + 2},z=${CZ + 0.5},distance=..1,limit=1] Item.count`);
  const orbs = await cnt(`@e[type=experience_orb,x=${CX + 0.5},y=${Y + 2},z=${CZ + 0.5},distance=..1.5]`), stray = await cnt(`@e[type=#bm:p49_loose,x=${CX + 0.5},y=${Y + 2},z=${CZ + 0.5},distance=1.5..14]`);
  ok('compactor: 6 drops merged into one stack, XP gathered with it', stack === 6 && orbs >= 1 && stray === 0, `${before} entities -> ${after}; stack of ${stack}; orbs on it ${orbs}; stray ${stray}`);
  // ---- WIRELESS
  const TX = X - 10, TZ = Z, RXX = X + 10, RXZ = Z + 6;
  ok('transmitter placed (redstone lamp)', (await place('wireless_transmitter', TX, TZ)) === 1 && await blk(TX, Y + 1, TZ, 'redstone_lamp'));
  ok('receiver placed (copper)', (await place('wireless_receiver', RXX, RXZ)) === 1);
  ok('named receiver placed', (await place('wireless_receiver', RXX - 4, RXZ, 'Gate')) === 1);
  await run(`tp TestRat ${X} ${Y + 1} ${Z}`); await run(`setblock ${RXX} ${Y + 2} ${RXZ} redstone_lamp`); await sleep(1500);
  await run(`setblock ${TX} ${Y + 1} ${TZ - 1} redstone_block`); await sleep(500);
  ok('power the transmitter: the receiver on its channel turns on, 20 blocks away', await blk(RXX, Y + 1, RXZ, 'redstone_block'));
  ok('...the one on another channel stays off', await blk(RXX - 4, Y + 1, RXZ, 'waxed_chiseled_copper'));
  ok('...and its redstone lights a lamp on top', await blk(RXX, Y + 2, RXZ, 'redstone_lamp[lit=true]'));
  await run(`setblock ${TX} ${Y + 1} ${TZ - 1} air`); await sleep(800);
  ok('unpower: the receiver turns off', await blk(RXX, Y + 1, RXZ, 'waxed_chiseled_copper'));
  // ---- REDSTONE CLOCK (+ wrench)
  const KX = X - 4, KZ = Z + 6;
  ok('clock placed', (await place('redstone_clock', KX, KZ)) === 1);
  await run(`tp TestRat ${X} ${Y + 1} ${Z}`);
  let edges = 0, last = false;
  for (let i = 0; i < 70; i++) { const on = await blk(KX, Y + 1, KZ, 'redstone_block'); if (on && !last) edges++; last = on; await sleep(45); }
  ok('clock: about one pulse a second', edges >= 2 && edges <= 5, edges + ' pulses in ~3.2 s');
  await run(`tp TestRat ${KX + 0.5} ${Y + 1} ${KZ + 2.5} 180 39`); await look(180, 39);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/tinker_wrench'); await sleep(150);
  A.use(); await sleep(250); A.release(); await sleep(250); A.use(); await sleep(250); A.release(); await sleep(250);
  const per = await num('scoreboard players get @e[type=marker,tag=bm.rs_redstone_clock,limit=1] bm.rsp');
  ok('wrench: right-click twice sets 3 s', per === 3, `${per} s; bar: ${A.bars.slice(-1)[0]}`);
  A.input({ shift: true }); await sleep(200); A.use(); await sleep(250); A.release(); A.input({}); await sleep(300);
  ok('wrench: sneak + right-click takes a second off', (await num('scoreboard players get @e[type=marker,tag=bm.rs_redstone_clock,limit=1] bm.rsp')) === 2);
  // ---- BLOCK BREAKER
  const BX = X + 4, BZ = Z + 6;
  ok('breaker placed (dispenser facing you, locked)', (await place('block_breaker', BX, BZ)) === 1 && await blk(BX, Y + 1, BZ, 'dispenser[facing=south]'));
  await run(`tp TestRat ${X} ${Y + 1} ${Z - 6}`);
  await run(`setblock ${BX} ${Y + 1} ${BZ + 1} oak_log`); await run(`setblock ${BX + 1} ${Y + 1} ${BZ} redstone_block`); await sleep(500);
  ok('powered: breaks the log in front, which drops', await blk(BX, Y + 1, BZ + 1, 'air') && (await cnt(`@e[type=item,x=${BX + 0.5},y=${Y + 1},z=${BZ + 1.5},distance=..2,nbt={Item:{id:"minecraft:oak_log"}}]`)) === 1);
  await run(`setblock ${BX + 1} ${Y + 1} ${BZ} air`); await run(`setblock ${BX} ${Y + 1} ${BZ + 1} bedrock`); await sleep(300); await run(`setblock ${BX + 1} ${Y + 1} ${BZ} redstone_block`); await sleep(500);
  ok('...but never bedrock', await blk(BX, Y + 1, BZ + 1, 'bedrock'));
  await run(`setblock ${BX + 1} ${Y + 1} ${BZ} air`); await run(`setblock ${BX} ${Y + 1} ${BZ + 1} air`);
  // ---- BLOCK PLACER
  const PX = X + 10, PZ = Z - 4;
  ok('placer placed (dropper)', (await place('block_placer', PX, PZ)) === 1 && await blk(PX, Y + 1, PZ, 'dropper[facing=south]'));
  await run(`tp TestRat ${X} ${Y + 1} ${Z - 6}`);
  await run(`data modify block ${PX} ${Y + 1} ${PZ} Items set value [{Slot:4b,id:"minecraft:bricks",count:2}]`);
  await run(`setblock ${PX + 1} ${Y + 1} ${PZ} redstone_block`); await sleep(800);
  ok('powered: places the block instead of throwing it', await blk(PX, Y + 1, PZ + 1, 'bricks') && !(await cnt(`@e[type=item,x=${PX + 0.5},y=${Y + 1},z=${PZ + 1.5},distance=..2]`)) && (await items(PX, Y + 1, PZ)).includes('count: 1'));
  await run(`setblock ${PX + 1} ${Y + 1} ${PZ} air`); await run(`setblock ${PX} ${Y + 1} ${PZ + 1} air`); await sleep(300);
  await run(`data modify block ${PX} ${Y + 1} ${PZ} Items set value [{Slot:0b,id:"minecraft:apple",count:1}]`);
  await run(`setblock ${PX + 1} ${Y + 1} ${PZ} redstone_block`); await sleep(800);
  ok('non-blocks are dropped as usual', (await cnt(`@e[type=item,x=${PX + 0.5},y=${Y + 1},z=${PZ + 1.5},distance=..6,nbt={Item:{id:"minecraft:apple"}}]`)) === 1);
  await run(`setblock ${PX + 1} ${Y + 1} ${PZ} air`);
  // ---- SORTING CHEST
  const SX = X, SZ = Z + 10;
  ok('sorting chest placed (single, facing you)', (await place('sorting_chest', SX, SZ)) === 1 && await blk(SX, Y + 1, SZ, 'chest[type=single,facing=south]'));
  await run(`data modify block ${SX} ${Y + 1} ${SZ} Items set value [{Slot:0b,id:"minecraft:stone",count:20},{Slot:3b,id:"minecraft:dirt",count:10},{Slot:5b,id:"minecraft:dirt",count:60},{Slot:7b,id:"minecraft:ender_pearl",count:10},{Slot:8b,id:"minecraft:ender_pearl",count:10},{Slot:9b,id:"minecraft:diamond_sword",count:1},{Slot:12b,id:"minecraft:apple",count:3}]`);
  A.useOn(SX, Y + 1, SZ, 3); await sleep(800);
  const si = await items(SX, Y + 1, SZ);
  const order = [...si.matchAll(/count: (\d+), Slot: (\d+)b, id: "minecraft:(\w+)"|Slot: (\d+)b, id: "minecraft:(\w+)", count: (\d+)|id: "minecraft:(\w+)", count: (\d+), Slot: (\d+)b/g)].map(m => m[0].match(/minecraft:(\w+)/)[1] + ':' + m[0].match(/count: (\d+)/)[1]);
  ok('opened: merged and sorted A to Z', order.join(' ') === 'apple:3 diamond_sword:1 dirt:64 dirt:6 ender_pearl:16 ender_pearl:4 stone:20', order.join(' '));
  for (const w of A.windows) A.close(w.windowId);
  // ---- LAG LENS
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/lag_lens'); const nc = A.chats.length; await sleep(150);
  A.use(); await sleep(250); A.release(); await sleep(500);
  const lens = A.chats.slice(nc).join(' | ');
  ok('lag lens: a 3x3 chunk report', /Lag Lens/.test(lens) && (lens.match(/\[/g) || []).length >= 9, lens.slice(0, 220));
  // ---- not inside the Market's wards
  const mk = await run('data get entity @e[type=marker,tag=bm.mkt,limit=1] Pos');
  console.log('  (market marker:', mk.slice(-50), ')');
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });
