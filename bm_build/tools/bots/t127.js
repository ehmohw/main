// repro: the end-of-heist Go to the Lounge, then the den/lounge menus, by real clicks (triggers, right-clicks, item use)
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const A = await bot('TestRat'); await sleep(2500);
  const epos = async sel => { const m = (await run(`data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const near = (p) => { let best = null, bd = 1e9; for (const e of Object.values(A.ents)) { const d = (e.x - p[0]) ** 2 + (e.y - p[1]) ** 2 + (e.z - p[2]) ** 2; if (d < bd) { bd = d; best = e; } } return bd < 0.5 ? best : null; };
  const click = async (tag) => {
    const sel = `@e[type=minecraft:interaction,tag=${tag},limit=1,sort=nearest,x=-307,y=68,z=-243]`;
    const p = await run(`execute in bm:gutter run data get entity ${sel} Pos`); const m = p.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (!m) return 'no entity';
    await run('tag TestRat add bm.gvok'); await run(`execute in bm:gutter run tp TestRat ${m[1]} ${+m[2]} ${+m[3] - 1.5} 0 0`); await sleep(600);
    await run(`execute in bm:gutter as ${sel} run data modify entity @s interaction set value {player:[I;0,0,0,0],timestamp:1L}`);
    await run(`execute in bm:gutter as ${sel} run data modify entity @s interaction.player set from entity TestRat UUID`); await sleep(700); return 'clicked';
  };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect clear TestRat');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await run('execute in minecraft:overworld run fill 12998 120 12998 13002 120 13002 stone'); await sleep(2500);

  // 1. a leader's Go to the Lounge, by the trigger a real button sends
  await run('tag TestRat add bm.gvask'); await run('scoreboard players set TestRat bm.gvnx 1'); await run('tag TestRat add bm.gvp'); await run('scoreboard players set TestRat bm.gvi 1');
  await run('scoreboard players set TestRat bm.menu 7720');
  A.cmd('trigger bm.act set 7730'); await sleep(2000);
  const p1 = await pos();
  ok('Leader clicks Go to the Lounge (real trigger): into the lounge', p1 && p1[0] < -290 && /gutter/.test(await run('data get entity TestRat Dimension')), `${p1} ${await run('data get entity TestRat Dimension')}`);
  console.log('tags', await run('tag TestRat list'));
  // 2. the lounge's bank, by a real right-click
  await run('scoreboard players set TestRat bm.menu -5');
  console.log('bank click:', await click('bm.of_bank'));
  ok('...then the lounge\'s bank opens on a right-click', (await sc('TestRat', 'bm.menu')) === 7802, `menu ${await sc('TestRat', 'bm.menu')}`);
  // and a button in it: the trigger goes through
  await run('scoreboard players set TestRat bm.menu -5');
  console.log('armory click:', await click('bm.of_arm'));
  ok('...and the armory', (await sc('TestRat', 'bm.menu')) !== -5, `menu ${await sc('TestRat', 'bm.menu')}`);
  // 3. home through the door, then the Ledger by holding it
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(2000);
  ok('The lounge door: home', /overworld/.test(await run('data get entity TestRat Dimension')));
  await run('clear TestRat'); await run('item replace entity TestRat hotbar.0 with minecraft:stone'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
  A.slot(0); await sleep(200); await run('scoreboard players set TestRat bm.menu -5');
  A.use(); await sleep(400); A.release(); await sleep(400);
  ok('Holding the Ledger opens the Office', (await sc('TestRat', 'bm.menu')) === 7800, `menu ${await sc('TestRat', 'bm.menu')}`);
  // 4. the Ledger plans heists now: Plan a Heist in the Office
  A.cmd('trigger bm.act set 7809'); await sleep(600);
  ok('The Ledger\'s Office: Plan a Heist opens the heist menu', (await sc('TestRat', 'bm.menu')) === 1100, `menu ${await sc('TestRat', 'bm.menu')}`);
  // 5. old Heist Plans fold into the Ledger
  await run('clear TestRat'); await run('give TestRat minecraft:totem_of_undying[minecraft:custom_data={bm:"heist_plans",bmv:33}]'); await sleep(1600);
  ok('Old Heist Plans in a pack become a Ledger', !/Found [1-9]/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"heist_plans"}] 0')) && /Found 1/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"fixers_ledger"}] 0')));
  // 6. planning from the lounge
  await run('execute as TestRat at @s run function bm:p121/enter'); await sleep(1200);
  await run('scoreboard players set TestRat bm.menu 7800'); A.chats.length = 0;
  A.cmd('trigger bm.act set 7809'); await sleep(600);
  ok('In the lounge: Plan a Heist opens too (no "already in the vault")', (await sc('TestRat', 'bm.menu')) === 1100 && !A.chats.some(c => /already in the vault/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  A.chats.length = 0; A.bars.length = 0;
  A.cmd('trigger bm.act set 7601'); await sleep(800);
  ok('...and a tier can be picked there (on to the tries)', !A.chats.concat(A.bars).some(c => /don't work|planned from here|already in the vault/.test(c)) && (await sc('TestRat', 'bm.gvpt')) === 1,
     `gvpt ${await sc('TestRat', 'bm.gvpt')} ${A.chats.concat(A.bars).slice(-3).join(' | ').slice(0, 200)}`);
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(1500);
  // 7. the supply barrels: stocked, and topped up when a part runs out everywhere
  await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await run('clear TestRat');
  await run('execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=t127m]');
  await run('execute in minecraft:overworld run summon minecraft:marker 13012 121 13000 {Tags:["t127m"]}');
  for (const [x, z] of [[6, 20], [11, 20], [16, 20]]) await run(`execute in minecraft:overworld positioned 13012 121 13000 run setblock ~${x - 12} ~ ~${z - 12} minecraft:barrel`);
  await run('execute in minecraft:overworld as @e[type=minecraft:marker,tag=t127m] at @s run function bm:p126/stk/s1'); await sleep(200);
  const b0 = await run('execute in minecraft:overworld run data get block 13006 121 13008 Items');
  ok('A Tinker\'s Bench barrel holds two sets of the parts', /iron_ingot/.test(b0) && /count: 8/.test(b0), b0.slice(0, 160));
  await run('scoreboard players set @e[type=minecraft:marker,tag=t127m] bm.gvs 1');
  for (const [x, z] of [[6, 20], [11, 20], [16, 20]]) await run(`execute in minecraft:overworld positioned 13012 121 13000 run item replace block ~${x - 12} ~ ~${z - 12} container.0 with minecraft:air`);
  await sleep(1600);
  const b1 = await run('execute in minecraft:overworld run data get block 13006 121 13008 Items');
  ok('Iron run out everywhere: the Fixer tops the barrels up', /iron_ingot/.test(b1), b1.slice(0, 120));
  await run('execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=t127m]');
  console.log(A.chats.slice(-6).join(' | ').slice(0, 600));
  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
