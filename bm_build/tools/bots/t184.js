// 2.80d: A SMUGGLER'S JAR IN A DISPLAY CASE - as a regular (non-op) player, every step a real packet (rcon sets the stage: a
// floor, a wall, the cases and the jars): a jarred pig right-clicked into a floor case - on the cushion, facing out of the
// case, its head with its body; small enough that the circle it sweeps as it turns stays inside the glass; sneak + right-click
// - it turns, and its head turns with it (the head-turn packets the client gets follow the body round); again - it stops; taken
// back out. A jarred wolf the same size rule; then a pig in a wall case - side-on, small enough for the shallow case, and
// sneak + right-click doesn't set it turning there (it would poke through the glass).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (sel, path) => +(((await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?data: /, '').match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(400); };
  const jar = (eid) => `minecraft:totem_of_undying[minecraft:custom_data={bm:"smuggler_jar",bmv:33,jar:{eid:"minecraft:${eid}",name:"${eid}",data:{}}}]`;
  const angle = (a) => ((a % 360) + 540) % 360 - 180;                     // (-180..180)
  const X = 16760, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  // (the head-turn packets the client is sent, per entity)
  const heads = {}; A.on('entity_head_rotation', (p) => { (heads[p.entityId] = heads[p.entityId] || []).push(p.headYaw * 360 / 256); });
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await sleep(1200);

  // ---------------------------------------------------------------- a floor case, a pig
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  ok('a floor case set down', (await cnt(caseSel)) === 1);
  const PIG = `@e[type=minecraft:pig,tag=bm.dcmob,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  await run(`item replace entity TestRat hotbar.0 with ${jar('pig')}`);
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(1000);
  ok('the jarred pig right-clicked into it: on the cushion', (await cnt(PIG)) === 1);
  const sc = await num(PIG, 'attributes[{id:"minecraft:scale"}].base');
  // (a pig's model is about 1.15 long and 0.9 wide: turning, it sweeps a circle 0.5 * hypot(1.15, 0.9) * scale across - the glass is 0.33 from the middle)
  const r = 0.5 * Math.hypot(1.15, 0.9) * sc;
  ok('...small enough to turn inside the glass (the circle it sweeps within 0.33 of the middle)', sc > 0.3 && r <= 0.335, `scale ${sc}, radius ${r.toFixed(3)}`);
  const cy = await num(`@e[type=minecraft:item_display,tag=bm.dcase,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`, 'Rotation[0]');
  const py = await num(PIG, 'Rotation[0]');
  ok('...facing out of the case', Math.abs(angle(py - cy)) < 1, `pig ${py}, case ${cy}`);
  const pe = await entOf(PIG);
  await sleep(800);
  const h0 = pe && heads[pe.entityId] ? heads[pe.entityId].slice(-1)[0] : null;
  ok('...its head facing the same way as its body', pe != null && (h0 == null ? true : Math.abs(angle(h0 - py)) < 3), `head ${h0}, body ${py}`);

  // ---------------------------------------------------------------- sneak + right-click: it turns - head and all
  if (pe) heads[pe.entityId] = [];
  A.slot(8); await sleep(200); A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId, true); await sleep(300); A.input({}); await sleep(200);
  const ys = []; for (let i = 0; i < 8; i++) { ys.push(await num(PIG, 'Rotation[0]')); await sleep(250); }
  ok('sneak + right-click: it turns', new Set(ys.map(v => Math.round(v))).size >= 4, ys.map(v => v.toFixed(0)).join(' '));
  const hs = pe ? (heads[pe.entityId] || []) : [];
  ok('...and its head turns with it (the head-turn packets follow it round)', new Set(hs.map(v => Math.round(v))).size >= 4, `${hs.length} head turns`);
  const yb = await num(PIG, 'Rotation[0]'); await sleep(120); const hl = hs.slice(-1)[0];
  ok('...never twisted on its neck: its head points where its body does', hl != null && Math.abs(angle(hl - yb)) < 20, `head ${hl}, body ${yb}`);
  await sleep(1300); A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId, true); await sleep(300); A.input({}); await sleep(400);
  const s0 = await num(PIG, 'Rotation[0]'); await sleep(600); const s1 = await num(PIG, 'Rotation[0]');
  ok('again: it stops', Math.abs(s1 - s0) < 0.01, `${s0} -> ${s1}`);
  await sleep(1200); box = await entOf(caseSel); A.slot(8); await sleep(200); if (box) A.interact(box.entityId); await sleep(800);
  ok('empty-handed: the pig back in its jar', (await cnt(PIG)) === 0 && /"pig"/.test(await run('data get entity TestRat Inventory')));
  await run('clear TestRat *[minecraft:custom_data~{bm:"smuggler_jar"}]');

  // ---------------------------------------------------------------- a wolf in the floor case (long, as pigs are)
  const WOLF = PIG.replace('minecraft:pig', 'minecraft:wolf');
  await run(`item replace entity TestRat hotbar.0 with ${jar('wolf')}`); await sleep(1200);
  box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(1000);
  const ws = await num(WOLF, 'attributes[{id:"minecraft:scale"}].base');
  ok('a jarred wolf: small enough to turn inside the glass too', (await cnt(WOLF)) === 1 && 0.5 * Math.hypot(1.25, 0.6) * ws <= 0.335, `scale ${ws}`);
  await sleep(1200); box = await entOf(caseSel); A.slot(8); await sleep(200); if (box) A.interact(box.entityId); await sleep(800);
  await run('clear TestRat *[minecraft:custom_data~{bm:"smuggler_jar"}]');
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..10]`);

  // ---------------------------------------------------------------- a wall case: side-on, still
  await run(`${O}fill ${X - 3} ${Y + 1} ${Z + 4} ${X + 3} ${Y + 4} ${Z + 4} minecraft:stone`);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -5);                                // (looking at the wall)
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_gilded'); await use(5);
  const wcase = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 2},z=${Z + 3.5},distance=..1.5,limit=1]`;
  const wok = (await cnt(wcase)) === 1 && /0\.6f/.test(await run(`${O}data get entity ${wcase} width`));
  ok('a wall case hung on the wall', wok, await run(`${O}data get entity ${wcase} width`));
  const WPIG = `@e[type=minecraft:pig,tag=bm.dcmob,x=${X + 0.5},y=${Y + 2},z=${Z + 3.5},distance=..1.5,limit=1]`;
  await run(`item replace entity TestRat hotbar.0 with ${jar('pig')}`); await sleep(400);
  box = await entOf(wcase); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(1000);
  const wsc = await num(WPIG, 'attributes[{id:"minecraft:scale"}].base');
  const wy = await num(WPIG, 'Rotation[0]'), wc = await num(`@e[type=minecraft:item_display,tag=bm.dcase,x=${X + 0.5},y=${Y + 2},z=${Z + 3.5},distance=..1.5,limit=1]`, 'Rotation[0]');
  ok('the jarred pig in the wall case: side-on (its length along the wall)', (await cnt(WPIG)) === 1 && Math.abs(Math.abs(angle(wy - wc)) - 90) < 1, `pig ${wy}, case ${wc}`);
  ok('...small enough for the shallow case (1.15 long in 0.46, 0.9 wide in 0.28)', 1.15 * wsc <= 0.465 && 0.9 * wsc <= 0.285, `scale ${wsc}`);
  await sleep(1200); A.slot(8); await sleep(200); A.input({ shift: true }); await sleep(250); box = await entOf(wcase); if (box) A.interact(box.entityId, true); await sleep(300); A.input({}); await sleep(400);
  const t0 = await num(WPIG, 'Rotation[0]'); await sleep(700); const t1 = await num(WPIG, 'Rotation[0]');
  ok('...sneak + right-click: it stays still (it would poke through the glass)', Math.abs(t1 - t0) < 0.01, `${t0} -> ${t1}`);
  await sleep(1200); box = await entOf(wcase); A.slot(8); await sleep(200); if (box) A.interact(box.entityId); await sleep(800);

  // ---------------------------------------------------------------- clean up
  await run('clear TestRat'); await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
