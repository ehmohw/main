// 2.80: BOSS THEMES - as a regular (non-op) player, bosses called with their own summon items (rcon only sets the stage: the
// arena, the boss held still where the test needs it, a boss's health brought down for the killing blow, a theme's clock run
// down). What the player's client is sent: the Headless Horseman's arrival starts THE WILD HUNT on the jukebox channel (not
// his old vanilla record), and the vanilla soundtrack is held off while it plays. A step back (80 blocks) doesn't stop it;
// walking well away (130) does, and coming back starts it again. When its minute is up it plays again. The Sand Pharaoh
// arriving outranks him: SANDS OF THE DEAD takes over; the Pharaoh's death (the player's blow) hands back to the Hunt; the
// Horseman's death silences it the moment it begins, and nothing plays while he dies.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => { const r = await run(cmd); const m = r.match(/has (-?\d+) \[/) || r.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/); return m ? +m[1] : NaN; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const eidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const give = async (iid, slot = 0) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); await sleep(150); };
  const HH = '@e[type=minecraft:wither_skeleton,tag=bm.hhm,limit=1]', PH = '@e[type=minecraft:husk,tag=bm.sph,limit=1]';
  const tags = (s) => run(`${O}data get entity ${s} Tags`);
  const setReal = async (s, real) => { const b = await num(`${O}scoreboard players get ${s} bm.cbuf`); await run(`${O}data modify entity ${s} Health set value ${b + real}f`); };
  const heard = (nm, since) => A.sounds.some(s => s.name === `bm:music.boss_${nm}` && s.cat === 2 && s.t >= since);
  const stopped = (nm, since) => A.stops.some(s => s.sound === `bm:music.boss_${nm}` && s.t >= since);
  const theme = () => num('scoreboard players get TestRat bm.bmt');

  // the stage: a grass platform high over the Overworld, a long walkway out from it
  const X = 18400, Y = 150, Z = 16000;
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y} ${Z + 30} minecraft:grass_block`);
  for (let y = Y + 1; y <= Y + 24; y += 8) await run(`${O}fill ${X - 30} ${y} ${Z - 30} ${X + 30} ${y + 7} ${Z + 30} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run(`${O}kill @e[type=minecraft:wither_skeleton,tag=bm.hhm]`); await run(`${O}kill @e[type=minecraft:husk,tag=bm.sph]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000'); await run('weather clear');
  for (const e of ['resistance 1200 4', 'fire_resistance 1200 0', 'regeneration 1200 3', 'saturation 1200 0', 'slow_falling 1200 0']) await run(`effect give TestRat minecraft:${e} true`);
  const at = async (dx) => { await run(`${O}tp TestRat ${X + 0.5 + dx} ${Y + 1} ${Z + 0.5} -90 0`); await sleep(300); };
  await at(0); await sleep(1500); A.stand();
  // (the walk away: a path of glass out along x, so the player stands somewhere at 80 and at 130)
  await run(`${O}fill ${X + 31} ${Y} ${Z} ${X + 140} ${Y} ${Z} minecraft:glass`);
  await run('scoreboard players set TestRat bm.bmt 0'); await run('scoreboard players set TestRat bm.bmu 0');
  await run('tag TestRat remove bm.hhsensed'); await run('tag TestRat remove bm.sphsensed');

  // ---- the Horseman: the Wild Hunt
  let t0 = Date.now(); A.sounds.length = 0; A.stops.length = 0;
  await give('sum_horseman'); await use(0);
  ok('The Horseman\'s summon item, used: he is here', await wait(3000, async () => (await cnt(HH)) === 1));
  ok('...THE WILD HUNT starts for the player, on the jukebox channel', await wait(4000, async () => heard('hunt', t0)), A.sounds.filter(s => /music/.test(s.name)).map(s => s.name).join(' '));
  ok('...his old vanilla record is not played', !A.sounds.some(s => /music_disc/.test(s.name)));
  const tHunt = Date.now();
  await sleep(3200);
  ok('...the vanilla soundtrack held off while it plays (the music channel stopped, again and again)', A.stops.filter(s => s.source === 1 && !s.sound && s.t >= tHunt).length >= 2,
     `${A.stops.filter(s => s.source === 1 && s.t >= tHunt).length} music stops`);
  await wait(9000, async () => /bm\.carm/.test(await tags(HH)));          // (his arrival over)
  // (the stage: held still in the middle, so the distances are the test's)
  await run(`${O}data merge entity ${HH} {NoAI:1b}`); await run(`${O}execute as ${HH} on vehicle run data merge entity @s {NoAI:1b}`);
  await run(`${O}execute as ${HH} on vehicle run tp @s ${X + 0.5} ${Y + 1} ${Z + 0.5}`);
  t0 = Date.now(); await at(80); A.stand();
  await sleep(3000);
  ok('A step back (80 blocks): the Hunt carries on', !stopped('hunt', t0) && (await theme()) === 1, `theme ${await theme()}`);
  t0 = Date.now(); await at(130); A.stand();
  ok('Walking well away (130): it stops', await wait(3500, async () => stopped('hunt', t0)) && (await theme()) === 0, `theme ${await theme()}`);
  t0 = Date.now(); await at(6); A.stand();
  ok('...coming back: it starts again', await wait(3500, async () => heard('hunt', t0)) && (await theme()) === 1);
  // ---- its minute up: it plays again (the stage: its clock run down to its last two seconds)
  await run('scoreboard players set TestRat bm.bmu 2');
  t0 = Date.now();
  ok('When its minute is up, it plays again (no stop between)', await wait(4500, async () => heard('hunt', t0)) && !stopped('hunt', t0));

  // ---- the Pharaoh: Sands of the Dead outranks the Hunt
  t0 = Date.now();
  await run('clear TestRat'); await give('sum_pharaoh'); await use(0);
  ok('The Pharaoh called too: SANDS OF THE DEAD takes over (the Hunt stopped)', await wait(5000, async () => heard('sands', t0) && stopped('hunt', t0)) && (await theme()) === 2,
     `theme ${await theme()}`);
  await wait(9000, async () => /bm\.carm/.test(await tags(PH)));
  // ---- the Pharaoh falls to the player's blow: back to the Hunt
  await run(`${O}data merge entity ${PH} {NoAI:1b}`); await run(`${O}tp ${PH} ${X + 8.5} ${Y + 1} ${Z + 0.5}`);
  await setReal(PH, 1);
  await wait(4000, async () => { const t = await tags(PH); return /bm\.sph_rage/.test(t) && !/bm\.cfrz/.test(t); });     // (its rage moment first)
  await run(`${O}execute at ${PH} run tp TestRat ~1.8 ${Y + 1} ~ facing entity ${PH} eyes`);
  await run('item replace entity TestRat hotbar.1 with minecraft:netherite_sword'); A.slot(1); await sleep(1300);
  t0 = Date.now();
  let id = await eidOf(PH); if (id) A.attack(id);
  ok('The Pharaoh\'s death begins: Sands stops, the Hunt comes back (the Horseman still here)', await wait(3000, async () => stopped('sands', t0) && heard('hunt', t0)) &&
     /bm\.cdie/.test(await tags(PH)) && (await theme()) === 1, `theme ${await theme()} eid ${id} hp ${await num(`${O}data get entity ${PH} Health`)} buf ${await num(`${O}scoreboard players get ${PH} bm.cbuf`)} ${(await tags(PH)).slice(-160)}`);
  await wait(9000, async () => (await cnt(PH)) === 0);

  // ---- the Horseman falls: silence as he dies
  await run(`${O}execute as ${HH} on vehicle run tp @s ${X + 0.5} ${Y + 1} ${Z + 0.5}`);
  await setReal(HH, 1);
  await wait(4000, async () => { const t = await tags(HH); return /bm\.hh_rage/.test(t) && !/bm\.cfrz/.test(t); });
  await run(`${O}execute at ${HH} run tp TestRat ~1.8 ${Y + 1} ~ facing entity ${HH} eyes`); A.slot(1); await sleep(1300);
  t0 = Date.now();
  id = await eidOf(HH); if (id) A.attack(id);
  const dying = await wait(1500, async () => /bm\.cdie/.test(await tags(HH)), 100);
  ok('The Horseman\'s death begins: the Hunt stops at once', dying && await wait(1600, async () => stopped('hunt', t0)), `eid ${id} dying ${dying} hp ${await num(`${O}data get entity ${HH} Health`)} ${(await tags(HH)).slice(-160)}`);
  await sleep(3500);
  ok('...and nothing plays while he dies', !A.sounds.some(s => /^bm:music\.boss_/.test(s.name) && s.t >= t0) && (await theme()) === 0 && (await cnt(HH)) <= 1);

  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run(`${O}fill ${X + 31} ${Y} ${Z} ${X + 140} ${Y} ${Z} minecraft:air`);
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run('clear TestRat'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
