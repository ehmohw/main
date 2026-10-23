// 2.93d: PEARLMAN'S SEASONS, as a regular (non-op) player - his Business Card used as an item: out on the plains he wears his
// own colours; walked into a dappled forest he turns to his Fall look (the one he was drawn in) and the look is unlocked; his
// card's menu (sneak + use) -> Seasons (the buttons the client was sent): Off keeps his own colours in the forest, a locked
// season says where to find it, the snow unlocks Christmas, Christmas picked stays on back on the plains, Dynamic again
// follows the land - and the summer heat; his wardrobe colour on his own colours, never on a season's outfit; the NPC lands
// in the cherry grove in his Easter look. (rcon sets the stage: a floor, the biomes under it, the card.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const tags = async () => await run('tag TestRat list');
  const X = 17400, Y = 100, Z = 16000;
  const model = async (tag = 'bm.pmd') => ((await run(`${O}data get entity @e[type=minecraft:item_display,tag=${tag},limit=1] item.components."minecraft:item_model"`)).match(/"([^"]+)"/) || [])[1];
  const biome = async (b) => { await run(`${O}fillbiome ${X - 14} ${Y - 4} ${Z - 14} ${X + 14} ${Y + 12} ${Z + 14} minecraft:${b}`); };
  const isModel = async (m, ms = 4000) => wait(ms, async () => (await model()) === m);
  const menu = async () => { A.slot(1); await sleep(250); A.input({ shift: true }); await sleep(250); const o = await A.useWait(); A.input({}); await sleep(250); return o; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:grass_block`); await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] run function bm:p128/pm/go`); await run('kill @e[type=minecraft:item_display,tag=bm.pmd]');
  await run('scoreboard players reset TestRat bm.pmsea'); await run('scoreboard players set TestRat bm.cospm 0');
  for (const k of ['fall', 'xmas', 'easter', 'summer']) await run(`tag TestRat remove bm.pmu_${k}`);
  await biome('plains');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500);

  // ---------------------------------------------------------------- out on the plains: his own colours
  await run('loot replace entity TestRat hotbar.1 loot bm:items/pearl_card'); A.slot(1); await sleep(300);
  A.use(); await sleep(400); A.release(); await sleep(2500);
  ok('His Business Card used on the plains: Pearlman out, in his own colours', (await cnt('@e[type=minecraft:cat,tag=bm.pmpet]')) === 1 && (await model()) === 'bm:pearlman',
     `model ${await model()}`);

  // ---------------------------------------------------------------- into a dappled forest: Fall - and it's his to keep
  A.chats.length = 0; await biome('dappled_forest');
  ok('The land turns to dappled forest: his Fall look (Dynamic, the default)', await isModel('bm:pearlman_fall'), `model ${await model()}`);
  ok('...the Fall look unlocked, and he says so', /bm\.pmu_fall/.test(await tags()) && A.chats.some(c => /Fall look/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 160));

  // ---------------------------------------------------------------- his card's menu -> Seasons
  ok('Sneak + use the card: his menu', await menu() && A.buttons().some(b => /Seasons/.test(b.label)), A.buttons().map(b => b.label).join(', '));
  let b = await A.press(/Seasons/);
  const labels = A.buttons().map(b => b.label).join(', ');
  ok('Seasons: Dynamic, Off, Fall unlocked - Christmas, Easter, Summer locked', !!b && b.next && /Dynamic/.test(labels) && /Off/.test(labels) &&
     A.buttons().some(x => x.label === 'Fall') && /Christmas \(locked\)/.test(labels) && /Easter \(locked\)/.test(labels) && /Summer \(locked\)/.test(labels), labels);
  await A.press(/^Off/); await sleep(1500);
  ok('Off: his own colours, even in the forest', (await score('bm.pmsea')) === 1 && await isModel('bm:pearlman'), `mode ${await score('bm.pmsea')} model ${await model()}`);
  await menu(); await A.press(/Seasons/); A.chats.length = 0;
  b = await A.press(/Christmas \(locked\)/, 2500); await sleep(500);
  ok('A locked season: he says where to find it (and the choice stays)', A.chats.some(c => /somewhere snowy/.test(c)) && (await score('bm.pmsea')) === 1,
     A.chats.slice(-2).join(' | ').slice(0, 160));

  // ---------------------------------------------------------------- the snow: Christmas unlocked (still Off), then picked
  await biome('snowy_plains'); await sleep(2500);
  ok('In the snow: Christmas unlocked - and with Off chosen he keeps his own colours', /bm\.pmu_xmas/.test(await tags()) && (await model()) === 'bm:pearlman', `model ${await model()}`);
  await menu(); await A.press(/Seasons/);
  ok('...Christmas no longer locked on the card', A.buttons().some(x => x.label === 'Christmas'), A.buttons().map(b => b.label).join(', '));
  await A.press(/^Christmas$/); await sleep(1000);
  ok('Christmas picked: his Christmas look', (await score('bm.pmsea')) === 3 && await isModel('bm:pearlman_xmas'), `mode ${await score('bm.pmsea')} model ${await model()}`);
  await biome('plains'); await sleep(2500);
  ok('...and it stays on, back on the plains', (await model()) === 'bm:pearlman_xmas', `model ${await model()}`);
  // (recalled: still Christmas)
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] run function bm:p128/pm/go`); await sleep(500);
  A.slot(1); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(2000);
  ok('Sent home and called again: still in Christmas', (await cnt('@e[type=minecraft:cat,tag=bm.pmpet]')) === 1 && (await model()) === 'bm:pearlman_xmas', `model ${await model()}`);

  // ---------------------------------------------------------------- Dynamic again: the land decides
  await menu(); await A.press(/Seasons/); await A.press(/Dynamic/); await sleep(1500);
  ok('Dynamic: on the plains, his own colours again', (await score('bm.pmsea')) === 0 && await isModel('bm:pearlman'), `model ${await model()}`);
  A.chats.length = 0; await biome('desert');
  ok('...the desert heat: his Summer look, unlocked as he goes', await isModel('bm:pearlman_summer') && /bm\.pmu_summer/.test(await tags()), `model ${await model()}`);

  // ---------------------------------------------------------------- his wardrobe colour: on his own colours, not a season's outfit
  await run('scoreboard players set TestRat bm.cospm 1'); await biome('plains');
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] run function bm:p128/pm/go`); await sleep(500);
  A.slot(1); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(2000);
  ok('His wardrobe colour on his own colours (bm:pearlman_c1)', await isModel('bm:pearlman_c1'), `model ${await model()}`);
  await biome('dappled_forest');
  ok('...and a season\'s outfit replaces it (Fall, no colour suffix)', await isModel('bm:pearlman_fall'), `model ${await model()}`);
  await biome('plains');
  ok('...back on the plains, the colour comes back', await isModel('bm:pearlman_c1'), `model ${await model()}`);
  await run('scoreboard players set TestRat bm.cospm 0');

  // ---------------------------------------------------------------- the NPC: dressed for where he lands
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] run function bm:p128/pm/go`);
  await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
  await biome('cherry_grove');
  await run(`${O}execute positioned ${X + 4.5} ${Y} ${Z + 4.5} run function bm:p60/pm/spawn`); await sleep(500);
  ok('Pearlman the salesman lands in a cherry grove: his Easter look', (await model('bm.pearld')) === 'bm:pearlman_easter', `model ${await model('bm.pearld')}`);
  await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
  await biome('plains');
  await run(`${O}execute positioned ${X + 4.5} ${Y} ${Z + 4.5} run function bm:p60/pm/spawn`); await sleep(500);
  ok('...and on the plains, his own colours', (await model('bm.pearld')) === 'bm:pearlman', `model ${await model('bm.pearld')}`);
  await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
