// 2.69 (II): the Dial Lock, the Three Coffers, the Signal Lamps, the Lamp Floor, the Tumbler Lock, the Bell Tower and the
// Crumbling Rafters in their B and C variants
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const allVar = async (k, v) => { const Q = await qs(k); for (const q of Q) if ((await sc(k, q, 'bm.gvvar')) !== v) return false; return Q.length > 0; };
  const btn = async (k, q, x, y, z, st) => { await at(k, q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[${st},powered=true]`); await sleep(250);
    await at(k, q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[${st},powered=false]`); await sleep(150); };
  const waitFor = async (f, ms) => { const t = Date.now(); while (Date.now() - t < ms) { if (await f()) return true; await sleep(250); } return false; };

  // ================================================================== THE DIAL LOCK
  if (want('dial')) {
    const DX = [10, 12, 14];
    const frame = i => `@e[type=minecraft:item_frame,tag=bm.gvdial${i},distance=..14,limit=1]`;
    const getR = async (q, i) => num(`execute in bm:gutter as ${room('dial', q)} at @s run data get entity ${frame(i)} ItemRotation`);
    const setR = (q, i, r) => at('dial', q, `data modify entity ${frame(i)} ItemRotation set value ${r}b`);
    await heist('dial', 'b'); await begin();
    let Q = await qs('dial'); ok('Dial Locks, all variant B (the Numbered Dials)', await allVar('dial', 1), `${Q}`);
    let q = Q[0]; await go('dial', q);
    const code = await sc('dial', q, 'bm.gvc'); const r = [code & 7, (code >> 3) & 7, (code >> 6) & 7];
    const val = { right: (r[0] + 1) % 8, middle: (r[1] + 1) % 8, left: (r[2] + 1) % 8 };
    const txt = await at('dial', q, 'data get entity @e[type=minecraft:text_display,tag=bm.gvboard,distance=..14,limit=1] text');
    const clues = (txt.match(/color: "white", text: "([^"]+)"/) || [0, ''])[1].split('\\n').filter(x => x);
    const N = ['left', 'middle', 'right'];
    const ev = (c, w) => { let m; const g = s => w[N.indexOf(s.toLowerCase())];
      if ((m = c.match(/^(\w+) \+ (\w+) = (\d+)/))) return g(m[1]) + g(m[2]) === +m[3];
      if ((m = c.match(/^(\w+) - (\w+) = (\d+)/))) return g(m[1]) - g(m[2]) === +m[3];
      if ((m = c.match(/^(\w+) is twice the (\w+)/))) return g(m[1]) === 2 * g(m[2]);
      if ((m = c.match(/^(\w+) is more than the (\w+)/))) return g(m[1]) > g(m[2]);
      if ((m = c.match(/^All three add up to (\d+)/))) return w[0] + w[1] + w[2] === +m[1];
      if ((m = c.match(/^(\w+) is (odd|even)/))) return g(m[1]) % 2 === (m[2] === 'odd' ? 1 : 0);
      return null; };
    const fits = []; for (let a = 0; a < 8; a++) for (let b = 0; b < 8; b++) for (let c = 0; c < 8; c++) if (clues.length && clues.every(cl => ev(cl, [a, b, c]))) fits.push([a, b, c].join());
    ok('...its sums (read off the wall) fit one setting - the one the lock wants', fits.length === 1 && fits[0] === [val.left, val.middle, val.right].join(), `${clues.join(' | ')} -> ${fits} want ${[val.left, val.middle, val.right]}`);
    const rings = await at('dial', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:text_display,distance=..14]');
    ok('...a ring of numbers round each dial', +(rings.match(/(\d+)/) || [0, 0])[1] >= 24, rings);
    const a0 = await alarm(); for (let i = 0; i < 3; i++) await setR(q, i, (r[i] + 1) % 8); await btn('dial', q, 16, 5, 22, 'face=wall,facing=north');
    ok('...the wrong numbers: the alarm', (await alarm()) > a0 && !(await solved('dial', q)));
    for (let i = 0; i < 3; i++) await setR(q, i, r[i]); await btn('dial', q, 16, 5, 22, 'face=wall,facing=north'); await sleep(300);
    ok('...the numbers that fit: open', await solved('dial', q));

    await heist('dial', 'c'); await begin();
    Q = await qs('dial'); ok('Variant C (the Geared Dials) when forced', await allVar('dial', 2), `${Q}`);
    q = Q[0]; await go('dial', q); await sleep(300);
    const cur = async () => [await getR(q, 0), await getR(q, 1), await getR(q, 2)];
    const click = async i => { const c = await getR(q, i); await setR(q, i, (c + 1) % 8); await sleep(150); };
    let c0 = await cur(); await click(0); let c1 = await cur();
    const d = (a, b) => b.map((x, i) => (x - a[i] + 8) % 8).join();
    ok('...turn the right dial: all three turn', d(c0, c1) === '1,1,1', d(c0, c1));
    c0 = c1; await click(1); c1 = await cur(); ok('...turn the middle: it and the left turn', d(c0, c1) === '0,1,1', d(c0, c1));
    c0 = c1; await click(2); c1 = await cur(); ok('...turn the left: it and the right turn', d(c0, c1) === '1,0,1', d(c0, c1));
    const code2 = await sc('dial', q, 'bm.gvc'); const tgt = [code2 & 7, (code2 >> 3) & 7, (code2 >> 6) & 7];
    let plan = null;
    for (let n0 = 0; n0 < 8 && !plan; n0++) for (let n1 = 0; n1 < 8 && !plan; n1++) for (let n2 = 0; n2 < 8 && !plan; n2++)
      if ((c1[0] + n0 + n2) % 8 === tgt[0] && (c1[1] + n0 + n1) % 8 === tgt[1] && (c1[2] + n0 + n1 + n2) % 8 === tgt[2]) plan = [n0, n1, n2];
    for (let i = 0; i < 3; i++) for (let k = 0; k < plan[i]; k++) await click(i);
    const fin = await cur(); await btn('dial', q, 16, 5, 22, 'face=wall,facing=north'); await sleep(300);
    ok('...work out the turns: the blueprint\'s arrows line up - open', fin.join() === tgt.join() && await solved('dial', q), `${fin} vs ${tgt} plan ${plan}`);
  }

  // ================================================================== THE THREE COFFERS
  const CZ = [6, 10, 14, 18];
  if (want('coffers')) {
    await heist('coffers', 'b'); await begin();
    let Q = await qs('coffers'); ok('Coffer rooms, all variant B (the Lying Coffers)', await allVar('coffers', 1), `${Q}`);
    let q = Q[0]; await go('coffers', q, 12, 12);
    const h = await sc('coffers', q, 'bm.gvc');
    const plac = await at('coffers', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:text_display,distance=..14]');
    ok('...each coffer says something', +(plac.match(/(\d+)/) || [0, 0])[1] >= 5, plac);
    const clickC = (k2, q2, tag) => at(k2, q2, `data modify entity @e[type=minecraft:interaction,tag=${tag},distance=..14,limit=1] interaction set value {player:[I;1,2,3,4],timestamp:1L}`);
    const a0 = await alarm(); await clickC('coffers', q, `bm.gvcof${(h + 1) % 4}`); await sleep(500);
    ok('...a liar\'s coffer: a Mimic, the alarm', (await alarm()) > a0 && (await cnt('@e[type=minecraft:rabbit,tag=bm.gvmimic]')) >= 1);
    await run('execute in bm:gutter run kill @e[type=minecraft:rabbit,tag=bm.gvmimic]');
    await clickC('coffers', q, `bm.gvcof${h}`); await sleep(500);
    ok('...the honest one: open', await solved('coffers', q));

    await heist('coffers', 'c'); await begin();
    Q = await qs('coffers'); ok('Variant C (the Shell Game) when forced', await allVar('coffers', 2), `${Q}`);
    q = Q[0]; await go('coffers', q, 12, 12); await sleep(500);
    const gold = await cnt('@e[type=minecraft:item_display,tag=bm.gvgold]');
    const start = await sc('coffers', q, 'bm.gvc');
    ok('...walk in: the gold is shown over one chest', gold === 1 && (await sc('coffers', q, 'bm.gvs')) === 1, `${gold}`);
    await sleep(2600); const a1 = await alarm();
    await clickC('coffers', q, `bm.gvshi${start}`); await sleep(300);
    const moving = (await sc('coffers', q, 'bm.gvy2')) >= 0 && (await sc('coffers', q, 'bm.gvs')) === 1;
    ok('...they shuffle; a click while they move counts for nothing', moving && (await alarm()) === a1 && !(await solved('coffers', q)));
    const ready = await waitFor(async () => (await sc('coffers', q, 'bm.gvs')) === 2, 20000);
    const hh = await sc('coffers', q, 'bm.gvc');
    let pos = 0; for (let i = 0; i < 4; i++) if (/passed/.test(await at('coffers', q, `execute positioned ${relf(19.5, 5, CZ[i] + 0.5)} if entity @e[type=minecraft:item_display,tag=bm.gvsd${i},distance=..0.2]`))) pos++;
    ok('...the shuffle ends: four chests back in their places, the gold moved with its chest', ready && pos === 4, `ready ${ready}, in place ${pos}, gold ${start} -> ${hh}`);
    await clickC('coffers', q, `bm.gvshi${(hh + 1) % 4}`); await sleep(500);
    ok('...a wrong one: a Mimic, the alarm - and they shuffle again', (await alarm()) > a1 && (await cnt('@e[type=minecraft:rabbit,tag=bm.gvmimic]')) >= 1 && (await sc('coffers', q, 'bm.gvs')) === 1);
    await run('execute in bm:gutter run kill @e[type=minecraft:rabbit,tag=bm.gvmimic]');
    await waitFor(async () => (await sc('coffers', q, 'bm.gvs')) === 2, 20000);
    await clickC('coffers', q, `bm.gvshi${await sc('coffers', q, 'bm.gvc')}`); await sleep(500);
    ok('...the one with the gold: open', await solved('coffers', q));
  }

  // ================================================================== THE SIGNAL LAMPS
  const LX = [8, 11, 14, 17];
  const DER = []; { const p = (a, k) => { if (k === 4) { if (a.every((x, i) => x !== i)) DER.push(a.slice()); return; } for (let v = 0; v < 4; v++) if (!a.includes(v)) { a.push(v); p(a, k + 1); a.pop(); } }; p([], 0); }
  if (want('lamps')) {
    for (const [v, vi] of [['b', 1], ['c', 2]]) {
      await heist('lamps', v); await begin();
      const Q = await qs('lamps'); ok(`Signal Lamps, all variant ${v.toUpperCase()}`, await allVar('lamps', vi), `${Q}`);
      const q = Q[0]; await go('lamps', q, 12, 6);
      await waitFor(async () => (await sc('lamps', q, 'bm.gvs')) === 2, 20000);
      const g = await sc('lamps', q, 'bm.gvc'), n = await sc('lamps', q, 'bm.gvx'); const seq = []; for (let i = 0; i < n; i++) seq.push(Math.floor(g / 4 ** i) % 4);
      const cip = DER[await sc('lamps', q, 'bm.gvy1')] || [0, 1, 2, 3];
      const want_ = v === 'b' ? seq.slice().reverse() : seq.map(x => cip[x]);
      const a0 = await alarm();
      const naive = seq[0] === want_[0] ? (seq[0] + 1) % 4 : seq[0];      // (pressing what you saw, in order, is wrong)
      await btn('lamps', q, LX[naive], 5, 1, 'face=wall,facing=south');
      ok(v === 'b' ? '...pressing them in the order shown: wrong - the alarm, watch again' : '...pressing the colours you saw: wrong - the alarm, watch again', (await alarm()) > a0 && (await sc('lamps', q, 'bm.gvs')) === 1);
      await waitFor(async () => (await sc('lamps', q, 'bm.gvs')) === 2, 20000);
      for (const j of want_) await btn('lamps', q, LX[j], 5, 1, 'face=wall,facing=south');
      await sleep(300);
      ok(v === 'b' ? `...the ${n} flashes backwards: open` : `...what each of the ${n} flashes means: open`, await solved('lamps', q), `${seq} -> ${want_}`);
    }
  }

  // ================================================================== THE LAMP FLOOR
  if (want('lightsout')) {
    const PAT = { b: (i, j) => { const s = [[i, j]]; for (const a of [-1, 1]) for (const c of [-1, 1]) if (i + a >= 0 && i + a < 3 && j + c >= 0 && j + c < 3) s.push([i + a, j + c]); return s; },
                  c: (i, j) => { const s = []; for (let a = 0; a < 3; a++) s.push([a, j]); for (let c = 0; c < 3; c++) if (c !== j) s.push([i, c]); return s; } };
    for (const [v, vi] of [['b', 1], ['c', 2]]) {
      await heist('lightsout', v); await begin();
      const Q = await qs('lightsout'); ok(`Lamp Floors, all variant ${v.toUpperCase()}`, await allVar('lightsout', vi), `${Q}`);
      const q = Q[0]; await go('lightsout', q, 4, 12);
      const mask = (i, j) => PAT[v](i, j).reduce((m, [a, c]) => m | (1 << (a + 3 * c)), 0);
      const s0 = await sc('lightsout', q, 'bm.gvc');
      await btn('lightsout', q, 5 + 1, 5, 11 + 1, 'face=floor,facing=east');
      const s1 = await sc('lightsout', q, 'bm.gvc');
      ok(v === 'b' ? '...the middle button flips it and the four corners' : '...the middle button flips its row and column', (s0 ^ s1) === mask(1, 1), `${(s0 ^ s1).toString(2)}`);
      let best = null; for (let b = 0; b < 512 && best === null; b++) { let st = s1; for (let k = 0; k < 9; k++) if ((b >> k) & 1) st ^= mask(k % 3, Math.floor(k / 3)); if (st === 511) best = b; }
      for (let k = 0; k < 9; k++) if ((best >> k) & 1) await btn('lightsout', q, 5 + (k % 3), 5, 11 + Math.floor(k / 3), 'face=floor,facing=east');
      await sleep(300);
      ok('...every lamp lit: open', best !== null && await solved('lightsout', q), `presses ${best}`);
    }
  }

  // ================================================================== THE TUMBLER LOCK
  if (want('tumbler')) {
    const TX = [8, 9, 10, 11, 12, 13, 14, 15, 16];
    await heist('tumbler', 'b'); await begin();
    let Q = await qs('tumbler'); ok('Tumbler Locks, all variant B (the Wandering Gate)', await allVar('tumbler', 1), `${Q}`);
    let q = Q[0]; await go('tumbler', q, 12, 6);
    const tryAt = async (p, vv) => { await run(`execute in bm:gutter run scoreboard players set ${room('tumbler', q)} bm.gvc ${p}`); await at('tumbler', q, `function bm:p111/tumbler/${vv}/try`); await sleep(100); };
    const g0 = await sc('tumbler', q, 'bm.gvy1');
    ok('...the gate is a lamp marked green (not always the middle)', g0 >= 1 && g0 <= 7 && /passed/.test(await at('tumbler', q, `execute if block ${rel(TX[g0], 6, 0)} minecraft:emerald_block`)), `gate ${g0}`);
    const a0 = await alarm(); await tryAt(g0 === 4 ? 3 : 4, 'b');
    ok('...press off the gate: missed (the alarm)', (await alarm()) > a0 && (await sc('tumbler', q, 'bm.gvw')) === 0);
    let moved = true, g = g0;
    for (let k = 0; k < 3; k++) { await tryAt(k === 1 ? 16 - g : g, 'b'); const ng = await sc('tumbler', q, 'bm.gvy1');
      if (k < 2 && (ng === g || !/passed/.test(await at('tumbler', q, `execute if block ${rel(TX[ng], 6, 0)} minecraft:emerald_block unless block ${rel(TX[g], 6, 0)} minecraft:emerald_block`)))) moved = false; g = ng; }
    ok('...on the gate (either way the light runs): a click - and the mark moves; three: open', moved && await solved('tumbler', q));

    await heist('tumbler', 'c'); await begin();
    Q = await qs('tumbler'); ok('Variant C (the Blind Tumbler) when forced', await allVar('tumbler', 2), `${Q}`);
    q = Q[0]; await go('tumbler', q, 12, 6); await sleep(8000);
    let lit = 0; for (let i = 0; i < 6; i++) { if (/passed/.test(await at('tumbler', q, `execute if block ${rel(8, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(9, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(10, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(11, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(12, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(13, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(14, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(15, 7, 0)} minecraft:redstone_lamp[lit=false] if block ${rel(16, 7, 0)} minecraft:redstone_lamp[lit=false]`))) lit++; await sleep(120); }
    ok('...after one run the light goes dark (only the ticking left)', lit === 6 && (await sc('tumbler', q, 'bm.gvy2')) === 0, `${lit}`);
    const a1 = await alarm(); await tryAt(5, 'c');
    ok('...a press off the gate: missed - and it shows itself again', (await alarm()) > a1 && (await sc('tumbler', q, 'bm.gvy2')) >= 16);
    for (let k = 0; k < 3; k++) await tryAt(k % 2 ? 12 : 4, 'c');
    ok('...three on the gate: open', await solved('tumbler', q));
  }

  // ================================================================== THE BELL TOWER
  if (want('climb')) {
    await heist('climb', 'b'); await begin();
    let Q = await qs('climb'); ok('Bell Towers, all variant B (the South Stair)', await allVar('climb', 1), `${Q}`);
    let q = Q[0]; await go('climb', q, 2, 12);
    const POSTS = [[3, 20, 4], [5, 21, 5], [7, 20, 6], [9, 21, 7], [12, 21, 7], [14, 20, 8], [16, 21, 9], [18, 20, 10], [21, 21, 10], [21, 19, 11], [21, 17, 12]];
    let posts = 0; for (const [x, z, t] of POSTS) if (/passed/.test(await at('climb', q, `execute unless block ${rel(x, t, z)} minecraft:air if block ${rel(x, t + 1, z)} minecraft:air if block ${rel(x, t + 2, z)} minecraft:air`))) posts++;
    const gone = /passed/.test(await at('climb', q, `execute if block ${rel(3, 4, 7)} minecraft:air if block ${rel(21, 12, 7)} minecraft:air`));
    let jumps = true; for (let i = 1; i < POSTS.length; i++) { const [a, b] = [POSTS[i - 1], POSTS[i]]; const dist = Math.hypot(a[0] - b[0], a[1] - b[1]); if (b[2] - a[2] > 1 || dist > 3.2) jumps = false; }
    ok('...eleven single posts, room to stand on each, every jump at most one up and three across; the old steps gone', posts === 11 && gone && jumps, `${posts} posts, old gone ${gone}`);
    await at('climb', q, `summon minecraft:item ${relf(21.5, 14.1, 12.5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(800);
    ok('...the landing\'s plate at the top: open', (await sc('climb', q, 'bm.gvs')) === 3);

    await heist('climb', 'c'); await begin();
    Q = await qs('climb'); ok('Variant C (the Falling Stair) when forced', await allVar('climb', 2), `${Q}`);
    q = Q[0]; await go('climb', q, 2, 12);
    await at('climb', q, `tp TestRat ${relf(7, 7, 21)}`); await sleep(400);
    const there = /passed/.test(await at('climb', q, `execute unless block ${rel(6, 6, 20)} minecraft:air`));
    await sleep(1500); const fell = /passed/.test(await at('climb', q, `execute if block ${rel(6, 6, 20)} minecraft:air if block ${rel(7, 6, 21)} minecraft:air`));
    await at('climb', q, `tp TestRat ${rel(2, 4, 12)}`); await sleep(4000);
    const back = /passed/.test(await at('climb', q, `execute unless block ${rel(6, 6, 20)} minecraft:air`));
    ok('...stand on a step: it gives way a moment later, and comes back', there && fell && back, `${there} ${fell} ${back}`);
    await at('climb', q, `summon minecraft:item ${relf(21.5, 14.1, 12.5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(800);
    ok('...the plate at the top: open', (await sc('climb', q, 'bm.gvs')) === 3);
  }

  // ================================================================== THE CRUMBLING RAFTERS
  if (want('rafters')) {
    await heist('rafters', 'b'); await begin();
    let Q = await qs('rafters'); ok('Rafters, all variant B (the Blinking Beams)', await allVar('rafters', 1), `${Q}`);
    let q = Q[0]; await go('rafters', q, 2, 12);
    let on = 0, off = 0; for (let i = 0; i < 16; i++) { if (/passed/.test(await at('rafters', q, `execute if block ${rel(4, 3, 12)} minecraft:air`))) off++; else on++; await sleep(200); }
    const oldGone = /passed/.test(await at('rafters', q, `execute if block ${rel(5, 3, 12)} minecraft:air if block ${rel(13, 3, 13)} minecraft:air`));
    ok('...a beam winks out and comes back; the old beams are gone', on > 0 && off > 0 && oldGone, `on ${on} off ${off}`);
    await at('rafters', q, `tp TestRat ${rel(10, 1, 12)}`); await sleep(600); const l = await local('rafters', q);
    ok('...fall into the hay: back to the start', l && l[0] < 2.5, `${l}`);
    await at('rafters', q, `tp TestRat ${rel(22, 4, 12)}`); await sleep(500);
    ok('...the far plate: through', await solved('rafters', q));

    await heist('rafters', 'c'); await begin();
    Q = await qs('rafters'); ok('Variant C (the Ghost Beams) when forced', await allVar('rafters', 2), `${Q}`);
    q = Q[0]; await go('rafters', q, 2, 12);
    const m = +((await at('rafters', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.gvrg,distance=..16]')).match(/(\d+)/) || [0, 0])[1];
    ok('...a hidden path of beams (28 or more), the old beams gone', m >= 28 && /passed/.test(await at('rafters', q, `execute if block ${rel(5, 3, 12)} minecraft:air`)), `${m}`);
    let bar = true; for (let i = 0; i < 5; i++) { const t = await at('rafters', q, `execute as @e[type=minecraft:marker,tag=bm.gvrg,distance=..16,sort=random,limit=1] at @s if block ~ ~-1 ~ minecraft:barrier`); if (!/passed/.test(t)) bar = false; }
    ok('...each one invisible (a barrier) under its marker', bar);
    await at('rafters', q, `tp TestRat ${rel(22, 4, 12)}`); await sleep(500);
    ok('...the far plate: through', await solved('rafters', q));
  }
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
