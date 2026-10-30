// 3.0b: THE PARTICLE TOGGLER (noparts.py) as a regular (non-op) player, every step a real packet. rcon sets the stage only: a
// floor, the Fence at his stall, the Token to pay with, a Smuggler's set and a Songbird handed over (as a trader would), the
// particle kinds learned once, a death.
//   buy     the Fence sells the Particle Toggler (1 Token): his window opened, the trade picked, the toggler taken out
//   gear    the Smuggler's set put on as a player (each piece right-clicked on), the Songbird swapped to the off hand (F):
//           the set's orbit (wax_off) and the songbird's notes reach the client round the bot; the set's Luck is on
//   menu    the toggler used: its menu (four switches, all ON); Armour pressed: a click, "Armour: particles OFF", the menu back
//           with Armour OFF - the set's orbit stops, the songbird's notes don't (another kind still shows), its Luck stays
//           (only the particles go); Everything pressed: the notes stop too; a death and a respawn: still off; Everything
//           again: both back; sneak + right-click: everything off without the menu, and again: on
//   node t327.js
const { bot, rcon, sleep } = require('./lib_resp');
const O = 'execute in minecraft:overworld run ';
const X = 21200, Y = 100, Z = 16800;
const TG = '{components:{"minecraft:custom_data":{bm:"particle_toggler"}}}';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const tags = async () => (await run('tag TestRat list'));
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const use = async () => { A.use(); await sleep(350); A.release(); await sleep(500); };
  const dd = d => d && (d.data || d);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (const t of ['bm.np_charm', 'bm.np_armor', 'bm.np_weap']) await run(`tag TestRat remove ${t}`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:saturation infinite 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`spawnpoint TestRat ${X} ${Y + 1} ${Z}`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- the particles that reach the client, by kind
  // (26.3 sends them raw: the particle's type (a varint) and its own data first, then two flags and x y z as doubles. Each
  //  kind's number is learned once - rcon shows one far over the bot's head - so nothing here depends on the registry's order.)
  const parts = []; A.on('world_particles', p => { const b = p.data && Buffer.from(p.data.data || p.data); if (b) parts.push({ t: Date.now(), b }); });
  const vint = (b) => { let v = 0, s = 0, i = 0; for (;;) { const x = b[i++]; v |= (x & 0x7f) << s; if (!(x & 0x80)) return v; s += 7; } };
  const learn = async (kind) => { const n0 = parts.length; await run(`${O}particle minecraft:${kind} ${X} ${Y + 7} ${Z} 0 0 0 0 1 force TestRat`);
    await wait(2000, async () => parts.length > n0, 50); return parts.length > n0 ? vint(parts[parts.length - 1].b) : -1; };
  const WAX = await learn('wax_off'), NOTE = await learn('note');
  ok('(the kinds learned: wax_off and note)', WAX >= 0 && NOTE >= 0 && WAX !== NOTE, `wax_off ${WAX}, note ${NOTE}`);
  const count = async (type, ms = 3000) => { const t0 = Date.now(); await sleep(ms); return parts.filter(e => e.t >= t0 && vint(e.b) === type).length; };

  // ---------------------------------------------------------------- the Fence sells it: a real trade
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z - 4.5} rotated 0 0 run function bm:npc/fence`); await sleep(1200);
  const FEN = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 0.5},y=${Y + 1},z=${Z - 4.5},distance=..2,limit=1]`;
  let idx = -1;
  for (let i = 0; i < 60 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(FEN, `Offers.Recipes[${i}].sell.count`))) break;
    if (/"particle_toggler"/.test(await nbt(FEN, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`))) idx = i; }
  ok('the Fence sells the Particle Toggler', idx >= 0, `trade #${idx}`);
  const price = idx < 0 ? 0 : +(((await nbt(FEN, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const buyId = idx < 0 ? '' : (await nbt(FEN, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  ok('...cheap, a convenience: 1 Token', buyId === 'token' && price === 1, `${price} ${buyId}`);
  for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
  await at(X + 0.5, Y + 1, Z - 2.5, 180, 0);
  const fen = await entOf(FEN); A.windows.length = 0; if (fen) A.interact(fen.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  ok('right-clicking the Fence opens his trades', !!w);
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok('...bought in his window: a toggler in the pack, the Token gone', (await has('particle_toggler')) === 1 && (await has(buyId)) === 0);
  const lore = await nbt('TestRat', `Inventory[${TG}].components."minecraft:lore"`);
  ok('...its lore says what it does', /particles your own gear/.test(lore) && /Sneak \+ right-click/.test(lore), lore.slice(0, 160));
  await run(`${O}kill ${FEN}`);
  // (the toggler into hotbar slot 8 for what follows)
  const slot = +(((await nbt('TestRat', `Inventory[${TG}].Slot`)).match(/(-?\d+)/) || [0, -1])[1]);
  if (slot !== 8 && slot >= 0) { const from = slot < 9 ? 'hotbar.' + slot : 'inventory.' + (slot - 9);
    await run(`item replace entity TestRat hotbar.8 from entity TestRat ${from}`); await run(`item replace entity TestRat ${from} with minecraft:air`); }

  // ---------------------------------------------------------------- gear on, as a player: the set's orbit and the songbird's notes
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const SET = ['smuggler_helmet', 'smuggler_chestplate', 'smuggler_leggings', 'smuggler_boots'];
  for (let i = 0; i < 4; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${SET[i]}`);
  await run('loot replace entity TestRat hotbar.4 loot bm:items/songbird');
  for (let i = 0; i < 4; i++) { A.slot(i); await sleep(250); await use(); }
  const worn = await run('execute ' + ['head', 'chest', 'legs', 'feet'].map(p => `if items entity TestRat armor.${p} *[minecraft:custom_data~{bm_set:"smuggler"}]`).join(' '));
  ok('the Smuggler\'s set put on, piece by piece (right-clicked)', /passed/i.test(worn), worn.slice(0, 80));
  A.slot(4); await sleep(250); A.swap(); await sleep(600);
  ok('...and the Songbird swapped into the off hand (F)', /songbird/.test(await nbt('TestRat', 'equipment.offhand')));
  A.slot(7); await sleep(300);
  let wx = await count(WAX), nt = await count(NOTE);
  ok('the set\'s orbit reaches the client (wax_off round the bot)', wx >= 5, `${wx} in 3 s`);
  ok('...and the songbird\'s notes', nt >= 2, `${nt} in 3 s`);

  // ---------------------------------------------------------------- the menu: Armour off
  A.slot(8); await sleep(300);
  let got = await A.useWait(2500);
  const d0 = dd(A.dialogN[A.dialogN.length - 1]);
  ok('the toggler used: its menu', got && /PARTICLE TOGGLER/.test(JSON.stringify(d0 && d0.title)));
  const labels = () => A.buttons().map(b => b.label).join(' | ');
  ok('...four switches, all ON', ['Charms', 'Armour', 'Weapons', 'Everything'].every(k => new RegExp(k + ': ON').test(labels())), labels());
  ok('...and the toggler kept (never used up)', await wait(1500, async () => (await has('particle_toggler')) === 1));
  A.bars.length = 0; const s0 = A.sounds.length;
  let pr = await A.press(/Armour/);
  ok('Armour pressed: the menu back, Armour OFF, the rest ON', pr && pr.next && /Armour: OFF/.test(labels()) && /Charms: ON/.test(labels()) && /Everything: SOME/.test(labels()), labels());
  ok('...a click, and the action bar says so', A.sounds.slice(s0).some(s => /ui\.button\.click/.test(s.name)) && A.bars.some(b => /Armour: particles OFF/.test(b)), A.bars.join(' / '));
  ok('...the setting is the player\'s own tag (bm.np_armor)', /bm\.np_armor/.test(await tags()) && !/bm\.np_charm/.test(await tags()));
  A.write('close_window', { windowId: 0 }); A.slot(7); await sleep(1200);
  wx = await count(WAX); nt = await count(NOTE);
  ok('the set\'s orbit stops', wx === 0, `${wx} in 3 s`);
  ok('...the songbird\'s notes (a charm) don\'t', nt >= 2, `${nt} in 3 s`);
  await run('effect clear TestRat minecraft:luck'); await sleep(1500);
  ok('...and the set still works: its Luck comes back (only the particles go)', /luck/.test(await nbt('TestRat', 'active_effects')));

  // ---------------------------------------------------------------- Everything off
  A.slot(8); await sleep(300); await A.useWait(2500); await sleep(300);
  A.bars.length = 0; pr = await A.press(/Everything/);
  ok('Everything pressed: every switch OFF', pr && pr.next && ['Charms', 'Armour', 'Weapons', 'Everything'].every(k => new RegExp(k + ': OFF').test(labels())), labels());
  ok('...the action bar says so', A.bars.some(b => /Everything: your gear's particles OFF/.test(b)), A.bars.join(' / '));
  A.write('close_window', { windowId: 0 }); A.slot(7); await sleep(1200);
  wx = await count(WAX); nt = await count(NOTE);
  ok('the notes stop too - nothing from your gear', wx === 0 && nt === 0, `wax ${wx}, notes ${nt}`);

  // ---------------------------------------------------------------- it lasts: a death and a respawn
  await run('effect clear TestRat'); await run('kill TestRat'); await sleep(3500);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const tl = await tags();
  ok('after a death and a respawn: still off', /bm\.np_charm/.test(tl) && /bm\.np_armor/.test(tl) && /bm\.np_weap/.test(tl), tl);
  await run('effect give TestRat minecraft:resistance infinite 4 true');
  // (death dropped what it carried: the gear back the same way, rcon setting the stage)
  await run('clear TestRat'); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`);
  for (let i = 0; i < 4; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${SET[i]}`);
  await run('loot replace entity TestRat hotbar.4 loot bm:items/songbird'); await run('loot replace entity TestRat hotbar.8 loot bm:items/particle_toggler');
  for (let i = 0; i < 4; i++) { A.slot(i); await sleep(250); await use(); }
  A.slot(4); await sleep(250); A.swap(); await sleep(600); A.slot(7); await sleep(1200);
  wx = await count(WAX); nt = await count(NOTE);
  ok('...the gear back on: still nothing', wx === 0 && nt === 0, `wax ${wx}, notes ${nt}`);

  // ---------------------------------------------------------------- Everything back on
  A.slot(8); await sleep(300); await A.useWait(2500); await sleep(300);
  pr = await A.press(/Everything/);
  ok('Everything pressed again: every switch ON', pr && pr.next && ['Charms', 'Armour', 'Weapons', 'Everything'].every(k => new RegExp(k + ': ON').test(labels())), labels());
  A.write('close_window', { windowId: 0 }); A.slot(7); await sleep(1200);
  wx = await count(WAX); nt = await count(NOTE);
  ok('...the orbit and the notes are back', wx >= 5 && nt >= 2, `wax ${wx}, notes ${nt}`);

  // ---------------------------------------------------------------- sneak + right-click: everything at once, no menu
  A.slot(8); await sleep(300); A.input({ shift: true }); await sleep(400);
  const n1 = A.dialogN.length; A.bars.length = 0; await use(); await sleep(400);
  ok('sneak + right-click: everything off, no menu', A.dialogN.length === n1 && /bm\.np_charm/.test(await tags()) && /bm\.np_armor/.test(await tags()) &&
     A.bars.some(b => /particles OFF/.test(b)), A.bars.join(' / '));
  await sleep(2400); A.bars.length = 0; await use(); await sleep(400); A.input({}); await sleep(300);
  ok('...and again: everything on', !/bm\.np_(charm|armor|weap)/.test(await tags()) && A.bars.some(b => /particles ON/.test(b)), A.bars.join(' / '));

  // ---------------------------------------------------------------- clean up
  for (const t of ['bm.np_charm', 'bm.np_armor', 'bm.np_weap']) await run(`tag TestRat remove ${t}`);
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
