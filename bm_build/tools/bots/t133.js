// 2.76 regression (regular players, real packets): Emma's everyday life after the Wraithfire update - Cecil's harmony,
// fainting, "Send her home" - and the carry's edges: she faints in mid-air, her ribbon is dropped in mid-air, and sending your
// Emma home beside a friend's flying Emma leaves the friend in the air. Every fall is a real client's fall (a move a tick).
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async sel => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const uuidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const hp = async sel => +(((await run(`${O}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?\s*$/) || [0, NaN])[1]);
  const fx = who => run(`data get entity ${who} active_effects`);
  const onEmma = async who => /returned 1/.test(await run(`execute as ${who} run function bm:p130/carry/on_emma`));
  const carryMod = async who => !/no modifier|There is no|not found/i.test(await run(`attribute ${who} minecraft:fall_damage_multiplier modifier value get bm:em_carry`));
  const X = 13400, Y = 121, Z = 13000;
  const A = await bot('TestRat'); await sleep(1500);
  const B = want('mp') ? await bot('TestRat2') : null; await sleep(2500);
  const show = (C, tag) => console.log(`   [${tag}] ` + C.buttons().map(b => `${b.label.replace(/[^\x20-\x7e·]/g, '').trim()} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const pidOf = async who => sc(who, 'bm.pid');
  const emmaOf = async who => `@e[type=minecraft:cat,tag=bm.emmapet,scores={bm.pid=${await pidOf(who)}},limit=1]`;
  const partsOf = async who => cnt(`@e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emencp,scores={bm.pid=${await pidOf(who)}}]`);
  const use = async (C, slot) => { C.slot(slot); await sleep(250); C.use(); await sleep(400); C.release(); };
  const menu = async C => { C.slot(8); await sleep(250); C.input({ shift: true }); await sleep(200); const opened = await C.useWait(); C.input({}); await sleep(200); return opened; };
  // (a real client falls by itself: gravity every tick - gentler under Slow Falling - a move a tick, and says when it lands)
  const fall = async (C, who, floorY) => {
    C.unride(); C.unstand(); C.input({});
    const p = await epos(who); if (!p) return false; C.pos.x = p[0]; C.pos.y = p[1]; C.pos.z = p[2];
    let v = 0;
    for (let k = 0; k < 900 && C.pos.y > floorY; k++) {
      const slow = /slow_falling/.test(await fx(who));
      v = slow ? Math.min((v + 0.01) * 0.98, 0.12) : (v + 0.08) * 0.98;
      C.pos.y = Math.max(floorY, C.pos.y - v);
      C.write('position', { x: C.pos.x, y: C.pos.y, z: C.pos.z, flags: { onGround: C.pos.y <= floorY, hasHorizontalCollision: false } }); C.write('tick_end', {});
      await sleep(50);
    }
    C.stand(); await sleep(600); return true;
  };
  // (sneak + right-click her empty-handed, then let go of sneak)
  const lift = async (C, who, at) => {
    const EMx = await emmaOf(who);
    await run(`${O}tp ${who} ${at[0] + 0.5} ${Y} ${at[1] + 0.5} 0 0`); await run(`${O}tp ${EMx} ${at[0] + 0.5} ${Y} ${at[1] + 2.0}`); await sleep(1500); C.stand();
    C.slot(3); await sleep(300); const e = await entOf(C, EMx);
    C.input({ shift: true }); await sleep(300); if (e) C.interact(e.entityId, true); await sleep(400);
    C.input({}); await sleep(1200);
    const r = await onEmma(who);
    if (!r) console.log(`   [lift failed] ent ${e ? e.entityId : 'none'}; emma ${(await epos(EMx) || []).map(v => v.toFixed(2))} me ${(await epos(who) || []).map(v => v.toFixed(2))}; tags ${(await run(`${O}data get entity ${EMx} Tags`)).replace(/.*data: /, '')}; bars ${C.bars.slice(-3).join(' / ').slice(0, 300)}`);
    return r;
  };
  const stage = async (who) => {
    await run(`${O}tp ${who} ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run(`gamemode survival ${who}`); await run(`clear ${who}`); await run(`effect clear ${who}`);
    for (const o of ['bm.emwf', 'bm.emst', 'bm.emsty']) await run(`scoreboard players set ${who} ${o} 0`);
    await run(`tag ${who} remove bm.emcarried`); await run(`tag ${who} remove bm.emsoft`);
    await run(`attribute ${who} minecraft:fall_damage_multiplier modifier remove bm:em_carry`);
  };

  // ---- the stage: open sky; regular players; no Emma, no Cecil, nothing resting
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
  for (let y = Y; y < Y + 30; y += 6) await run(`${O}fill ${X - 20} ${y} ${Z - 20} ${X + 20} ${y + 5} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.emp]`); await run(`${O}kill @e[type=minecraft:cat,tag=bm.emmapet]`); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.cecilpet]`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  await stage('TestRat'); if (B) await stage('TestRat2');
  await sleep(2500);
  for (const w of ['TestRat', 'TestRat2']) for (const o of ['bm.emcd', 'bm.cpcd', 'bm.cpel']) await run(`scoreboard players reset ${w} ${o}`);
  A.stand(); if (B) B.stand(); await sleep(400);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('effect give TestRat minecraft:resistance 600 4 true');
  let EM = '';

  if (want('life')) {
    // ================================================================== 1. Emma and Cecil: harmony
    await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/cecil_gem');
    await use(A, 8); await sleep(2500); EM = await emmaOf('TestRat');
    ok('Use the ribbon: Emma comes', !!(await epos(EM)));
    await use(A, 7); await sleep(2500);
    const CW = `@e[type=minecraft:wolf,tag=bm.cecilpet,scores={bm.pid=${await pidOf('TestRat')}},limit=1]`;
    ok('Use Cecil\'s gem: Cecil comes', !!(await epos(CW)));
    A.slot(3); await sleep(300);
    const harm = await wait(6000, async () => (await cnt(`@e[type=minecraft:cat,tag=bm.emmapet,tag=bm.harmony]`)) === 1 && (await cnt(`@e[type=minecraft:wolf,tag=bm.cecilpet,tag=bm.harmony]`)) === 1);
    ok('Emma and Cecil out together: their harmony (both tagged)', harm, `emma ${(await run(`${O}data get entity ${EM} Tags`)).replace(/.*data: /, '').slice(0, 120)}`);
    ok('...and Cecil stays with you (his gem in your pack)', !!(await epos(CW)));
    await use(A, 7); await sleep(300); A.input({ shift: true }); await sleep(150); A.use(); await sleep(300); A.release(); A.input({}); await sleep(2500);   // (sneak + use his gem: he goes home)
    await run(`${O}kill @e[type=minecraft:wolf,tag=bm.cecilpet]`); await run('scoreboard players reset TestRat bm.cpcd'); await run('clear TestRat *[minecraft:custom_data~{bm:"cecil_gem"}]');

    // ================================================================== 2. she faints (her ordinary self)
    await sleep(1000);
    const p0 = await partsOf('TestRat');
    await run(`${O}damage ${EM} 1000 minecraft:mob_attack`);                      // (a monster's blow too many)
    const gone = await wait(6000, async () => (await partsOf('TestRat')) === 0);
    const cd = await sc('TestRat', 'bm.emcd');
    ok('She faints: her rig fades away, and her ribbon rests 5 minutes', gone && cd >= 280 && cd <= 300, `parts ${p0} -> ${await partsOf('TestRat')}; emcd ${cd}`);
    await use(A, 8); await sleep(1500);
    ok('...her ribbon refuses meanwhile', !(await epos(EM)));
    await run('scoreboard players reset TestRat bm.emcd');                         // (the stage: the five minutes pass)
    await use(A, 8); await sleep(2500); EM = await emmaOf('TestRat');
    ok('...after the rest she comes again', !!(await epos(EM)));

    // ================================================================== 3. "Send her home" (her ordinary menu)
    await menu(A); show(A, 'her menu');
    const sh = await A.press(/Send her home/); await sleep(2500);
    ok('Her menu: "Send her home" - host and rig gone, no rest', !!sh && !(await epos(EM)) && (await partsOf('TestRat')) === 0 && !((await sc('TestRat', 'bm.emcd')) > 0),
       `pressed ${!!sh}; emma ${!!(await epos(EM))}; parts ${await partsOf('TestRat')}; emcd ${await sc('TestRat', 'bm.emcd')}`);
    await use(A, 8); await sleep(2500); EM = await emmaOf('TestRat');
    ok('...and her ribbon calls her straight back', !!(await epos(EM)));
  }

  if (want('air')) {
    // ================================================================== 4. her Wraithfire Form; she faints in mid-air
    if (!(await has('TestRat', 'emma_ribbon'))) await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon');
    EM = await emmaOf('TestRat');
    if (!(await epos(EM))) { await use(A, 8); await sleep(2500); EM = await emmaOf('TestRat'); }
    await run(`${O}tp ${EM} ${X + 0.5} ${Y} ${Z + 2.5}`); await sleep(1200);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/wraithfire_heart'); A.slot(0); await sleep(300);
    const e = await entOf(A, EM); if (e) A.interact(e.entityId); await sleep(3500);
    ok('Hand her the Wraithfire Heart: her Wraithfire Form', (await sc('TestRat', 'bm.emwf')) === 1 && (await sc('TestRat', 'bm.emst')) === 1);
    const flyHigh = async () => { A.ride(0, -45); await sleep(2200); A.ride(0, 0, {}); await sleep(500); const p = await epos('TestRat'); return p && p[1] > Y + 6 ? p[1] : 0; };
    if (await lift(A, 'TestRat', [X, Z])) {
      const hy = await flyHigh();
      ok('She lifts you and flies you up high', hy > 0, `y ${hy}`);
      await run('effect clear TestRat minecraft:resistance'); const h0 = await hp('TestRat');
      const t0 = Date.now(); await run(`${O}damage ${EM} 1000 minecraft:mob_attack`);
      const freed = await wait(2500, async () => !(await onEmma('TestRat')) && /slow_falling/.test(await fx('TestRat')), 50); const ms = Date.now() - t0;
      ok('She faints in mid-air: you\'re let go at once, with her rig (not a second later), and gently (Slow Falling)', freed && ms < 800, `${ms} ms; riding ${await onEmma('TestRat')}`);
      const fell = await fall(A, 'TestRat', Y);
      const p = await epos('TestRat'); const h1 = await hp('TestRat');
      ok('...you fall all the way down and land unhurt', fell && p && p[1] < Y + 0.5 && h1 >= h0 - 0.01, `y ${p && p[1].toFixed(2)}; health ${h0} -> ${h1}`);
      ok('...and once you\'ve landed, falls hurt as usual again (no lasting fall immunity)', !(await carryMod('TestRat')) && !(await run('tag TestRat list')).includes('bm.emsoft'));
      await run('effect give TestRat minecraft:resistance 600 4 true');
    } else ok('She lifts you (for the mid-air faint)', false, 'no lift');

    // ================================================================== 5. her ribbon dropped in mid-air: she goes home - and lets you go first
    await run('scoreboard players reset TestRat bm.emcd'); await sleep(500);
    await use(A, 8); await sleep(2500); EM = await emmaOf('TestRat');
    ok('Called again after fainting: still in her Wraithfire Form', !!(await epos(EM)) && (await sc('TestRat', 'bm.emwf')) === 1 && (await sc('TestRat', 'bm.emst')) === 1);
    if (await lift(A, 'TestRat', [X, Z])) {
      const hy = await flyHigh();
      await run('effect clear TestRat minecraft:resistance'); const h0 = await hp('TestRat');
      A.slot(8); await sleep(300);
      A.write('block_dig', { status: 4, location: { x: 0, y: 0, z: 0 }, face: 0, sequence: A.seq++ });        // (Q: drop the held item)
      await sleep(500); const dropped = (await has('TestRat', 'emma_ribbon')) === 0;
      await wait(7000, async () => !(await onEmma('TestRat')));                     // (3 seconds out of your pockets, then she goes)
      const off = !(await onEmma('TestRat')); const f = await fx('TestRat');
      ok('Drop her ribbon while she flies you: she goes home - letting you go gently first', dropped && off && !(await epos(EM)) && /slow_falling/.test(f),
         `y ${hy}; dropped ${dropped}; riding ${!off}; emma ${!!(await epos(EM))}; ${f.slice(0, 90)}`);
      const fell = await fall(A, 'TestRat', Y);
      const p = await epos('TestRat'); const h1 = await hp('TestRat');
      ok('...and you land unhurt', fell && p && p[1] < Y + 0.5 && h1 >= h0 - 0.01, `y ${p && p[1].toFixed(2)}; health ${h0} -> ${h1}`);
      await run('effect give TestRat minecraft:resistance 600 4 true');
      await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..40]`);
    } else ok('She lifts you (for the dropped ribbon)', false, 'no lift');
  }

  if (want('mp') && B) {
    // ================================================================== 6. two players: yours sent home, theirs keeps flying
    await run('scoreboard players reset TestRat bm.emcd'); await run('scoreboard players reset TestRat2 bm.emcd');
    for (const who of ['TestRat', 'TestRat2']) { await run(`clear ${who}`); await run(`loot replace entity ${who} hotbar.8 loot bm:items/emma_ribbon`); await run(`effect give ${who} minecraft:resistance 600 4 true`); }
    B.chats.length = 0; B.cmd('gamemode creative'); await sleep(500);
    ok('TestRat2 is a regular player too', /unknown|incomplete/i.test(B.chats.join(' ')));
    if (!(await epos(await emmaOf('TestRat')))) await use(A, 8);
    await run(`${O}tp TestRat2 ${X + 6.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800); B.stand();
    await use(B, 8); await sleep(2500);
    const EB = await emmaOf('TestRat2');
    ok('TestRat2 calls their own Emma', !!(await epos(EB)) && EB !== (await emmaOf('TestRat')));
    await run(`${O}tp ${EB} ${X + 6.5} ${Y} ${Z + 2.5}`); await sleep(1000);
    await run('loot replace entity TestRat2 hotbar.0 loot bm:items/wraithfire_heart'); B.slot(0); await sleep(300);
    const eb = await entOf(B, EB); if (eb) B.interact(eb.entityId); await sleep(3500);
    const up = (await sc('TestRat2', 'bm.emwf')) === 1 && await lift(B, 'TestRat2', [X + 1, Z]);   // (TestRat2 lifts off right beside TestRat)
    B.ride(0, 0, {}); await sleep(800);
    const EA = await emmaOf('TestRat'); const pe = await epos(EB) || [X + 1.5, Y + 1, Z];
    await run(`${O}tp ${EA} ${X - 3.5} ${Y} ${Z + 0.5}`); await run(`${O}tp TestRat ${(pe[0] + 0.6).toFixed(2)} ${Y} ${pe[2].toFixed(2)} 0 0`); await sleep(600); A.stand();   // (right under TestRat2's Emma)
    const pa = await epos('TestRat'), pb = await epos(EB); const dd = pa && pb ? Math.hypot(pa[0] - pb[0], pa[1] - pb[1], pa[2] - pb[2]) : 99;
    ok('TestRat2\'s Emma hovers within 2 blocks of TestRat, carrying TestRat2', up && dd <= 2 && (await onEmma('TestRat2')), `up ${up}; distance ${dd.toFixed(2)}`);
    await menu(A); const sh = await A.press(/Send her home/); await sleep(2500);
    ok('TestRat sends their own Emma home: theirs is gone...', !!sh && !(await epos(EA)));
    ok('...and TestRat2 is still in their Emma\'s arms (not dropped)', await onEmma('TestRat2') && !!(await epos(EB)), `riding ${await onEmma('TestRat2')}`);
    B.ride(0, 0, { shift: true }); await sleep(600); B.unride(); B.input({}); await fall(B, 'TestRat2', Y);
    await run(`${O}kill @e[type=minecraft:cat,tag=bm.emmapet]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.emp]`);
  }

  if (want('ledger')) {
    // ================================================================== 7. the Ledger: Raid Crew -> Outfits & Emma's buff (she isn't out); she arrives on it
    await run(`${O}kill @e[type=minecraft:cat,tag=bm.emmapet]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.emp]`); await sleep(1500);
    await run('scoreboard players reset TestRat bm.emcd'); await run('clear TestRat'); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800); A.stand();
    await run('scoreboard players set TestRat bm.emode 4');                                // (the stage: she's on Healing)
    await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); await run('loot replace entity TestRat hotbar.8 loot bm:items/emma_ribbon');
    A.slot(0); await sleep(300); await A.useWait(); show(A, 'office');
    const rc = await A.press(/Raid Crew/); await sleep(600); show(A, 'raid crew');
    const of = await A.press(/Outfits/); await sleep(600); show(A, 'outfits & buff');
    const offB = A.buttons().find(b => /Offense/.test(b.label));
    const pr = offB ? await A.press(/Offense/) : null; await sleep(700); show(A, 'after Offense');
    ok('Ledger -> Raid Crew -> "Outfits & Emma\'s buff" -> Offense (she isn\'t out): remembered', !!rc && !!of && !!pr && (await sc('TestRat', 'bm.emode')) === 2, `emode ${await sc('TestRat', 'bm.emode')}`);
    const wd = A.buttons().find(b => /Emma/.test(b.label) && /ward|outfit|Emma's/i.test(b.label));
    if (wd) { await A.press(new RegExp(wd.label.replace(/[^\w ]/g, '.').slice(0, 20))); await sleep(700); show(A, 'emma wardrobe (from the ledger)');
      const first = A.buttons()[0]; ok('...Emma\'s wardrobe opens from it, its first button is a way back (not "Send her home")', !!first && !/Send her home/.test(first.label), first && first.label); }
    A.close && A.dialogN.length; A.slot(8); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(2500);
    EM = await emmaOf('TestRat');
    ok('Call her: she arrives on the remembered buff (Offense)', (await sc(EM, 'bm.emm')) === 2, `emm ${await sc(EM, 'bm.emm')}`);
  }

  if (want('cap')) {
    // ================================================================== 8. three followers at most - the fourth is refused (each called with its own item)
    for (const t of ['cat,tag=bm.emmapet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet']) await run(`${O}kill @e[type=minecraft:${t}]`);
    await run(`${O}kill @e[type=minecraft:item_display,tag=bm.emp]`); await sleep(2000);
    for (const o of ['bm.emcd', 'bm.cpcd', 'bm.cpel', 'bm.cecd', 'bm.zbcd']) await run(`scoreboard players reset TestRat ${o}`);
    await run('clear TestRat'); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800); A.stand();
    const kit = [[8, 'emma_ribbon', 'cat', 'bm.emmapet'], [7, 'cecil_gem', 'wolf', 'bm.cecilpet'], [6, 'celi_charm', 'wolf', 'bm.celipet'], [5, 'donadian_medal', 'wolf', 'bm.zibpet']];
    for (const [sl, iid] of kit) await run(`loot replace entity TestRat hotbar.${sl} loot bm:items/${iid}`);
    const mine = async (ty, tag) => cnt(`@e[type=minecraft:${ty},tag=${tag},scores={bm.pid=${await pidOf('TestRat')}}]`);
    for (const [sl] of kit.slice(0, 3)) { await use(A, sl); await sleep(2500); }
    const three = [];
    for (const [, , ty, tag] of kit.slice(0, 3)) three.push(await mine(ty, tag));
    ok('Ribbon, gem, charm: Emma, Cecil and Celi all come', three.every(n => n === 1), three.join(','));
    A.bars.length = 0; await use(A, 5); await sleep(2500);
    ok('A fourth (Zib\'s medal) is refused: "send one home first"', (await mine('wolf', 'bm.zibpet')) === 0 && A.bars.some(b => /Send one home first/.test(b)), A.bars.slice(-1).join('').slice(0, 120));
    for (const t of ['cat,tag=bm.emmapet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet']) await run(`${O}kill @e[type=minecraft:${t}]`);
  }

  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  R.end(); process.exit(0);
})().catch(e => { console.log('ERROR', e && e.stack || e); process.exit(1); });
