// 3.0c: WORN WINGS FLAT BY DEFAULT, 3D FOR SCREENSHOTS (seraph_wings.py's gate, flat_wings.py, noparts.py's fifth row), as a
// regular (non-op) player, every step a real packet. rcon sets the stage only: a floor and a wall, the gear handed over (as a
// trader would), an old world's wings left on the bot, a frame on the wall, counts and NBT read back.
//   flat     the Dread Carapace put on (right-clicked): no 3D wing displays anywhere near; its elytra layer the flat one
//            (equippable asset bm:dread_carapace); an old world's wings (a wearer's tags and four displays of his, as 2.99 left
//            them) are gone within a second
//   toggler  the Particle Toggler's menu: a fifth row "3D wings (for screenshots): OFF" (its tooltip: great standing still,
//            trailing when you move fast); pressed: the menu back with it ON, a click, the action bar, the bm.w3d tag - the four
//            displays come out on the bot (the client is sent them), his own, and the item wears the mantle layer
//            (bm:dread_carapace_mantle); pressed again: OFF, the displays gone, the flat layer back
//   trigger  no toggler: /trigger bm.wings3d - ON, the displays out; again - OFF, gone
//   sweep    the 3D wings on, the carapace taken off (its mantle kept), the wings switched off, the carapace worn again: the
//            flat layer back within a second
//   sov      the Wings of the Last Night worn: no displays, the flat sov_wings layer
//   frame    the carapace hung in a frame by a right-click: the frame holds it, and its item model shows its 3D wings in a
//            frame or a display case (the 'fixed' context: bm:item/dread_carapace_3d) - the same for the Seraph's Wings
//   node t331.js
const fs = require('fs');
const path = require('path');
const { bot, rcon, sleep } = require('./lib_resp');
const O = 'execute in minecraft:overworld run ';
const X = 21400, Y = 100, Z = 16800;
const TG = '{components:{"minecraft:custom_data":{bm:"particle_toggler"}}}';
const RP = path.join(__dirname, '..', '..', 'out_p2', 'BlackMarket_RP', 'assets', 'bm');

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const nbt = async (sel, p) => (await run(`${O}data get entity ${sel} ${p}`)).replace(/^.*?has the following entity data: /, '');
  const cnt = async (sel) => +(((await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const tags = async () => (await run('tag TestRat list'));
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const use = async () => { A.use(); await sleep(350); A.release(); await sleep(500); };
  const dd = d => d && (d.data || d);
  const pid = async () => +(((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, -9])[1]);
  // the bot's own wing displays (any set), and every wing display within 16 blocks
  const mine = async (set = '') => cnt(`@e[type=minecraft:item_display,tag=bm.swd${set ? '_' + set : ''},x=${X},y=${Y},z=${Z},distance=..16,scores={bm.pid=${await pid()}}]`);
  const any = async () => cnt(`@e[type=minecraft:item_display,tag=bm.swd,x=${X},y=${Y},z=${Z},distance=..16]`);
  const asset = async () => (await nbt('TestRat', 'equipment.chest.components."minecraft:equippable".asset_id')).replace(/"/g, '');
  // (entities the client is sent near the bot: what it sees come out)
  const nearEnts = () => Object.values(A.ents).filter(e => A.pos && Math.abs(e.x - A.pos.x) < 2 && Math.abs(e.z - A.pos.z) < 2 && Math.abs(e.y - A.pos.y) < 2).length;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (const t of ['bm.w3d', 'bm.np_charm', 'bm.np_armor', 'bm.np_weap', 'bm.sww', 'bm.sww_dread', 'bm.sww_seraph', 'bm.sww_sovn', 'bm.sww_sovl']) await run(`tag TestRat remove ${t}`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('time set noon');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:saturation infinite 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}fill ${X - 4} ${Y + 1} ${Z + 5} ${X + 4} ${Y + 4} ${Z + 5} minecraft:stone`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`spawnpoint TestRat ${X} ${Y + 1} ${Z}`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  if (await pid() < 1) { await run('execute as TestRat run function bm:p21/pid'); }

  // ---------------------------------------------------------------- flat by default
  await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_carapace');
  A.slot(0); await sleep(300); await use(); await sleep(1500);
  ok('the Dread Carapace put on (right-clicked)', /dread_carapace/.test(await nbt('TestRat', 'equipment.chest')));
  ok('...no 3D wing displays come out (none within 16 blocks)', (await any()) === 0, `${await any()}`);
  ok('...its elytra layer the flat one (bm:dread_carapace)', (await asset()) === 'bm:dread_carapace', await asset());
  ok('...and the bot is no 3D wearer (no bm.sww_dread)', !/bm\.sww_dread/.test(await tags()));
  // an old world's wings, as 2.99 left them: the wearer's tags and scores, four displays of his
  const P = await pid();
  await run('tag TestRat add bm.sww_dread'); await run('tag TestRat add bm.sww'); await run('scoreboard players set TestRat bm.swn 1'); await run('scoreboard players set TestRat bm.sws 1');
  for (const p of ['w1r', 'w1l', 'w2r', 'w2l'])
    await run(`${O}summon minecraft:item_display ${X + 0.5} ${Y + 1} ${Z + 0.5} {Tags:["bm.swd","bm.swd_dread","bm.sw_${p}","bm.t331old"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"bm:dkw_${p}"}}}`);
  await run(`${O}scoreboard players set @e[type=minecraft:item_display,tag=bm.t331old] bm.pid ${P}`);
  ok('(an old world\'s four wing displays staged on the bot)', (await cnt('@e[type=minecraft:item_display,tag=bm.t331old]')) === 4);
  ok('...gone within a second (the wearer switched off on his next tick)', await wait(1500, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.t331old]')) === 0, 100) &&
     !/bm\.sww/.test(await tags()), await tags());

  // ---------------------------------------------------------------- the toggler's fifth row
  await run('loot replace entity TestRat hotbar.8 loot bm:items/particle_toggler');
  A.slot(8); await sleep(300);
  let got = await A.useWait(2500);
  const d0 = dd(A.dialogN[A.dialogN.length - 1]);
  const labels = () => A.buttons().map(b => b.label).join(' | ');
  ok('the Particle Toggler used: its menu', got && /PARTICLE TOGGLER/.test(JSON.stringify(d0 && d0.title)));
  ok('...a row "3D wings (for screenshots): OFF"', /3D wings \(for screenshots\): OFF/.test(labels()), labels());
  const tip = JSON.stringify((d0 && d0.actions || []).find(b => /3D wings/.test(JSON.stringify(b.label))) || {});
  ok('...its tooltip: great standing still, but they trail behind when you move fast', /look great standing still/.test(tip) && /trail behind you when you move fast/.test(tip), tip.slice(0, 200));
  const b = A.buttons().find(x => /3D wings/.test(x.label));
  ok('...its code is 6905', b && /trigger bm\.act set 6905$/.test(b.command), b && b.command);
  A.bars.length = 0; const s0 = A.sounds.length; const e0 = nearEnts();
  let pr = await A.press(/3D wings/);
  ok('pressed: the menu back with it ON', pr && pr.next && /3D wings \(for screenshots\): ON/.test(labels()) && /Armour: ON/.test(labels()), labels());
  ok('...a click, and the action bar says so', A.sounds.slice(s0).some(s => /ui\.button\.click/.test(s.name)) && A.bars.some(x => /3D wings: ON/.test(x)), A.bars.join(' / '));
  ok('...the player\'s own tag (bm.w3d)', /bm\.w3d/.test(await tags()));
  A.write('close_window', { windowId: 0 });
  ok('...the four 3D wing displays come out, his own', await wait(2000, async () => (await mine('dread')) === 4), `${await mine('dread')}`);
  ok('...on him (within a block of his feet)', (await cnt(`@e[type=minecraft:item_display,tag=bm.swd_dread,x=${X + 0.5},y=${Y + 1},z=${Z + 0.5},distance=..1]`)) === 4);
  ok('...the client is sent them', await wait(1500, async () => nearEnts() - e0 >= 4, 100), `${nearEnts() - e0} new near the bot`);
  ok('...and the carapace wears the mantle layer under them (bm:dread_carapace_mantle)', await wait(1500, async () => (await asset()) === 'bm:dread_carapace_mantle'), await asset());
  A.slot(8); await sleep(2300); await A.useWait(2500); await sleep(300);
  A.bars.length = 0; pr = await A.press(/3D wings/);
  ok('pressed again: OFF', pr && pr.next && /3D wings \(for screenshots\): OFF/.test(labels()) && A.bars.some(x => /3D wings: OFF/.test(x)) && !/bm\.w3d/.test(await tags()), labels());
  A.write('close_window', { windowId: 0 });
  ok('...the displays removed', await wait(1500, async () => (await any()) === 0, 100), `${await any()}`);
  ok('...the flat layer back', await wait(1500, async () => (await asset()) === 'bm:dread_carapace'), await asset());

  // ---------------------------------------------------------------- without the toggler: /trigger bm.wings3d
  await run('clear TestRat *[minecraft:custom_data~{bm:"particle_toggler"}]'); A.slot(7); await sleep(600);
  A.bars.length = 0; A.cmd('trigger bm.wings3d'); await sleep(300);
  ok('/trigger bm.wings3d (no toggler): ON, the action bar says so', await wait(1500, async () => /bm\.w3d/.test(await tags())) && A.bars.some(x => /3D wings: ON/.test(x)), A.bars.join(' / '));
  ok('...the displays out', await wait(2000, async () => (await mine('dread')) === 4), `${await mine('dread')}`);
  A.bars.length = 0; A.cmd('trigger bm.wings3d'); await sleep(300);
  ok('...again: OFF', await wait(1500, async () => !/bm\.w3d/.test(await tags())) && A.bars.some(x => /3D wings: OFF/.test(x)), A.bars.join(' / '));
  ok('...the displays gone', await wait(1500, async () => (await any()) === 0, 100), `${await any()}`);

  // ---------------------------------------------------------------- a mantle taken off with the wings on, worn again with them off
  A.cmd('trigger bm.wings3d'); await wait(2000, async () => (await mine('dread')) === 4);
  ok('(the 3D wings on again, the mantle worn)', (await asset()) === 'bm:dread_carapace_mantle', await asset());
  await run('item replace entity TestRat hotbar.0 from entity TestRat armor.chest'); await run('item replace entity TestRat armor.chest with minecraft:air');
  ok('the carapace taken off (rcon): its displays gone with it', await wait(1500, async () => (await any()) === 0, 100));
  A.cmd('trigger bm.wings3d'); await wait(1500, async () => !/bm\.w3d/.test(await tags()));
  ok('...still the mantle in the hand', /dread_carapace_mantle/.test(await nbt('TestRat', 'Inventory[{Slot:0b}]')));
  A.slot(0); await sleep(300); await use();
  ok('worn again with the 3D wings off: the flat layer back within a second', await wait(1500, async () => (await asset()) === 'bm:dread_carapace', 100), await asset());
  ok('...and no displays', (await any()) === 0);

  // ---------------------------------------------------------------- the Wings of the Last Night
  await run('item replace entity TestRat armor.chest with minecraft:air'); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/sov_wings'); A.slot(0); await sleep(300); await use(); await sleep(1500);
  ok('the Wings of the Last Night put on (right-clicked)', /sov_wings/.test(await nbt('TestRat', 'equipment.chest')));
  ok('...no 3D displays, the flat layer (bm:sov_wings)', (await any()) === 0 && (await asset()) === 'bm:sov_wings', `${await any()} ${await asset()}`);
  const lore = await nbt('TestRat', 'equipment.chest.components."minecraft:lore"');
  ok('...its lore says how to get the 3D wings', /trigger bm\.wings3d/.test(lore));
  A.cmd('trigger bm.wings3d');
  ok('...switched on: its four displays out (the halo among them)', await wait(2000, async () => (await mine('sovn')) === 4) &&
     (await cnt(`@e[type=minecraft:item_display,tag=bm.sw_halo,x=${X},y=${Y},z=${Z},distance=..4]`)) === 1, `${await mine('sovn')}`);
  A.cmd('trigger bm.wings3d');
  ok('...off: gone, the flat layer back', await wait(1500, async () => (await any()) === 0 && (await asset()) === 'bm:sov_wings'), `${await any()} ${await asset()}`);

  // ---------------------------------------------------------------- a display piece: the carapace in a frame
  await run('item replace entity TestRat armor.chest with minecraft:air'); await run('clear TestRat');
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t331f"]}`); await sleep(400);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_carapace');
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
  const frSel = `@e[type=minecraft:item_frame,tag=bm.t331f,limit=1]`;
  const uu = (await nbt(frSel, 'UUID')).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/);
  const h = uu ? uu.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join('') : '';
  const u = h && `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
  let fr = null; await wait(4000, async () => (fr = Object.values(A.ents).find(e => e.objectUUID === u)) != null, 250);
  ok('a frame on the wall', !!fr);
  A.slot(0); await sleep(300); if (fr) A.interact(fr.entityId); await sleep(1200);
  ok('the Dread Carapace hung in it by a right-click', /dread_carapace/.test(await nbt(frSel, 'Item')));
  const im = (iid) => { try { return JSON.parse(fs.readFileSync(path.join(RP, 'items', `${iid}.json`), 'utf8')); } catch (e) { return null; } };
  const fixedOf = (iid) => { const m = im(iid); const c = m && m.model && (m.model.cases || []).find(c => (c.when || []).includes('fixed')); return c && c.model.model; };
  ok('...framed (and in a display case: the same "fixed" context) it shows its 3D wings', fixedOf('dread_carapace') === 'bm:item/dread_carapace_3d' &&
     fs.existsSync(path.join(RP, 'models', 'item', 'dread_carapace_3d.json')), fixedOf('dread_carapace'));
  ok("...so does the Seraph's Wings (the holy carapace)", fixedOf('angel_dread_carapace') === 'bm:item/angel_dread_carapace_3d' &&
     fs.existsSync(path.join(RP, 'models', 'item', 'angel_dread_carapace_3d.json')), fixedOf('angel_dread_carapace'));
  ok('...and both Sovereign\'s wings (as before)', fixedOf('sov_wings') === 'bm:item/sov_wings_3d' && fixedOf('sov_wings_holy') === 'bm:item/sov_wings_holy_3d');
  const m = im('dread_carapace');
  ok('...in the hand and the inventory, its sprite as before', m && m.model.fallback && m.model.fallback.model === 'bm:item/dread_carapace');

  // ---------------------------------------------------------------- clean up
  await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t331f]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('tag TestRat remove bm.w3d'); await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
