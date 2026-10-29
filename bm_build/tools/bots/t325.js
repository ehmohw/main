// 3.00: THE MARKET's NIGHTS AND THE SHIPS' MUSIC (phase250) as a regular (non-op) player - what the client hears (the sound
// and stop-sound packets, music channel) and the track the pack says it's playing (bm.mkm: 1 the theme, 2 lucky, 3 invasion,
// 4 blood moon, 5 dread; 11/12 the mothership, normal/invasion; 21/22 the Dreadnought). rcon only sets the stage: t162's
// market (placed if it's missing) with a Market Key in hand; each night started and ended by its own admin command (the
// Blood Moon forced, the clock moved); two nights at once (lucky + invasion -> invasion; dread + invasion -> dread); a
// mothership and a Vorn Dreadnought placed far out (only if they aren't there already), TestRat standing on their lower decks.
//   node t325.js
const { bot, rcon, sleep } = require('./lib_resp');
const O = 'execute in minecraft:overworld run ';
const CX = 24000, CY = 30, CZ = 24000;                               // (t162's market: template (x, y, z) at world (CX + x, CY + y, CZ + z))
const SHIPS = { mothership: [26000, 196, 26000, 'bm.tbeam', 'bm:mothership'], dreadnought: [26200, 196, 26000, 'bm.tbeam_red', 'bm:red_mothership'] };

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { const v = await fn(); if (v) return v; await sleep(step); } return null; };
  const passes = async c => /passed/i.test(await run(c));
  const score = async (who, obj) => { const m = (await run(`scoreboard players get ${who} ${obj}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const heard = (name, t0, ms) => wait(ms, async () => A.sounds.find(s => s.name === `bm:music.${name}` && s.cat === 1 && s.t >= t0));
  const stopped = (name, t0) => A.stops.some(s => s.t >= t0 && (s.sound || '') === `bm:music.${name}`);
  const tp = async (x, y, z) => { await run(`${O}tp TestRat ${x} ${y} ${z} 0 0`); await wait(3000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(300); };
  // (the nights, through their own admin commands; calm() ends them all and brings the morning)
  const calm = async () => {
    await run('scoreboard players set #forced bm.bm 0'); await run('function bm:admin/invasion_stop'); await run('scoreboard players set #lucky bm.bm 0');
    await run('scoreboard players set #dnday bm.bm -1'); await run('time set 1000'); await sleep(2500);
  };
  const night = {
    lucky: async () => { await run('time set 14000'); await run('function bm:admin/lucky_night'); await run('time set 15000'); },
    invasion: async () => { await run('time set 14000'); await run('function bm:admin/invasion_now'); await run('time set 15000'); },
    blood: async () => { await run('scoreboard players set #forced bm.bm 1'); await run('time set 15000'); },
    dread: async () => { await run('time set 14000'); await run('function bm:admin/dread_night'); await run('time set 15000'); },
  };
  // (start a stage, then: the track the pack plays for TestRat becomes `id`, and its sound reaches the client after t0)
  const expect = async (label, id, name, t0, ms = 8000) => {
    const got = await wait(ms, async () => (await score('TestRat', 'bm.mkm')) === id);
    const snd = await heard(name, t0, 3000);
    ok(`${label}: ${name} (bm.mkm ${id})`, got && snd, `bm.mkm ${await score('TestRat', 'bm.mkm')}, sound ${snd ? 'heard' : 'not heard'}`);
    return snd;
  };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await wait(4000, async () => /unknown|incomplete/i.test(A.chats.join(' ')), 200);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #mktmus bm.cfg 1'); await run('scoreboard players set #shpmus bm.cfg 1');
  const vfell = await score('#vfell', 'bm.cfg');
  await run('scoreboard players set #vfell bm.cfg 0');                  // (invasion nights possible - put back at the end)
  await calm();

  // ---- the stage: the market, TestRat inside with a key
  await run(`${O}forceload add ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) {
    for (let t = 0; t < 30; t++) { const pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
  }
  ok('the stage: t162\'s market is there', !!(await wait(40000, async () => passes(`${O}execute if entity ${MK}`), 500)));
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
  A.sounds.length = 0; A.stops.length = 0;
  let t0 = Date.now();
  await tp(CX + 38.5, CY + 10, CZ + 72.5);
  await expect('inside the market with a key, no special night', 1, 'market_theme', t0, 15000);

  // ---- each night: its own variant, the one before stopped; the night over: the theme again
  for (const [nm, id, file] of [['lucky', 2, 'market_lucky'], ['invasion', 3, 'market_invasion'], ['blood', 4, 'market_blood'], ['dread', 5, 'market_dread']]) {
    t0 = Date.now(); await night[nm]();
    const s = await expect(`a ${nm} night begins mid-track`, id, file, t0);
    ok(`...the theme was stopped as it came in`, s && stopped('market_theme', t0));
    t0 = Date.now(); await calm();
    const b = await expect(`...dawn: back to the theme`, 1, 'market_theme', t0);
    ok(`...the ${nm} variant stopped`, b && stopped(file, t0));
  }

  // ---- two nights at once: the priority (dread > blood moon > invasion > lucky)
  t0 = Date.now(); await night.lucky(); await run('function bm:admin/invasion_now'); await sleep(1500);
  ok('the stage: a Lucky Night and an invasion together', (await score('#lnight', 'bm.bm')) === 1 && (await score('#inv', 'bm.bm')) === 1);
  await expect('lucky + invasion: the invasion wins', 3, 'market_invasion', t0);
  await calm();
  t0 = Date.now(); await night.dread(); await run('function bm:admin/invasion_now'); await sleep(1500);
  ok('the stage: a Dread Night and an invasion together', (await score('#dnight', 'bm.bm')) === 1 && (await score('#inv', 'bm.bm')) === 1);
  await expect('dread + invasion: the Dread Night wins', 5, 'market_dread', t0);
  await calm();

  // ---- the loop: still the same one a few seconds on (no restart while it plays), and out of the market it stops
  t0 = Date.now(); await sleep(4000);
  ok('no restart mid-track (the theme not sent again within 4 s)', !A.sounds.some(s => s.t >= t0 && s.name === 'bm:music.market_theme'));
  t0 = Date.now(); await tp(CX + 38.5, CY + 45, CZ + 72.5);              // (up above the cavern's roof: out of the market)
  ok('out of the market: the music stops', !!(await wait(5000, async () => (await score('TestRat', 'bm.mkm')) === 0 && stopped('market_theme', t0))));
  await run('clear TestRat');

  // ---- the ships: placed far out (if not there yet), TestRat on the lower deck
  await run('gamemode creative TestRat');                               // (the Dreadnought's guards wake only for survival players)
  for (const [ship, [x, y, z, mk, tpl]] of Object.entries(SHIPS)) {
    await run(`${O}forceload add ${x} ${z} ${x + 50} ${z + 50}`); await sleep(2500);
    const sel = `@e[type=minecraft:marker,tag=${mk},x=${x + 25.5},y=${y + 7},z=${z + 25.5},distance=..2]`;
    if (!(await passes(`${O}execute if entity ${sel}`))) {
      for (let t = 0; t < 30; t++) { const pl = await run(`${O}place template ${tpl} ${x} ${y} ${z}`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
    }
    ok(`the stage: a ${ship} (its beam marker ${mk})`, !!(await wait(10000, async () => passes(`${O}execute if entity ${sel}`), 500)));
    const id = ship === 'mothership' ? 11 : 21, file = `ship_${ship}`;
    t0 = Date.now(); await tp(x + 25.5, y + 7, z + 30.5);
    await expect(`aboard the ${ship}, no special night`, id, file, t0, 10000);
    t0 = Date.now(); await night.invasion();
    const s = await expect(`aboard the ${ship}, an invasion begins`, id + 1, `${file}_inv`, t0);
    ok('...the ordinary one stopped', s && stopped(file, t0));
    t0 = Date.now(); await calm();
    await expect(`aboard the ${ship}, the invasion over`, id, file, t0);
    if (ship === 'mothership') {
      t0 = Date.now(); await run('function bm:admin/set/shpmus_0');
      ok('"Ship music" switched off: it stops', !!(await wait(4000, async () => (await score('TestRat', 'bm.mkm')) === 0 && stopped(file, t0))));
      await sleep(1500); ok('...and stays off', (await score('TestRat', 'bm.mkm')) === 0);
      t0 = Date.now(); await run('function bm:admin/set/shpmus_1');
      await expect('switched on again', id, file, t0);
    }
    t0 = Date.now(); await tp(x + 25.5, y - 30, z + 25.5);                 // (below the hull, out of the beam's reach)
    ok(`off the ${ship}: the music stops`, !!(await wait(5000, async () => (await score('TestRat', 'bm.mkm')) === 0 && stopped(file, t0))));
    await run(`${O}forceload remove ${x} ${z} ${x + 50} ${z + 50}`);
  }

  // ---- clean up
  await calm();
  if (vfell !== null) await run(`scoreboard players set #vfell bm.cfg ${vfell}`);
  await run(`${O}forceload remove ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}tp TestRat 13000.5 120 13000.5`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
