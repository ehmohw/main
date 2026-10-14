// 2.78: the Frog with Mustache and Donado carry a token, like every follower - as a regular (non-op) player: the Frog hired
// at his hut (1 Medallion) hands over his Signet (again: no charge); handed a sword, sent home from the Signet's menu and
// called back with it; he faints - the Signet rests, nothing is dropped, and after the rest he's back with his sword; his
// gear handed back from the menu (and no copy of it left with him); he fades when you die. Donado freed from a pen hands
// over his Collar Tag; the three-follower limit counts him now. The Signet in a display case: a little Frog; Donado's tag in
// an item frame: Donado comes out of it. A Frog from before (no token) hands his Signet over instead of going home.
// rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const vanilla = async (who, id) => +(((await run(`clear ${who} minecraft:${id} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const slotOf = async (iid) => { for (let i = 0; i < 36; i++) if (new RegExp(`"${iid}"`).test(await nbt('TestRat', `Inventory[{Slot:${i}b}].components."minecraft:custom_data".bm`))) return i; return -1; };
  const X = 16360, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.fgcd 0'); await run('scoreboard players set TestRat bm.dncd 0'); await run('scoreboard players set TestRat bm.cpcd 0');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.frogpet]`); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.donado]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const pid = await sc('TestRat', 'bm.pid');
  const FROG = `@e[type=minecraft:wolf,tag=bm.frogpet,tag=!bm.ffpet,scores={bm.pid=${pid}},limit=1]`;
  const DON = `@e[type=minecraft:wolf,tag=bm.donado,tag=!bm.ffpet,scores={bm.pid=${pid}},limit=1]`;
  const useSlot = async (s, sneak = false) => { A.slot(s); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(250); }
    const n0 = A.dialogN.length; A.use(); await sleep(450); A.release(); if (sneak) { await sleep(150); A.input({}); } await sleep(400); return A.dialogN.length > n0; };
  const tokenUse = async (iid, sneak = false) => { const s = await slotOf(iid); await sleep(2100); return useSlot(s, sneak); };    // (2 s apart: the token's debounce)

  // ---------------------------------------------------------------- the Frog's hut: hire him, and he hands over his Signet
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} rotated 180 0 run function bm:npc/frog_hut`); await sleep(800);
  for (let i = 0; i < 2; i++) await run('loot give TestRat loot bm:items/medallion');
  const hire = await entOf(A, `@e[type=minecraft:interaction,tag=bm.frog_hire,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..2,limit=1]`);
  A.slot(8); await sleep(200);
  if (hire) A.interact(hire.entityId); await sleep(1500);
  ok('hiring the Frog (1 Medallion) hands you his Signet', (await has('TestRat', 'frog_signet')) === 1 && (await has('TestRat', 'medallion')) === 1);
  ok('...and he joins you (his own: the token\'s, ready to keep his gear)', await wait(3000, async () => (await cnt(FROG.replace('limit=1', 'tag=bm.f136'))) === 1));
  await sleep(2200);
  if (hire) A.interact(hire.entityId); await sleep(1200);
  ok('the hut again: "already sworn" - no charge, no second Signet, no second Frog', (await has('TestRat', 'medallion')) === 1 && (await has('TestRat', 'frog_signet')) === 1 &&
     (await cnt(FROG.replace(',limit=1', ''))) === 1);

  // ---------------------------------------------------------------- hand him a sword; send him home from the menu; call him back
  await run('item replace entity TestRat hotbar.3 with minecraft:iron_sword');
  let fw = await entOf(A, FROG);
  A.slot(3); await sleep(300); if (fw) A.interact(fw.entityId); await sleep(900);
  ok('right-click him holding a sword: he takes it', /iron_sword/.test(await nbt(FROG, 'equipment.mainhand.id')) && (await vanilla('TestRat', 'iron_sword')) === 0);
  let shown = await tokenUse('frog_signet', true);
  const bt = A.buttons().map(b => b.label || b.text || JSON.stringify(b)).join(' | ');
  ok('sneak + use the Signet: his menu (sit / hand back gear / send home)', shown && /Sit \/ follow/.test(bt) && /Hand back my gear/.test(bt) && /Send him home/.test(bt), bt.slice(0, 160));
  await A.press(/Send him home/); await sleep(1200);
  ok('"Send him home": he goes', (await cnt(FROG)) === 0);
  ok('...his sword saved with him', /iron_sword/.test((await run(`data get storage bm:fol fg.p${pid}`))));
  await tokenUse('frog_signet');
  ok('use the Signet: he comes back - with his sword', await wait(3000, async () => (await cnt(FROG)) === 1) && /iron_sword/.test(await nbt(FROG, 'equipment.mainhand.id')));
  await at(X + 6.5, Y + 1, Z - 4.5, 0, 10);
  await tokenUse('frog_signet');
  ok('use it while he\'s out: he comes to your side', await wait(2500, async () => (await cnt(`${FROG.replace(']', `,x=${X + 6.5},y=${Y + 1},z=${Z - 4.5},distance=..2.5]`)}`)) === 1));

  // ---------------------------------------------------------------- he faints: the Signet rests, nothing is dropped, he's back with his sword after
  await run(`${O}kill ${FROG}`);
  ok('he faints: the Signet rests (5 minutes)', await wait(4000, async () => (await sc('TestRat', 'bm.fgcd')) > 250));
  ok('...and nothing he wore is left lying about', (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20,nbt={Item:{id:"minecraft:iron_sword"}}]`)) === 0);
  A.titles && (A.titles.length = 0); A.bars && (A.bars.length = 0);
  await tokenUse('frog_signet');
  ok('use the Signet while he rests: not yet', (await cnt(FROG)) === 0);
  await run('scoreboard players set TestRat bm.fgcd 1'); await sleep(2200);
  await tokenUse('frog_signet');
  ok('...rested: he\'s back, sword and all', await wait(3000, async () => (await cnt(FROG)) === 1) && /iron_sword/.test(await nbt(FROG, 'equipment.mainhand.id')));

  // ---------------------------------------------------------------- his gear handed back from the menu - and no copy left with him
  await tokenUse('frog_signet', true);
  await A.press(/Hand back my gear/); await sleep(1500);
  ok('"Hand back my gear": the sword comes back to you', await wait(3000, async () => (await vanilla('TestRat', 'iron_sword')) === 1) && !/iron_sword/.test(await nbt(FROG, 'equipment')));
  await sleep(1300);
  await tokenUse('frog_signet', true); await A.press(/Send him home/); await sleep(1200);
  await tokenUse('frog_signet');
  ok('...sent home and called again: no sword appears from nowhere', await wait(3000, async () => (await cnt(FROG)) === 1) && !/iron_sword/.test(await nbt(FROG, 'equipment')) &&
     (await vanilla('TestRat', 'iron_sword')) === 1);

  // ---------------------------------------------------------------- Donado's pen: free him, and he hands over his Collar Tag
  await at(X + 0.5, Y + 1, Z + 0.5, 90, 10);
  await run(`${O}execute positioned ${X - 3.5} ${Y + 1} ${Z + 0.5} rotated -90 0 run function bm:npc/donado_pen`); await sleep(800);
  const pen = await entOf(A, `@e[type=minecraft:interaction,tag=bm.don_hire,x=${X - 3.5},y=${Y + 1},z=${Z + 0.5},distance=..2,limit=1]`);
  A.slot(8); await sleep(200);
  if (pen) A.interact(pen.entityId); await sleep(1500);
  ok('freeing Donado hands you his Collar Tag - and he joins you', (await has('TestRat', 'donado_tag')) === 1 && await wait(3000, async () => (await cnt(DON)) === 1));
  ok('...and his cell stands empty for a while', (await sc(`@e[type=minecraft:item_display,tag=bm.don_pen,x=${X - 3.5},y=${Y + 1},z=${Z + 0.5},distance=..2,limit=1]`, 'bm.dng')) > 0);

  // ---------------------------------------------------------------- the three-follower limit counts Donado now
  await run('loot give TestRat loot bm:items/cecil_gem'); await sleep(300);
  await tokenUse('cecil_gem');
  ok('the Frog, Donado and Cecil: three with you', await wait(3000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.cecilpet,scores={bm.pid=${pid}}]`)) === 1));
  await run('loot give TestRat loot bm:items/leo_crest'); await run('scoreboard players set TestRat bm.lecd 0');
  await tokenUse('leo_crest');
  ok('...a fourth is refused (Donado counts)', (await cnt(`@e[type=minecraft:wolf,tag=bm.leopet,scores={bm.pid=${pid}}]`)) === 0);
  await run(`${O}execute as @e[type=minecraft:wolf,tag=bm.cecilpet,scores={bm.pid=${pid}}] at @s run function bm:p62/cecil_go`);

  // ---------------------------------------------------------------- the Signet in a display case: a little Frog
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 70);
  await run('item replace entity TestRat hotbar.0 with minecraft:air');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/display_case_oak');
  A.slot(0); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(500);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  const box = await entOf(A, caseSel);
  const ss = await slotOf('frog_signet'); A.slot(ss); await sleep(300);
  if (box) A.interact(box.entityId); await sleep(1200);
  ok('the Signet in a display case: a little Frog stands on the cushion', (await cnt('@e[type=minecraft:item_display,tag=bm.dcfg]')) >= 4);
  A.slot(8); await sleep(250); if (box) A.interact(box.entityId); await sleep(1200);
  ok('...empty-handed, the Signet comes back out (and the figurine goes)', (await has('TestRat', 'frog_signet')) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.dcfg]')) === 0);

  // ---------------------------------------------------------------- Donado's tag in an item frame: he comes out of it (nobody's - not yours)
  await run(`${O}fill ${X + 2} ${Y + 1} ${Z + 5} ${X + 2} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X + 2} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t142f"]}`); await sleep(400);
  const fr = await entOf(A, `@e[type=minecraft:item_frame,tag=bm.t142f,limit=1]`);
  await at(X + 2.5, Y + 1, Z + 2.5, 0, -10);
  const ds = await slotOf('donado_tag'); A.slot(ds); await sleep(300);
  if (fr) A.interact(fr.entityId); await sleep(2600);
  ok('Donado\'s tag in an item frame: a Donado climbs out of it', (await cnt(`@e[type=minecraft:wolf,tag=bm.donado,tag=bm.ffpet,x=${X + 2},y=${Y + 2},z=${Z + 4},distance=..8]`)) === 1);
  ok('...he isn\'t yours (your own Donado still at your side)', (await cnt(DON)) === 1);
  await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t142f]`); await sleep(2500);
  ok('...the frame gone: so is he', (await cnt(`@e[type=minecraft:wolf,tag=bm.donado,tag=bm.ffpet]`)) === 0);

  // ---------------------------------------------------------------- you die: they fade with you
  await run('effect clear TestRat'); await run('kill TestRat'); await sleep(2500);   // (resistance V would shrug off any damage)
  ok('you die: the Frog and Donado fade with you', (await cnt(FROG)) === 0 && (await cnt(DON)) === 0);
  await sleep(1500); A.stand(); await run('effect give TestRat minecraft:resistance 900 4 true');

  // ---------------------------------------------------------------- a Frog from before (no token): he hands over his Signet instead of going home
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`);   // (what the bot dropped when it died)
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);
  await run('clear TestRat *[minecraft:custom_data~{bm:"frog_signet"}]');
  ok('(no Signet in the bot\'s pack)', (await has('TestRat', 'frog_signet')) === 0);
  await run(`${O}execute as TestRat at TestRat run function bm:p136/fg/fspawn`); await run(`${O}tag ${FROG.replace(',limit=1', '')} remove bm.f136`);
  ok('a Frog from before (no token yet) at the bot\'s side', (await cnt(FROG.replace(',limit=1', ''))) === 1);
  ok('...within a few seconds he hands you his Signet - and stays', await wait(5000, async () => (await has('TestRat', 'frog_signet')) === 1 &&
     (await cnt(FROG.replace('limit=1', 'tag=bm.f136'))) === 1), `signets ${await has('TestRat', 'frog_signet')} tags ${await nbt(FROG, 'Tags')}`);
  await sleep(4000);
  ok('...and he\'s still with you a few seconds on (just the one)', (await cnt(FROG.replace(',limit=1', ''))) === 1);

  // ---- another from before turning up while he's out: one Frog only - the old one leaves the gear he wore on the ground
  await run(`${O}execute as TestRat at TestRat positioned ~2 ~ ~ run function bm:p136/fg/fspawn`);
  const OLD = `@e[type=minecraft:wolf,tag=bm.frogpet,tag=!bm.f136,scores={bm.pid=${pid}}]`;
  await run(`${O}item replace entity ${OLD} weapon.mainhand with minecraft:golden_sword`);
  ok('a second, older Frog turns up (no token-era tag; a golden sword)', (await cnt(OLD)) === 1);
  ok('...he goes home: one Frog with you', await wait(4000, async () => (await cnt(OLD)) === 0 && (await cnt(FROG.replace(',limit=1', ''))) === 1));
  ok('...and his golden sword is on the ground, not lost', (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20,nbt={Item:{id:"minecraft:golden_sword"}}]`)) === 1);
  ok('...nor copied onto the one with you', !/golden_sword/.test(await nbt(FROG, 'equipment')));

  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.frogpet]`);
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.donado]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
