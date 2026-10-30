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
const { AO, AS } = require('./armada_cfg');                  // (p2/armadacfg.ORIGIN / SIZE - 3.0e: high in the End's sky)
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
    ok('the wild Mire\'s roll: never in or near the Armada (its first line)', roll === 'execute if predicate bm:p255/near_armada run return 0', roll);
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
  const dfell = await sc('#dfell', 'bm.cfg'), hard = await sc('#hard', 'bm.cfg'), active = await sc('#active', 'bm.bm');
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
    // 3.0e: NO DREAD MIRES IN THE ARMADA - they're the Dread's, not the Vorn's
    const END = 'minecraft:the_end', NEAR = 48;
    const NB = `x=${AO[0] - NEAR},y=${AO[1] - NEAR},z=${AO[2] - NEAR},dx=${AS[0] + 2 * NEAR - 1},dy=${AS[1] + 2 * NEAR - 1},dz=${AS[2] + 2 * NEAR - 1}`;
    const mires = async (sel = NB) => count(END, `@e[type=minecraft:husk,tag=bm.mire,${sel}]`);
    await run('scoreboard players set #hard bm.cfg 1'); await run('scoreboard players set #active bm.bm 1');      // (hard mode; a Blood Moon's 3x odds)
    // (forced rolls aboard: the wild Mire's natural roll, run again and again as a monster rising at TestRat's feet)
    await run(`${at}summon minecraft:zombie ~ ~ ~ {NoAI:1b,Silent:1b,Tags:["bm.seen","bm.dgmob","bm.avorn","bm.t329r"]}`);
    let rolled = 0;
    for (let i = 0; i < 900; i++) {
      await run('scoreboard players reset TestRat bm.mday');
      await run(`execute in ${END} as @e[type=minecraft:zombie,tag=bm.t329r,limit=1] at @s run function bm:p246/roll`); rolled++;
      if (i % 150 === 149 && (await mires()) > 0) break;
    }
    ok(`armada: ${rolled} forced Mire rolls with TestRat aboard (hard mode, a Blood Moon's odds) - no Mire anywhere in or within ${NEAR} of the fleet`, (await mires()) === 0, String(await mires()));
    // (straight in, as any caller of p246/spawn would: refused there itself)
    await run(`${at}function bm:p246/spawn`); await sleep(300);
    ok('armada: p246/spawn aboard - refused, no Mire', (await mires()) === 0);
    // (a Mire Heart, sneak + used on the deck: refused, kept)
    await run('loot replace entity TestRat hotbar.0 loot bm:items/mire_heart'); A.slot(0); await sleep(300); A.bars.length = 0;
    await run(`execute in ${END} as TestRat at @s run tp @s ~ ~ ~ ~ 70`); await sleep(600);
    A.input({ shift: true }); await sleep(300); A.use(); await sleep(900); A.release(); A.input({}); await sleep(600);
    const heart = +(((await run('clear TestRat *[minecraft:custom_data~{bm:"mire_heart"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
    ok('armada: a Mire Heart planted aboard - refused, the Heart kept, no Mire', heart === 1 && (await mires()) === 0 && A.bars.some(b => /hive-fleet/.test(b)), `heart ${heart}, bars ${A.bars.slice(-2).join(' | ')}`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"mire_heart"}]');
    // (one that gets in anyway: risen out in the void and teleported aboard - it melts, rig and all)
    const far = [AO[0] + AS[0] + 400, 100, AO[2]];
    await run(`${E}forceload add ${far[0]} ${far[2]}`); await run(`${E}setblock ${far[0]} ${far[1] - 1} ${far[2]} minecraft:obsidian`); await sleep(1500);
    await run(`execute in ${END} positioned ${far[0]}.5 ${far[1]} ${far[2]}.5 run function bm:p246/spawn`);
    const out1 = await count(END, `@e[type=minecraft:husk,tag=bm.mire,x=${far[0]},y=${far[1]},z=${far[2]},distance=..2]`);
    await run(`execute in ${END} as @e[type=minecraft:husk,tag=bm.mire,x=${far[0]},y=${far[1]},z=${far[2]},distance=..2] at TestRat run tp @s ~ ~ ~`);
    ok('armada: a Dread Mire teleported aboard melts away within ~2 s', out1 === 1 && await wait(3000, async () => (await mires(B)) === 0, 200), `spawned ${out1}`);
    const parts = +(((await run(`execute in ${END} if entity @e[type=minecraft:item_display,tag=bm.mr]`)).match(/count: (\d+)/i) || [0, 0])[1]);
    ok('armada: ...none of its parts left behind', parts === 0, String(parts));
    await run(`execute in ${END} as @e[type=minecraft:zombie,tag=bm.t329r] at @s run tp @s ~ -400 ~`); await run(`${E}kill @e[tag=bm.t329r]`);
    // (the positive control: the same forced rolls in the outer End, far from the fleet - a Mire can still rise there)
    // (a closed obsidian room: the End's open sky is too bright for a Mire - p246/dark wants light 4 or less)
    const ROOM = `${far[0] - 3} ${far[1] - 1} ${far[2] - 3} ${far[0] + 9} ${far[1] + 3} ${far[2] + 3}`;
    await run(`${E}fill ${ROOM} minecraft:obsidian hollow`);
    await run(`${E}tp TestRat ${far[0] + 6}.5 ${far[1]} ${far[2]}.5`); await sleep(2500);
    await run(`${E}summon minecraft:zombie ${far[0]}.5 ${far[1]} ${far[2]}.5 {NoAI:1b,Silent:1b,Tags:["bm.seen","bm.t329r"]}`);
    const FB = `x=${far[0] - 3},y=${far[1] - 2},z=${far[2] - 3},dx=6,dy=5,dz=6`;
    let n = 0;
    for (; n < 3000 && (await count(END, `@e[type=minecraft:husk,tag=bm.mire,${FB}]`)) === 0; n++) {
      await run('scoreboard players reset TestRat bm.mday');
      await run(`execute in ${END} as @e[type=minecraft:zombie,tag=bm.t329r,limit=1] at @s run function bm:p246/roll`);
    }
    ok('armada: ...the same rolls in the outer End, far from it: a Mire still rises there', (await count(END, `@e[type=minecraft:husk,tag=bm.mire,${FB}]`)) === 1, `after ${n} rolls`);
    await run(`execute in ${END} as @e[type=minecraft:husk,tag=bm.mire,${FB}] at @s run function bm:p246/melt`);
    await run(`execute in ${END} as @e[type=minecraft:zombie,tag=bm.t329r] at @s run tp @s ~ -400 ~`); await run(`${E}kill @e[tag=bm.t329r]`);
    await run(`${E}tp TestRat 1200.5 89 0.5`); await sleep(500); await run(`${E}fill ${ROOM} minecraft:air`);
    await run('scoreboard players reset TestRat bm.mday'); await run(`scoreboard players set #active bm.bm ${active === -99 ? 0 : active}`); await run(`scoreboard players set #hard bm.cfg ${hard === -99 ? 0 : hard}`);
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`); await sleep(1000);
  }

  await run(`time set ${day}`); await run(`scoreboard players set #dfell bm.cfg ${dfell === -99 ? 0 : dfell}`);
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
