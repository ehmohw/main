// 2.88: THE STALKER, REMADE - as a regular (non-op) player on a Dread Night (rcon sets the stage: hard mode, a King-slayer, the
// night rung in, the Stalker raised, a stone hut built round the player).
//   its body is the follower's own jointed rig at Dread size - ten parts at its feet, not two stiff displays riding it;
//   still, it draws itself up tall (stand); closing in it goes down on all fours (crawl) and runs you down flat out (sprint);
//   walled in: six seconds without getting closer and it winds up ("Walls won't stop it.", rigid, screaming), then comes
//     straight through the stone to you - and out inside the hut;
//   the night's own monsters are left alone (a husk out before nightfall stays; a fresh one rises).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)[dfb]?$/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/.test(await run(c));
  const O = 'execute in minecraft:overworld run ';
  const X = 13800, Y = 121, Z = 13400;
  const STK = '@e[type=minecraft:zombie,tag=bm.stalker,limit=1]';
  const pos = async sel => { const p = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return p ? p.slice(1).map(Number) : null; };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); A.stand(); };
  const still = () => run('scoreboard players set TestRat bm.dnst -1000');     // (staged: no Stalker steps out of the dark behind a player standing about)
  const heal = () => run('effect give TestRat minecraft:instant_health 1 4 true');
  const saved = { conq: await sc('TestRat', 'bm.conq'), hard: await sc('#hard', 'bm.cfg'), bmoff: await sc('#bmoff', 'bm.cfg') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set #hard bm.cfg 1'); await run('scoreboard players set #bmoff bm.cfg 1');
  await run('time set 6000');
  // ---- the pad: a wide floor in the sky
  await run(`${O}forceload add ${X - 64} ${Z - 64} ${X + 64} ${Z + 64}`);
  await run(`${O}fill ${X - 45} ${Y - 1} ${Z - 45} ${X + 45} ${Y - 1} ${Z + 45} minecraft:stone`);
  for (const [y0, y1] of [[Y, Y + 2], [Y + 3, Y + 6]]) await run(`${O}fill ${X - 45} ${y0} ${Z - 45} ${X + 45} ${y1} ${Z + 45} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..70]`);
  await at(X + 0.5, Y, Z + 0.5, 0, 0);
  await run('effect give TestRat minecraft:regeneration 900 4 true'); await run('effect give TestRat minecraft:saturation 900 0 true');
  // ---- the night rung in (the bell's own scores), a monster out before it falls; nightfall
  await run('scoreboard players operation #dnday bm.bm = #day bm.bm');
  await run(`${O}summon minecraft:husk ${X + 12.5} ${Y} ${Z - 12.5} {Tags:["bm.seen","t247a"],PersistenceRequired:1b,NoAI:1b}`);
  await run('time set 13100');
  ok('(staged) a Dread Night, and the player hunted', await wait(4000, async () => (await sc('#dnight', 'bm.bm')) === 1) &&
     await wait(3000, async () => passes('execute if entity @a[name=TestRat,tag=bm.dnh]')));
  await still();

  // ================================================================== 1. the night's own monsters
  await sleep(2000);
  ok('A monster out before nightfall stays out - the night no longer clears them', await passes(`${O}execute if entity @e[tag=t247a]`));
  await run(`${O}summon minecraft:husk ${X - 12.5} ${Y} ${Z - 12.5} {Tags:["t247a"],NoAI:1b}`);           // (no bm.seen: as the night would spawn it)
  await sleep(3000);
  ok('...and a fresh one rises as on any night', (await num(`${O}execute if entity @e[type=minecraft:husk,tag=t247a]`)) === 2);
  await run(`${O}kill @e[tag=t247a]`);

  // ================================================================== 2. its body: the rig
  await still(); await run('scoreboard players set TestRat bm.dnsp 1');
  ok('A Stalker rises', await wait(5000, async () => passes(`${O}execute if entity ${STK}`)));
  const sid = await sc(STK, 'bm.stkid');
  const parts = await num(`${O}execute if entity @e[type=minecraft:item_display,tag=bm.stkpart,scores={bm.stkid=${sid}}]`);
  const riders = await passes(`${O}execute as ${STK} if entity @s[nbt={Passengers:[{}]}]`);
  ok('...its body the jointed rig: ten parts of its own, none riding it', parts === 10 && !riders, `${parts} parts, riders ${riders}`);
  // ---- held still (NoAI, as the test holds it): drawn up tall, its parts at its feet
  await run(`${O}data merge entity ${STK} {NoAI:1b}`); await run(`${O}tp ${STK} ${X + 0.5} ${Y} ${Z + 20.5} 180 0`); await sleep(1500);
  const sp = await pos(STK);
  const body = await pos(`@e[type=minecraft:item_display,tag=bm.stkp_body,scores={bm.stkid=${sid}},limit=1]`);
  ok('Still: it stands (drawn up tall), its rig with it', (await sc(STK, 'bm.stka')) === 0 && body && sp && Math.hypot(body[0] - sp[0], body[2] - sp[2]) < 0.6 &&
     Math.abs(body[1] - sp[1]) < 0.6, `gait ${await sc(STK, 'bm.stka')}, body ${body && body.map(v => v.toFixed(2))} host ${sp && sp.map(v => v.toFixed(2))}`);
  // ---- let go: it comes for you - on all fours, then flat out
  await still(); await heal();
  const seen = new Set();
  await run(`${O}data merge entity ${STK} {NoAI:0b}`);
  await wait(6000, async () => { seen.add(await sc(STK, 'bm.stka')); return seen.has(2); }, 100);
  ok('Let go, it comes for you: on all fours (crawl), and flat out (sprint)', seen.has(2) || seen.has(1), `gaits seen ${[...seen].join(',')}`);
  ok('...flat out at a run', seen.has(2), `gaits seen ${[...seen].join(',')}`);
  await run(`${O}tp ${STK} ${X + 0.5} ${Y} ${Z + 30.5}`); await heal();

  // ================================================================== 3. through the walls
  // (a stone hut round the player - walls a block thick, a roof; the Stalker set outside it, 12 off, its cooldown spent)
  await still(); await heal();
  await run(`${O}fill ${X - 2} ${Y} ${Z - 2} ${X + 2} ${Y + 3} ${Z + 2} minecraft:stone hollow`);
  await at(X + 0.5, Y, Z + 0.5, 180, 0);
  await run(`${O}tp ${STK} ${X + 0.5} ${Y} ${Z + 12.5}`);
  await run(`${O}scoreboard players set ${STK} bm.stkwc 0`); await run(`${O}scoreboard players set ${STK} bm.stkd 999`); await run(`${O}scoreboard players set ${STK} bm.stkw 0`);
  A.bars.length = 0;
  const wound = await wait(14000, async () => { await still(); return (await sc(STK, 'bm.stkp')) > 0; }, 300);
  ok('Walled in: it can\'t get closer - and winds up ("Walls won\'t stop it.")', wound && A.bars.some(b => /Walls won't stop it/.test(b)), A.bars.slice(-2).join(' | '));
  ok('...rigid while it gathers itself (no AI)', /1b/.test(await run(`${O}data get entity ${STK} NoAI`)));
  await heal();
  const inside = async () => { const p = await pos(STK); return p && Math.abs(p[0] - (X + 0.5)) <= 1.6 && Math.abs(p[2] - (Z + 0.5)) <= 1.6 && Math.abs(p[1] - Y) < 1.5; };
  const through = await wait(8000, async () => { await still(); return inside(); }, 150);
  const sp2 = await pos(STK);
  ok('...then straight through the stone: it comes out inside the hut, beside you', through, `at ${sp2 && sp2.map(v => v.toFixed(1)).join(', ')}`);
  ok('...the walls still standing (it passes through, it doesn\'t break them)', await passes(`${O}execute if block ${X + 0.0} ${Y + 1} ${Z + 2} minecraft:stone`) &&
     await passes(`${O}execute if block ${X} ${Y} ${Z + 2} minecraft:stone`));
  await sleep(1000);
  ok('...and the chase goes on (its AI back, a cooldown before the next)', /0b/.test(await run(`${O}data get entity ${STK} NoAI`)) && (await sc(STK, 'bm.stkwc')) > 0 &&
     (await sc(STK, 'bm.stkp')) === 0, `wc ${await sc(STK, 'bm.stkwc')}, p ${await sc(STK, 'bm.stkp')}`);
  await heal();

  // ---- put things back
  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.stalker]`); await run(`${O}kill @e[tag=bm.stkpart]`);
  await run('time set 23100'); await wait(4000, async () => (await sc('#dnight', 'bm.bm')) === 0);
  await run(`${O}fill ${X - 45} ${Y - 1} ${Z - 45} ${X + 45} ${Y + 6} ${Z + 45} minecraft:air`);
  await run(`scoreboard players set TestRat bm.conq ${isNaN(saved.conq) ? 6 : saved.conq}`); await run(`scoreboard players set #hard bm.cfg ${isNaN(saved.hard) ? 0 : saved.hard}`);
  await run(`scoreboard players set #bmoff bm.cfg ${isNaN(saved.bmoff) ? 0 : saved.bmoff}`); await run('scoreboard players set #dnday bm.bm -1');
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true'); await run('gamemode creative TestRat');
  await run('time set 6000');
  await run(`${O}forceload remove ${X - 64} ${Z - 64} ${X + 64} ${Z + 64}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
