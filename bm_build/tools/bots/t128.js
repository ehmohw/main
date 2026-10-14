// 2.76: the Wraithfire Heart - Pearlman's fusion, carried, the hearth, Cecil / KillerWatt / Emma - by real clicks where a player would click
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const A = await bot('TestRat'); await sleep(2500);
  const O = 'execute in minecraft:overworld run ';
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const near = (p, r = 0.7, skip = []) => { let best = null, bd = 1e9; for (const e of Object.values(A.ents)) { if (skip.includes(e.entityId)) continue;
    const d = (e.x - p[0]) ** 2 + (e.y - p[1]) ** 2 + (e.z - p[2]) ** 2; if (d < bd) { bd = d; best = e; } } return bd < r * r ? best : null; };
  const uuidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entByUuid = u => Object.values(A.ents).find(e => e.objectUUID === u);
  const count = async sel => { const m = (await run(`${O}execute if entity ${sel}`)).match(/Count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`));
  const X = 14000, Y = 121, Z = 14000;
  const reset = async () => {
    await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`);
    await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 5} ${Z + 12} minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
  };
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 80} ${Z - 80} ${X + 80} ${Z + 80}`);
  await reset(); await sleep(2000);
  await run(`${O}kill @e[type=minecraft:zombie,x=${X},y=${Y},z=${Z},distance=..90]`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.wfh]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.wfhd]`);

  if (want('pearl')) {   // 1. Pearlman: the fusion, every visit
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
    await run(`execute in minecraft:overworld positioned ${X + 3.5} ${Y} ${Z + 0.5} run function bm:p60/pm/spawn`); await sleep(300);
    await sleep(400);
    const rec = async (i, k) => (await run(`${O}data get entity @e[type=minecraft:villager,tag=bm.pearl,limit=1] Offers.Recipes[${i}].${k}.components."minecraft:custom_data".bm`)).replace(/.*data: /, '');
    let n = 0; for (let i = 0; i < 3; i++) if (/gem_/.test(await rec(i, 'sell'))) n++;
    const offers = [await rec(3, 'buy'), await rec(3, 'buyB'), await rec(3, 'sell')].join(' ');
    ok('Pearlman stocks his three gems and the fusion (Scorching Heart + Ethereal Gem -> Wraithfire Heart)',
       /scorching_heart.*ethereal_gem.*wraithfire_heart/.test(offers) && n === 3, `gems ${n}; ${offers}`);
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
  }

  if (want('carry')) {   // 2. carried
    await run('clear TestRat'); await run('effect clear TestRat');
    await run('loot replace entity TestRat inventory.5 loot bm:items/wraithfire_heart'); await sleep(1600);
    ok('Carried in the pack: Fire Resistance', /fire_resistance/.test(await run('data get entity TestRat active_effects')));
    await run(`${O}summon minecraft:husk ${X + 2.5} ${Y} ${Z + 0.5} {Tags:["t128z"],NoAI:1b,PersistenceRequired:1b}`); await sleep(1600);
    const f = await run(`${O}data get entity @e[type=minecraft:husk,tag=t128z,limit=1] Fire`);
    ok('Carried: a monster 2 blocks away catches soul fire', /data: ([1-9]\d*)s/.test(f), f.slice(-30));
    await run(`${O}kill @e[type=minecraft:husk,tag=t128z]`);
    await run(`${O}summon minecraft:husk ${X + 9.5} ${Y} ${Z + 0.5} {Tags:["t128z"],NoAI:1b,PersistenceRequired:1b}`); await sleep(1600);
    const f2 = await run(`${O}data get entity @e[type=minecraft:husk,tag=t128z,limit=1] Fire`);
    ok('...one 9 blocks away doesn\'t', !/data: ([1-9]\d*)s/.test(f2), f2.slice(-30));
    await run(`${O}kill @e[type=minecraft:husk,tag=t128z]`);
  }

  if (want('hearth')) {  // 3. set down: the Wraithfire Hearth
    await reset(); await run('clear TestRat'); await sleep(500);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 75`); await sleep(700);
    A.input({ shift: true }); await sleep(400); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(600);
    console.log('bars:', A.bars.slice(-4).join(' | ').slice(0, 300));
    const placed = await count(`@e[type=minecraft:interaction,tag=bm.wfh,x=${X},y=${Y},z=${Z},distance=..4]`);
    ok('Sneak + use on the block: the Wraithfire Hearth is set down, and the heart leaves your hand', placed === 1 && !(await has('wraithfire_heart')), `hearths ${placed}`);
    const hp = await epos(`@e[type=minecraft:interaction,tag=bm.wfh,limit=1]`);
    // a stray (despawnable) monster 40 blocks off is snuffed out; one with a name isn't; one within 16 burns
    await run(`${O}summon minecraft:zombie ${X + 40.5} ${Y} ${Z + 0.5} {Tags:["t128s"],NoAI:1b}`);
    await run(`${O}summon minecraft:zombie ${X + 40.5} ${Y} ${Z + 3.5} {Tags:["t128n"],NoAI:1b,CustomName:"Bob"}`);
    await run(`${O}summon minecraft:zombie ${X + 7.5} ${Y} ${Z + 0.5} {Tags:["t128p"],NoAI:1b,PersistenceRequired:1b,CustomName:"Near"}`);
    await sleep(2600);
    ok('No monster spawns within 64: a stray 40 blocks off is snuffed out', (await count('@e[type=minecraft:zombie,tag=t128s]')) === 0);
    ok('...a named one is left be', (await count('@e[type=minecraft:zombie,tag=t128n]')) === 1);
    const h = await run(`${O}data get entity @e[type=minecraft:zombie,tag=t128p,limit=1] Health`);
    ok('A monster within 16 burns blue and is worn down', /data: (1?\d(\.\d+)?)f/.test(h) && parseFloat(h.match(/data: ([\d.]+)f/)[1]) < 20, h.slice(-20));
    await run(`${O}kill @e[type=minecraft:zombie,tag=t128n]`); await run(`${O}kill @e[type=minecraft:zombie,tag=t128p]`);
    // sneak + punch it: back in your hand
    let ent = hp && near(hp, 0.3);
    const all = hp ? Object.values(A.ents).filter(e => (e.x - hp[0]) ** 2 + (e.y - hp[1]) ** 2 + (e.z - hp[2]) ** 2 < 0.2) : [];
    A.input({ shift: true }); await sleep(300);
    for (const e of all) { A.attack(e.entityId); await sleep(150); }
    await sleep(500); A.input({}); await sleep(300);
    ok('Sneak + punch it: the heart comes back, the hearth is gone', (await has('wraithfire_heart')) && (await count('@e[type=minecraft:interaction,tag=bm.wfh]')) === 0,
       `ents near ${all.length}`);
  }

  // the followers: stand them right in front, click them
  const clickPet = async (sel, shift = false) => {
    const p = await epos(sel); if (!p) return 'no pet';
    await run(`${O}tp ${sel} ${X + 0.5} ${Y} ${Z + 2.5}`); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(900);
    const e = entByUuid(await uuidOf(sel));
    if (!e) return 'no entity seen';
    if (shift) { A.input({ shift: true }); await sleep(250); }
    A.interact(e.entityId, shift); await sleep(700);
    if (shift) { A.input({}); await sleep(200); }
    return 'clicked';
  };
  if (want('cecil')) {   // 4. Cecil
    await reset(); await run('clear TestRat'); await run('scoreboard players set TestRat bm.cpel 0'); await run('scoreboard players reset TestRat bm.cpcd');
    await run(`${O}kill @e[type=minecraft:wolf,tag=bm.cecilpet]`); await sleep(300);
    await run('loot replace entity TestRat hotbar.7 loot bm:items/cecil_gem');
    await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
    const c1 = await clickPet('@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]');
    await sleep(600);
    const body = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.cp_body,limit=1] item.components."minecraft:item_model"`);
    ok('Right-click Cecil with the heart: his Wraithfire Form (bm.cpel 11, wraith robe), the heart taken', (await sc('TestRat', 'bm.cpel')) === 11 && /cec2_body_wraith/.test(body) && !(await has('wraithfire_heart')),
       `${c1} cpel ${await sc('TestRat', 'bm.cpel')} ${body.slice(-30)}`);
    await run(`${O}summon minecraft:husk ${X + 4.5} ${Y} ${Z + 3.5} {Tags:["t128c"],PersistenceRequired:1b,NoAI:1b}`); await sleep(3500);
    const zf = await run(`${O}data get entity @e[type=minecraft:husk,tag=t128c,limit=1] Fire`); const zh = await run(`${O}data get entity @e[type=minecraft:husk,tag=t128c,limit=1] Health`);
    const zalive = await count('@e[type=minecraft:husk,tag=t128c]');
    ok('His soul-fire bolts: a husk near him is burnt and hurt (or already dead)', zalive === 0 || (/data: [1-9]\d*s/.test(zf) && parseFloat((zh.match(/data: ([\d.]+)f/) || [0, 20])[1]) < 20), `${zf.slice(-12)} ${zh.slice(-12)}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=t128c]`);
    // an Ethereal Gem swaps him back - and gives the heart back
    await run('item replace entity TestRat hotbar.0 with minecraft:air'); await run('clear TestRat *[minecraft:custom_data~{bm:"wraithfire_heart"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ethereal_gem'); A.slot(0); await sleep(300);
    await run('scoreboard players set TestRat bm.cpck 0'); await sleep(600);
    await clickPet('@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]'); await sleep(500);
    ok('An Ethereal Gem in its place: his Ethereal Form - and the heart back in your hands', (await sc('TestRat', 'bm.cpel')) === 10 && (await has('wraithfire_heart')));
    // and back to wraith, then sneak + right-click empty-handed: take it back
    await run('item replace entity TestRat hotbar.0 with minecraft:air'); await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(1700);
    await clickPet('@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]'); await sleep(500);
    const back = (await sc('TestRat', 'bm.cpel')) === 11 && await has('ethereal_gem');
    await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"wraithfire_heart"}]'); A.slot(4); await sleep(1700);
    const c4 = await clickPet('@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]', true); await sleep(500);
    ok('...the heart again (the Ethereal Gem back), then sneak + right-click empty-handed: the heart back, his own poison', back && (await sc('TestRat', 'bm.cpel')) === 0 && (await has('wraithfire_heart')),
       `back ${back} ${c4} cpel ${await sc('TestRat', 'bm.cpel')} bars ${A.bars.slice(-2).join(' / ').slice(0, 160)}`);
    await run(`${O}execute as @e[type=minecraft:wolf,tag=bm.cecilpet] run tp @s ~ -400 ~`);
  }

  if (want('kw')) {      // 5. KillerWatt
    await reset(); await run('clear TestRat'); await run('scoreboard players set TestRat bm.kxel 0'); await run('scoreboard players reset TestRat bm.kxcd');
    await run(`${O}execute as @e[type=minecraft:wolf,tag=bm.kxpet] run tp @s ~ -400 ~`); await sleep(300);
    await run('loot replace entity TestRat hotbar.7 loot bm:items/kw_spark');
    await run('execute as TestRat at @s run function bm:p79/pet/summon'); await sleep(2000);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
    const k1 = await clickPet('@e[type=minecraft:wolf,tag=bm.kxpet,limit=1]'); await sleep(800);
    const kb = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.kxp_body,tag=bm.kxp_pet,limit=1] item.components."minecraft:item_model"`);
    ok('Right-click KillerWatt with the heart: his Wraithfire Form (bm.kxel 11, the wraith hide), the heart taken',
       (await sc('TestRat', 'bm.kxel')) === 11 && /kw_body_wf/.test(kb) && !(await has('wraithfire_heart')), `${k1} kxel ${await sc('TestRat', 'bm.kxel')} ${kb.slice(-24)}`);
    await run('item replace entity TestRat hotbar.0 with minecraft:air'); A.slot(1); await sleep(1700);
    await clickPet('@e[type=minecraft:wolf,tag=bm.kxpet,limit=1]', true); await sleep(600);
    ok('Sneak + right-click him empty-handed: the heart back, his own lightning', (await sc('TestRat', 'bm.kxel')) === 0 && (await has('wraithfire_heart')));
    await run(`${O}execute as @e[type=minecraft:wolf,tag=bm.kxpet] run tp @s ~ -400 ~`);
  }

  if (want('emma')) {    // 6. Emma
    await reset(); await run('clear TestRat'); await run('effect clear TestRat'); await run('scoreboard players set TestRat bm.emwf 0'); await run('scoreboard players set TestRat bm.emst 0');
    await run('scoreboard players reset TestRat bm.emcd'); await run(`${O}kill @e[type=minecraft:cat,tag=bm.emmapet]`); await sleep(300);
    await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon');
    await run('execute as TestRat at @s run function bm:p57/summon'); await sleep(1500);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
    const e1 = await clickPet('@e[type=minecraft:cat,tag=bm.emmapet,limit=1]'); await sleep(2600);
    const eme = await sc('@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', 'bm.eme');
    ok('Right-click Emma with the heart: she keeps it and stays ethereal', (await sc('TestRat', 'bm.emwf')) === 1 && (await sc('TestRat', 'bm.emst')) === 1 && eme >= 1 && !(await has('wraithfire_heart')),
       `${e1} emwf ${await sc('TestRat', 'bm.emwf')} eme ${eme}`);
    await run('effect clear TestRat'); await sleep(3500);
    const fx = await run('data get entity TestRat active_effects');
    ok('...and blesses you: Fire Resistance and Regeneration', /fire_resistance/.test(fx) && /regeneration/.test(fx), fx.slice(0, 160));
    await run(`${O}scoreboard players set @e[type=minecraft:cat,tag=bm.emmapet] bm.eme 3`); await sleep(5000);
    ok('Her Ethereal Form doesn\'t run out while she stays (it was about to)', (await sc('@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', 'bm.eme')) >= 20);
    // her menu: stay ethereal off, then take the heart back (real triggers)
    A.slot(8); await sleep(300); A.input({ shift: true }); await sleep(250); A.use(); await sleep(400); A.release(); A.input({}); await sleep(500);
    ok('Sneak + use the ribbon: her menu', (await sc('TestRat', 'bm.menu')) === 960, `menu ${await sc('TestRat', 'bm.menu')}`);
    A.cmd('trigger bm.act set 7307'); await sleep(2500);
    ok('Stay ethereal: off - she comes back down', (await sc('TestRat', 'bm.emst')) === 0 && (await sc('@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', 'bm.eme')) === 0);
    A.cmd('trigger bm.act set 7308'); await sleep(800);
    ok('Take back the heart: in your pack, and she no longer has it', (await sc('TestRat', 'bm.emwf')) === 0 && (await has('wraithfire_heart')));
    await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] run tp @s ~ -400 ~`);
  }

  await run(`${O}forceload remove ${X - 80} ${Z - 80} ${X + 80} ${Z + 80}`);
  console.log(A.chats.slice(-6).join(' | ').slice(0, 600));
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
