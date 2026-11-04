// 3.0k: THE VORN WALK, THE HUNTER'S CRAWL, A DREAD NIGHT - as a regular (non-op) player; rcon sets the stage and reads what it sees.
//   VORN   a Trooper beamed down on a pad in the sky: it wears the jointed rig (eight parts riding it, no one-piece body); closing on
//          the player it walks / runs, its cycle advanced by the ground it covers (phase vs distance), each frame an interpolation
//          of 1-4 ticks, the targets moving a little at a time (no jumps); held still it eases into its idle; turned 90 degrees
//          at once, its body follows in steps (eased), not in one snap.
//   DREAD  a Dread Night called by the operators' command AFTER DAWN (23500: it used to set the night for a day that had just
//          ended - nothing came): it falls - the title, the bar, the player hunted - and a Stalker rises (ten parts).
//   STALKER running the player down: flat out (gait 2), its cycle by the ground, its parts at its side every sample (nothing left
//          behind), its body hugging the ground; it pauses dead (NoAI) and lunges (gait 5 then 6); its head jerks (bm.stkj).
//   DAWN   time set past 23000: the night lifts - the Stalker and its parts gone, the bar hidden, the dawn line in chat.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const count = async c => +(((await run(c)).match(/count: (\d+)/i) || [0, 0])[1]);
  const O = 'execute in minecraft:overworld run ';
  const X = 14400, Y = 121, Z = 14400;
  const pos = async sel => { const p = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return p ? p.slice(1).map(Number) : null; };
  const nums = s => (s.match(/-?[\d.]+(?=[fd]?[,\]])/g) || []).map(Number);
  const xf = async sel => { const t = await run(`${O}data get entity ${sel} transformation`);
    const g = k => { const m = t.match(new RegExp(k + ':\\s*\\[([^\\]]*)\\]')); return m ? m[1].split(',').map(v => parseFloat(v)) : null; };
    return { lr: g('left_rotation'), rr: g('right_rotation'), tr: g('translation') }; };
  const qang = (a, b) => { const d = Math.abs(a.reduce((s, v, i) => s + v * b[i], 0)); return 2 * Math.acos(Math.min(1, d)) * 180 / Math.PI; };
  const at = async (x, y, z, yaw = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} 0`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); A.stand(); };
  const heal = () => run('effect give TestRat minecraft:instant_health 1 4 true');
  const saved = { conq: await sc('TestRat', 'bm.conq'), hard: await sc('#hard', 'bm.cfg'), bmoff: await sc('#bmoff', 'bm.cfg') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat'); await run('time set 6000');
  await run(`${O}forceload add ${X - 64} ${Z - 64} ${X + 64} ${Z + 64}`);
  await run(`${O}fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y - 1} ${Z + 40} minecraft:stone`);
  await run(`${O}fill ${X - 40} ${Y} ${Z - 40} ${X + 40} ${Y + 5} ${Z + 40} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..70]`);
  await at(X + 0.5, Y, Z + 0.5);
  for (const e of ['regeneration 900 4', 'resistance 900 4', 'saturation 900 0']) await run(`effect give TestRat minecraft:${e} true`);

  // ================================================================== VORN
  const H = '@e[type=minecraft:husk,tag=bm.vrg,limit=1]';
  await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z + 18.5} run function bm:p32/spawn/trooper`);
  await sleep(400);
  const hp = await pos(H);
  const nparts = hp ? await count(`${O}execute positioned ${hp.join(' ')} if entity @e[type=minecraft:item_display,tag=bm.vrp,distance=..3]`) : 0;
  await run('scoreboard players set #t385 bm.rng 0');
  if (hp) await run(`${O}execute positioned ${hp.join(' ')} as @e[type=minecraft:item_display,tag=bm.vrp,distance=..3] on vehicle run scoreboard players add #t385 bm.rng 1`);
  const ridden = await sc('#t385', 'bm.rng');
  const old = await count(`${O}execute as ${H} on passengers if items entity @s contents *[minecraft:item_model="bm:vorn3d"]`);
  ok('A Trooper wears the jointed rig: eight parts riding it (a chain on the husk), no one-piece body', nparts === 8 && ridden === 8 && old === 0, `${nparts} parts, ${ridden} riding, ${old} old`);
  // its walk, sampled as fast as rcon goes: host position, gait, phase, the right leg's display
  const L = { 1: await sc('#gkLvrg_t_1', 'bm.rng'), 2: await sc('#gkLvrg_t_2', 'bm.rng') };
  const walk = async (host, leg, ms, Ls) => {
    const S = []; const t0 = Date.now();
    while (Date.now() - t0 < ms) {
      const p = await pos(host); const g = await sc(host, 'bm.gkg'); const ph = await sc(host, 'bm.gkp');
      const lx = leg ? await xf(leg) : null; const dur = leg ? +(((await run(`${O}data get entity ${leg} interpolation_duration`)).match(/(-?\d+)$/) || [0, NaN])[1]) : NaN;
      if (p) S.push({ t: Date.now() - t0, p, g, ph, lx, dur });
    }
    return S;
  };
  const audit = (S, Ls, label) => {
    let dist = 0, adv = 0, maxStep = 0, maxRot = 0, maxTr = 0; const gaits = new Set(), durs = new Set();
    for (let i = 1; i < S.length; i++) {
      const a = S[i - 1], b = S[i]; const d = Math.hypot(b.p[0] - a.p[0], b.p[2] - a.p[2]); maxStep = Math.max(maxStep, d);
      gaits.add(b.g); if (!isNaN(b.dur)) durs.add(b.dur);
      if (a.g >= 1 && b.g === a.g && d < 1.5) { let dp = b.ph - a.ph; if (dp < -4000) dp += 8000; if (dp > 4000) dp -= 8000; adv += dp * Ls[b.g] / 8000 / 1000; dist += d; }
      if (a.lx && b.lx && a.lx.lr && b.lx.lr) { maxRot = Math.max(maxRot, qang(a.lx.lr, b.lx.lr)); maxTr = Math.max(maxTr, Math.hypot(...b.lx.tr.map((v, k) => v - a.lx.tr[k]))); }
    }
    console.log(`  ${label}: ${S.length} samples over ${S.length ? S[S.length - 1].t : 0} ms; gaits ${[...gaits]}; durations ${[...durs]}; ground ${dist.toFixed(2)} b, ` +
                `cycle advance x L ${adv.toFixed(2)} b; largest step ${maxStep.toFixed(2)} b; leg target change <= ${maxRot.toFixed(1)} deg, ${maxTr.toFixed(3)} b between samples`);
    for (const s of S.filter((_s, i) => i % Math.max(1, Math.floor(S.length / 12)) === 0))
      console.log(`    t=${s.t}ms pos ${s.p.map(v => v.toFixed(2)).join(' ')} gait ${s.g} phase ${s.ph}` + (s.lx && s.lx.lr ? ` leg rot [${s.lx.lr.map(v => v.toFixed(3))}] tr [${s.lx.tr.map(v => v.toFixed(3))}] dur ${s.dur}` : ''));
    return { dist, adv, maxStep, maxRot, maxTr, gaits, durs };
  };
  const LEG = '@e[type=minecraft:item_display,tag=bm.vrp_legr,limit=1]';
  const W = audit(await walk(H, LEG, 5000), L, 'Vorn closing in');
  ok('Closing in it walks / runs (gait 1 or 2), the frames eased over 1-4 ticks (8 / 30: easing into its stance)', (W.gaits.has(1) || W.gaits.has(2)) &&
     [...W.durs].every(d => (d >= 1 && d <= 4) || d === 8 || d === 30) && [1, 2, 3, 4].some(d => W.durs.has(d)),
     `gaits ${[...W.gaits]}, durations ${[...W.durs]}`);
  ok('...its cycle goes with the ground it covers (feet planted: cycle advance x L = distance, within 20%)', W.dist > 2 && Math.abs(W.adv - W.dist) / W.dist < 0.2,
     `${W.adv.toFixed(2)} vs ${W.dist.toFixed(2)} blocks`);
  ok('...smoothly: no teleports, each leg target only a little from the last', W.maxStep < 1.0 && W.maxRot < 60 && W.maxTr < 0.2, `step ${W.maxStep.toFixed(2)}, ${W.maxRot.toFixed(1)} deg, ${W.maxTr.toFixed(3)} b`);
  // held still: it eases into its idle
  await run(`${O}data merge entity ${H} {NoAI:1b}`); await sleep(1500);
  const lx = await xf(LEG); const g0 = await sc(H, 'bm.gkg');
  ok('Held still it stands (gait 0), legs back under it', g0 === 0 && lx.lr && qang(lx.lr, [0, 0, 0, 1]) < 3, `gait ${g0}, leg ${lx.lr}`);
  // turned at once: the body follows in steps
  const yaw0 = +(((await run(`${O}data get entity ${H} Rotation[0]`)).match(/(-?[\d.]+)f?$/) || [0, 0])[1]);
  await run(`${O}execute as ${H} at @s run tp @s ~ ~ ~ ${(yaw0 + 90).toFixed(1)} 0`);
  const yaws = [];
  for (let i = 0; i < 8; i++) { yaws.push(+(((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.vrp_torso,limit=1] Rotation[0]`)).match(/(-?[\d.]+)f?$/) || [0, NaN])[1])); await sleep(40); }
  const dy = yaws.map(y => (((y - yaw0) % 360) + 540) % 360 - 180);
  ok('Turned 90 degrees at once, its body eases round (in between on the way, then there)', dy.some(v => v > 5 && v < 85) && Math.abs(dy[dy.length - 1] - 90) < 12,
     `body yaw - start: ${dy.map(v => v.toFixed(0)).join(', ')}`);
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.vrg]`); await sleep(1500);
  ok('...and its rig goes with it', (await count(`${O}execute if entity @e[type=minecraft:item_display,tag=bm.vrp]`)) === 0);

  // ================================================================== A DREAD NIGHT, called after dawn
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set #hard bm.cfg 1'); await run('scoreboard players set #bmoff bm.cfg 1');
  await run('scoreboard players set #bday bm.bm 0'); await run('scoreboard players set #dfell bm.cfg 0');
  await run('scoreboard players set TestRat bm.dnst -1000');
  await run('time set 23500'); await sleep(2500);
  A.titles.length = 0; A.chats.length = 0;
  await run('execute as TestRat at TestRat run function bm:admin/dread_night');
  const fell = await wait(5000, async () => (await sc('#dnight', 'bm.bm')) === 1);
  ok('Called after dawn (23500), the Dread Night still falls', fell, `#dnight ${await sc('#dnight', 'bm.bm')}, #dnday ${await sc('#dnday', 'bm.bm')}, #day ${await sc('#day', 'bm.bm')}`);
  await wait(3000, async () => passes('execute if entity @a[name=TestRat,tag=bm.dnh]'));
  ok('...the title, the bar - and the player hunted', A.titles.some(t => /DREAD NIGHT/.test(t)) && /currently visible/.test(await run('bossbar get bm:dreadnight visible')) &&
     await passes('execute if entity @a[name=TestRat,tag=bm.dnh]'), `titles ${A.titles.slice(0, 2).join(' | ')}`);

  // ================================================================== THE STALKER
  const STK = '@e[type=minecraft:zombie,tag=bm.stalker,limit=1]';
  await run('scoreboard players set TestRat bm.dnst -1000'); await run('scoreboard players set TestRat bm.dnsp 1');
  const rose = await wait(6000, async () => passes(`${O}execute if entity ${STK}`)); await sleep(300);
  ok('A Stalker rises - its ten parts with it', rose && (await count(`${O}execute if entity @e[type=minecraft:item_display,tag=bm.stkpart]`)) === 10);
  await run(`${O}scoreboard players set ${STK} bm.stkl 99`);              // (no pause yet: first, its run)
  const Ls = { 1: await sc('#gkLp181_stk_gk_1', 'bm.rng'), 2: await sc('#gkLp181_stk_gk_2', 'bm.rng') };
  const BODY = '@e[type=minecraft:item_display,tag=bm.stkp_body,limit=1]';
  const S = []; const t0 = Date.now(); let left = 0, low = [];
  while (Date.now() - t0 < 5000) {
    await run('scoreboard players set TestRat bm.dnst -1000'); await heal();
    const p = await pos(STK); const b = await pos(BODY); const g = await sc(STK, 'bm.stka'); const ph = await sc(STK, 'bm.gkp');
    if (!p) break;
    if (b) { left = Math.max(left, Math.hypot(b[0] - p[0], b[2] - p[2])); if (g === 2 && low.length < 40) { const bx = await xf(BODY); if (bx.tr) low.push(b[1] + bx.tr[1] - p[1]); } }
    S.push({ t: Date.now() - t0, p, g, ph, lx: null, dur: NaN });
    const q = A.pos; if (q && Math.hypot(q.x - p[0], q.z - p[2]) < 6) await at(X + 0.5, Y, (q.z > Z ? Z - 30 : Z + 30) + 0.5);   // (keep it running)
  }
  const T = audit(S, Ls, 'Stalker running you down');
  ok('Running you down it goes flat out (gait 2), its cycle with the ground (within 20%)', T.gaits.has(2) && T.dist > 3 && Math.abs(T.adv - T.dist) / T.dist < 0.2,
     `gaits ${[...T.gaits]}, ${T.adv.toFixed(2)} vs ${T.dist.toFixed(2)} blocks`);
  ok('...its parts always at its side (none left behind), its body low to the ground', left < 2.6 && low.length > 0 && Math.max(...low) < 1.7,
     `farthest part ${left.toFixed(2)}, body height ${low.length ? Math.min(...low).toFixed(2) + '..' + Math.max(...low).toFixed(2) : '-'}`);
  // the pause, then the lunge: held at 6-9 blocks, its cooldown spent
  await run(`${O}scoreboard players set ${STK} bm.stkl 0`);
  const seen = new Set(); let jerk = false, noai = false; const t1 = Date.now();
  while (Date.now() - t1 < 14000 && !(seen.has(5) && seen.has(6))) {
    await run('scoreboard players set TestRat bm.dnst -1000'); await heal(); await run(`${O}scoreboard players set ${STK} bm.dnsp 20`);
    const p = await pos(STK); if (!p) break; const g = await sc(STK, 'bm.stka'); seen.add(g);
    if (g === 5 && /1b/.test(await run(`${O}data get entity ${STK} NoAI`))) noai = true;
    if ((await sc(STK, 'bm.stkj')) >= 1) jerk = true;
    const q = A.pos; const d = q ? Math.hypot(q.x - p[0], q.z - p[2]) : 99;
    if (g <= 2 && (d < 6 || d > 10)) { const dir = q.z > p[2] ? 1 : -1; await run(`${O}tp TestRat ${p[0].toFixed(2)} ${Y} ${(p[2] + dir * 8).toFixed(2)}`); }
    if (g <= 2) await run(`${O}scoreboard players set ${STK} bm.stkl 0`);
  }
  await sleep(800);
  ok('Closing in it stops dead (rigid, gait 5) - then lunges (gait 6) - and goes on', seen.has(5) && noai && seen.has(6) && !/1b/.test(await run(`${O}data get entity ${STK} NoAI`)),
     `gaits seen ${[...seen].join(',')}`);
  ok('...its head jerks to one side now and then', jerk);
  await heal();

  // ================================================================== DAWN
  A.chats.length = 0;
  await run('time set 23100');
  const dawn = await wait(5000, async () => (await sc('#dnight', 'bm.bm')) === 0);
  await sleep(500);
  ok('Dawn: the night lifts - the Stalker and its parts gone, the bar hidden', dawn && !(await passes(`${O}execute if entity @e[tag=bm.stalker]`)) &&
     !(await passes(`${O}execute if entity @e[tag=bm.stkpart]`)) && /currently hidden/.test(await run('bossbar get bm:dreadnight visible')) &&
     A.chats.some(c => /Dawn\. The Dread Night lifts/.test(c)), A.chats.slice(-2).join(' | '));

  // ---- put things back
  await run(`${O}fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y + 5} ${Z + 40} minecraft:air`);
  await run(`scoreboard players set TestRat bm.conq ${isNaN(saved.conq) ? 6 : saved.conq}`); await run(`scoreboard players set #hard bm.cfg ${isNaN(saved.hard) ? 0 : saved.hard}`);
  await run(`scoreboard players set #bmoff bm.cfg ${isNaN(saved.bmoff) ? 0 : saved.bmoff}`); await run('scoreboard players set #dnday bm.bm -1');
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true'); await run('gamemode creative TestRat');
  await run('time set 6000');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
