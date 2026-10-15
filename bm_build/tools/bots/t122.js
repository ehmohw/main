// 2.74b: Speed Run with the alarm off, patrols stop at the vault, puzzle skip, a mistake's guard cleared, solo crew of 3,
// boss bar range, Endless/Pit alarm switch, Minecart A retired, loose carpets swept, kit armour unbreakable
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const fs = require('fs');
const OUT = BMB + 'out_p2/BlackMarket_DP/data/bm/function/';
const res = [];
const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, room, at, sc, qs, heist, begin } = H;
  const want = k => !ONLY || ONLY.test(k);
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter if entity ${sel}`); return /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0; };
  const A = await bot('TestRat'); await sleep(2500);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');

  if (want('speed')) {
    await heist('levers', 'a', 1); await begin(); await sleep(1000);
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const I = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gval 0`); await run(`execute in bm:gutter run scoreboard players set ${I} bm.gva 0`);
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvmod 4`); await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvtm 999999`);
    await sleep(2500);
    const lk = await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlk`), ga = await num(`execute in bm:gutter run scoreboard players get ${I} bm.gva`);
    ok('Speed Run, alarm off, time runs out: TIME\'S UP (the haul shrinks) - but no alarm', lk === 1 && ga === 0, `lk ${lk} alarm ${ga}`);
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvw 39`); await run(`execute in bm:gutter run scoreboard players set ${I} bm.gva 100`);
    const g0 = await cnt(`@e[tag=bm.gvg,scores={bm.gvi=${GI}}]`); await sleep(17000);
    const g1 = await cnt(`@e[tag=bm.gvg,scores={bm.gvi=${GI}}]`);
    ok('...and no patrols come, however long you take', g1 <= g0, `${g0} -> ${g1}`);
    // alarm ON: patrols, but not once the vault's open
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gval 1`); await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvst 3`);
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvw 0`); await sleep(3000);
    ok('Alarm on, vault open (the boss beaten): the patrol clock stops', (await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvw`)) === 0);
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvst 2`); await sleep(3000);
    ok('...while the heist is on, it runs as before', (await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvw`)) >= 2);
  }

  if (want('skip')) {
    await heist('levers', 'a', 2); await begin(); await sleep(1000);
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const I = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
    const [q1, q2] = await qs('levers');
    A.chats.length = 0;
    await at('levers', q1, `tp TestRat ${rel(4, 4, 12)}`); await sleep(2500);
    ok('Walk into a puzzle: "Stuck? [Skip this puzzle - costs a try]"', A.chats.some(c => /Skip this puzzle/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 160));
    const lv0 = await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlv`);
    A.cmd('trigger bm.act set 7733'); await sleep(700);
    ok('Click it: it asks first (nothing skipped yet)', (await sc('levers', q1, 'bm.gvs')) < 3 && (await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlv`)) === lv0);
    A.chats.length = 0;
    A.cmd('trigger bm.act set 7734'); await sleep(700);
    const lv1 = await num(`execute in bm:gutter run scoreboard players get ${I} bm.gvlv`);
    ok(`Skip it: the way on opens, a try gone (${lv0} -> ${lv1}), no flawless mark`, (await sc('levers', q1, 'bm.gvs')) === 3 && lv1 === lv0 - 1 && (await sc('levers', q1, 'bm.gvf')) >= 1);
    ok('...the crew is told', A.chats.some(c => /skipped the puzzle/.test(c) && /cost a try/.test(c)));
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvlv 1`);
    await at('levers', q2, `tp TestRat ${rel(4, 4, 12)}`); await sleep(500);
    A.chats.length = 0;
    A.cmd('trigger bm.act set 7734'); await sleep(700);
    ok('Never on the last try', (await sc('levers', q2, 'bm.gvs')) < 3 && A.chats.some(c => /last try/.test(c)));
    // a wrong move's guard, gone when the room is solved
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvlv 5`);
    await at('levers', q2, 'function bm:p70/ctx'); await at('levers', q2, `execute positioned ${rel(6, 4, 12)} run function bm:p70/guard`); await sleep(500);
    const inroom = async () => { const o = await at('levers', q2, 'execute positioned ~-12.5 ~-4 ~-12.5 if entity @e[tag=bm.gvg,tag=!bm.gvboss,dx=24,dy=24,dz=24]'); return /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0; };
    const gA = await inroom();
    await at('levers', q2, 'function bm:p70/solved'); await sleep(500);
    const gB = await inroom();
    ok(`A wrong move calls a guard (${gA}); the room solved, it goes (${gB})`, gA >= 1 && gB === 0);
    // loose carpets: swept
    await at('levers', q2, `summon minecraft:item ${rel(6, 5, 12)} {Item:{id:"minecraft:moss_carpet",count:1}}`);
    await at('levers', q2, `summon minecraft:item ${rel(7, 5, 12)} {Item:{id:"minecraft:red_carpet",count:1}}`); await sleep(2200);
    const lo = await at('levers', q2, 'execute positioned ~-12.5 ~-6 ~-12.5 if entity @e[type=minecraft:item,dx=24,dy=26,dz=24]'); const lc = /passed/.test(lo) ? 1 : 0;
    ok('Loose carpets in a room near the crew are swept up', lc === 0, `${lc}`);
    // boss bar: only near the guardian
    const s = GI - 1;
    await at('levers', q1, `tp TestRat ${rel(4, 4, 12)}`); await sleep(1500);
    const far = await run(`bossbar get bm:gvb${s} players`);
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1] at @s run tp TestRat ${rel(10, 4, 12)} -90 0`); await sleep(4000);
    const near = await run(`bossbar get bm:gvb${s} players`);
    const back = async () => { await at('levers', q1, `tp TestRat ${rel(4, 4, 12)}`); await sleep(1500); return run(`bossbar get bm:gvb${s} players`); };
    const far2 = await back();
    ok('The guardian\'s bar: hidden far off, shown near it', /no players/i.test(far) && /TestRat/.test(near) && /no players/i.test(far2), `${far.slice(0, 50)} | ${near.slice(0, 50)} | ${far2.slice(0, 50)}`);
  }

  if (want('static')) {
    await run('execute as TestRat run function bm:p98/count');
    ok('Raiding alone: room for three followers', (await num('scoreboard players get #lim bm.rng')) === 3);
    const na = fs.readFileSync(OUT + 'p122/lives_show_na.mcfunction', 'utf8'), lm = fs.readFileSync(OUT + 'p75/lives_menu.mcfunction', 'utf8');
    ok('Endless Vault / the Pit: the tries page has no ALARM switch (the alarm stays off)', !/set 7619/.test(na) && /gvpt matches 6\.\.7/.test(lm) && /unless score @s bm.gvpt matches 6\.\.7/.test(fs.readFileSync(OUT + 'p75/pick_lives.mcfunction', 'utf8')));
    const mi = fs.readFileSync(OUT + 'p115/minecart/init.mcfunction', 'utf8');
    ok('The Minecart Run\'s shooting gallery is out of the draw', /if score @s bm.gvvar matches 0 store result score @s bm.gvvar run random value 1\.\.2/.test(mi));
    let tot = 0, ub = 0;
    for (const f of fs.readdirSync(OUT + 'p80/kit').filter(f => /^give_\d_\d\.mcfunction$/.test(f)))
      for (const l of fs.readFileSync(OUT + 'p80/kit/' + f, 'utf8').split('\n')) if (/armor\.(head|chest|legs|feet) with/.test(l)) { tot++; if (/unbreakable/.test(l)) ub++; }
    ok(`Every kit's armour, every rank, unbreakable (${ub}/${tot})`, tot > 0 && ub === tot);
    await run('clear TestRat'); await run('scoreboard players set TestRat bm.kr2 1'); await run('execute as TestRat at @s run function bm:p80/kit/give_2_1'); await sleep(300);
    ok('...the Offense kit\'s armour on you: unbreakable', /unbreakable/.test(await run('data get entity TestRat equipment.chest')));
  }

  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
