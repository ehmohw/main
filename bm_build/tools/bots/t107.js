// v2.68: the vault's loose ends - the tile floor's sides, crew changes rescale the guards, leave from the Ledger, a dropped
// connection keeps the heist, knock-outs give back what you dropped, safe plans, a full city, a full Locker Hall, a leader drop-out
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16800, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); let A = await bot('TestRat'); await sleep(2000); const B = await bot('TestMouse'); await sleep(2000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const fsc = async (o, who) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (who, pred) => { const o = await run(`clear ${who} ${pred} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const setToks = async (who, n) => { await run(`clear ${who} *[minecraft:custom_data~{bm:"token"}]`); for (let i = 0; i < n; i++) await run(`loot give ${who} loot bm:items/token`); };
  const has = async (who, t) => new RegExp(`"${t.replace('.', '\\.')}"`).test(await run(`data get entity ${who} Tags`));
  const dim = async who => (await run(`data get entity ${who} Dimension`)).replace(/.*data: /, '');
  const act = async (who, code) => { await run(`scoreboard players set ${who} bm.act ${code}`); await sleep(500); };
  const until = async (f, ms = 6000) => { for (let t = 0; t < ms; t += 250) { if (await f()) return true; await sleep(250); } return !!(await f()); };
  const said = (c, re) => c.chats.some(x => re.test(x));
  const ground = (c, on) => c.write('flying', { flags: { onGround: on, hasHorizontalCollision: false } });
  const gi = async (who = 'TestRat') => sc('bm.gvi', who);
  const win = async who => { const g = await gi(who);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${g}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${g}},limit=1] at @s run function bm:p70/payout`); };
  const home = async () => { for (const p of ['TestRat', 'TestMouse']) { if (await has(p, 'bm.gvp')) await run(`execute as ${p} at @s run function bm:p70/leave`); }
    await sleep(2500); for (const [p, dx] of [['TestRat', 0], ['TestMouse', 2]]) await run(`execute in minecraft:overworld run tp ${p} ${X + 0.5 + dx} ${Y + 1} ${Z + 0.5}`);
    await sleep(800); ground(A, true); ground(B, true); };
  const plan = async (tier = 1, lives = 7613) => {
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const plany = /has 1 /.test(await run('scoreboard players get #plany bm.rng')); await run('function bm:admin/heist_plans_safe');
  await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
  for (const p of ['TestRat', 'TestMouse']) {
    await run(`gamemode survival ${p}`); await run(`clear ${p}`); await run(`effect clear ${p}`);
    await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); await run(`execute as ${p} run function bm:p80/init_me`);
    for (const o of ['bm.crew', 'bm.crewoff', 'bm.fcon', 'bm.gvhc', 'bm.lkht']) await run(`scoreboard players set ${p} ${o} 0`);
    for (const t of ['bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvin', 'bm.gvwait', 'bm.gvp', 'bm.gvwaitd', 'bm.gvpre', 'bm.exon', 'bm.exask', 'bm.gvq', 'bm.lkch']) await run(`tag ${p} remove ${t}`);
  }
  await run(`execute in minecraft:overworld run forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(1500);
  await run(`fill ${X - 3} ${Y} ${Z - 3} ${X + 5} ${Y} ${Z + 3} minecraft:stone`); await run(`fill ${X - 3} ${Y + 1} ${Z - 3} ${X + 5} ${Y + 3} ${Z + 3} minecraft:air`);
  await home();
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestMouse bm.pty = TestRat bm.pid');
  await setToks('TestRat', 40); await setToks('TestMouse', 20);
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');

  // ---- 1. the tile floor: the pit runs wall to wall
  await run(`place template bm:gv_tiles_t1 ${X - 12} ${Y + 20} ${Z - 12}`); await sleep(500);
  const air = async (x, y, z) => /passed/.test(await run(`execute if block ${X - 12 + x} ${Y + 20 + y} ${Z - 12 + z} minecraft:air`));
  ok('Tile floor: the side strips are pit now (no walking round the tiles)', (await air(10, 3, 2)) && (await air(10, 3, 22)) && (await air(4, 3, 1)) && (await air(19, 3, 23)) &&
     /passed/.test(await run(`execute if block ${X - 12 + 10} ${Y + 20} ${Z - 12 + 2} minecraft:hay_block`)));
  ok('...the start and finish ledges are still there', !(await air(2, 3, 12)) && !(await air(22, 3, 12)) && !(await air(1, 3, 2)));
  await run(`fill ${X - 12} ${Y + 20} ${Z - 12} ${X + 12} ${Y + 36} ${Z + 12} minecraft:air`);
  await run(`kill @e[type=!player,x=${X - 13},y=${Y + 19},z=${Z - 13},dx=27,dy=19,dz=27]`);   // the template's room markers and props

  // ---- 2. safe plans
  await run(`tp TestRat ${X + 0.5} ${Y + 30} ${Z + 0.5}`); await sleep(500); ground(A, false); await sleep(200); A.chats.length = 0;
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier'); await sleep(300);
  ok('Heist Plans in mid-air: no ("find your feet")', said(A, /Find your feet/) && !(await has('TestRat', 'bm.gvp')), A.chats.slice(-1).join(''));
  await home(); await run('effect clear TestRat'); await run('damage TestRat 1 minecraft:generic'); await sleep(400); A.chats.length = 0;
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier'); await sleep(300);
  ok('...right after getting hurt: no ("wait N more seconds")', said(A, /hurt just now/) && !(await has('TestRat', 'bm.gvp')), A.chats.slice(-1).join(''));
  await sleep(1200); await run('scoreboard players reset TestRat bm.lkdt'); await run('scoreboard players set TestRat bm.lkht 0'); await run('effect give TestRat minecraft:instant_health 1 1 true'); await home();
  // a crewmate in mid-air isn't pulled in (or charged)
  await run(`tp TestMouse ${X + 2.5} ${Y + 6} ${Z + 0.5}`); await sleep(500); ground(B, false); await sleep(200); B.chats.length = 0;
  const mt0 = await cnt('TestMouse', '*[minecraft:custom_data~{bm:"token"}]');
  A.chats.length = 0; A.bars.length = 0; await plan(1);
  ok('From safe ground: in (the leader)', await has('TestRat', 'bm.gvp'), A.chats.slice(-4).join(' / ') + ' | ' + A.bars.slice(-2).join(' / ') + ' | ' + (await run('data get entity TestRat OnGround')) + ' ' + (await run('scoreboard players get TestRat bm.lkht')));
  ok('...the crewmate in mid-air isn\'t pulled in, or charged - and is told why', !(await has('TestMouse', 'bm.gvp')) && said(B, /weren't on safe ground/) &&
     (await cnt('TestMouse', '*[minecraft:custom_data~{bm:"token"}]')) === mt0, B.chats.slice(-1).join(''));
  await run(`tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await sleep(500); ground(B, true); await sleep(200);
  await run('loot give TestMouse loot bm:items/fixers_ledger'); await run('execute as TestMouse at @s run function bm:p70/plans'); await sleep(2500);
  ok('...once on safe ground, their own plans take them in', (await has('TestMouse', 'bm.gvp')) && (await gi('TestMouse')) === (await gi()));

  // ---- 3. the crew shrinks: the guards ease off
  const g0 = await gi();
  const guard = '@e[tag=bm.t107g,limit=1]';
  for (const [k, v] of [['#gi', g0], ['#gt', 1], ['#gn', 0], ['#gm', 0]]) await run(`scoreboard players set ${k} bm.rng ${v}`);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${g0}},limit=1] at @s positioned ~2 ~ ~2 run function bm:p70/guard`); await sleep(300);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${g0}},limit=1] at @s positioned ~2 ~ ~2 run tag @e[tag=bm.gvg,distance=..3,limit=1,sort=nearest] add bm.t107g`);
  const mh = async () => +((await run(`execute in bm:gutter run attribute ${guard} minecraft:max_health base get`)).match(/([\d.]+)/g) || [0]).slice(-1)[0];
  const cw = async () => { const m = (await run(`execute in bm:gutter run scoreboard players get ${guard} bm.gvcw`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const h2 = await mh(); const c2 = await cw();
  ok('A guard scaled for a crew of two', c2 === 2 && h2 > 0, `cw ${c2} hp ${h2}`);
  A.chats.length = 0;
  await act('TestMouse', 7729); await sleep(1500);
  ok('Leave from the Ledger\'s card (anywhere in the vault): home', /overworld/.test(await dim('TestMouse')) && !(await has('TestMouse', 'bm.gvp')));
  const h1 = await mh(); const c1 = await cw();
  ok('...and the guards still standing lose the extra health (crew of one now)', c1 === 1 && Math.abs(h1 - h2 * 100 / 135) < 1.5, `${h2} -> ${h1} (cw ${c1})`);
  ok('...the crew is told', said(A, /1 in the crew now/) && said(A, /ease off/), A.chats.slice(-2).join(' / '));
  await run('execute as TestMouse at @s run function bm:p70/plans'); await sleep(2500);
  ok('Back in: they toughen up again', (await cw()) === 2 && Math.abs((await mh()) - h2) < 1.5, `${await mh()}`);
  await run(`execute in bm:gutter run kill ${guard}`);

  // ---- 4. knocked out: what you dropped comes back
  await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]'); for (let i = 0; i < 5; i++) await run('loot give TestRat loot bm:items/token');
  await run('effect clear TestRat'); await run('kill TestRat'); await sleep(4500);
  ok('Knocked out in the vault: back in the den with the Tokens you dropped', (await has('TestRat', 'bm.gvp')) && (await cnt('TestRat', '*[minecraft:custom_data~{bm:"token"}]')) === 5 &&
     A.bars.some(b => /back in your pockets/.test(b)), `${await cnt('TestRat', '*[minecraft:custom_data~{bm:"token"}]')} ${A.chats.slice(-3).join(' / ')} ${A.bars.slice(-2).join(' / ')} ${await dim('TestRat')}`);
  await setToks('TestRat', 40);

  // ---- 5. the leader drops out at the end: the choice passes on
  await win('TestRat');
  ok('Won: the leader is asked', await until(async () => has('TestRat', 'bm.gvask'), 8000));
  await act('TestMouse', 7727);
  A.end(); await sleep(2500);
  ok('The leader drops their connection: the choice passes to the crew', await until(async () => has('TestMouse', 'bm.gvask'), 4000) && said(B, /dropped out/));
  A = await bot('TestRat'); await sleep(3000);
  ok('...the leader, back, finds it moved on', !(await has('TestRat', 'bm.gvask')) && said(A, /choice passed to your crew/));
  await act('TestMouse', 7720); await sleep(1500);
  ok('The crew\'s new decider sends everyone home', /overworld/.test(await dim('TestMouse')) && /overworld/.test(await dim('TestRat')));
  await home();

  // ---- 6. a dropped connection keeps the heist for a while; walking out frees it fast
  await run('scoreboard players reset TestMouse bm.pty'); await home(); A.chats.length = 0; await plan(1);
  const g6 = await gi(); const s6 = g6 - 1; const ch6 = A.chats.slice(-4).join(' / ');
  A.end(); await sleep(26000);
  ok('Everyone dropped (26 s): the heist is still there', (await fsc('bm.gvon', `#s${s6}`)) === 1, `g6 ${g6} ${await fsc('bm.gvon', `#s${s6}`)} ${ch6}`);
  A = await bot('TestRat'); await sleep(3500);
  ok('...back: still on the heist, in the vault', (await has('TestRat', 'bm.gvp')) && /gutter/.test(await dim('TestRat')) && (await gi()) === g6);
  await run("execute as TestRat at @s run function bm:p70/leave"); await sleep(26000);
  ok('Walked out instead: the vault frees within ~20 s', (await fsc('bm.gvon', `#s${s6}`)) !== 1, `on ${await fsc('bm.gvon', `#s${s6}`)} e ${await fsc('bm.gve', `#e${s6}`)} lf ${await fsc('bm.gve', `#lf${s6}`)} crew ${await run(`execute store result score #t bm.rng if entity @a[tag=bm.gvp,scores={bm.gvi=${g6}}]`)} mouse ${await run('data get entity TestMouse Tags')}`);
  await home();

  // ---- 7. a full city: told when a crew frees up
  await home(); for (let s = 0; s < 8; s++) await run(`scoreboard players set #s${s} bm.gvon 1`);
  A.chats.length = 0; A.bars.length = 0;
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(400);
  ok('Every vault crew busy: turned away (and noted)', (await has('TestRat', 'bm.gvq')) && !(await has('TestRat', 'bm.gvp')) && A.bars.some(b => /tell you when one frees/.test(b)));
  await run('function bm:p70/s3/clean'); await sleep(300);
  ok('...a crew frees up: told at once', said(A, /A vault crew is free now/) && !(await has('TestRat', 'bm.gvq')));
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);

  // ---- 8. a full Locker Hall (the reset rebuilds the hall on the next second's tick: wait for it, or it wipes the setup below)
  await run('function bm:admin/lockers_reset');
  await until(async () => /passed/.test(await run('execute if data storage bm:lk built')), 6000); await sleep(1200);
  for (let n = 1; n <= 18; n++) for (const c of ['-254 64 -255']) {}
  const bay = n => `@e[type=minecraft:interaction,tag=bm.lkb${n},limit=1]`;
  const ridR = await sc('bm.pid'); const ridM = await sc('bm.pid', 'TestMouse');
  // fake keepers: 900001.. hold three each (bays 4-18); TestMouse holds bays 1-3 (bay 1 with a diamond; bays 2-3 crammed full)
  for (let n = 4; n <= 18; n++) await run(`execute in bm:gutter run scoreboard players set ${bay(n)} bm.lko ${900000 + Math.ceil((n - 3) / 3)}`);
  for (let n = 1; n <= 3; n++) await run(`execute in bm:gutter run scoreboard players set ${bay(n)} bm.lko ${ridM}`);
  for (let n = 1; n <= 18; n++) await run(`execute in bm:gutter run scoreboard players set ${bay(n)} bm.lkday 999999`);
  await run('execute in bm:gutter run data modify block -254 64 -255 Items set value [{Slot:0b,id:"minecraft:diamond",count:3}]');
  const fill27 = '[' + Array.from({ length: 27 }, (_, i) => `{Slot:${i}b,id:"minecraft:cobblestone",count:64}`).join(',') + ']';
  for (const c of ['-252 64 -255', '-252 65 -255', '-251 64 -255', '-251 65 -255', '-250 64 -255', '-250 65 -255', '-249 64 -255', '-249 65 -255']) await run(`execute in bm:gutter run data modify block ${c} Items set value ${fill27}`);
  // TestRat (no bay) into the hall, clicks TestMouse's bay 1
  await run('execute in bm:gutter run tp TestRat -253 64 -253'); await sleep(1500); A.chats.length = 0;
  await run(`execute in bm:gutter as ${bay(1)} at @s run data modify entity @s interaction set value {player:[I;0,0,0,0],timestamp:1L}`);
  await run(`execute in bm:gutter as ${bay(1)} run scoreboard players operation #b bm.rng = @s bm.lkn`); await run(`execute in bm:gutter as ${bay(1)} run scoreboard players operation #o bm.rng = @s bm.lko`);
  await run(`execute in bm:gutter as ${bay(1)} run tag @s add bm.lkme`); await run('execute as TestRat at @s run function bm:p84/lk/claim'); await run(`execute in bm:gutter run tag @e[tag=bm.lkme] remove bm.lkme`);
  await run(`execute in bm:gutter as ${bay(1)} run data remove entity @s interaction`); await sleep(500);
  const own1 = await fsc('bm.lko', bay(1).replace('@e', '@e'));
  const own1b = +((await run(`execute in bm:gutter run scoreboard players get ${bay(1)} bm.lko`)).match(/has (-?\d+)/) || [0, -1])[1];
  ok('Hall full, no bay of your own: the Fixer frees a spare - bay 1 (someone\'s third) is yours', own1b === ridR && said(A, /cleared out a spare/), `owner ${own1b} (me ${ridR})`);
  ok('...its old contents are out of it', !/diamond/.test(await run('execute in bm:gutter run data get block -254 64 -255 Items')));
  const lost = await run(`data get storage bm:lk lost.p${ridM}`);
  ok('...their keeper\'s other bays were full, so the diamonds wait as Lost & Found', /diamond/.test(lost), lost.slice(0, 160));
  await run('clear TestMouse minecraft:barrel'); await run('execute in bm:gutter run tp TestMouse -247 64 -246'); await sleep(2500);
  const lf1 = await run(`data get storage bm:lk lost.p${ridM}`); const crates = await cnt('TestMouse', 'minecraft:barrel[minecraft:custom_data~{bm_haul:1b}]');
  const near = await run('execute in bm:gutter store result score #t bm.rng if entity @e[type=minecraft:item,x=-256,y=60,z=-256,dx=16,dy=10,dz=16]');
  ok('The keeper steps into the Locker Hall: handed a Lost & Found crate with the diamonds', said(B, /Lost & Found/) && !/diamond/.test(lf1) && (crates === 1 || /Count: 1/.test(near)),
     `${B.chats.slice(-2).join(' / ')} | ${lf1.slice(0, 80)} | crates ${crates} | items ${near} | ${await dim('TestMouse')} ${await run('data get entity TestMouse Pos')}`);
  // one each while the hall's nearly full: TestRat has a bay - bay 4 freed, TestRat tries for it
  await run(`execute in bm:gutter run scoreboard players set ${bay(4)} bm.lko 0`); A.chats.length = 0;
  await run(`execute in bm:gutter as ${bay(4)} run scoreboard players operation #b bm.rng = @s bm.lkn`); await run('scoreboard players set #o bm.rng 0');
  await run(`execute in bm:gutter as ${bay(4)} run tag @s add bm.lkme`); await run('execute as TestRat at @s run function bm:p84/lk/claim'); await run(`execute in bm:gutter run tag @e[tag=bm.lkme] remove bm.lkme`);
  ok('Fewer than five bays free: no second bay ("one bay each")', said(A, /one bay each/) &&
     +((await run(`execute in bm:gutter run scoreboard players get ${bay(4)} bm.lko`)).match(/has (-?\d+)/) || [0, -1])[1] === 0);
  // cleanup
  for (const c of ['-252 64 -255', '-252 65 -255', '-251 64 -255', '-251 65 -255', '-250 64 -255', '-250 65 -255', '-249 64 -255', '-249 65 -255', '-254 64 -255']) await run(`execute in bm:gutter run data modify block ${c} Items set value []`);
  await run('function bm:admin/lockers_reset'); await run(`data remove storage bm:lk lost.p${ridM}`);
  await run('execute in bm:gutter run kill @e[type=minecraft:item,x=-256,y=60,z=-256,dx=16,dy=10,dz=16]');
  for (const p of ['TestRat', 'TestMouse']) { await run(`clear ${p}`); await run(`execute in minecraft:overworld run tp ${p} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`scoreboard players reset ${p} bm.pty`); }
  await run(`execute in minecraft:overworld run forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  if (plany) await run('function bm:admin/heist_plans_anywhere');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
