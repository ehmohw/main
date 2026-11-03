// 3.0g: THE UNDERCROWN IN ITS LAVA LAKE, AND NOTHING BUILT ON IT (phase237 p237/lake, p2/underroad, settle.py), as a regular (non-op)
// player. rcon sets the stage: the Summons' want, foreign things planted in the box (an Ember Rat's Outpost's marker and bricks,
// the dirt its settling banked into a hall, a cave in the box's skin), the Undercrown asked to carve its lake again
// (/function bm:admin/under/lake), and an Ember Rat's seed dropped on the lake; it checks the blocks. The bot is in the Nether
// throughout and walks into the court: Adventure mode, said once.
//   - the lake: lava at the Nether's lava sea (y 31) and below it, open air above, on every side of the box; the old cave in
//     the box's skin is rock now; the foreign bricks and dirt in its Nether cells are netherrack; the outpost's marker gone;
//   - the forecourts on blackstone plinths out of the lava, walled round; each road's causeway (deck, parapets, piers) to the
//     far shore, and both roads' ends marked;
//   - an Ember Rat's seed on the lake: gone, and nothing built;
//   - an Ember Rat's Outpost built in a biome no vanilla tag names (the Undercrown's own, far off): on netherrack, never grass
//     or dirt.
//   node t336.js [lake|seed|settle]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OX = 2560, OY = 6, OZ = -2560;                       // (p2/undercfg.ORIGIN)
const N = 'execute in minecraft:the_nether run ';
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${N}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const block = async (x, y, z, b) => /passed/.test(await run(`${N}execute if block ${x} ${y} ${z} ${b}`));
  const L = (x, y, z) => [OX + x, OY + y, OZ + z];              // (local -> world)
  // (how many of a block a box holds: turned to structure voids and straight back, counted)
  const count = async (x1, y1, z1, x2, y2, z2, b) => {
    const per = Math.max(1, Math.floor(32768 / ((x2 - x1 + 1) * (z2 - z1 + 1)))); let n = 0;      // (a fill's limit: in slices along y)
    for (let y = y1; y <= y2; y += per) { const yb = Math.min(y2, y + per - 1);
      const m = (await run(`${N}fill ${x1} ${y} ${z1} ${x2} ${yb} ${z2} minecraft:structure_void replace ${b} strict`)).match(/(\d+) block/);
      await run(`${N}fill ${x1} ${y} ${z1} ${x2} ${yb} ${z2} ${b} replace minecraft:structure_void strict`); n += m ? +m[1] : 0; }
    return n; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass'); await run('gamemode survival TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('effect give TestRat minecraft:slow_falling infinite 0 true');

  if (on('lake')) {
    // ---- the stage: the Undercrown placed (any version), then foreign things in its box, and its lake asked for again
    if ((await sc('#uver', 'bm.p2')) < 1) await run('function bm:admin/under/place');
    ok('the Undercrown is placed in the Nether', await wait(400000, async () => (await sc('#uver', 'bm.p2')) >= 1, 2000));
    await wait(400000, async () => (await sc('#uver', 'bm.p2')) === 8, 2000);       // (an older copy rebuilds itself first)
    await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`); await sleep(3000);
    const C1 = L(53, 57, 174), C2 = L(158, 80, 141), SK = L(0, 39, 40);        // (two cells the Undercrown leaves to the Nether; one in its skin)
    await run(`${N}setblock ${C1.join(' ')} minecraft:dirt`); await run(`${N}setblock ${C2.join(' ')} minecraft:nether_bricks`);
    await run(`${N}fill ${SK[0]} ${SK[1]} ${SK[2]} ${SK[0] + 3} ${SK[1] + 2} ${SK[2] + 2} minecraft:air`);
    await run(`${N}summon minecraft:marker ${OX + 100.5} ${OY + 60} ${OZ + 100.5} {Tags:["bm.outpost","bm.t336"]}`);
    ok('...the stage: dirt and bricks in its Nether cells, a cave in its skin, an outpost\'s marker in it',
       await block(...C1, 'minecraft:dirt') && await block(...C2, 'minecraft:nether_bricks') && await block(...SK, 'minecraft:air') && (await cnt('@e[type=minecraft:marker,tag=bm.t336]')) === 1);
    await run('function bm:admin/under/lake');
    await run(`${N}tp TestRat ${OX + 214.5} ${OY + 72} ${OZ + 210.5}`); await sleep(2000); A.stand();
    ok('...the lake is carved and the Undercrown re-placed (#ulake 1, #uver 8)',
       await wait(600000, async () => (await sc('#ulake', 'bm.p2')) === 1 && (await sc('#uver', 'bm.p2')) === 8, 2000), `ulake ${await sc('#ulake', 'bm.p2')} ulk ${await sc('#ulk', 'bm.p2')}`);
    await sleep(2000);
    for (const q of [[OX - 70, OZ - 70, OX + 111, OZ + 111], [OX + 112, OZ - 70, OX + 293, OZ + 111], [OX - 70, OZ + 112, OX + 111, OZ + 293], [OX + 112, OZ + 112, OX + 293, OZ + 293]])
      await run(`${N}forceload add ${q.join(' ')}`);
    await sleep(4000);

    // ---- the lake, round all four sides
    const sides = { west: [-30, 112], north: [112, -30], east: [300 - 40, 40], south: [40, 300 - 40] };
    const lk = []; let all = true;
    for (const [nm, [x, z]] of Object.entries(sides)) {
      const [wx, , wz] = L(x, 0, z);
      const g = await block(wx, 31, wz, 'minecraft:lava') && await block(wx, 20, wz, 'minecraft:lava') && await block(wx, 32, wz, 'minecraft:air') && await block(wx, 80, wz, 'minecraft:air');
      lk.push(`${nm} ${g ? 'lava/air' : 'NOT'}`); all = all && g;
    }
    ok('a lava lake on every side: lava at y 31 and 20, open air at 32 and 80', all, lk.join('; '));
    ok('...the cave in the box\'s skin is rock again', await block(...SK, 'minecraft:netherrack'));
    ok('...the dirt and the bricks in its Nether cells are netherrack', await block(...C1, 'minecraft:netherrack') && await block(...C2, 'minecraft:netherrack'));
    ok('...the outpost\'s marker taken', (await cnt('@e[type=minecraft:marker,tag=bm.t336]')) === 0);
    ok('...the court is the Undercrown\'s own again (its air, its floor)', await block(...L(214, 73, 200), 'minecraft:air') && !(await block(...L(214, 71, 200), 'minecraft:air')));

    // ---- the forecourts and the causeways
    ok('the east forecourt stands on a blackstone plinth out of the lava', await block(...L(240, 34, 190), 'minecraft:blackstone') && await block(...L(240, 60, 200), 'minecraft:blackstone'));
    ok('...walled where it looks out over the lake', await block(...L(240, 72, 174), 'minecraft:polished_blackstone_brick_wall') && await block(...L(240, 72, 214), 'minecraft:polished_blackstone_brick_wall'));
    let deck = 0, gaps = [];
    for (let x = 264; x <= 278; x++) { if (await block(...L(x, 71, 194), 'minecraft:red_nether_bricks') && await block(...L(x, 71, 190), 'minecraft:polished_blackstone_bricks')) deck++; else gaps.push(x); }
    ok('the east road\'s causeway: its deck all the way to the far shore (x 264-278)', deck === 15, `gaps ${gaps.join(',')}`);
    ok('...parapets either side, and a pier down to the lake\'s bed', await block(...L(270, 72, 188), 'minecraft:polished_blackstone_brick_wall') &&
       await block(...L(270, 72, 200), 'minecraft:polished_blackstone_brick_wall') && await block(...L(267, 40 - OY, 188), 'minecraft:polished_blackstone_bricks'));
    deck = 0; gaps = [];
    for (let z = 264; z <= 275; z++) { if (await block(...L(213, 71, z), 'minecraft:red_nether_bricks')) deck++; else gaps.push(z); }
    ok('the south road\'s causeway: its deck to the far shore (z 264-275)', deck === 12, `gaps ${gaps.join(',')}`);
    ok('...both roads end at a marked landing (or their run\'s end)', (await cnt('@e[type=minecraft:marker,tag=bm.uroadend]')) === 2);
    ok('no grass or dirt anywhere on the east forecourt', (await count(...L(224, 60, 174), ...L(263, 75, 214), 'minecraft:grass_block')) +
       (await count(...L(224, 60, 174), ...L(263, 75, 214), 'minecraft:dirt')) === 0);

    // ---- the bot in the court: Adventure, said once (out of it a few seconds first: Survival again)
    await run(`${N}tp TestRat ${OX - 30.5} 90 ${OZ + 112.5}`); await sleep(6000); A.stand();
    A.bars.length = 0;
    await run(`${N}tp TestRat ${OX + 214.5} ${OY + 72} ${OZ + 210.5}`); await sleep(1500); A.stand();
    const gm = async () => ((await run('data get entity TestRat playerGameType')).match(/(-?\d+)$/) || [])[1];
    ok('TestRat in the court: Adventure mode', await wait(5000, async () => (await gm()) === '2', 250));
    await sleep(8000);
    ok('...its word on the action bar once, not again and again', A.bars.filter(b => /will not break|cannot be broken/.test(b)).length === 1, `${A.bars.filter(b => /break/.test(b)).length} times`);
  }

  if (on('seed')) {
    // ---- an Ember Rat's seed on the lake: never built
    if ((await sc('#ulake', 'bm.p2')) === 1) {
      const [sx, , sz] = L(-30, 0, 112);
      await run(`${N}forceload add ${sx - 40} ${sz - 40} ${sx + 40} ${sz + 40}`);
      await run(`${N}tp TestRat ${sx + 0.5} 90 ${sz + 0.5}`); await sleep(2500); A.stand();
      await run(`${N}summon minecraft:marker ${sx + 0.5} 70 ${sz + 0.5} {Tags:["bm.p200seed","bm.p200seed_ember_outpost"]}`);
      ok('an Ember Rat\'s seed dropped on the lake: gone within seconds', await wait(8000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.p200seed,x=${sx},y=70,z=${sz},distance=..3]`)) === 0, 500));
      ok('...and nothing built (no outpost)', (await cnt(`@e[type=minecraft:marker,tag=bm.outpost,x=${sx},y=60,z=${sz},distance=..60]`)) === 0 &&
         (await count(sx - 20, 25, sz - 20, sx + 20, 60, sz + 20, 'minecraft:nether_bricks')) === 0);
    } else ok('(seed) the lake isn\'t carved yet - run the lake section first', false);
  }

  if (on('settle')) {
    // ---- an Ember Rat's Outpost in the Undercrown's own biome, far off: settled on netherrack
    const X = -3000, Y = 60, Z = -3000;
    await run(`${N}forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`); await sleep(2500);
    await run(`${N}fill ${X - 30} ${Y - 12} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:netherrack`);
    await run(`${N}fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 14} ${Z + 30} minecraft:air`);
    await run(`${N}fill ${X - 30} ${Y - 8} ${Z - 30} ${X + 30} ${Y - 4} ${Z + 30} minecraft:air`);      // (a hollow under it: the settling banks it up)
    await run(`${N}fillbiome ${X - 30} ${Y - 12} ${Z - 30} ${X + 30} ${Y + 14} ${Z + 30} bm:undercrown`);
    await run(`${N}tp TestRat ${X + 0.5} ${Y + 20} ${Z + 0.5}`); await sleep(2000); A.stand();
    await run(`${N}execute positioned ${X} ${Y} ${Z} run function bm:p200/ember_outpost/place`); await sleep(1500);
    ok('an Ember Rat\'s Outpost built in the Undercrown\'s biome', (await cnt(`@e[type=minecraft:marker,tag=bm.outpost,x=${X},y=${Y},z=${Z},distance=..30]`)) === 1);
    const g = await count(X - 30, Y - 12, Z - 30, X + 30, Y + 14, Z + 30, 'minecraft:grass_block'), d = await count(X - 30, Y - 12, Z - 30, X + 30, Y + 14, Z + 30, 'minecraft:dirt');
    ok('...its ground settled in netherrack: no grass, no dirt', g === 0 && d === 0, `grass ${g} dirt ${d}`);
    await run(`${N}execute as @e[type=minecraft:wandering_trader,tag=bm.orat,x=${X},y=${Y},z=${Z},distance=..40] at @s run tp @s ~ -300 ~`);
    await run(`${N}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  }

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
