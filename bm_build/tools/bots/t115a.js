// 2.72 (I): the Library, the Pipes, the Apothecary, the Grapple, the Minecart Run - three ways each
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const DATA = require('./p115.json');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local, pos } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const has = async (sel) => /passed/.test(await run(`execute if items entity TestRat container.* ${sel}`));
  const uuid = (await run('data get entity TestRat UUID')).match(/\[I; ?(-?\d+), ?(-?\d+), ?(-?\d+), ?(-?\d+)\]/).slice(1).join(',');
  const click = async (k, q, sel) => { await at(k, q, `data modify entity ${sel} interaction set value {player:[I;${uuid}],timestamp:1L}`); await sleep(250); };
  const isb = async (k, q, p, b) => /passed/.test(await at(k, q, `execute if block ${p} ${b}`));
  const fresh = async (k, v, t) => { if (k === 'minecart') { await run('function bm:admin/room_minecart'); await heist('guards', v, t); } else await heist(k, v, t); await begin(); const Q = await qs(k); return Q[0]; };

  // ================================================================== THE LIBRARY
  if (want('library')) {
    const bk = (q, s) => `@e[type=minecraft:interaction,tag=bm.gvbk,distance=..20,scores={${s}},limit=1]`;
    let q = await fresh('library', 'a', 3);
    ok('The Library (A, the Catalogue): 36 books on the wall', (await sc('library', q, 'bm.gvvar')) === 0 &&
       +((await at('library', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:interaction,tag=bm.gvbk,distance=..20]')).match(/(\d+)/) || [0, 0])[1] === 36);
    await go('library', q, 12, 10);
    const need = await sc('library', q, 'bm.gvx');
    let a0 = await alarm();
    await click('library', q, bk(q, 'bm.gvy2=1')); await click('library', q, bk(q, 'bm.gvy2=0'));
    ok('...a wrong book: the alarm, and every book slides back', (await alarm()) > a0 && (await sc('library', q, 'bm.gvw')) === 0 &&
       !/passed/.test(await at('library', q, 'execute if entity @e[type=minecraft:interaction,tag=bm.gvbkp,distance=..20]')), `need ${need}`);
    for (let r = 1; r <= need; r++) await click('library', q, bk(q, `bm.gvy2=${r}`));
    ok(`...the ${need} books on the card: open`, await solved('library', q));
    q = await fresh('library', 'b', 2); await go('library', q, 12, 10);
    const len = await sc('library', q, 'bm.gvx'); const lq = []; for (let k = 0; k < len; k++) lq.push(await sc('library', q, `bm.lq${k}`));
    a0 = await alarm();
    await click('library', q, bk(q, `bm.gvy2=${lq[1] === lq[0] ? lq[2] : lq[1]}`));
    ok('Variant B (the Acrostic): the second letter first - wrong, the alarm', (await alarm()) > a0 && (await sc('library', q, 'bm.gvw')) === 0);
    for (const L of lq) await at('library', q, `execute as @e[type=minecraft:interaction,tag=bm.gvbk,tag=!bm.gvbkp,distance=..20,scores={bm.gvy2=${L}},limit=1] run data modify entity @s interaction set value {player:[I;${uuid}],timestamp:1L}`), await sleep(250);
    ok(`...the answer (${lq.map(c => String.fromCharCode(64 + c)).join('')}) spelt in order: open`, await solved('library', q));
    q = await fresh('library', 'c', 4); await go('library', q, 12, 10);
    const tgt = await sc('library', q, 'bm.gvz');
    const books = [];
    for (let i = 0; i < 36; i++) { const v = await num(`execute in bm:gutter as ${room('library', q)} at @s run scoreboard players get ${bk(q, `bm.gvy1=${i}`)} bm.gvy2`); if (v > 0) books.push([i, v, Math.floor(i / 12)]); }
    let sol = null, bad = null;
    for (const a of books) for (const b of books) for (const c of books) if (a[0] < b[0] && b[0] < c[0]) {
      if (a[1] + b[1] + c[1] === tgt && new Set([a[2], b[2], c[2]]).size === 3) sol = sol ? 'many' : [a, b, c];
      if (!bad && a[1] + b[1] + c[1] === tgt && new Set([a[2], b[2], c[2]]).size < 3) bad = [a, b, c]; }
    ok(`Variant C (the Sum): 12 numbered books, exactly one way to make ${tgt} from three shelves`, books.length === 12 && Array.isArray(sol), JSON.stringify(sol));
    a0 = await alarm();
    const wrong3 = books.filter(b => !sol.find(s => s[0] === b[0])).slice(0, 3);
    for (const b of wrong3) await click('library', q, bk(q, `bm.gvy1=${b[0]}`));
    ok('...three that don\'t add up: the alarm, back on the shelf', !(await solved('library', q)) && (await alarm()) > a0);
    for (const b of sol) await click('library', q, bk(q, `bm.gvy1=${b[0]}`));
    ok('...the three that do: open', await solved('library', q));
  }

  // ================================================================== THE PIPES
  if (want('pipes')) {
    const cell = (r, c) => `@e[type=minecraft:marker,tag=bm.gvpcell,distance=..12,scores={bm.pr=${r},bm.pc=${c}},limit=1]`;
    const icell = (r, c) => `@e[type=minecraft:interaction,tag=bm.gvpint,distance=..12,limit=1,sort=nearest]`;
    const clickCell = async (q, r, c) => { await at('pipes', q, `execute positioned ${relf(8 + 2 * c + 0.5, 4, 8 + 2 * r + 0.5)} as @e[type=minecraft:interaction,tag=bm.gvpint,distance=..0.5,limit=1] run data modify entity @s interaction set value {player:[I;${uuid}],timestamp:1L}`); await sleep(300); };
    for (const v of ['a', 'b', 'c']) {
      const q = await fresh('pipes', v, 2); await go('pipes', q, 4, 12); await sleep(300);
      const j = await sc('pipes', q, 'bm.gvc'); const P = DATA['pipe' + v.toUpperCase()][j];
      const wet0 = +((await at('pipes', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.gvwet,distance=..12]')).match(/(\d+)/) || [0, 0])[1];
      const nd = +((await at('pipes', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:block_display,tag=bm.gvpd,distance=..12]')).match(/(\d+)/) || [0, 0])[1];
      ok(`The Pipes (${v.toUpperCase()}): 25 pieces drawn, not yet running through`, nd >= 50 && !(await solved('pipes', q)), `${nd} parts, ${wet0} wet`);
      // set every piece right but one (A, C: one turn short; B: two swapped), then click
      const keys = Object.keys(P[2]); let last = null, pair = null;
      for (const kk of keys) { const [r, c] = kk.split(',').map(Number); const [t, k] = P[2][kk];
        await at('pipes', q, `scoreboard players set ${cell(r, c)} bm.gvy1 ${t}`); await at('pipes', q, `scoreboard players set ${cell(r, c)} bm.gvy2 ${k}`); }
      if (v === 'b') {
        const a1 = keys[7], a2 = keys.find(kk => JSON.stringify(P[2][kk]) !== JSON.stringify(P[2][a1]));
        const [r1, c1] = a1.split(',').map(Number), [r2, c2] = a2.split(',').map(Number);
        await at('pipes', q, `scoreboard players set ${cell(r1, c1)} bm.gvy1 ${P[2][a2][0]}`); await at('pipes', q, `scoreboard players set ${cell(r1, c1)} bm.gvy2 ${P[2][a2][1]}`);
        await at('pipes', q, `scoreboard players set ${cell(r2, c2)} bm.gvy1 ${P[2][a1][0]}`); await at('pipes', q, `scoreboard players set ${cell(r2, c2)} bm.gvy2 ${P[2][a1][1]}`);
        await clickCell(q, r1, c1); await sleep(300); const sel = /passed/.test(await at('pipes', q, 'execute if entity @e[type=minecraft:marker,tag=bm.gvpsel,distance=..12]'));
        ok('...click a piece: picked up (nothing turns)', sel && !(await solved('pipes', q)));
        await clickCell(q, r2, c2);
        ok('...click another: they swap - the water runs through: open', await solved('pipes', q));
      } else {
        const [r, c] = [P[0], 0]; const [t, k] = P[2][`${r},${c}`];
        await at('pipes', q, `scoreboard players set ${cell(r, c)} bm.gvy2 ${(k + 3) % 4}`);
        await clickCell(q, r, c);
        const w = +((await at('pipes', q, 'execute store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.gvwet,distance=..12]')).match(/(\d+)/) || [0, 0])[1];
        ok(`...turn the last piece: the water runs through${v === 'c' ? ' both gauges' : ''} (${w} pieces blue): open`, w >= 5 && await solved('pipes', q));
      }
    }
    // C: through to OUT but missing a gauge stays shut (checked on the data: every C puzzle's path passes its gauges)
  }

  // ================================================================== THE APOTHECARY
  if (want('apoth')) {
    const hand = async q => { await at('apoth', q, `data modify entity @e[type=minecraft:interaction,tag=bm.gvhatch,distance=..14,limit=1] interaction set value {player:[I;${uuid}],timestamp:1L}`); await sleep(400); };
    for (const [v, t] of [['a', 2], ['b', 3], ['c', 4]]) {
      const q = await fresh('apoth', v, t); await go('apoth', q, 10, 12); await sleep(700);
      const rc = await sc('apoth', q, 'bm.gvc'); const j = rc % 10, tt = Math.floor(rc / 10);
      const want_ = v === 'a' ? DATA.brewA[tt][j] : v === 'b' ? ['potion', DATA.brewB[tt][j]] : DATA.brewC[tt][j];
      const stands = /passed/.test(await at('apoth', q, `execute if block ${rel(8, 5, 20)} minecraft:brewing_stand if block ${rel(16, 5, 20)} minecraft:brewing_stand`));
      ok(`The Apothecary (${v.toUpperCase()}, Tier ${t}): brewing stands, water, blaze powder and ingredients handed out`, stands && await has('minecraft:potion') && await has('minecraft:blaze_powder') && await has('minecraft:nether_wart'),
         `wants ${want_.join(' ')}`);
      const a0 = await alarm();
      await run(`item replace entity TestRat weapon.mainhand with minecraft:potion[minecraft:potion_contents={potion:"minecraft:${want_[1] === 'poison' ? 'swiftness' : 'poison'}"}]`); await hand(q);
      ok('...the wrong potion: poured out, and the alarm', !(await solved('apoth', q)) && (await alarm()) > a0);
      await run(`item replace entity TestRat weapon.mainhand with minecraft:${want_[0]}[minecraft:potion_contents={potion:"minecraft:${want_[1]}"}]`); await hand(q);
      ok(`...${want_[1]} (${want_[0]}): open`, await solved('apoth', q));
    }
  }

  // ================================================================== THE GRAPPLE
  if (want('grapple')) {
    const hook = async (k, q, x, y, z) => { await run('clear TestRat *[minecraft:custom_data~{bm_rhook:1b}]'); await run('item replace entity TestRat weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={bm:"grappling_hook",bm_room:1b,bm_rhook:1b}]');
      const mp = await H.mpos(k, q); const f = [mp[0] + x - 12.5, mp[1] + y - 4, mp[2] + z - 12.5].map(v => v.toFixed(3)).join(' ');
      await run(`execute in bm:gutter as TestRat at @s anchored eyes facing ${f} anchored feet run function bm:p21/grap/use`); await sleep(300); };
    const hanging = async () => /bm\.grappling/.test(await run('data get entity TestRat Tags'));
    const letgo = async () => { await run('execute as TestRat at @s run function bm:p21/grap/release'); await sleep(300); };
    let q = await fresh('grapple', 'a', 3);
    const j = await sc('grapple', q, 'bm.gvc') ; const [isl, h] = DATA.chasms[await sc('grapple', q, 'bm.gvc')];
    await go('grapple', q, 2, 12); await sleep(600);
    ok(`The Grapple (A, the Chasm): the Fixer's hook lent, ${h} hooks`, await has('*[minecraft:custom_data~{bm_rhook:1b}]') && (await num('scoreboard players get TestRat bm.gvhu')) === h);
    await hook('grapple', q, 0.5, 6, 6.5);
    ok('...hook the wall: it won\'t bite (only the lamps)', !(await hanging()) && (await num('scoreboard players get TestRat bm.gvhu')) === h);
    // a lamp in reach: from the start ledge's edge, or from an island
    const hd = (fx, fz, cx, cz) => Math.hypot(Math.max(0, Math.abs(cx - 0.5 - fx)), Math.abs(cz - 0.5 - fz), 3.88);
    let from = null, cx, cz;
    for (const [ix, iz] of isl) { const fz = Math.min(14.7, Math.max(10.3, iz - 0.5)); if (hd(3.6, fz, ix, iz) <= 7.8) { from = [3.6, fz]; [cx, cz] = [ix, iz]; break; } }
    if (!from) for (const [ax, az] of isl) { for (const [ix, iz] of isl) if ((ix !== ax || iz !== az) && hd(ax - 0.5, az - 0.5, ix, iz) <= 7.8) { from = [ax - 0.5, az - 0.5]; [cx, cz] = [ix, iz]; break; } if (from) break; }
    await at('grapple', q, `tp TestRat ${relf(from[0], 4, from[1])} -90 0`); await sleep(300);
    await hook('grapple', q, cx - 0.5, 9.5, cz - 0.5); const hu1 = await num('scoreboard players get TestRat bm.gvhu'); await sleep(2500);
    const p = await local('grapple', q);
    ok('...hook a lamp in reach: hanging right under it, a hook spent', await hanging() && hu1 === h - 1 &&
       Math.abs(p[0] - (cx - 0.5)) < 0.8 && Math.abs(p[2] - (cz - 0.5)) < 0.8, `at ${p.map(v => v.toFixed(1))} lamp ${cx - 0.5},${cz - 0.5} hanging ${await hanging()} hooks ${await num('scoreboard players get TestRat bm.gvhu')}`);
    await letgo(); await sleep(500);
    const p2 = await local('grapple', q);
    ok('...let go: free, right over the island (it drops you on it)', !(await hanging()) && Math.abs(p2[0] - (cx - 0.5)) < 0.8 && Math.abs(p2[2] - (cz - 0.5)) < 0.8 &&
       /passed/.test(await at('grapple', q, `execute if block ${rel(cx - 1, 3, cz - 1)} minecraft:air`)) === false, `${p2.map(v => v.toFixed(1))}`);
    await at('grapple', q, `tp TestRat ${rel(12, 1, 12)}`); await sleep(600);
    const p3 = await local('grapple', q);
    ok('...into the hay: back to the start, the hooks back', p3[0] < 4 && (await num('scoreboard players get TestRat bm.gvhu')) === h, `${p3.map(v => v.toFixed(1))}`);
    await run('item replace entity TestRat weapon.mainhand with minecraft:carrot_on_a_stick[minecraft:custom_data={bm:"grappling_hook",bm_room:1b,bm_rhook:1b}]');
    await at('grapple', q, `tp TestRat ${rel(23, 4, 12)}`); await sleep(600);
    ok('...the far ledge: open', await solved('grapple', q), `${(await local('grapple', q)).map(v => v.toFixed(1))} s ${await sc('grapple', q, 'bm.gvs')}`);
    // the hook outside its room
    await run('scoreboard players set TestRat bm.gvhk 0');
    await run('execute as TestRat at @s run function bm:p21/grap/use'); await sleep(200);
    ok('Out of its room the Fixer\'s hook does nothing', !(await hanging()));
    // B: the swinging lamps
    q = await fresh('grapple', 'b', 3); await go('grapple', q, 2, 12);
    const lx = DATA.lanes[0] - 1;
    const where = async () => { for (const dz of [-3, 0, 3]) if (await isb('grapple', q, rel(lx, 9, 11 + dz), 'minecraft:target')) return dz; return null; };
    const seen = new Set(); for (let i = 0; i < 8; i++) { seen.add(await where()); await sleep(300); }
    seen.delete(null); ok('Variant B (the Swinging Lamps): the lamp swings through three places', seen.size === 3, [...seen].join(','));
    let w = null; for (let i = 0; i < 40 && w !== 0; i++) { w = await where(); if (w !== 0) await sleep(100); }
    await at('grapple', q, `tp TestRat ${relf(3.6, 4, 12.5)} -90 0`);
    await hook('grapple', q, lx + 0.5, 9.5, 11.5); await sleep(2000);
    const pb = await local('grapple', q);
    ok('...hooked as it swings over the island: hanging over the island', await hanging() && Math.abs(pb[2] - 11.5) < 0.9, `${pb.map(v => v.toFixed(1))}`);
    await letgo();
    // C: the bells
    q = await fresh('grapple', 'c', 3); await go('grapple', q, 4, 12); await sleep(500);
    const order = []; for (let k = 0; k < 4; k++) order.push(await sc('grapple', q, `bm.lq${k}`));
    const ring = async b => { const [x, y, z] = DATA.bells[b]; await at('grapple', q, `tp TestRat ${relf(7.5, 4, z + 0.5)} -90 0`); await sleep(200); await hook('grapple', q, x + 0.5, y + 0.5, z + 0.5); };
    const a0 = await alarm();
    await ring(order[1]);
    ok('Variant C (the Bells): a bell rung out of order - the alarm (and the hook doesn\'t pull)', (await alarm()) > a0 && !(await hanging()));
    for (const b of order) await ring(b);
    ok('...the four in the mural\'s order: the bridge comes out - open', await solved('grapple', q) && await isb('grapple', q, rel(12, 3, 12), 'minecraft:air') === false);
  }

  // ================================================================== THE MINECART RUN
  if (want('minecart')) {
    const mount = async q => { await at('minecart', q, 'ride TestRat mount @e[type=minecraft:minecart,tag=bm.gvcart,distance=..20,limit=1]'); await sleep(300); };
    const lp = async q => (await local('minecart', q)).map(v => +v.toFixed(1));
    const waitRide = async (q, ms) => { const t0 = Date.now(); let p; while (Date.now() - t0 < ms) { await sleep(500); if ((await sc('minecart', q, 'bm.gvs')) !== 2) break; } };
    // (Version A, the Rail Shooter, was retired in 2.74 - the cart's speed made its targets near impossible: B and C remain)
    let q;
    // B
    q = await fresh('minecart', 'b', 2); await go('minecart', q, 2, 12); await sleep(500);
    const a1 = await alarm(); await mount(q); await waitRide(q, 30000);
    ok('Variant B (the Switch Yard): points left as they are - a dead end, the alarm', (await alarm()) > a1 && !(await solved('minecart', q)), `${await lp(q)}`);
    await at('minecart', q, `setblock ${rel(2, 5, 14)} minecraft:lever[face=floor,facing=north,powered=true]`); await sleep(400);
    const sw = await isb('minecart', q, rel(12, 4, 12), 'minecraft:rail[shape=south_west]');
    await mount(q); await waitRide(q, 30000);
    ok('...points 2 thrown (the south loop): into the gold station - open', sw && await solved('minecart', q), `switch ${sw} at ${await lp(q)}`);
    // C
    q = await fresh('minecart', 'c', 2); await go('minecart', q, 2, 12); await sleep(500);
    await mount(q); await sleep(4000);
    const pc = await lp(q);
    ok('Variant C (the Drawbridges): no button pressed - into the gap, back to the station', pc[0] < 4.5 && (await sc('minecart', q, 'bm.gvs')) === 1, `${pc}`);
    const pressB = async i => { const [x, y, z] = DATA.buttons[i]; await at('minecart', q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[face=floor,facing=east,powered=true]`); await sleep(100);
      await at('minecart', q, `setblock ${rel(x, y, z)} minecraft:pale_oak_button[face=floor,facing=east,powered=false]`); };
    await pressB(0); await sleep(150); await mount(q);
    const t0 = Date.now(); const done = [false, false, false]; done[0] = true;
    while (Date.now() - t0 < 25000 && (await sc('minecart', q, 'bm.gvs')) === 2) {
      const p = await lp(q);
      if (!done[1] && p[0] >= 12) { await pressB(1); done[1] = true; }
      if (!done[2] && p[2] <= 6 && p[0] >= 16) { await pressB(2); done[2] = true; }
      await sleep(150);
    }
    ok('...each button pressed as the cart nears its gap: across all three - open', await solved('minecart', q), `${await lp(q)} ${done}`);
  }
  await run('function bm:admin/variant_random'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
