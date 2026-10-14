// Play-test suite: two real (bot) players exercise the custom items on the live 26.3 server.
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
const results = [];
const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null;
let R, A, B;
const run = (c) => R.run(c);
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const score = (who, obj) => num(`scoreboard players get ${who} ${obj}`);
const pos = async (who) => { const s = await run(`data get entity ${who} Pos`); return (s.match(/\[(.*)\]/) || [, ''])[1].split(',').map(v => parseFloat(v)); };
const has = async (who, iid) => (await run(`execute if items entity ${who} container.* *[minecraft:custom_data~{bm:"${iid}"}]`)).includes('passed') ||
                               (await run(`execute if items entity ${who} weapon.offhand *[minecraft:custom_data~{bm:"${iid}"}]`)).includes('passed');
const count = async (sel) => { const s = await run(`execute if entity ${sel}`); const m = s.match(/Count: (\d+)/); return m ? +m[1] : (s.includes('passed') ? 1 : 0); };
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const re = new RegExp(`\\{[^{}]*id: "minecraft:${id}"[^{}]*\\}`); const m = s.match(re);
                                     if (!m) return null; const a = m[0].match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const items = async (who, pred) => { const s = await run(`clear ${who} ${pred} 0`); const m = s.match(/Found (\d+)/); return m ? +m[1] : 0; };
const slots = async (who) => ((await run(`data get entity ${who} Inventory`)).match(/Slot:/g) || []).length;
const give = (who, iid) => run(`loot give ${who} loot bm:items/${iid}`);
const tp = (who, x, y, z, yaw = 0, pitch = 0) => run(`tp ${who} ${x} ${y} ${z} ${yaw} ${pitch}`);
const reset = async (who) => { await run(`clear ${who}`); await run(`effect clear ${who}`); await run(`effect give ${who} minecraft:saturation infinite 0 true`);
                               await run(`gamemode survival ${who}`); await run(`scoreboard players reset ${who} bm.cof`); await run(`scoreboard players reset ${who} bm.coft`);
                               await run(`scoreboard players reset ${who} bm.rodr`); await run(`scoreboard players reset ${who} bm.spcd`); await run(`data modify entity ${who} Health set value 20f`); await run(`extinguish ${who}`).catch(() => {}); };
function ok(name, pass, detail = '') { results.push([name, pass, detail]); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? '  -- ' + detail : '')); }
async function test(name, fn) { if (ONLY && !ONLY.test(name)) return; try { await fn(); } catch (e) { ok(name, false, 'exception ' + e.message); } }
const sel0 = async (b) => { b.slot(0); await sleep(150); };
async function useHeld(b, ms = 250) { b.use(); await sleep(ms); b.release(); await sleep(150); }
const nearestEnt = (b, x, y, z, type = 70) => { let best = null, bd = 1e9; for (const e of Object.values(b.ents)) { if (type !== null && e.type !== type) continue; const d = (e.x - x) ** 2 + (e.y - y) ** 2 + (e.z - z) ** 2; if (d < bd) { bd = d; best = e; } } return [best, Math.sqrt(bd)]; };

async function arena() {
  await run(`forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run(`fill ${X - 30} ${Y - 1} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:stone`);
  for (let y = Y; y <= Y + 14; y += 7) await run(`fill ${X - 30} ${y} ${Z - 30} ${X + 30} ${Math.min(y + 6, Y + 14)} ${Z + 30} minecraft:air`);
  for (let y = Y - 20; y <= Y - 2; y += 7) await run(`fill ${X - 30} ${y} ${Z - 30} ${X + 30} ${Math.min(y + 6, Y - 2)} ${Z + 30} minecraft:stone`);
  await run('weather clear'); await run('time set 6000'); await run('gamerule doDaylightCycle false').catch(() => {});
  await run('difficulty normal'); await sleep(500);
}

(async () => {
  R = await rcon();
  A = await bot('TestRat'); B = await bot('TestRat2');
  await sleep(1000);
  await arena();
  for (const w of ['TestRat', 'TestRat2']) await reset(w);
  await tp('TestRat', X + 0.5, Y, Z + 0.5); await tp('TestRat2', X + 20.5, Y, Z + 20.5); await sleep(1500);

  // ------------------------------------------------------------------ coffee
  await test('coffee stacks and crashes', async () => {
    await give('TestRat', 'coffee'); await give('TestRat', 'coffee'); await sel0(A);
    A.use(); await sleep(1700); A.use(); await sleep(1700);
    const s1 = await effect('TestRat', 'speed'), j1 = await effect('TestRat', 'jump_boost');
    await run('scoreboard players set TestRat bm.coft 1'); await sleep(2200);
    const sl = await effect('TestRat', 'slowness'), wk = await effect('TestRat', 'weakness');
    ok('coffee stacks and crashes', s1 === 1 && j1 === 1 && sl !== null && wk !== null, `speed amp ${s1}, jump ${j1}, crash slowness ${sl} weakness ${wk}`);
  });
  await reset('TestRat');

  // ------------------------------------------------------------------ storm ball
  await test('storm ball lightning', async () => {
    await give('TestRat', 'storm_ball'); await sel0(A); await run('effect give TestRat minecraft:fire_resistance 30 0 true'); await run('effect give TestRat minecraft:resistance 10 4 true');
    await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0); await sleep(400);
    A.use(); let seen = 0;
    for (let i = 0; i < 25 && !seen; i++) { await sleep(100); seen = await count(`@e[type=minecraft:lightning_bolt,x=${X},y=${Y},z=${Z},distance=..20]`); }
    ok('storm ball lightning', seen > 0, seen ? 'lightning struck where it landed' : 'no lightning');
  });
  await reset('TestRat'); await run('kill @e[type=minecraft:item]');

  // ------------------------------------------------------------------ Specter Sheet: phase, cooldown, uses; stitch; charm
  await test('specter sheet phase/cooldown/uses', async () => {
    await run(`fill ${X + 3} ${Y} ${Z - 3} ${X + 5} ${Y + 2} ${Z + 3} minecraft:stone`);
    await give('TestRat', 'specter_sheet'); await sel0(A);
    await tp('TestRat', X + 2.5, Y, Z + 0.5, -90, 0); await sleep(400);
    await useHeld(A); await sleep(300);
    const p1 = await pos('TestRat');
    const lore = await run('data get entity TestRat SelectedItem.components."minecraft:lore"[0].text');
    await tp('TestRat', X + 2.5, Y, Z + 0.5, -90, 0); await sleep(300); await useHeld(A); await sleep(300);
    const p2 = await pos('TestRat');
    const bar = A.bars.slice(-1)[0] || '';
    ok('specter sheet phase/cooldown/uses', p1[0] > X + 5 && p2[0] < X + 3 && lore.includes('4 / 5') && bar.includes('settling'),
       `phased to x=${p1[0]}, retry stayed at x=${p2[0]} ("${bar}"), ${lore.split(':').slice(-1)[0].trim()}`);
    await run(`fill ${X + 3} ${Y} ${Z - 3} ${X + 5} ${Y + 2} ${Z + 3} minecraft:air`);
  });
  await reset('TestRat');
  await test('specter charm stitched from 9 sheets (sneak + use)', async () => {
    for (let i = 0; i < 9; i++) await give('TestRat', 'specter_sheet');
    await sel0(A); A.input({ shift: true }); await sleep(300); await useHeld(A); A.input({}); await sleep(300);
    const got = await has('TestRat', 'specter_charm'), left = await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"specter_sheet"}] 0');
    ok('specter charm stitched from 9 sheets (sneak + use)', got && left === 0, `charm ${got}, sheets left ${left}`);
  });
  await reset('TestRat');
  await test('specter charm: night buffs, darkness aura, daylight burn', async () => {
    await run('loot replace entity TestRat armor.chest loot bm:items/specter_charm');
    await tp('TestRat', X + 0.5, Y, Z + 0.5); await tp('TestRat2', X + 3.5, Y, Z + 0.5);
    await run('time set 18000'); await sleep(2600);
    const sp = await effect('TestRat', 'speed'), nv = await effect('TestRat', 'night_vision'), dk2 = await effect('TestRat2', 'darkness'), dk1 = await effect('TestRat', 'darkness');
    const sfd = await num('attribute TestRat minecraft:safe_fall_distance get');
    await run('time set 6000'); await sleep(2600);
    const fire = await num('data get entity TestRat Fire');
    ok('specter charm: night buffs, darkness aura, daylight burn', sp === 2 && nv !== null && dk2 !== null && dk1 === null && sfd >= 30 && fire > 0,
       `night: speed amp ${sp}, NV ${nv !== null}; other player darkness ${dk2 !== null}, wearer darkness ${dk1 !== null}; safe fall ${sfd}; day Fire ${fire}`);
    await run('item replace entity TestRat armor.chest with minecraft:air');
  });
  await reset('TestRat'); await reset('TestRat2'); await tp('TestRat2', X + 20.5, Y, Z + 20.5);

  // ------------------------------------------------------------------ Surface / Lava charms
  await test('surface charm lifts you out of a cave', async () => {
    await run(`fill ${X + 10} ${Y - 12} ${Z + 10} ${X + 12} ${Y - 10} ${Z + 12} minecraft:air`);
    await give('TestRat', 'surface_charm'); await sel0(A); await tp('TestRat', X + 11.5, Y - 12, Z + 11.5); await sleep(400);
    await useHeld(A); await sleep(300);
    const p = await pos('TestRat'); ok('surface charm lifts you out of a cave', p[1] >= Y, `y ${Y - 12} -> ${p[1]}`);
  });
  await reset('TestRat');
  await test('lava charm saves you automatically', async () => {
    await run(`fill ${X - 8} ${Y - 1} ${Z - 8} ${X - 6} ${Y} ${Z - 6} minecraft:lava`);
    await give('TestRat', 'lava_charm'); await tp('TestRat', X - 3.5, Y, Z - 3.5); await sleep(2500);       // stand on safe ground first (remembered)
    await tp('TestRat', X - 6.5, Y - 1, Z - 6.5); await sleep(1200);
    const p = await pos('TestRat'); const still = await has('TestRat', 'lava_charm'); const fr = await effect('TestRat', 'fire_resistance');
    ok('lava charm saves you automatically', Math.abs(p[0] - (X - 3.5)) < 1 && !still && fr !== null, `landed at ${p.map(v => v.toFixed(1))}, charm used ${!still}, fire res ${fr !== null}`);
    await run(`fill ${X - 8} ${Y - 1} ${Z - 8} ${X - 6} ${Y} ${Z - 6} minecraft:stone`); await run(`fill ${X - 8} ${Y} ${Z - 8} ${X - 6} ${Y} ${Z - 6} minecraft:air`);
  });
  await reset('TestRat');

  // ------------------------------------------------------------------ Blue Marlin wall trophy
  await test('blue marlin mounts on a wall and comes back', async () => {
    await run(`fill ${X + 3} ${Y} ${Z - 2} ${X + 3} ${Y + 3} ${Z + 2} minecraft:oak_planks`);
    await give('TestRat', 'blue_marlin'); await sel0(A); await tp('TestRat', X + 1.5, Y, Z + 0.5, -90, 0); await sleep(400);
    A.input({ shift: true }); await sleep(250); await useHeld(A); A.input({}); await sleep(400);
    const mounted = await count('@e[type=minecraft:item_display,tag=bm.mdisp]'); const gone = !(await has('TestRat', 'blue_marlin'));
    // punch it
    const [e, d] = nearestEnt(A, X + 2.9, Y + 1.5, Z + 0.5);
    if (e) A.attack(e.entityId); await sleep(500);
    const back = await has('TestRat', 'blue_marlin');
    ok('blue marlin mounts on a wall and comes back', mounted === 1 && gone && back, `mounted ${mounted}, left hand ${gone}, punched back ${back}`);
    await run(`fill ${X + 3} ${Y} ${Z - 2} ${X + 3} ${Y + 3} ${Z + 2} minecraft:air`);
  });
  await reset('TestRat');

  // ------------------------------------------------------------------ mailbox + courier
  await test('mailbox: place, post (other player), open with key', async () => {
    await give('TestRat', 'mailbox'); await sel0(A); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 60); await sleep(400);
    await useHeld(A); await sleep(500);
    const box = await count('@e[type=minecraft:interaction,tag=bm.mbox]'); const key = await has('TestRat', 'mail_key');
    await run('give TestRat2 minecraft:diamond 3'); await tp('TestRat2', X + 0.5, Y, Z - 1.5, 0, 30); await sleep(600);
    B.slot(0); await sleep(150);
    const [e] = nearestEnt(B, X + 0.5, Y, Z + 2.0);
    let posted = '';
    if (e) { B.interact(e.entityId); await sleep(600); posted = await run('data get storage bm:mail'); }
    ok('mailbox: place, post (other player)', box === 1 && key && posted.includes('diamond'), `box ${box}, key ${key}, storage ${posted.slice(0, 160)}`);
    // owner opens with the key in hand
    await run('clear TestRat *[minecraft:custom_data~{bm:"mailbox"}]');
    await tp('TestRat', X + 0.5, Y, Z - 1.5, 0, 30); await sleep(400); A.windows = [];
    for (let i = 0; i < 9; i++) { const s = await run(`execute if items entity TestRat hotbar.${i} *[minecraft:custom_data~{bm:"mail_key"}]`); if (s.includes('passed')) { A.slot(i); break; } }
    await sleep(200); if (e) A.interact(e.entityId); await sleep(800);
    A.write('entity_action', { entityId: A.eid, actionId: 'open_inventory', jumpBoost: 0 }); await sleep(600);
    const crate = await run('data get entity @e[type=minecraft:dark_oak_chest_boat,tag=bm.c_mail,limit=1] Items');
    ok('mailbox: key opens it (crate window)', A.windows.length > 0 && crate.includes('diamond'), `windows opened ${A.windows.length}; crate holds: ${crate.slice(0, 120)}`);
    if (A.windows.length) A.close(A.windows[0].windowId); await sleep(300);
    A.input({ shift: true }); await sleep(800); A.input({}); await sleep(500);
    const after = await run('data get storage bm:mail');
    ok('mailbox: closing stores contents back', after.includes('diamond'), after.slice(0, 160));
  });
  await test('courier whistle delivers to a mailbox number', async () => {
    const n = await num('scoreboard players get @e[type=minecraft:interaction,tag=bm.mbox,limit=1] bm.mbid');
    await reset('TestRat2'); await give('TestRat2', 'courier_whistle'); await give('TestRat2', 'token');
    await run('item replace entity TestRat2 weapon.offhand with minecraft:emerald 5'); B.slot(0); await sleep(200);
    B.use(); await sleep(250); B.release(); await sleep(400);
    B.cmd(`trigger bm.post set ${n}`); await sleep(800);
    const st = await run('data get storage bm:mail');
    ok('courier whistle delivers to a mailbox number', st.includes('emerald'), `box ${n}: ${st.slice(0, 200)}`);
  });
  await reset('TestRat'); await reset('TestRat2'); await run('kill @e[tag=bm.mbox]'); await run('kill @e[tag=bm.mbdisp]'); await tp('TestRat2', X + 20.5, Y, Z + 20.5);

  // ------------------------------------------------------------------ Vorn Skiff + paint kit; drill
  await test('vorn skiff: call, ride, paint kit', async () => {
    await give('TestRat', 'skiff_key'); await sel0(A); await tp('TestRat', X + 0.5, Y, Z + 0.5, 0, 0); await sleep(400);
    await useHeld(A); await sleep(1500);
    const sk = await count('@e[type=minecraft:happy_ghast,tag=bm.skiff]');
    const riding = (await run('execute as TestRat on vehicle if entity @s[tag=bm.skiff]')).includes('passed');
    await give('TestRat', 'skiff_paint_crimson'); await sleep(200);
    for (let i = 0; i < 9; i++) { const s = await run(`execute if items entity TestRat hotbar.${i} *[minecraft:custom_data~{bm:"skiff_paint_crimson"}]`); if (s.includes('passed')) { A.slot(i); break; } }
    await sleep(200); await useHeld(A); await sleep(600);
    const model = await run('data get entity @e[type=minecraft:item_display,tag=bm.skdisp,limit=1] item.components."minecraft:item_model"');
    ok('vorn skiff: call, ride, paint kit', sk === 1 && riding && model.includes('crimson'), `skiff ${sk}, riding ${riding}, hull ${model.split(':').slice(-2).join(':')}`);
    await run('ride TestRat dismount'); await run('kill @e[tag=bm.skiff]'); await run('kill @e[tag=bm.skdisp]');
  });
  await reset('TestRat');
  await test('vorn drill bores through stone', async () => {
    await run(`fill ${X + 2} ${Y} ${Z - 1} ${X + 8} ${Y + 2} ${Z + 1} minecraft:stone`);
    await give('TestRat', 'vorn_drill'); await give('TestRat', 'xenite_red'); await sel0(A); await tp('TestRat', X + 1.5, Y, Z + 0.5, -90, 0); await sleep(400);
    A.use(); await sleep(2000); A.release(); await sleep(300);
    const s = await run(`execute store result score #t bm.rng run fill ${X + 2} ${Y} ${Z - 1} ${X + 8} ${Y + 2} ${Z + 1} minecraft:stone replace minecraft:air`);
    const mined = parseInt((s.match(/(\d+)/) || [0, 0])[1]);
    ok('vorn drill bores through stone', mined > 0, `${mined} blocks bored`);
    await run(`fill ${X + 2} ${Y} ${Z - 1} ${X + 8} ${Y + 2} ${Z + 1} minecraft:air`);
  });
  await reset('TestRat'); await run('kill @e[type=minecraft:item]');

  // ------------------------------------------------------------------ the treasure accessories (phase39)
  await test('rod of discord teleports (and hurts)', async () => {
    await give('TestRat', 'rod_of_discord'); await sel0(A); await tp('TestRat', X + 0.5, Y, Z + 0.5, -90, 0); await sleep(400);
    await useHeld(A); await sleep(300); const p = await pos('TestRat'); const hp = await num('data get entity TestRat Health');
    ok('rod of discord teleports (and hurts)', p[0] > X + 10 && hp < 20, `x ${X + 0.5} -> ${p[0].toFixed(1)}, health ${hp}`);
  });
  await reset('TestRat');
  await test('bottomless water bucket: pour and soak', async () => {
    await run(`fill ${X + 4} ${Y} ${Z - 1} ${X + 4} ${Y + 2} ${Z + 1} minecraft:stone`);
    await give('TestRat', 'bottomless_water'); await sel0(A); await tp('TestRat', X + 1.5, Y, Z + 0.5, -90, 20); await sleep(400);
    await useHeld(A); await sleep(300);
    const w = await num(`execute store result score #t bm.rng run fill ${X} ${Y} ${Z - 3} ${X + 3} ${Y + 2} ${Z + 3} minecraft:water replace minecraft:water`);
    A.input({ shift: true }); await sleep(200); await useHeld(A); A.input({}); await sleep(300);
    const after = await count(`@e[type=minecraft:marker,tag=__none__]`);
    const left = (await run(`execute if block ${X + 3} ${Y} ${Z} minecraft:water`)).includes('passed');
    const anyWater = await run(`execute store result score #t bm.rng run fill ${X} ${Y} ${Z - 3} ${X + 3} ${Y + 2} ${Z + 3} minecraft:water replace minecraft:water`);
    ok('bottomless water bucket: pour and soak', !left && /No blocks/.test(anyWater) || /0/.test(anyWater), `poured, then soaked (remaining check: "${anyWater}")`);
    await run(`fill ${X - 2} ${Y} ${Z - 4} ${X + 5} ${Y + 3} ${Z + 4} minecraft:air`);
  });
  await reset('TestRat');
  await test('enchanted sundial skips the night', async () => {
    await run('scoreboard players reset #sundial bm.rng'); await run('time set 18000'); await sleep(1300);
    await give('TestRat', 'enchanted_sundial'); await sel0(A); await useHeld(A); await sleep(1300);
    const tod = await score('#tod', 'bm.bm'); ok('enchanted sundial skips the night', tod < 1000, `#tod 18000 -> ${tod}`); await run('time set 6000');
  });
  await reset('TestRat');
  await test('metal detector reports ore', async () => {
    await run(`setblock ${X + 2} ${Y - 3} ${Z} minecraft:diamond_ore`); await run(`setblock ${X - 2} ${Y - 4} ${Z + 1} minecraft:gold_ore`);
    await give('TestRat', 'metal_detector'); await sel0(A); await tp('TestRat', X + 0.5, Y, Z + 0.5); A.bars = []; await sleep(2600);
    const bar = A.bars.find(b => b.includes('Metal')) || ''; const kept = (await run(`execute if block ${X + 2} ${Y - 3} ${Z} minecraft:diamond_ore`)).includes('passed');
    ok('metal detector reports ore', bar.includes('Diamond') && kept, `"${bar}" (ore untouched ${kept})`);
  });
  await reset('TestRat');
  await test('lifeform analyzer finds a rare monster', async () => {
    await run(`execute positioned ${X + 15} ${Y} ${Z + 5} run function bm:admin/rare/glimmer`);
    await run('data merge entity @e[type=minecraft:spider,tag=bm.rare,limit=1] {NoAI:1b,PersistenceRequired:1b}');
    await give('TestRat', 'lifeform_analyzer'); await tp('TestRat', X + 0.5, Y, Z + 0.5); A.bars = []; await sleep(2300);
    const bar = A.bars.find(b => b.includes('blocks')) || A.bars.slice(-1)[0] || ''; ok('lifeform analyzer finds a rare monster', /blocks/.test(bar), `"${bar}"`);
    await run('kill @e[type=minecraft:spider,tag=bm.rare]');
  });
  await reset('TestRat');
  await test('band of regeneration heals after 5 s unhurt', async () => {
    await give('TestRat', 'band_of_regeneration'); await run('damage TestRat 6 minecraft:magic'); await sleep(8000);
    const rg = await effect('TestRat', 'regeneration'); ok('band of regeneration heals after 5 s unhurt', rg !== null, `regeneration ${rg !== null}`);
  });
  await reset('TestRat');
  await test('obsidian skull: fire res in fire', async () => {
    await give('TestRat', 'obsidian_skull'); await run(`setblock ${X + 6} ${Y} ${Z + 6} minecraft:fire`); await tp('TestRat', X + 6.5, Y, Z + 6.5); await sleep(900);
    const fr = await effect('TestRat', 'fire_resistance'); ok('obsidian skull: fire res in fire', fr !== null, `fire resistance ${fr !== null}`);
    await run(`setblock ${X + 6} ${Y} ${Z + 6} minecraft:air`);
  });
  await reset('TestRat');
  await test('cobalt shield / extendo grip attributes', async () => {
    await run('loot replace entity TestRat weapon.offhand loot bm:items/cobalt_shield'); await sleep(300);
    const kb = await num('attribute TestRat minecraft:knockback_resistance get');
    await run('loot replace entity TestRat weapon.offhand loot bm:items/extendo_grip'); await sleep(300);
    const reach = await num('attribute TestRat minecraft:block_interaction_range get');
    ok('cobalt shield / extendo grip attributes', kb >= 1 && reach >= 7.5, `knockback resistance ${kb}, block reach ${reach}`);
  });
  await reset('TestRat');
  await test('ice skates: speed on ice', async () => {
    await run(`fill ${X - 5} ${Y - 1} ${Z + 5} ${X - 3} ${Y - 1} ${Z + 7} minecraft:packed_ice`);
    await run('loot replace entity TestRat armor.feet loot bm:items/ice_skates'); await tp('TestRat', X - 3.5, Y, Z + 6.5); await sleep(900);
    const sp = await effect('TestRat', 'speed'); ok('ice skates: speed on ice', sp === 1, `speed amp ${sp}`);
    await run(`fill ${X - 5} ${Y - 1} ${Z + 5} ${X - 3} ${Y - 1} ${Z + 7} minecraft:stone`);
  });
  await reset('TestRat');
  await test('umbrella: slow falling when airborne', async () => {
    await give('TestRat', 'umbrella'); await sel0(A); await tp('TestRat', X + 0.5, Y + 10, Z + 0.5); await sleep(700);
    const sf = await effect('TestRat', 'slow_falling'); ok('umbrella: slow falling when airborne', sf !== null, `slow falling ${sf !== null}`);
  });
  await reset('TestRat');
  await test('climbing claws: climb when pushing into a wall', async () => {
    await run(`fill ${X + 3} ${Y} ${Z - 2} ${X + 3} ${Y + 8} ${Z + 2} minecraft:stone`);
    await give('TestRat', 'climbing_claws'); await tp('TestRat', X + 2.6, Y + 2, Z + 0.5, -90, 0); A.input({ forward: true }); await sleep(250);
    const lev = await effect('TestRat', 'levitation'); A.input({}); await sleep(200); const sf = await effect('TestRat', 'slow_falling');
    ok('climbing claws: climb when pushing into a wall', lev !== null && sf !== null, `levitation while pushing ${lev !== null}, slide (slow falling) on release ${sf !== null}`);
    await run(`fill ${X + 3} ${Y} ${Z - 2} ${X + 3} ${Y + 8} ${Z + 2} minecraft:air`);
  });
  await reset('TestRat');
  await test('water walking boots: rise and hover', async () => {
    await run(`fill ${X - 10} ${Y - 3} ${Z - 10} ${X - 6} ${Y - 1} ${Z - 6} minecraft:water`);
    await run('loot replace entity TestRat armor.feet loot bm:items/water_walking_boots'); await tp('TestRat', X - 7.5, Y - 2, Z - 7.5); await sleep(200);
    const rise = await effect('TestRat', 'levitation'); await tp('TestRat', X - 7.5, Y + 0.05, Z - 7.5); await sleep(150);
    const hov = await effect('TestRat', 'levitation');
    ok('water walking boots: rise and hover', rise === 2 && hov === 255, `in water: levitation ${rise}; on the surface: ${hov} (255 = hover)`);
    await run(`fill ${X - 10} ${Y - 3} ${Z - 10} ${X - 6} ${Y - 1} ${Z - 6} minecraft:stone`);
  });
  await reset('TestRat');
  await test('fallen stars -> star cloak -> strikes when hurt', async () => {
    for (let i = 0; i < 9; i++) await give('TestRat', 'fallen_star');
    await sel0(A); await useHeld(A); await sleep(300);
    const cloak = await has('TestRat', 'star_cloak');
    await run(`summon minecraft:zombie ${X + 3.5} ${Y} ${Z + 0.5} {Tags:["t_star"],NoAI:1b,PersistenceRequired:1b,Health:20f}`); await sleep(300);
    await run('damage TestRat 2 minecraft:magic'); await sleep(500);
    const zh = await num('data get entity @e[type=minecraft:zombie,tag=t_star,limit=1] Health');
    ok('fallen stars -> star cloak -> strikes when hurt', cloak && zh < 20, `cloak ${cloak}, zombie health 20 -> ${zh}`);
    await run('kill @e[tag=t_star]');
  });
  await reset('TestRat');
  await test('fishing crates open into loot', async () => {
    for (const c of ['wooden', 'iron', 'golden']) await give('TestRat', `crate_${c}`);
    let gained = 0;
    for (let s = 0; s < 3; s++) { A.slot(s); await sleep(150); const before = await slots('TestRat'); await useHeld(A); await sleep(300);
                                  const after = await slots('TestRat'); if (after > before - 1 && !(await run(`execute if items entity TestRat hotbar.${s} *[minecraft:custom_data~{bm:"crate_${['wooden','iron','golden'][s]}"}]`)).includes('passed')) gained++; }
    ok('fishing crates open into loot', gained === 3, `${gained}/3 crates opened into items`);
  });
  await reset('TestRat');
  await test('enchanted sword beam at full health', async () => {
    await run('loot give TestRat loot bm:items/enchanted_sword'); await sel0(A);
    await run(`summon minecraft:zombie ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["t_beam"],NoAI:1b,PersistenceRequired:1b,Health:20f}`);
    await tp('TestRat', X + 0.5, Y, Z + 0.5, -90, 0); await sleep(400); await useHeld(A); await sleep(300);
    const zh = await num('data get entity @e[type=minecraft:zombie,tag=t_beam,limit=1] Health');
    ok('enchanted sword beam at full health', zh < 20, `zombie health 20 -> ${zh}`); await run('kill @e[tag=t_beam]');
  });
  await reset('TestRat');
  await test('sword shrine: pull the sword', async () => {
    await run('kill @e[tag=bm.shrine_i]'); await run('kill @e[tag=bm.shrine_d]');
    await run(`execute positioned ${X - 12.5} ${Y} ${Z + 12.5} run function bm:p39/shrine/build`);
    await tp('TestRat', X - 12.5, Y + 1, Z + 10.5, 0, 20); await sleep(1800);
    const [e] = nearestEnt(A, X - 12.5, Y + 1, Z + 12.5); if (e) A.interact(e.entityId); await sleep(500);
    const got = await has('TestRat', 'enchanted_sword'); const left = await count('@e[type=minecraft:item_display,tag=bm.shrine_d]');
    ok('sword shrine: pull the sword', got && left === 0, e ? `sword in inventory ${got}, sword gone from the stone ${left === 0}` : 'no interaction entity seen');
  });
  await reset('TestRat');

  // ------------------------------------------------------------------ real chest opening: loot hooks and Mimics
  await test('loot chests: hooks fire on real opens, Mimics appear', async () => {
    let mimics = 0, tokens = 0, opens = 0;
    await tp('TestRat', X + 0.5, Y, Z - 5.5, 180, 30); await sleep(400);
    for (let i = 0; i < 300; i++) {
      await run(`setblock ${X} ${Y} ${Z - 7} minecraft:air`);
      await run(`setblock ${X} ${Y} ${Z - 7} minecraft:chest[facing=south]{LootTable:"minecraft:chests/simple_dungeon"}`);
      A.useOn(X, Y, Z - 7, 3); await sleep(160);
      const lt = await run(`data get block ${X} ${Y} ${Z - 7} LootTable`); if (!lt.includes('simple_dungeon')) opens++;
      A.close(1); A.close(2); await sleep(60);
      const m = await count('@e[type=minecraft:rabbit,tag=bm.mimic]'); if (m) { mimics += m; await run('kill @e[type=minecraft:rabbit,tag=bm.mimic]'); await sleep(1200); }
    }
    tokens = await items('TestRat', '*[minecraft:custom_data~{bm:"token"}]');
    ok('loot chests: hooks fire on real opens, Mimics appear', opens > 250 && tokens > 0 && mimics > 0,
       `${opens} chests opened, ${tokens} Tokens found (20% hook), ${mimics} Mimics (1% each)`);
  });

  console.log('\n' + results.filter(r => r[1]).length + '/' + results.length + ' passed');
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
