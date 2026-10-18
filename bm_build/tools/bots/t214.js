// 2.82l: NO FREE BLOCKS FROM POP-UP CONTAINERS - as a regular (non-op) player TestRat, every step a real packet (rcon sets the
// stage: a field, the item in hand, a netherite axe/pickaxe with Efficiency V and Haste to break with, goods put inside).
//   The Prime Cooler's barrel, the Vacuum Satchel's barrel and the Ender Pouch's ender chest, each set down with a real
//   right-click and then broken by TestRat (real dig packets): no barrel / ender chest / obsidian comes out of it - not on the
//   ground, not in TestRat's pack; the goods that were inside are on the ground; the cooler comes back to TestRat (empty).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const X = 32000, Y = 100, Z = 32000, BX = [X, Y, Z + 2];
  const have = async (item) => { const o = await run(`clear TestRat ${item} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const ground = async (item) => +(((await run(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8] if items entity @s contents ${item}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const block = (b) => passes(`${O}execute if block ${BX.join(' ')} ${b}`);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:haste 900 4 true');

  const CASES = [
    ['the Prime Cooler', 'prime_cooler', false, 'minecraft:barrel', ['minecraft:barrel'], 'minecraft:netherite_axe'],
    ['the Vacuum Satchel', 'vacuum_satchel', true, 'minecraft:barrel', ['minecraft:barrel'], 'minecraft:netherite_axe'],
    ['the Ender Pouch', 'ender_pouch', false, 'minecraft:ender_chest', ['minecraft:ender_chest', 'minecraft:obsidian'], 'minecraft:netherite_pickaxe'],
  ];
  for (const [nm, iid, sneak, blk, drops, tool] of CASES) {
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat');
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800); A.stand();
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`);
    await run(`item replace entity TestRat hotbar.1 with ${tool}[minecraft:enchantments={"minecraft:efficiency":5}]`);
    A.slot(0); await sleep(300);
    if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.use(); await sleep(300); A.release(); await sleep(150);
    if (sneak) A.input({});
    await sleep(900);
    const up = await block(blk);
    if (blk === 'minecraft:barrel') await run(`${O}item replace block ${BX.join(' ')} container.4 with minecraft:cobblestone 7`);   // (the stage: goods inside)
    A.slot(1); await sleep(300);
    await A.mine(BX[0], BX[1], BX[2], blk === 'minecraft:barrel' ? 900 : 2600); await sleep(1500);
    const gone = !(await block(blk));
    let freeBlocks = 0; for (const d of drops) freeBlocks += (await ground(d)) + (await have(d));
    ok(`${nm}: set down with a right-click, then broken by hand (real dig packets) - no ${drops.join(' / ').replace(/minecraft:/g, '')} comes out of it`,
       up && gone && freeBlocks === 0, `up ${up}, broken ${gone}, free blocks ${freeBlocks} ${A.bars.slice(-2).join(' | ')}`);
    if (blk === 'minecraft:barrel') {
      const cob = (await ground('minecraft:cobblestone')) + (await have('minecraft:cobblestone'));
      ok(`...the goods inside are not lost (on the ground or picked up)`, cob === 7, `${cob}`);
    }
    if (iid === 'prime_cooler') ok('...and the cooler comes back to TestRat', await wait(3000, async () => (await have(`*[minecraft:custom_data~{bm:"prime_cooler"}]`)) === 1, 250));
  }

  // ---- clean up
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run(`${O}kill @e[type=minecraft:marker,x=${X},y=${Y},z=${Z},distance=..12,tag=!bm.keep]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
