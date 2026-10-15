// 2.80: THE ROAMING BOSSES, STAGED - as a regular (non-op) player, each boss called with its own summon item (rcon only sets
// the stage: the arena, the hour, the items in hand, a boss's health brought down to a threshold). For each of the six:
// it ARRIVES frozen (no AI, invulnerable - a hit during it does nothing) in its own way (the Horseman's steed far off and
// galloping in; the Pharaoh and the Treant out of the ground and growing; the Roc out of the sky; the Colossus out of the
// floor; the Voidwalker tiny, out of a rift), then its title card is on the player's screen, its song starts (the player is
// marked as having sensed it), and it is released and armed: its bar reads its true health. Brought below its rage line it
// FREEZES for its rage moment (the rage line on screen), then rages. A wind-up (the Colossus's slam, the Pharaoh's
// sandblast): the boss charges first (squatting, for the Colossus), then strikes and is itself again. Brought down by the
// player's own sword it DIES as a sequence - frozen, the bar gone, still there seconds later - then falls as the player's
// kill: its relic on the ground. The Horseman's head tumbles and his steed goes with him; the Pharaoh sinks; the Treant
// leaves a sapling; the Colossus still bursts into Magma Spawn (awake, visible).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ', N = 'execute in minecraft:the_nether run ', E = 'execute in minecraft:the_end run ';
  const cnt = async (sel, d = O) => { const m = (await run(`${d}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => { const r = await run(cmd); const m = r.match(/has (-?\d+) \[/) || r.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/); return m ? +m[1] : NaN; };
  const P = async (cmd) => { const m = (await run(cmd)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : [NaN, NaN, NaN]; };
  const flat2 = (a, b) => Math.hypot(a[0] - b[0], a[2] - b[2]);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const eidOf = async (sel, d) => { const m = (await run(`${d}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const give = async (iid, slot = 0) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); await sleep(150); };
  // kind: entity, summon item, relic, rage line (real hp), its rage tag, bar id, max health, sensed tag, dimension
  const K = {
    hhm: ['wither_skeleton', 'sum_horseman', 'horseman_head', 180, 'bm.hh_rage', 'bm:hhm', 360, 'bm.hhsensed', O, 'THE HEADLESS HORSEMAN', 'The Horseman rages'],
    sph: ['husk', 'sum_pharaoh', 'pharaoh_crook', 160, 'bm.sph_rage', 'bm:sph', 320, 'bm.sphsensed', O, 'THE SAND PHARAOH', 'The sandstorm thickens'],
    roc: ['phantom', 'sum_roc', 'storm_talon', 130, 'bm.roc_rage', 'bm:roc', 260, 'bm.rocsensed', O, 'THE STORM ROC', 'The storm breaks'],
    trt: ['creaking', 'sum_treant', 'heartwood_branch', 170, 'bm.trt_rage', 'bm:trt', 340, 'bm.trtsensed', O, 'THE ELDER TREANT', 'The forest rises'],
    mcol: ['magma_cube', 'sum_colossus', 'molten_gauntlet', 210, 'bm.mcol_rage', 'bm:mcol', 420, 'bm.mcolsensed', N, 'THE MAGMA COLOSSUS', 'It boils over'],
    vwk: ['enderman', 'sum_voidwalker', 'void_scepter', 225, 'bm.vwk_rage', 'bm:vwk', 450, 'bm.vwksensed', E, 'THE VOIDWALKER', 'The stars go out'],
  };
  const sel = (k, x = '') => `@e[type=minecraft:${K[k][0]},tag=bm.${k}${x},limit=1]`;
  const tags = async (k) => (await run(`${K[k][8]}data get entity ${sel(k)} Tags`));
  const hp = async (k) => num(`${K[k][8]}data get entity ${sel(k)} Health`);
  const buf = async (k) => num(`${K[k][8]}scoreboard players get ${sel(k)} bm.cbuf`);
  const posY = async (k) => num(`${K[k][8]}data get entity ${sel(k)} Pos[1]`);
  const scale = async (k) => num(`${K[k][8]}attribute ${sel(k)} minecraft:scale base get`);
  const setReal = async (k, real) => { const b = await buf(k); await run(`${K[k][8]}data modify entity ${sel(k)} Health set value ${b + real}f`); };
  const near = async (d, x, y, z) => { await run(`${d}tp TestRat ${x + 0.5} ${y} ${z + 0.5} 0 0`); await sleep(400); };

  // the stages: a grass platform high over the Overworld, a hall in the Nether, an end-stone floor in the End
  const X = 17800, Y = 150, Z = 16000;
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}fill ${X - 36} ${Y} ${Z - 36} ${X + 36} ${Y} ${Z + 36} minecraft:grass_block`);
  for (let y = Y + 1; y <= Y + 40; y += 8) await run(`${O}fill ${X - 36} ${y} ${Z - 36} ${X + 36} ${Math.min(y + 7, Y + 40)} ${Z + 36} minecraft:air`);
  for (let y = Y - 12; y < Y; y += 6) await run(`${O}fill ${X - 36} ${y} ${Z - 36} ${X + 36} ${y + 5} ${Z + 36} minecraft:air`);
  const NX = 3000, NY = 100, NZ = 3000;
  await run(`${N}forceload add ${NX - 30} ${NZ - 30} ${NX + 30} ${NZ + 30}`);
  await run(`${N}fill ${NX - 28} ${NY - 1} ${NZ - 28} ${NX + 28} ${NY - 1} ${NZ + 28} minecraft:netherrack`);
  await run(`${N}fill ${NX - 28} ${NY} ${NZ - 28} ${NX + 28} ${NY + 8} ${NZ + 28} minecraft:air`);
  await run(`${N}fill ${NX - 28} ${NY - 10} ${NZ - 28} ${NX + 28} ${NY - 2} ${NZ + 28} minecraft:air`);
  await run(`${N}fill ${NX - 28} ${NY + 9} ${NZ - 28} ${NX + 28} ${NY + 9} ${NZ + 28} minecraft:netherrack`);
  const EX = 1000, EY = 100, EZ = 1000;
  await run(`${E}forceload add ${EX - 30} ${EZ - 30} ${EX + 30} ${EZ + 30}`);
  await run(`${E}fill ${EX - 28} ${EY - 1} ${EZ - 28} ${EX + 28} ${EY - 1} ${EZ + 28} minecraft:end_stone`);
  await run(`${E}fill ${EX - 28} ${EY} ${EZ - 28} ${EX + 28} ${EY + 10} ${EZ + 28} minecraft:air`);
  const STAGE = { [O]: [X, Y + 1, Z], [N]: [NX, NY, NZ], [E]: [EX, EY, EZ] };
  for (const k of Object.keys(K)) await run(`${K[k][8]}kill @e[type=minecraft:${K[k][0]},tag=bm.${k}]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000'); await run('weather clear');
  for (const e of ['resistance 1200 4', 'fire_resistance 1200 0', 'regeneration 1200 3', 'saturation 1200 0', 'water_breathing 1200 0']) await run(`effect give TestRat minecraft:${e} true`);

  for (const k of ['hhm', 'sph', 'roc', 'trt', 'mcol', 'vwk']) {
    const [ent, item, relic, rageAt, rageTag, bar, maxHp, sensed, d, title, rageLine] = K[k];
    const [sx, sy, sz] = STAGE[d];
    await run(`${d}kill @e[type=!minecraft:player,x=${sx},y=${sy},z=${sz},distance=..60]`);
    await near(d, sx, sy, sz); await sleep(1200); A.stand();
    await run(`tag TestRat remove ${sensed}`);
    A.titles.length = 0;
    await run('clear TestRat'); await give(item); await use(0);
    if (!ok(`[${k}] the summon item, used: the boss is here`, await wait(3000, async () => (await cnt(sel(k), d)) === 1))) continue;
    // ---- the arrival
    const t1 = await tags(k);
    ok(`[${k}] ...arriving: frozen (no AI, invulnerable)`, /bm\.carr/.test(t1) && /bm\.cfrz/.test(t1) && /1b/.test(await run(`${d}data get entity ${sel(k)} NoAI`)) &&
       /1b/.test(await run(`${d}data get entity ${sel(k)} Invulnerable`)));
    const steed = () => P(`${d}execute as ${sel(k)} on vehicle run data get entity @s Pos`);
    const spot = () => P(`${d}data get entity @e[type=minecraft:marker,tag=bm.cdst_hhm,limit=1] Pos`);
    if (k === 'hhm') ok('[hhm] ...his steed starts far off, out of the dark (and gallops in)', flat2(await steed(), await spot()) > 12, `${flat2(await steed(), await spot()).toFixed(1)} blocks`);
    if (k === 'sph' || k === 'trt' || k === 'mcol') ok(`[${k}] ...below the ground, to rise out of it`, (await posY(k)) < sy - 3, `y ${await posY(k)} (floor ${sy})`);
    if (k === 'sph' || k === 'trt') ok(`[${k}] ...small, to grow`, (await scale(k)) < 1.6, `${await scale(k)}`);
    if (k === 'roc') ok('[roc] ...high in the sky, to dive', (await posY(k)) > sy + 25, `y ${await posY(k)}`);
    if (k === 'vwk') ok('[vwk] ...tiny, inside its rift', (await scale(k)) < 0.2, `${await scale(k)}`);
    if (k === 'sph') {       // a hit while it arrives does nothing
      const h0 = await hp(k); await run(`${d}execute at ${sel(k)} run tp TestRat ~1.5 ~4.5 ~ facing entity ${sel(k)} eyes`); await sleep(300);
      const id = await eidOf(sel(k), d); A.slot(1); await run('item replace entity TestRat hotbar.1 with minecraft:netherite_sword'); await sleep(200);
      if (id) A.attack(id); await sleep(400);
      ok('[sph] ...a hit while it arrives does nothing (invulnerable)', (await hp(k)) === h0, `${h0} -> ${await hp(k)}`);
      await near(d, sx, sy, sz);
    }
    ok(`[${k}] ...its title card on the player's screen: "${title}"`, await wait(7000, async () => A.titles.some(t => t.includes(title))), A.titles.join(' | ').slice(0, 100));
    if (k === 'sph' || k === 'trt') ok(`[${k}] ...risen to the ground, at full size (still frozen for its title)`, Math.abs((await posY(k)) - sy) < 0.05 && Math.abs((await scale(k)) - 2.6) < 0.05,
                                       `y ${await posY(k)} scale ${await scale(k)}`);
    if (k === 'mcol') ok('[mcol] ...out of the floor, landed (still frozen for its title)', Math.abs((await posY(k)) - sy) < 0.3, `y ${await posY(k)}`);
    if (k === 'vwk') ok('[vwk] ...stepped out at full size', Math.abs((await scale(k)) - 2.5) < 0.05, `${await scale(k)}`);
    ok(`[${k}] ...released and armed once it's done`, await wait(4000, async () => { const t = await tags(k); return /bm\.carm/.test(t) && !/bm\.cfrz/.test(t); }));
    ok(`[${k}] ...awake again (AI back)`, !/1b/.test(await run(`${d}data get entity ${sel(k)} NoAI`)));
    ok(`[${k}] ...its song: the player has sensed it`, /passed/i.test(await run(`execute if entity @a[name=TestRat,tag=${sensed}]`)));
    if (k === 'hhm') ok('[hhm] ...still mounted, his steed pulled up at the spot', flat2(await steed(), await spot()) < 1.5, `${flat2(await steed(), await spot()).toFixed(2)} blocks`);
    ok(`[${k}] ...its bar reads its true health (${maxHp} of ${maxHp})`, await wait(2500, async () => (await num(`bossbar get ${bar} value`)) === maxHp),
       `bar ${await num(`bossbar get ${bar} value`)}, health ${await hp(k)}, buffer ${await buf(k)}`);
    // ---- party scaling: a second player arrives - its health grows half again, on its real health (the buffer intact)
    if (k === 'hhm') {
      const B = await bot('PartyPal'); await sleep(2500); B.stand();
      await run('gamemode survival PartyPal'); await run(`${d}tp PartyPal ${sx + 3.5} ${sy} ${sz + 0.5}`); await run('effect give PartyPal minecraft:resistance 120 4 true');
      ok('[hhm] a second player near: his health grows half again (540), still near full, still armed', await wait(8000, async () =>
         (await num(`bossbar get ${bar} max`)) === 540 && (await num(`bossbar get ${bar} value`)) >= 530 && (await buf(k)) > 0 && /bm\.carm/.test(await tags(k))),
         `bar ${await num(`bossbar get ${bar} value`)}/${await num(`bossbar get ${bar} max`)} health ${await hp(k)} buffer ${await buf(k)}`);
      B.end(); await sleep(500);
      ok('[hhm] ...the second player gone: back to 360', await wait(9000, async () => (await num(`bossbar get ${bar} max`)) === 360 && (await num(`bossbar get ${bar} value`)) >= 352),
         `bar ${await num(`bossbar get ${bar} value`)}/${await num(`bossbar get ${bar} max`)}`);
    }
    // ---- a wind-up (staged: its turn counter set one short of the blow)
    if (k === 'mcol' || k === 'sph') {
      await run(`${d}tp TestRat ${sx + 4.5} ${sy} ${sz + 0.5}`); await run(`${d}tp ${sel(k)} ${sx + 0.5} ${sy} ${sz + 0.5}`);
      await run(`${d}scoreboard players set ${sel(k)} bm.r53t ${k === 'mcol' ? 2 : 5}`);
      const wound = await wait(2500, async () => /bm\.cwind/.test(await tags(k)), 100);
      ok(`[${k}] a wind-up: it charges first (${k === 'mcol' ? 'the slam' : 'the sandblast'})`, wound);
      if (k === 'mcol') ok('[mcol] ...squatting', (await scale(k)) < 0.95, `${await scale(k)}`);
      ok(`[${k}] ...then strikes, and is itself again`, await wait(2500, async () => !/bm\.cwind/.test(await tags(k)), 100) && (k !== 'mcol' || Math.abs((await scale(k)) - 1) < 0.01),
         `scale ${await scale(k)}`);
      await near(d, sx, sy, sz);
    }
    // ---- its rage: a moment
    A.titles.length = 0;
    await setReal(k, rageAt - 6);
    ok(`[${k}] below its rage line: it freezes for its rage moment`, await wait(2500, async () => { const t = await tags(k); return /bm\.crage/.test(t) && /bm\.cfrz/.test(t); }, 100));
    ok(`[${k}] ...its rage line on the player's screen`, await wait(1500, async () => A.titles.some(t => t.includes(rageLine))), A.titles.join(' | ').slice(0, 100));
    ok(`[${k}] ...then rages, free again`, await wait(4000, async () => { const t = await tags(k); return new RegExp(rageTag.replace('.', '\\.')).test(t) && !/bm\.cfrz/.test(t); }));
    // ---- its death, by the player's sword
    await run(`${d}kill @e[type=minecraft:item,x=${sx},y=${sy},z=${sz},distance=..60]`);
    // (the stage, not the test: the boss held still in the middle, near death; the player beside it, sword ready)
    await run(`${d}data merge entity ${sel(k)} {NoAI:1b}`);
    if (k === 'hhm') await run(`${d}execute as ${sel(k)} on vehicle run tp @s ${sx + 0.5} ${sy} ${sz + 0.5}`);
    else await run(`${d}tp ${sel(k)} ${sx + 0.5} ${k === 'roc' ? sy + 1 : sy} ${sz + 0.5}`);
    await setReal(k, 1);
    await run(`${d}execute at ${sel(k)} run tp TestRat ~1.8 ${sy} ~ facing entity ${sel(k)} eyes`);
    await run('item replace entity TestRat hotbar.1 with minecraft:netherite_sword'); A.slot(1); await sleep(1300);
    const id = await eidOf(sel(k), d);
    if (id) A.attack(id); await sleep(300);
    const dying = await wait(1500, async () => /bm\.cdie/.test(await tags(k)), 100);
    ok(`[${k}] the player's blow brings it down: its death begins (frozen)`, dying && /bm\.cfrz/.test(await tags(k)), `eid ${id} health ${await hp(k)}`);
    ok(`[${k}] ...its bar gone`, await wait(1500, async () => /hidden/.test(await run(`bossbar get ${bar} visible`))));
    const dpos = (await run(`${d}data get entity ${sel(k)} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    await near(d, sx, sy, sz);
    await sleep(2200);
    ok(`[${k}] ...still there, mid-sequence, two seconds on`, (await cnt(sel(k), d)) === 1);
    if (k === 'hhm') ok('[hhm] ...his head has fallen from his hand (tumbling to the ground)', (await cnt('@e[type=minecraft:item_display,tag=bm.chead]', d)) === 1);
    if (k === 'sph') ok('[sph] ...sinking into the sand', (await posY(k)) < sy - 0.8, `y ${await posY(k)}`);
    const fell = await wait(6000, async () => (await cnt(sel(k), d)) === 0);
    ok(`[${k}] ...then it falls`, fell);
    ok(`[${k}] ...as the player's kill: its relic lies on the ground`, await wait(2500, async () =>
       (await cnt(`@e[type=minecraft:item,x=${sx},y=${sy},z=${sz},distance=..60,nbt={Item:{components:{"minecraft:custom_data":{bm:"${relic}"}}}}]`, d)) > 0));
    if (k === 'hhm') ok('[hhm] ...his steed gone with him, the head too', (await cnt('@e[type=minecraft:skeleton_horse,tag=bm.hhs]', d)) === 0 &&
                        (await cnt('@e[type=minecraft:item_display,tag=bm.chead]', d)) === 0);
    if (k === 'trt' && dpos) ok('[trt] ...where it fell, a sapling has taken root', /passed/i.test(await run(`${d}execute positioned ${dpos[1]} ${sy} ${dpos[3]} if block ~ ~ ~ minecraft:oak_sapling`)) ||
                                 /passed/i.test(await run(`${d}execute positioned ${dpos[1]} ${dpos[2]} ${dpos[3]} if block ~ ~ ~ minecraft:oak_sapling`)), dpos.slice(1).join(' '));
    if (k === 'mcol') {
      const spawn = '@e[type=minecraft:magma_cube,tag=bm.mcolmin]';
      ok('[mcol] ...and still bursts into Magma Spawn', await wait(3000, async () => (await cnt(spawn, d)) > 0), `${await cnt(spawn, d)}`);
      ok('[mcol] ...awake and visible (not frozen by its death)', !/1b/.test(await run(`${d}data get entity ${spawn.replace(']', ',limit=1]')} NoAI`)) &&
         !/invisibility/.test(await run(`${d}data get entity ${spawn.replace(']', ',limit=1]')} active_effects`)));
      await run(`${d}kill @e[type=minecraft:magma_cube,tag=bm.mcolmin]`);
    }
    ok(`[${k}] ...and the sequence leaves nothing behind (markers, displays)`, await wait(3000, async () =>
       (await cnt('@e[type=minecraft:marker,tag=bm.cdst_hhm]', d)) + (await cnt('@e[type=minecraft:marker,tag=bm.cpos_sph]', d)) + (await cnt('@e[type=minecraft:marker,tag=bm.cgnd_roc]', d)) +
       (await cnt('@e[type=minecraft:marker,tag=bm.cdst_roc]', d)) + (await cnt('@e[type=minecraft:marker,tag=bm.cpos_vwk]', d)) + (await cnt('@e[type=minecraft:marker,tag=bm.cdst_vwk]', d)) === 0));
    await run(`${d}kill @e[type=!minecraft:player,x=${sx},y=${sy},z=${sz},distance=..60]`);
  }
  await near(O, X, Y + 1, Z);
  for (const b of ['bm:hhm', 'bm:sph', 'bm:roc', 'bm:trt', 'bm:mcol', 'bm:vwk']) await run(`bossbar set ${b} visible false`);
  await run('effect clear TestRat'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${N}forceload remove ${NX - 30} ${NZ - 30} ${NX + 30} ${NZ + 30}`); await run(`${E}forceload remove ${EX - 30} ${EZ - 30} ${EX + 30} ${EZ + 30}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
