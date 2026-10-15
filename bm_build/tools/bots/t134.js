// 2.77: Apophiss, as a regular (non-op) player - the serpent seal in the Hollow throne room (a conqueror; Emma, Leo and Cecil
// called with their own items, one by one: the seal stirs, then breaks), the den, the fight (both phases, his attacks seen
// landing), the bot's own blows through his hitbox, the win and its drops, the pad back up; then the Serpent's Oath: his rig,
// sitting, the saddle, riding, his fangs, his menu, his fights, fainting. rcon only sets the stage.
// 2.77b: the den lets in only those the seal swallowed (section "den": a teleport in, a stand on the dome - thrown back up)
// and he rises only when someone who has beaten the Hollow King comes back with Emma, Leo and Cecil; he comes in black fire (a vortex of 16 tongues, about
// 7 seconds, then the burst and his name); at half he plays dead (the bar gone, his court too, his old enemies wondering)
// before THE SERPENT UNBOUND; the follower is his full size.
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
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6'); await run('tag TestRat add bm.got_warp');
  const tough = async () => { await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true');
    await run('effect give TestRat minecraft:resistance 900 3 true'); };
  let deaths = 0; A.on('update_health', p => { if (p.health <= 0) deaths++; });
  await tough();
  await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`);
  await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apfire]`); await run(`${H}kill @e[type=minecraft:marker,tag=bm.apvx]`);
  let boss = '@e[type=minecraft:husk,tag=bm.apboss,limit=1]';

  if (want('den')) {
    // ================================================================== 0. no way in but the seal; and he rises only for the worthy
    const BACK = [1078.5, 103, 1083.5];
    const inDen = async () => dist(await epos('TestRat'), BACK) > 3;
    await run('tag TestRat remove bm.apin'); await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run('scoreboard players set #apwake bm.p2 0');
    A.bars.length = 0;
    await run(`${H}tp TestRat ${ARRIVE[0]} ${ARRIVE[1]} ${ARRIVE[2]} 180 0`); await sleep(400); A.stand();
    ok('teleported into the den without the seal: thrown straight back up to the throne room', await wait(3000, async () => dist(await epos('TestRat'), BACK) < 2),
       JSON.stringify(await epos('TestRat')));
    ok('..."Only the serpent\'s seal takes anyone down there."', /Only the serpent's seal/.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 120));
    await run(`${H}tp TestRat 1076.5 41 1076.5 0 0`); await sleep(300); A.stand();
    ok('standing on the den\'s dome (to dig in, or pearl through it): thrown back up too', await wait(3000, async () => dist(await epos('TestRat'), BACK) < 2),
       JSON.stringify(await epos('TestRat')));
    // (in, as the seal would bring you - but not worthy: no boss, and the den says why)
    await run('scoreboard players set TestRat bm.conq 5'); await run('scoreboard players set TestRat bm.conqb 5');
    // (as the seal would: in, with its mark - one command, or the den could find the bot unmarked between two)
    await run('execute as TestRat run function bm:admin/apophiss_den'); await run('scoreboard players set #apwake bm.p2 0'); await sleep(500); A.stand();
    await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon'); await run('loot replace entity TestRat hotbar.1 loot bm:items/leo_crest');
    await run('loot replace entity TestRat hotbar.2 loot bm:items/cecil_gem');
    await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
    for (const k of [0, 1, 2]) { await use(A, k); await sleep(2300); }      // (follower items share a 2 s use debounce, bm.gvhc)
    await run('scoreboard players set TestRat bm.conq 5'); await run('scoreboard players set TestRat bm.conqb 5');
    const three = async () => (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.cecilpet]')) === 1;
    ok('(in the den with the seal\'s mark, and Emma, Leo and Cecil with the bot)', await inDen() && await three());
    A.bars.length = 0; await run('scoreboard players set #apwake bm.p2 1'); await sleep(5500);
    ok('...but the Hollow King not felled by this player: he doesn\'t rise', !(await cnt(boss)));
    ok('..."He rises only when one who has beaten the Hollow King comes back with Emma, Leo and Cecil"', /has beaten the Hollow King comes back/.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 140));
    // (a conqueror - but without the three)
    await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
    for (const t of ['bm.emmapet', 'bm.leopet', 'bm.cecilpet']) await run(`${H}kill @e[tag=${t}]`);
    await run('clear TestRat'); await sleep(2500);
    ok('a conqueror without Emma, Leo and Cecil: still nothing', !(await cnt(boss)));
    // (a teleport out of the den takes the mark with it)
    await run(`${H}tp TestRat ${BACK[0]} ${BACK[1]} ${BACK[2]} -90 0`); await sleep(1600); A.stand();
    ok('out of the den, the seal\'s mark is gone (coming back needs the seal again)', !/passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.apin]')));
    await run('scoreboard players set #apwake bm.p2 0'); await reset(); await tough();
    for (const o of ['bm.emcd', 'bm.lecd', 'bm.cpcd']) await run(`scoreboard players set TestRat ${o} 0`);
  }

  if (want('seal')) {
    // ================================================================== 1. the seal: it shows, it reads, it stirs, it breaks
    await run(`${H}tp TestRat ${SEAL[0] - 4} ${SEAL[1]} ${SEAL[2]} -90 0`); await sleep(3000); A.stand();
    await run(`${H}scoreboard players set @e[type=minecraft:marker,tag=bm.apseal] bm.apt 0`); await run(`${H}scoreboard players set @e[type=minecraft:marker,tag=bm.apseal] bm.apsn 0`);
    ok('the serpent seal is in the throne room floor (marker + plate)', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.apseal]')) === 1 &&
                                                                                (await cnt('@e[type=minecraft:item_display,tag=bm.apsealv]')) === 1));
    await run('tag TestRat remove bm.apread');
    await run(`${H}tp TestRat ${SEAL[0]} ${SEAL[1]} ${SEAL[2]} -90 0`); A.bars.length = 0; A.chats.length = 0; await sleep(500); A.stand();
    ok('standing on it, a conqueror reads it: three hollows - a ribbon, a crest, a gem', await wait(6000, async () => /Three hollows ring it/.test(A.bars.join(' '))),
       A.bars.slice(-2).join(' / ').slice(0, 160));
    ok('...and the words cut round it: "HE WHO SITS THIS THRONE SITS IT BY MY LEAVE"', /SITS IT BY MY LEAVE/.test(A.chats.join(' ')), A.chats.slice(-1).join('').slice(0, 160));
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
    A.stand();
    // (his coming, watched as one from the moment they land: the fire, his rig, the spiral and his own clock, every ~100 ms
    //  until the burst - a slow check here would miss what it's checking)
    const ha = await hp('TestRat');
    A.titles.length = 0;
    let aptBurst = NaN, sawFire = 0, sawMarker = false, invul = false, scale0 = NaN, grew = 0, r1 = NaN, r2 = NaN, moved = false, prevF = null;
    const vxr = async () => { const c = await epos('@e[type=minecraft:marker,tag=bm.apvx,limit=1]'), f = await epos('@e[type=minecraft:item_display,tag=bm.apfire,scores={bm.apfi=3},limit=1]');
      return c && f ? [Math.hypot(f[0] - c[0], f[2] - c[2]), f] : [NaN, null]; };
    const coil = async () => +(((await nbt('@e[type=minecraft:item_display,tag=bm.app_coil,tag=bm.apb,limit=1]', 'transformation.scale[0]')).match(/([\d.]+)f/) || [0, NaN])[1]);
    for (const t0 = Date.now(); Date.now() - t0 < 20000;) {
      const apt = await sc(boss, 'bm.apt');
      if (Number.isNaN(apt)) { await sleep(100); continue; }
      sawFire = Math.max(sawFire, await cnt('@e[type=minecraft:item_display,tag=bm.apfire]'));
      if (await cnt('@e[type=minecraft:marker,tag=bm.apvx]')) sawMarker = true;
      if (/1b/.test(await nbt(boss, 'Invulnerable'))) invul = true;
      if (apt < 60 && Number.isNaN(scale0)) scale0 = await coil();
      if (apt > 115 && apt < 145) grew = Math.max(grew, await coil());
      if (apt >= 40 && apt <= 60 && Number.isNaN(r1)) r1 = (await vxr())[0];
      if (apt >= 110 && apt <= 140 && Number.isNaN(r2)) r2 = (await vxr())[0];
      if (apt >= 30 && apt <= 140) { const [, f] = await vxr(); if (prevF && f && dist(prevF, f) > 0.1) moved = true; prevF = f; }
      if (A.titles.some(t => /APOPHISS/.test(t))) { aptBurst = apt; break; }
      await sleep(60);
    }
    ok('he comes: black fire climbs out of the floor before his throne - a vortex of sixteen tongues', sawFire === 16 && sawMarker, `tongues ${sawFire} marker ${sawMarker}`);
    ok('...and he is there inside it, but not yet seen (his rig at nothing)', scale0 === 0, `coil scale early ${scale0}`);
    ok('...invulnerable while he comes', invul);
    ok('...the tongues spiral, tighter as it goes', moved && r2 < r1 - 0.8, `radius ${r1.toFixed(2)} -> ${r2.toFixed(2)}`);
    ok('...while he grows in it', grew > 0.5, `coil scale ${grew}`);
    ok('...then the burst: APOPHISS, the Serpent King', !Number.isNaN(aptBurst), A.titles.join(' / ').slice(0, 120));
    ok('...the whole coming lasts five to ten seconds (by his own clock)', aptBurst >= 100 && aptBurst <= 200, `the burst ${(aptBurst / 20).toFixed(1)} s after he began`);
    ok('...and the fire is gone after', await wait(4000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.apfire]'))));
    const air = async (x, y, z) => /passed/i.test(await run(`${H}execute if block ${x} ${y} ${z} minecraft:air`));
    ok('...onto open floor - nobody lands in a wall (no suffocation)', (await air(1076, 6, 1097)) && (await air(1076, 7, 1097)) && (await hp('TestRat')) >= ha,
       `health ${ha} -> ${await hp('TestRat')}`);
    const near = async t => cnt(`@e[tag=${t},x=${ARRIVE[0]},y=${ARRIVE[1]},z=${ARRIVE[2]},distance=..12]`);
    ok('Emma, Leo and Cecil came down with them', (await near('bm.emmapet')) === 1 && (await near('bm.leopet')) === 1 && (await near('bm.cecilpet')) === 1);
    ok('the den lets them in (the seal\'s mark)', /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.apin]')));
  }

  if (want('seal') || want('fight')) {
    // ================================================================== 2. the fight
    // (the den floor is y 5; his followers fight too - rcon holds his health between the steps so each threshold is the test's)
    const FLOOR = 5;
    if (!(await cnt(boss))) {          // (on its own: as the seal would - in with its mark, and the three called with their own items)
      await run('execute as TestRat run function bm:admin/apophiss_den'); await sleep(800); A.stand();
      for (const [k, iid] of [[0, 'emma_ribbon'], [1, 'leo_crest'], [2, 'cecil_gem']]) { await run(`loot replace entity TestRat hotbar.${k} loot bm:items/${iid}`); await use(A, k); await sleep(1200); }
      await run('scoreboard players set #apwake bm.p2 1'); await wait(5000, async () => (await cnt(boss)) === 1);
    }
    await run('loot replace entity TestRat hotbar.3 loot bm:items/apo_oath'); await run('clear TestRat *[minecraft:custom_data~{bm:"apo_oath"}]');
    await run('item replace entity TestRat hotbar.4 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]');
    const bp = await epos(boss);
    await run(`${H}tp TestRat ${bp[0]} ${bp[1]} ${bp[2] + 11} 180 0`); await sleep(500); A.stand();     // (still the seal's mark: a teleport within the den keeps it)
    // (2.77c: his rig is never doubled - one coil from his rising to his fall - sampled throughout the fight)
    let coils = 0; const coilT = setInterval(async () => { try { coils = Math.max(coils, await cnt('@e[type=minecraft:item_display,tag=bm.apb,tag=bm.app_coil]')); } catch (e) {} }, 1500);
    ok('"the little princess" - he knows them', await wait(14000, async () => /little princess/.test(A.chats.join(' '))));
    ok('...and he made their Hollow King: "His crown of shadow was MINE. I lent it."', await wait(5000, async () => /crown of shadow was MINE/.test(A.chats.join(' '))));
    // (NoAI:0b and Invulnerable:0b aren't saved at all in 26.x: "not 1b" is the check)
    ok('the intro ends: he fights (AI on, hurtable)', await wait(9000, async () => !/1b/.test(await nbt(boss, 'NoAI')) && !/1b/.test(await nbt(boss, 'Invulnerable'))));
    const mx = +(((await run(`${H}attribute ${boss} minecraft:max_health get`)).match(/([\d.]+)\s*$/) || [0, 900])[1]);
    const hold = async (lo, to) => { const h = await hp(boss); if (h < mx * lo) await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * to)}f`); };
    // (his attacks: every code the mind starts, sampled; and they land on the bot)
    await tough(); await run('effect give TestRat minecraft:regeneration 900 2 true');
    const seen = new Set(); let lowest = 999;
    for (let k = 0; k < 120; k++) {
      await hold(0.8, 0.95);
      const a = await sc(boss, 'bm.apatk'); if (a > 0) seen.add(a);
      // (now in his reach, now twelve blocks off - so he has a reason for each of his attacks)
      const b = await epos(boss), me = await epos('TestRat'), far = Math.floor(k / 20) % 2 === 1;
      if (b && !far && dist(b, me) > 6) await run(`${H}tp TestRat ${b[0]} ${FLOOR} ${b[2] + 3} 180 0`);
      if (b && far && dist(b, me) < 9) await run(`${H}tp TestRat ${b[0] + (b[0] < 1076 ? 12 : -12)} ${FLOOR} ${b[2]} 90 0`);
      lowest = Math.min(lowest, await hp('TestRat'));
      await sleep(250);
    }
    ok('phase 1: he attacks (claw / bite / mace / fangs / venom)', [1, 2, 3, 4, 5].filter(a => seen.has(a)).length >= 3, `seen ${[...seen].join(',')}`);
    ok('...and his blows land (the bot was hurt)', lowest < 199, `lowest health ${lowest}`);
    ok('...no court and no ascent above three quarters', !seen.has(6) && !seen.has(7) && (await sc(boss, 'bm.apph')) === 1, `seen ${[...seen].join(',')}`);
    // (the bot's own blows, on his hitbox)
    await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * 0.95)}f`);
    A.slot(4); await sleep(300);
    let dealt = 0;
    for (let k = 0; k < 16 && dealt <= 10; k++) {         // (he moves while he fights: a few swings miss - so up to sixteen)
      const b = await epos(boss); await run(`${H}tp TestRat ${b[0]} ${b[1]} ${b[2] + 2.2} 180 0`); await sleep(250);
      const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_ap,limit=1]');
      const h0 = await hp(boss); if (box) A.attack(box.entityId); await sleep(150); const h1 = await hp(boss); if (h1 < h0) dealt += h0 - h1;
      await sleep(600);
    }
    ok('the bot\'s sword on his hitbox hurts him (the relay)', dealt > 10, `dealt ${dealt.toFixed(1)}`);
    // (three quarters: the court)
    await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * 0.7)}f`);
    let court = 0;
    ok('at three quarters he calls his drowned court', await wait(6000, async () => (court = Math.max(court, await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]'))) >= 3), `court ${court}`);
    // (2.77c: each courtier rises where there is room for it - none in the floor or a wall, suffocating)
    const inWall = async () => { let n = 0; for (const dy of [0, 1]) { const m = (await run(`${H}execute as @e[type=minecraft:drowned,tag=bm.apcourt] at @s unless block ~ ~${dy} ~ #minecraft:replaceable`)).match(/count: (\d+)/i); n += m ? +m[1] : 0; } return n; };
    const w1 = await inWall(); await sleep(1000); const w2 = await inWall();
    ok('...every courtier in open air - none caught in the floor or a wall', w1 === 0 && w2 === 0, `stuck ${w1} / ${w2}`);
    ok('..."RISE, MY COURT"', /RISE, MY COURT/.test(A.bars.join(' ')));
    await sleep(2500);
    // (half: the serpent unbound)
    await run(`${H}data modify entity ${boss} Health set value ${Math.round(mx * 0.45)}f`);
    A.chats.length = 0; A.titles.length = 0; const k0 = await sc('TestRat', 'bm.apk');
    ok('at half he falls: the bar goes...', await wait(4000, async () => (await sc(boss, 'bm.apatk')) === 7) && await wait(1500, async () => /hidden/.test(await run('bossbar get bm:apob visible'))));
    ok('...his court crumbles with him', await wait(2500, async () => !(await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]'))));
    ok('...and he can\'t be hurt while he lies there', /1b/.test(await nbt(boss, 'Invulnerable')));
    ok('"Is he... did we...?" - "Please be dead." - "Serpents play dead."', await wait(8000, async () => /did we/.test(A.chats.join(' ')) && /Please be dead/.test(A.chats.join(' ')) &&
       /Serpents play dead/.test(A.chats.join(' '))), A.chats.slice(-3).join(' | ').slice(0, 200));
    ok('...still lying there, nothing won (no "APOPHISS FALLS", no drops)', (await sc(boss, 'bm.apph')) === 1 && !/I am yours/.test(A.chats.join(' ')) && (await sc('TestRat', 'bm.apk')) === k0);
    ok('a heartbeat - and a laugh: "Did you really think the Hollow would let me die so EASILY?"', await wait(5000, async () => /die so EASILY/.test(A.chats.join(' '))));
    ok('..."That \"king\" wore a SLIVER of my power"', await wait(3000, async () => /SLIVER of my power/.test(A.chats.join(' '))));
    ok('then: THE SERPENT UNBOUND (phase 2)', await wait(6000, async () => (await sc(boss, 'bm.apph')) === 2), `apph ${await sc(boss, 'bm.apph')}`);
    ok('...the title says so', await wait(2000, async () => A.titles.some(t => /SERPENT UNBOUND/.test(t))), A.titles.join(' / ').slice(0, 120));
    let aptMax = await sc(boss, 'bm.apt');
    await wait(5000, async () => { const a = await sc(boss, 'bm.apatk'); if (a === 7) aptMax = Math.max(aptMax, await sc(boss, 'bm.apt')); return a !== 7; }, 100);
    ok('...the feint and the change last ten to fifteen seconds (by his own clock)', aptMax >= 200 && aptMax <= 300, `${(aptMax / 20).toFixed(1)} s`);
    ok('...and his bar is back', /currently visible/.test(await run('bossbar get bm:apob visible')));
    ok('...the ethereal king: his look changes', await wait(1500, async () => /apo_head_eth/.test(await nbt('@e[type=minecraft:item_display,tag=bm.app_head,tag=bm.apb,limit=1]', 'item'))));
    ok('...and he flies (no AI, no gravity, well up off the floor)', /1b/.test(await nbt(boss, 'NoAI')) && /1b/.test(await nbt(boss, 'NoGravity')) && (await epos(boss))[1] > FLOOR + 3.5,
       JSON.stringify(await epos(boss)));
    const wing = await nbt('@e[type=minecraft:item_display,tag=bm.app_wingr,tag=bm.apb,limit=1]', 'transformation.scale');
    ok('...on violet wings (shown)', /\[([1-9][\d.]*)f/.test(wing), wing);
    const seen2 = new Set(); let sawOrb = false, sawFangs = false, vexMax = 0, high = 0;
    for (let k = 0; k < 240 && !(k >= 160 && sawOrb && sawFangs); k++) {
      await hold(0.25, 0.4);
      const a = await sc(boss, 'bm.apatk'); if (a > 0) seen2.add(a);
      if (await cnt('@e[type=minecraft:item_display,tag=bm.aporb]')) sawOrb = true;
      if (await cnt('@e[type=minecraft:evoker_fangs]')) sawFangs = true;
      vexMax = Math.max(vexMax, await cnt('@e[type=minecraft:vex,tag=bm.apvex]'));
      const b = await epos(boss); if (b) high = Math.max(high, b[1] - FLOOR);
      if (b && dist([b[0], FLOOR, b[2]], await epos('TestRat')) > 9) await run(`${H}tp TestRat ${b[0]} ${FLOOR} ${b[2] + 4} 180 0`);
      await sleep(250);
    }
    ok('phase 2: his ethereal attacks (orbs / swoop / gust / grand fangs / call)', [11, 12, 13, 14, 15].filter(a => seen2.has(a)).length >= 3, `seen ${[...seen2].join(',')}`);
    ok('...void orbs and fangs seen in the den', sawOrb && sawFangs, `orbs ${sawOrb} fangs ${sawFangs}`);
    ok('...never more than three spectral serpents', vexMax <= 3, `max ${vexMax}`);
    ok('...hovering five to seven up between dives', high >= 5 && high < 9, `highest ${high.toFixed(2)}`);
    // (the end: the bot lands the last blow - brought down where it can reach)
    await wait(4000, async () => (await sc(boss, 'bm.apatk')) === 0);
    await run(`${H}data modify entity ${boss} Health set value 4f`);
    A.chats.length = 0; A.titles.length = 0;
    let jolts = 0; A.on('player_rotation', () => jolts++);
    for (let k = 0; k < 8 && (await cnt(boss)); k++) {
      const b = await epos(boss); await run(`${H}tp TestRat ${b[0]} ${Math.max(FLOOR, b[1] - 1)} ${b[2] + 1.6} 180 0`); await sleep(250);
      const box = await entOf(A, '@e[type=minecraft:interaction,tag=bm.bhit_ap,limit=1]'); if (box) A.attack(box.entityId); await sleep(700);
    }
    ok('the bot\'s blow brings him down', await wait(4000, async () => !(await cnt(boss))));
    clearInterval(coilT);
    ok('his rig was never doubled (one coil the whole fight)', coils === 1, `most coils at once: ${coils}`);
    // (2.77c: his defeat - he roars and the den shakes; black fire gathers into him; he bursts into black magic; a seal opens
    //  under it and drags it down, and closes; his crown drifts down for the bot, who walks over and picks it up)
    ok('he roars: "NO! Not again - not to HER!"', await wait(3000, async () => /Not again - not to HER/.test(A.chats.join(' '))), A.chats.slice(-1).join('').slice(0, 120));
    ok('...and the screen shakes (the bot\'s view jolted, again and again)', await wait(3000, async () => jolts >= 20), `jolts ${jolts}`);
    ok('black fire gathers round him (16 tongues)', await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.apfire]')) === 16));
    ok('he bursts into black magic: his rig gone', await wait(5000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.apb]'))));
    const CRF = '@e[type=minecraft:item_display,tag=bm.apcrf,limit=1]';
    ok('...his crown left hanging in the air where his head was', (await cnt(CRF)) === 1);
    await sleep(900); const c0 = await epos(CRF); await sleep(1500); const c1 = await epos(CRF);
    ok('...and drifting slowly down', c0 && c1 && c1[1] < c0[1] && c0[1] - c1[1] < 5, `y ${c0 && c0[1].toFixed(2)} -> ${c1 && c1[1].toFixed(2)}`);
    ok('a seal opens in the floor under the black magic', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.apdseal]')) === 1));
    ok('...and closes over it: APOPHISS IS SEALED', await wait(7000, async () => A.titles.some(t => /APOPHISS IS SEALED/.test(t))), A.titles.slice(-2).join(' | ').slice(0, 120));
    ok('"...The old oath binds me to the victor. I am yours."', await wait(2000, async () => /I am yours/.test(A.chats.join(' '))));
    ok('the drops: the Oath and the Mace - and the hoard (medallions)', (await has('TestRat', 'apo_oath')) === 1 && (await has('TestRat', 'apo_mace')) === 1 && (await has('TestRat', 'medallion')) >= 6,
       `oath ${await has('TestRat', 'apo_oath')} mace ${await has('TestRat', 'apo_mace')} medallions ${await has('TestRat', 'medallion')}`);
    ok('...but the crown isn\'t handed over: it is still falling', (await has('TestRat', 'apo_true_crown')) === 0);
    ok('...and the win counted once (his tally 1)', (await sc('TestRat', 'bm.apk')) === 1, `bm.apk ${await sc('TestRat', 'bm.apk')}`);
    const CI = '@e[type=minecraft:item,tag=bm.apcrd,limit=1]';
    ok('the crown lands: one lies on the floor for the bot', await wait(15000, async () => (await cnt(CI)) === 1));
    const myId = (await nbt('TestRat', 'UUID')).replace(/\s/g, ''), owner = (await nbt(CI, 'Owner')).replace(/\s/g, '');
    ok('...the bot\'s alone, glowing, and it never goes', owner === myId && /1b/.test(await nbt(CI, 'Glowing')) && /-32768s/.test(await nbt(CI, 'Age')), `owner ${owner} me ${myId}`);
    // (the bot was put up beside him where he flew - and a bot doesn't fall by itself: set it down on the floor first)
    const me0 = await epos('TestRat'); await run(`${H}tp TestRat ${me0[0]} ${FLOOR} ${me0[2]}`); await wait(2000, async () => A.pos && Math.abs(A.pos.y - FLOOR) < 0.1, 100); await sleep(300);
    const ci = await epos(CI); await A.walkTo(ci[0], ci[2]);
    ok('the bot walks over and picks it up: Apophiss\'s True Crown', await wait(4000, async () => (await has('TestRat', 'apo_true_crown')) === 1), JSON.stringify(ci));
    ok('nothing of it is left behind (no black fire, no seal, no markers, no falling crown)', await wait(6000, async () => !(await cnt('@e[type=minecraft:item_display,tag=bm.apfire]')) &&
       !(await cnt('@e[type=minecraft:item_display,tag=bm.apdseal]')) && !(await cnt('@e[type=minecraft:marker,tag=bm.apend]')) && !(await cnt('@e[type=minecraft:marker,tag=bm.apflr]')) &&
       !(await cnt(CRF))));
    ok('his court and his serpents go with him', await wait(3000, async () => !(await cnt('@e[type=minecraft:drowned,tag=bm.apcourt]')) && !(await cnt('@e[type=minecraft:vex,tag=bm.apvex]'))));
  }

  if (want('seal') || want('fight') || want('pad')) {
    // ================================================================== the pad by the door: back up
    // (walk only once the server has put the bot at the door - a teleport that lands mid-walk stops the walk)
    await run(`${H}tp TestRat ${ARRIVE[0]} ${ARRIVE[1]} ${ARRIVE[2]} 180 0`);
    await wait(4000, async () => A.pos && dist([A.pos.x, A.pos.y, A.pos.z], ARRIVE) < 0.3, 100); A.stand(); await sleep(500);
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
    ok('the Oath calls him (host + 14 parts)', await wait(4000, async () => (await cnt(pet, O)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.app_pet]', O)) === 14),
       A.bars.slice(-2).join(' / '));
    await sleep(1500);
    const pp = await epos(pet, O), cp = await epos('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_coil,limit=1]', O);
    ok('his rig stands with him', dist(pp, cp) < 4, `host ${pp} coil ${cp}`);
    const psc = await run(`${O}attribute ${pet} minecraft:scale get`), csc = await nbt('@e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_coil,limit=1]', 'transformation.scale[0]', O);
    ok('his full size, as the boss is (host scale 2.8, his rig as big as the boss\'s)', /2\.8/.test(psc) && +((csc.match(/([\d.]+)f/) || [0, 0])[1]) > 2.5, `host ${psc.slice(-12)} coil ${csc}`);
    ok('...and a click box to match', /3\.4/.test(await nbt('@e[type=minecraft:interaction,tag=bm.aphit,limit=1]', 'width', O)));
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
    const saddles = async () => +(((await run('clear TestRat minecraft:saddle 0')).match(/Found (\d+)/) || [0, 0])[1]);
    ok('...the saddle is used up', (await saddles()) === 0);
    // (ride: the Oath beside him)
    await run(`${O}tp ${pet} ${X + 0.5} ${Y} ${Z + 1.8}`); await sleep(700);
    await use(A, 0); await sleep(600);
    const riding = async () => /passed/i.test(await run('execute as TestRat on vehicle if entity @s[type=minecraft:wolf,tag=bm.appet]'));
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
    ok('"Take off the saddle": he is bare, and the saddle is yours again', b0 && (await sc('TestRat', 'bm.apsd')) === 0 && (await saddles()) === 1);
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

  console.log(`(the bot died ${deaths} times)`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  await reset(); await run('attribute TestRat minecraft:max_health base set 20');
  R.end(); A.end(); process.exit(0);
})();
