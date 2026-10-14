// 2.77: Apophiss, as a regular (non-op) player - the serpent seal in the Hollow throne room (a conqueror; Emma, Leo and Cecil
// called with their own items, one by one: the seal stirs, then breaks), the den, the fight (both phases, his attacks seen
// landing), the bot's own blows through his hitbox, the win and its drops, the pad back up; then the Serpent's Oath: his rig,
// sitting, the saddle, riding, his fangs, his menu, his fights, fainting. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = 'execute in bm:hollow_throne run ', O = 'execute in minecraft:overworld run ';
  const cnt = async (sel, d = H) => { const m = (await run(`${d}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const epos = async (sel, d = H) => { const m = (await run(`${d}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const nbt = async (sel, path, d = H) => (await run(`${d}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel, d = H) => { const m = (await run(`${d}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel, d = H) => { const u = await uuidOf(sel, d); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const hp = async (sel, d = H) => +(((await run(`${d}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?\s*$/) || [0, NaN])[1]);
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  const dist = (a, b) => a && b ? Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]) : 1e9;
  const SEAL = [1084.5, 103, 1083.5], ARRIVE = [1076.5, 6, 1097.5];
  const A = await bot('TestRat'); await sleep(2500);
  A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const reset = async () => {
    for (const t of ['bm.emmapet', 'bm.leopet', 'bm.cecilpet', 'bm.appet']) { await run(`${H}kill @e[tag=${t}]`); await run(`${O}kill @e[tag=${t}]`); }
    for (const o of ['bm.emcd', 'bm.lecd', 'bm.cpcd', 'bm.apcd', 'bm.apsd', 'bm.apk', 'bm.apcl']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('clear TestRat'); await run('effect clear TestRat');
  };
  await reset();
  await run('scoreboard players set TestRat bm.conq 6'); await run('tag TestRat add bm.got_warp');
  await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true');
  await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`);
  let boss = '@e[type=minecraft:husk,tag=bm.apboss,limit=1]';

  if (want('seal')) {
    // ================================================================== 1. the seal: it shows, it reads, it stirs, it breaks
    await run(`${H}tp TestRat ${SEAL[0] - 4} ${SEAL[1]} ${SEAL[2]} -90 0`); await sleep(3000); A.stand();
    ok('the serpent seal is in the throne room floor (marker + plate)', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.apseal]')) === 1 &&
                                                                                (await cnt('@e[type=minecraft:item_display,tag=bm.apsealv]')) === 1));
    await run(`${H}tp TestRat ${SEAL[0]} ${SEAL[1]} ${SEAL[2]} -90 0`); A.bars.length = 0; await sleep(500); A.stand();
    ok('standing on it, a conqueror reads it: three hollows - a ribbon, a crest, a gem', await wait(6000, async () => /Three hollows ring it/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / ').slice(0, 160));
    // (their own items, used as items - the Hollow lets its conqueror's followers in)
    await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon');
    await run('loot replace entity TestRat hotbar.1 loot bm:items/leo_crest');
    await run('loot replace entity TestRat hotbar.2 loot bm:items/cecil_gem');
    A.chats.length = 0; A.bars.length = 0;
    await use(A, 0);
    ok('Emma answers her ribbon in the Hollow (a conqueror)', await wait(4000, async () => (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) === 1), A.bars.slice(-2).join(' / ').slice(0, 160));
    ok('one of the three: the seal stirs', await wait(5000, async () => /one of the three/.test(A.bars.join(' '))), A.bars.slice(-3).join(' / ').slice(0, 200));
    ok('...and Emma knows the mark', await wait(4000, async () => /I know this mark/.test(A.chats.join(' '))));
    A.bars.length = 0; await sleep(1200);
    await use(A, 1);
    ok('Leo answers his crest', await wait(4000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1));
    ok('two of the three: one more', await wait(5000, async () => /two of the three/.test(A.bars.join(' '))), A.bars.slice(-3).join(' / ').slice(0, 200));
    A.chats.length = 0;
    await use(A, 2);
    ok('Cecil answers his gem', await wait(4000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.cecilpet]')) === 1));
    ok('all three on the seal: it breaks', await wait(5000, async () => (await sc('@e[type=minecraft:marker,tag=bm.apseal,limit=1]', 'bm.apw')) === 1));
    ok('they remember (Emma, Cecil, Leo speak)', await wait(6000, async () => /really him/.test(A.chats.join(' ')) && /made sure he was dead/.test(A.chats.join(' ')) &&
                                                                       /Stay behind me, Princess/.test(A.chats.join(' '))), A.chats.slice(-4).join(' | ').slice(0, 300));
    ok('...and swallows them: the bot is in the den', await wait(8000, async () => dist(await epos('TestRat'), ARRIVE) < 3), JSON.stringify(await epos('TestRat')));
    await sleep(800); A.stand();
    const near = async t => cnt(`@e[tag=${t},x=${ARRIVE[0]},y=${ARRIVE[1]},z=${ARRIVE[2]},distance=..10]`);
    ok('Emma, Leo and Cecil came down with them', (await near('bm.emmapet')) === 1 && (await near('bm.leopet')) === 1 && (await near('bm.cecilpet')) === 1);
    ok('he is there, asleep before his throne (host + 15 parts)', await wait(5000, async () => (await cnt(boss)) === 1 &&
                                                                                (await cnt('@e[type=minecraft:item_display,tag=bm.apb]')) === 15),
       `boss ${await cnt(boss)} parts ${await cnt('@e[type=minecraft:item_display,tag=bm.apb]')}`);
    ok('asleep: invulnerable, his eyes shut', /Invulnerable: 1b/.test(await nbt(boss, '')) || /1b/.test(await nbt(boss, 'Invulnerable')));
  }

  if (want('seal') || want('fight')) {
    // ================================================================== 2. the fight
    if (!(await cnt(boss))) { await run(`${H}tp TestRat ${ARRIVE[0]} ${ARRIVE[1]} ${ARRIVE[2]} 180 0`); await run('scoreboard players set #apwake bm.p2 1'); await sleep(3500); A.stand(); }
    await run('loot replace entity TestRat hotbar.3 loot bm:items/apo_oath'); await run('clear TestRat *[minecraft:custom_data~{bm:"apo_oath"}]');
    await run('item replace entity TestRat hotbar.4 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]');
    const bp = await epos(boss);
    A.chats.length = 0;
    await run(`${H}tp TestRat ${bp[0]} ${bp[1]} ${bp[2] + 11} 180 0`); await sleep(500); A.stand();
    ok('coming close wakes him (the intro begins)', await wait(4000, async () => (await sc(boss, 'bm.apph')) === 1), `apph ${await sc(boss, 'bm.apph')}`);
    ok('"the little princess" - he knows them', await wait(6000, async () => /little princess/.test(A.chats.join(' '))));
    ok('the intro ends: he fights (AI on, hurtable)', await wait(9000, async () => /0b/.test(await nbt(boss, 'NoAI')) && /0b/.test(await nbt(boss, 'Invulnerable'))));
    // (his attacks: every code the mind starts, sampled; and they land on the bot)
    await run('effect give TestRat minecraft:regeneration 60 2 true');
    const seen = new Set(); let lowest = 999;
    for (let k = 0; k < 120; k++) {
      const a = await sc(boss, 'bm.apatk'); if (a > 0) seen.add(a);
      const b = await epos(boss); if (b && dist(b, await epos('TestRat')) > 7) { await run(`${H}tp TestRat ${b[0]} ${b[1]} ${b[2] + 4} 180 0`); }
      lowest = Math.min(lowest, await hp('TestRat'));
      await sleep(250);
    }
    ok('phase 1: he attacks (claw / bite / mace / fangs / venom)', [1, 2, 3, 4, 5].filter(a => seen.has(a)).length >= 2, `seen ${[...seen].join(',')}`);
    ok('...and his blows land (the bot was hurt)', lowest < 195, `lowest health ${lowest}`);
    // (the bot's own blows, on his hitbox)
    const h0 = await hp(boss);
    const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_ap,limit=1]');
    A.slot(4); await sleep(300);
    for (let k = 0; k < 4; k++) { const b = await epos(boss); await run(`${H}tp TestRat ${b[0]} ${b[1]} ${b[2] + 2.2} 180 0`); await sleep(200); if (box) A.attack(box.entityId); await sleep(700); }
    const h1 = await hp(boss);
    ok('the bot\'s sword on his hitbox hurts him (the relay)', h1 < h0 - 10, `health ${h0} -> ${h1}`);
    // (three quarters: the court)
    const mx = +(((await run(`${H}attribute ${boss} minecraft:max_health get`)).match(/([\d.]+)\s*$/) || [0, 900])[1]);
    await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * 0.7)}f`);
    ok('at three quarters he calls his drowned court', await wait(6000, async () => (await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]')) >= 3), `court ${await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]')}`);
    // (half: the serpent unbound)
    await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * 0.45)}f`);
    ok('at half: THE SERPENT UNBOUND (phase 2)', await wait(8000, async () => (await sc(boss, 'bm.apph')) === 2), `apph ${await sc(boss, 'bm.apph')}`);
    await sleep(1500);
    ok('...the ethereal king: his look changes', /apo_head_eth/.test(await nbt('@e[type=minecraft:item_display,tag=bm.app_head,tag=bm.apb,limit=1]', 'item')));
    ok('...and he flies (no AI, no gravity, up off the floor)', /1b/.test(await nbt(boss, 'NoGravity')) && (await epos(boss))[1] > ARRIVE[1] + 1.5, JSON.stringify(await epos(boss)));
    const wing = await nbt('@e[type=minecraft:item_display,tag=bm.app_wingr,tag=bm.apb,limit=1]', 'transformation.scale');
    ok('...on violet wings (shown)', /\[([1-9][\d.]*)f/.test(wing), wing);
    const seen2 = new Set(); let sawOrb = false, sawFangs = false;
    for (let k = 0; k < 140; k++) {
      const a = await sc(boss, 'bm.apatk'); if (a > 0) seen2.add(a);
      if (await cnt('@e[type=minecraft:item_display,tag=bm.aporb]')) sawOrb = true;
      if (await cnt('@e[type=minecraft:evoker_fangs]')) sawFangs = true;
      const b = await epos(boss); if (b && dist(b, await epos('TestRat')) > 10) await run(`${H}tp TestRat ${b[0]} ${ARRIVE[1] - 3} ${b[2] + 4} 180 0`);
      await sleep(250);
    }
    ok('phase 2: his ethereal attacks (orbs / swoop / gust / grand fangs / call)', [11, 12, 13, 14, 15].filter(a => seen2.has(a)).length >= 2, `seen ${[...seen2].join(',')}`);
    ok('...void orbs or fangs seen in the den', sawOrb || sawFangs, `orbs ${sawOrb} fangs ${sawFangs}`);
    // (the end: the bot lands the last blow)
    await run(`${H}data modify entity ${boss} Health set value 4f`);
    const b = await epos(boss); await run(`${H}tp ${boss} ${b[0]} ${ARRIVE[1] - 3} ${b[2]}`); await sleep(300);
    const b2 = await epos(boss); await run(`${H}tp TestRat ${b2[0]} ${b2[1]} ${b2[2] + 2} 180 0`); await sleep(400);
    const box2 = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_ap,limit=1]');
    A.chats.length = 0;
    for (let k = 0; k < 6 && (await cnt(boss)); k++) { if (box2) A.attack(box2.entityId); await sleep(800); }
    ok('the bot\'s blow brings him down', await wait(4000, async () => !(await cnt(boss))));
    ok('APOPHISS FALLS - "I am yours"', await wait(5000, async () => /I am yours/.test(A.chats.join(' '))), A.chats.slice(-2).join(' | ').slice(0, 200));
    ok('the drops: the Oath, the True Crown, the Mace', (await has('TestRat', 'apo_oath')) === 1 && (await has('TestRat', 'apo_true_crown')) === 1 && (await has('TestRat', 'apo_mace')) === 1,
       `oath ${await has('TestRat', 'apo_oath')} crown ${await has('TestRat', 'apo_true_crown')} mace ${await has('TestRat', 'apo_mace')}`);
    ok('...and the hoard (medallions)', (await has('TestRat', 'medallion')) >= 6);
    ok('his rig sinks and fades away', await wait(6000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.apb]'))));
    ok('his court goes with him', await wait(3000, async () => !(await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]'))));
    // (the pad by the door: back up)
    await run(`${H}tp TestRat 1076.5 6 1099.5 180 0`); await sleep(600); A.stand(); await sleep(300);
    await A.walkTo(1076.5, 1100.5);
    ok('the pad by the door takes you back up to the throne room', await wait(4000, async () => dist(await epos('TestRat'), [1078.5, 103, 1083.5]) < 2), JSON.stringify(await epos('TestRat')));
  }

  if (want('pet')) {
    // ================================================================== 3. the Serpent's Oath
    await reset(); await run('effect give TestRat minecraft:resistance 600 4 true');
    const X = 13400, Y = 121, Z = 13060;
    await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
    await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
    for (let y = Y; y < Y + 12; y += 6) await run(`${O}fill ${X - 20} ${y} ${Z - 20} ${X + 20} ${y + 5} ${Z + 20} minecraft:air`);
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await sleep(2500); A.stand();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_oath');
    A.bars.length = 0;
    await use(A, 0);
    const pet = '@e[type=minecraft:wolf,tag=bm.appet,limit=1]';
    ok('the Oath calls him (host + 15 parts)', await wait(4000, async () => (await cnt(pet, O)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.app_pet]', O)) === 15),
       A.bars.slice(-2).join(' / '));
    await sleep(1500);
    const pp = await epos(pet, O), cp = await epos('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_coil,limit=1]', O);
    ok('his rig stands with him', dist(pp, cp) < 2.5, `host ${pp} coil ${cp}`);
    const r1 = await nbt('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_head,limit=1]', 'transformation.left_rotation', O); await sleep(1600);
    const r2 = await nbt('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_head,limit=1]', 'transformation.left_rotation', O);
    ok('he breathes (the idle cycle moves him)', r1 !== r2, `${r1} / ${r2}`);
    // (sit by right-clicking him)
    await run(`${O}tp ${pet} ${X + 0.5} ${Y} ${Z + 2.5}`); await sleep(1200);
    let box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.aphit,limit=1]', O);
    A.slot(5); await sleep(200); if (box) A.interact(box.entityId); await sleep(900);
    ok('right-click him: he coils down to sit', /1b/.test(await nbt(pet, 'Sitting', O)), `box ${box ? 'yes' : 'no'}`);
    await sleep(600); if (box) A.interact(box.entityId); await sleep(900);
    ok('again: he rises', /0b/.test(await nbt(pet, 'Sitting', O)));
    // (the saddle)
    await run('item replace entity TestRat hotbar.6 with minecraft:saddle'); A.slot(6); await sleep(300);
    box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.aphit,limit=1]', O);
    if (box) A.interact(box.entityId); await sleep(900);
    ok('right-click with a saddle: he wears it', (await sc('TestRat', 'bm.apsd')) === 1 && /apo_body_saddle/.test(await nbt('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_body,limit=1]', 'item', O)));
    ok('...the saddle is used up', !/saddle/.test(await run('data get entity TestRat Inventory')));
    // (ride: the Oath beside him)
    await run(`${O}tp ${pet} ${X + 0.5} ${Y} ${Z + 1.8}`); await sleep(700);
    await use(A, 0); await sleep(600);
    const riding = async () => /returned 1/.test(await run('execute as TestRat run function bm:p131/on_him'));
    ok('the Oath beside him, saddled: you climb on', await riding());
    const s0 = await epos(pet, O);
    A.ride(0, 0, { forward: true }); await sleep(2200);
    const s1 = await epos(pet, O);
    ok('walk: he slithers on under you', dist(s0, s1) > 3, `${s0} -> ${s1}`);
    A.ride(0, 0, {}); await sleep(400);
    A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(400);
    ok('the Oath while riding: Serpent\'s Fangs ahead', (await cnt('@e[type=minecraft:evoker_fangs]', O)) >= 5);
    A.ride(0, 0, { shift: true }); await sleep(700); A.unride(); A.input({}); await sleep(300);
    ok('sneak: you climb off', !(await riding()));
    A.stand(); await sleep(500);
    // (his menu: sneak + use)
    A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); const opened = await A.useWait(); A.input({}); await sleep(200);
    ok('sneak + use the Oath: his menu', opened && A.buttons().some(b => /Sit \/ follow/.test(b.label)) && A.buttons().some(b => /Send him home/.test(b.label)),
       A.buttons().map(b => b.label).join(' | '));
    const b0 = await A.press(/Take off the saddle/);
    await sleep(600);
    ok('"Take off the saddle": he is bare, and the saddle is yours again', b0 && (await sc('TestRat', 'bm.apsd')) === 0 && /saddle/.test(await run('data get entity TestRat Inventory')));
    // (he fights)
    await run(`${O}summon minecraft:husk ${X + 4.5} ${Y} ${Z + 4.5} {Tags:["bm.t134foe"],Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}`);
    const f0 = await hp('@e[type=minecraft:husk,tag=bm.t134foe,limit=1]', O);
    await wait(10000, async () => !(await cnt('@e[type=minecraft:husk,tag=bm.t134foe]', O)) || (await hp('@e[type=minecraft:husk,tag=bm.t134foe,limit=1]', O)) < f0 - 8);
    const f1 = (await cnt('@e[type=minecraft:husk,tag=bm.t134foe]', O)) ? await hp('@e[type=minecraft:husk,tag=bm.t134foe,limit=1]', O) : 0;
    ok('he fights: claw, bite, spit at a husk', f1 < f0 - 8, `husk ${f0} -> ${f1}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t134foe]`);
    // (send him home from the menu)
    A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); await A.useWait(); A.input({}); await sleep(200);
    await A.press(/Send him home/); await sleep(900);
    ok('"Send him home": he goes', !(await cnt(pet, O)) && await wait(3000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.app_pet]', O))));
    // (fainting)
    await use(A, 0); await wait(4000, async () => (await cnt(pet, O)) === 1); await sleep(1000);
    await run(`${O}kill ${pet}`);
    ok('he faints: his rig dissolves, the Oath rests 5 minutes', await wait(4000, async () => (await sc('TestRat', 'bm.apcd')) >= 290 && !(await cnt('@e[type=minecraft:item_display,tag=bm.app_pet]', O))),
       `cd ${await sc('TestRat', 'bm.apcd')}`);
  }

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  await reset(); await run('attribute TestRat minecraft:max_health base set 20');
  R.end(); A.end(); process.exit(0);
})();
