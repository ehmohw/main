// 2.99a: THE STATUE KNIGHTS (phase245) as a regular (non-op) player. rcon sets the stage (hard mode, the dungeon placed, the trials
// before the guarded one solved, a knight's health brought to the edge); the bot plays: it drops the Ciphers / the Crown Shards,
// stands by the knights while they fight, strikes them down, and sets a statue up at home and takes it back.
//   lock     the Armada's Command Lock: two Vorn Sentinels stand there as statues; the three Ciphers dropped: they wake (the door
//            stays shut, the room's bar shows), one strikes you; struck down: they turn to stone, their statues are yours, the door opens
//   gate     the Undercrown's Throne Gate: the same with the Dread Sentinels and the three Crown Shards
//   home     a Dread Sentinel's Statue: sneak + use on a block sets it up; sneak + punch takes it back
//   node t319.js [lock|gate|home]
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
    ok('...the puzzle solved: they wake ("The statues stir")', await wait(6000, async () => (await cnt(D, host)) === 2) && A.titles.some(t => /statues stir/i.test(t)), A.titles.slice(-2).join(' / '));
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
    await run(`${E}scoreboard players set ${DG} bm.pz 16`);
    await run(`${E}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz17,tag=bm.d_armada] at @s run function bm:p2/armada/pz17_reset`);
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
    if ((await sc('#uver', 'bm.p2')) !== 6) await run('function bm:admin/under/place');
    ok('the stage: the Undercrown placed (version 6: its Sentinels)', await wait(900000, async () => (await sc('#uver', 'bm.p2')) === 6, 2000));
    const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
    await run(`${N}forceload add ${UO[0] + 96} ${UO[2] + 104} ${UO[0] + 128} ${UO[2] + 136}`); await sleep(3000);
    await run(`${N}scoreboard players set ${DG} bm.pz 15`);
    await run(`${N}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz16,tag=bm.d_under] at @s run function bm:p2/under/pz16_reset`);
    const c = UW(112, 18, 126);
    await room(N, 'under', 16, 'dread', 'Dread Sentinel', UW(112, 18, 116), 'minecraft:crying_obsidian', async () => {
      for (const s of ['snow', 'witch', 'shark']) {
        const p = await pos(N, `@e[type=minecraft:marker,tag=bm.ok_${s},limit=1]`);
        await run(`loot replace entity TestRat hotbar.0 loot bm:items/ushard_${s}`); await at(N, p[0], p[1], p[2] - 0.6, 0, 70);
        A.slot(0); await sleep(200); A.drop(true); await sleep(1500);
      }
    }, [c[0] + 0.5, c[1], c[2] + 0.5]);
    await run(`${N}forceload remove ${UO[0] + 96} ${UO[2] + 104} ${UO[0] + 128} ${UO[2] + 136}`);
  }

  if (on('home')) {
    const O = 'execute in minecraft:overworld run ';
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

  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
