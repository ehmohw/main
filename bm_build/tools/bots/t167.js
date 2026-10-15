// 2.79c: THE HEX CHAPEL'S WITCHES - the second trial spawner in the Hex Cathedral's nave was built over by a pew row, so it
// never existed. As a regular (non-op) player in a freshly placed Hex dungeon (rcon places it and sets the stage): the witch
// spawner stands among the pews (bm:hex/witches, its ominous twin), the vindicator spawner too; walking up to it, witches come
// (dungeon mobs). Then an old dungeon (the spawner missing, the 2.79c patch not yet run): with the player near, it's put back.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // the stage: a Hex Cathedral placed far out (its marker turns with it: the template offsets are ^left ^up ^forward from it)
  const X = 21000, Z = 21000;
  await run(`${O}forceload add ${X - 96} ${Z - 96} ${X + 96} ${Z + 96}`); await sleep(1500);
  const pl = await run(`${O}place structure bm:p2_hex ${X} 64 ${Z}`);
  ok('A Hex Cathedral places', /Generated/i.test(pl), pl.slice(0, 120));
  await sleep(1500);
  const DG = `@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_hex,x=${X},y=0,z=${Z},distance=..220,sort=nearest,limit=1]`;
  ok('...its dungeon marker is there', /passed/i.test(await run(`${O}execute if entity ${DG}`)));
  const at = (dx, dy, dz) => `${O}execute as ${DG} at @s rotated ~ 0 positioned ^${dx} ^${dy} ^${dz} `;
  const WIT = [6, -8, -23], VIN = [-6, -8, -26];             // (template (30,6,17) and (18,6,14), from the marker at (24,14,40))
  const isSpawner = async ([dx, dy, dz], cfg) => /passed/i.test(await run(at(dx, dy, dz) + 'if block ~ ~ ~ minecraft:trial_spawner')) &&
    new RegExp(`bm:hex/${cfg}"`).test(await run(at(dx, dy, dz) + 'run data get block ~ ~ ~ normal_config'));
  ok('The witch spawner stands in the nave, among the pews (bm:hex/witches)', await isSpawner(WIT, 'witches'),
     await run(at(...WIT) + 'run data get block ~ ~ ~ normal_config'));
  ok('...with its ominous twin', /bm:hex\/witches_ominous/.test(await run(at(...WIT) + 'run data get block ~ ~ ~ ominous_config')));
  ok('...and the vindicator spawner still on the other side', await isSpawner(VIN, 'vindicators'));

  // the player walks up to it: witches come
  await run('gamemode survival TestRat'); await run('clear TestRat');
  for (const e of ['resistance 300 4', 'regeneration 300 2', 'saturation 300 0', 'fire_resistance 300 0']) await run(`effect give TestRat minecraft:${e} true`);
  await run(`${O}kill @e[type=minecraft:witch,x=${X},y=0,z=${Z},distance=..220]`);
  await run('difficulty normal');
  await run(at(WIT[0], WIT[1], WIT[2] + 3) + 'run tp TestRat ~ ~ ~'); await sleep(500); A.stand();
  const witches = async () => +(((await run(at(...WIT) + 'if entity @e[type=minecraft:witch,tag=bm.dgmob,distance=..14]')).match(/count: (\d+)/i) || [0, 0])[1]);
  ok('Walking up to it: witches come (dungeon mobs)', await wait(20000, async () => (await witches()) > 0), `${await witches()} witches`);

  // an old dungeon: the spawner missing - the patch puts it back once the player is near
  await run(`${O}kill @e[type=minecraft:witch,x=${X},y=0,z=${Z},distance=..220]`);
  await run(at(...WIT) + 'run setblock ~ ~ ~ minecraft:air'); await run(`${O}tag ${DG} remove bm.hexw79`);
  ok('(an old Hex dungeon: no witch spawner)', !(await isSpawner(WIT, 'witches')));
  ok('With the player near, the 2.79c patch puts it back', await wait(5000, async () => await isSpawner(WIT, 'witches')));
  ok('...once (the dungeon is marked done)', /passed/i.test(await run(`${O}execute if entity ${DG.replace(']', ',tag=bm.hexw79]')}`)));
  await run(at(...WIT) + 'run setblock ~ ~ ~ minecraft:air'); await sleep(2500);
  ok('...and a broken one stays broken (it doesn\'t come back again)', !(await isSpawner(WIT, 'witches')));

  await run(`${O}kill @e[type=minecraft:witch,x=${X},y=0,z=${Z},distance=..220]`);
  await run(`${O}kill @e[type=minecraft:vindicator,x=${X},y=0,z=${Z},distance=..220]`);
  await run(`${O}forceload remove ${X - 96} ${Z - 96} ${X + 96} ${Z + 96}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
