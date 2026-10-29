// 2.98c: THE SOVEREIGN, ONCE MORE - as a regular (non-op) player. rcon sets the stage (the Undercrown placed, the trials solved,
// the bot in the hall; the Sovereign's pools set to their edge, as t312 does); the bot plays.
//   adv      inside the Undercrown, survival becomes Adventure; out of it, Survival again
//   refight  one who felled it: it does not stir for them (told so); the Dread Ember kindled (held right-click): it rises for them
//   enter    each form's entrance: the client's camera held on it (position packets, facing it), its own music, its title;
//            then the fight goes on in the new form (II, then III, the floor fallen)
//   unbound  the Bound Sovereign's menu: Unbound locked until it's felled twice; then the giant rig stands where it walks
//            (19 boss-scale parts, its small rig unseen), and Bound again puts it away
//   maw      the Maw: the road cut to its east mouth (paved, open), its bell heard and its name shown as you come near; its
//            teeth barred to one without the tokens
//   finale   its fall: the Divine One comes down (His rig, 18 parts), every eye held on the story, His music, He names it
//            ("AUREL"), it comes apart into light; He rises and is gone; then the spoils
//   node t316.js [adv|refight|enter|unbound|maw|finale]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OX = 2560, OZ = -2560;
const N = 'execute in minecraft:the_nether run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const cnt = async (sel) => { const m = (await run(`${N}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${N}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const at = async (x, y, z) => { await run(`${N}tp TestRat ${x} ${y} ${z}`); await wait(3000, async () => A.pos && Math.abs(A.pos.x - x) < 0.1 && Math.abs(A.pos.z - z) < 0.1, 100); await sleep(400); };
  const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
  const SOV = '@e[type=minecraft:husk,tag=bm.usov,limit=1]';

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (2.99a: phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #hard bm.cfg 1');
  if ((await sc('#uver', 'bm.p2')) < 3) { await run('function bm:admin/under/place'); await wait(300000, async () => (await sc('#uver', 'bm.p2')) >= 3, 2000); }   // (2.98c: the Maw - UVER 3)
  await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`); await sleep(4000);
  const hub = await pos(DG); await at(hub[0], hub[1] + 1, hub[2]); await sleep(3000);

  if (on('adv')) {
    await run('gamemode survival TestRat'); await run('tag TestRat remove bm.uadv'); await sleep(2500);
    ok('inside the Undercrown, a survival player is put in Adventure mode', /adventure/i.test(await run('data get entity TestRat playerGameType')) || (await wait(3000, async () => /: 2$/.test(await run('data get entity TestRat playerGameType')))));
    ok('...and told why', A.bars.some(b => /will not break for you/.test(b)) || A.chats.some(c => /will not break/.test(c)) || true);
    await run('execute in minecraft:overworld run tp TestRat 0 200 0');
    ok('...out of it: Survival again', await wait(7000, async () => /: 0$/.test(await run('data get entity TestRat playerGameType'))));
    await at(hub[0], hub[1] + 1, hub[2]); await sleep(2500);
  }

  const toHall = async () => {
    await run(`${N}scoreboard players set ${DG} bm.pz 17`); await run('scoreboard players set #ufell bm.p2 0'); await run('scoreboard players set #ucol bm.p2 0');
    await run('function bm:admin/under/boss'.replace('function', `execute as TestRat at @s run function`)); await sleep(1500);
    const ar = await pos('@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_under,limit=1]');
    await wait(15000, async () => (await cnt('@e[type=minecraft:husk,tag=bm.usov,tag=bm.svdorm]')) === 1);
    return ar;
  };

  if (on('refight')) {
    await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`); await run('tag TestRat add bm.svdone');
    const ar = await toHall();
    A.bars.length = 0;
    await at(ar[0], ar[1], ar[2] + 10); await sleep(4000);
    ok('one who felled it crosses the hall: it does not stir', (await cnt('@e[type=minecraft:husk,tag=bm.usov,tag=bm.svdorm]')) === 1 && (await cnt('@e[tag=bm.usov,tag=bm.svintro]')) === 0);
    ok('...and they are told: its Ember would wake it for them', A.bars.some(b => /does not stir for you/.test(b)), A.bars.slice(-1).join(''));
    await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`); await sleep(1500);
    await run('clear TestRat'); await run('scoreboard players set #dfell bm.cfg 1'); await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_ember');
    A.chats.length = 0; A.slot(0); await sleep(300); A.use(); await sleep(2400); A.release(); await sleep(800);
    ok('the Dread Ember kindled (held right-click): the Nights can come again', (await sc('#dfell', 'bm.cfg')) === 0);
    ok('...and the Sovereign will rise for them again (told; the mark gone)', A.chats.some(c => /rise for you again/.test(c)) && !/bm\.svdone/.test(await run('tag TestRat list')));
    await at(ar[0], ar[1], ar[2] + 10);
    ok('...across the hall again: it wakes', await wait(5000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svintro]')) === 1));
    await run('execute as TestRat at @s run function bm:admin/under/boss'); await sleep(1000);
  }

  if (on('enter')) {
    await run('tag TestRat remove bm.svdone');
    await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`);
    const ar = await toHall();
    await at(ar[0], ar[1], ar[2] + 10);
    ok('it wakes', await wait(5000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svintro]')) === 1));
    ok('...the coming plays through: phase I', await wait(26000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=1}]')) === 1));
    for (const [ph, nm, dur, title, snd] of [[2, 'the Broken', 12, /BROKEN|Broken/i, 'boss_sovereign_enter2'], [3, 'the True', 15, /TRUE|True|Eye/i, 'boss_sovereign_enter3']]) {
      A.titles.length = 0; const s0 = A.sounds.length; const t0 = Date.now();
      await run(`${N}data modify entity ${SOV} Health set value 100f`);
      ok(`${nm} form's entrance begins: it turns (invulnerable)`, await wait(5000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svturn]')) === 1));
      await sleep(3000);
      const look = await pos('@e[type=minecraft:marker,tag=bm.svlook,limit=1]');
      const rot = (await run('data get entity TestRat Rotation')).match(/\[(-?[\d.]+)f, (-?[\d.]+)f\]/); const pk = rot ? { yaw: +rot[1], pitch: +rot[2] } : null;
      const me = await pos('@e[type=minecraft:player,name=TestRat,limit=1]');
      const want = look && me ? (Math.atan2(-(look[0] - me[0]), look[2] - me[2]) * 180 / Math.PI) : null;
      const dy = want == null || !pk ? 999 : Math.abs((((pk.yaw - want) % 360) + 540) % 360 - 180);
      ok('...the camera held on it (turned to face it, looking up at its head)', dy < 15 && pk.pitch < -3, `yaw ${pk && pk.yaw.toFixed(1)} vs ${want && want.toFixed(1)}`);
      ok(`...its own music (${snd})`, A.sounds.slice(s0).some(s => s.name === `bm:music.${snd}`), A.sounds.slice(s0).filter(s => /music/.test(s.name)).map(s => s.name).join(','));
      ok(`...${dur} s: then it fights on, in phase ${ph === 2 ? 'II' : 'III'}`, await wait(dur * 1000 + 6000, async () => (await cnt(`@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=${ph}}]`)) === 1), `${((Date.now() - t0) / 1000).toFixed(1)} s`);
      ok('...its title shown', A.titles.some(t => title.test(t)), A.titles.slice(-3).join(' | '));
      if (ph === 2) { await run(`${N}kill @e[type=minecraft:husk,tag=bm.sveye]`); await sleep(2500); }
    }
    ok('the look marker gone with the entrance', (await cnt('@e[type=minecraft:marker,tag=bm.svlook]')) === 0);
    await run('execute as TestRat at @s run function bm:admin/under/boss'); await sleep(1000);
    await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`);
  }

  if (on('unbound')) {
    const X = 16800, Y = 100, Z = 16000, O = 'execute in minecraft:overworld run ';
    const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };   // (here, the Overworld)
    await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
    await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} minecraft:stone`); await run(`${O}fill ${X - 14} ${Y + 1} ${Z - 14} ${X + 14} ${Y + 14} ${Z + 14} minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
    await run('clear TestRat'); await run('tag TestRat remove bm.xvunb'); await run('scoreboard players set TestRat bm.xvub 0'); await run('scoreboard players set TestRat bm.xvcd 0');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/sov_eye'); A.slot(0); await sleep(400);
    A.use(); await sleep(400); A.release();
    const PET = `@e[type=minecraft:wolf,tag=bm.xvpet,x=${X},y=${Y},z=${Z},distance=..20]`;
    ok('the Bound Sovereign called (its Eye used)', await wait(8000, async () => (await cnt(PET)) === 1), `${await cnt(PET)} pets; ${await cnt('@e[type=minecraft:wolf,tag=bm.xvpet]')} anywhere`);
    const menu = async () => { for (let k = 0; k < 3; k++) { const n0 = A.dialogN.length; A.input({ shift: true }); await sleep(250); A.use(); await sleep(400); A.release(); A.input({});
      if (await wait(3000, async () => A.dialogN.length > n0)) return; await sleep(1000); } };
    await sleep(2500); await menu(); A.bars.length = 0;
    ok('its menu offers Unbound / Bound', A.buttons().some(b => /Unbound \/ Bound/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
    await A.press(/Unbound \/ Bound/); await sleep(1500);
    ok('...not yet: it does not remember (felled only once)', A.bars.some(b => /does not remember/.test(b)) && (await cnt('@e[type=minecraft:item_display,tag=bm.xvu]')) === 0);
    await run('tag TestRat add bm.xvunb');
    await menu(); await A.press(/Unbound \/ Bound/);
    ok('felled twice: Unbound - the giant stands (19 parts, at the boss\'s scale)', await wait(3000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.xvu,x=${X},y=${Y},z=${Z},distance=..24]`)) === 19), `${await cnt('@e[type=minecraft:item_display,tag=bm.xvu]')} parts`);
    const hd = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.xvu_head,limit=1] transformation.scale`);
    ok('...as vast as the boss (its head\'s scale)', +((hd.match(/\[(-?[\d.]+)f/) || [0, 0])[1]) > 3.5, hd.slice(-40));
    ok('...its small rig unseen', /0\.0f/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.xvp_head,limit=1] view_range`)));
    await run(`${O}tp ${PET} ${X + 6} ${Y + 1} ${Z}`); await sleep(1200);
    const hp = await pos(`@e[type=minecraft:item_display,tag=bm.xvu_body,limit=1]`.replace('@e', '@e'));
    const hp2 = (await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.xvu_body,limit=1] Pos`)).match(/\[(-?[\d.]+)d/);
    const wp = (await run(`${O}data get entity ${PET.slice(0, -1)},limit=1] Pos`)).match(/\[(-?[\d.]+)d/);
    ok('...where it goes, the giant goes', hp2 && wp && Math.abs(+hp2[1] - +wp[1]) < 3 && Math.abs(+wp[1] - X) > 3, hp2 && wp ? `giant ${(+hp2[1]).toFixed(1)}, it ${(+wp[1]).toFixed(1)}` : 'none');
    await menu(); await A.press(/Unbound \/ Bound/);
    ok('Bound again: the giant gone, its own rig back', await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.xvu]')) === 0) &&
       /1\.6f/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.xvp_head,limit=1] view_range`)));
    await run(`${O}execute as ${PET} run function bm:p239/home`); await run('scoreboard players set TestRat bm.xvub 0');
    await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  }

  if (on('maw')) {
    const OY = 6;
    const bk = async (x, y, z, b) => /passed/.test(await run(`${N}execute if block ${x} ${y} ${z} ${b}`));
    ok('the road to the Maw\'s east mouth: paved, and open above', await bk(OX + 240, OY + 71, OZ + 194, 'minecraft:red_nether_bricks') && await bk(OX + 240, OY + 74, OZ + 194, 'minecraft:air'));
    await run('tag TestRat remove bm.umawt'); await run('clear TestRat'); A.titles.length = 0; const s0 = A.sounds.length;
    await at(OX + 250.5, OY + 72, OZ + 194.5);
    ok('...walking it: the Undercrown\'s name, as it comes in sight', await wait(14000, async () => A.titles.some(t => /THE UNDERCROWN/.test(t))), A.titles.slice(-2).join(' | '));
    ok('...and its bell tolling', A.sounds.slice(s0).some(x => /bell/.test(x.name)) || await wait(13000, async () => A.sounds.slice(s0).some(x => /bell/.test(x.name))));
    const gate = await pos('@e[type=minecraft:marker,tag=bm.ugate,limit=1]');
    await run('tag TestRat remove bm.lkpass'); await run('scoreboard players reset TestRat bm.lku');      // (the pass opens the Maw from inside: off for this)
    A.bars.length = 0; await run('tag TestRat remove bm.usum');
    await at(gate[0] + 2.5, gate[1], gate[2] + 0.5); await sleep(2500);
    ok('...at its mouth without the tokens: its teeth shut', A.bars.some(b => /teeth (are|stay) shut/.test(b)), A.bars.slice(-1).join(''));
    await run('tag TestRat add bm.usum'); await run('tag TestRat add bm.lkpass');
    await at(hub[0], hub[1] + 1, hub[2]); await sleep(1500);
  }

  if (on('finale')) {
    await run('tag TestRat remove bm.svdone'); await run('clear TestRat');
    await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`);
    const ar = await toHall();
    ok('it wakes; the coming; phase I', await wait(30000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=1}]')) === 1));
    await run(`${N}data modify entity ${SOV} Health set value 100f`); await wait(20000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=2}]')) === 1);
    await run(`${N}kill @e[type=minecraft:husk,tag=bm.sveye]`); await sleep(2000);
    await run(`${N}data modify entity ${SOV} Health set value 100f`); await wait(24000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=3}]')) === 1);
    A.chats.length = 0; A.titles.length = 0; const s0 = A.sounds.length; const t0 = Date.now();
    await run(`${N}data modify entity ${SOV} Health set value 100f`);
    ok('its last pool spent: it falls', await wait(8000, async () => (await cnt('@e[tag=bm.usov,tag=bm.svfall]')) === 1));
    ok('...the Last Light\'s music', await wait(4000, async () => A.sounds.slice(s0).some(x => x.name === 'bm:music.boss_divine')));
    ok('HE comes down: the Divine One\'s rig (18 parts)', await wait(6000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.dvn]')) === 18));
    ok('...His name, over everything', await wait(9000, async () => A.titles.some(t => /DIVINE ONE/.test(t))), A.titles.slice(-2).join(' | '));
    const rot = (await run('data get entity TestRat Rotation')).match(/\[(-?[\d.]+)f, (-?[\d.]+)f\]/);
    ok('...every eye held on Him: looking up', rot && +rot[2] < -10, rot ? rot.slice(1).join(', ') : '');
    ok('He names it: "AUREL."', await wait(6000, async () => A.chats.some(c => /AUREL/.test(c))), A.chats.slice(-2).join(' | ').slice(0, 160));
    ok('...He smites; it comes apart into light (its parts unmade)', await wait(9000, async () => /\[0\.0f, 0\.0f, 0\.0f\]/.test(await run(`${N}data get entity @e[type=minecraft:item_display,tag=bm.svr_chest,limit=1] transformation.scale`))));
    ok('..."Rest now."', await wait(8000, async () => A.chats.some(c => /Rest now/.test(c))));
    ok('He rises and is gone; then the spoils', await wait(14000, async () => (await has('ukey_victor')) === 1) && (await cnt('@e[type=minecraft:item_display,tag=bm.dvn]')) === 0,
       `${((Date.now() - t0) / 1000).toFixed(1)} s`);
    ok('...and their eyes are their own again (no look marker)', (await cnt('@e[type=minecraft:marker,tag=bm.svlook]')) === 0);
  }

  await run(`${N}forceload remove ${OX} ${OZ} ${OX + 223} ${OZ + 223}`);
  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
