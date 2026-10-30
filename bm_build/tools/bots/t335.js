// 3.0e: THE BROOD-MIRE (phase258, on mirekit - the Dread Mire's runtime) and THE BROOD MIRELING, as a regular (non-op) player.
// rcon sets the stage (hard mode, places, a Mire set down, a stand-in spawn's roll, an Invasion Night begun, items given);
// the player walks, holds, uses, sneaks and strikes.
//   rules     where it may be: one set down in the Overworld outside an invasion, or in the Nether, melts away; with Vexis fallen
//             (#vfell) one in the End melts and none rises; the natural roll (an End monster's) brings none near the main island, one
//             far out in the outer End (a puddle, dormant) - and no second for the same player that day (bm.bxday)
//   end       its puddle (26 parts: the Dread Mire's 23 and three eyestalks); holding the Severed Link it won't rise for you - not
//             holding it, it rises; walked away from, it sinks back to wait; a SIGNAL JAMMER switched on in the End (10 minutes,
//             bm.jamt): it shrieks, recoils and sinks, won't rise while the jammer hums, slips away from it; off: it rises
//   fight     risen in the End: the SPIT at range (a glob of acid flies, the player poisoned, an acid pool), the GRAB in reach; worn to
//             half, three Broodlings burst out; felled by the player's blow: it melts (purple goop, dfx_bgoop; green bubbles,
//             bbubble), the Broodlings melt with it, every part gone, Brood Ichor and Xenite where it was
//   items     4 Brood Ichor used: Hive Scent; drunk: no Brood-Mire fights you (and when it wears off, it does); 16, sneak + used: a
//             Brood Pod; planted (sneak + use on a block): a Bound Brood-Mire that rises for a monster and hurts it, never you;
//             sneak + punch its puddle: the pod back
//   invasion  an Invasion Night: a saucer's drop (the surge's own try, as the player): lowered down a tractor beam (ms 9), it
//             splats and rises; one a night for that player; dawn: it melts away
//   armada    the Armada (placed; its box's chunks held): the roam's places (fx markers whose nearest trial is a puzzle or wave
//             room) - some, none by a vault; one lurks there as a puddle; the Bio-Wave's last wave brings one down a short beam,
//             tagged the wave's own (it holds the wave)
//   costume   the Mireling called; a Brood Ichor used beside it: it drinks, its looks 8 (and, its shiny owned, 9) unlocked and worn
//             (ml_body_c8); the wardrobe's two Brood buttons; FULL-GROWN in the costume: the Brood-Mire's 26 parts (bx_*), the
//             shiny's (bx_*_sh), the plain look: the Dread Mire's 23 (mr_*); the honour takes Brood Ichor (its function)
//   node t335.js [rules|end|fight|items|invasion|armada|costume]
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const DP = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function';
const OX = 18480, OZ = 16080, Y = 100;              // (the Overworld stage)
const EX = -6000, EZ = 6000;                         // (the outer End's)
const NX = 18480, NZ = 16080;                        // (the Nether's)
const O = 'execute in minecraft:overworld run ', E = 'execute in minecraft:the_end run ', N = 'execute in minecraft:the_nether run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const cnt = async (sel, D = E) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (who, o, D = E) => +((await run(`${D}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const nbt = async (sel, path, D = E) => (await run(`${D}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const give = async (iid, n = 1) => { for (let i = 0; i < n; i++) await run(`loot give TestRat loot bm:items/${iid}`); };
  const uuidOf = async (sel, D = E) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (+v >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel, D = E) => { const u = await uuidOf(sel, D); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const vec = (s) => (s.match(/\[(-?[\d.E-]+)f, (-?[\d.E-]+)f, (-?[\d.E-]+)f\]/) || []).slice(1).map(Number);
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2500, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const use = async (slot, sneak = false, ms = 300) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(ms); A.release(); if (sneak) { A.input({}); await sleep(150); } await sleep(300); };
  const BM = (x, y, z, r = 6, D = '') => `@e[type=minecraft:husk,tag=bm.bmire,x=${x},y=${y},z=${z},distance=..${r},limit=1]`;
  const stage = async (D, x, z) => {
    await run(`${D}forceload add ${x - 32} ${z - 32} ${x + 32} ${z + 32}`); await sleep(2500);
    await run(`${D}fill ${x - 30} ${Y} ${z - 30} ${x + 30} ${Y} ${z + 30} minecraft:end_stone`);
    await run(`${D}fill ${x - 30} ${Y + 1} ${z - 30} ${x + 30} ${Y + 14} ${z + 30} minecraft:air`);
    await run(`${D}kill @e[type=!minecraft:player,x=${x},y=${Y},z=${z},distance=..40]`);
  };
  const clean = async (D, x, z) => { await run(`${D}kill @e[type=minecraft:item,x=${x},y=${Y},z=${z},distance=..40]`); await run(`${D}kill @e[type=minecraft:item_display,tag=bm.bxr,x=${x},y=${Y},z=${z},distance=..40]`);
    await run(`${D}kill @e[type=minecraft:interaction,tag=bm.bxtk,x=${x},y=${Y},z=${z},distance=..40]`); await run(`${D}kill @e[type=minecraft:slime,tag=bm.bxling,x=${x},y=${Y},z=${z},distance=..40]`);
    await run(`${D}execute as @e[type=minecraft:husk,tag=bm.bmire,x=${x},y=${Y},z=${z},distance=..40] run tp @s ~ -400 ~`); await sleep(400); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const keep = {}; for (const k of ['#hard', '#vfell', '#dfell']) keep[k] = await sc(k, 'bm.cfg', '');
  await run('scoreboard players set #hard bm.cfg 1'); await run('scoreboard players set #vfell bm.cfg 0'); await run('scoreboard players set #dfell bm.cfg 0');
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run('scoreboard players reset TestRat bm.bxday'); await run('tag TestRat remove bm.jam'); await run('scoreboard players reset TestRat bm.jamt');
  await run('tag TestRat remove bm.hsc'); await run('scoreboard players reset TestRat bm.hscent');
  await stage(E, EX, EZ);
  const H = (dz) => BM(EX + 0.5, Y + 1, EZ + dz + 0.5);

  if (on('rules')) {
    await stage(O, OX, OZ);
    await at(E, EX + 0.5, Y + 1, EZ + 0.5);
    await run(`${O}execute positioned ${OX + 0.5} ${Y + 1} ${OZ + 6.5} run function bm:p258/spawn`);
    ok('one set down in the Overworld outside an Invasion Night melts away (host and rig)', await wait(3000, async () =>
      (await cnt(BM(OX + 0.5, Y + 1, OZ + 6.5), O)) === 0 && (await cnt(`@e[type=minecraft:item_display,tag=bm.bxr,x=${OX},y=${Y},z=${OZ},distance=..20]`, O)) === 0));
    await run(`${N}forceload add ${NX - 8} ${NZ - 8} ${NX + 8} ${NZ + 8}`); await sleep(2000);
    await run(`${N}fill ${NX - 3} 64 ${NZ - 3} ${NX + 3} 64 ${NZ + 3} minecraft:netherrack`); await run(`${N}fill ${NX - 3} 65 ${NZ - 3} ${NX + 3} 70 ${NZ + 3} minecraft:air`);
    await run(`${N}execute positioned ${NX + 0.5} 65 ${NZ + 0.5} run function bm:p258/spawn`);
    ok('...one in the Nether (the Undercrown\'s) melts away too', await wait(3000, async () =>
      (await cnt(BM(NX + 0.5, 65, NZ + 0.5), N)) === 0 && (await cnt(`@e[type=minecraft:item_display,tag=bm.bxr,x=${NX},y=65,z=${NZ},distance=..10]`, N)) === 0));
    await run(`${E}execute positioned ${EX + 0.5} ${Y + 1} ${EZ + 8.5} run function bm:p258/spawn`); await sleep(1200);
    ok('in the outer End one stays (dormant, its puddle)', (await cnt(H(8))) === 1 && (await sc(H(8), 'bm.ms')) === 0);
    await run('scoreboard players set #vfell bm.cfg 1');
    ok('...Admiral Vexis fallen (#vfell): it melts away', await wait(3000, async () => (await cnt(H(8))) === 0));
    // (the natural roll: an End monster rising, as the pack rolls it - a stand-in enderman, its roll run until it comes up a Brood-Mire)
    const roll = async (x, z, n) => {
      await run(`${E}summon minecraft:enderman ${x} ${Y + 1} ${z} {NoAI:1b,Tags:["bm.seen","bm.bxt"],PersistenceRequired:1b}`);
      for (let i = 0; i < n; i++) {           // (the roll takes the monster away when it comes up a Brood-Mire)
        await run(`${E}execute as @e[type=minecraft:enderman,tag=bm.bxt,limit=1] at @s run function bm:p258/roll`);
        if ((await cnt('@e[type=minecraft:enderman,tag=bm.bxt]')) === 0) return i + 1;
      }
      await run(`${E}kill @e[type=minecraft:enderman,tag=bm.bxt]`); return 0;
    };
    ok('...and while it stays fallen none rises (the roll, 800 tries: nothing)', (await roll(EX + 4.5, EZ - 6.5, 800)) === 0 && (await cnt(`@e[type=minecraft:husk,tag=bm.bmire,x=${EX},y=${Y},z=${EZ},distance=..30]`)) === 0);
    await run('scoreboard players set #vfell bm.cfg 0');
    await run(`${E}forceload add 90 -10 110 10`); await sleep(1500);
    await run(`${E}fill 96 ${Y} -4 104 ${Y} 4 minecraft:end_stone`); await run(`${E}fill 96 ${Y + 1} -4 104 ${Y + 4} 4 minecraft:air`);
    await at(E, 100.5, Y + 1, 0.5);
    ok('the roll near the main island (100 from 0, 0): none in 800', (await roll(102.5, 2.5, 800)) === 0);
    await at(E, EX + 0.5, Y + 1, EZ + 0.5);
    const n = await roll(EX + 4.5, EZ - 6.5, 3000);
    ok('the roll far out in the outer End: a Brood-Mire comes up instead of the monster (dormant)', n > 0 && (await cnt(`@e[type=minecraft:husk,tag=bm.bmire,x=${EX + 4.5},y=${Y + 1},z=${EZ - 6.5},distance=..2]`)) === 1, `after ${n}`);
    ok('...TestRat\'s day counted (bm.bxday)', (await sc('TestRat', 'bm.bxday')) >= 0);
    await clean(E, EX, EZ);
    ok('...and no second for TestRat that day (3000 tries: none)', (await roll(EX + 4.5, EZ - 6.5, 3000)) === 0);
    await run('scoreboard players reset TestRat bm.bxday');
  }

  if (on('end')) {
    await clean(E, EX, EZ); await at(E, EX + 0.5, Y + 1, EZ - 14.5);
    await run(`${E}execute positioned ${EX + 0.5} ${Y + 1} ${EZ + 0.5} run function bm:p258/spawn`); await sleep(1200);
    const BR = BM(EX + 0.5, Y + 1, EZ + 0.5, 8);
    ok('a Brood-Mire\'s puddle: 26 parts (the Dread Mire\'s 23 and three eyestalks), dormant', (await cnt(`@e[type=minecraft:item_display,tag=bm.bxr,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..6]`)) === 26 && (await sc(BR, 'bm.ms')) === 0);
    ok('...the puddle shows; the rest sunk at nothing (an eyestalk at scale 0)', vec(await nbt(`@e[type=minecraft:item_display,tag=bm.bxr_puddle,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..6,limit=1]`, 'transformation.scale'))[0] > 1 &&
       vec(await nbt(`@e[type=minecraft:item_display,tag=bm.bxr_es1,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..6,limit=1]`, 'transformation.scale'))[0] === 0);
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/vexis_link'); A.slot(0); await sleep(300);
    await at(E, EX + 0.5, Y + 1, EZ - 5.5);
    await sleep(4000);
    ok('holding the Severed Link 6 blocks off: it doesn\'t rise for you (4 s)', (await sc(BR, 'bm.ms')) === 0);
    A.slot(4); await sleep(300);
    ok('...not holding it: it rises', await wait(4000, async () => (await sc(BR, 'bm.ms')) >= 1, 200));
    ok('...risen (ms 2)', await wait(4000, async () => (await sc(BR, 'bm.ms')) === 2, 200));
    await at(E, EX + 0.5, Y + 1, EZ - 27.5);
    ok('walked away from (over 20): after 10 s it sinks back down to wait', await wait(16000, async () => (await sc(BR, 'bm.ms')) === 0, 500));
    await run('clear TestRat'); await give('signal_jammer');
    await at(E, EX + 0.5, Y + 1, EZ - 5.5);
    await wait(4000, async () => (await sc(BR, 'bm.ms')) === 2, 200);
    A.bars.length = 0; await use(0, false, 1300);
    ok('a Signal Jammer switched on in the End: on for 10 minutes (bm.jam, bm.jamt)', /bm\.jam\b/.test(await run('tag TestRat list')) && (await sc('TestRat', 'bm.jamt', '')) > 500, A.bars.slice(-1).join(''));
    ok('...it shrieks and recoils (ms 5), then sinks (ms 0)', await wait(3000, async () => [5, 6].includes(await sc(BR, 'bm.ms')), 100) && await wait(4000, async () => (await sc(BR, 'bm.ms')) === 0, 200));
    const p0 = (await nbt(BR, 'Pos')).match(/-?[\d.]+/g).map(Number);
    await sleep(4000);
    const p1 = (await nbt(BR, 'Pos')).match(/-?[\d.]+/g).map(Number);
    ok('...while it hums: it doesn\'t rise for you, and its puddle slips away from the jammer', (await sc(BR, 'bm.ms')) === 0 && Math.hypot(p1[0] - (EX + 0.5), p1[2] - (EZ - 5.5)) > Math.hypot(p0[0] - (EX + 0.5), p0[2] - (EZ - 5.5)) + 0.5,
       `${p0[2].toFixed(1)} -> ${p1[2].toFixed(1)}`);
    await run('tag TestRat remove bm.jam'); await run('scoreboard players reset TestRat bm.jamt');
    await at(E, p1[0], Y + 1, p1[2] - 5);
    ok('...the jammer off: it rises again', await wait(5000, async () => (await sc(BR, 'bm.ms')) >= 1, 200));
  }

  if (on('fight')) {
    await clean(E, EX, EZ); await run('clear TestRat');
    await at(E, EX + 0.5, Y + 1, EZ - 10.5, 0, 0);
    await run(`${E}execute positioned ${EX + 0.5} ${Y + 1} ${EZ + 0.5} rotated 180 0 run function bm:p258/spawn`);
    const BR = BM(EX + 0.5, Y + 1, EZ + 0.5, 8);
    await run(`${E}execute as ${BR} at @s run function bm:p258/rise0`);
    ok('risen in the End (ms 2)', await wait(4000, async () => (await sc(BR, 'bm.ms')) === 2, 200));
    await run('effect clear TestRat minecraft:poison');
    ok('at range (11): THE SPIT - it rears (ms 8) and a glob of acid flies (bm.bxglob)', await wait(8000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.bxglob,x=${EX},y=${Y},z=${EZ},distance=..30]`)) >= 1, 100));
    ok('...it lands: the player poisoned, or a pool of acid at their feet (bm.bxacid)', await wait(4000, async () =>
      /poison/.test(await nbt('@a[name=TestRat,limit=1]', 'active_effects', '')) || (await cnt(`@e[type=minecraft:area_effect_cloud,tag=bm.bxacid,x=${EX + 0.5},y=${Y + 1},z=${EZ - 10.5},distance=..5]`)) >= 1, 100));
    await at(E, EX + 0.5, Y + 1, EZ - 5.5, 0, 0);
    ok('in reach (6): THE GRAB - a tentacle has you (bm.bxgrab)', await wait(9000, async () => /bm\.bxgrab/.test(await run('tag TestRat list')), 100));
    await run(`${E}data merge entity ${BR} {Health:185f}`);
    ok('worn to half: three Broodlings burst out of its cysts', await wait(3000, async () => (await cnt(`@e[type=minecraft:slime,tag=bm.bxling,x=${EX},y=${Y},z=${EZ},distance=..20]`)) === 3, 150));
    await run('item replace entity TestRat hotbar.8 with minecraft:netherite_sword'); A.slot(8);
    await at(E, EX + 0.5, Y + 1, EZ - 2.5, 0, 10);
    await run(`${E}data merge entity ${BR} {Health:104f}`);
    for (let k = 0; k < 8 && (await sc(BR, 'bm.ms')) !== 7; k++) { const e = await entOf(BR); if (e) A.attack(e.entityId); await sleep(700); }
    ok('felled by the player\'s blow: it melts (ms 7)', await wait(3000, async () => (await sc(BR, 'bm.ms')) === 7, 100));
    ok('...its Broodlings melt with it', await wait(2000, async () => (await cnt(`@e[type=minecraft:slime,tag=bm.bxling,x=${EX},y=${Y},z=${EZ},distance=..30]`)) === 0, 150));
    const G = `@e[type=minecraft:item_display,tag=bm.bxgoop,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..6,limit=1]`;
    ok('...a pile of PURPLE-GREEN goop wells up (dfx_bgoop)', await wait(5000, async () => /dfx_bgoop/.test(await nbt(G, 'item')), 150));
    ok('...and green-lit bubbles on it (bbubble sprites)', await wait(4000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.dfx_bbubble,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..5]`)) >= 1, 100));
    ok('...then it is gone - host, every part, the goop', await wait(9000, async () => (await cnt(BR)) === 0 && (await cnt(`@e[type=minecraft:item_display,tag=bm.bxr,x=${EX},y=${Y},z=${EZ},distance=..20]`)) === 0, 250));
    const drop = (iid) => `@e[type=minecraft:item,x=${EX + 0.5},y=${Y + 1},z=${EZ + 0.5},distance=..5,nbt={Item:{components:{"minecraft:custom_data":{bm:"${iid}"}}}}]`;
    ok('...and Brood Ichor where it was', await wait(2500, async () => (await cnt(drop('brood_ichor'))) >= 1, 200));
    ok('...and Xenite (green or violet)', (await cnt(drop('xenite_green'))) + (await cnt(drop('xenite_violet'))) >= 1);
  }

  if (on('items')) {
    await clean(E, EX, EZ); await run('clear TestRat');
    await at(E, EX + 0.5, Y + 1, EZ - 10.5, 0, 0);
    await give('brood_ichor', 4); A.bars.length = 0; await use(0);
    ok('4 Brood Ichor used: a vial of Hive Scent (the ichor gone)', await wait(2000, async () => (await has('hive_scent')) === 1 && (await has('brood_ichor')) === 0), A.bars.slice(-1).join(''));
    await run(`${E}execute positioned ${EX + 0.5} ${Y + 1} ${EZ + 0.5} rotated 180 0 run function bm:p258/spawn`);
    const BR = BM(EX + 0.5, Y + 1, EZ + 0.5, 8);
    await run(`${E}execute as ${BR} at @s run function bm:p258/rise0`); await wait(4000, async () => (await sc(BR, 'bm.ms')) === 2, 200);
    await use(0, false, 1900);
    ok('...drunk: the hive\'s scent on TestRat (bm.hsc, 5 minutes)', /bm\.hsc\b/.test(await run('tag TestRat list')) && (await sc('TestRat', 'bm.hscent', '')) > 250);
    await at(E, EX + 0.5, Y + 1, EZ - 3.5, 0, 0);
    let fought = false; const t0 = Date.now(); while (Date.now() - t0 < 7000) { if ([3, 4, 8].includes(await sc(BR, 'bm.ms'))) fought = true; await sleep(150); }
    ok('...a risen Brood-Mire 4 blocks off doesn\'t fight you (7 s: no grab, stab or spit)', !fought);
    await run('scoreboard players set TestRat bm.hscent 1');
    ok('...it wears off ("You smell like yourself again"): and it fights you', await wait(3000, async () => !/bm\.hsc\b/.test(await run('tag TestRat list'))) &&
       await wait(9000, async () => [3, 4, 8].includes(await sc(BR, 'bm.ms')), 100));
    await clean(E, EX, EZ); await run('clear TestRat');
    await give('brood_ichor', 16); await use(0, true);
    ok('16 Brood Ichor, sneak + used: a Brood Pod', await wait(2000, async () => (await has('brood_pod')) === 1 && (await has('brood_ichor')) === 0));
    await at(E, EX + 0.5, Y + 1, EZ - 4.5, 0, 60);
    await use(0, true);
    const T = `@e[type=minecraft:husk,tag=bm.bxtame,x=${EX},y=${Y},z=${EZ},distance=..12,limit=1]`;
    ok('...planted (sneak + use on a block): a Bound Brood-Mire takes root (bm.bxtame), the pod spent', await wait(2000, async () => (await cnt(T)) === 1) && (await has('brood_pod')) === 0);
    const tp = (await nbt(T, 'Pos')).match(/-?[\d.]+/g).map(Number);
    await at(E, tp[0], Y + 1, tp[2] - 6, 0, 0); await sleep(2500);
    ok('...it doesn\'t rise for its owner', (await sc(T, 'bm.ms')) === 0);
    await run(`${E}summon minecraft:zombie ${tp[0] + 6} ${Y + 1} ${tp[2]} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.bxz"],attributes:[{id:"minecraft:max_health",base:200}],Health:200f}`);
    ok('...a monster near: it rises', await wait(4000, async () => (await sc(T, 'bm.ms')) >= 1, 200));
    ok('...and hurts it', await wait(12000, async () => +(((await nbt('@e[type=minecraft:zombie,tag=bm.bxz,limit=1]', 'Health')).match(/([\d.]+)/) || [0, 200])[1]) < 199, 300));
    await run(`${E}kill @e[type=minecraft:zombie,tag=bm.bxz]`);
    await wait(14000, async () => (await sc(T, 'bm.ms')) === 0, 500);
    const I = `@e[type=minecraft:interaction,tag=bm.bxtk,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..2,limit=1]`;
    await at(E, tp[0], Y + 1, tp[2] - 2.5, 0, 45);
    A.input({ shift: true }); await sleep(250); const e = await entOf(I); if (e) A.attack(e.entityId); await sleep(800); A.input({}); await sleep(300);
    ok('...sneak + punch its puddle: the Brood Pod back, the Brood-Mire gone', await wait(2500, async () => (await has('brood_pod')) === 1 && (await cnt(T)) === 0));
  }

  if (on('invasion')) {
    await stage(O, OX, OZ); await run('clear TestRat');
    await at(O, OX + 0.5, Y + 1, OZ + 0.5, 0, 0);
    await run(`${O}time set 13500`); await run('execute as TestRat run function bm:admin/invasion_now');
    ok('an Invasion Night begins', await wait(8000, async () => (await sc('#inv', 'bm.bm', '')) === 1, 300));
    await run(`${O}execute at TestRat run summon minecraft:marker ~ ~ ~ {Tags:["bm.vsp"],Rotation:[0f,0f]}`);
    await run(`${O}execute as TestRat at @s run function bm:p258/inv/try`); await run(`${O}kill @e[type=minecraft:marker,tag=bm.vsp]`);
    const IV = `@e[type=minecraft:husk,tag=bm.bmire,tag=bm.bxinv,x=${OX + 0.5},y=${Y + 1},z=${OZ + 20.5},distance=..16,limit=1]`;
    ok('a saucer\'s drop: a Brood-Mire in a tractor beam 20 blocks off (ms 9), lifted above the ground', (await cnt(IV, O)) === 1 && (await sc(IV, 'bm.ms', O)) === 9 &&
       +((await nbt(IV, 'Pos', O)).match(/-?[\d.]+/g)[1]) > Y + 6);
    ok('...lowered down the beam, it splats and rises (ms 1, then 2)', await wait(4000, async () => (await sc(IV, 'bm.ms', O)) >= 1 && (await sc(IV, 'bm.ms', O)) !== 9, 100) &&
       await wait(5000, async () => (await sc(IV, 'bm.ms', O)) === 2, 200));
    ok('...on the ground', Math.abs(+((await nbt(IV, 'Pos', O)).match(/-?[\d.]+/g)[1]) - (Y + 1)) < 0.6);
    await run(`${O}execute at TestRat run summon minecraft:marker ~ ~ ~ {Tags:["bm.vsp"],Rotation:[90f,0f]}`);
    await run(`${O}execute as TestRat at @s run function bm:p258/inv/try`); await run(`${O}kill @e[type=minecraft:marker,tag=bm.vsp]`);
    ok('...one a night for each player: a second try brings none', (await cnt(`@e[type=minecraft:husk,tag=bm.bmire,x=${OX},y=${Y},z=${OZ},distance=..40]`, O)) === 1);
    await run('execute as TestRat run function bm:admin/invasion_stop');
    ok('dawn (the invasion ends): it melts away, its rig with it', await wait(3000, async () => (await cnt(`@e[type=minecraft:husk,tag=bm.bmire,x=${OX},y=${Y},z=${OZ},distance=..40]`, O)) === 0 &&
       (await cnt(`@e[type=minecraft:item_display,tag=bm.bxr,x=${OX},y=${Y},z=${OZ},distance=..40]`, O)) === 0));
    await run(`${O}time set 6000`); await run('scoreboard players reset TestRat bm.bxday');
  }

  if (on('armada')) {
    const [ox, oy, oz, sx, sy, sz] = require('child_process').execSync(`cd /home/user/main/bm_build && python3 -c "import p2.armadacfg as A; print(*A.ORIGIN, *A.SIZE)"`).toString().trim().split(/\s+/).map(Number);
    await run(`${E}forceload add ${ox} ${oz} ${ox + sx - 1} ${oz + sz - 1}`); await sleep(6000);
    const pz3 = `@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz3,tag=bm.d_armada,limit=1]`;
    if (!ok('the Armada is placed (its Bio-Wave\'s trial marker found)', (await cnt(pz3)) === 1)) { console.log('  (place the Armada first)'); }
    else {
      const FX = '@e[type=minecraft:marker,tag=bm.dgfx,tag=bm.d_armada]';
      const all = await cnt(FX);
      const open = +((await run(`${E}execute as ${FX} at @s if function bm:p258/arm/open`)).match(/count: (\d+)/i) || [0, 0])[1];
      ok('the roam\'s places: some of its fx markers (whose nearest trial is a puzzle or wave room), not all', open >= 1 && open < all, `${open} of ${all}`);
      const byVault = +((await run(`${E}execute as ${FX} at @s if function bm:p258/arm/open if entity @e[type=minecraft:marker,tag=bm.vaultm,distance=..14]`)).match(/count: (\d+)/i) || [0, 0])[1];
      ok('...none by a vault', byVault === 0);
      const byBoss = +((await run(`${E}execute as ${FX} at @s if function bm:p258/arm/open if entity @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_armada,distance=..40,sort=nearest,limit=1,tag=bm.pz13]`)).match(/count: (\d+)/i) || [0, 0])[1];
      ok('...none whose nearest trial is a guardian\'s (the Star-Seer\'s)', byBoss === 0);
      await run(`${E}execute as ${FX} at @s if function bm:p258/arm/open run tag @s add bm.bxt`);
      await run(`${E}execute as @e[type=minecraft:marker,tag=bm.bxt,limit=1,sort=random] at @s run function bm:p258/arm/lurk`); await run(`${E}tag @e[tag=bm.bxt] remove bm.bxt`);
      ok('...one lurks there: a puddle (dormant, bm.bxroam) on the floor', await wait(2000, async () => (await cnt('@e[type=minecraft:husk,tag=bm.bmire,tag=bm.bxroam]')) === 1));
      await run(`${E}execute as @e[type=minecraft:husk,tag=bm.bmire,tag=bm.bxroam] at @s run function bm:p258/melt`);
      await run(`${E}execute as ${pz3} at @s run function bm:p2/armada/pz3_w3`);
      const WB = `@e[type=minecraft:husk,tag=bm.bmire,tag=bm.wm_armada3,limit=1]`;
      ok('the Bio-Wave\'s last wave: a Brood-Mire comes down a short beam (ms 9), the wave\'s own (bm.wm_armada3)', await wait(1500, async () => (await cnt(WB)) === 1 && (await sc(WB, 'bm.ms')) === 9));
      ok('...splats and rises', await wait(5000, async () => (await sc(WB, 'bm.ms')) === 2, 200));
      ok('...and the wave holds while it stands (the trial sees its wave mark)', +((await run(`${E}execute as ${pz3} at @s if entity @e[tag=bm.wm_armada3,distance=..64]`)).match(/count: (\d+)/i) || [0, 0])[1] === 1);
      await run(`${E}execute as @e[tag=bm.wm_armada3] at @s run function bm:p2/util/vanish`); await run(`${E}execute as ${pz3} at @s run function bm:p2/armada/pz3_wabort`);
      ok('...the wave aborted: its rig goes with it (no Brood-Mire part left within 2 s)', await wait(2500, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.bxr]')) === 0, 250));
    }
  }

  if (on('costume')) {
    await stage(O, OX, OZ); await run('clear TestRat'); await run(`${O}time set 6000`);
    await run('kill @e[type=minecraft:wolf,tag=bm.mlpet]'); await sleep(500);
    await run('scoreboard players set TestRat bm.wumireling 128'); await run('scoreboard players set TestRat bm.cosml 0'); await run('scoreboard players set TestRat bm.mlub 0');
    await run('scoreboard players set TestRat bm.mlcd 0');
    await at(O, OX + 0.5, Y + 1, OZ + 0.5, 0, 0);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/mire_seed'); await use(0);
    const PET = '@e[type=minecraft:wolf,tag=bm.mlpet,limit=1]';
    ok('the Mireling called (its seed used)', await wait(4000, async () => (await cnt(PET, O)) === 1)); await sleep(1500);
    const BODY = '@e[type=minecraft:item_display,tag=bm.mlp_pet,tag=bm.mlp_body,tag=!bm.mlfade,limit=1]';
    const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"', O)).replace(/"/g, '');
    ok('...in its own look (ml_body)', /bm:ml_body$/.test(await model()), await model());
    await run('item replace entity TestRat hotbar.1 with minecraft:air'); await run('loot replace entity TestRat hotbar.1 loot bm:items/brood_ichor');
    A.chats.length = 0; await use(1); await sleep(800);
    ok('a Brood Ichor used beside it: it drinks it ("one long slurp")', A.chats.some(c => /drinks the ichor/.test(c)) && (await has('brood_ichor')) === 0, A.chats.slice(-2).join(' / '));
    const un = await sc('TestRat', 'bm.wumireling', '');
    ok('...THE BROOD MIRELING in its wardrobe for good (bit 8) - and, its shiny owned, Shiny Pearl Brood (bit 9)', Math.floor(un / 256) % 2 === 1 && Math.floor(un / 512) % 2 === 1, `${un}`);
    ok('...worn at once: every part in the costume (ml_body_c8)', (await sc('TestRat', 'bm.cosml', '')) === 8 && await wait(3000, async () => /ml_body_c8$/.test(await model())), await model());
    const sneakMenu = async () => { const n0 = A.dialogN.length; await use(0, true); await wait(3000, async () => A.dialogN.length > n0); };
    await sneakMenu(); const w = await A.press(/Wardrobe/);
    ok('its menu -> Wardrobe: both Brood looks', w && A.buttons().some(b => /Brood Mireling/.test(b.label)) && A.buttons().some(b => /Shiny Pearl Brood/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await A.press(/Shiny Pearl Brood/); await sleep(1200);
    ok('...Shiny Pearl Brood pressed: worn (ml_body_c9)', /ml_body_c9$/.test(await model()), await model());
    await sneakMenu(); await A.press(/Wardrobe/); await A.press(/Brood Mireling/); await sleep(1200);
    ok('...Brood Mireling pressed: back (ml_body_c8)', /ml_body_c8$/.test(await model()), await model());
    // FULL-GROWN in the costume (Queen Ava's rank III staged)
    await run('scoreboard players set TestRat bm.hn_mireling 1555');
    await sneakMenu(); await A.press(/Grown \/ Little/); await sleep(2500);
    const GP = (p) => `@e[type=minecraft:item_display,tag=bm.mlu,tag=bm.mlu_${p},x=${OX},y=${Y},z=${OZ},distance=..30,limit=1]`;
    const gcount = async () => await cnt(`@e[type=minecraft:item_display,tag=bm.mlu,x=${OX},y=${Y},z=${OZ},distance=..30]`, O);
    ok('FULL-GROWN in the costume: the Brood-Mire\'s 26 parts (bx_head, its eyestalks)', (await gcount()) === 26 && /bm:bx_head$/.test(await model(GP('head'))) && /bm:bx_es1$/.test(await model(GP('es1'))), `${await gcount()} ${await model(GP('head'))}`);
    await sneakMenu(); await A.press(/Wardrobe/); await A.press(/Shiny Pearl Brood/); await sleep(1500);
    ok('...the shiny look picked while grown: the giant swapped for the shiny\'s (bx_head_sh)', await wait(2500, async () => /bm:bx_head_sh$/.test(await model(GP('head')))), await model(GP('head')));
    await sneakMenu(); await A.press(/Wardrobe/); await A.press(/Blood-red veins/); await sleep(1500);
    ok('...its own look: the Dread Mire\'s 23 parts (mr_head)', await wait(2500, async () => (await gcount()) === 23 && /bm:mr_head$/.test(await model(GP('head')))), `${await gcount()} ${await model(GP('head'))}`);
    await sneakMenu(); await A.press(/Grown \/ Little/); await sleep(1500);
    ok('...Grown / Little again: little', await wait(2500, async () => (await gcount()) === 0));
    const pay = fs.readdirSync(`${DP}/p201/pay`).filter(f => /^mireling\d\.mcfunction$/.test(f)).map(f => fs.readFileSync(`${DP}/p201/pay/${f}`, 'utf8')).join('\n');
    ok('Queen Ava\'s honour for the Mireling takes 8 Brood Ichor in place of 8 Shadow Remnants (its rank\'s function)', /brood_ichor/.test(pay) && /shadow_remnant/.test(pay));
    await run('scoreboard players set TestRat bm.hn_mireling 0'); await run('scoreboard players set TestRat bm.cosml 0'); await run('kill @e[type=minecraft:wolf,tag=bm.mlpet]');
  }

  await clean(E, EX, EZ); await clean(O, OX, OZ);
  for (const k of Object.keys(keep)) await run(`scoreboard players set ${k} bm.cfg ${keep[k] === -99 ? 0 : keep[k]}`);
  await run('clear TestRat'); await run('tag TestRat remove bm.jam'); await run('tag TestRat remove bm.hsc');
  await run(`${E}tp TestRat ${EX + 0.5} ${Y + 1} ${EZ + 0.5}`);
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  await R.end(); process.exit(0);
})();
