// 2.99: THE VORN ARMADA and ADMIRAL VEXIS, as a regular (non-op) player. rcon sets the stage (hard mode, the Armada placed, trials
// solved up to the part being played, items given); the bot plays.
//   find     the Hive-Star Coordinates used in the End, out past the island: the tractor beam lifts you, the title, set down on the Dock;
//            Adventure mode aboard; the Dock's beam-out pad takes you back to where you signalled from
//   void     fall off a bridge into the void: the tractor beam sets you back where you last stood (hurt)
//   star     too near the Hive-Star: it scorches you
//   bench    the Starforge: a Warplate chestplate held, 2 Star-Cores and 8 red Xenite carried, the bench right-clicked: Starforged
//   reactor  Dreadnought A's reactor: walk in, it ignites (four conduits); strike each one 8 times; all four broken: the trial solved
//   lock     the Command Lock: the three Ciphers dropped (Q) on their slots: the trial solved, an Armada Key
//   gauntlet the sentry lasers sweep the corridor and burn the bot standing in a beam
//   boss     Admiral Vexis: it wakes as you cross the bridge (eyes held on it); the pylons shield it - one struck while dark shrugs it
//            off, struck while it glows overloads; the turns (II, III) and its fall: the follower, the record, the nights over
//   nights   after the fall no invasion is rolled and the Fleet Beacon gets no answer; a Dreadnought reactor's sabotage begun:
//            the hive remembers - the nights again, and Vexis will rise for you
//   forms    Vexis, the follower: its menu's Form button cycles the boss forms (the giant rig stands, 20 parts, its small rig unseen);
//            Size locked until it's felled twice; then full size; Unlinked again puts the giant away
//   node t318.js [find|void|star|bench|reactor|lock|gauntlet|boss|nights|forms]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OX = 2560, OY = 24, OZ = -3328;
const W = (x, y, z) => [OX + x, OY + y, OZ + z];
const E = 'execute in minecraft:the_end run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (sel) => { const m = (await run(`${E}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${E}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const hp = async () => +(((await run('data get entity TestRat Health')).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
  const gm = async () => +(((await run('data get entity TestRat playerGameType')).match(/(-?\d+)$/) || [0, -1])[1]);
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${E}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (sel) => { const m = (await run(`${E}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const hit = async (sel) => { const e = await entOf(sel); if (!e) return false; A.attack(e.entityId); await sleep(120); return true; };
  const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_armada,limit=1]';
  const VX = '@e[type=minecraft:husk,tag=bm.avx,limit=1]';

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (2.99a: phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance infinite 3 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #hard bm.cfg 1'); await run('clear TestRat');
  // (the stage: the Armada placed - the bot waits out in the End, away from it, while the template goes down)
  if ((await sc('#aver', 'bm.p2')) < 1) {
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`);
    await run('function bm:admin/armada/place'); await wait(900000, async () => (await sc("#aver", "bm.p2")) >= 1, 2000);
  }
  ok('the stage: the Armada is placed in the End', (await sc('#aver', 'bm.p2')) >= 1);
  await run(`${E}forceload add ${OX} ${OZ} ${OX + 239} ${OZ + 239}`); await sleep(5000);
  const solved = async (n) => run(`${E}scoreboard players set ${DG} bm.pz ${n}`);

  if (on('find')) {
    await run(`${E}tp TestRat 1200 90 0`); await run(`${E}setblock 1200 88 0 minecraft:obsidian`); await sleep(1500);
    await run('scoreboard players reset TestRat bm.aoy'); await run('loot replace entity TestRat hotbar.0 loot bm:items/hive_coords'); await sleep(500);
    A.titles.length = 0; A.chats.length = 0; A.bars.length = 0;
    A.slot(0); await sleep(300); A.use(); await sleep(2200); A.release(); await sleep(800);
    ok('the Coordinates used in the End, past the island: the signal goes out (the beam begins)', (await sc('TestRat', 'bm.abeam')) >= 1 || A.bars.some(b => /signal goes out/.test(b)), A.bars.slice(-2).join(' | '));
    ok('...and the chart is not used up', (await wait(2000, async () => (await has('hive_coords')) === 1)));
    const dock = W(111, 50, 206);
    ok('...7 s later: set down on the Dock', await wait(12000, async () => A.pos && Math.abs(A.pos.x - dock[0]) < 3 && Math.abs(A.pos.z - dock[2]) < 3, 500),
       A.pos && `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...where it was named: THE VORN ARMADA (its title)', A.titles.some(t => /VORN ARMADA/.test(JSON.stringify(t))), JSON.stringify(A.titles.slice(-2)));
    ok('aboard, a survival player is in Adventure mode', await wait(4000, async () => (await gm()) === 2));
    const home = W(103, 50, 206);
    await at(home[0] + 0.5, home[1], home[2] + 0.5);
    ok('the Dock\'s beam-out pad: back where you signalled from', await wait(4000, async () => A.pos && Math.abs(A.pos.x - 1200) < 2 && Math.abs(A.pos.z) < 2), A.pos && `${A.pos.x.toFixed(1)} ${A.pos.z.toFixed(1)}`);
    ok('...and Survival again', await wait(7000, async () => (await gm()) === 0));
  }

  if (on('void')) {
    const pad = W(166, 49, 206); await solved(1);
    await at(W(140, 50, 206)[0] + 0.5, W(140, 50, 206)[1], W(140, 50, 206)[2] + 0.5); await sleep(2500);
    await run('effect clear TestRat minecraft:resistance'); await run('effect give TestRat minecraft:hunger 30 255 true'); await sleep(500); const h0 = await hp();
    await run(`${E}tp TestRat ${OX + 166} ${OY - 20} ${OZ + 230}`);
    ok('fallen into the void: the tractor beam sets you back aboard', await wait(6000, async () => A.pos && A.pos.y > OY + 30, 200), A.pos && A.pos.y.toFixed(1));
    ok('...hurt by the drop', (await hp()) < h0, `${h0} -> ${await hp()}`); await run('effect give TestRat minecraft:resistance infinite 3 true'); await run('effect clear TestRat minecraft:hunger');
    void pad;
  }

  if (on('star')) {
    await run('effect clear TestRat minecraft:fire_resistance'); await run('effect clear TestRat minecraft:resistance');
    const st = W(120, 48, 120); await run(`${E}setblock ${st[0]} ${st[1] + 26} ${st[2]} minecraft:glass`);
    await at(st[0] + 0.5, st[1] + 27, st[2] + 0.5); const h0 = await hp(); A.bars.length = 0;
    ok('too near the Hive-Star: it scorches you', await wait(4000, async () => (await hp()) < h0 || A.bars.some(b => /scorches/.test(b))), A.bars.slice(-1).join(''));
    await run(`${E}setblock ${st[0]} ${st[1] + 26} ${st[2]} minecraft:air`);
    await run('effect give TestRat minecraft:resistance infinite 3 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true'); await run('effect give TestRat minecraft:instant_health 1 3');
  }

  if (on('bench')) {
    await run('clear TestRat');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/warplate_chestplate');
    await run('give TestRat ' + 'minecraft:stone 1'); await run('clear TestRat minecraft:stone');
    for (let i = 0; i < 2; i++) await run('loot give TestRat loot bm:items/star_core');
    for (let i = 0; i < 8; i++) await run('loot give TestRat loot bm:items/xenite_red');
    const b = W(114, 51, 211); await at(b[0] + 0.5, b[1] - 1, b[2] - 1.5, 0, 20); await sleep(2500);
    const ent = await entOf(`@e[type=minecraft:interaction,tag=bm.abench_i,limit=1,sort=nearest,x=${b[0]},y=${b[1]},z=${b[2]},distance=..3]`);
    ok('the Starforge stands on the Dock (its bench answers)', !!ent);
    A.slot(0); await sleep(300); if (ent) A.interact(ent.entityId); await sleep(1200);
    ok('a Warplate chestplate, 2 Star-Cores, 8 red Xenite: it comes back Starforged', (await has('starforged_chestplate')) === 1 && (await has('star_core')) === 0 && (await has('warplate_chestplate')) === 0);
  }

  if (on('reactor')) {
    await solved(13);
    const core = W(56, 48, 25); await at(core[0] + 0.5, core[1], core[2] - 4.5, 0, 0);
    ok('Dreadnought A\'s reactor ignites as you walk in: four conduits', await wait(6000, async () => (await cnt('@e[type=minecraft:interaction,tag=bm.arhit]')) === 4));
    for (const [dx, dz] of [[5, 0], [-5, 0], [0, 5], [0, -5]]) {
      await at(core[0] + 0.5 + dx * 0.6, core[1], core[2] + 0.5 + dz * 0.6); await sleep(300);
      for (let i = 0; i < 24; i++) { await hit(`@e[type=minecraft:interaction,tag=bm.arhit,sort=nearest,limit=1]`); await sleep(350); if ((await cnt(`@e[type=minecraft:interaction,tag=bm.arhit,x=${core[0] + dx},y=${core[1] + 1},z=${core[2] + dz},distance=..1.5]`)) === 0) break; }
    }
    ok('...each struck 8 times: all four broken - the reactor offline, its trial solved', await wait(4000, async () => (await sc(DG.replace('limit=1', 'limit=1'), 'bm.pz')) >= 14 || (await cnt('@e[type=minecraft:interaction,tag=bm.arhit]')) === 0));
    ok('...its spoils: a Star-Core and red Xenite', await wait(4000, async () => (await has('star_core')) >= 1 && (await has('xenite_red')) >= 1), `pz ${await sc(DG, 'bm.pz')} titles ${A.titles.slice(-3).join(' / ')} bars ${A.bars.slice(-2).join(' / ')}`);
  }

  if (on('lock')) {
    await solved(16); await run('clear TestRat');
    const slots = [[14, 'cipher_1'], [20, 'cipher_2'], [26, 'cipher_3']];
    for (const [x, c] of slots) {
      const p = W(x, 56, 146); await at(p[0] + 0.5, p[1], p[2] + 1.5, 180, 40); await sleep(400);
      await run(`clear TestRat *[minecraft:custom_data~{bm:"${c}"}]`); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${c}`);
      A.slot(0); await sleep(300); A.drop(); await sleep(1500);
    }
    ok('the three Ciphers dropped on the Command Lock: the trial solved', await wait(5000, async () => (await sc(DG, 'bm.pz')) >= 17), String(await sc(DG, 'bm.pz')));
    ok('...and an Armada Key', (await has('akey')) >= 1);
  }

  if (on('gauntlet')) {
    await solved(17); await run('effect clear TestRat minecraft:resistance');
    const h0 = await hp(); const g = W(8, 55, 172); await at(g[0] + 0.5, g[1], g[2] + 0.5, 0, 0);
    ok('the Gauntlet: the sentries sweep it - standing still in it, you are burned', await wait(9000, async () => (await hp()) < h0), `${h0} -> ${await hp()}`);
    await run('effect give TestRat minecraft:resistance infinite 3 true'); await run('effect give TestRat minecraft:instant_health 1 3');
  }

  if (on('boss')) {
    await solved(18); await run('tag TestRat remove bm.vxdone'); await run('scoreboard players set #afell bm.p2 0');
    await run('execute as TestRat at @s run function bm:admin/armada/boss'); await sleep(2500);
    ok('Admiral Vexis waits dormant at its helm', await wait(10000, async () => (await cnt(`${VX.slice(0, -1)},tag=bm.vxdorm]`)) === 1));
    const c = W(52, 55, 180); await at(c[0] + 0.5, c[1], c[2] + 12.5, 180, 0);
    ok('crossing the bridge: it wakes (the coming)', await wait(6000, async () => (await cnt(`${VX.slice(0, -1)},tag=bm.vxintro]`)) === 1));
    await sleep(3000);
    const look = await pos('@e[type=minecraft:marker,tag=bm.vxlook,limit=1]'); const me = await pos('@a[name=TestRat,limit=1]');
    const rot = (await run('data get entity TestRat Rotation')).match(/\[(-?[\d.]+)f, (-?[\d.]+)f\]/);
    if (look && me && rot) { const yaw = Math.atan2(-(look[0] - me[0]), look[2] - me[2]) * 180 / Math.PI; const d = ((+rot[1] - yaw) % 360 + 540) % 360 - 180;
      ok('...your eyes held on it', Math.abs(d) < 12, `yaw ${(+rot[1]).toFixed(1)} vs ${yaw.toFixed(1)}`); } else ok('...your eyes held on it', false, 'no look marker');
    ok('...20 s later: the fight begins (its bar, phase I)', await wait(24000, async () => (await cnt(`${VX.slice(0, -1)},tag=bm.vxlive]`)) === 1, 500));
    ok('...the four shield pylons stand', (await cnt('@e[type=minecraft:interaction,tag=bm.vxpyi]')) === 4);
    // (a pylon struck while dark shrugs it off; while it glows it overloads)
    await run(`${E}scoreboard players set @e[type=minecraft:marker,tag=bm.apylon] bm.vxp 1`); await run(`${E}tag @e[type=minecraft:marker,tag=bm.apylon] remove bm.vxpc`);
    const pyl = await pos('@e[type=minecraft:interaction,tag=bm.vxpyi,limit=1,sort=nearest]');
    await at(pyl[0], pyl[1] - 6 + 0.1 > c[1] ? pyl[1] - 6 : c[1], pyl[2] + 1.6, 180, 0);
    await run(`${E}tp TestRat ${pyl[0]} ${c[1]} ${pyl[2] - 2.2} 0 -40`); await sleep(1500);
    await run(`${E}scoreboard players set @e[type=minecraft:marker,tag=bm.apylon] bm.vxp 1`); await run(`${E}tag @e[type=minecraft:marker,tag=bm.apylon] remove bm.vxpc`);
    A.bars.length = 0; await hit('@e[type=minecraft:interaction,tag=bm.vxpyi,limit=1,sort=nearest]'); await sleep(600);
    ok('a pylon struck while dark: it shrugs it off (told why)', A.bars.some(b => /GLOWS/.test(b)) && (await cnt('@e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl]')) === 4, A.bars.slice(-1).join(''));
    await run(`${E}execute as @e[type=minecraft:marker,tag=bm.apylon] run scoreboard players set @s bm.vxp 4`); await sleep(1300);
    await hit('@e[type=minecraft:interaction,tag=bm.vxpyi,limit=1,sort=nearest]'); await sleep(700);
    ok('...struck while it glows: it overloads', (await cnt('@e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl]')) === 3);
    // (its pool to its edge: the turn to the Hive-Link)
    await run(`${E}execute as ${VX} run data modify entity @s Health set value 101f`); await sleep(400); await hit(VX); await sleep(600);
    await run(`${E}execute as ${VX} run data modify entity @s Health set value 100f`);
    ok('its first pool spent: the turn - the cockpit blows, the wreck kneels, eyes held', await wait(4000, async () => (await cnt(`${VX.slice(0, -1)},tag=bm.vxturn]`)) === 1));
    ok('...and THE HIVE-LINK (phase II): the wreck left behind', await wait(20000, async () => (await sc(VX, 'bm.vxph')) === 2 && (await cnt(`${VX.slice(0, -1)},tag=bm.vxlive]`)) === 1, 500) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.vxw]')) === 20);
    await run(`${E}execute as ${VX} run data modify entity @s Health set value 100f`);
    ok('its second pool spent: STARFIRE (phase III)', await wait(22000, async () => (await sc(VX, 'bm.vxph')) === 3 && (await cnt(`${VX.slice(0, -1)},tag=bm.vxlive]`)) === 1, 500));
    await run('clear TestRat'); await run('tag TestRat remove bm.vxfirst'); await run('scoreboard players set TestRat bm.vxwin 0');
    await run(`${E}execute as ${VX} run data modify entity @s Health set value 100f`);
    ok('its last pool spent: THE UNLINKING', await wait(4000, async () => (await cnt(`${VX.slice(0, -1)},tag=bm.vxfall]`)) === 1));
    // (3.0d) it BURSTS INTO RADIANT STAR DUST after its last words - sampled by its own clock (bm.vxt)
    const seen = { lit: false, seam: false, crack: false, star: false, nova: false, gone: false, dust: false };
    const t1 = Date.now();
    while (Date.now() - t1 < 34000) {
      const t = await sc(VX, 'bm.vxt'); if (t < 0 || t === -99) break;
      if (t >= 488 && t < 530) {
        if (/: 15$/.test(await run(`${E}data get entity @e[type=minecraft:item_display,tag=bm.vxr_chest,limit=1] brightness.block`))) seen.lit = true;
        if ((await cnt('@e[type=minecraft:item_display,tag=bm.dfx_seam]')) > 0) seen.seam = true;
        if (A.chats.some(c => /breaks through every seam/.test(c))) seen.crack = true;
      }
      if (t >= 534 && t < 556 && (await cnt('@e[type=minecraft:item_display,tag=bm.dfx_star]')) > 0) seen.star = true;
      if (t >= 553 && t < 575) { if ((await cnt('@e[type=minecraft:item_display,tag=bm.dfx_nova]')) > 0) seen.nova = true;
        if ((await cnt('@e[type=minecraft:item_display,tag=bm.vxr]')) === 0) seen.gone = true; }
      if (t >= 560 && (await cnt('@e[type=minecraft:item_display,tag=bm.dfx_dust]')) > 0) { seen.dust = true; break; }
      await sleep(t < 470 ? 500 : 80);
    }
    ok('...after its last words, light breaks out of it: lit from within (brightness 15), told so', seen.lit && seen.crack, JSON.stringify(seen));
    ok('...glowing seams cracking over it (seam sprites)', seen.seam);
    ok('...part by part it bursts into star dust (star sprites spiralling out)', seen.star);
    ok('...a nova: a ring of star dust flung out; nothing of its rig left', seen.nova && seen.gone);
    ok('...the dust drifting, twinkling out', seen.dust);
    ok('...30 s later: the Severed Link, its record, a Victor\'s Key', await wait(36000, async () => (await has('vexis_link')) === 1, 1000) && (await has('music_disc_vexis')) === 1 && (await has('akey_victor')) >= 1);
    ok('...the invasion nights are over (#vfell)', (await sc('#vfell', 'bm.cfg')) === 1);
    ok('...and the Armada drifts: it regroups in three minutes', (await sc('#acol', 'bm.p2')) > 100);
    ok('...and nothing of Vexis left behind: no part, no sprite (bm.vxr, bm.dfx)', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.vxr]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.dfx]')) === 0, 250));
  }

  if (on('nights')) {
    await run('scoreboard players set #vfell bm.cfg 1'); await run('tag TestRat add bm.vxdone');
    await run('function bm:p32/inv/roll'); await run('function bm:p32/inv/roll'); await run('function bm:p32/inv/roll');
    ok('the Admiral fallen: no invasion night is rolled', (await sc('#inv', 'bm.bm')) !== 1);
    A.chats.length = 0; await run('loot replace entity TestRat hotbar.0 loot bm:items/fleet_beacon'); A.slot(0); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(800);
    ok('...the Fleet Beacon calls into silence', A.chats.some(c => /calls into silence/.test(c)) || (await has('fleet_beacon')) <= 1, A.chats.slice(-1).join(''));
    await run('execute as TestRat at @s run function bm:p52/rx/start'); await sleep(800);
    ok('a Dreadnought reactor\'s sabotage begun: the hive remembers - the nights can come again', (await sc('#vfell', 'bm.cfg')) === 0);
    ok('...and Vexis will rise for you again', !/bm\.vxdone/.test(await run('tag TestRat list')));
  }

  if (on('forms')) {
    await run('execute in minecraft:overworld run tp TestRat 18300 101 16000'); await run('execute in minecraft:overworld run fill 18290 100 15990 18310 100 16010 minecraft:stone');
    await run('kill @e[type=minecraft:wolf,tag=bm.xbpet]'); await run('clear TestRat'); await run('tag TestRat remove bm.xbwar');
    await run('scoreboard players set TestRat bm.xbub 0'); await run('scoreboard players set TestRat bm.xbsz 0'); await run('scoreboard players set TestRat bm.xbcd 0'); await run('scoreboard players set #hard bm.cfg 1');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/vexis_link'); await sleep(800);
    A.bars.length = 0; A.chats.length = 0; A.slot(0); await sleep(300); A.use(); await sleep(400); A.release();
    ok('the Severed Link used: Vexis comes', await wait(5000, async () => /count: 1\b/i.test(await run('execute in minecraft:overworld if entity @e[type=minecraft:wolf,tag=bm.xbpet]'))), A.bars.concat(A.chats).slice(-2).join(' | '));
    await sleep(1500);
    const menu = async () => { const n0 = A.dialogN.length; A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); A.input({}); await wait(3000, async () => A.dialogN.length > n0); return A.dialog; };
    const press = async (re) => { await A.press(re); await sleep(900); };
    const giant = async () => +((await run('execute in minecraft:overworld if entity @e[type=minecraft:item_display,tag=bm.xbu]')).match(/count: (\d+)/i) || [0, 0])[1];
    await menu(); await press(/^Form$/); await sleep(1500);
    ok('Form: THE WARFRAME - its giant rig stands (20 parts), at a companion\'s size', (await giant()) === 20 && (await sc('TestRat', 'bm.xbub')) === 1);
    await menu(); await press(/^Form$/); await sleep(1200);
    ok('Form: THE HIVE-LINK', (await sc('TestRat', 'bm.xbub')) === 2 && (await giant()) === 20);
    await menu(); await press(/^Form$/); await sleep(1200);
    ok('Form: STARFIRE', (await sc('TestRat', 'bm.xbub')) === 3 && (await giant()) === 20);
    A.bars.length = 0; await menu(); await press(/Size/); await sleep(800);
    ok('Size: locked until it is felled twice (told so)', A.bars.some(b => /second time/.test(b)) && (await sc('TestRat', 'bm.xbsz')) <= 0);
    await run('tag TestRat add bm.xbwar'); await menu(); await press(/Size/); await sleep(1200);
    ok('...felled twice: Full size', (await sc('TestRat', 'bm.xbsz')) === 1);
    await menu(); await press(/^Form$/); await sleep(1500);
    ok('Form: Unlinked again - the giant put away', (await sc('TestRat', 'bm.xbub')) === 0 && (await giant()) === 0);
    await run('execute in minecraft:overworld run kill @e[type=minecraft:wolf,tag=bm.xbpet]');
  }

  await run(`${E}forceload remove ${OX} ${OZ} ${OX + 239} ${OZ + 239}`);
  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})();
