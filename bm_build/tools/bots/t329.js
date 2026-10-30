// 3.0a: NOTHING RISES IN THE DEEP (phase255) as a regular (non-op) player, at night, standing at each dungeon's entrance.
// rcon sets the stage (the dungeons placed, the box's chunks held, TestRat let in by the admin's own way in, the mobs summoned
// as the game or a combat room would); the bot only stands there.
//   static   the two biomes as built spawn nothing (no natural_mob_spawns, no patrols, no raids); p246/roll refuses the Armada
//   under    the Undercrown's biome over the whole box (its eight corners, and #ubio); bare zombies / skeletons / piglins /
//            endermen (a natural spawn: no tags, no name), a magma cube and a ghast (no mob roll of their own), and a wanderer
//            (bm.seen and a stray tag of its own): all gone within ~2 s; a zombie summoned as its combat rooms do (bm.dgmob,
//            bm.udread) and a persistent one (a player's name-tagged pet) stay; a Dread Mire risen by its own p246/uc/* stays
//   armada   the Armada's biome over the whole box (#abio); the same natural spawns and wanderer gone; its combat rooms' kind
//            (bm.dgmob, bm.avorn) and the pet stay; a Dread Mire spawned there melts away, rig and all
//   node t329.js [static|under|armada]
const fs = require('fs');
const path = require('path');
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OUT = process.env.BM_OUT || path.join(__dirname, '..', '..', 'out_p2');
const DATA = path.join(OUT, 'BlackMarket_DP', 'data', 'bm');
const UO = [2560, 6, -2560], US = [224, 112, 224];           // (p2/undercfg.ORIGIN / SIZE)
const AO = [2560, 24, -3328], AS = [240, 96, 240];           // (p2/armadacfg.ORIGIN / SIZE)
const N = 'execute in minecraft:the_nether run ', E = 'execute in minecraft:the_end run ';
const SRC = path.join(__dirname, '..', '..');
const UVER = +fs.readFileSync(path.join(SRC, 'phase237.py'), 'utf8').match(/^UVER = (\d+)/m)[1], AVER = +fs.readFileSync(path.join(SRC, 'phase241.py'), 'utf8').match(/^AVER = (\d+)/m)[1];   // (the versions the build places: read, not hard-coded - 3.0a's UVER 7)
const box = (o, s) => `x=${o[0]},y=${o[1]},z=${o[2]},dx=${s[0] - 1},dy=${s[1] - 1},dz=${s[2] - 1}`;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const count = async (D, sel) => { const r = await run(`execute in ${D} if entity ${sel}`); return +((r.match(/count: (\d+)/i) || [0, 0])[1]); };

  // ---- static: what the build wrote
  if (on('static')) {
    for (const b of ['undercrown', 'armada']) {
      const j = JSON.parse(fs.readFileSync(path.join(DATA, 'worldgen', 'biome', b + '.json'), 'utf8'));
      const a = j.attributes || {}, ns = a['minecraft:gameplay/natural_mob_spawns'] || {};
      const arg = ns.argument || {};
      ok(`bm:${b}: no natural spawns (overridden, every category and cost empty)`, ns.modifier === 'override' && JSON.stringify(arg.spawns_by_category) === '{}' && JSON.stringify(arg.spawn_costs) === '{}', JSON.stringify(ns).slice(0, 160));
      ok(`bm:${b}: no patrols, no raids`, a['minecraft:gameplay/can_pillager_patrol_spawn'] === false && a['minecraft:gameplay/can_start_raid'] === false);
    }
    const roll = fs.readFileSync(path.join(DATA, 'function', 'p246', 'roll.mcfunction'), 'utf8').split('\n')[0];
    ok('the wild Mire\'s roll: never in the Armada (its first line)', roll === 'execute if predicate bm:p255/in_armada run return 0', roll);
    for (const t of ['zombie', 'enderman', 'piglin']) {
      const L = fs.readFileSync(path.join(DATA, 'function', 'mobs', 'init', t + '.mcfunction'), 'utf8').split('\n');
      ok(`mobs/init/${t}: a bare monster first seen in a placed box is taken before anything rolls it`, /p255\/in_under/.test(L[0]) && /p255\/in_armada/.test(L[1]) && /p255\/gone/.test(L[0]));
    }
  }
  if (!on('under') && !on('armada')) { const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`); R.end(); process.exit(p === res.length ? 0 : 1); }

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('effect give TestRat minecraft:saturation infinite 0 true');
  const day = +(((await run('time query daytime')).match(/(\d+)/) || [0, 1000])[1]);
  await run('time set midnight');
  const dfell = await sc('#dfell', 'bm.cfg');
  await run('scoreboard players set #dfell bm.cfg 0');          // (the Dread unfallen: a fallen Dread melts every Mire)

  // ---- one dungeon: TestRat at its entrance; the natural spawns gone, the dungeon's own and the pet kept
  const play = async (key, D, o, s, ver, VER, bio, biome, keepTags) => {
    const B = box(o, s), X = `execute in ${D} run `;
    if ((await sc(ver, 'bm.p2')) !== VER) await run(`function bm:admin/${key === 'under' ? 'under' : 'armada'}/place`);
    ok(`the stage: ${key} placed`, await wait(900000, async () => (await sc(ver, 'bm.p2')) === VER, 2000));
    await run(`${X}forceload add ${o[0]} ${o[2]} ${o[0] + s[0] - 1} ${o[2] + s[2] - 1}`); await sleep(4000);
    // (the biome: every corner of the box; and the world knows it's done)
    ok(`${key}: the biome filled (${bio})`, await wait(30000, async () => (await sc(bio, 'bm.p2')) >= 1, 1000), String(await sc(bio, 'bm.p2')));
    const corners = []; for (const x of [o[0], o[0] + s[0] - 1]) for (const y of [o[1], o[1] + s[1] - 1]) for (const z of [o[2], o[2] + s[2] - 1]) corners.push([x, y, z]);
    const miss = [];
    for (const c of corners) if (!/passed/i.test(await run(`execute in ${D} if biome ${c[0]} ${c[1]} ${c[2]} ${biome}`))) miss.push(c.join(' '));
    ok(`${key}: ${biome} at all eight corners of the box`, miss.length === 0, miss.join(' | '));
    await run(`execute as TestRat run function bm:admin/${key === 'under' ? 'under' : 'armada'}/go`);     // (in, and admitted: phase251's own admin way)
    await wait(4000, async () => A.pos && A.pos.x >= o[0] && A.pos.x < o[0] + s[0] && A.pos.z >= o[2] && A.pos.z < o[2] + s[2]);
    await sleep(2500);
    const at = `execute in ${D} at TestRat run `;
    // (the natural spawns: bare - no tags, no name - as the game puts them; a wanderer from outside: seen, a stray tag)
    const kinds = ['zombie', 'skeleton', 'piglin', 'enderman', 'magma_cube', 'ghast'];
    let made = 0;
    for (const t of kinds) if (/Summoned/.test(await run(`${at}summon minecraft:${t}`))) made++;
    if (/Summoned/.test(await run(`${at}summon minecraft:zombified_piglin ~ ~ ~ {Tags:["bm.seen","bm.t329w"]}`))) made++;
    // (the dungeon's own, as its combat rooms summon them; and a player's name-tagged pet)
    await run(`${at}summon minecraft:zombie ~ ~ ~ {Tags:["bm.seen","bm.dgmob",${keepTags},"bm.t329k"]}`);
    await run(`${at}summon minecraft:skeleton ~ ~ ~ {Tags:["bm.t329k"],PersistenceRequired:1b,CustomName:"Bonesy"}`);
    // (counted round TestRat - none of the dungeon's own, nor the two kept)
    const bareAt = async () => { let n = 0; for (const t of kinds) { const r = await run(`execute in ${D} at TestRat if entity @e[type=minecraft:${t},distance=..32,tag=!bm.dgmob,tag=!bm.t329k,tag=!bm.mire]`); n += +((r.match(/count: (\d+)/i) || [0, 0])[1]); } return n; };
    ok(`${key}: six natural spawns and a wanderer summoned at TestRat`, made === kinds.length + 1, String(made));
    ok(`${key}: ...and within ~2 s every one is gone (zombie, skeleton, piglin, enderman, magma cube, ghast)`, await wait(3000, async () => (await bareAt()) === 0, 200), String(await bareAt()) + ' ' + (await Promise.all(kinds.map(async t => t + ':' + ((await run(`execute in ${D} at TestRat if entity @e[type=minecraft:${t},distance=..32,tag=!bm.dgmob,tag=!bm.t329k,tag=!bm.mire]`)).match(/count: (\d+)/i) || [0, 0])[1] + ((await run(`execute in ${D} at TestRat run data get entity @e[type=minecraft:${t},distance=..32,tag=!bm.dgmob,tag=!bm.t329k,tag=!bm.mire,limit=1] Tags`)).match(/data: (.*)$/) || ['', ''])[1].slice(0, 80)))).join(' '));
    ok(`${key}: ...the wanderer too (seen elsewhere, a tag none of the dungeon's)`, await wait(2000, async () => (await count(D, `@e[${B},tag=bm.t329w]`)) === 0, 200));
    await sleep(3000);
    ok(`${key}: the combat rooms' own kind stays (bm.dgmob, ${keepTags})`, (await count(D, `@e[type=minecraft:zombie,${B},tag=bm.t329k,tag=bm.dgmob]`)) === 1,
       `anywhere ${await count(D, '@e[tag=bm.t329k]')} | ${(await run(`${X}data get entity @e[tag=bm.t329k,limit=1] Pos`)).slice(-60)} | me ${(await run(`${X}data get entity TestRat Pos`)).slice(-60)}`);
    ok(`${key}: a player's name-tagged pet stays`, (await count(D, `@e[type=minecraft:skeleton,${B},tag=bm.t329k]`)) === 1);
    await run(`${X}execute as @e[${B},tag=bm.t329k] on passengers run kill @s`);
    await run(`${X}execute as @e[${B},tag=bm.t329k] at @s run tp @s ~ -400 ~`); await run(`${X}kill @e[tag=bm.t329k]`);
    return { at, X, B };
  };

  if (on('under')) {
    const { at, X, B } = await play('under', 'minecraft:the_nether', UO, US, '#uver', UVER, '#ubio', 'bm:undercrown', '"bm.udread","bm.udk_zombie"');
    // (a Dread Mire risen by the Undercrown's own: let down from the nearest room's fx marker, as p246/uc/try does)
    const m0 = await count('minecraft:the_nether', `@e[type=minecraft:husk,tag=bm.mire,tag=bm.muc,${B}]`);
    await run(`${at}execute as @e[type=minecraft:marker,tag=bm.dgfx,tag=bm.d_under,sort=nearest,limit=1] at @s run function bm:p246/uc/down`);
    let m1 = await count('minecraft:the_nether', `@e[type=minecraft:husk,tag=bm.mire,tag=bm.muc,${B}]`);
    if (m1 === m0) { await run(`${at}function bm:p246/uc/down`); m1 = await count('minecraft:the_nether', `@e[type=minecraft:husk,tag=bm.mire,tag=bm.muc,${B}]`); }   // (no floor under that marker: at TestRat's feet)
    ok('under: a Dread Mire rises by its own function (p246/uc/*)', m1 === m0 + 1, `${m0} -> ${m1}`);
    await sleep(4000);
    ok('under: ...and stays (the Mires are the Undercrown\'s own)', (await count('minecraft:the_nether', `@e[type=minecraft:husk,tag=bm.mire,tag=bm.muc,${B}]`)) === m1);
    await run(`${X}execute as @e[type=minecraft:husk,tag=bm.mire,tag=bm.muc,${B}] at @s run function bm:p246/melt`);
    await run(`execute as TestRat run function bm:admin/under/outside`); await sleep(1000);
  }

  if (on('armada')) {
    const { at, X, B } = await play('armada', 'minecraft:the_end', AO, AS, '#aver', AVER, '#abio', 'bm:armada', '"bm.avorn","bm.avk_zombie"');
    // (a Dread Mire in the Armada - spawned straight in, as the roll would: it melts away, rig and all)
    await run(`${at}function bm:p246/spawn`);
    ok('armada: a Dread Mire spawned aboard melts away within ~2 s', await wait(3000, async () => (await count('minecraft:the_end', `@e[type=minecraft:husk,tag=bm.mire,tag=!bm.mtame,${B}]`)) === 0, 200));
    const parts = +(((await run(`execute in minecraft:the_end at TestRat if entity @e[type=minecraft:item_display,tag=bm.mr,distance=..8]`)).match(/count: (\d+)/i) || [0, 0])[1]);
    ok('armada: ...none of its parts left behind', parts === 0, String(parts));
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`); await sleep(1000);
  }

  await run(`time set ${day}`); await run(`scoreboard players set #dfell bm.cfg ${dfell === -99 ? 0 : dfell}`);
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
