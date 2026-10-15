// 2.80: THE DUNGEON BOSSES, STAGED - the Broodmother's fight as a regular (non-op) player in a freshly placed Brood Nest (rcon
// only sets the stage: the dungeon placed, its puzzles marked solved, a conquest record, the key in hand, her health brought to
// a threshold). Kneeling at the altar with the key: the intro runs, then she MATERIALISES (frozen, a tenth of her size,
// growing out of a column of silk; the bar up) and only then moves - armed, the bar reading her true health. Below her
// rage line she freezes for a moment, then rages. Her web spit is telegraphed (a gather and a hiss) before the web lands
// on the player. Brought down by the player's sword she DIES as a sequence - frozen, curling up, the bar gone, still there
// seconds later - then falls: her loot on the floor, "The Broodmother has fallen" on the player's screen, the way out open.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => { const r = await run(cmd); const m = r.match(/has (-?\d+) \[/) || r.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/); return m ? +m[1] : NaN; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const eidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  // the stage: a Brood Nest placed far out
  const X = 23000, Z = 23000;
  await run(`${O}forceload add ${X - 96} ${Z - 96} ${X + 96} ${Z + 96}`); await sleep(1500);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=64,z=${Z},distance=..220]`); await sleep(300);    // (a run before this one: its markers)
  await run('bossbar set bm:boss_brood visible false');
  const pl = await run(`${O}place structure bm:p2_brood ${X} 64 ${Z}`);
  ok('A Brood Nest places', /Generated/i.test(pl), pl.slice(0, 100));
  await sleep(1500);
  const near = `x=${X},y=64,z=${Z},distance=..220`;
  const DG = `@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_brood,${near},sort=nearest,limit=1]`;
  const ALT = `@e[type=minecraft:marker,tag=bm.altar,tag=bm.d_brood,${near},sort=nearest,limit=1]`;
  const ARN = `@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_brood,${near},sort=nearest,limit=1]`;
  const BOSS = `@e[type=minecraft:spider,tag=bm.boss_brood,${near},limit=1]`;
  ok('...its altar and arena are there', (await cnt(ALT)) === 1 && (await cnt(ARN)) === 1);
  await run(`${O}scoreboard players set ${DG} bm.pz 3`);
  await run('scoreboard players set TestRat bm.conq 0');
  await run('gamemode survival TestRat'); await run('clear TestRat');
  for (const e of ['resistance 600 4', 'regeneration 600 3', 'saturation 600 0', 'fire_resistance 600 0']) await run(`effect give TestRat minecraft:${e} true`);
  await run('difficulty normal');
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/key_brood'); await sleep(200);
  await run(`${O}execute at ${ALT} run tp TestRat ~1 ~ ~ facing entity ${ALT} feet`); await sleep(800); A.stand();
  A.titles.length = 0;
  A.input({ shift: true }); await sleep(1500); A.input({}); await sleep(300);
  ok('Kneeling at the altar with her key: the fight begins (the intro)', await wait(3000, async () => (await num(`${O}scoreboard players get ${ARN} bm.bs`)) >= 1),
     `bs ${await num(`${O}scoreboard players get ${ARN} bm.bs`)}`);
  // ---- she materialises
  ok('...after the intro she is there', await wait(6000, async () => (await cnt(BOSS)) === 1, 100));
  const tg = async () => run(`${O}data get entity ${BOSS} Tags`);
  const sc = async () => num(`${O}attribute ${BOSS} minecraft:scale base get`);
  const hp = async () => num(`${O}data get entity ${BOSS} Health`);
  const buf = async () => num(`${O}scoreboard players get ${BOSS} bm.cbuf`);
  ok('...materialising: frozen, and small, growing', /bm\.carr/.test(await tg()) && /bm\.cfrz/.test(await tg()) && (await sc()) < 2.0, `scale ${await sc()}`);
  ok('...then at full size, free, armed', await wait(4000, async () => { const t = await tg(); return /bm\.carm/.test(t) && !/bm\.cfrz/.test(t); }) && Math.abs((await sc()) - 3.0) < 0.05,
     `scale ${await sc()}`);
  ok('...her bar up, reading her true health (360)', await wait(2500, async () => (await num('bossbar get bm:boss_brood value')) === 360 &&
     /currently visible/.test(await run('bossbar get bm:boss_brood visible'))), `bar ${await num('bossbar get bm:boss_brood value')} health ${await hp()} buffer ${await buf()}`);
  // ---- her web spit, telegraphed
  await run(`${O}execute at ${ARN} run tp TestRat ~3 ~ ~`); await sleep(1500);      // (in the arena, among her targets)
  await run(`${O}scoreboard players set ${BOSS} bm.at 7`);
  ok('Her web spit: she gathers herself first (the wind-up)', await wait(2500, async () => /bm\.cwind/.test(await tg()), 100));
  ok('...then the web lands on the player', await wait(3000, async () => /passed/i.test(await run(`${O}execute at TestRat if block ~ ~ ~ minecraft:cobweb`)), 100));
  await run(`${O}execute at TestRat run fill ~-1 ~ ~-1 ~1 ~1 ~1 minecraft:air replace minecraft:cobweb`);
  // ---- her rage, a moment
  await run(`${O}data modify entity ${BOSS} Health set value ${(await buf()) + 170}f`);
  ok('Below her rage line: she freezes for the moment', await wait(2500, async () => { const t = await tg(); return /bm\.crage/.test(t) && /bm\.cfrz/.test(t); }, 100));
  ok('...then rages, free again', await wait(4000, async () => { const t = await tg(); return /bm\.rage/.test(t) && !/bm\.cfrz/.test(t); }));
  // ---- her death, by the player's sword
  await run(`${O}kill @e[type=minecraft:item,${near}]`);
  await run(`${O}data merge entity ${BOSS} {NoAI:1b}`);
  await run(`${O}execute at ${ARN} run tp ${BOSS} ~ ~ ~`); await sleep(300);
  await run(`${O}data modify entity ${BOSS} Health set value ${(await buf()) + 1}f`);
  await run(`${O}execute at ${BOSS} run tp TestRat ~2.6 ~ ~ facing entity ${BOSS} eyes`);
  await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword'); await sleep(1300);
  A.titles.length = 0;
  const id = await eidOf(BOSS); if (id) A.attack(id); await sleep(300);
  ok('The player\'s blow brings her down: her death begins (frozen)', await wait(1500, async () => /bm\.cdie/.test(await tg()) && /bm\.cfrz/.test(await tg()), 100), `eid ${id} health ${await hp()}`);
  ok('...her bar gone', await wait(1500, async () => /hidden/.test(await run('bossbar get bm:boss_brood visible'))));
  await sleep(1800);
  ok('...still there, curling up, two seconds on', (await cnt(BOSS)) === 1 && (await sc()) < 2.9, `scale ${await sc()}`);
  ok('...then she falls', await wait(5000, async () => (await cnt(BOSS)) === 0));
  ok('..."The Broodmother has fallen" on the player\'s screen', await wait(3000, async () => A.titles.some(t => /Broodmother has fallen/.test(t))), A.titles.join(' | ').slice(0, 100));
  ok('...her loot on the floor (the player\'s kill)', await wait(2000, async () => (await cnt(`@e[type=minecraft:item,${near}]`)) > 0));
  ok('...and the death leaves no marker behind', await wait(3000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.cpos_d,${near}]`)) === 0));

  await run(`${O}kill @e[type=!minecraft:player,type=!minecraft:marker,${near}]`);
  await run('effect clear TestRat'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 96} ${Z - 96} ${X + 96} ${Z + 96}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
