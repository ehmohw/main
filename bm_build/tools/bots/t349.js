// 3.0g: THE RAT KING CROWNED, THE GEMS OUT OF THE SHOP, FORMS THROUGH THE DOOR - as a regular player (rcon sets the stage).
//  shop     Goldtooth (the heist's shop, in the den) sells no elemental gems any more; TestRat opens his trades.
//  forms    Cecil's Ethereal form, KillerWatt's Wraithfire and Apophiss's Ethereal, given outside, come into the heist with TestRat
//           and out again; a gem Cecil was given in the lobby before 3.0g comes back to TestRat as the gem.
//  ratking  THE RAT KING in a heist's Champion's Pit (its own summon): his rig (13 parts) on an invisible host; frozen while he comes
//           out of the dark, then free; he waddles and idles (his parts move); in reach, his sceptre comes down on TestRat (his
//           own blow - the zombie's swing does nothing); THE ROYAL DECREE (a shockwave and Plague Rats); he flinches when TestRat
//           hits him; brought down by TestRat he dies on his timeline - his rig goes with him, and the crew's Rat King find is in.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
const want = (k) => !process.argv[2] || process.argv[2].split(',').includes(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  ok('TestRat is a regular player (no operator commands)', await new Promise(r => { const n0 = A.chats.length; A.cmd('gamemode creative');
    setTimeout(() => r(A.chats.slice(n0).some(c => /unknown or incomplete|Unknown command/i.test(c))), 1200); }));
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  const G = 'execute in bm:gutter run ';
  const sc = (o) => num(`scoreboard players get TestRat ${o}`);
  const eidOf = async (sel, pre = G) => { const m = (await run(`${pre}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };

  if (want('shop') || want('forms')) {
    // (forms given outside, as Cecil, KillerWatt and Apophiss keep them; a lobby gem of Cecil's from before 3.0g)
    for (const [o, v] of [['bm.cpel', 10], ['bm.kxel', 11], ['bm.apel', 10], ['bm.cpell', 3], ['bm.vgcl', 0], ['bm.kxell', 0], ['bm.apell', 0]]) await run(`scoreboard players set TestRat ${o} ${v}`);
    await run('tag TestRat remove bm.gem3g'); await run('tag TestRat remove bm.gemlob');
    await heist('levers', 'a', 1); await sleep(1500);
    if (want('forms')) {
      ok('Into the heist: Cecil\'s Ethereal form comes too', (await sc('bm.cpel')) === 10, `${await sc('bm.cpel')}`);
      ok('...KillerWatt\'s Wraithfire form', (await sc('bm.kxel')) === 11, `${await sc('bm.kxel')}`);
      ok('...Apophiss\'s Ethereal form', (await sc('bm.apel')) === 10, `${await sc('bm.apel')}`);
      ok('...and the gem Cecil wore in the lobby before comes back to TestRat as the gem', (await num('clear TestRat *[minecraft:custom_data~{bm:"gem_poison"}] 0')) === 1 &&
         (await sc('bm.cpell')) <= 0);
    }
    if (want('shop')) {
      const GT = '@e[type=minecraft:villager,tag=bm.gvgt,limit=1,sort=nearest]';
      await run(`execute in bm:gutter at ${GT.replace(',sort=nearest', '')} run tp TestRat ^ ^ ^1.5 facing entity @e[type=minecraft:villager,tag=bm.gvgt,limit=1,sort=nearest] eyes`); await sleep(800);
      const offers = await run(`execute at TestRat run data get entity ${GT} Offers.Recipes`);
      ok('The heist shop (Goldtooth) sells no elemental gems', !/gem_(fire|water|poison|earth|electric|rock|air|grass|ice)/.test(offers) && !/bm_vault/.test(offers), offers.slice(0, 120));
      ok('...and still sells the rest (the wardrobe, the contracts)', /cos_outfit_|fcontract_/.test(offers));
      const id = await eidOf(GT, 'execute at TestRat run '); const w0 = A.windows.length;
      if (id) A.interact(id); await sleep(1000);
      ok('...TestRat opens his trades', id && A.windows.length > w0);
      if (A.windows.length > w0) A.close(A.windows[A.windows.length - 1].windowId);
    }
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2500);
    if (want('forms')) ok('Home again: the forms are still theirs', (await sc('bm.cpel')) === 10 && (await sc('bm.kxel')) === 11 && (await sc('bm.apel')) === 10,
                          `${await sc('bm.cpel')} ${await sc('bm.kxel')} ${await sc('bm.apel')}`);
    for (const o of ['bm.cpel', 'bm.kxel', 'bm.apel']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"gem_poison"}]');
  }

  if (want('ratking')) {
    await heist('pit', 'a', 2); await begin();
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const PIT = `@e[type=minecraft:marker,tag=bm.gvr_pit,scores={bm.gvi=${GI}},limit=1]`;
    const K = '@e[type=minecraft:zombie,tag=bm.gvratking,distance=0..,limit=1]';
    const tags = () => run(`${G}data get entity ${K} Tags`);
    const parts = () => cnt('@e[type=minecraft:item_display,tag=bm.rkr,distance=0..]');
    ok('A heist with a Champion\'s Pit', (await cnt(PIT)) === 1);
    await run(`scoreboard players set #gi bm.rng ${GI}`); await run('function bm:p70/ctx');
    await run(`${G}execute as ${PIT} at @s positioned ${rel(12, 4, 12)} run function bm:p76/champ/ratking`);
    await run(`${G}scoreboard players set ${PIT} bm.gvs 1`); await run(`${G}scoreboard players set ${PIT} bm.gvtm 0`);
    ok('THE RAT KING enters the pit: an invisible host and his rig, 13 parts', (await cnt(K)) === 1 && (await parts()) === 13, `${await parts()} parts`);
    ok('...no little rat model any more', (await cnt('@e[type=minecraft:item_display,tag=bm.gvrkd,distance=0..]')) === 0);
    ok('...frozen while he comes out of the dark', /bm\.carr/.test(await tags()) && /bm\.cfrz/.test(await tags()));
    await run('effect clear TestRat'); await run('effect give TestRat instant_health 1 4'); await run('effect give TestRat resistance 900 1 true');
    await run(`${G}execute as ${PIT} at @s run tp TestRat ${rel(4, 4, 12)} -90 0`);
    ok('...then free, armed (his health past its buffer)', await wait(5000, async () => !/bm\.cfrz/.test(await tags()) && /bm\.carm/.test(await tags())));
    const tf = () => run(`${G}data get entity @e[type=minecraft:item_display,tag=bm.rkr_legr,distance=0..,limit=1] transformation.left_rotation`);
    const t0 = await tf(); await sleep(1500); const t1 = await tf();
    ok('He moves: his rig is posed, not a statue', t0 !== t1, `${t0.slice(-40)} / ${t1.slice(-40)}`);
    ok('...his own swing is off (the zombie does no damage), his sceptre carries it', (await num(`${G}attribute ${K} minecraft:attack_damage base get`)) === 0 &&
       (await num(`${G}scoreboard players get ${K} bm.rkd`)) >= 5);
    // in reach: the sceptre
    await run('effect give TestRat instant_health 1 4'); await sleep(300); const hp0 = A.health;
    await run(`${G}execute at ${K} run tp TestRat ^ ^ ^1.6 facing entity ${K} eyes`);
    ok('In his reach: the sceptre comes down on TestRat', await wait(4000, async () => (await num(`${G}scoreboard players get ${K} bm.rks`)) === 1) &&
       await wait(2500, async () => A.health < hp0), `health ${hp0} -> ${A.health}`);
    // THE ROYAL DECREE
    await run('effect give TestRat instant_health 1 4'); A.bars.length = 0;
    await run(`${G}scoreboard players set ${K} bm.rkc 170`); await run(`${G}scoreboard players set ${K} bm.rka 0`);
    await run(`${G}execute at ${K} run tp TestRat ^ ^ ^5 facing entity ${K} eyes`);
    ok('THE ROYAL DECREE: he rears up (TestRat is warned)', await wait(3000, async () => A.bars.some(b => /ROYAL DECREE/.test(b))));
    ok('...the sceptre slammed down: Plague Rats out of the dark', await wait(4000, async () => (await cnt('@e[type=minecraft:silverfish,distance=0..,nbt={CustomName:{text:"Plague Rat"}}]')) +
       (await cnt('@e[type=minecraft:silverfish,tag=bm.gvg,distance=0..]')) >= 1));
    await run(`${G}kill @e[type=minecraft:silverfish,distance=0..]`);
    // hurt, then brought down
    await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword'); A.slot(0);
    await wait(4000, async () => (await num(`${G}scoreboard players get ${K} bm.rks`)) === 0);
    await run(`${G}scoreboard players set ${K} bm.rka -200`); await run(`${G}scoreboard players set ${K} bm.rkc -400`);
    await run(`${G}execute at ${K} run tp TestRat ^ ^ ^2.4 facing entity ${K} eyes`); await sleep(500);
    const id = await (async () => { for (let i = 0; i < 10; i++) { const e = await eidOf(K); if (e) return e; await sleep(200); } return null; })();
    A.attack(id);
    ok('TestRat strikes him: he flinches', await wait(1500, async () => (await num(`${G}scoreboard players get ${K} bm.rks`)) === 3, 50));
    const buf = await num(`${G}scoreboard players get ${K} bm.cbuf`);
    await run(`${G}data merge entity ${K} {Health:${buf + 3}f}`); await sleep(900);
    let dying = false;
    for (let i = 0; i < 6 && !dying; i++) { A.attack(id); await sleep(700); dying = /bm\.cdie/.test(await tags()); }
    ok('...and brings him down: he dies on his timeline (staggers, topples)', dying);
    ok('...his rig goes with him, and he\'s gone', await wait(5000, async () => (await cnt(K)) === 0) && await wait(2500, async () => (await parts()) === 0));
    const pid = await num('scoreboard players get TestRat bm.pid');
    ok('...the crew\'s Rat King find is in TestRat\'s haul', /p76\/ratking/.test(await run(`data get storage bm:gv pot.p${pid}`)));
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('clear TestRat');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
