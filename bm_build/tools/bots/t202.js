// 2.82b: A CREW OF THREE - the tries they pick, puzzles and fights in turn, and a lost heist that doesn't open the vault - as
// regular (non-op) players TestRat, TestMouse and TestVole (rcon sets the stage: a party, Tokens for the fee, the Ledger).
//   TestRat opens the Fixer's Ledger, picks Plan a Heist, Tier V, 3 TRIES: the whole crew goes down (each pays), and the crew
//   has exactly 3 tries - not one more for each crewmate.
//   The rooms laid (that heist and three more planned the same way): puzzles and fights take turns - a puzzle, then a fight,
//   then a puzzle... (an event room can stand in for either) - so every heist is about half and half; and no Mason's Plan is
//   the retired Mosaic.
//   Lost in the vault (the stage: down to the last try, the guardian up; TestMouse knocked out): THE HEIST HAS FAILED, and
//   nobody is told the vault is open; the crew is back in the den, the leader deciding what next.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 300) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const G = 'execute in bm:gutter run ';
  const num = async (c) => { const o = await run(c); return +((o.match(/has (-?\d+)/) || o.match(/(-?\d+)\s*$/)) || [0, NaN])[1]; };
  const cnt = async (sel) => { const m = (await run(`${G}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1];
  const rel = (x, y, z) => `^${-(x - 12.5)} ^${y - 4} ^${z - 12.5}`;
  const NAMES = ['TestRat', 'TestMouse', 'TestVole'];
  const FIGHTS = ['guards', 'ambush', 'pit', 'isles'];
  const PUZZLES = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters', 'spire', 'bench', 'mason', 'dig',
                   'library', 'pipes', 'apoth', 'grapple'];
  const bots = [];
  for (const n of NAMES) { bots.push(await bot(n)); await sleep(1500); }
  const [A, M, V] = bots;
  for (const b of bots) b.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player (and so are TestMouse and TestVole)', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  for (const f of ['plan_anywhere', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never', 'rooms_any', 'variant_random']) await run(`function bm:admin/${f}`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const seen = []; let nT = 0; const tick = setInterval(() => { while (nT < A.titles.length) seen.push(A.titles[nT++]); }, 50);

  // ---- the stage: three raiders together, a party led by TestRat
  const stage = async () => {
    await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 minecraft:stone');
    for (const [i, n] of NAMES.entries()) {
      await run(`execute in minecraft:overworld run tp ${n} ${13000.5 + i} 120 13000.5`); await run(`gamemode survival ${n}`); await run(`clear ${n}`);
      await run(`effect give ${n} minecraft:resistance 900 4 true`); await run(`effect give ${n} minecraft:saturation 900 0 true`);
      await run(`tag ${n} remove bm.gvzap`); await run(`scoreboard players set ${n} bm.gvhc 0`);
      await run(`execute as ${n} unless score @s bm.pid matches 1.. run function bm:p21/pid`);
      for (let k = 0; k < 12; k++) await run(`loot give ${n} loot bm:items/token`);
      await run(`scoreboard players set ${n} bm.gvu 5`); await run(`scoreboard players set ${n} bm.gval 1`);
    }
    for (const n of NAMES) await run(`scoreboard players operation ${n} bm.pty = TestRat bm.pid`);
    await run('loot replace entity TestRat hotbar.8 loot bm:items/fixers_ledger');
    await sleep(2500);
  };
  // ---- planned by TestRat, every step a button the client was shown
  const plan = async () => {
    A.slot(8); await sleep(300); await A.useWait();
    const p1 = await A.press(/Plan a Heist/); await sleep(800);
    A.chats.length = 0; A.cmd('trigger bm.act set 7605'); await sleep(1000);                    // (Tier V)
    const tries = await wait(3000, async () => A.buttons().some(b => /3 TRIES/.test(b.label)));
    A.cmd('trigger bm.act set 7611'); await sleep(8000);                    // (3 TRIES)
    return { p1: !!p1, tries: !!tries };
  };
  const rooms = async (gi) => {
    const out = [];
    const r = await run(`${G}execute as @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvi=${gi}}] run data get entity @s`);
    for (const m of r.matchAll(/Pos: \[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\][^]*?Tags: \[([^\]]*)\]/g)) {
      const tags = m[4].replace(/"/g, '').split(', ');
      const k = (tags.find(t => /^bm\.gvr_/.test(t) && !/^bm\.gvr_(lobby|vault)$/.test(t)) || '').replace('bm.gvr_', '');
      if (k && k !== 'cache') out.push([+m[1], k]);       // (the cache is a side room off the den, not on the way)
    }
    return out.sort((a, b) => a[0] - b[0]).map(x => x[1]);
  };

  await stage();
  const p = await plan();
  const GI = await sc('TestRat', 'bm.gvi');
  const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
  const crew = await Promise.all(NAMES.map(n => sc(n, 'bm.gvi')));
  ok('TestRat: the Ledger, Plan a Heist, Tier V, 3 TRIES - the crew of three goes down together', p.p1 && p.tries && GI >= 1 && crew.every(g => g === GI), `gvi ${crew} plan ${p.p1} tries ${p.tries}`);
  ok('...and the crew has exactly the 3 tries picked (not one more for each crewmate)', (await num(`${G}scoreboard players get ${inst} bm.gvlv`)) === 3,
     `tries ${await num(`${G}scoreboard players get ${inst} bm.gvlv`)}`);

  // ---- puzzles and fights, turn about: this heist and three more like it
  const lays = [await rooms(GI)];
  const masonB = [];
  for (const q of await rooms(GI)) if (q === 'mason') masonB.push(await num(`${G}execute as @e[type=minecraft:marker,tag=bm.gvr_mason,scores={bm.gvi=${GI}},limit=1] run scoreboard players get @s bm.gvvar`));
  for (let k = 0; k < 3; k++) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    for (const n of NAMES) { await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`); }
    await stage(); await plan();
    const gi = await sc('TestRat', 'bm.gvi');
    lays.push(await rooms(gi));
    for (const q of lays[lays.length - 1]) if (q === 'mason') masonB.push(await num(`${G}execute as @e[type=minecraft:marker,tag=bm.gvr_mason,scores={bm.gvi=${gi}},limit=1] run scoreboard players get @s bm.gvvar`));
  }
  const kinds = k => FIGHTS.includes(k) ? 'F' : (PUZZLES.includes(k) ? 'P' : 'E');     // (anything else: an event or themed room)
  const strs = lays.map(L => L.map(kinds).join(''));
  const turnAbout = lays.every(L => L.length >= 5 && L.every((k, i) => kinds(k) === (i % 2 === 0 ? (kinds(k) === 'E' ? 'E' : 'P') : 'F')));
  const totP = strs.join('').split('P').length - 1, totF = strs.join('').split('F').length - 1;
  ok('four Tier V heists: puzzles and fights take turns (an event room may stand in for a puzzle, never a fight) - about half and half', turnAbout && totF >= 8 && totF >= totP - 6,
     `${strs.join(' | ')}  (P ${totP}, F ${totF}) ${lays.map(L => L.join(',')).join(' / ').slice(0, 300)}`);
  ok('...and no Mason\'s Plan was the retired Mosaic', masonB.every(v => v !== 1), `mason variants ${masonB}`);

  // ---- lost in the vault: no word of the vault opening
  const GI2 = await sc('TestRat', 'bm.gvi');
  const inst2 = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI2}},limit=1]`;
  // (TestRat presses the den's BEGIN button himself - nobody took a kit, so the ready check names them; he presses again to go anyway)
  const LB = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI2}},limit=1]`;
  await run(`execute in bm:gutter as ${LB} at @s run tp TestRat ~10 ~ ~3 -90 0`); await sleep(1500);
  const lp = (await run(`${G}data get entity ${LB} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [bx, by, bz] = [Math.floor(+lp[1]) + 11, Math.floor(+lp[2]) + 1, Math.floor(+lp[3]) + 3];
  A.chats.length = 0; A.useOn(bx, by, bz, 4); await sleep(2600);
  const named = A.chats.some(c => /Not everyone's ready/.test(c));
  A.useOn(bx, by, bz, 4);
  const begun = await wait(6000, async () => (await num(`${G}scoreboard players get ${inst2} bm.gvst`)) >= 2);
  ok('TestRat presses BEGIN: nobody has a kit, so the ready check names them; again, and the heist is on', named && begun, A.chats.slice(-3).join(' | ').slice(0, 200));
  const VM = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI2}},limit=1]`;
  for (const n of NAMES) await run(`execute in bm:gutter as ${VM} at @s run tp ${n} ${rel(6, 4, 12)} -90 0`);
  const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI2}},limit=1]`;
  const up = await wait(15000, async () => (await cnt(B)) === 1);
  await run(`${G}scoreboard players set ${inst2} bm.gvlv 1`); await sleep(500);
  seen.length = 0; A.chats.length = 0;
  await run('damage TestMouse 1000 minecraft:out_of_world');
  ok('down to the last try in the vault, the guardian up, TestMouse knocked out: THE HEIST HAS FAILED', begun && up && await wait(6000, async () => seen.some(t => /THE HEIST HAS FAILED/.test(t))),
     `begun ${begun} boss ${up} ` + seen.join(' | ').slice(0, 200));
  await sleep(6000);
  ok('...and nobody is told the vault is open', !seen.some(t => /vault is open/i.test(t)) && !A.chats.some(c => /vault is open/i.test(c)), seen.join(' | ').slice(0, 300));
  ok('...the crew is back in the den, and the leader decides what next', await wait(8000, async () => A.chats.some(c => /Back in the den/.test(c))) && (await sc('TestRat', 'bm.gvi')) === GI2,
     A.chats.slice(-2).join(' | ').slice(0, 200));

  // ---- clean up
  clearInterval(tick);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const n of NAMES) { await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`); await run(`scoreboard players reset ${n} bm.pty`);
    await run(`clear ${n}`); await run(`effect clear ${n}`); await run(`execute in minecraft:overworld run tp ${n} 13000.5 120 13000.5`); }
  for (const f of ['prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'rooms_any', 'variant_random', 'plan_safe']) await run(`function bm:admin/${f}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  for (const b of bots) b.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
