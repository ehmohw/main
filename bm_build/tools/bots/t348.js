// 3.0g: FOUR VAULT HALLS AND THE HARD-MODE GUARDIANS - as a regular player (rcon sets the stage: the plan, the hall forced, the
// guardian's health set low where a test would take minutes, a sword handed over).
//  pylons   THE PYLON HALL: the guardian shells; four soul pylons rise; TestRat smashes each with three blows; the shell cracks.
//  crumble  THE CRUMBLING HALL: the floor cracks under TestRat and gives way - he's thrown back to the hall's door; the floor mends;
//           the shelled guardian over a crack when it falls: its shell breaks.
//  blade    THE TURNING BLADE: standing in its path, TestRat is cut; holding the hub while it passes through the shelled guardian
//           cracks the shell.
//  hard     hard mode, a hard-mode guardian forced - a Dread Mire, a Statue Knight, a Brood-Mire, each from its own summon: it
//           guards the vault with the guardian's bar; TestRat's blows bring it down; the pot is paid and the vault opens.
// Each hall: the sign at the door and the crew's word say which it is.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
const want = (k) => !process.argv[2] || process.argv[2].split(',').includes(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  ok('TestRat is a regular player (no operator commands)', await new Promise(r => { const n0 = A.chats.length; A.cmd('gamemode creative');
    setTimeout(() => r(A.chats.slice(n0).some(c => /unknown or incomplete|Unknown command/i.test(c))), 1200); }));
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  await run('function bm:admin/heist_boss_std');
  const G = 'execute in bm:gutter run ';
  const eidOf = async (sel, pre = G) => { const m = (await run(`${pre}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  let GI, V, B, atV;
  const into = async (tier = 1) => {
    await heist('levers', 'a', tier); await begin();
    GI = await num('scoreboard players get TestRat bm.gvi');
    V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
    B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
    atV = (cmd) => run(`execute in bm:gutter as ${V} at @s run ${cmd}`);
    A.chats.length = 0;
    await atV(`tp TestRat ${rel(6, 4, 12)} -90 0`);
  };
  const vgs = () => num(`${G}scoreboard players get ${V} bm.gvs`);
  const shell = async () => { const mx = await num(`${G}attribute ${B} minecraft:max_health get`); await run(`${G}data merge entity ${B} {Health:${Math.max(2, Math.floor(mx * 0.4))}f}`);
    return wait(3000, async () => /bm\.gvshell/.test(await run(`${G}data get entity ${B} Tags`))); };
  const shelled = async () => /bm\.gvshell/.test(await run(`${G}data get entity ${B} Tags`));
  const freeB = () => wait(7000, async () => (await cnt(B)) === 1 && !/bm\.cfrz/.test(await run(`${G}data get entity ${B} Tags`)));
  const signSays = async (re) => re.test(await run('execute at TestRat run data get entity @e[type=minecraft:text_display,tag=bm.h3gsign,limit=1,sort=nearest] text'));
  const leave = async () => { await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500); };

  if (want('pylons')) {
    await run('function bm:admin/heist_hall_1'); await run('function bm:admin/heist_hard_never'); await into(1);
    ok('THE PYLON HALL: the sign at the door says so', await signSays(/PYLON HALL/));
    ok('...and so does the word to the crew when the guardian wakes', await wait(5000, async () => A.chats.some(c => /PYLON HALL/.test(c))));
    await freeB();
    ok('The guardian shells: four soul pylons rise', await shell() && await wait(1500, async () => (await cnt('@e[type=minecraft:interaction,tag=bm.h3gpy,distance=0..]')) === 4));
    await run(`${G}data merge entity ${B} {NoAI:1b}`);                           // (held still while the bot goes round)
    for (const [x, z] of [[6, 6], [18, 6], [6, 18], [18, 18]]) {
      await atV(`tp TestRat ${rel(x - 1.5, 4, z)} -90 0`); await sleep(600);
      const id = await (async () => { for (let i = 0; i < 10; i++) { const e = await eidOf('@e[type=minecraft:interaction,tag=bm.h3gpy,sort=nearest,limit=1]', 'execute in bm:gutter at TestRat run '); if (e) return e; await sleep(200); } return null; })();
      for (let i = 0; i < 3 && id; i++) { A.attack(id); await sleep(350); }
    }
    ok('...three blows each from TestRat: every pylon shattered', await wait(2000, async () => (await cnt('@e[type=minecraft:interaction,tag=bm.h3gpy,distance=0..]')) === 0));
    ok('...and the shell cracks', await wait(3000, async () => !(await shelled())));
    await run(`${G}data merge entity ${B} {NoAI:0b}`);
    await run(`${G}kill ${B}`);
    ok('Its fall opens the vault, as ever', await wait(8000, async () => (await vgs()) === 2));
    await leave();
  }

  if (want('crumble')) {
    await run('function bm:admin/heist_hall_2'); await run('function bm:admin/heist_hard_never'); await into(1);
    ok('THE CRUMBLING HALL: the sign at the door says so', await signSays(/CRUMBLING HALL/));
    await freeB(); await run(`${G}data merge entity ${B} {NoAI:1b}`); await atV(`tp ${B} ${rel(20, 4, 20)}`);
    await run('effect clear TestRat'); await run('effect give TestRat instant_health 1 4');
    await atV(`tp TestRat ${rel(8, 4, 8)} -90 0`); await sleep(400);
    const CR = '@e[type=minecraft:marker,tag=bm.h3gcr,distance=0..]';
    ok('The floor cracks under TestRat', await wait(4000, async () => (await cnt(CR)) >= 1));
    const vp = (await run(`${G}data get entity ${V} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    ok('...gives way: he\'s thrown back to the hall\'s door', await wait(4000, async () => { const p = A.pos; return p && Math.abs(p.x - (vp[0] - 10)) < 1.2 && Math.abs(p.z - vp[2]) < 1.2; }),
       `at ${A.pos && [A.pos.x.toFixed(1), A.pos.z.toFixed(1)]}`);
    ok('...the hole is there', /passed/i.test(await atV(`execute if block ${rel(8, 3, 8)} minecraft:air`)));
    ok('...and mends 8 s later', await wait(11000, async () => !/passed/i.test(await atV(`execute if block ${rel(8, 3, 8)} minecraft:air`))));
    // the shelled guardian over a crack when it falls
    await run('effect give TestRat resistance 900 4 true');
    ok('The guardian shells', await shell());
    await atV(`tp TestRat ${rel(8, 4, 16)} -90 0`);
    const fresh = '@e[type=minecraft:marker,tag=bm.h3gcr,scores={bm.h3gt=..24},distance=0..,limit=1]';
    ok('...a new crack under TestRat', await wait(5000, async () => (await cnt(fresh)) === 1));
    await run(`${G}execute at ${fresh} run tp ${B} ~ ~ ~`);                       // (lured over it)
    ok('...the floor falls away under the shelled guardian: its shell breaks', await wait(4000, async () => !(await shelled())));
    await run(`${G}data merge entity ${B} {NoAI:0b}`); await run(`${G}kill ${B}`);
    ok('Its fall opens the vault - and every crack is mended', await wait(9000, async () => (await vgs()) === 2) && await wait(3000, async () => (await cnt(CR)) === 0));
    await leave();
  }

  if (want('blade')) {
    await run('function bm:admin/heist_hall_3'); await run('function bm:admin/heist_hard_never'); await into(1);
    ok('THE TURNING BLADE: the sign at the door says so', await signSays(/TURNING BLADE/));
    await freeB(); await run(`${G}data merge entity ${B} {NoAI:1b}`); await atV(`tp ${B} ${rel(12, 4, 20)}`);
    await run('effect clear TestRat'); await run('effect give TestRat instant_health 1 4'); await sleep(300);
    A.bars.length = 0; await atV(`tp TestRat ${rel(17, 4, 12)} -90 0`);
    ok('Standing in the blade\'s path: TestRat is cut', await wait(8000, async () => A.bars.some(b => /The blade/.test(b))));
    await run('effect give TestRat resistance 900 4 true');
    ok('The guardian shells', await shell());
    await atV(`tp TestRat ~ ~ ~`); await atV(`tp ${B} ${rel(16, 4, 12)}`);
    ok('Holding the hub while the blade cuts it: the shell cracks', await wait(8000, async () => !(await shelled())));
    await run(`${G}data merge entity ${B} {NoAI:0b}`); await run(`${G}kill ${B}`);
    ok('Its fall opens the vault (and the blade stops)', await wait(8000, async () => (await vgs()) === 2) && await wait(2000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.h3gbl,distance=0..]')) === 0));
    await leave();
  }

  if (want('hard')) {
    const hard0 = await num('scoreboard players get #hard bm.cfg');
    await run('scoreboard players set #hard bm.cfg 1'); await run('function bm:admin/heist_hard_always'); await run('function bm:admin/heist_hall_0');
    for (const [k, sel, down] of [['mire', '@e[type=minecraft:husk,tag=bm.mire,tag=bm.h3gb,distance=0..,limit=1]', 'bm.ms'],
                                  ['knight', '@e[type=minecraft:husk,tag=bm.khost,tag=bm.h3gb,distance=0..,limit=1]', 'bm.ks'],
                                  ['brood', '@e[type=minecraft:husk,tag=bm.bmire,tag=bm.h3gb,distance=0..,limit=1]', 'bm.ms']]) {
      await run(`function bm:admin/heist_hard_${k}`); await into(2);
      ok(`Hard mode (${k}): its own guardian comes for the vault`, await wait(5000, async () => (await cnt(sel)) === 1), `${await cnt(sel)}`);
      ok('...no vault guardian beside it', (await cnt(B)) === 0);
      const awake = () => wait(12000, async () => (await num(`${G}scoreboard players get ${sel} ${down}`)) >= (k === 'knight' ? 1 : 2));
      ok('...it wakes for the crew (rises / stirs from stone)', await awake(), `${down} ${await num(`${G}scoreboard players get ${sel} ${down}`)}`);
      const pot0 = await num(`${G}scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1] bm.gvpot`);
      await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword'); A.slot(0);
      await run(`${G}data merge entity ${sel} {Health:104f}`);
      await run(`${G}execute at ${sel} run tp TestRat ^ ^ ^2.5 facing entity ${sel} eyes`); await sleep(500);
      const id = await (async () => { for (let i = 0; i < 10; i++) { const e = await eidOf(sel); if (e) return e; await sleep(200); } return null; })();
      let fell = false;
      for (let i = 0; i < 12 && id && !fell; i++) { A.attack(id); await sleep(700);
        fell = (await num(`${G}scoreboard players get ${sel} ${down}`)) === (k === 'knight' ? 5 : 7) || (await cnt(sel)) === 0; }
      ok('...TestRat\'s blows bring it down', fell);
      ok('...the pot is paid for it', await wait(3000, async () => (await num(`${G}scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1] bm.gvpot`)) > pot0));
      ok('...and the vault opens', await wait(14000, async () => (await vgs()) === 2));
      await leave();
    }
    await run(`scoreboard players set #hard bm.cfg ${Math.max(0, hard0)}`); await run('function bm:admin/heist_hard_any');
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('clear TestRat');
  await run('function bm:admin/heist_hall_any'); await run('function bm:admin/heist_boss_any');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
