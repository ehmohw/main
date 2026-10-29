// 2.99a: NO WAY IN BUT THE DOOR (phase251) as a regular (non-op) player. rcon sets the stage (hard mode, the dungeons placed, the
// Summons / the tokens / the Coordinates given, a trial's progress, a trial solved as its controller would); the bot plays.
//   under    the Undercrown: teleported in without the Summons - carried out to the Maw's cave, told why; the Summons and the tokens
//            at the seam: the Maw opens and it knows you (admitted), inside you stay; trial 2 the last solved, standing past gate 3: sent
//            back to where you last stood; trial 3 solved: you may stay; the Throne Gate's knights not yet fallen (progress 16): past it,
//            sent back; fallen (pz16_open): you stay; a thrown pearl is drunk by the floor; 6 s out of the box: admission gone
//   armada   the Vorn Armada: teleported onto the Dock with no beam - beamed out; the Coordinates used in the End: the tractor beam
//            sets you down, admitted, you stay; trial 2 the last solved, standing past gate 3: sent back; trial 3 solved: you stay; the
//            Command Lock's sentinels not yet fallen (progress 17): past it, sent back; fallen: you stay; the pad home: admission gone
//   node t322.js [under|armada]
// (the cells are phase251's own: `python3 phase251.py` prints a standing cell of each stage, 2 inside its boxes)
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const UO = [2560, 6, -2560], AO = [2560, 24, -3328];          // (p2/undercfg.ORIGIN, p2/armadacfg.ORIGIN)
const N = 'execute in minecraft:the_nether run ', E = 'execute in minecraft:the_end run ';
const CELL = { under: { 0: [2632, 84, -2417], 2: [2584, 84, -2441], 3: [2584, 84, -2464], 16: [2669, 19, -2470] },
               armada: { 0: [2661, 74, -3124], 2: [2755, 70, -3149], 3: [2738, 70, -3154], 17: [2566, 79, -3171] } };

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat ${iid.includes(':') ? iid : `*[minecraft:custom_data~{bm:"${iid}"}]`} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const pos = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const near = (p, r = 1.5) => A.pos && Math.abs(A.pos.x - p[0]) < r && Math.abs(A.pos.z - p[2]) < r && Math.abs(A.pos.y - p[1]) < 3;
  const at = async (D, p) => { await run(`${D}tp TestRat ${p[0] + 0.5} ${p[1]} ${p[2] + 0.5}`); await wait(4000, async () => near([p[0] + 0.5, p[1], p[2] + 0.5], 0.3), 100); await sleep(300); };
  const where = () => A.pos ? `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}` : '?';
  // (stays: 4 s where it was put, nothing said)
  const stays = async (p) => { A.bars.length = 0; await sleep(4000); return near([p[0] + 0.5, p[1], p[2] + 0.5]) && !A.bars.some(b => /Back you go|carried out/.test(b)); };
  // (sent back: away from p within 3 s, to where it stood, told)
  //  (the bars are cleared by the caller BEFORE the teleport: sent back within a tick, the bot never sees itself there, at() waits
  //   its 4 s out, and the "will not be skipped" line came - and was wiped - in that wait)
  const sentBack = async (p, home) => {
    return await wait(3500, async () => near([home[0] + 0.5, home[1], home[2] + 0.5])) && A.bars.some(b => /will not be skipped/.test(b)) && !near([p[0] + 0.5, p[1], p[2] + 0.5]); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat remove bm.lkpass');            // (the older tests' pass: this one plays without it)
  await run('gamemode survival TestRat'); await run('scoreboard players set #hard bm.cfg 1'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('effect give TestRat minecraft:saturation infinite 0 true');

  // ---- the stages each dungeon's checks run on: its progress, and a guarded trial's knights
  const stage = async (D, d, upto) => {         // (as solving trial `upto` would leave it: progress, and the next trial re-armed)
    await run(`${D}scoreboard players set @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_${d},limit=1] bm.pz ${upto}`);
    await run(`${D}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz${upto + 1},tag=bm.d_${d}] at @s run function bm:p2/${d}/pz${upto + 1}_reset`);
    await sleep(1500);
  };
  const solve = async (D, d, n) => run(`${D}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz${n},tag=bm.d_${d},limit=1] at @s run function bm:p2/${d}/pz${n}_solve`);
  const play = async (D, d, C, guard) => {
    // (arrive, and let a dungeon left alone reset, before setting any stage; on the ground there, it's where you last stood)
    await at(D, C[0]); await sleep(3500);
    await stage(D, d, 2);
    A.bars.length = 0; await at(D, C[3]);
    ok(`trial 2 the last solved, standing past gate 3: sent back to where you last stood`, await sentBack(C[3], C[0]), where() + ' | ' + A.bars.slice(-2).join(' / ').slice(0, 160));
    await sleep(1500);
    await solve(D, d, 3); await sleep(1500);
    await at(D, C[3]);
    ok('...trial 3 solved: there you may stay', await stays(C[3]), where());
    await at(D, C[0]); await sleep(2500);
    await stage(D, d, guard - 1);
    await run(`${D}scoreboard players set @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_${d},limit=1] bm.pz ${guard}`); await sleep(1500);   // (its puzzle solved, its knights awake)
    A.bars.length = 0; await at(D, C[guard]);
    ok(`trial ${guard} solved but its knights still standing: past their door, sent back`, await sentBack(C[guard], C[0]), where());
    await sleep(1500);
    await run(`${D}execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz${guard},tag=bm.d_${d},limit=1] at @s run function bm:p2/${d}/pz${guard}_open`); await sleep(1500);   // (they fell: phase245 opens it)
    await at(D, C[guard]);
    ok('...the knights fallen and the door open: you stay', await stays(C[guard]), where());
    await at(D, C[0]); await sleep(1500);
    await run(`${D}execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_${d},limit=1] at @s run function bm:p2/${d}/reset`); await sleep(500);
  };

  if (on('under')) {
    const C = CELL.under;
    await run(`${N}tp TestRat ${UO[0] - 40} 100 ${UO[2] - 40}`); await run(`${N}setblock ${UO[0] - 40} 98 ${UO[2] - 40} minecraft:obsidian`);
    if ((await sc('#uver', 'bm.p2')) !== 6) await run('function bm:admin/under/place');
    ok('the stage: the Undercrown placed', await wait(900000, async () => (await sc('#uver', 'bm.p2')) === 6, 2000));
    await run(`${N}forceload add ${UO[0]} ${UO[2]} ${UO[0] + 223} ${UO[2] + 223}`); await sleep(4000);
    const outer = await pos(N, '@e[type=minecraft:marker,tag=bm.uouter,limit=1]');
    const gate = await pos(N, '@e[type=minecraft:marker,tag=bm.ugate,limit=1]');
    // (no Summons, no admission)
    await run('tag TestRat remove bm.usum'); for (const k of ['snow', 'witch', 'shark']) await run(`scoreboard players reset TestRat bm.dbwin_${k}`);
    await run('scoreboard players reset TestRat bm.lku'); A.chats.length = 0; A.bars.length = 0;
    await at(N, C[0]);
    ok('teleported in without the Summons: carried out to the Maw\'s cave', await wait(4000, async () => outer && near(outer, 2)), where());
    ok('...and told why ("does not know you", "no way in but its own")', A.bars.some(b => /does not know you/.test(b)) && A.chats.some(c => /no way in but its own/.test(c)),
       [...A.bars, ...A.chats].slice(-2).join(' | ').slice(0, 200));
    // (the Summons and the three tokens, at the seam)
    await run('tag TestRat add bm.usum'); for (const t of ['tok_frost', 'tok_hex', 'tok_saw']) await run(`loot give TestRat loot bm:items/${t}`);
    await at(N, [Math.floor(gate[0] + 1.5), Math.floor(gate[1]), Math.floor(gate[2])]);
    ok('the Summons and the tokens at the seam: the Maw opens, and knows you (admitted)', await wait(5000, async () => (await sc('TestRat', 'bm.lku')) === (await sc('#urun', 'bm.p2'))),
       `${await sc('TestRat', 'bm.lku')} / ${await sc('#urun', 'bm.p2')}`);
    await at(N, C[0]);
    ok('...inside, you stay', await stays(C[0]), where());
    await play(N, 'under', C, 16);
    // (a pearl thrown inside: the floor drinks it, and gives it back)
    await run('clear TestRat minecraft:ender_pearl'); await run('item replace entity TestRat hotbar.0 with minecraft:ender_pearl 1'); A.slot(0); await sleep(300);
    A.use(); await sleep(200); A.release();
    ok('a pearl thrown inside: the floor drinks it (it comes back, you don\'t go)', await wait(4000, async () => (await has('minecraft:ender_pearl')) === 1) && near([C[0][0] + 0.5, C[0][1], C[0][2] + 0.5], 3), where());
    // (out of the box: 5 s, and it's gone)
    await run(`${N}tp TestRat ${UO[0] + 250} ${UO[1] + 72} ${UO[2] + 194}`); await sleep(7000);
    ok('6 s out on the road, out of its box: admission gone', (await sc('TestRat', 'bm.lku')) === -99, String(await sc('TestRat', 'bm.lku')));
    await run(`${N}forceload remove ${UO[0]} ${UO[2]} ${UO[0] + 223} ${UO[2] + 223}`);
  }

  if (on('armada')) {
    const C = CELL.armada;
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`); await sleep(1000);
    if ((await sc('#aver', 'bm.p2')) < 5) await run('function bm:admin/armada/place');
    ok('the stage: the Armada placed', await wait(900000, async () => (await sc('#aver', 'bm.p2')) >= 5, 2000));
    await run(`${E}forceload add ${AO[0]} ${AO[2]} ${AO[0] + 239} ${AO[2] + 239}`); await sleep(4000);
    await run('clear TestRat'); await run('tag TestRat remove bm.acoord'); await run('scoreboard players reset TestRat bm.lka'); await run('scoreboard players reset TestRat bm.aoy');
    A.chats.length = 0; A.bars.length = 0;
    await at(E, C[0]);
    ok('teleported onto the Dock with no beam: beamed out (the End\'s island)', await wait(4000, async () => A.pos && Math.abs(A.pos.x - 100.5) < 3 && Math.abs(A.pos.z - 0.5) < 3), where());
    ok('...and told why', A.bars.some(b => /does not know you/.test(b)) && A.chats.some(c => /no way in but its own/.test(c)), [...A.bars, ...A.chats].slice(-2).join(' | ').slice(0, 200));
    // (the Coordinates used in the End, past the island: the beam)
    await run(`${E}tp TestRat 1200 90 0`); await sleep(1500);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/hive_coords'); await sleep(400);
    A.slot(0); await sleep(300); A.use(); await sleep(2200); A.release();
    const dock = [AO[0] + 111, AO[1] + 50, AO[2] + 206];
    ok('the Coordinates used: the tractor beam sets you down on the Dock', await wait(14000, async () => near(dock, 3), 500), where());
    ok('...admitted', (await sc('TestRat', 'bm.lka')) === (await sc('#arun', 'bm.p2')), `${await sc('TestRat', 'bm.lka')} / ${await sc('#arun', 'bm.p2')}`);
    ok('...aboard, you stay', await stays([Math.floor(A.pos.x), Math.floor(A.pos.y), Math.floor(A.pos.z)]), where());
    await play(E, 'armada', C, 17);
    // (the pad home: out, and admission gone at once)
    const home = [AO[0] + 103, AO[1] + 50, AO[2] + 206];
    await at(E, home);
    ok('the Dock\'s pad home: beamed out, admission gone', await wait(4000, async () => near([1200.5, 90, 0.5], 3) && (await sc('TestRat', 'bm.lka')) === -99), where());
    await run(`${E}forceload remove ${AO[0]} ${AO[2]} ${AO[0] + 239} ${AO[2] + 239}`);
  }

  await run('tag TestRat remove bm.usum');      // (the Summons this test gave: left on, it hands the Lightbringer's herald over unasked - t309)
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
