// 2.69 (I): the Combination Room, the Weighing Room, the Gauntlet and the Tile Floor in their B and C variants; the tile seam
// exploit; no flying, no wind charges; the Ranged crossbow
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, pos, local } = H;
  const ONLY = process.argv[2] || '';
  const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const B = await bot('TestMouse'); await sleep(1500);
  const press = async (k, q, x, y, z, facing) => { await at(k, q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[face=wall,facing=${facing},powered=true]`); await sleep(300);
    await at(k, q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[face=wall,facing=${facing},powered=false]`); await sleep(150); };
  const LV = [8, 10, 12, 14, 16];
  const setLevers = async (k, q, mask) => { for (let i = 0; i < 5; i++) await at(k, q, `setblock ${rel(LV[i], 5, 23)} minecraft:lever[face=wall,facing=north,powered=${(mask >> i) & 1 ? 'true' : 'false'}]`); };
  const allVar = async (k, v) => { let all = true; const Q = await qs(k); for (const q of Q) if ((await sc(k, q, 'bm.gvvar')) !== v) all = false; return all && Q.length > 0; };

  // ================================================================== the kit, and THE COMBINATION ROOM
  if (want('levers')) {
    await heist('levers', 'b');
    await run('scoreboard players set TestRat bm.ksec 1'); await run('scoreboard players set TestRat bm.gvrole 0');
    await run('execute as TestRat at @s run function bm:p72/kit/pick_3'); await sleep(300);
    const axe = /passed/.test(await run('execute if items entity TestRat container.* minecraft:iron_axe[minecraft:custom_data~{bm_kit:1b}]'));
    const xb = /passed/.test(await run('execute if items entity TestRat container.* minecraft:crossbow'));
    ok('Ranged kit with the Crossbow secondary: a battle axe instead, no crossbow', axe && !xb, `axe ${axe} crossbow ${xb}`);
    await run('execute as TestRat at @s run function bm:p72/kit/pick_2'); await sleep(300);
    const axe2 = /passed/.test(await run('execute if items entity TestRat container.* minecraft:iron_axe'));
    const xb2 = /passed/.test(await run('execute if items entity TestRat container.* minecraft:crossbow[minecraft:custom_data~{bm_kit:1b}]'));
    ok('...the Offense kit with it: the crossbow (and no axe)', xb2 && !axe2, `axe ${axe2} crossbow ${xb2}`);
    await begin();
    const Q = await qs('levers');
    ok('A heist of Combination Rooms, all variant B (the Weighed Ledger)', Q.length >= 2 && await allVar('levers', 1), `rooms ${Q}`);
    const q = Q[0]; await go('levers', q);
    const W = {}; for (const m of fnText('p110/levers/b/try').matchAll(/matches (\d) if block ~(-?\d*) ~1 ~11 minecraft:lever\[powered=true\] run scoreboard players add #sum bm\.rng (\d+)/g)) W[`${m[1]}:${+(m[2] || 0) + 12}`] = +m[3];
    const p = await sc('levers', q, 'bm.gvx'), tgt = await sc('levers', q, 'bm.gvc');
    const ws = LV.map(x => W[`${p}:${x}`]);
    const labels = await at('levers', q, `execute store result score #t bm.rng if entity @e[type=minecraft:text_display,distance=..14,y=~2,dy=0.5]`);
    let mask = 0; ws.forEach((w, i) => { if (tgt & w) mask |= 1 << i; });
    const signTxt = await at('levers', q, 'data get entity @e[type=minecraft:text_display,distance=..14,sort=furthest,limit=1] text');
    ok('...the levers carry 1, 2, 4, 8, 16 (shuffled); the ledger asks for a sum', ws.slice().sort((a, b) => a - b).join() === '1,2,4,8,16' && tgt >= 3 && tgt <= 31, `${ws} -> ${tgt}`);
    const a0 = await alarm(); await setLevers('levers', q, mask ^ 1); await press('levers', q, 12, 7, 23, 'north');
    ok('...the wrong levers: the alarm, they snap back', (await alarm()) > a0 && !(await solved('levers', q)) && /passed/.test(await at('levers', q, `execute if block ${rel(8, 5, 23)} minecraft:lever[powered=false]`)), `${a0} -> ${await alarm()}`);
    await setLevers('levers', q, mask); await press('levers', q, 12, 7, 23, 'north'); await sleep(300);
    ok('...the levers that add up to it: open', await solved('levers', q), `mask ${mask}`);

    await heist('levers', 'c'); await begin();
    const Q2 = await qs('levers');
    ok('Variant C (the Logic Ledger) every time when forced', await allVar('levers', 2), `rooms ${Q2}`);
    const q2 = Q2[0]; await go('levers', q2);
    const m2 = await sc('levers', q2, 'bm.gvc');
    const txt = await at('levers', q2, 'data get entity @e[type=minecraft:text_display,tag=bm.gvboard,distance=..14,limit=1] text');
    const clues = [...txt.matchAll(/\d\. ([^\\"]+?)(?:\\n|")/g)].map(m => m[1]);
    const RO = ['I', 'II', 'III', 'IV', 'V']; const ix = s => RO.indexOf(s);
    const bit = (p, k) => (p >> k) & 1;
    const ev = (c, p) => { let m;
      if ((m = c.match(/^Exactly (\d) levers? (?:are|is) pulled/))) return bitc(p) === +m[1];
      if ((m = c.match(/^Levers (\w+) and (\w+) are set the same way/))) return bit(p, ix(m[1])) === bit(p, ix(m[2]));
      if ((m = c.match(/^Levers (\w+) and (\w+) are set differently/))) return bit(p, ix(m[1])) !== bit(p, ix(m[2]));
      if ((m = c.match(/^Lever (\w+) or lever (\w+) is pulled/))) return !!(bit(p, ix(m[1])) | bit(p, ix(m[2])));
      if ((m = c.match(/^If lever (\w+) is pulled, so is lever (\w+)/))) return !bit(p, ix(m[1])) || !!bit(p, ix(m[2]));
      if ((m = c.match(/^Lever (\w+) is pulled/))) return !!bit(p, ix(m[1]));
      if ((m = c.match(/^Lever (\w+) is left alone/))) return !bit(p, ix(m[1]));
      if (/^No two pulled levers stand side by side/.test(c)) return ![0, 1, 2, 3].some(k => ((p >> k) & 3) === 3);
      if (/^At least two pulled levers stand side by side/.test(c)) return [0, 1, 2, 3].some(k => ((p >> k) & 3) === 3);
      const L = bitc(p & 3), Rr = bitc(p & 24);
      if (/^More are pulled left of III/.test(c)) return L > Rr; if (/^More are pulled right of III/.test(c)) return Rr > L; if (/^As many are pulled/.test(c)) return L === Rr;
      if ((m = c.match(/^At most one of levers (\w+), (\w+) and (\w+) is pulled/))) return bit(p, ix(m[1])) + bit(p, ix(m[2])) + bit(p, ix(m[3])) <= 1;
      return null; };
    const bitc = p => p.toString(2).split('').filter(x => x === '1').length;
    const pat = [0, 1, 2, 3, 4].reduce((a, i) => a | (bit(m2, i) << (4 - i)), 0);
    const fits = []; for (let pp = 0; pp < 32; pp++) if (clues.every(c => ev(c, pp))) fits.push(pp);
    ok('...its clues (read off the wall, lever I on the left) fit one setting - the one that opens it', clues.length >= 3 && clues.every(c => ev(c, pat) !== null) && fits.length === 1 && fits[0] === pat,
       `${clues.length} clues, fits ${fits}, want ${pat}: ${clues.join(' | ')}`);
    const a1 = await alarm(); await setLevers('levers', q2, m2 ^ 6); await press('levers', q2, 12, 7, 23, 'north');
    ok('...a setting that breaks a clue rings the alarm', (await alarm()) > a1 && !(await solved('levers', q2)));
    await setLevers('levers', q2, m2); await press('levers', q2, 12, 7, 23, 'north'); await sleep(300);
    ok('...the one that fits them all opens it', await solved('levers', q2));
  }

  // ================================================================== THE WEIGHING ROOM
  const PL = [[5, 5], [19, 5], [5, 19], [19, 19]];
  if (want('plates')) {
    await heist('plates', 'b'); await begin(); await H.mouse(B);
    const Q = await qs('plates'); ok('Weighing Rooms, all variant B (the Order of the Scales)', await allVar('plates', 1), `${Q}`);
    const q = Q[0]; await go('plates', q, 12, 12);
    const sym = []; for (const [x, z] of PL) sym.push(await num(`execute in bm:gutter as ${room('plates', q)} at @s positioned ${rel(x, 4, z)} run scoreboard players get @e[type=minecraft:marker,tag=bm.gvpl,distance=..0.6,limit=1] bm.gvy1`));
    const enc = await sc('plates', q, 'bm.gvy2'); const order = [0, 1, 2, 3].map(s => Math.floor(enc / 4 ** s) % 4);
    const plateOf = s => sym.indexOf(s);
    const step = async (j, who = 'TestRat') => { await at('plates', q, `tp ${who} ${rel(PL[j][0], 4, PL[j][1])}`); await sleep(300); await at('plates', q, `tp ${who} ${rel(12, 4, 12)}`); await sleep(250); };
    ok('...four scales, each a different symbol (crown, key, coin, skull)', sym.slice().sort().join() === '0,1,2,3', `${sym} order ${order}`);
    await at('plates', q, `summon minecraft:item ${rel(PL[plateOf(order[0])][0], 4, PL[plateOf(order[0])][1])} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s,Tags:["t110i"]}`); await sleep(800);
    ok('...a dropped item on a scale counts for nothing (only feet)', (await sc('plates', q, 'bm.gvw')) === 0);
    await run('execute in bm:gutter run kill @e[type=minecraft:item,tag=t110i]');
    const a0 = await alarm(); const wrong = [order[1], order[0], order[2], order[3]];
    for (let i = 0; i < 3; i++) await step(plateOf(wrong[i]));
    ok('...three steps in, the scales say nothing yet', (await sc('plates', q, 'bm.gvw')) === 3 && (await alarm()) === a0);
    await step(plateOf(wrong[3]));
    ok('...the fourth: wrong order - the alarm, and they reset', (await alarm()) > a0 && (await sc('plates', q, 'bm.gvw')) === 0 && !(await solved('plates', q)), `${a0} -> ${await alarm()}`);
    // two at once
    const a1 = await alarm();
    await at('plates', q, `tp TestRat ${rel(PL[0][0], 4, PL[0][1])}`); await at('plates', q, `tp TestMouse ${rel(PL[1][0], 4, PL[1][1])}`); await sleep(400);
    await at('plates', q, `tp TestRat ${rel(12, 4, 12)}`); await at('plates', q, `tp TestMouse ${rel(12, 4, 14)}`); await sleep(300);
    ok('...two scales stepped on at once: that\'s a wrong step too', (await alarm()) > a1 && (await sc('plates', q, 'bm.gvw')) === 0, `${a1} -> ${await alarm()}`);
    for (const s of order) await step(plateOf(s));
    await sleep(300);
    ok('...the riddle\'s order: open', await solved('plates', q), `order ${order}`);

    await heist('plates', 'c'); await begin(); await H.mouse(B);
    const Q2 = await qs('plates'); ok('Variant C (the Baton Run) when forced', await allVar('plates', 2), `${Q2}`);
    const q2 = Q2[0]; await go('plates', q2, 12, 12); await sleep(600);
    const hasBaton = async (who) => /passed/.test(await run(`execute if items entity ${who} container.* *[minecraft:custom_data~{bm_baton:1b}]`));
    ok('...walk in: the Relay Baton is handed over, a scale lights', await hasBaton('TestRat') && (await sc('plates', q2, 'bm.gvs')) === 1 && (await sc('plates', q2, 'bm.gvc')) >= 0);
    let lit = await sc('plates', q2, 'bm.gvc'); const w0 = await sc('plates', q2, 'bm.gvw');
    await at('plates', q2, `tp TestMouse ${rel(PL[lit][0], 4, PL[lit][1])}`); await sleep(500); await at('plates', q2, `tp TestMouse ${rel(12, 4, 14)}`);
    ok('...a crewmate without the baton on the lit scale: nothing', (await sc('plates', q2, 'bm.gvw')) === w0);
    const need = await sc('plates', q2, 'bm.gvy2'); let adj = true, n = 0;
    while (!(await solved('plates', q2)) && n < 12) {
      const before = await sc('plates', q2, 'bm.gvc');
      await at('plates', q2, `tp TestRat ${rel(PL[before][0], 4, PL[before][1])}`); await sleep(300); await at('plates', q2, `tp TestRat ${rel(12, 4, 12)}`); await sleep(200);
      const after = await sc('plates', q2, 'bm.gvc'); n++;
      if (!(await solved('plates', q2)) && (after === before || after + before === 3)) { adj = false; console.log('   run', n, before, '->', after, 'w', await sc('plates', q2, 'bm.gvw'), 'x', await sc('plates', q2, 'bm.gvx'), 'bat', await hasBaton('TestRat'), await hasBaton('TestMouse')); }
    }
    ok(`...the baton to ${need} lit scales in a row: open (each next one a neighbouring corner)`, await solved('plates', q2) && adj && n === need, `${n} runs, adjacent ${adj}`);
    ok('...and the baton goes back to the Fixer', !(await hasBaton('TestRat')));
    const q3 = Q2[1]; await go('plates', q3, 12, 12); await sleep(600);
    const a2 = await alarm(); await sleep(5600);
    ok('...dawdle past the light: the alarm, and the run starts over', (await alarm()) > a2 && (await sc('plates', q3, 'bm.gvw')) === 0 && (await sc('plates', q3, 'bm.gvf')) >= 1, `${a2} -> ${await alarm()}`);
    await run('clear TestRat *[minecraft:custom_data~{bm_baton:1b}]'); await sleep(1500);
    ok('...a lost baton turns up again in the crew\'s hands', await hasBaton('TestRat') || await hasBaton('TestMouse'));
  }

  // ================================================================== THE GAUNTLET
  const LZ = [5, 9, 13, 17, 21];
  if (want('lasers')) {
    await heist('lasers', 'b'); await begin();
    const Q = await qs('lasers'); ok('Gauntlets, all variant B (the Low and the High)', await allVar('lasers', 1), `${Q}`);
    const q = Q[0]; await go('lasers', q, 2, 12);
    const pat = await sc('lasers', q, 'bm.gvc'); const hi = [0, 1, 2, 3, 4].map(i => (pat >> i) & 1);
    const lo = hi.indexOf(0), hj = hi.indexOf(1);
    const zapAt = async (x, y, sneak) => { const a = await alarm(); if (sneak) { A.input({ shift: true }); await sleep(300); }
      await at('lasers', q, `tp TestRat ${relf(x + 0.5, y, 12.5)}`); await sleep(400); const z = (await alarm()) > a; const l = await local('lasers', q);
      A.input({}); await sleep(200); await at('lasers', q, `tp TestRat ${rel(2, 4, 12)}`); await sleep(1700); return [z, l]; };
    ok('...two or three violet (high) beams, the rest red (low)', hi.filter(x => x).length >= 2 && hi.filter(x => x).length <= 3, `${hi}`);
    let [z1, l1] = await zapAt(LZ[lo], 4, false);
    ok('...walk into a low beam: zap, back to the start', z1 && l1 && l1[0] < 4, `${l1}`);
    await at('lasers', q, `setblock ${rel(LZ[lo], 4, 12)} minecraft:smooth_stone_slab[type=bottom]`);
    let [z2] = await zapAt(LZ[lo], 4.5, false);
    await at('lasers', q, `setblock ${rel(LZ[lo], 4, 12)} minecraft:air`);
    ok('...over it (half a block up, as a jump carries you): no zap', !z2);
    let [z3] = await zapAt(LZ[hj], 4, false);
    ok('...stand up in a high beam: zap', z3);
    let [z4] = await zapAt(LZ[hj], 4, true);
    ok('...sneak beneath it: no zap', !z4);
    await at('lasers', q, `setblock ${rel(LZ[hj], 4, 12)} minecraft:smooth_stone_slab[type=bottom]`);
    let [z5] = await zapAt(LZ[hj], 4.5, true);
    await at('lasers', q, `setblock ${rel(LZ[hj], 4, 12)} minecraft:air`);
    ok('...a sneak-jump into it: zap', z5);
    const a3 = await alarm(); await at('lasers', q, `tp TestRat ${relf(11.5, 9.5, 12.5)}`); await sleep(500); const lf = await local('lasers', q);
    ok('...fly over the beams (higher than a jump): back to the start', lf && lf[0] < 4, `${lf}`);
    await sleep(1200); await at('lasers', q, `tp TestRat ${rel(22, 4, 12)}`); await sleep(400);
    ok('...the far plate: through', await solved('lasers', q));

    await heist('lasers', 'c'); await begin();
    const Q2 = await qs('lasers'); ok('Variant C (the Mirror Gauntlet) when forced', await allVar('lasers', 2), `${Q2}`);
    const q2 = Q2[0]; await go('lasers', q2, 2, 12); await sleep(800);
    const grid = {}, rot = [];
    for (let c = 0; c < 5; c++) for (let r = 0; r < 3; r++) {
      grid[`${c},${r}`] = await num(`execute in bm:gutter as ${room('lasers', q2)} at @s run scoreboard players get @e[type=minecraft:marker,tag=bm.gvsk${c}${r},distance=..16,limit=1] bm.gvy1`);
      if (/passed/.test(await at('lasers', q2, `execute positioned ${relf(LZ[c] + 0.5, 4, 8 + 4 * r + 0.5)} if entity @e[type=minecraft:interaction,tag=bm.gvmirc,distance=..0.3]`))) rot.push([c, r]);
    }
    const RECV = ['S0', 'S1', 'S2', 'S3', 'S4', 'N1', 'N2', 'N3', 'N4', 'E0', 'E1', 'E2'];
    const recv = RECV[await sc('lasers', q2, 'bm.gvy2')];
    const REF = { 1: { E: 'N', N: 'E', W: 'S', S: 'W' }, 2: { E: 'S', S: 'E', W: 'N', N: 'W' } }, DV = { N: [0, -1], S: [0, 1], E: [1, 0], W: [-1, 0] };
    const trace = g => { let c = 0, r = 0, d = 'S'; for (let i = 0; i < 64; i++) { const m = g[`${c},${r}`]; if (m) d = REF[m][d]; const [dc, dr] = DV[d];
      if (c + dc < 0 || c + dc > 4 || r + dr < 0 || r + dr > 2) return d === 'S' ? `S${c}` : d === 'N' ? `N${c}` : d === 'E' ? `E${r}` : `W${r}`; c += dc; r += dr; } return 'loop'; };
    const sols = []; for (let b = 0; b < 2 ** rot.length; b++) { const g = { ...grid }; rot.forEach(([c, r], i) => { g[`${c},${r}`] = 1 + ((b >> i) & 1); }); if (trace(g) === recv) sols.push(g); }
    ok(`...${rot.length} glass mirrors, steel ones fixed; exactly one setting strikes the target (${recv})`, rot.length >= 4 && sols.length === 1 && trace(grid) !== recv, `${sols.length} sols`);
    await sleep(600); ok('...not lit at the start', !(await solved('lasers', q2)));
    const flips = rot.filter(([c, r]) => sols[0] && sols[0][`${c},${r}`] !== grid[`${c},${r}`]);
    let early = false;
    for (let i = 0; i < flips.length; i++) { const [c, r] = flips[i];
      await at('lasers', q2, `execute positioned ${relf(LZ[c] + 0.5, 4, 8 + 4 * r + 0.5)} run data modify entity @e[type=minecraft:interaction,tag=bm.gvmirc,distance=..0.3,limit=1] interaction set value {player:[I;1,2,3,4],timestamp:1L}`);
      await sleep(250); if (i < flips.length - 1 && await solved('lasers', q2)) early = true; }
    await sleep(400);
    ok(`...turn the right ${flips.length} mirror(s) (right-click): the beam strikes the target - open`, await solved('lasers', q2) && !early, `early ${early}`);
    const md = await at('lasers', q2, `execute positioned ${relf(LZ[flips[0][0]] + 0.5, 4, 8 + 4 * flips[0][1] + 0.5)} run data get entity @e[type=minecraft:block_display,tag=bm.gvmird,distance=..0.3,limit=1] transformation.left_rotation`);
    ok('...a turned mirror\'s glass swings round with it', /0\.38268|-0\.38268/.test(md), md.slice(-60));
  }

  // ================================================================== THE TILE FLOOR
  const tc = (c, r) => [4 + 3 * c, 6 + 3 * r];
  if (want('tiles')) {
    // A: the seam exploit, closed
    await heist('tiles', 'a'); await begin();
    const QA = await qs('tiles'); const qa = QA[0]; await go('tiles', qa, 1, 12);
    let un = null; for (let c = 1; c < 5 && !un; c++) for (let r = 1; r < 4 && !un; r++)
      if ((await num(`execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvt${c}${r},limit=1,sort=nearest] bm.gvsafe`)) === 0) un = [c, r];
    const [ux, uz] = tc(...un);
    await at('tiles', qa, `tp TestRat ${relf(ux + 0.5 + 1.35, 4, uz + 0.5)}`); await sleep(500);
    ok('Tile Floor A: standing on the edge of a false tile (not its middle) drops it now', /passed/.test(await at('tiles', qa, `execute if block ${rel(ux, 3, uz)} minecraft:air`)), `tile ${un}`);
    await at('tiles', qa, `tp TestRat ${relf(ux + 0.5 + 1.5, 4.0, uz + 0.5 + 1.5)}`); await sleep(200);

    for (const [v, vi, nm] of [['b', 1, 'the Colour Trail'], ['c', 2, 'the Counted Floor']]) {
      await heist('tiles', v); await begin();
      const Q = await qs('tiles'); ok(`Tile Floors, all variant ${v.toUpperCase()} (${nm})`, await allVar('tiles', vi), `${Q}`);
      const q = Q[0]; await go('tiles', q, 1, 12);
      const safe = []; for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++)
        if ((await num(`execute in bm:gutter as ${room('tiles', q)} at @s run scoreboard players get @e[type=minecraft:marker,tag=bm.gvt${c}${r},distance=..14,limit=1] bm.gvsafe`)) === 1) safe.push([c, r]);
      if (v === 'b') {
        let colored = 0; for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++) { const [x, z] = tc(c, r);
          for (const col of ['red', 'blue', 'lime', 'yellow']) if (/passed/.test(await at('tiles', q, `execute if block ${rel(x, 3, z)} minecraft:${col}_concrete`))) { colored++; break; } }
        ok('...every tile wears a colour', colored === 30 || colored === -1, `${colored}`);
      } else {
        const nums = await at('tiles', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:text_display,distance=..14]');
        ok('...numbers along the edges (five rows, six columns)', (+(nums.match(/(\d+)/) || [0, 0])[1]) >= 11, nums);
      }
      ok('...the safe tiles: a path across, one tile at least in every column', [0, 1, 2, 3, 4, 5].every(c => safe.some(t => t[0] === c)), `${safe.length} safe`);
      const a0 = await alarm(); let dropped = false;
      for (const [c, r] of safe) { const [x, z] = tc(c, r); await at('tiles', q, `tp TestRat ${rel(x, 4, z)}`); await sleep(150); }
      for (const [c, r] of safe) { const [x, z] = tc(c, r); if (/passed/.test(await at('tiles', q, `execute if block ${rel(x, 3, z)} minecraft:air`))) dropped = true; }
      ok('...walk the safe tiles: none gives way, no alarm', !dropped && (await alarm()) === a0);
      await at('tiles', q, `tp TestRat ${rel(22, 4, 12)}`); await sleep(400);
      ok('...the far side: through', await solved('tiles', q));
      if (Q[1]) {
        const q2 = Q[1]; await go('tiles', q2, 1, 12);
        await at('tiles', q2, `tp TestRat ${relf(10.5, 9.2, 12.5)}`); await sleep(500); const lf = await local('tiles', q2);
        ok('...fly over the floor: back to the start', lf && lf[0] < 2.5, `${lf}`);
        await run('give TestRat minecraft:wind_charge 5'); await run('give TestRat minecraft:ender_pearl 2'); await sleep(200);
        await at('tiles', q2, `tp TestRat ${rel(1, 4, 12)}`); await sleep(500);
        const wc = await num('execute store result score #t bm.rng run clear TestRat minecraft:wind_charge 0');
        const ep = await num('execute store result score #t bm.rng run clear TestRat minecraft:ender_pearl 0');
        ok('...wind charges and pearls are held at the door', wc <= 0 && ep <= 0, `${wc} ${ep}`);
        await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(600);
        const wc2 = await num('execute store result score #t bm.rng run clear TestRat minecraft:wind_charge 0');
        const ep2 = await num('execute store result score #t bm.rng run clear TestRat minecraft:ender_pearl 0');
        ok('...and handed back once you\'re out of the room', wc2 === 5 && ep2 === 2, `${wc2} ${ep2}`);
      }
    }
  }
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})();
