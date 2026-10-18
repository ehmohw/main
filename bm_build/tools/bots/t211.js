// 2.82h: THE HEIST'S NETHER - with a regular (non-op) player TestRat standing by (rcon sets the stage: a patch of the gutter, a magma
// floor, heist monsters set down on it).
//   A heist monster on (or beside) a magma floor is fireproofed within a second and the floor doesn't hurt it; one on a plain floor
//   isn't. A baby heist piglin grows up within a second (a baby isn't hostile). The Golden Jockey's piglin rides in as an adult.
const fs = require('fs');
const { bot, rcon, sleep } = require('./lib_resp');
const OUT = (process.env.BM_OUT || __dirname + '/../../out_p2') + '/BlackMarket_DP/data/bm/function/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const G = 'execute in bm:gutter run ';
  const passes = async c => /passed/i.test(await run(c));
  const X = 6000, Y = 100, Z = 6000;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${G}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${G}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:polished_blackstone`);
  await run(`${G}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
  await run(`${G}fill ${X - 8} ${Y - 1} ${Z - 8} ${X - 2} ${Y - 1} ${Z + 8} minecraft:magma_block`);           // (the west half is a hot floor)
  await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat fire_resistance 900 0 true');
  await run(`${G}tp TestRat ${X + 5.5} ${Y} ${Z + 0.5}`); await sleep(1500);
  const mob = (tag, x) => run(`${G}summon minecraft:husk ${x} ${Y} ${Z + 0.5} {Tags:["bm.gvg","${tag}"],NoAI:1b,PersistenceRequired:1b,Health:20f}`);
  await mob('t211hot', X - 4.5); await mob('t211cold', X + 2.5);
  await run(`${G}summon minecraft:piglin ${X + 3.5} ${Y} ${Z + 3.5} {Tags:["bm.gvg","t211pig"],IsBaby:1b,NoAI:1b,PersistenceRequired:1b,IsImmuneToZombification:1b}`);
  await sleep(4000);
  const fr = async (t) => passes(`${G}execute if entity @e[tag=${t},nbt={active_effects:[{id:"minecraft:fire_resistance"}]}]`);
  const hp = async (t) => +(((await run(`${G}data get entity @e[tag=${t},limit=1] Health`)).match(/(-?[\d.]+)f/) || [0, -1])[1]);
  ok('a heist monster on the magma floor: fireproofed, and four seconds there leave it unhurt', (await fr('t211hot')) && (await hp('t211hot')) >= 20, `health ${await hp('t211hot')}`);
  ok('...one on a plain floor: not fireproofed', !(await fr('t211cold')));
  ok('a baby heist piglin is grown within seconds', await passes(`${G}execute if entity @e[tag=t211pig,nbt={IsBaby:0b}]`));
  const all = fs.readdirSync(OUT, { recursive: true }).filter(f => f.endsWith('.mcfunction')).flatMap(f => fs.readFileSync(OUT + f, 'utf8').split('\n'));
  const jk = all.filter(l => l.includes('Golden Jockey') && l.includes('summon minecraft:') && l.includes('minecraft:piglin'));   // (the roster's and the boss's)
  const babies = all.filter(l => l.includes('minecraft:piglin') && l.includes('IsBaby:1b'));
  ok('the Golden Jockey\'s piglin rides in as an adult, and no heist summons a baby piglin', jk.length >= 2 && !babies.length,
     `${jk.length} jockey lines, ${babies.length} baby piglin lines`);

  // ---- clean up
  await run(`${G}kill @e[tag=t211hot]`); await run(`${G}kill @e[tag=t211cold]`); await run(`${G}kill @e[tag=t211pig]`);
  await run(`${G}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
