// 2.80: THE HEIST'S CLIMAX - a Tier V heist (rcon sets the stage: a heist of one room kind, the plans bought, the vault
// reached). Walking into the vault: the guardian RISES - frozen, below the floor and shrunk, the hall dark - then stands at
// full size on the floor, free, with "The vault's guardian wakes" on the player's screen. Its fall OPENS THE VAULT as an
// event: the great gold door parts from the middle outward (the middle column first, the edges still gold), then it is
// all open, the way out swirls and "The vault is open" is on screen; the heist's music hushes for the vault's fanfare. The treasury dressed: chandeliers over the strongbox,
// candles on the gold, soul-lantern sconces, light enough to see the gold - and the strongbox ring still clear. A heist
// room dressed in its own look (2.80): the Lever Room's copper frieze, ceiling lights and pipework, above the trim only.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  const G = 'execute in bm:gutter run ';

  await heist('levers', 'a', 5); await begin();
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
  const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
  const atV = (cmd) => run(`execute in bm:gutter as ${V} at @s run ${cmd}`);
  const isBlock = async (x, y, z, bl) => /passed/i.test(await atV(`execute if block ${rel(x, y, z)} ${bl}`));
  const vy = +(((await run(`${G}data get entity ${V} Pos[1]`)).match(/(-?[\d.]+)d\s*$/) || [0, 0])[1]);
  const by = async () => +(((await run(`${G}data get entity ${B} Pos[1]`)).match(/(-?[\d.]+)d\s*$/) || [0, NaN])[1]);
  const tags = () => run(`${G}data get entity ${B} Tags`);
  const sz = async (what) => +(((await run(`${G}attribute ${B} minecraft:scale ${what}`)).match(/(-?[\d.]+)\s*$/) || [0, NaN])[1]);

  // ---- the treasury, dressed (before anything happens)
  ok('The treasury dressed: chandeliers over the strongbox (in the tier\'s own lanterns)', !(await isBlock(28, 12, 10, 'minecraft:air')) && await isBlock(32, 14, 14, 'minecraft:iron_chain'));
  ok('...candles lit on the gold piles, soul-lantern sconces on the walls', await isBlock(27, 7, 3, 'minecraft:candle') && await isBlock(28, 7, 1, 'minecraft:soul_lantern'));
  ok('...hidden lights over the gold, a glint of gems', await isBlock(27, 10, 4, 'minecraft:light') && await isBlock(29, 4, 2, 'minecraft:diamond_block'));
  ok('...and the strongbox ring and the way to it still clear', await isBlock(28, 4, 9, 'minecraft:light_weighted_pressure_plate') && await isBlock(26, 4, 12, 'minecraft:air') &&
     await isBlock(30, 4, 12, 'minecraft:gold_block') && await isBlock(34, 4, 12, 'minecraft:air'));

  // ---- a heist room dressed in its own look (the Lever Room: copper)
  const RQ = `@e[type=minecraft:marker,tag=bm.gvr_levers,scores={bm.gvi=${GI},bm.gvq=1},limit=1]`;
  const isR = async (x, y, z, bl) => /passed/i.test(await run(`execute in bm:gutter as ${RQ} at @s run execute if block ${rel(x, y, z)} ${bl}`));
  ok('A heist room dressed in its own look: a copper frieze above the trim, copper lights in the ceiling, pipes overhead',
     await isR(1, 10, 0, 'minecraft:waxed_cut_copper') && await isR(2, 15, 2, 'minecraft:waxed_copper_bulb') && await isR(5, 14, 3, 'minecraft:lightning_rod'));
  ok('...nothing below the trim touched: the levers on the wall, the floor clear', await isR(10, 5, 23, 'minecraft:lever') && await isR(12, 7, 23, 'minecraft:pale_oak_button') && await isR(12, 5, 12, '#minecraft:air'));

  // ---- the guardian rises
  A.titles.length = 0;
  await atV(`tp TestRat ${rel(6, 4, 12)} -90 0`);
  ok('Walk into the vault: the guardian is there', await wait(4000, async () => (await cnt(B)) === 1));
  ok('...rising: frozen, below the floor', /bm\.carr/.test(await tags()) && /bm\.cfrz/.test(await tags()) && (await by()) < vy - 0.5, `y ${await by()} (floor ${vy})`);
  ok('...shrunk, growing as it comes', (await sz('get')) < (await sz('base get')) * 0.8, `${await sz('get')} of ${await sz('base get')}`);
  ok('...the hall goes dark for the crew', /darkness/.test(await run('data get entity TestRat active_effects')));
  ok('..."The vault\'s guardian wakes" on the player\'s screen', await wait(5000, async () => A.titles.some(t => /guardian wakes/.test(t))), A.titles.join(' | ').slice(0, 100));
  ok('...then it stands on the floor at full size, free', await wait(3000, async () => !/bm\.cfrz/.test(await tags())) && Math.abs((await by()) - vy) < 0.3 &&
     Math.abs((await sz('get')) - (await sz('base get'))) < 0.01, `y ${await by()} scale ${await sz('get')} of ${await sz('base get')}`);

  // ---- its fall opens the vault
  A.titles.length = 0; const tk = Date.now();
  await run(`${G}data modify entity ${B} DeathLootTable set value "minecraft:empty"`);
  await run(`${G}kill ${B}`);
  const middle = await wait(4000, async () => await isBlock(24, 6, 12, 'minecraft:air'), 50);
  const edges = await isBlock(24, 6, 9, 'minecraft:gold_block') && await isBlock(24, 6, 15, 'minecraft:gold_block');
  ok('The guardian falls: the great door parts from the middle (its edges still gold)', middle && edges);
  ok('...then it is all open', await wait(4000, async () => await isBlock(24, 6, 9, 'minecraft:air') && await isBlock(24, 6, 15, 'minecraft:air') && await isBlock(24, 4, 12, 'minecraft:air')));
  ok('..."The vault is open" on the player\'s screen', await wait(3000, async () => A.titles.some(t => /vault is open/.test(t))), A.titles.join(' | ').slice(0, 100));
  ok('...the heist\'s music holds its breath as the door parts, and the vault\'s fanfare plays (on the jukebox channel)',
     A.stops.some(st => st.source === 1 && st.t >= tk) && await wait(3000, async () => A.sounds.some(x => x.name === 'bm:music.boss_vault' && x.cat === 2 && x.t >= tk)));
  await sleep(3000);
  ok('...no heist track over the fanfare', !A.sounds.some(x => /^bm:music\.gv_/.test(x.name) && x.t >= tk));
  ok('...then the heist\'s music comes back', await wait(9000, async () => A.sounds.some(x => /^bm:music\.gv_/.test(x.name) && x.t >= tk)));
  ok('...the way out swirls in the treasury', (await num(`execute in bm:gutter as ${V} at @s positioned ${rel(35, 4, 12)} store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.exitm,distance=..1.5]`)) === 1);
  ok('...and the sequence is over (the vault ready for the strongbox ring)', await wait(3000, async () => !/bm\.cvault/.test(await run(`${G}data get entity ${V} Tags`))) &&
     (await num(`${G}scoreboard players get ${V} bm.gvs`)) === 2);

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
