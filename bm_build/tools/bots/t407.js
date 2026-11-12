// 3.1v: THE FIFTY (phase281), as a regular (non-op) player - the monument to every follower of the Compass of Bonds.
// Earned with the compass (rcon sets the stage: the compass's tag, bm.kbcomp, without the monument's): it arrives once, with a word.
// Used without sneaking: a hint. Sneak + use with a block in its way: refused, kept. Sneak + use on open ground: three tiers, fifty
// dolls (every one a different follower, each facing out), the compass on top, the plaque on the side facing you; the item is spent.
// A second one set down within 9 blocks: refused. Right-click: a word. A plain punch: a hint, it stays. Sneak + punch: back in the
// pack, every part gone.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const uuidOf = async sel => { const m = (await run(`data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async sel => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const has = async iid => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const count = async sel => +(((await run(`execute store result score #t407 bm.rng if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const X = 5200, Y = 100, Z = 5000;
  const near = `x=${X},y=${Y},z=${Z},distance=..20`;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  // ---- the stage: a stone floor with open air over it; TestRat holds the compass's tag but not the monument's
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 3.5} 0 25`); await sleep(1500);
  await run(`kill @e[tag=bm.f50d,${near}]`); await run(`kill @e[tag=bm.f50,${near}]`); await run(`kill @e[tag=bm.f50m,${near}]`);
  await run(`fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`); await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} minecraft:air`);
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 300 4 true');
  await run('tag TestRat remove bm.f50got'); await run('tag TestRat add bm.kbcomp');
  A.chats.length = 0;
  ok('earned: with the compass, The Fifty arrives in the pack', await wait(5000, async () => (await has('fifty_monument')) === 1), `${await has('fifty_monument')}`);
  ok('...with a word', A.chats.some(c => /The Fifty/.test(c)), A.chats.join(' | ').slice(0, 200));
  await sleep(2500);
  ok('...once (not again the next second)', (await has('fifty_monument')) === 1);
  await run('item replace entity TestRat hotbar.0 with minecraft:air');
  await run(`clear TestRat *[minecraft:custom_data~{bm:"fifty_monument"}]`); await run('loot replace entity TestRat hotbar.0 loot bm:items/fifty_monument'); A.slot(0); await sleep(400);
  // ---- not sneaking: a hint
  A.bars.length = 0; A.use(); await sleep(500); A.release(); await sleep(500);
  ok('used without sneaking: "Sneak + use..."', A.bars.some(b => /Sneak \+ use/.test(b)), A.bars.join(' | '));
  // ---- in the way: a block inside its 5 x 5
  await run(`setblock ${X + 2} ${Y + 1} ${Z + 1} minecraft:oak_planks`);
  const placeAt = async () => { A.bars.length = 0; A.input({ shift: true }); await sleep(300); A.useOn(X, Y - 1, Z, 1); A.use(); await sleep(600); A.release(); A.input({}); await sleep(600); };
  await placeAt();
  ok('a block in its space: refused ("a clear space")', A.bars.some(b => /clear space/.test(b)), A.bars.join(' | '));
  ok('...and kept', (await has('fifty_monument')) === 1);
  await run(`setblock ${X + 2} ${Y + 1} ${Z + 1} minecraft:air`);
  // ---- set up
  await placeAt();
  ok('sneak + use on open ground: "The Fifty stands"', A.bars.some(b => /The Fifty stands/.test(b)), A.bars.join(' | '));
  ok('...the item is spent', (await has('fifty_monument')) === 0);
  const nd = await count(`@e[type=minecraft:item_display,tag=bm.f50d,${near}]`), nb = await count(`@e[type=minecraft:block_display,tag=bm.f50d,${near}]`);
  ok('...51 item displays (fifty dolls and the compass)', nd === 51, `${nd}`);
  ok('...seven blocks (three tiers, three lips, the stand)', nb === 7, `${nb}`);
  ok('...a click box and a marker', (await count(`@e[type=minecraft:interaction,tag=bm.f50,${near}]`)) === 1 && (await count(`@e[type=minecraft:marker,tag=bm.f50m,${near}]`)) === 1);
  // every doll a different follower, every one facing out
  const seen = new Set(); let out = 0, dolls = 0;
  for (let i = 0; i < 51; i++) {
    const sel = `@e[type=minecraft:item_display,tag=bm.f50d,tag=!bm.f50c,tag=!t407,${near},limit=1]`;
    const mdl = (await run(`data get entity ${sel} item.components."minecraft:item_model"`)).replace(/.*data: /, '');
    if (!/"/.test(mdl)) break;
    const pos = (await run(`data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    const yaw = +((await run(`data get entity ${sel} Rotation[0]`)).match(/(-?[\d.]+)f?\s*$/) || [0, NaN])[1];
    const dx = pos[0] - (X + 0.5), dz = pos[2] - (Z + 0.5), fx = -Math.sin(yaw * Math.PI / 180), fz = Math.cos(yaw * Math.PI / 180);
    if (fx * dx + fz * dz > 0) out++;
    seen.add(mdl); dolls++; await run(`tag ${sel} add t407`);
  }
  await run(`tag @e[tag=t407] remove t407`);
  ok('...fifty dolls, every one a different follower', dolls === 50 && seen.size === 50, `${dolls} dolls, ${seen.size} models`);
  ok('...every doll facing out', out === 50, `${out}/50`);
  const pz = (await run(`data get entity @e[type=minecraft:text_display,tag=bm.f50d,${near},limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  ok('...the plaque on the side facing you (north: you stood north of it, facing south)', pz && +pz[3] < Z, pz ? pz[0] : 'no plaque');
  // ---- a second one too close
  await run('loot replace entity TestRat hotbar.1 loot bm:items/fifty_monument'); A.slot(1); await sleep(300);
  await run(`tp TestRat ${X + 7.5} ${Y} ${Z - 3.5} 0 25`); await sleep(1200);
  A.bars.length = 0; A.input({ shift: true }); await sleep(300); A.useOn(X + 7, Y - 1, Z, 1); A.use(); await sleep(600); A.release(); A.input({}); await sleep(600);
  ok('a second one 7 blocks off: refused ("too close")', A.bars.some(b => /too close/.test(b)), A.bars.join(' | '));
  ok('...and kept', (await has('fifty_monument')) === 1);
  await run(`clear TestRat *[minecraft:custom_data~{bm:"fifty_monument"}]`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 3.5} 0 30`); await sleep(1200); A.slot(0);
  // ---- right-click; a plain punch; sneak + punch
  const hb = await entOf(`@e[type=minecraft:interaction,tag=bm.f50,${near},limit=1]`);
  ok('the click box is in view', !!hb);
  if (hb) {
    A.bars.length = 0; A.interact(hb.entityId); await sleep(1200);
    ok('right-click: "Fifty friends - every one of them yours."', A.bars.some(b => /Fifty friends/.test(b)), A.bars.join(' | '));
    A.bars.length = 0; A.attack(hb.entityId); await sleep(1200);
    ok('a plain punch: "Sneak + punch to take The Fifty down." - and it stays', A.bars.some(b => /Sneak \+ punch/.test(b)) && (await count(`@e[type=minecraft:item_display,tag=bm.f50d,${near}]`)) === 51,
       A.bars.join(' | '));
    A.bars.length = 0; A.input({ shift: true }); await sleep(300); A.attack(hb.entityId); await sleep(1200); A.input({}); await sleep(300);
    ok('sneak + punch: back in the pack', (await has('fifty_monument')) === 1, A.bars.join(' | '));
    ok('...every part gone', (await count(`@e[tag=bm.f50d,${near}]`)) + (await count(`@e[tag=bm.f50,${near}]`)) + (await count(`@e[tag=bm.f50m,${near}]`)) === 0);
  }
  await run('clear TestRat'); await run('effect clear TestRat'); await run('tag TestRat remove bm.kbcomp');   // (the compass's tag would have the sky island woven)
  A.end(); R.end();
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
