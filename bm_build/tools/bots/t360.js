// 3.0i: PROTECTED GROUND - a Survival player walks into the Black Market (the test market near 304, 288) and is put in Adventure
// (the "Protected ground" word on the action bar), and can't break the floor; out again, back in Survival. As a plain player,
// with a stale market tag (bm.adv) left on from before, with another place's tag left on (bm.kadv), and as an OPERATOR on a
// vanilla scoreboard team (deopped and taken off the team at the end, whatever happens).
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const res = []; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); res.push(!!c); };
  const is = async (sel) => /Test passed/.test(await run(`execute if entity ${sel}`));
  let opped = false;
  try {
    await run('deop TestRat'); await sleep(300);
    A.cmd('gamemode creative'); await sleep(500);
    ok(!(await is('@a[name=TestRat,gamemode=creative]')), 'the bot is no operator (its own /gamemode creative refused)');
    // the market: its nearest zone marker, a floor spot by it
    await run('tp TestRat 280 140 270'); await sleep(5000);
    const mp = (await run('execute positioned 304 0 288 run data get entity @e[type=minecraft:marker,tag=bm.zone_m,limit=1,sort=nearest] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    ok(mp, 'the test market\'s zone marker (bm.zone_m) is there' + (mp ? ` (${mp.slice(1).join(', ')})` : ''));
    if (!mp) throw new Error('no market');
    const [mx, my, mz] = mp.slice(1).map(Number);
    let spot = null;
    for (let d = 0; d < 6 && !spot; d++) for (const [dx, dz] of [[0, 0], [d, 0], [-d, 0], [0, d], [0, -d]]) {
      const x = Math.floor(mx) + dx, z = Math.floor(mz) + dz;
      for (let y = Math.floor(my) + 1; y >= Math.floor(my) - 6 && !spot; y--)
        if (/passed/.test(await run(`execute if block ${x} ${y} ${z} #bm:zone_floor_m if block ${x} ${y + 1} ${z} #minecraft:air if block ${x} ${y + 2} ${z} #minecraft:air`))) spot = [x, y + 1, z];
      if (spot) break;
    }
    ok(spot, 'a market floor spot by it' + (spot ? ` (${spot.join(' ')})` : ''));
    if (!spot) throw new Error('no floor');
    const [fx, fy, fz] = spot;
    await run('clear TestRat'); await run('loot give TestRat loot bm:items/market_key'); A.stand();
    const away = async () => { await run(`tp TestRat ${fx + 0.5} 140 ${fz + 0.5}`); await sleep(1800); };
    const walkIn = async (label) => {
      A.bars.length = 0; await run('scoreboard players reset TestRat bm.gdmsg');
      await run(`tp TestRat ${fx + 0.5} ${fy} ${fz + 0.5}`); await sleep(2000);
      ok(await is('@a[name=TestRat,gamemode=adventure]'), `${label}: on the market floor in Survival - now in Adventure`);
      ok(A.bars.some(b => /Protected ground/.test(b)), `${label}: told "Protected ground" on the action bar`);
      A.mine(fx, fy - 1, fz, 1200); await sleep(1600);
      ok(/passed/.test(await run(`execute if block ${fx} ${fy - 1} ${fz} #bm:zone_floor_m`)), `${label}: the floor under them doesn't break`);
      await away();
      ok(await is('@a[name=TestRat,gamemode=survival,tag=!bm.adv,tag=!bm.gdlk]'), `${label}: out of the market - Survival again, no tag left`);
    };
    // 1. a plain player
    await away(); await run('gamemode survival TestRat'); await run('tag TestRat remove bm.adv'); await run('tag TestRat remove bm.kadv'); await sleep(800);
    await walkIn('plain');
    // 2. a stale market tag (left on from before: died, logged out, crossed over...), put on out in the world
    await run('tag TestRat add bm.adv'); await sleep(200);
    await walkIn('stale bm.adv');
    // 3. a stale tag of another place (the Kingdom's), and the market tag too, given while standing ON the floor in Survival
    await run(`tp TestRat ${fx + 0.5} ${fy} ${fz + 0.5}`); await sleep(1500); await run('gamemode survival TestRat'); await run('tag TestRat add bm.adv'); await run('tag TestRat add bm.kadv');
    await sleep(2000);
    ok(await is('@a[name=TestRat,gamemode=adventure]'), 'stale tags, switched to Survival while inside: back in Adventure');
    await run('tag TestRat remove bm.kadv'); await away();
    ok(await is('@a[name=TestRat,gamemode=survival,tag=!bm.adv]'), 'stale tags: out of the market - Survival again');
    // 4. an operator on a vanilla team
    await run('team add t360'); await run('team join t360 TestRat'); await run('op TestRat'); opped = true; await sleep(500);
    await run('gamemode survival TestRat'); await sleep(500);
    await walkIn('op on a team');
  } catch (e) { console.log('FATAL', e.message); res.push(false); }
  finally {
    if (opped) await run('deop TestRat');
    await run('team leave TestRat'); await run('team remove t360'); await run('gamemode survival TestRat');
    await run('tag TestRat remove bm.adv'); await run('tag TestRat remove bm.kadv');
  }
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });
