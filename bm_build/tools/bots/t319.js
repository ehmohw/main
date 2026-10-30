// 2.99a: THE STATUE KNIGHTS (phase245) as a regular (non-op) player. rcon sets the stage (hard mode, the dungeon placed, the trials
// before the guarded one solved, a knight's health brought to the edge); the bot plays: it drops the Ciphers / the Crown Shards,
// stands by the knights while they fight, strikes them down, and sets a statue up at home and takes it back.
//   lock     the Armada's Command Lock: two Vorn Sentinels stand there as statues; the three Ciphers dropped: they wake (the door
//            stays shut, the room's bar shows), one strikes you; struck down: they turn to stone, their statues are yours, the door opens
//   gate     the Undercrown's Throne Gate: the same with the Dread Sentinels and the three Crown Shards
//   home     a Dread Sentinel's Statue: sneak + use on a block sets it up; sneak + punch takes it back
//   guard    (3.0) a Dread Sentinel's Statue set up, right-clicked: its dialog; "Stand guard": it wakes (live), a zombie (rcon) near it
//            is struck down, you are never hurt and your own blow does nothing; right-clicked again, "Rest": stone on its plinth.
//            "Duel me": it wakes against you, its bar shows, its mace lands; brought to the edge (rcon) and struck: it falls, its
//            plinth empties and its statue drops - picked up. A Vorn Sentinel's Statue the same way to "Stand guard" and "Rest".
//   node t319.js [lock|gate|home|guard]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const AO = [2560, 24, -3328], UO = [2560, 6, -2560];          // (p2/armadacfg.ORIGIN, p2/undercfg.ORIGIN)
const AW = (x, y, z) => [AO[0] + x, AO[1] + y, AO[2] + z], UW = (x, y, z) => [UO[0] + x, UO[1] + y, UO[2] + z];
const E = 'execute in minecraft:the_end run ', N = 'execute in minecraft:the_nether run ';
const FLOOR = 100;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (D, sel) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const block = async (D, p, b) => /passed/i.test(await run(`${D}execute if block ${p[0]} ${p[1]} ${p[2]} ${b}`));
  const hp = async () => +(((await run('data get entity TestRat Health')).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (D, sel) => { const u = await uuidOf(D, sel); return Object.values(A.ents).find(e => e.objectUUID === u); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (2.99a: phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('scoreboard players set #hard bm.cfg 1'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 2 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('effect clear TestRat');      // (no Resistance left over from an earlier test - the maces must land)
  await run('effect give TestRat minecraft:regeneration infinite 1 true');

  // ---- the knights of one room: watched as statues, woken by the puzzle, fought, struck down
  const room = async (D, d, n, kind, name, gate, gateBlock, solve, near) => {
    const G = `tag=bm.kg_${d}${n}`;
    const host = `@e[type=minecraft:husk,${G}]`;
    await at(D, near[0], near[1], near[2]); await sleep(3000);
    ok(`two ${name}s stand there as statues (stone: ${13 * 2} parts)`, await wait(6000, async () => (await cnt(D, `@e[type=minecraft:marker,tag=bm.kstat,tag=bm.kn${n},tag=bm.d_${d},scores={bm.kst=1}]`)) === 2 &&
       (await cnt(D, `@e[type=minecraft:item_display,tag=bm.kr,distance=..40,x=${near[0]},y=${near[1]},z=${near[2]}]`)) >= 26));
    A.titles.length = 0;
    await solve();
    ok('...the puzzle solved: they wake ("The statues stir")', await wait(6000, async () => (await cnt(D, host)) === 2) && A.titles.some(t => /statues stir/i.test(t)), A.titles.slice(-2).join(' / ') + ` | hosts ${await cnt(D, host)} dg ${await run(`${D}execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_${d}] run scoreboard players get @s bm.pz`)} done ${await run(`${D}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz${n},tag=bm.d_${d}] run scoreboard players get @s bm.done`)} items ${await cnt(D, '@e[type=minecraft:item,distance=..30,x=' + near[0] + ',y=' + near[1] + ',z=' + near[2] + ']')}`);
    ok('...and the door stays shut', await block(D, gate, gateBlock));
    await sleep(2500);
    ok('...stone no longer: awake, eyes lit (the live models)', /_live_/.test(await run(`${D}data get entity @e[type=minecraft:item_display,tag=bm.kr_head,distance=..40,x=${near[0]},y=${near[1]},z=${near[2]},sort=nearest,limit=1] item.components."minecraft:item_model"`)));
    ok('...the room\'s bar shows them', await wait(4000, async () => /has [1-9]/.test(await run(`bossbar get bm:kn_${d}${n} players`))), await run(`bossbar get bm:kn_${d}${n} players`));
    // (stand beside one: it slams or spins at you)
    const h0 = await hp(); const k = await pos(D, `${host.slice(0, -1)},limit=1]`);
    let hurt = false;
    for (let i = 0; i < 40 && !hurt; i++) { const kp = await pos(D, `${host.slice(0, -1)},limit=1]`) || k; await run(`${D}tp TestRat ${kp[0] + 1.5} ${kp[1]} ${kp[2]}`); await sleep(500); hurt = (await hp()) < h0 - 0.5; }
    ok(`a ${name} strikes you (its mace)`, hurt, `${h0} -> ${await hp()}`);
    // (struck down, each: its strength brought to the edge, then a blow from you)
    for (let i = 0; i < 2; i++) {
      const sel = `${host.slice(0, -1)},scores={bm.ks=1..4},limit=1]`;
      const kp = await pos(D, sel); if (!kp) break;
      await run(`${D}execute as ${sel} run data modify entity @s Health set value ${FLOOR + 1}f`);
      await at(D, kp[0] + 1.5, kp[1], kp[2], 90, 0);
      const e = await entOf(D, sel); if (e) { A.attack(e.entityId); await sleep(300); A.attack(e.entityId); }
      await sleep(800);
    }
    ok(`struck down: both fall, kneel and turn to stone`, await wait(8000, async () => (await cnt(D, host)) === 0) &&
       /_stone_/.test(await run(`${D}data get entity @e[type=minecraft:item_display,tag=bm.kr_head,distance=..40,x=${near[0]},y=${near[1]},z=${near[2]},sort=nearest,limit=1] item.components."minecraft:item_model"`)));
    ok(`...their statues are yours (${kind})`, (await has(`knight_statue_${kind}`)) >= 1, String(await has(`knight_statue_${kind}`)));
    ok('...and the door opens', await wait(4000, async () => !(await block(D, gate, gateBlock))));
  };

  if (on('lock')) {
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`);
    if ((await sc('#aver', 'bm.p2')) < 5) await run('function bm:admin/armada/place');
    ok('the stage: the Armada placed (version 5: its Sentinels and the hangar)', await wait(900000, async () => (await sc('#aver', 'bm.p2')) >= 5, 2000));
    await run(`${E}forceload add ${AO[0]} ${AO[2]} ${AO[0] + 239} ${AO[2] + 239}`); await sleep(5000);
    const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_armada,limit=1]';
    // (the dungeon's markers loaded before the stage is set: a chunk's entities come a while after it - set too soon, bm.pz stayed
    //  0, the Ciphers did nothing and the knights never woke)
    ok('...its markers loaded (the dungeon, the Lock\'s puzzle)', await wait(90000, async () => (await cnt(E, DG)) === 1 &&
       (await cnt(E, '@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,tag=bm.d_armada]')) === 1, 1000));
    await run(`${E}scoreboard players set ${DG} bm.pz 16`);
    await run(`${E}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,tag=bm.d_armada] at @s run function bm:p2/armada/pz17_reset`);
    // (and its door shut again: a room's reset leaves its door as it was - only the dungeon's whole reset closes them - and the last run opened it)
    await run(`${E}execute as @e[type=minecraft:marker,tag=bm.gate,tag=bm.g17,tag=bm.d_armada] at @s run function bm:p2/armada/gate_close`);
    const c = AW(20, 55, 144);
    await room(E, 'armada', 17, 'vorn', 'Vorn Sentinel', AW(8, 55, 152), 'minecraft:lime_stained_glass', async () => {
      for (const [x, ci] of [[14, 'cipher_1'], [20, 'cipher_2'], [26, 'cipher_3']]) {
        const p = AW(x, 56, 146); await at(E, p[0] + 0.5, p[1], p[2] + 1.5, 180, 40); await sleep(400);
        await run(`loot replace entity TestRat hotbar.0 loot bm:items/${ci}`); A.slot(0); await sleep(300); A.drop(); await sleep(1500);
      }
    }, [c[0] + 0.5, c[1], c[2] + 0.5]);
    await run(`${E}forceload remove ${AO[0]} ${AO[2]} ${AO[0] + 239} ${AO[2] + 239}`);
  }

  if (on('gate')) {
    await run(`${N}tp TestRat ${UO[0] - 40} 100 ${UO[2] - 40}`); await run(`${N}setblock ${UO[0] - 40} 98 ${UO[2] - 40} minecraft:obsidian`);
    for (const b of ['snow', 'witch', 'shark']) await run(`scoreboard players set TestRat bm.dbwin_${b} 1`);
    if ((await sc('#uver', 'bm.p2')) !== 7) await run('function bm:admin/under/place');
    ok('the stage: the Undercrown placed (version 7: its Sentinels)', await wait(900000, async () => (await sc('#uver', 'bm.p2')) === 7, 2000));
    const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
    await run(`${N}forceload add ${UO[0] + 96} ${UO[2] + 104} ${UO[0] + 128} ${UO[2] + 136}`); await sleep(3000);
    ok('...its markers loaded (the dungeon, the Gate\'s puzzle)', await wait(90000, async () => (await cnt(N, DG)) === 1 &&
       (await cnt(N, '@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz16,tag=bm.d_under]')) === 1, 1000));      // (as the Lock: else the reset missed, the door left open)
    await run(`${N}scoreboard players set ${DG} bm.pz 15`);
    await run(`${N}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz16,tag=bm.d_under] at @s run function bm:p2/under/pz16_reset`);
    await run(`${N}execute as @e[type=minecraft:marker,tag=bm.gate,tag=bm.g16,tag=bm.d_under] at @s run function bm:p2/under/gate_close`);      // (its door shut again, as the Lock's)
    const c = UW(112, 18, 126);
    await room(N, 'under', 16, 'dread', 'Dread Sentinel', UW(112, 18, 116), 'minecraft:crying_obsidian', async () => {
      for (const s of ['snow', 'witch', 'shark']) {
        const p = await pos(N, `@e[type=minecraft:marker,tag=bm.ok_${s},limit=1]`);
        await run(`loot replace entity TestRat hotbar.0 loot bm:items/ushard_${s}`); await at(N, p[0], p[1], p[2] - 0.6, 0, 70);
        A.slot(0); await sleep(200); A.drop(true); await sleep(1500);
      }
    }, [c[0] + 0.5, c[1], c[2] + 0.5]);
    await run(`${N}forceload remove ${UO[0] + 96} ${UO[2] + 104} ${UO[0] + 128} ${UO[2] + 136}`);
    for (const b of ['snow', 'witch', 'shark']) await run(`scoreboard players reset TestRat bm.dbwin_${b}`);      // (the bosses' wins given: off again,
    await run('tag TestRat remove bm.usum'); await run('clear TestRat *[minecraft:custom_data~{bm:"usummons"}]');   //  and the Summons they earned)
  }

  if (on('home')) {
    const O = 'execute in minecraft:overworld run ';
    await run(`${O}forceload add 18384 15984 18416 16016`); await sleep(2000);      // (the stage's chunks: the bot may log in far off, and a fill there is "not loaded")
    await run(`${O}fill 18390 100 15990 18410 104 16010 minecraft:air`); await run(`${O}fill 18390 99 15990 18410 99 16010 minecraft:stone`);
    await at(O, 18400.5, 100, 16000.5, 0, 60); await run('clear TestRat');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/knight_statue_dread'); A.slot(0); await sleep(400);
    A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
    ok('the statue, sneak + used on a block: it stands there', (await cnt(O, '@e[type=minecraft:item_display,tag=bm.knsd_dread,distance=..4,x=18400,y=100,z=16001]')) === 1 &&
       (await has('knight_statue_dread')) === 0);
    const e = await entOf(O, '@e[type=minecraft:interaction,tag=bm.knst_dread,limit=1,sort=nearest,x=18400,y=100,z=16001]');
    A.input({ shift: true }); await sleep(300); if (e) A.attack(e.entityId); await sleep(600); A.input({}); await sleep(600);
    ok('...sneak + punched: back in your pack', (await has('knight_statue_dread')) === 1 && (await cnt(O, '@e[type=minecraft:item_display,tag=bm.knsd_dread,distance=..4,x=18400,y=100,z=16001]')) === 0);
    await run(`${O}kill @e[type=minecraft:interaction,tag=bm.knst,distance=..6,x=18400,y=100,z=16001]`);
  }

  if (on('guard')) {
    const O = 'execute in minecraft:overworld run ';
    const X = 18400, Y = 100, Z = 16000;
    const near = `distance=..12,x=${X},y=${Y},z=${Z + 1}`;
    await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(2000);      // (as above: else the fills fail and the statue falls to the ground)
    await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 5} ${Z + 12} minecraft:air`); await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`);
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t319z]`); await run('difficulty normal');
    const place = async (kind) => {
      await at(O, X + 0.5, Y, Z + 0.5, 0, 60); await run('clear TestRat');
      await run(`loot replace entity TestRat hotbar.0 loot bm:items/knight_statue_${kind}`); A.slot(0); await sleep(400);
      A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
      return cnt(O, `@e[type=minecraft:interaction,tag=bm.knst_${kind},${near}]`);
    };
    const statue = (kind) => `@e[type=minecraft:interaction,tag=bm.knst_${kind},${near},limit=1]`;
    const host = (kind) => `@e[type=minecraft:husk,tag=bm.kh_${kind},tag=bm.khome,${near.replace('..12', '..24')},limit=1]`;
    const click = async (kind) => {      // (right-click its plinth, standing, as a player does - and wait for a screen)
      const e = await entOf(O, statue(kind)); if (!e) return false;
      const n0 = A.dialogN.length; A.interact(e.entityId, false);
      return wait(3000, async () => A.dialogN.length > n0, 100);
    };
    const model = async () => await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.kr_head,${near},sort=nearest,limit=1] item.components."minecraft:item_model"`);
    const shown = async (kind) => /scale: \[1\.0f/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.knsd_${kind},${near},limit=1] transformation`));

    // ---- the Dread Sentinel: on guard
    ok('a Dread Sentinel\'s Statue set up (sneak + use)', (await place('dread')) === 1);
    await at(O, X + 0.5, Y, Z - 2.5, 0, 10);
    ok('...right-clicked: its dialog ("Stand guard", "Duel me")', await click('dread') && A.buttons().some(b => /Stand guard/.test(b.label)) && A.buttons().some(b => /Duel me/.test(b.label)),
       JSON.stringify(A.buttons().map(b => b.label)));
    await A.press(/Stand guard/);
    ok('..."Stand guard": it wakes (a guard: its host, the stone hidden)', await wait(4000, async () => (await cnt(O, host('dread'))) === 1) && !(await shown('dread')));
    ok('...stone no longer: the live models', await wait(5000, async () => /_live_/.test(await model())), await model());
    ok('...its plinth knows its owner (bm.pid) and that it is on guard (bm.kgm 1)', (await sc(statue('dread'), 'bm.kgm')) === 1 && (await sc(statue('dread'), 'bm.pid')) === (await sc('TestRat', 'bm.pid')));
    await sleep(1500);
    const h0 = await hp(); let lo = h0;
    const g = await entOf(O, host('dread'));
    if (g) { await at(O, X + 0.5, Y, Z - 0.2, 0, 10); A.attack(g.entityId); await sleep(600); A.attack(g.entityId); await sleep(600); }
    const gh = async () => +(((await run(`${O}data get entity ${host('dread')} Health`)).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
    ok('...your own blows do it no harm (a guard)', (await gh()) >= 339.5, String(await gh()));
    await at(O, X + 0.5, Y, Z - 3.5, 0, 10);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 6.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t319z","bm.seen"],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b,show_particles:0b}]}`);
    const dead = await wait(30000, async () => { lo = Math.min(lo, await hp()); return (await cnt(O, '@e[type=minecraft:zombie,tag=bm.t319z]')) === 0; }, 250);
    ok('...a zombie near it: struck down by the guard', dead);
    ok('...and you were never hurt', lo >= h0 - 0.5, `${h0} -> lowest ${lo}`);
    ok('...back on its post after', await wait(10000, async () => { const p = await pos(O, host('dread')); return p && Math.hypot(p[0] - (X + 0.5), p[2] - (Z + 1.5)) < 1.2; }), String(await pos(O, host('dread'))));
    await at(O, X + 0.5, Y, Z - 2.5, 0, 10);
    ok('...right-clicked again: "Rest"', await click('dread') && A.buttons().some(b => /Rest/.test(b.label)), JSON.stringify(A.buttons().map(b => b.label)));
    await A.press(/Rest/);
    ok('..."Rest": a statue on its plinth again (no host, the stone shown, bm.kgm 0)', await wait(8000, async () => (await cnt(O, host('dread'))) === 0 && await shown('dread')) &&
       (await sc(statue('dread'), 'bm.kgm')) === 0 && (await cnt(O, `@e[type=minecraft:item_display,tag=bm.kr,${near}]`)) === 0);

    // ---- the Dread Sentinel: a duel
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:regeneration infinite 1 true');
    ok('right-clicked: "Duel me"', await click('dread') && !!(await A.press(/Duel me/)));
    ok('...it wakes to duel you (bm.kduel, bm.kgm 2)', await wait(4000, async () => (await cnt(O, `@e[type=minecraft:husk,tag=bm.kduel,${near}]`)) === 1) && (await sc(statue('dread'), 'bm.kgm')) === 2);
    await sleep(2500);
    ok('...its bar shows', await wait(4000, async () => /TestRat/.test(await run('bossbar get bm:kduel1 players'))), await run('bossbar get bm:kduel1 players'));
    A.dialogN.length = 0;
    ok('...right-clicked mid-duel: no dialog ("a duel is under way")', !(await click('dread')));
    const d0 = await hp(); let hurt = false;
    for (let i = 0; i < 40 && !hurt; i++) { const kp = await pos(O, host('dread')); if (kp) await run(`${O}tp TestRat ${kp[0] + 1.5} ${kp[1]} ${kp[2]}`); await sleep(500); hurt = (await hp()) < d0 - 0.5; }
    ok('...its mace lands on you', hurt, `${d0} -> ${await hp()}`);
    await run('effect give TestRat minecraft:resistance 60 3 true');
    const kp = await pos(O, host('dread'));
    await run(`${O}data modify entity ${host('dread')} Health set value ${FLOOR + 1}f`);
    if (kp) await at(O, kp[0] + 1.5, kp[1], kp[2], 90, 0);
    const e = await entOf(O, host('dread')); if (e) { A.attack(e.entityId); await sleep(300); A.attack(e.entityId); }
    ok('...struck down: it falls (no host), its plinth empty (no statue, no interaction)', await wait(8000, async () => (await cnt(O, host('dread'))) === 0) &&
       (await cnt(O, `@e[type=minecraft:interaction,tag=bm.knst_dread,${near.replace('..12', '..40')}]`)) === 0 && (await cnt(O, `@e[type=minecraft:item_display,tag=bm.knsd_dread,${near.replace('..12', '..40')}]`)) === 0);
    const it = await pos(O, `@e[type=minecraft:item,${near.replace('..12', '..40')},nbt={Item:{components:{"minecraft:custom_data":{bm:"knight_statue_dread"}}}},limit=1]`);
    ok('...and its statue drops', !!it, String(it));
    if (it) await at(O, it[0], it[1], it[2]);
    ok('...picked up: yours again', await wait(4000, async () => (await has('knight_statue_dread')) === 1));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:regeneration infinite 1 true');

    // ---- the Vorn Sentinel: on guard, and at rest
    await run(`${O}kill @e[type=minecraft:item,${near.replace('..12', '..40')}]`);
    ok('a Vorn Sentinel\'s Statue set up', (await place('vorn')) === 1);
    await at(O, X + 0.5, Y, Z - 2.5, 0, 10);
    ok('...right-clicked, "Stand guard": it wakes, live', await click('vorn') && !!(await A.press(/Stand guard/)) &&
       await wait(6000, async () => (await cnt(O, host('vorn'))) === 1 && /_live_/.test(await model())));
    await sleep(1000);
    ok('..."Rest": stone again', await click('vorn') && !!(await A.press(/Rest/)) && await wait(8000, async () => (await cnt(O, host('vorn'))) === 0 && await shown('vorn')));
    const v = await entOf(O, statue('vorn'));
    A.input({ shift: true }); await sleep(300); if (v) A.attack(v.entityId); await sleep(600); A.input({}); await sleep(600);
    ok('...sneak + punched: back in your pack', (await has('knight_statue_vorn')) === 1);
    await run(`${O}kill @e[type=minecraft:interaction,tag=bm.knst,${near.replace('..12', '..40')}]`); await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t319z]`);
  }

  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  await run('effect clear TestRat');              // (the Regeneration and Fire Resistance given at the start, and any Resistance)
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
