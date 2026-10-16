// 2.80i: tough mobs, not health sponges - and not faster than a sprinting player. As a regular (non-op) player standing at
// the end of a long, flat stone runway at night; rcon sets the stage: a zombie at the far end, made a Blood Moon horror,
// a Champion or an Elite the way the game makes them, mounted on its steed where it has one.
//   Each one comes at you: its chase speed (blocks a second over the stretch it runs straight at you) stays under a
//   sprinting player's 5.6 - a vanilla zombie's pace for reference. (It starts 30 blocks off: in every one's follow range.)
//   Creepers - a Blood Moon one, a Champion, an Elite - run no faster than a plain creeper.
//   Gear: twelve of each kind - no full Protection sets any more, most pieces light, some bare.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const X = 18000, Y = 120, Z = 18000, LEN = 56;
  const at = `x=${X},y=${Y},z=${Z},dx=${LEN + 4},dy=8,dz=6`;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + LEN + 8} ${Z + 14}`); await sleep(1500);
  await run(`${O}fill ${X - 4} ${Y - 1} ${Z - 2} ${X + LEN + 4} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 4} ${Y} ${Z - 2} ${X + LEN + 4} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}fill ${X - 4} ${Y} ${Z - 3} ${X + LEN + 4} ${Y + 3} ${Z - 3} minecraft:glass`); await run(`${O}fill ${X - 4} ${Y} ${Z + 9} ${X + LEN + 4} ${Y + 3} ${Z + 9} minecraft:glass`);
  await run('time set 18000'); await run('weather clear'); await run('gamerule doMobSpawning false');
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('effect give TestRat minecraft:regeneration 600 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 3.5} -90 0`); await sleep(800); A.stand();
  const clear = async () => { await run(`${O}kill @e[type=!minecraft:player,${at}]`); await sleep(300); };
  const xOf = async sel => { const m = (await run(`${O}data get entity ${sel} Pos[0]`)).match(/(-?[\d.]+)d\s*$/); return m ? +m[1] : NaN; };

  // ---- the chase: blocks a second over the stretch it runs straight at you
  const chase = async (label, make, mount) => {
    await clear();
    await run(`${O}summon minecraft:zombie ${X + 30.5} ${Y} ${Z + 3.5} {Tags:["t193","bm.seen"],PersistenceRequired:1b}`);
    const Zs = `@e[type=minecraft:zombie,tag=t193,limit=1,${at}]`;
    if (make) await run(`${O}execute as ${Zs} at @s run function bm:${make}`);
    await run(`${O}kill @e[tag=bm.minion,${at}]`);                                   // (a Champion's two minions: not this test)
    if (mount) for (let k = 0; k < 60 && !/passed/.test(await run(`${O}execute as ${Zs} on vehicle if entity @s`)); k++) {
      await run(`${O}execute as ${Zs} at @s run function bm:${mount}`); }
    const S = mount ? `@e[type=minecraft:zombie_horse,${at},limit=1]` : Zs;
    if (mount && !/passed/.test(await run(`${O}execute as ${Zs} on vehicle if entity @s`))) { ok(`${label}: mounted for the chase`, false); return 0; }
    await run(`${O}effect clear @e[${at},type=!minecraft:player] minecraft:slowness`);
    let t0 = 0, x0 = 0, t1 = 0, x1 = 0;
    const s0 = Date.now();
    while (Date.now() - s0 < 20000) {
      const x = await xOf(S); const t = Date.now();
      if (!t0 && x < X + 28) { t0 = t; x0 = x; }                                   // (going: start the clock once it's moving)
      if (t0 && (x < X + 6 || t - t0 > 4000)) { t1 = t; x1 = x; break; }
      await sleep(100);
    }
    const v = t1 > t0 && t0 ? (x0 - x1) / ((t1 - t0) / 1000) : 0;
    return v;
  };
  const vz = await chase('a vanilla zombie', null, null);
  console.log(`   (a vanilla zombie: ${vz.toFixed(2)} blocks/s)`);
  for (const [label, make, mount] of [['a Blood Moon horror', 'mobs/blood/zombie', null], ['a Champion', 'mobs/champion/zombie', null],
                                      ['a Blood Moon horror on its Steed', 'mobs/blood/zombie', 'mounts/blood_zombie_horse'],
                                      ['a Champion on its zombie horse', 'mobs/champion/zombie', 'mounts/zombie_horse']]) {
    const v = await chase(label, make, mount);
    ok(`${label} comes at you slower than you can sprint (5.6 blocks/s)`, v > 0.5 && v < 5.3, `${v.toFixed(2)} blocks/s (vanilla zombie ${vz.toFixed(2)})`);
  }
  // ---- the quick kinds: a spider, as a Blood Moon horror and a Champion (a sprint still gets you away)
  let vc = 0;
  for (const [kind, label, make] of [['spider', 'a vanilla spider', null], ['spider', 'a Blood Moon spider', 'mobs/blood/spider'], ['spider', 'a Champion spider', 'mobs/champion/spider'],
                                     ['creeper', 'a vanilla creeper', null], ['creeper', 'a Blood Moon creeper', 'mobs/blood/creeper'], ['creeper', 'a Champion creeper', 'mobs/champion/creeper'],
                                     ['creeper', 'an Elite creeper', 'mobs/elite/creeper']]) {
    await clear();
    await run(`${O}summon minecraft:${kind} ${X + 30.5} ${Y} ${Z + 3.5} {Tags:["t193","bm.seen"],PersistenceRequired:1b,Fuse:32767s}`);
    const Sp = `@e[type=minecraft:${kind},tag=t193,limit=1,${at}]`;
    if (make) await run(`${O}execute as ${Sp} at @s run function bm:${make}`);
    else await run(`${O}attribute ${Sp} minecraft:follow_range base set 40`);          // (the plain one: noticing you from 30 blocks, as the tiered ones do)
    await run(`${O}kill @e[tag=bm.minion,${at}]`); await run(`${O}kill @e[type=!minecraft:${kind},type=!minecraft:player,${at}]`);
    await run(`${O}data merge entity ${Sp} {Fuse:32767s}`);                             // (no blast mid-measure)
    let t0 = 0, x0 = 0, t1 = 0, x1 = 0; const s0 = Date.now();
    while (Date.now() - s0 < 15000) { const x = await xOf(Sp), t = Date.now();
      if (!t0 && x < X + 28) { t0 = t; x0 = x; } if (t0 && (x < X + 6 || t - t0 > 4000)) { t1 = t; x1 = x; break; } await sleep(100); }
    const v = t1 > t0 && t0 ? (x0 - x1) / ((t1 - t0) / 1000) : 0;
    if (!make) { console.log(`   (${label}: ${v.toFixed(2)} blocks/s)`); if (kind === 'creeper') vc = v; }
    else if (kind === 'creeper') ok(`${label} runs at a plain creeper's pace (no speed boost: you can get clear)`, v > 0.5 && v <= vc * 1.12 + 0.15, `${v.toFixed(2)} blocks/s (vanilla ${vc.toFixed(2)})`);
    else ok(`${label} comes at you slower than you can sprint (5.6 blocks/s)`, v > 0.5 && v < 5.3, `${v.toFixed(2)} blocks/s`);
  }
  // ---- a spider Champion and Elite (the unarmored kinds' Speed effect is gone)
  await clear();
  await run(`${O}summon minecraft:spider ${X + 20.5} ${Y} ${Z + 3.5} {Tags:["t193s","bm.seen"]}`);
  await run(`${O}execute as @e[type=minecraft:spider,tag=t193s,${at}] run function bm:mobs/champion/spider`);
  const resE = (s_) => (s_.match(/\{[^{}]*id: "minecraft:resistance"[^{}]*\}/) || [''])[0];
  const eff = await run(`${O}data get entity @e[type=minecraft:spider,tag=t193s,limit=1,${at}] active_effects`);
  ok('an unarmored Champion (a spider): no Speed effect, Resistance I (not II)', !/minecraft:speed/.test(eff) && !!resE(eff) && !/amplifier: [1-9]/.test(resE(eff)), eff.slice(-200));

  // ---- gear: twelve of each, no full Protection sets
  const survey = async (make) => {
    let full = 0, bare = 0, pieces = 0, epf = 0;
    for (let k = 0; k < 12; k++) {
      await clear();
      await run(`${O}summon minecraft:zombie ${X + 20.5} ${Y} ${Z + 3.5} {Tags:["t193g","bm.seen"],NoAI:1b}`);
      await run(`${O}execute as @e[type=minecraft:zombie,tag=t193g,${at}] run function bm:${make}`);
      let lv4 = 0;
      for (const s of ['head', 'chest', 'legs', 'feet']) {
        const o = await run(`${O}data get entity @e[type=minecraft:zombie,tag=t193g,limit=1,${at}] equipment.${s}.components."minecraft:enchantments"."minecraft:protection"`);
        const lv = +((o.match(/(\d+)\s*$/) || [0, 0])[1]); pieces++; epf += lv; if (lv >= 4) lv4++;
        const any = await run(`${O}data get entity @e[type=minecraft:zombie,tag=t193g,limit=1,${at}] equipment.${s}.components."minecraft:enchantments"`);
        if (!/\{/.test(any)) bare++;                                                          // (no enchantments compound at all)
      }
      if (lv4 === 4) full++;
    }
    return { full, bare, pieces, epf: epf / 12 };
  };
  for (const [label, make, cap] of [['Elites', 'mobs/elite/zombie', 6], ['Champions', 'mobs/champion/zombie', 9], ['Blood Moon horrors', 'mobs/blood/zombie', 8]]) {
    const g = await survey(make);
    ok(`${label}: no full Protection sets, some bare pieces, light on average`, g.full === 0 && g.bare >= 1 && g.epf <= cap,
       `full sets ${g.full}, bare ${g.bare}/${g.pieces}, Protection points ${g.epf.toFixed(1)} a mob (was ${label === 'Champions' ? 20 : 16})`);
  }

  await clear(); await run('gamerule doMobSpawning true'); await run('time set 1000'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 8} ${Z - 8} ${X + LEN + 8} ${Z + 14}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
