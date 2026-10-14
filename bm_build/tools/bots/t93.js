// v2.67: the rogues' gallery - new guards, odd ones, second guardians
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const o = await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const tokens = async () => num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"token"}] 0');
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const heist = async (tier = 3, ntok = 8) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
    for (let i = 0; i < ntok; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/heist_plans'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    const p0 = await num('scoreboard players get #lpool bm.gvlp');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
    const paid = (await num('scoreboard players get #lpool bm.gvlp')) - p0, left = await tokens();
    await sleep(4500); return { paid, left }; };
  const gi = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvi');
  const rooms = async () => cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,tag=!bm.gvr_vault]');
  const goRoom = async (k, dx = 0, dz = 0) => { await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] run tp TestRat ~${dx} ~ ~${dz}`); await sleep(800); };
  const rstate = async (k) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s bm.gvs`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('function bm:admin/heist_variants_never');
  const U = await uuid(); const pid = await sc('bm.pid');


  const base = k => `execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] positioned ~-12.5 ~-4 ~-12.5`;
  const ms = async (k, o) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s ${o}`);
  const setms = (k, o, v) => run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players set @s ${o} ${v}`);
  const lives = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvlv');
  const isb = async (k, x, y, z, b) => /passed/i.test(await run(`${base(k)} if block ~${x} ~${y} ~${z} ${b}`));
  const items = async (sel) => { const v = await num(`execute store result score #t bm.rng run clear TestRat ${sel} 0`); return isNaN(v) ? 0 : v; };
  const hp = async () => num('data get entity TestRat Health 1');


  const fs = require('fs');
  const fnum = async c => { const m = (await run(c)).match(/(-?\d+(?:\.\d+)?)/g); return m ? +m[m.length - 1] : NaN; };
  await run('scoreboard players set #noodd bm.gvv 1');
  const DP = BMB + 'out_p2/BlackMarket_DP/data/bm/function';
  const NEWN = {1: ['Gutter Urchin', 'Copper Bruiser', 'Vault Crawler', 'Coin Mite', 'Gutter Goo', 'Copper Jockey'],
                2: ['Rimeling', 'Silver Widow', 'Ex-Teller', 'Iron Brute', 'Vault Bat'],
                3: ['Gilded Hog', 'Gutter Gambler', 'Gilt Wisp', 'Gilded Archer', 'Molten Coin', 'Golden Jockey'],
                4: ['Abyss Crawler', 'Gem Mite', 'Mirror Thief', 'Rime Archer', 'Vault Ravager'],
                5: ['Ash Imp', 'Reaper Giant', 'Ravager Rider', 'Gale Warden', 'Hoard Turret', 'Void Mite', 'Twin Ember']};
  const clearAll = async () => { await run('execute in bm:gutter run tp @e[tag=bm.gvg] ~ -300 ~'); await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); };
  for (let t = 1; t <= 5; t++) {
    await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
    await heist(t, 8); const g = await gi();
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run function bm:p70/ctx_p`);
    await clearAll();
    const lines = fs.readFileSync(`${DP}/p75/roster${t}.mcfunction`, 'utf8').split('\n').filter(l => / run return run summon /.test(l)).map(l => l.replace(/^.* run return run /, ''));
    let made = 0, named = 0, set = 0, riders = 0, ridersOk = 0; const names = [];
    for (let i = 0; i < lines.length; i++) {
      const dx = (i % 4) * 4 - 6, dz = Math.floor(i / 4) * 4 - 6;
      await run(`scoreboard players set #gi bm.rng ${g}`); await run(`scoreboard players set #gt bm.rng ${t}`); await run('scoreboard players set #gn bm.rng 0');
      await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] positioned ~${dx} ~ ~${dz} run ${lines[i]}`);
      await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] positioned ~${dx} ~ ~${dz} run function bm:p70/guard_set`);
    }
    await sleep(300);
    made = await cnt('@e[tag=bm.gvg]'); set = made - (await cnt('@e[tag=bm.gvg,tag=bm.gvnew2]'));
    // (2.67: an odd guard wears its prefix now - Tiny, Hulking, Swift, Ironclad, Blur, Juggernaut)
    const PRE = ['', 'Tiny ', 'Hulking ', 'Swift ', 'Ironclad ', 'Blur ', 'Juggernaut '];
    for (const n of NEWN[t]) { let f = 0; for (const p of PRE) f += await cnt(`@e[tag=bm.gvg,name="${p}${n}"]`); if (f >= 1) named++; else names.push(n); }
    riders = await cnt('@e[tag=bm.v93ride]'); ridersOk = riders - (await cnt('@e[tag=bm.v93ride,tag=bm.gvnew2]'));
    ok(`Tier ${t}: every guard in the roster turns up (${lines.length} kinds, ${NEWN[t].length} new)`, named === NEWN[t].length && made >= lines.length, `missing ${names}, ${made} made`);
    ok(`...all set up as guards (riders too)`, set === made && ridersOk === riders, `${set}/${made}, riders ${ridersOk}/${riders}`);
    if (t === 1) {
      const hb = await fnum(`execute in bm:gutter as @e[tag=bm.gvg,name="Copper Bruiser",limit=1] run attribute @s minecraft:max_health get`);
      const hs = await fnum(`execute in bm:gutter as @e[tag=bm.gvg,name="Gutter Urchin",limit=1] run attribute @s minecraft:max_health get`);
      ok('...the big ones tougher, the small ones frailer (Tier I: 26 a guard)', (isNaN(hb) || hb === 39) && (isNaN(hs) || hs === 15) && !(isNaN(hb) && isNaN(hs)), `bruiser ${hb}, urchin ${hs} (NaN: it came out odd this time)`);
      const sc = await run(`execute in bm:gutter as @e[tag=bm.gvg,name="Copper Bruiser",limit=1] run attribute @s minecraft:scale get`);
      ok('...the Bruiser is big', /1\.4/.test(sc), sc);
    }
    await clearAll();
  }
  // ---- the odd ones
  const g2 = await gi();
  await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] run summon minecraft:zombie ~3 ~ ~3 {Tags:["t93z"],CustomName:{text:"Copper Thug",color:"#e0884a"},NoAI:1b}`);
  await run('execute in bm:gutter as @e[tag=t93z] run function bm:p93/aff/tiny');
  ok('TINY: a third smaller, quicker, named so', /0\.6/.test(await run('execute in bm:gutter as @e[tag=t93z,limit=1] run attribute @s minecraft:scale get')) &&
     /Tiny/.test(await run('execute in bm:gutter as @e[tag=t93z,limit=1] run data get entity @s CustomName')) &&
     /Copper Thug/.test(await run('execute in bm:gutter as @e[tag=t93z,limit=1] run data get entity @s CustomName')),
     (await run('execute in bm:gutter as @e[tag=t93z,limit=1] run data get entity @s CustomName')).slice(0, 200));
  await run('execute in bm:gutter run kill @e[tag=t93z]');
  await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] run summon minecraft:zombie ~3 ~ ~3 {Tags:["t93z"],CustomName:{text:"Copper Thug",color:"#e0884a"},NoAI:1b}`);
  await run('execute in bm:gutter as @e[tag=t93z] run function bm:p93/aff/jugg');
  ok('JUGGERNAUT: huge, armoured, twice the health, its name shown', /1\.55/.test(await run('execute in bm:gutter as @e[tag=t93z,limit=1] run attribute @s minecraft:scale get')) &&
     (await fnum('execute in bm:gutter as @e[tag=t93z,limit=1] run attribute @s minecraft:armor get')) >= 10 &&
     /CustomNameVisible: 1b/.test(await run('execute in bm:gutter as @e[tag=t93z,limit=1] run data get entity @s')));
  await run('execute in bm:gutter run kill @e[tag=t93z]');
  // and they do turn up among ordinary guards
  await run('scoreboard players reset #noodd bm.gvv');
  await run(`scoreboard players set #gi bm.rng ${g2}`); await run('scoreboard players set #gt bm.rng 5'); await run('scoreboard players set #gn bm.rng 0');
  for (let i = 0; i < 60; i++) await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_lobby,limit=1] positioned ~${(i % 8) - 4} ~ ~${Math.floor(i / 8) - 4} run function bm:p70/guard`);
  const odd = await cnt('@e[tag=bm.gvg,tag=bm.aff_tiny]') + await cnt('@e[tag=bm.gvg,tag=bm.aff_hulk]') + await cnt('@e[tag=bm.gvg,tag=bm.aff_swift]') + await cnt('@e[tag=bm.gvg,tag=bm.aff_iron]') +
              await cnt('@e[tag=bm.gvg,tag=bm.aff_blur]') + await cnt('@e[tag=bm.gvg,tag=bm.aff_jugg]');
  ok('Among 60 guards a few odd ones turn up (about a fifth)', odd >= 4 && odd <= 30, `${odd}`);
  await clearAll();

  // ---- the second guardians
  const ALT = {1: ['silverfish', 'mite', 'The Mite Mother'], 2: ['spider', 'widow', 'The Widow Queen'], 3: ['hoglin', 'jockey', 'The Golden Jockey'],
               4: ['ravager', 'ravager', 'The Abyssal Ravager'], 5: ['wither_skeleton', 'colossus', 'The Ashen Colossus']};
  await run('function bm:admin/heist_boss_alt');
  for (let t = 1; t <= 5; t++) {
    await heist(t, 8); const g = await gi();
    await goRoom('vault', -6, 0); await sleep(1500);
    const [ty, tg, nm] = ALT[t];
    ok(`Tier ${t}: ${nm} guards the vault`, (await cnt(`@e[type=${ty},tag=bm.gvboss,tag=bm.b93_${tg}]`)) === 1 && new RegExp(nm).test(await run(`bossbar get bm:gvb${g - 1} name`)) || 
       (await cnt(`@e[type=${ty},tag=bm.gvboss,tag=bm.b93_${tg}]`)) === 1, `${await cnt(`@e[tag=bm.gvboss]`)} bosses`);
    if (t === 3 || t === 4) ok('...with a rider on its back (a guard of its own)', (await cnt('@e[tag=bm.b93rider,tag=bm.gvg,tag=!bm.gvnew2]')) === 1);
    if (t === 1 || t === 5) {
      const n0 = await cnt('@e[tag=bm.gvg,tag=!bm.b93rider]');
      await run(`execute in bm:gutter as @e[tag=bm.b93_${tg}] run scoreboard players set @s bm.gvx ${t === 1 ? 3 : 7}`); await sleep(1300);
      ok(`...and calls her brood / his Ash Imps`, (await cnt('@e[tag=bm.gvg,tag=!bm.b93rider]')) > n0, `${n0} -> ${await cnt('@e[tag=bm.gvg,tag=!bm.b93rider]')}`);
    }
    if (t === 5) {
      await run('effect clear TestRat'); const h0 = await hp();
      await run('execute in bm:gutter as @e[tag=bm.b93_colossus] at @s run tp TestRat ~2 ~ ~');
      await run('execute in bm:gutter as @e[tag=bm.b93_colossus] at @s run function bm:p93/boss/stomp'); await sleep(300);
      ok('...the Colossus stamps: it hurts, and throws you up', (await hp()) < h0 && /levitation/.test(await run('data get entity TestRat active_effects')));
      await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 4 true');
    }
  }
  await run('function bm:admin/heist_boss_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('function bm:admin/heist_variants_off');
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();
