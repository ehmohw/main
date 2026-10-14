const { bot, rcon, sleep } = require('./lib');
const X = 14000, Y = 100, Z = 14000; const res = [];
const rel = (x, y, z) => `~${x - 12} ~${y - 4} ~${z - 12}`;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500); const B = await bot('TestRat2'); await sleep(3000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => { const m = (await run(`execute in bm:gutter run scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const inV = async (p) => /passed/.test(await run(`execute as ${p} at @s if dimension bm:gutter`));
  const atRoom = (k, cmd) => run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] at @s run ${cmd}`);
  for (const p of ['TestRat', 'TestRat2']) { await run(`tp ${p} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`clear ${p}`); await run(`gamemode survival ${p}`); await run(`effect give ${p} resistance 600 4 true`);
    await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); await run(`tag ${p} remove bm.gvzap`); await run(`scoreboard players set ${p} bm.gvu 1`); }
  await sleep(2500);
  await run(`fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} stone`);
  // a party of two (the leader's id is the party's)
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestRat2 bm.pty = TestRat bm.pid');
  // a Blood Moon tonight
  await run('scoreboard players set #active bm.bm 1');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('loot give TestRat2 loot bm:items/fixers_ledger');
  await run('execute as TestRat2 at @s run function bm:p70/plans'); await sleep(300);
  ok('A party member (not the leader) can\'t plan the heist', !(await inV('TestRat2')) && B.bars.slice(-4).some(b => /leader/.test(b)), B.bars.slice(-2).join(' / '));
  for (let i = 0; i < 3; i++) { await run('loot give TestRat loot bm:items/token'); await run('loot give TestRat2 loot bm:items/token'); } await run('execute as TestRat at @s run function bm:p70/plans'); await sleep(200); A.cmd('trigger bm.act set 7601'); await sleep(900); A.cmd('trigger bm.act set 7613');
  await sleep(3000);
  // (the Blood Moon can't be faked from here - the night logic resets its flag: make this heist a Blood Moon heist directly)
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst] run scoreboard players set @s bm.gvnt 1');
  await run('scoreboard players set #gn bm.rng 1'); await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst] run scoreboard players operation #gt bm.rng = @s bm.gvt');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvinst] run scoreboard players operation #gm bm.rng = @s bm.gvmod');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby] at @s run function bm:p70/sheet');
  ok('The leader plans it: both party members are led into the vault', await inV('TestRat') && await inV('TestRat2'));
  ok('...and it\'s a BLOOD MOON HEIST', /BLOOD MOON HEIST/.test(await run('execute in bm:gutter run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1] text')));
  await run('scoreboard players set #active bm.bm 0');
  // the member slips out, then rejoins with their own plans
  await atRoom('lobby', `tp TestRat2 ${rel(0, 4, 12)}`); await sleep(1200);
  ok('The member steps through the den\'s Fixer\'s Door (before the heist begins): home at once', !(await inV('TestRat2')));
  await run(`tp TestRat2 ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(500);
  await run('execute as TestRat2 at @s run function bm:p70/plans'); await sleep(1500);
  ok('...and their own plans take them back into the party\'s heist', await inV('TestRat2'));
  // a knock-out
  await atRoom('lobby', 'setblock ' + rel(23, 5, 15) + ' minecraft:pale_oak_button[face=wall,facing=west,powered=true]'); await sleep(500);
  const a0 = await sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gva');
  await run('effect clear TestRat2 resistance'); await run('kill TestRat2'); await sleep(2500);
  ok('Knocked out in the vault: dragged back to the den, and the alarm rings', await inV('TestRat2') && (await sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gva')) > a0,
     `${a0} -> ${await sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gva')}`);
  // the Blood Moon guards and guardian
  await atRoom('vault', 'tp TestRat ~ ~ ~-3'); await atRoom('vault', 'tp TestRat2 ~ ~ ~-4'); await sleep(1500);
  ok('...and in a Blood Moon heist the guardian is the Crimson Treasurer', /Crimson Treasurer/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] CustomName')));
  await run('execute in bm:gutter as @e[tag=bm.gvboss] at @s run function bm:p70/boss/call'); await sleep(500);
  ok('...its guards are Blood Moon guards', /Blood Moon/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvg,limit=1] CustomName')));
  // both leave; cleanup
  await atRoom('lobby', `tp TestRat ${rel(0, 4, 12)}`); await atRoom('lobby', `tp TestRat2 ${rel(0, 4, 12)}`); await sleep(800);
  ok('Mid-heist, the door asks first', (await inV('TestRat')) && (await inV('TestRat2')));
  A.cmd('trigger bm.act set 7724'); B.cmd('trigger bm.act set 7724'); await sleep(1500);
  ok('Both out (Leave now)', !(await inV('TestRat')) && !(await inV('TestRat2')));
  await sleep(22000);
  ok('...the vault is cleared', (await cnt('@e[type=marker,tag=bm.gvr]')) === 0 && (await cnt('@e[tag=bm.gvboss]')) === 0);
  for (const p of ['TestRat', 'TestRat2']) await run(`scoreboard players reset ${p} bm.pty`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
