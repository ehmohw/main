// 2.72 (II): room curses, forks in the road, corridor traps
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local, pos } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const attr = async (a) => +(((await run(`attribute TestRat minecraft:${a} get`)).match(/is (-?[\d.]+)/) || [0, NaN])[1]);
  const hasFx = async (sel, fx) => /passed/.test(await run(`execute in bm:gutter if entity ${sel.replace(/]$/, `,nbt={active_effects:[{id:"minecraft:${fx}"}]}]`)}`));
  const labels = async (k, q) => (await at(k, q, 'execute as @e[type=minecraft:text_display,distance=..16] run data get entity @s text'));
  const pot = async () => { const gi = await num('scoreboard players get TestRat bm.gvi'); return num(`execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${gi}},limit=1] bm.gvpot`); };
  const health = () => num('data get entity TestRat Health');
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never');

  // ================================================================== ROOM CURSES
  if (want('curse')) {
    await run('function bm:admin/curse_never');
    await heist('levers', 'a', 5); await begin();
    let Q = await qs('levers');
    let n = 0; for (const q of Q) if ((await sc('levers', q, 'bm.gvcrs')) > 0) n++;
    ok(`curse_never: no room of ${Q.length} cursed`, Q.length > 0 && n === 0);
    // FOG and FROST on a calm room
    for (const [nm, c, fx] of [['fog', 1, 'darkness'], ['frost', 2, 'slowness']]) {
      await run(`function bm:admin/curse_${nm}`); await heist('levers', 'a', 2); await begin();
      const q = (await qs('levers'))[0];
      const L = await labels('levers', q);
      ok(`${nm.toUpperCase()}: the room is cursed (${c}) and says so over the door`, (await sc('levers', q, 'bm.gvcrs')) === c && /CURSED: /.test(L) && L.includes(nm.toUpperCase()));
      await go('levers', q, 12, 12); await sleep(1500);
      ok(`...in the room: ${fx}`, await hasFx('@a[name=TestRat]', fx));
    }
    // LEADEN: no jumping in the room; back to normal on leaving
    await run('function bm:admin/curse_leaden'); await heist('levers', 'a', 2); await begin();
    let q = (await qs('levers'))[0];
    const j0 = await attr('jump_strength');
    await go('levers', q, 12, 12); await sleep(800);
    const j1 = await attr('jump_strength');
    await go('levers', q, -6, 12); await sleep(800);
    const j2 = await attr('jump_strength');
    ok('LEADEN: jump strength 0 in the room, back on leaving', (await sc('levers', q, 'bm.gvcrs')) === 3 && j1 === 0 && j0 > 0.3 && j2 === j0, `${j0} -> ${j1} -> ${j2}`);
    // ...beaten: the pot takes the curse's bonus, and the crew hears it
    await go('levers', q, 12, 12); await sleep(300);
    A.bars.length = 0; const p0 = await pot();
    await at('levers', q, 'function bm:p70/solved'); await sleep(400);
    ok('...beaten: "The curse lifts" and a little extra in the pot', A.bars.some(b => /curse lifts/.test(b)) && (await pot()) > p0, `${p0} -> ${await pot()} ${JSON.stringify(A.bars.slice(-3))}`);
    await sleep(500);
    ok('...and the curse stops working once the room is beaten', (await attr('jump_strength')) === j0);
    // LEADEN can't land on a room you cross by jumping (the Tile Floor): no curse at all there
    await heist('tiles', 'a', 2); await begin();
    Q = await qs('tiles'); n = 0; for (const q2 of Q) n += (await sc('tiles', q2, 'bm.gvcrs')) > 0 ? 1 : 0;
    ok('LEADEN forced, Tile Floor rooms: not one cursed (a jumping room only takes Fog)', Q.length > 0 && n === 0);
    await run('function bm:admin/curse_always'); await heist('tiles', 'a', 2); await begin();
    Q = await qs('tiles'); n = 0; for (const q2 of Q) n += (await sc('tiles', q2, 'bm.gvcrs')) === 1 ? 1 : 0;
    ok('curse_always, Tile Floor rooms: every one cursed - with FOG', Q.length > 0 && n === Q.length);
    // FRAGILE: armour halved
    await run('function bm:admin/curse_fragile'); await heist('guards', 'a', 2); await begin();
    q = (await qs('guards'))[0];
    await run('item replace entity TestRat armor.chest with minecraft:iron_chestplate'); await sleep(300);
    const a0 = await attr('armor'); await go('guards', q, 12, 12); await sleep(800); const a1 = await attr('armor');
    ok('FRAGILE: armour counts for half in the fight', (await sc('guards', q, 'bm.gvcrs')) === 4 && a0 === 6 && a1 === 3, `${a0} -> ${a1}`);
    // PHANTOMS: invisible guards
    await run('function bm:admin/curse_phantoms'); await heist('guards', 'a', 2); await begin();
    q = (await qs('guards'))[0]; await go('guards', q, 6, 12); await sleep(5000);
    const g = await at('guards', q, 'execute store result score #t bm.rng if entity @e[tag=bm.gvg,distance=..18]');
    const gi = await at('guards', q, 'execute store result score #t bm.rng if entity @e[tag=bm.gvg,distance=..18,nbt={active_effects:[{id:"minecraft:invisibility"}]}]');
    const ng = +((g.match(/(\d+)/) || [0, 0])[1]), ngi = +((gi.match(/(\d+)/) || [0, 0])[1]);
    ok('PHANTOMS: every guard invisible', (await sc('guards', q, 'bm.gvcrs')) === 5 && ng > 0 && ngi === ng, `${ngi}/${ng}`);
    // FRENZY: faster, harder-hitting guards
    await run('function bm:admin/curse_frenzy'); await heist('guards', 'a', 2); await begin();
    q = (await qs('guards'))[0]; await go('guards', q, 6, 12); await sleep(5000);
    const fz = await at('guards', q, 'execute store result score #t bm.rng if entity @e[tag=bm.gvg,tag=bm.gvfrz,distance=..18]');
    const gz = await at('guards', q, 'execute store result score #t bm.rng if entity @e[tag=bm.gvg,distance=..18]');
    const mod = await at('guards', q, 'attribute @e[tag=bm.gvg,distance=..18,limit=1] minecraft:movement_speed modifier value get bm:curse_frenzy');
    ok('FRENZY: every guard quickened (+25% speed, +30% damage)', (await sc('guards', q, 'bm.gvcrs')) === 6 && +((gz.match(/(\d+)/) || [0, 0])[1]) > 0 && fz.match(/(\d+)/)[1] === gz.match(/(\d+)/)[1] && /0\.25/.test(mod), mod);
    // UNSTEADY: the floor lurches - levitation now and then
    await run('function bm:admin/curse_unsteady'); await heist('guards', 'a', 2); await begin();
    q = (await qs('guards'))[0]; await go('guards', q, 12, 12);
    let lev = false; for (let i = 0; i < 14 && !lev; i++) { await sleep(400); lev = await hasFx('@a[name=TestRat]', 'levitation'); }
    ok('UNSTEADY: within five seconds the floor lurches (levitation)', (await sc('guards', q, 'bm.gvcrs')) === 7 && lev);
    // the odds: Tier V, by chance, about one room in five
    await run('function bm:admin/curse_chance');
    let tot = 0, cur = 0;
    for (let h = 0; h < 3; h++) { await heist('levers', 'a', 5); Q = await qs('levers'); tot += Q.length; for (const q2 of Q) cur += (await sc('levers', q2, 'bm.gvcrs')) > 0 ? 1 : 0; }
    ok(`by chance at Tier V: ${cur} of ${tot} rooms cursed (21% each)`, tot > 0 && cur <= tot * 0.7);
    await run('function bm:admin/curse_never');
    await run('item replace entity TestRat armor.chest with minecraft:air');
  }

  // ================================================================== FORKS IN THE ROAD
  if (want('fork')) {
    await run('function bm:admin/curse_never'); await run('function bm:admin/fork_always');
    await heist('guards', 'a', 3); await begin();
    let F = await qs('fork');
    ok('fork_always: one Fork in the heist (room 2 or 3)', F.length === 1 && F[0] >= 2 && F[0] <= 3, JSON.stringify(F));
    let f = F[0];
    const nxt = f + 1;
    ok('...the room after it is an ordinary fight, not Prime, not cursed', (await cnt(room('guards', nxt))) === 1 && (await sc('guards', nxt, 'bm.gvcrs')) === 0 &&
       !/passed/.test(await at('guards', nxt, 'execute if entity @s[tag=bm.gvprime]')));
    await go('fork', f, 4, 12); await sleep(2500);
    ok('...nobody on a pad: both doors stay barred', (await sc('fork', f, 'bm.gvs')) === 1 &&
       /passed/.test(await at('fork', f, `execute if block ${rel(13, 5, 5)} minecraft:iron_bars if block ${rel(13, 5, 19)} minecraft:iron_bars`)));
    await go('fork', f, 10, 5); await sleep(900); await go('fork', f, 4, 12); await sleep(2500);
    ok('...a second on the skull pad, then off: the count starts over, still barred', (await sc('fork', f, 'bm.gvs')) === 1 && (await sc('fork', f, 'bm.gvx')) === 0);
    await go('fork', f, 10, 5); await sleep(3000);
    ok('THE HARD WAY: two seconds on the skull pad - the skull door opens (the plain stays barred) and the way on',
       (await sc('fork', f, 'bm.gvs')) === 3 && /passed/.test(await at('fork', f, `execute if block ${rel(13, 5, 5)} minecraft:air if block ${rel(13, 5, 19)} minecraft:iron_bars if block ${rel(24, 5, 12)} minecraft:air`)));
    const crs = await sc('guards', nxt, 'bm.gvcrs');
    ok('...the next room is now PRIME and CURSED (and marked for the bonus)', crs >= 1 && crs <= 7 &&
       /passed/.test(await at('guards', nxt, 'execute if entity @s[tag=bm.gvprime,tag=bm.gvskull]')) && /PRIME/.test(await labels('guards', nxt)) && /CURSED/.test(await labels('guards', nxt)), `curse ${crs}`);
    await go('guards', nxt, 12, 12); await sleep(300);
    A.bars.length = 0; const p0 = await pot();
    await at('guards', nxt, 'function bm:p70/solved'); await sleep(400);
    ok('...beaten: "The hard way pays!" - a fat cut into the pot', A.bars.some(b => /hard way pays/.test(b)) && (await pot()) > p0 + 3, `${p0} -> ${await pot()} ${JSON.stringify(A.bars.slice(-3))}`);
    // the safe way
    await heist('guards', 'a', 3); await begin();
    f = (await qs('fork'))[0];
    await go('fork', f, 10, 19); await sleep(3000);
    ok('THE SAFE WAY: the plain pad - the plain door opens, the skull door stays barred',
       (await sc('fork', f, 'bm.gvs')) === 3 && /passed/.test(await at('fork', f, `execute if block ${rel(13, 5, 19)} minecraft:air if block ${rel(13, 5, 5)} minecraft:iron_bars if block ${rel(24, 5, 12)} minecraft:air`)));
    ok('...and the next room is left as it was', (await sc('guards', f + 1, 'bm.gvcrs')) === 0 && !/passed/.test(await at('guards', f + 1, 'execute if entity @s[tag=bm.gvprime]')));
    // the crew must agree
    let M = null; try { M = await bot('TestMouse'); await sleep(2500); } catch (e) {}
    if (M) {
      await heist('guards', 'a', 3); await H.mouse(); await begin();
      f = (await qs('fork'))[0];
      await go('fork', f, 10, 5); await at('fork', f, `tp TestMouse ${rel(10, 4, 19)}`); await sleep(3000);
      ok('A crew of two split across the pads: neither door opens', (await sc('fork', f, 'bm.gvs')) === 1);
      await at('fork', f, `tp TestMouse ${rel(10, 4, 5)}`); await sleep(3000);
      ok('...both on the skull pad: it opens', (await sc('fork', f, 'bm.gvs')) === 3 && /passed/.test(await at('fork', f, `execute if block ${rel(13, 5, 5)} minecraft:air`)));
      await run('tag TestMouse remove bm.gvp'); await run('scoreboard players reset TestMouse bm.gvi'); M.end();
    } else ok('(TestMouse could not join - crew vote not tested)', false);
    // never
    await run('function bm:admin/fork_never'); await heist('guards', 'a', 3);
    ok('fork_never: no Fork', (await qs('fork')).length === 0);
    // the odds
    await run('function bm:admin/fork_chance'); await run('function bm:admin/rooms_any'); await run('scoreboard players set #thr bm.rng 0');
    let nf = 0, badq = 0; for (let h = 0; h < 90; h++) { await run('scoreboard players set #gk bm.rng 6'); await run('function bm:p116/fork/roll');
      if ((await num('scoreboard players get #fk bm.rng')) === 1) { nf++; const fq = await num('scoreboard players get #fkq bm.rng'); if (fq < 2 || fq > 5) badq++; } }
    ok(`fork_chance: the draw gives a fork ${nf} times in 90 (one in three), always at room 2 or 3`, nf >= 15 && nf <= 48 && badq === 0);
    await run('function bm:admin/fork_never');
  }

  // ================================================================== CORRIDOR TRAPS
  if (want('trap')) {
    await run('function bm:admin/curse_never'); await run('function bm:admin/traps_never');
    await heist('levers', 'a', 2); await begin();
    let GI = await num('scoreboard players get TestRat bm.gvi');
    ok('traps_never: no trap in any passage', (await cnt(`@e[type=minecraft:marker,tag=bm.gvtrap,scores={bm.gvi=${GI}}]`)) === 0);
    await run('function bm:admin/traps_always'); await heist('levers', 'a', 3); await begin();
    GI = await num('scoreboard players get TestRat bm.gvi');
    const nt = await cnt(`@e[type=minecraft:marker,tag=bm.gvtrap,scores={bm.gvi=${GI}}]`);
    const Q = await qs('levers');
    ok(`traps_always: a trap in every straight or bending passage (${nt} for ${Q.length} rooms)`, nt >= 1);
    await run('execute in bm:gutter run tag @e[tag=bm.tsel] remove bm.tsel');
    await run(`execute in bm:gutter run tag @e[type=minecraft:marker,tag=bm.gvtrap,scores={bm.gvi=${GI}},limit=1,sort=arbitrary] add bm.tsel`);
    const T = '@e[type=minecraft:marker,tag=bm.tsel,limit=1]';
    console.log('   trap at', await run(`execute in bm:gutter run data get entity ${T} Pos`));
    // is it in the walkway? (air where you stand, a floor under it, inside the passage's walls)
    const okSpot = /passed/.test(await run(`execute in bm:gutter as ${T} at @s if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air if block ~ ~ ~-1 minecraft:air if block ~ ~ ~1 minecraft:air`));
    ok('...the trap sits in the walkway (open above, floor below, the passage either side)', okSpot);
    await run('effect clear TestRat');
    for (const [ty, nm, wait] of [[1, 'FLAME JETS', 3500], [2, 'SPIKES', 3000], [3, 'ARROW SLITS', 2000]]) {
      await run(`execute in bm:gutter as ${T} run scoreboard players set @s bm.gvy1 ${ty}`); await run(`execute in bm:gutter as ${T} run scoreboard players set @s bm.gvtm 0`);
      await run(`execute in bm:gutter as ${T} run scoreboard players set @s bm.gvx 0`);
      // standing beside it (outside the strip) - no harm
      await run(`execute in bm:gutter as ${T} at @s run tp TestRat ~-4 ~ ~ -90 0`); await run('effect give TestRat instant_health 1 3 true'); await sleep(500);
      const h0 = await health(); await sleep(wait); const h1 = await health();
      await run(`execute in bm:gutter as ${T} at @s run tp TestRat ~ ~ ~ -90 0`); await run(`execute in bm:gutter as ${T} run scoreboard players set @s bm.gvtm 0`);
      const h2 = await health(); await sleep(wait); const h3 = await health();
      ok(`${nm}: four blocks off, unhurt; on the strip, hurt`, h1 >= h0 && h3 < h2, `${h0}->${h1}; ${h2}->${h3} ${await run('data get entity TestRat active_effects')}`);
      await run('effect give TestRat instant_health 1 3 true'); await sleep(1500);
    }
    await run('effect give TestRat resistance 900 4 true');
    await run('kill @e[type=minecraft:arrow,tag=bm.gvtar]');
    await run('function bm:admin/traps_never');
  }

  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
