// 3.0e: THE ARMADA IN THE SKY, as a regular (non-op) player. The fleet moved up (p2/armadacfg.ORIGIN, read by armada_cfg.js) so
// no island is cut away; a world's 3.0 copy (2560 24 -3328, the same x/z, low among the islands) comes down first, once.
//   move     a 3.0 world staged by rcon: its copy placed at the 3.0 site, the scores 3.0 left (#aver 5, #p241_old 1, no 3.0e
//            flag), the new site empty, TestRat aboard the old copy (signalled from 1200 90 0): the fleet wanted - TestRat is
//            carried out to where he signalled from; the old copy gone (no marker, every sampled hull block air, its biome
//            the End's again); the new one placed (#aver, the Dock's marker at its new height); its flag set - and it stays
//            gone (a second placing doesn't touch the 3.0 site again)
//   clear    the new volume holds the fleet and nothing else: per 32-block cube, end stone exactly the template's count, and no
//            chorus, end stone bricks, obsidian, bedrock or gateway (an island's or an End City's) anywhere in it
//   arrive   the Hive-Star Coordinates used out past the main island: lifted, then set down ON THE DOCK at its new height
//   fall     stepped off a deck into the open sky and falling (the bot's own moves, ~4 blocks a tick): caught before
//            y < the fleet's underside - 10, set back where you last stood, hurt
//   node t334.js [move|clear|arrive|fall]
const fs = require('fs'), path = require('path');
const nbt = require('prismarine-nbt');
const { bot, rcon, sleep } = require('./lib_resp');
const { AO, AS, OLD, CATCH_LOW, W } = require('./armada_cfg');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OUT = process.env.BM_OUT || path.join(__dirname, '..', '..', 'out_p2');
const AVER = +fs.readFileSync(path.join(__dirname, '..', '..', 'phase241.py'), 'utf8').match(/^AVER = (\d+)/m)[1];
const E = 'execute in minecraft:the_end run ', END = 'minecraft:the_end';
const box = (o, s) => `x=${o[0]},y=${o[1]},z=${o[2]},dx=${s[0] - 1},dy=${s[1] - 1},dz=${s[2] - 1}`;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${E}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const hp = async () => +(((await run('data get entity TestRat Health')).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
  const cubes = (o, s) => { const L = []; for (let x = 0; x < s[0]; x += 32) for (let y = 0; y < s[1]; y += 32) for (let z = 0; z < s[2]; z += 32)
    L.push([o[0] + x, o[1] + y, o[2] + z, o[0] + Math.min(s[0], x + 32) - 1, o[1] + Math.min(s[1], y + 32) - 1, o[2] + Math.min(s[2], z + 32) - 1]); return L; };
  const quarters = (o, s) => { const mx = o[0] + s[0] / 2, mz = o[2] + s[2] / 2;
    return [[o[0] - 8, mx], [mx + 1, o[0] + s[0] + 8]].flatMap(([a, c]) => [[o[2] - 8, mz], [mz + 1, o[2] + s[2] + 8]].map(([b, e]) => `${a} ${b} ${c} ${e}`)); };
  const loadBox = async (o, s) => { for (const q of quarters(o, s)) await run(`${E}forceload add ${q}`);
    await wait(30000, async () => /passed/i.test(await run(`${E}execute if loaded ${o[0]} ${o[1]} ${o[2]} if loaded ${o[0] + s[0] - 1} ${o[1]} ${o[2] + s[2] - 1} if loaded ${o[0]} ${o[1]} ${o[2] + s[2] - 1} if loaded ${o[0] + s[0] - 1} ${o[1]} ${o[2]}`)), 500); await sleep(3000); };

  // ---- the template, as built: its blocks (local), the end stone in each 32-cube, the columns it fills
  const st = nbt.simplify((await nbt.parse(fs.readFileSync(path.join(OUT, 'BlackMarket_DP', 'data', 'bm', 'structure', 'p2_armada.nbt')))).parsed);
  const solid = st.blocks.filter(b => !/:(cave_|void_)?air$/.test(st.palette[b.state].Name));
  const under = AO[1] + solid.reduce((m, b) => Math.min(m, b.pos[1]), 1e9);
  const esIn = (c) => solid.filter(b => st.palette[b.state].Name === 'minecraft:end_stone' && b.pos[0] + AO[0] >= c[0] && b.pos[0] + AO[0] <= c[3] &&
                                    b.pos[1] + AO[1] >= c[1] && b.pos[1] + AO[1] <= c[4] && b.pos[2] + AO[2] >= c[2] && b.pos[2] + AO[2] <= c[5]).length;
  console.log(`(the fleet: ${solid.length} blocks, its underside y ${under}, the volume y ${AO[1]}..${AO[1] + AS[1] - 1}; the catch from ${under - 2} down to ${CATCH_LOW})`);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 3 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #hard bm.cfg 1');
  const outside = async () => { await run(`${E}setblock 1200 88 0 minecraft:obsidian`); await run(`${E}tp TestRat 1200.5 89 0.5`); await sleep(1500); };
  await outside();

  if (on('move')) {
    const O = OLD.s30, OB = box(O, AS);
    // (the stage: a 3.0 world - its copy at the 3.0 site, the new site empty, the scores 3.0 left behind)
    await run('scoreboard players set #awant bm.p2 0'); await sleep(1500);
    await loadBox(AO, AS);
    await run(`${E}kill @e[type=!minecraft:player,${box(AO, AS)}]`);
    for (const c of cubes(AO, AS)) await run(`${E}fill ${c.join(' ')} minecraft:air`);
    await loadBox(O, AS);
    await run(`${E}kill @e[type=!minecraft:player,${OB}]`);
    await run('scoreboard players set #aver bm.p2 5'); await run('scoreboard players set #p241_old bm.p2 1'); await run('scoreboard players set #acol bm.p2 0');
    for (const f of ['#p241_o30', '#p241_o30w', '#asite', '#await']) await run(`scoreboard players reset ${f} bm.p2`);
    const pl = await run(`${E}place template bm:p2_armada ${O.join(' ')}`);
    ok('the stage: a 3.0 copy placed at the 3.0 site (2560 24 -3328)', /placed/i.test(pl) && (await cnt(`@e[type=minecraft:marker,tag=bm.d_armada,${OB}]`)) > 50, pl);
    const odock = [O[0] + 111, O[1] + 50, O[2] + 206];
    await run(`${E}tp TestRat ${odock[0]}.5 ${odock[1]} ${odock[2]}.5`); await sleep(2500);
    await run('scoreboard players set TestRat bm.aox 1200'); await run('scoreboard players set TestRat bm.aoy 89'); await run('scoreboard players set TestRat bm.aoz 0');
    ok('...TestRat aboard the old copy, on its Dock', A.pos && Math.abs(A.pos.y - odock[1]) < 2, A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    for (const q of quarters(AO, AS).concat(quarters(O, AS))) await run(`${E}forceload remove ${q}`);     // (the pack's own forceloads from here)
    await run('scoreboard players set #awant bm.p2 1');
    ok('the fleet wanted: TestRat is carried out to where he signalled from', await wait(60000, async () => A.pos && Math.abs(A.pos.x - 1200.5) < 2 && Math.abs(A.pos.z - 0.5) < 2, 500),
       A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...the 3.0 site\'s teardown flagged done (#p241_o30)', await wait(30000, async () => (await sc('#p241_o30', 'bm.p2')) === 1, 500));
    ok('...and the new one placed (#aver at the build\'s version)', await wait(900000, async () => (await sc('#aver', 'bm.p2')) === AVER, 2000), String(await sc('#aver', 'bm.p2')));
    await loadBox(O, AS);
    ok('the old copy: no marker of it left', (await cnt(`@e[type=minecraft:marker,tag=bm.d_armada,${OB}]`)) === 0);
    const smp = solid.filter((b, i) => i % Math.ceil(solid.length / 400) === 0);
    let left = [];
    for (const b of smp) { const p = [O[0] + b.pos[0], O[1] + b.pos[1], O[2] + b.pos[2]]; if (!/passed/i.test(await run(`${E}execute if block ${p.join(' ')} minecraft:air`))) left.push(p.join(' ')); }
    ok(`the old copy: ${smp.length} of its hull blocks sampled - every one back to the void's air`, left.length === 0, left.slice(0, 5).join(' | '));
    ok('the old copy: its biome the End\'s again (small_end_islands at a corner and the middle)',
       /passed/i.test(await run(`${E}execute if biome ${O[0]} ${O[1]} ${O[2]} minecraft:small_end_islands`)) && /passed/i.test(await run(`${E}execute if biome ${O[0] + 120} ${O[1] + 48} ${O[2] + 120} minecraft:small_end_islands`)));
    await loadBox(AO, AS);
    const dk = W(111, 50, 206);
    ok(`the new one: the Dock's marker at its new height (y ${dk[1]})`, (await cnt(`@e[type=minecraft:marker,tag=bm.adock,x=${dk[0]},y=${dk[1]},z=${dk[2]},distance=..2]`)) === 1);
    ok('the new one: placed in the sky (#asite)', (await sc('#asite', 'bm.p2')) === AO[1]);
    // (placed again - an admin's /place: the 3.0 site is never touched again)
    await run(`${E}setblock ${O[0] + 120} ${O[1] + 10} ${O[2] + 120} minecraft:glass`);
    await run('function bm:admin/armada/place');
    ok('placed again (admin): the new one back', await wait(900000, async () => (await sc('#aver', 'bm.p2')) === AVER, 2000));
    await loadBox(O, AS);
    ok('...and the 3.0 site untouched this time (a block set there since: still there)', /passed/i.test(await run(`${E}execute if block ${O[0] + 120} ${O[1] + 10} ${O[2] + 120} minecraft:glass`)));
    await run(`${E}setblock ${O[0] + 120} ${O[1] + 10} ${O[2] + 120} minecraft:air`);
  }

  if (on('clear')) {
    if ((await sc('#aver', 'bm.p2')) !== AVER) { await run('function bm:admin/armada/place'); await wait(900000, async () => (await sc('#aver', 'bm.p2')) === AVER, 2000); }
    await loadBox(AO, AS);
    const SW = 'minecraft:wet_sponge';      // (in no fleet and no island: each kind swapped to it and back, counted)
    const count = async (c, b) => { const m = (await run(`${E}fill ${c.join(' ')} ${SW} replace ${b}`)).match(/filled (\d+)/i); const n = m ? +m[1] : 0;
      if (n) await run(`${E}fill ${c.join(' ')} ${b} replace ${SW}`); return n; };
    const bad = [], foreign = {};
    for (const c of cubes(AO, AS)) {
      const n = await count(c, 'minecraft:end_stone'), want = esIn(c);
      if (n !== want) bad.push(`${c.slice(0, 3).join(' ')}: ${n} (template ${want})`);
      for (const b of ['chorus_plant', 'chorus_flower', 'end_stone_bricks', 'obsidian', 'bedrock', 'end_gateway']) { const k = await count(c, 'minecraft:' + b); if (k) foreign[b] = (foreign[b] || 0) + k; }
    }
    ok(`the new volume (y ${AO[1]}..${AO[1] + AS[1] - 1}): end stone exactly the fleet's own in all ${cubes(AO, AS).length} cubes`, bad.length === 0, bad.slice(0, 4).join(' | '));
    ok('...and no island or End City block in it (chorus, end stone bricks, obsidian, bedrock, a gateway)', Object.keys(foreign).length === 0, JSON.stringify(foreign));
  }

  if (on('arrive')) {
    if ((await sc('#aver', 'bm.p2')) !== AVER) { await run('function bm:admin/armada/place'); await wait(900000, async () => (await sc('#aver', 'bm.p2')) === AVER, 2000); }
    await outside();
    await run('scoreboard players reset TestRat bm.aoy'); await run('loot replace entity TestRat hotbar.0 loot bm:items/hive_coords'); await sleep(500);
    A.titles.length = 0; A.bars.length = 0;
    A.slot(0); await sleep(300); A.use(); await sleep(2200); A.release();
    const dock = W(111, 50, 206);
    ok(`the Coordinates used: set down on the Dock at its new height (${dock.join(' ')})`, await wait(14000, async () => A.pos && Math.abs(A.pos.x - dock[0] - 0.5) < 1.5 && Math.abs(A.pos.z - dock[2] - 0.5) < 1.5 && Math.abs(A.pos.y - dock[1]) < 1.5, 500),
       A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...standing on the deck (the block under the feet is the Dock\'s)', !/passed/i.test(await run(`${E}execute if block ${dock[0]} ${dock[1] - 1} ${dock[2]} minecraft:air`)));
    ok('...THE VORN ARMADA (its title)', A.titles.some(t => /VORN ARMADA/.test(JSON.stringify(t))));
    await sleep(3000);
  }

  if (on('fall')) {
    if ((await sc('#aver', 'bm.p2')) !== AVER) { await run('function bm:admin/armada/place'); await wait(900000, async () => (await sc('#aver', 'bm.p2')) === AVER, 2000); }
    await loadBox(AO, AS);
    // (a column of open sky near the Dock: no fleet block in it, none within 3)
    const cols = new Set(solid.map(b => `${b.pos[0]},${b.pos[2]}`));
    const free = (x, z) => { for (let dx = -3; dx <= 3; dx++) for (let dz = -3; dz <= 3; dz++) if (cols.has(`${x + dx},${z + dz}`)) return false; return true; };
    let col = null;
    for (let r = 1; r < 80 && !col; r++) for (let dx = -r; dx <= r && !col; dx++) for (const dz of [-r, r]) if (!col && free(140 + dx, 206 + dz)) col = [140 + dx, 206 + dz];
    const deck = W(140, 50, 206);
    await run(`${E}tp TestRat ${deck[0]}.5 ${deck[1]} ${deck[2]}.5`); await sleep(3000);      // (stood on the deck: where he last stood)
    const mark = [await sc('TestRat', 'bm.asx'), await sc('TestRat', 'bm.asy'), await sc('TestRat', 'bm.asz')];
    ok('stood on a deck: the fleet marks where he last stood', mark[1] === deck[1] && mark[0] === deck[0], mark.join(' '));
    await run('effect clear TestRat minecraft:resistance'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(600); const h0 = await hp();
    const sky = W(col[0], 50, col[1]);
    A.unstand(); A.ground(false); await sleep(100);      // (off the ground before the step: never marked standing in the sky)
    const tp0 = A.pos.teleportId;
    await run(`${E}tp TestRat ${sky[0]}.5 ${sky[1]} ${sky[2]}.5`);
    await wait(3000, async () => A.pos.teleportId !== tp0, 50);
    // (falling as a client does: gravity 0.08, drag 0.98, a move a tick - over 3.9 a tick long before the underside)
    const tp1 = A.pos.teleportId; let vy = 0, y = A.pos.y, minY = y;
    for (let t = 0; t < 400 && A.pos.teleportId === tp1; t++) {
      vy = (vy - 0.08) * 0.98; y += vy; minY = Math.min(minY, y);
      A.write('position', { x: A.pos.x, y, z: A.pos.z, flags: { onGround: false, hasHorizontalCollision: false } }); A.write('tick_end', {});
      if (y < CATCH_LOW - 40) break;
      await sleep(50);
    }
    const caught = A.pos.teleportId !== tp1;
    A.stand(); await sleep(1500);
    ok(`fallen off into the sky (from y ${sky[1]}, open sky to y ${under - 1}): caught at y ${minY.toFixed(1)} - before y < ${under - 10} (the underside - 10)`, caught && minY >= under - 10, `caught ${caught}, lowest ${minY.toFixed(1)}, speed ${(-vy).toFixed(2)} a tick`);
    ok('...set back where he last stood', A.pos && Math.abs(A.pos.x - deck[0] - 0.5) < 1.5 && Math.abs(A.pos.z - deck[2] - 0.5) < 1.5 && Math.abs(A.pos.y - deck[1]) < 1.5,
       A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...hurt by the drop', (await hp()) < h0, `${h0} -> ${await hp()}`);
    await run('effect give TestRat minecraft:resistance infinite 3 true');
  }

  await outside();
  await run('effect clear TestRat'); await run('clear TestRat'); await run('tag TestRat remove bm.lkpass');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
