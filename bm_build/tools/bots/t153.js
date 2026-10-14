// 2.78: a boss doesn't sit frozen where you left him. As a regular (non-op) player: Tullius risen in front of the bot (rcon sets
// the stage), the bot killed with nobody else near: he goes back into the sea at once. Risen again, the bot carried far away
// (respawned out of range - rcon stages that too) and his chunk left unloaded a minute: when it loads again, he's gone. And
// Apophiss in his den: the bot's death there, alone, ends the fight.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ', H = 'execute in bm:hollow_throne run ';
  const cnt = async (pre, sel) => { const m = (await run(`${pre}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const TB = '@e[type=minecraft:husk,tag=bm.tuboss]', AB = '@e[type=minecraft:husk,tag=bm.apboss]';
  const die = async () => { for (let i = 0; i < 12 && A.health > 0; i++) { await run('damage TestRat 8 minecraft:generic'); await sleep(400); } await sleep(1500); };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}spawnpoint TestRat 13000 121 13000`);
  const X = 15200, Y = 100, Z = 15200;
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} minecraft:air`);
  await run(`${O}kill ${TB}`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.tub]`);
  // 1. a death, nobody else near: he leaves
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('execute as TestRat at @s run function bm:admin/tullius');
  ok('Tullius rises in front of the bot', await wait(4000, async () => (await cnt(O, TB)) === 1));
  await sleep(3000);
  await die(); A.stand();
  ok('the bot dies with nobody else near: Tullius goes back into the sea', await wait(4000, async () => (await cnt(O, TB)) === 0), `left ${await cnt(O, TB)}`);
  // 2. carried far off, his chunk unloaded a minute: when it loads again, he's gone
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('execute as TestRat at @s run function bm:admin/tullius');
  await wait(4000, async () => (await cnt(O, TB)) === 1); await sleep(3000);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}tp TestRat 13000.5 121 13000.5`); await sleep(1000); A.stand();
  await sleep(66000);
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  ok('a minute away, his chunk loaded again: Tullius is gone (no frozen fight waiting)', await wait(6000, async () => (await cnt(O, TB)) === 0), `left ${await cnt(O, TB)}`);
  await run(`${O}kill ${TB}`); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  // 3. Apophiss: a lone death in the den ends it
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('execute as TestRat run function bm:admin/apophiss_den'); await run('scoreboard players set #apwake bm.p2 0'); await sleep(1500); A.stand();
  await run(`${H}kill ${AB}`); await run(`${H}tp TestRat 1076.5 3 1075.5 180 0`); await sleep(800); A.stand();
  await run('execute as TestRat at @s run function bm:admin/apophiss');
  ok('Apophiss comes', await wait(5000, async () => (await cnt(H, AB)) === 1));
  await sleep(3000);
  await die(); A.stand();
  ok('the bot dies alone in his den: Apophiss leaves', await wait(5000, async () => (await cnt(H, AB)) === 0), `left ${await cnt(H, AB)}`);
  await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`); await run('bossbar set bm:apob visible false'); await run('bossbar set bm:tub visible false');
  await run('tag TestRat remove bm.apin'); await run(`${O}tp TestRat 13000.5 121 13000.5`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
