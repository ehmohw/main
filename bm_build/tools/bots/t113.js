// 2.70: the throne rooms (gold, diamond, netherite - and their odds) and Prime fights
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, solved, go, qs, heist, begin } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const pid = await num('scoreboard players get TestRat bm.pid');
  const pot = () => num('execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,limit=1] bm.gvpot');
  const haul = () => run(`data get storage bm:gv pot.p${pid}`);
  const T = { gold: [1, 'gold_block', 20], diamond: [2, 'diamond_block', 35], netherite: [3, 'netherite_block', 50] };

  if (want('throne')) {
    for (const [key, [v, hb, coins]] of Object.entries(T)) {
      await run(`function bm:admin/throne_${key}`);
      await heist('guards', 'a', 2); await run('function bm:admin/rooms_any');
      const Q = await qs('throne');
      ok(`The ${key} throne: laid when forced, as room 2-4`, Q.length === 1 && Q[0] >= 2 && Q[0] <= 4, `${Q}`);
      if (!Q.length) continue;
      const q = Q[0];
      ok('...the hoard is ' + key + ' (seat back, piles), no stand-in blocks left', (await sc('throne', q, 'bm.gvvar')) === v &&
         /passed/.test(await at('throne', q, `execute if block ${rel(12, 6, 1)} minecraft:${hb} if block ${rel(4, 5, 3)} minecraft:${hb}`)) &&
         (await num(`execute in bm:gutter as ${room('throne', q)} at @s store result score #t bm.rng run fill ${rel(0, 4, 0)} ${rel(24, 10, 24)} minecraft:sponge replace minecraft:sponge`)) <= 0);
      ok('...the way on is shut until the coffer is opened', /passed/.test(await at('throne', q, `execute unless block ${rel(24, 5, 12)} minecraft:air`)));
      await begin();
      await go('throne', q, 6, 12); await sleep(800);
      ok('...walk in: the throne is announced', (await sc('throne', q, 'bm.gvs')) === 1);
      await run(`data remove storage bm:gv pot.p${pid}`);
      const p0 = await pot();
      await run('execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.gvthc] run data merge entity @s {interaction:{player:[I;1,2,3,4],timestamp:1L}}'); await sleep(600);
      const p1 = await pot(); const h = await haul();
      ok(`...open the Royal Coffer: coins in the pot (${coins}, the pot keeps a third), a ${key} share in the haul, the way opens`,
         p1 - p0 >= Math.floor(coins / 3) && new RegExp(`p113/throne_${key}`).test(h) && await solved('throne', q), `pot ${p0} -> ${p1}, haul ${h.slice(-80)}`);
      ok('...the coffer is spent (no second share)', (await cnt('@e[type=minecraft:interaction,tag=bm.gvthc]')) === 0);
      // the share itself (rolled now, into a test chest)
      await at('throne', q, `setblock ${rel(5, 4, 12)} minecraft:chest`);
      await at('throne', q, `loot insert ${rel(5, 4, 12)} loot bm:p113/throne_${key}`);
      const inv = await at('throne', q, `data get block ${rel(5, 4, 12)} Items`);
      const want_ = { gold: /gold_ingot/, diamond: /minecraft:diamond"/, netherite: /netherite_ingot/ }[key];
      ok(`...a ${key} share holds what it should`, want_.test(inv), inv.slice(0, 160));
      await at('throne', q, `setblock ${rel(5, 4, 12)} minecraft:air`);
    }
    // the odds: 1 in 50, 1 in 100, 1 in 150
    await run('scoreboard players set #frk bm.gvv 0'); await run('scoreboard players set #gk bm.rng 5');
    const n = { 0: 0, 1: 0, 2: 0, 3: 0 }; const N = 3000;
    for (let i = 0; i < N; i++) { await run('function bm:p113/throne/roll'); n[await num('scoreboard players get #thr bm.rng')]++; }
    ok(`The odds over ${N} heists: gold about 60, diamond about 30, netherite about 20`, n[1] >= 35 && n[1] <= 90 && n[2] >= 14 && n[2] <= 50 && n[3] >= 8 && n[3] <= 36,
       `gold ${n[1]} diamond ${n[2]} netherite ${n[3]}`);
    await run('function bm:admin/rooms_only_guards'); await run('scoreboard players set #r bm.rng 1');
    let any = 0; for (let i = 0; i < 200; i++) { await run('function bm:p113/throne/roll'); if (await num('scoreboard players get #thr bm.rng') > 0) any++; }
    ok('...never in a heist forced to one kind of room (admin/tests)', any === 0, `${any}`);
    await run('function bm:admin/rooms_any');
  }

  if (want('prime')) {
    await run('function bm:admin/prime_always');
    await heist('guards', 'a', 2); await begin();
    const Q = await qs('guards'); const q = Q[0];
    let all = true; for (const qq of Q) if (!/bm\.gvprime/.test(await run(`execute in bm:gutter run data get entity ${room('guards', qq)} Tags`))) all = false;
    ok('PRIME forced: every fight room is Prime, a red banner over its door', Q.length >= 2 && all &&
       (await cnt('@e[type=minecraft:text_display,tag=bm.gvprop]')) > 0 && /PRIME/.test(await at('guards', q, `data get entity @e[type=minecraft:text_display,distance=..14,sort=nearest,limit=1] text`)), `${Q}`);
    await go('guards', q, 6, 12); await sleep(2000);
    const g = await cnt(`@e[tag=bm.gvg]`); const gp = await cnt(`@e[tag=bm.gvg,tag=bm.gvprm]`);
    await run('execute in bm:gutter as @e[tag=bm.gvprm,limit=1] run tag @s add t113p');
    const fl = async c => +(((await run(c)).match(/(-?[\d.]+)f?\s*$/) || [0, -1])[1]);
    const hp = await fl('execute in bm:gutter as @e[tag=t113p] run attribute @s minecraft:max_health get');
    const base = await fl('execute in bm:gutter as @e[tag=t113p] run attribute @s minecraft:max_health base get');
    const nm = await run('execute in bm:gutter run data get entity @e[tag=t113p,limit=1] CustomName');
    const h = await fl('execute in bm:gutter run data get entity @e[tag=t113p,limit=1] Health');
    ok('...walk in: every guard is Prime - more health (and full of it), its name marked', g >= 2 && gp === g && hp >= base * 1.5 && h >= hp * 0.8 && h > base && /Prime/.test(nm),
       `${gp}/${g}, hp ${h}/${hp} (base ${base})`);
    const dmg = await run('execute in bm:gutter as @e[tag=bm.gvprm,limit=1] run attribute @s minecraft:attack_damage modifier value get bm:prime_dmg');
    ok('...and harder hits', /0\.5/.test(dmg), dmg);
    await run(`data remove storage bm:gv pot.p${pid}`); const p0 = await pot();
    for (let w = 0; w < 3; w++) { await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(1800); }
    const p1 = await pot(); const hl = await haul();
    ok('...beaten: extra coins in the pot (8 + 4 a tier, a third kept) and a better find in the haul', await solved('guards', q) && p1 - p0 >= 5 && /p113\/prime/.test(hl), `pot ${p0} -> ${p1}, ${hl.slice(-60)}`);
    await run('function bm:admin/prime_never');
    await heist('guards', 'a', 2);
    let none = true; for (const qq of await qs('guards')) if (/bm\.gvprime/.test(await run(`execute in bm:gutter run data get entity ${room('guards', qq)} Tags`))) none = false;
    ok('admin/prime_never: no Prime rooms', none);
    await run('function bm:admin/prime_chance');
    let pr = 0, tot = 0;
    for (let i = 0; i < 400; i++) { await run('execute in bm:gutter run summon minecraft:marker 0 200 0 {Tags:["t113m","bm.gvr_guards"]}');
      await run('execute in bm:gutter as @e[type=minecraft:marker,tag=t113m] run function bm:p113/prime/roll');
      if (/passed/.test(await run('execute in bm:gutter if entity @e[type=minecraft:marker,tag=t113m,tag=bm.gvprime]'))) pr++; tot++;
      await run('execute in bm:gutter run kill @e[type=minecraft:marker,tag=t113m]'); await run('execute in bm:gutter run kill @e[type=minecraft:text_display,x=0,y=200,z=0,distance=..20]'); }
    ok('...by chance: about one fight room in eight', pr >= 25 && pr <= 80, `${pr}/${tot}`);
    await run('function bm:admin/rooms_any');
  }
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
