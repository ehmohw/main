// 2.79b: CALLING THE BOSSES - as a regular (non-op) player, every summon used as an item (rcon sets the stage: the arenas, the
// hour, the weather, the items in hand): the Horseman's Lantern by day - he comes, called, and stays though it's day; a second
// Lantern while he's out is refused (kept); the Smouldering Idol refused outside the Nether (kept); under a roof: refused (kept).
// The Pharaoh's Scarab by night: he comes and stays; the same Pharaoh uncalled sinks back at once (the hour still rules the
// uncalled). The Thunderhead Feather in clear weather: the Roc stays past the 10 s the clear sky allows. The Elder Acorn by day.
// The Smouldering Idol in the Nether and the Starless Eye in the End: the Colossus and the Voidwalker come. The Smouldering Gourd
// on an ordinary day: the Arachno-Lantern grows (dormant), called, and stays; uncalled it leaves. Then the haul's rolls (a won
// heist's finds, sampled): Tier V on a Blood Moon - summons and gourds both turn up; Tier II - neither; Tier V on an ordinary
// night - no gourds. And the vault's Tier V rare stores: diamonds, netherite scrap and a template among the tier's gear (the gear
// still the most of it); Tier II's: none of them.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ', N = 'execute in minecraft:the_nether run ', E = 'execute in minecraft:the_end run ';
  const cnt = async (sel, d = O) => { const m = (await run(`${d}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(600); };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const bossKinds = { hhm: ['wither_skeleton', 'p42/boss/retreat'], sph: ['husk', 'p53/sph/retreat'], roc: ['phantom', 'p53/roc/retreat'],
                      trt: ['creaking', 'p54/trt/retreat'], mcol: ['magma_cube', 'p54/mcol/retreat'], vwk: ['enderman', 'p54/vwk/retreat'] };
  const sel = (k, x = '') => `@e[type=minecraft:${bossKinds[k][0]},tag=bm.${k}${x}]`;
  const gone = async (k, d = O) => { await run(`${d}execute as ${sel(k)} at @s run function bm:${bossKinds[k][1]}`); await sleep(300); };
  const give = async (iid, slot = 0) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); await sleep(150); };
  // the stage: a flat floor high in the sky (Overworld), a cleared hall (the Nether), an end-stone floor (the End)
  const X = 17200, Y = 200, Z = 16000;
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y} ${Z + 30} minecraft:stone`);
  for (let y = Y + 1; y <= Y + 24; y += 6) await run(`${O}fill ${X - 30} ${y} ${Z - 30} ${X + 30} ${Math.min(y + 5, Y + 24)} ${Z + 30} minecraft:air`);
  for (const k of Object.keys(bossKinds)) await gone(k);
  await run(`${O}kill @e[type=minecraft:giant,tag=bm.salboss]`);
  await run('gamemode survival TestRat'); await run('clear TestRat');
  for (const e of ['resistance 900 4', 'fire_resistance 900 0', 'regeneration 900 2', 'saturation 900 0']) await run(`effect give TestRat minecraft:${e} true`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  await run('weather clear');

  // ---------------------------------------------------------------- the Horseman's Lantern, by day
  await run('time set 1000'); await sleep(1200);
  await give('sum_horseman'); await use(0);
  await wait(3000, async () => (await cnt(sel('hhm'))) === 1);
  ok('The Horseman\'s Lantern, by day: he rides out - called (bm.called), and the Lantern is spent', (await cnt(sel('hhm', ',tag=bm.called'))) === 1 && (await has('sum_horseman')) === 0,
     `${await cnt(sel('hhm'))} horseman`);
  await sleep(3500);
  ok('...and stays, though it\'s day (the dawn would send an uncalled one off)', (await cnt(sel('hhm'))) === 1);
  await give('sum_horseman'); await use(0);
  ok('A second Lantern while he\'s out: refused, and kept', (await cnt(sel('hhm'))) === 1 && (await has('sum_horseman')) === 1);
  await gone('hhm'); await run('clear TestRat');
  // the Idol outside the Nether; a roof over you
  await give('sum_colossus'); await use(0);
  ok('The Smouldering Idol in the Overworld: refused ("only in the Nether"), kept', (await cnt(sel('mcol'))) === 0 && (await has('sum_colossus')) === 1);
  await run('clear TestRat');
  await run(`${O}fill ${X - 1} ${Y + 4} ${Z - 1} ${X + 1} ${Y + 4} ${Z + 1} minecraft:stone`);
  await give('sum_treant'); await use(0);
  ok('Under a roof: refused ("it needs the open sky"), kept', (await cnt(sel('trt'))) === 0 && (await has('sum_treant')) === 1);
  await run(`${O}fill ${X - 1} ${Y + 4} ${Z - 1} ${X + 1} ${Y + 4} ${Z + 1} minecraft:air`); await run('clear TestRat');

  // ---------------------------------------------------------------- the Pharaoh's Scarab, by night (a day boss)
  await run('time set 18000'); await sleep(1500);
  await give('sum_pharaoh'); await use(0);
  await wait(3000, async () => (await cnt(sel('sph'))) === 1);
  await sleep(3000);
  ok('The Pharaoh\'s Scarab, by night: the Sand Pharaoh walks out - and stays, called, in the dark', (await cnt(sel('sph', ',tag=bm.called'))) === 1);
  await run(`${O}tag ${sel('sph')} remove bm.called`); await sleep(2500);
  ok('...the same Pharaoh uncalled: he sinks back at once (night still sends an uncalled one home)', (await cnt(sel('sph'))) === 0);
  await run('clear TestRat');

  // ---------------------------------------------------------------- the Thunderhead Feather, clear skies
  await give('sum_roc'); await use(0);
  await wait(4000, async () => (await cnt(sel('roc'))) === 1);
  ok('The Thunderhead Feather under a clear sky: the Storm Roc comes, called', (await cnt(sel('roc', ',tag=bm.called'))) === 1);
  await sleep(12500);
  ok('...and is still here after 12 s of clear sky (an uncalled Roc leaves after 10)', (await cnt(sel('roc'))) === 1);
  await gone('roc'); await run('clear TestRat');

  // ---------------------------------------------------------------- the Elder Acorn, by day (a night boss)
  await run('time set 1000'); await sleep(1500);
  await give('sum_treant'); await use(0);
  await wait(3000, async () => (await cnt(sel('trt'))) === 1);
  await sleep(3000);
  ok('The Elder Acorn by day: the Elder Treant walks out - and stays, called', (await cnt(sel('trt', ',tag=bm.called'))) === 1);
  await gone('trt'); await run('clear TestRat');

  // ---------------------------------------------------------------- the Smouldering Gourd, on an ordinary day
  await give('sum_lantern'); await use(0);
  const LAN = '@e[type=minecraft:giant,tag=bm.salboss]';
  await wait(3000, async () => (await cnt(LAN)) === 1);
  ok('The Smouldering Gourd: the Arachno-Lantern grows from it - called, the Gourd spent', (await cnt('@e[type=minecraft:giant,tag=bm.salboss,tag=bm.called]')) === 1 && (await has('sum_lantern')) === 0);
  await sleep(3000);
  ok('...and stays, though there\'s no Blood Moon', (await cnt(LAN)) === 1);
  await run(`${O}tag ${LAN} remove bm.called`); await sleep(2500);
  ok('...uncalled, without a Blood Moon, it leaves', (await cnt(LAN)) === 0);
  await run(`${O}kill @e[type=minecraft:giant,tag=bm.salboss]`); await run('clear TestRat');

  // ---------------------------------------------------------------- the Idol in the Nether, the Eye in the End
  const NX = 3000, NY = 100, NZ = 3000;
  await run(`${N}forceload add ${NX - 26} ${NZ - 26} ${NX + 26} ${NZ + 26}`);
  await run(`${N}fill ${NX - 24} ${NY - 1} ${NZ - 24} ${NX + 24} ${NY - 1} ${NZ + 24} minecraft:netherrack`);
  await run(`${N}fill ${NX - 24} ${NY} ${NZ - 24} ${NX + 24} ${NY + 6} ${NZ + 24} minecraft:air`);
  await run(`${N}fill ${NX - 24} ${NY + 7} ${NZ - 24} ${NX + 24} ${NY + 7} ${NZ + 24} minecraft:netherrack`);
  await run(`${N}tp TestRat ${NX + 0.5} ${NY} ${NZ + 0.5} 0 0`); await sleep(3000);
  await gone('mcol', N);
  await give('sum_colossus'); await use(0);
  await wait(3000, async () => (await cnt(sel('mcol'), N)) === 1);
  ok('The Smouldering Idol in the Nether: the Magma Colossus rises - called, the Idol spent', (await cnt(sel('mcol', ',tag=bm.called'), N)) === 1 && (await has('sum_colossus')) === 0);
  await gone('mcol', N); await run('clear TestRat');
  const EX = 1000, EY = 100, EZ = 1000;
  await run(`${E}forceload add ${EX - 26} ${EZ - 26} ${EX + 26} ${EZ + 26}`);
  await run(`${E}fill ${EX - 24} ${EY - 1} ${EZ - 24} ${EX + 24} ${EY - 1} ${EZ + 24} minecraft:end_stone`);
  await run(`${E}fill ${EX - 24} ${EY} ${EZ - 24} ${EX + 24} ${EY + 8} ${EZ + 24} minecraft:air`);
  await run(`${E}tp TestRat ${EX + 0.5} ${EY} ${EZ + 0.5} 0 0`); await sleep(3000);
  await gone('vwk', E);
  await give('sum_voidwalker'); await use(0);
  await wait(3000, async () => (await cnt(sel('vwk'), E)) === 1);
  ok('The Starless Eye in the End: the Voidwalker steps in - called, the Eye spent', (await cnt(sel('vwk', ',tag=bm.called'), E)) === 1 && (await has('sum_voidwalker')) === 0);
  await gone('vwk', E); await run('clear TestRat');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);

  // ---------------------------------------------------------------- the haul's rolls, sampled (a won heist's finds, as the raider)
  const G = 'execute in bm:gutter run ', HA = '-200 64 -197', HB = '-198 64 -197';
  for (const b of [HA, HB]) await run(`${G}setblock ${b} minecraft:barrel`);
  const SUMS = ['sum_horseman', 'sum_pharaoh', 'sum_roc', 'sum_treant', 'sum_colossus', 'sum_voidwalker'];
  const inBarrels = async (iid) => { let n = 0; for (const b of [HA, HB]) { const m = (await run(`${G}execute if items block ${b} container.* *[minecraft:custom_data~{bm:"${iid}"}]`)).match(/count: (\d+)/i); n += m ? +m[1] : 0; } return n; };
  const sample = async (tier, night, runs) => {
    let s = 0, g = 0;
    await run(`scoreboard players set #gt bm.rng ${tier}`); await run(`scoreboard players set #gn bm.rng ${night}`);
    for (let i = 0; i < runs; i += 10) {
      for (const b of [HA, HB]) await run(`${G}data remove block ${b} Items`);
      // (#gt and #gn are shared scratch - other ticking functions use #gt too - so set them right before every roll, as the payout does)
      for (let j = 0; j < 10; j++) {
        await run(`scoreboard players set #gt bm.rng ${tier}`); await run(`scoreboard players set #gn bm.rng ${night}`);
        await run('execute as TestRat at @s run function bm:p105/finds');
      }
      for (const iid of SUMS) s += await inBarrels(iid);
      g += await inBarrels('sum_lantern');
    }
    for (const b of [HA, HB]) await run(`${G}data remove block ${b} Items`);
    return [s, g];
  };
  const [s5, g5] = await sample(5, 1, 300);
  ok('Tier V, a Blood Moon heist, 300 wins sampled: summons turn up (5% a win) and so do gourds (5%)', s5 >= 4 && s5 <= 32 && g5 >= 4 && g5 <= 32, `${s5} summons, ${g5} gourds`);
  const [s2, g2] = await sample(2, 1, 200);
  ok('Tier II (Blood Moon too), 200 wins: no summons, no gourds (Tier III and up only)', s2 === 0 && g2 === 0, `${s2} summons, ${g2} gourds`);
  const [s3n, g3n] = await sample(5, 0, 200);
  ok('Tier V on an ordinary night, 200 wins: summons, but never a gourd (Blood Moon only)', g3n === 0 && s3n >= 1, `${s3n} summons, ${g3n} gourds`);
  await run('scoreboard players set #gn bm.rng 0');

  // ---------------------------------------------------------------- the vault's rare stores
  await run(`${O}setblock ${X + 3} ${Y + 1} ${Z} minecraft:chest`);
  const store = async (t, n) => {
    const tot = { diamond: 0, netherite_scrap: 0, netherite_upgrade_smithing_template: 0, gear: 0 };
    for (let i = 0; i < n; i += 20) {
      await run(`${O}data remove block ${X + 3} ${Y + 1} ${Z} Items`);
      for (let j = 0; j < 20; j++) await run(`${O}loot insert ${X + 3} ${Y + 1} ${Z} loot bm:p105/rare_t${t}`);
      for (const k of ['diamond', 'netherite_scrap', 'netherite_upgrade_smithing_template']) {
        const m = (await run(`${O}execute if items block ${X + 3} ${Y + 1} ${Z} container.* minecraft:${k}`)).match(/count: (\d+)/i); tot[k] += m ? +m[1] : 0;
      }
      const m = (await run(`${O}execute if items block ${X + 3} ${Y + 1} ${Z} container.* *[minecraft:custom_data]`)).match(/count: (\d+)/i); tot.gear += m ? +m[1] : 0;
    }
    return tot;
  };
  const r5 = await store(5, 300);
  ok('The Tier V rare stores (300 rolls): diamonds, netherite scrap and a template turn up - the tier\'s gear still the most of it', r5.diamond > 0 && r5.netherite_scrap > 0 && r5.netherite_upgrade_smithing_template > 0 && r5.gear > 120,
     JSON.stringify(r5));
  const r2 = await store(2, 100);
  ok('...the Tier II stores (100 rolls): none of them', r2.diamond + r2.netherite_scrap + r2.netherite_upgrade_smithing_template === 0 && r2.gear === 100, JSON.stringify(r2));
  await run(`${O}setblock ${X + 3} ${Y + 1} ${Z} minecraft:air`);

  await run('time set 1000'); await run('clear TestRat');
  for (const f of [`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`, `${N}forceload remove ${NX - 26} ${NZ - 26} ${NX + 26} ${NZ + 26}`,
                   `${E}forceload remove ${EX - 26} ${EZ - 26} ${EX + 26} ${EZ + 26}`]) await run(f);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
