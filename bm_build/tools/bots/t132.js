// 2.76: Wraithfire Emma (as a regular player, every step a real packet) + the Fence's heist item.
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const EM = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]';
  const show = (tag) => console.log(`   [${tag}] ` + A.buttons().map(b => `${b.label.replace(/[^\x20-\x7e·]/g, '').trim()} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const uuidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async sel => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const has = async iid => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const hp = async sel => +(((await run(`${O}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?\s*$/) || [0, NaN])[1]);
  const model = async part => (await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.emp,tag=bm.ep_${part},limit=1,sort=nearest] item.components."minecraft:item_model"`)).replace(/.*data: /, '');
  const onEmma = async () => /returned 1/.test(await run('execute as TestRat run function bm:p130/carry/on_emma'));
  const X = 13300, Y = 121, Z = 13000;
  const A = await bot('TestRat'); await sleep(2500);
  // ---- the stage: open sky to fly in, a regular player, tough enough to stand among monsters
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
  for (let y = Y; y < Y + 30; y += 6) await run(`${O}fill ${X - 20} ${y} ${Z - 20} ${X + 20} ${y + 5} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  for (const o of ['bm.emwf', 'bm.emst', 'bm.emsty']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players reset TestRat bm.emcd'); await run(`${O}kill @e[type=minecraft:cat,tag=bm.emmapet]`);
  await run('tag TestRat remove bm.emcarried'); await run('tag TestRat remove bm.emsoft');
  await sleep(2000); A.stand(); await sleep(400);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('effect give TestRat minecraft:resistance 600 4 true');

  // ================================================================== 1. Emma, then the heart
  await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon'); A.slot(8); await sleep(300);
  A.use(); await sleep(400); A.release(); await sleep(2500);
  ok('Use the ribbon: Emma comes', !!(await epos(EM)));
  await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 2.5}`); await sleep(1200);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
  let e = await entOf(EM); if (e) A.interact(e.entityId); await sleep(3500);
  ok('Right-click her with the Wraithfire Heart: her Wraithfire Form - soul-blue armour, wings and blade',
     (await sc('TestRat', 'bm.emwf')) === 1 && /tag/.test('tag') && /bm:ew_body/.test(await model('body')) && /bm:ew_wingr/.test(await model('wingr')) && /bm:ew_armr/.test(await model('armr')),
     `emwf ${await sc('TestRat', 'bm.emwf')} body ${await model('body')} wing ${await model('wingr')}`);

  // ================================================================== 2. her menu: the form off and on, the styles
  const menu = async () => { A.slot(8); await sleep(250); A.input({ shift: true }); await sleep(200); const opened = await A.useWait(); A.input({}); await sleep(200); return opened; };
  await menu(); show('her menu');
  const mb = A.buttons();
  ok('Sneak + use the ribbon: her menu has Wraithfire Form on/off, Fly with me, three battle styles',
     ['Wraithfire Form', 'Fly with me', 'Style: Guardian', 'Style: Huntress', 'Style: Tempest'].every(t => mb.some(b => b.label.includes(t))));
  const body = JSON.stringify(A.dialogN[A.dialogN.length - 1] || {});
  ok('...and shows her form, her style and her charge', /Wraithfire Form: /.test(body) && /Battle style: /.test(body) && /Huntress/.test(body) && /Wraithfire charge: /.test(body));
  await A.press(/Wraithfire Form/); await sleep(3500);
  ok('"Wraithfire Form: on / off" - off: she\'s her usual self (not ethereal, her own clothes)',
     (await sc('TestRat', 'bm.emst')) === 0 && (await sc(EM, 'bm.eme')) === 0 && /bm:em_body/.test(await model('body')), `eme ${await sc(EM, 'bm.eme')} body ${await model('body')}`);
  await run('effect clear TestRat minecraft:fire_resistance'); await sleep(3500);
  ok('...no wraithfire blessing while it\'s off', !/fire_resistance/.test(await run('data get entity TestRat active_effects')));
  await menu(); await A.press(/Wraithfire Form/); await sleep(3500);
  ok('...and on again: the Wraithfire Form is back', (await sc('TestRat', 'bm.emst')) === 1 && /bm:ew_body/.test(await model('body')));
  await menu(); const st = await A.press(/Style: Tempest/); await sleep(400);
  ok('Style: Tempest - picked, and the menu says so', !!st && (await sc('TestRat', 'bm.emsty')) === 3 && /Tempest/.test(JSON.stringify(A.dialogN[A.dialogN.length - 1] || {})));
  await A.press(/Style: Huntress/); await sleep(300);
  ok('Style: Huntress - picked', (await sc('TestRat', 'bm.emsty')) === 2);
  A.write('close_window', { windowId: 0 });

  // ================================================================== 3. fighting: reach, the lance, burning
  if (want('fight')) {
    await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 1.5}`);
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 19.5} {NoAI:1b,Tags:["t132a"],PersistenceRequired:1b}`);
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z - 25.5} {NoAI:1b,Tags:["t132b"],PersistenceRequired:1b}`);
    const h0 = await hp('@e[tag=t132a,limit=1]');
    const hit = await wait(5000, async () => (await hp('@e[tag=t132a,limit=1]')) < h0 || !(await epos('@e[tag=t132a,limit=1]')));
    ok('Huntress: she strikes a monster 19 blocks off (her Ethereal Form reached 14) - and it burns', hit, `hp ${h0} -> ${await hp('@e[tag=t132a,limit=1]')}`);
    const hit2 = await wait(5000, async () => (await hp('@e[tag=t132b,limit=1]')) < 20 || !(await epos('@e[tag=t132b,limit=1]')));
    ok('...and her Wraith Lance reaches one 25 blocks off', hit2, `hp ${await hp('@e[tag=t132b,limit=1]')}`);
    await run(`${O}kill @e[tag=t132a]`); await run(`${O}kill @e[tag=t132b]`);
    // your mark: hit one yourself - she goes for it
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 2.6} {NoAI:1b,Tags:["t132m"],PersistenceRequired:1b,Health:80f,attributes:[{id:"minecraft:max_health",base:80d}]}`);
    await sleep(900); const m = await entOf('@e[tag=t132m,limit=1]');
    // (a player swings until it lands - a hit inside the half-second after one of hers doesn't count, as for any mob)
    for (let k = 0; k < 4 && !/bm.emfoc/.test(await run(`${O}data get entity @e[tag=t132m,limit=1] Tags`)); k++) { if (m) A.attack(m.entityId); await sleep(650); }
    ok('Hit a monster yourself: it\'s marked for her', /bm.emfoc/.test(await run(`${O}data get entity @e[tag=t132m,limit=1] Tags`)) &&
       (await sc('@e[tag=t132m,limit=1]', 'bm.emfo')) === (await sc('TestRat', 'bm.pid')), `seen ${!!m} tags ${(await run(`${O}data get entity @e[tag=t132m,limit=1] Tags`)).replace(/.*data: /, '')}`);
    await run(`${O}kill @e[tag=t132m]`);
  }

  // ================================================================== 4. charged attacks
  if (want('charged')) {
    const named = (t) => A.bars.some(b => b.includes(t));
    // a crowd round you: SOUL CYCLONE
    A.bars.length = 0; await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 1.5}`);
    for (let i = 0; i < 5; i++) await run(`${O}summon minecraft:husk ${X + 0.5 + [2, -2, 0, 2, -2][i]} ${Y} ${Z + 0.5 + [2, 2, -2.5, -2, -1][i]} {NoAI:1b,Tags:["t132c"],PersistenceRequired:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`);
    const cy = await wait(20000, async () => named('SOUL CYCLONE'), 300);
    await sleep(3500);
    let hurt = 0; for (let i = 0; i < 5; i++) if ((await hp(`@e[tag=t132c,limit=1,sort=random]`)) < 200) hurt++;
    ok('Charged, with monsters all round you: SOUL CYCLONE - the whirl cuts them all', cy && hurt >= 3, `named ${cy}; hurt ${hurt}/5 | ${A.bars.filter(b => /Emma/.test(b)).slice(-2).join(' / ').slice(0, 160)}`);
    await run(`${O}kill @e[tag=t132c]`);
    // a boss about: FALLING STAR
    A.bars.length = 0;
    await run(`${O}summon minecraft:ravager ${X + 0.5} ${Y} ${Z + 12.5} {NoAI:1b,Tags:["t132r"],PersistenceRequired:1b,Health:300f,attributes:[{id:"minecraft:max_health",base:300d}]}`);
    const fs = await wait(20000, async () => named('FALLING STAR'), 300);
    const r0 = await hp('@e[tag=t132r,limit=1]'); await sleep(2500);
    ok('Charged, with a big one about: FALLING STAR - she dives on it', fs && (await hp('@e[tag=t132r,limit=1]')) <= 300 - 40, `named ${fs}; hp ${r0} -> ${await hp('@e[tag=t132r,limit=1]')}`);
    await run(`${O}kill @e[tag=t132r]`);
    // one out on its own: REQUIEM CRESCENT
    A.bars.length = 0; await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 1.5}`);
    await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 14.5} {NoAI:1b,Tags:["t132q"],PersistenceRequired:1b,Health:300f,attributes:[{id:"minecraft:max_health",base:300d}]}`);
    const rq = await wait(22000, async () => named('REQUIEM CRESCENT'), 300);
    const q0 = await hp('@e[tag=t132q,limit=1]'); await sleep(3000);
    ok('Charged, one foe out ahead: REQUIEM CRESCENT - the wave reaches it', rq && (await hp('@e[tag=t132q,limit=1]')) < q0, `named ${rq}; hp ${q0} -> ${await hp('@e[tag=t132q,limit=1]')}`);
    await run(`${O}kill @e[tag=t132q]`);
  }

  // ================================================================== 5. she carries you: sneak + right-click her empty-handed
  if (want('carry')) {
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 2.0}`); await sleep(1500); A.stand();
    A.slot(3); await sleep(300); e = await entOf(EM);
    A.input({ shift: true }); await sleep(300); if (e) A.interact(e.entityId, true); await sleep(400);
    const notYet = !(await onEmma());
    A.input({}); await sleep(1200);
    const up = await onEmma();
    ok('Sneak + right-click her, empty-handed, and let go of sneak: she wraps her arms round you from behind and lifts you (her axe hand free)',
       up && /bm.emcar/.test(await run(`${O}data get entity ${EM} Tags`)) && /bm:ew_armr_free/.test(await model('armr')), `riding ${up}; arm ${await model('armr')}`);
    if (up) {
      const p0 = await epos(EM); A.ride(0, -45); await sleep(1500);
      const p1 = await epos(EM);
      ok('Look up: you rise', p1 && p1[1] > p0[1] + 2.5, `y ${p0 && p0[1].toFixed(2)} -> ${p1 && p1[1].toFixed(2)}`);
      A.ride(0, 0, { forward: true }); await sleep(1500); const p2 = await epos(EM);
      ok('Walk forward: she flies you that way (yaw 0 = south)', p2 && p2[2] > p1[2] + 6 && Math.abs(p2[1] - p1[1]) < 0.8, `z ${p1[2].toFixed(1)} -> ${p2 && p2[2].toFixed(1)}; y ${p2 && p2[1].toFixed(2)}`);
      A.ride(0, 0, {}); await sleep(400); const p3 = await epos(EM); await sleep(1500); const p4 = await epos(EM);
      ok('Let go of everything: you hover', p4 && Math.abs(p4[1] - p3[1]) < 0.3 && Math.hypot(p4[0] - p3[0], p4[2] - p3[2]) < 0.5, `moved ${p4 && Math.hypot(p4[0] - p3[0], p4[2] - p3[2]).toFixed(2)}; dy ${p4 && (p4[1] - p3[1]).toFixed(2)}`);
      A.ride(0, 60, {}); await sleep(900); const p5 = await epos(EM);
      ok('Look down: you sink', p5 && p5[1] < p4[1] - 1.5, `y ${p4[1].toFixed(2)} -> ${p5 && p5[1].toFixed(2)}`);
      // the lance from the air
      await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 26.5} {NoAI:1b,Tags:["t132f"],PersistenceRequired:1b}`);
      const fl = await wait(5000, async () => (await hp('@e[tag=t132f,limit=1]')) < 20 || !(await epos('@e[tag=t132f,limit=1]')));
      ok('Carrying you, she still fights - her lance strikes from the air', fl, `hp ${await hp('@e[tag=t132f,limit=1]')}`);
      await run(`${O}kill @e[tag=t132f]`);
      // let go up high: you drift down
      A.ride(0, 0, { shift: true }); await sleep(600); A.unride(); A.input({});
      const down = !(await onEmma()); const fx = await run('data get entity TestRat active_effects');
      ok('Sneak: she lets you go - high up, you drift down softly (Slow Falling)', down && /slow_falling/.test(fx), `riding ${!down}; ${fx.slice(0, 120)}`);
      const h0 = await hp('TestRat'); await run('effect clear TestRat minecraft:resistance');
      await wait(15000, async () => /1b/.test(await run('data get entity TestRat OnGround')));
      await sleep(800); const h1 = await hp('TestRat');
      ok('...and land unhurt', h1 >= h0 - 0.01, `health ${h0} -> ${h1}`);
      await run('effect give TestRat minecraft:resistance 600 4 true');
    }
    // her ribbon, used right beside her
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 2.0}`); await sleep(1200); A.stand();
    const diag = `emma ${(await run(`${O}data get entity ${EM} Tags`)).replace(/.*data: /, '')} at ${(await epos(EM) || []).map(v => v.toFixed(1))} xa ${await sc(EM, 'bm.emxa')}`;
    A.slot(8); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(1000);
    const up3 = await onEmma();
    ok('Use her ribbon right beside her: she lifts you too', up3, `${diag} | ${A.bars.slice(-1).join('').slice(0, 100)}`);
    if (up3) { A.ride(0, 0, { shift: true }); await sleep(600); A.unride(); A.input({}); await wait(8000, async () => /1b/.test(await run('data get entity TestRat OnGround'))); }
    // the menu's Fly with me; then the form switched off while she carries you
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1200); A.stand();
    await menu(); const fw = await A.press(/Fly with me/); await sleep(1200);
    const up2 = await onEmma();
    ok('Her menu: "Fly with me" - up you go', !!fw && up2, `riding ${up2}`);
    if (up2) {
      A.ride(0, -45); await sleep(1500); A.ride(0, 0);
      A.unride(); await menu(); A.ride(0, 0); await A.press(/Wraithfire Form/); await sleep(2500); A.unride();
      const fx = await run('data get entity TestRat active_effects');
      ok('Switch her form off while she carries you: she sets you down gently (Slow Falling)', !(await onEmma()) && /slow_falling/.test(fx), fx.slice(0, 100));
      await wait(12000, async () => /1b/.test(await run('data get entity TestRat OnGround')));
      await sleep(600); A.stand();
      ok('Form off: sneak + right-click no longer lifts you (she\'s her usual self)', await (async () => {
        await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 2.0}`); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(900); A.stand();
        const e2 = await entOf(EM); A.input({ shift: true }); await sleep(150); if (e2) A.interact(e2.entityId, true); await sleep(150); A.input({}); await sleep(800);
        return !(await onEmma()); })());
    }
    // the heart back
    await menu(); const tk = await A.press(/Take back the heart/); await sleep(800);
    ok('"Take back the heart": in your pack again', !!tk && (await has('wraithfire_heart')) === 1 && (await sc('TestRat', 'bm.emwf')) === 0);
  }

  // ================================================================== 6. the Fence: the heist item, first on his list - bought for real
  if (want('fence')) {
    const F = '@e[tag=bm.npc_fence,limit=1]';
    const first = (await run(`data get entity ${F} Offers.Recipes[0].sell.components."minecraft:custom_data"`)).replace(/.*data: /, '');
    ok('The Fence\'s first trade is the Fixer\'s Ledger (the current one)', /fixers_ledger/.test(first) && /bmlv: 276/.test(first), first);
    const fp = (await run(`data get entity ${F} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (fp) {
      await run('clear TestRat'); for (let i = 0; i < 3; i++) await run('loot give TestRat loot bm:items/token');
      await run('loot replace entity TestRat hotbar.7 loot bm:items/market_key');      // (a customer: the market lets keyholders in)
      await run(`execute in minecraft:overworld positioned ${fp[1]} ${fp[2]} ${fp[3]} run tp TestRat ^ ^ ^1.5 facing ${fp[1]} ${+fp[2] + 1} ${fp[3]}`);
      await sleep(2500); A.stand();
      const fe = await entOf(F); A.windows.length = 0;
      if (fe) A.interact(fe.entityId); await sleep(1200);
      const w = A.windows[A.windows.length - 1];
      if (w) { A.write('select_trade', { slot: 0 }); await sleep(300);
        A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
        A.write('close_window', { windowId: w.windowId }); }
      const led = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"fixers_ledger"}}}].components."minecraft:custom_data"');
      ok('Trade with him: 3 Tokens buy the Fixer\'s Ledger', !!w && /bmlv: 276/.test(led) && (await has('token')) === 0, `${w ? 'window' : 'no window'} | ${led.replace(/.*data: /, '').slice(0, 80)} | tokens ${await has('token')}`);
      await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
    }
  }
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] run tp @s ~ -400 ~`);
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
