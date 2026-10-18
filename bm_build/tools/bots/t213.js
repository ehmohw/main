// 2.82k: ADVENTURE MODE ABOARD THE SHIPS, AND ZORP'S EMPTY HANDS - as a regular (non-op) player TestRat (rcon sets the stage: a
// mothership and a Vorn Dreadnought placed in the sky, TestRat stood on their decks, a milk bucket put in Zorp's hand).
//   Aboard a mothership: TestRat is put in adventure mode within a couple of seconds (with a word), and digging the deck (real
//   dig packets) leaves it whole. Away from the ship: back to survival. The same aboard a Dreadnought. And a trader NPC left
//   holding something (Zorp, with a bucket in front of his face) has his hands emptied within a second or two.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const mode = async m => passes(`execute if entity @a[name=TestRat,gamemode=${m}]`);
  const Y = 100;
  const SHIPS = [['mothership', 31000, 31000, 'place_mothership', 'bm.tbeam'], ['Dreadnought', 31200, 31000, 'place_dreadnought', 'bm.tbeam_red']];

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:slow_falling 900 0 true');

  for (const [nm, X, Z, place, tag] of SHIPS) {
    await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
    await run(`${O}fill ${X - 2} ${Y - 1} ${Z - 2} ${X + 2} ${Y - 1} ${Z + 2} minecraft:stone`);
    await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/${place}`); await sleep(1500);
    const placed = await passes(`${O}execute positioned ${X} ${Y + 45} ${Z} if entity @e[type=minecraft:marker,tag=${tag},distance=..2]`);
    // ---- on the ground under it: survival
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(2500); A.stand();
    ok(`${nm} placed overhead; on the ground below it TestRat is still in survival`, placed && (await mode('survival')));
    // ---- aboard: find a deck floor block near the beam, stand on it
    let deck = null;
    for (const [dx, dz] of [[6, 0], [-6, 0], [0, 6], [0, -6], [8, 3], [-8, -3]]) {
      for (let y = Y + 56; y > Y + 42 && !deck; y--) {
        if ((await passes(`${O}execute unless block ${X + dx} ${y} ${Z + dz} #minecraft:replaceable unless block ${X + dx} ${y} ${Z + dz} #minecraft:climbable if block ${X + dx} ${y + 1} ${Z + dz} minecraft:air if block ${X + dx} ${y + 2} ${Z + dz} minecraft:air`))) deck = [X + dx, y, Z + dz];
      }
      if (deck) break;
    }
    A.bars.length = 0;
    await run(`${O}tp TestRat ${deck[0] + 0.5} ${deck[1] + 1} ${deck[2] + 0.5}`); await sleep(500); A.stand();
    const adv = await wait(4000, () => mode('adventure'), 300);
    ok(`aboard the ${nm} (deck at y ${deck[1]}): TestRat is put in adventure mode, with a word`, adv && A.bars.some(b => /Aboard the ship/.test(b)), A.bars.slice(-1).join(''));
    // ---- digging the deck under them: it stays
    const blk = (await run(`${O}data get block ${deck[0]} ${deck[1]} ${deck[2]}`)).length;
    const before = await run(`${O}execute if block ${deck[0]} ${deck[1]} ${deck[2]} minecraft:air`);
    await A.mine(deck[0], deck[1], deck[2], 1500); await sleep(600);
    ok(`...digging the ${nm}'s deck (real dig packets) leaves it whole`, /failed/i.test(before) && !(await passes(`${O}execute if block ${deck[0]} ${deck[1]} ${deck[2]} minecraft:air`)), `${blk}`);
    // ---- away from the ship: survival again
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 60.5}`); await run(`${O}fill ${X - 1} ${Y - 1} ${Z + 59} ${X + 1} ${Y - 1} ${Z + 61} minecraft:stone`);
    await sleep(500); A.stand();
    ok(`...walked away from the ${nm}: back to survival`, await wait(4000, () => mode('survival'), 300));
  }

  // ---- Zorp's hands: a bucket put in them is gone within a second or two
  const [, X, Z] = SHIPS[0];
  await run(`${O}summon minecraft:wandering_trader ${X + 0.5} ${Y} ${Z + 3.5} {NoAI:1b,Tags:["bm.npc","bm.npc_alien","t213z"],Silent:1b,Invulnerable:1b}`);
  await run(`${O}item replace entity @e[tag=t213z,limit=1] weapon.mainhand with minecraft:milk_bucket`);
  const had = await passes(`${O}execute if items entity @e[tag=t213z,limit=1] weapon.mainhand minecraft:milk_bucket`);
  const emptied = await wait(3000, async () => !(await passes(`${O}execute if items entity @e[tag=t213z,limit=1] weapon.mainhand *`)), 250);
  ok('a trader NPC holding a milk bucket (Zorp\'s bug) has its hands emptied within seconds', had && emptied);

  // ---- clean up
  await run(`${O}kill @e[tag=t213z]`);
  for (const [, X, Z] of SHIPS) {
    await run(`${O}execute positioned ${X} ${Y + 45} ${Z} run kill @e[type=!minecraft:player,distance=..40]`);
    for (let y = Y + 38; y < Y + 70; y += 8) await run(`${O}fill ${X - 26} ${y} ${Z - 26} ${X + 26} ${y + 7} ${Z + 26} minecraft:air`);
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 45},z=${Z},distance=..60]`);
    await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  }
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
