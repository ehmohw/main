// 2.85c: THE RAT RACE (Goal Day) - as a regular player TestRat (rcon sets the stage: the hour, a pass into the Lounge, the ore).
//   Goldtooth (the Lounge's) sells a Starter's Pistol for 2 Gutter Medallions: bought at his counter. Fired in the Lounge: no
//     (the Overworld only), it's handed back. It comes home with you.
//   fired at night: no - too late in the day, handed back. Fired in the morning: the race is on - a gold bar, a job for everyone.
//     (Fired again until the job is one to mine - the call-off between tries is the stage's.)
//   the job scales with the players online: alone, the base; a second player joins - more; they leave - it stays (the most seen).
//   ore set back down and mined again counts for nothing; the world's own ore (here, set by rcon) counts - halfway, a word to
//     everyone; done: the race is WON, the bar goes, and the player gets Tokens and a prize. The pistol again today: no.
//   a race not done by sunset: lost, no harm done (no Tokens taken).
//   the Lucky Horseshoe hung up by day: tonight is a Lucky Night; a second one won't hang (handed back).
//   (and the prize draw, rolled 40 times by rcon: Tokens every time, and a spread of prizes.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
const JOBS = ['iron', 'gold', 'copper', 'diamond', 'quartz', 'acacia', 'sand', 'obsidian', 'blaze', 'enderman', 'wskel', 'guardian', 'fish', 'breed', 'trade'];
const BASE = { iron: [30, 15, 'iron_ore'], gold: [24, 12, 'gold_ore'], copper: [48, 24, 'copper_ore'], diamond: [8, 4, 'diamond_ore'],
               quartz: [64, 32, 'nether_quartz_ore'], obsidian: [32, 16, 'obsidian'] };
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const passes = async c => /passed/i.test(await run(c));
  const slotOf = async id => { for (let s = 0; s < 36; s++) if (new RegExp(`"${id}"`).test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; };
  const uuidEnt = async sel => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const O = 'execute in minecraft:overworld run ', GU = 'execute in bm:gutter run ';
  const X = 13480, Y = 121, Z = 13400;
  const saved = { bmoff: await sc('#bmoff', 'bm.cfg') };
  const chat = re => A.chats.some(c => re.test(c));
  // (hold 'use' for the consume time; the pistol must be in the hotbar)
  const fire = async (id, ms = 1100) => { let s = await slotOf(id); if (s > 8) { await run(`item replace entity TestRat hotbar.4 from entity TestRat inventory.${s - 9}`); await run(`item replace entity TestRat inventory.${s - 9} with minecraft:air`); s = 4; }
    A.slot(s); await sleep(300); A.use(); await sleep(ms); A.release(); await sleep(700); };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('scoreboard players set #bmoff bm.cfg 1'); await run('function bm:admin/rat_race_end');

  // ================================================================== 1. Goldtooth's pistol, in the Lounge
  await run('tag TestRat add bm.gvok'); await run(`${GU}tp TestRat -316.5 68 -233.5 180 10`); await sleep(3000); A.stand();
  const GT = '@e[type=minecraft:villager,tag=bm.gvgt,x=-316,y=68,z=-235,distance=..6,limit=1]';
  let gi = -1; for (let i = 0; i < 60; i++) { const o = await run(`${GU}data get entity ${GT} Offers.Recipes[${i}].sell`); if (!/data:/.test(o)) break; if (/rat_race_pistol/.test(o)) { gi = i; break; } }
  const price = await run(`${GU}data get entity ${GT} Offers.Recipes[${gi}].buy`);
  ok('The Lounge\'s Goldtooth sells a Starter\'s Pistol for 2 Gutter Medallions', gi >= 0 && /gutter_medallion/.test(price) && /count: 2/.test(price), `#${gi} ${price.replace(/.*data: /, '').slice(0, 90)}`);
  for (let j = 0; j < 2; j++) await run('loot give TestRat loot bm:items/gutter_medallion');
  await sleep(500);
  A.windows.length = 0; A.interact(await uuidEnt(GT)); await sleep(1000); const w = A.windows[A.windows.length - 1];
  if (w) { A.write('select_trade', { slot: gi }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(600); A.close(w.windowId); await sleep(500); }
  ok('...bought at his counter: the pistol in the pack, the Medallions spent', (await has('rat_race_pistol')) === 1 && (await has('gutter_medallion')) === 0, `window ${!!w}`);
  A.chats.length = 0; A.bars.length = 0; await fire('rat_race_pistol');
  ok('Fired in the Lounge: no - out in the Overworld; it\'s handed back', A.bars.some(b => /Overworld/.test(b)) && (await has('rat_race_pistol')) === 1 && (await sc('#rron', 'bm.bm')) !== 1,
     A.bars.slice(-1).join(''));

  // ================================================================== 2. home with it; too late in the day
  await run('tag TestRat remove bm.gvok');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 180 20`); await sleep(3000); A.stand();
  ok('Home in the Overworld: the pistol came out of the den with you', (await has('rat_race_pistol')) === 1);
  await run('time set 13000'); await sleep(1500);
  A.bars.length = 0; await fire('rat_race_pistol');
  ok('Fired at night: too late in the day - handed back, no race', A.bars.some(b => /Too late/.test(b)) && (await has('rat_race_pistol')) === 1 && (await sc('#rron', 'bm.bm')) !== 1,
     A.bars.slice(-1).join(''));

  // ================================================================== 3. the race is on (fired until the job is one to mine)
  await run('time set 1000'); await sleep(1500);
  await run('scoreboard players set #rrday bm.bm -1');
  let job = null, tries = 0, first = true;
  while (tries++ < 40) {
    if ((await has('rat_race_pistol')) === 0) await run('loot give TestRat loot bm:items/rat_race_pistol');
    A.chats.length = 0; await fire('rat_race_pistol');
    if (first) { first = false;
      ok('Fired in the morning: the Rat Race is on - the word to everyone, the gold bar', (await sc('#rron', 'bm.bm')) === 1 && chat(/The Rat Race is on/) && chat(/The job:/) &&
         /currently visible/.test(await run('bossbar get bm:ratrace visible')), `on ${await sc('#rron', 'bm.bm')} | ${await run('bossbar get bm:ratrace visible')} | ${A.chats.join(' | ').slice(0, 300)}`); }
    const k = await sc('#rrk', 'bm.bm'); job = JOBS[k - 1];
    if (BASE[job]) break;
    await run('function bm:admin/rat_race_end'); await run('scoreboard players set #rrday bm.bm -1'); job = null;      // (the stage: called off, a fresh try)
  }
  ok(`...a job to mine came up: ${job} (${tries} firings)`, !!job);
  const [base, per, block] = BASE[job];
  ok(`...alone online: the base target (${base})`, (await sc('#rrt', 'bm.bm')) === base, `${await sc('#rrt', 'bm.bm')}`);
  const B = await bot('TestRat2'); await sleep(3500);
  ok(`...a second player joins: more (${base + per})`, await wait(4000, async () => (await sc('#rrt', 'bm.bm')) === base + per), `${await sc('#rrt', 'bm.bm')}`);
  B.end(); await sleep(3000);
  ok('...they leave: it stays (the most seen online)', (await sc('#rrt', 'bm.bm')) === base + per);
  const target = base + per;

  // ---- ore set back down counts for nothing
  await run('give TestRat minecraft:netherite_pickaxe[minecraft:enchantments={"minecraft:efficiency":5}] 1');
  await run('effect give TestRat minecraft:haste 600 1 true');
  await run(`give TestRat minecraft:${block} 1`); await sleep(500);
  const bs = await (async () => { for (let s = 0; s < 9; s++) if (new RegExp(`minecraft:${block}"`).test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].id`))) return s; return -1; })();
  const ps = await (async () => { for (let s = 0; s < 9; s++) if (/netherite_pickaxe/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].id`))) return s; return -1; })();
  A.slot(bs); await sleep(300); A.useOn(X, Y - 1, Z - 1, 1); await sleep(1500);
  const placedOk = await passes(`${O}execute if block ${X} ${Y} ${Z - 1} minecraft:${block}`);
  A.slot(ps); await sleep(300); await A.mine(X, Y, Z - 1, block === 'obsidian' ? 2400 : 400); await sleep(2000);
  ok('Ore set back down and mined again: counts for nothing', placedOk && !(await passes(`${O}execute if block ${X} ${Y} ${Z - 1} minecraft:${block}`)) && (await sc('#rrc', 'bm.bm')) === 0,
     `placed ${placedOk} count ${await sc('#rrc', 'bm.bm')}`);

  // ---- the world's own ore (rcon's), mined to the target
  A.chats.length = 0;
  const tokens0 = await has('token');
  const wall = []; for (let dx = -2; dx <= 2; dx++) for (let dy = 0; dy <= 2; dy++) wall.push([X + dx, Y + dy, Z - 2]);
  let mined = 0, guard = 0;
  while ((await sc('#rron', 'bm.bm')) === 1 && guard++ < 12) {
    await run(`${O}fill ${X - 2} ${Y} ${Z - 2} ${X + 2} ${Y + 2} ${Z - 2} minecraft:${block}`); await sleep(300);
    for (const [bx, by, bz] of wall) { if ((await sc('#rron', 'bm.bm')) !== 1) break; await A.mine(bx, by, bz, block === 'obsidian' ? 2200 : 350); mined++; await sleep(80); }
    await sleep(1300);
  }
  ok(`...halfway: a word to everyone`, chat(/halfway there/));
  ok(`The world's own ore mined (${mined} blocks): the race is WON - the bar gone`, chat(/Rat Race is WON/) && (await sc('#rron', 'bm.bm')) === 0 &&
     /currently hidden/.test(await run('bossbar get bm:ratrace visible')), `count ${await sc('#rrc', 'bm.bm')} / ${target}`);
  ok('...and the player\'s prize: Tokens and a draw', (await has('token')) >= tokens0 + 3 && chat(/Your prize:/), `tokens ${tokens0} -> ${await has('token')}; ${A.chats.filter(c => /prize/.test(c)).join('')}`);
  await run('loot give TestRat loot bm:items/rat_race_pistol'); A.bars.length = 0; await fire('rat_race_pistol');
  ok('The pistol again the same day: no - one race a day (handed back)', A.bars.some(b => /One Rat Race a day/.test(b)) && (await sc('#rron', 'bm.bm')) === 0);

  // ================================================================== 4. a race lost at sunset: no harm done
  await run('scoreboard players set #rrday bm.bm -1');                                        // (the stage: another day)
  A.chats.length = 0; await fire('rat_race_pistol');
  const t1 = await has('token');
  ok('Another race fired...', (await sc('#rron', 'bm.bm')) === 1);
  await run('time set 12000');
  ok('...the sun sets first: lost - no harm done (no Tokens taken)', await wait(4000, async () => (await sc('#rron', 'bm.bm')) === 0) && chat(/The Rat Race is lost/) && (await has('token')) === t1);

  // ================================================================== 5. the Lucky Horseshoe
  await run('time set 2000'); await run('scoreboard players set #lucky bm.bm 0'); await sleep(1500);
  await run('loot give TestRat loot bm:items/lucky_horseshoe'); await run('loot give TestRat loot bm:items/lucky_horseshoe');
  A.chats.length = 0; await fire('lucky_horseshoe', 1800);
  ok('The Lucky Horseshoe hung up by day: tonight is a Lucky Night', (await sc('#lucky', 'bm.bm')) === 1 && (await sc('#lday', 'bm.bm')) === (await sc('#day', 'bm.bm')) &&
     chat(/Tonight is a Lucky Night/) && (await has('lucky_horseshoe')) === 1);
  A.bars.length = 0; await fire('lucky_horseshoe', 1800);
  ok('...a second won\'t hang (luck already on its way): handed back', (await has('lucky_horseshoe')) === 1 && A.bars.some(b => /won't hang/.test(b)));

  // ================================================================== 6. the prize draw (rcon rolls it 40 times)
  await run('clear TestRat');
  A.chats.length = 0;
  for (let i = 0; i < 40; i++) await run('execute as TestRat at @s run function bm:p183/prize');
  await sleep(800);
  const kinds = new Set(A.chats.filter(c => /Your prize:/.test(c)).map(c => c.replace(/.*and /, '')));
  ok('The prize draw x40: Tokens every time (120+), and a spread of prizes', (await has('token')) >= 120 && kinds.size >= 4, `${await has('token')} tokens; ${[...kinds].join(' | ')}`);

  // ---- put things back
  await run('scoreboard players set #lucky bm.bm 0'); await run('function bm:admin/rat_race_end');
  await run(`scoreboard players set #bmoff bm.cfg ${isNaN(saved.bmoff) ? 0 : saved.bmoff}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat'); await run('time set 6000');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
