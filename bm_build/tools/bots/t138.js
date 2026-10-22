// 2.77b: follower figurines in display cases, as a regular (non-op) player: a case set down with the case item itself, a
// follower's summoning item right-clicked into it (a little statue of them appears on the cushion - all ten followers), a
// punch to show the item instead and another for the figurine, sneak + right-click to turn it, empty-handed to take it
// out; a wall case with Apophiss's Oath in it, picked up again; an ordinary item still shown as itself. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (C, slot) => { C.slot(slot); await sleep(250); C.use(); await sleep(400); C.release(); await sleep(300); };
  const X = 16120, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const FIG = '@e[type=minecraft:item_display,tag=bm.dcfg]';
  const figs = () => cnt(FIG);
  const scaleOf = async (sel) => +(((await nbt(sel, 'transformation.scale[0]')).match(/(-?[\d.]+)f/) || [0, NaN])[1]);

  // ---------------------------------------------------------------- a floor case, set down with the case itself; Leo's crest in it
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 70);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/display_case_oak'); await run('loot replace entity TestRat hotbar.1 loot bm:items/leo_crest');
  await use(A, 0);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  ok('the case is set down in front of the bot (floor)', (await cnt(caseSel)) === 1);
  const itemSel = `@e[type=minecraft:item_display,tag=bm.dcitem,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  let box = await entOf(A, caseSel);
  A.slot(1); await sleep(300); A.bars.length = 0;
  if (box) A.interact(box.entityId); await sleep(700);
  ok('Leo\'s crest right-clicked into it: a little Leo stands on the cushion (7 parts)', (await figs()) === 7, `parts ${await figs()}`);
  ok('...the crest is in the case (and out of the hand)', /leo_crest/.test(await nbt(itemSel, 'item')) && (await has('TestRat', 'leo_crest')) === 0);
  ok('...the crest itself is hidden while he stands there', (await scaleOf(itemSel)) === 0);
  ok('...the bot is told how to have the item instead', /Punch the case to show the item/.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 120));
  const sc = await scaleOf(`${FIG.slice(0, -1)},limit=1]`);
  ok('...shrunk to fit (a figurine, not Leo)', sc > 0.1 && sc < 0.32, `part scale ${sc}`);
  const ys = []; for (let k = 0; k < 7; k++) ys.push(+(((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.dcfg,limit=1,sort=random] transformation.translation[1]`)).match(/(-?[\d.]+)f/) || [0, 0])[1]));
  ok('...standing on the cushion, about as tall as the glass allows', Math.min(...ys) >= -0.01 && Math.max(...ys) < 0.62, `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
  const cy = +(((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.dcase,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1] Rotation[0]`)).match(/(-?[\d.]+)f/) || [0, NaN])[1]);
  const fy = +(((await run(`${O}data get entity ${FIG.slice(0, -1)},limit=1] Rotation[0]`)).match(/(-?[\d.]+)f/) || [0, NaN])[1]);
  ok('...facing out of the case, as the case faces', Math.abs(((cy - fy) % 360 + 540) % 360 - 180) < 1, `case ${cy} figure ${fy}`);
  { const stray = `@e[type=!minecraft:player,type=!minecraft:item_display,type=!minecraft:interaction,type=!minecraft:marker,type=!minecraft:text_display,x=${X},y=${Y},z=${Z},distance=..6]`;
    ok('...still as stone (display parts only - nothing with AI)', (await cnt(stray)) === 0, (await run(`${O}execute as ${stray.slice(0, -1)},limit=1] at @s run tp @s ~ ~ ~`)).slice(0, 140)); }
  // (punch: the item; again: the figurine)
  A.bars.length = 0; box = await entOf(A, caseSel); if (box) A.attack(box.entityId); await sleep(700);
  ok('a punch: the crest itself on show, the figurine gone', (await figs()) === 0 && Math.abs((await scaleOf(itemSel)) - 0.5) < 0.01, A.bars.slice(-1).join('').slice(0, 120));
  ok('..."The item itself. (Punch again for the figurine.)"', /The item itself/.test(A.bars.join(' ')));
  ok('...and the case is still there (only sneak + punch picks it up)', (await cnt(caseSel)) === 1);
  await sleep(400); A.bars.length = 0; if (box) A.attack(box.entityId); await sleep(700);
  ok('another punch: the figurine is back', (await figs()) === 7 && (await scaleOf(itemSel)) === 0, A.bars.slice(-1).join('').slice(0, 120));
  // (sneak + right-click: the case turns it)
  A.slot(4); await sleep(250); A.input({ shift: true }); await sleep(250); if (box) A.interact(box.entityId, true); await sleep(400); A.input({}); await sleep(300);
  const r0 = await nbt(`${FIG.slice(0, -1)},limit=1,sort=nearest]`, 'Rotation[0]'); await sleep(700); const r1 = await nbt(`${FIG.slice(0, -1)},limit=1,sort=nearest]`, 'Rotation[0]');
  ok('sneak + right-click: the figurine turns', (await cnt('@e[type=minecraft:item_display,tag=bm.dcfg,tag=bm.dcmspin]')) === 7 && r0 !== r1, `${r0.slice(-9)} -> ${r1.slice(-9)}`);
  A.input({ shift: true }); await sleep(250); if (box) A.interact(box.entityId, true); await sleep(400); A.input({}); await sleep(300);
  // (empty-handed: the crest comes back out, and Leo with it)
  A.slot(5); await sleep(250); if (box) A.interact(box.entityId); await sleep(700);
  ok('empty-handed: the crest comes back out - and the figurine goes', (await has('TestRat', 'leo_crest')) === 1 && (await figs()) === 0);
  await run('clear TestRat');      // (the crest came back into the hand that took it out: empty hands again)

  // ---------------------------------------------------------------- every follower's own figure
  const fdir = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p134/fig/';
  const parts = iid => (require('fs').readFileSync(fdir + `floor_${iid}.mcfunction`, 'utf8').match(/^summon /gm) || []).length;
  const NFROG = parts('frog_signet'), NDON = parts('donado_tag');
  const ALL = [['celi_charm', 'Celi', 9], ['demo_seal', 'Democratus', 8], ['emma_ribbon', 'Emma', 6], ['kw_spark', 'KillerWatt', 8], ['apo_oath', 'Apophiss', 12],
               ['tul_coin', 'Tullius', 9], ['donadian_medal', 'Zib', 9], ['cecil_gem', 'Cecil', 5], ['pearl_card', 'Pearlman', 1],
               ['frog_signet', 'the Frog with Mustache', NFROG], ['donado_tag', 'Donado', NDON], ['wilfrey_locket', 'Wilfrey', 1], ['fy_bowl', 'Fishy', 9],
               ['dw_horn', 'Dennis', 9], ['pi_cloche', 'Pistachio', 8], ['om_monocle', 'Omega', 12], ['ashur_cinder', 'Ashur', 9], ['chef_ladle', 'The Chef', 9], ['neighbor_baton', 'The Neighbor', 11],
               ['av_locket', 'Queen Ava', 8], ['pq_pearls', 'Queen Pearl', 9], ['bo_claw', 'Bloo', 11], ['st_hook', 'The Stalker', 10], ['ln_gourd', 'The Arachno-Lantern', 11], ['bv_ball', 'Bender', 7], ['bn_whistle', 'Bones', 8]];
  for (const [iid, name, n] of ALL) {
    await run(`loot replace entity TestRat hotbar.2 loot bm:items/${iid}`); A.slot(2); await sleep(300);
    box = await entOf(A, caseSel); if (box) A.interact(box.entityId); await sleep(700);
    const got = await figs(); const mx = await scaleOf(`${FIG.slice(0, -1)},limit=1]`);
    ok(`${name}: their figurine (${n} parts)`, got === n && /\d/.test(String(mx)), `parts ${got}`);
    A.slot(5); await sleep(250); box = await entOf(A, caseSel); if (box) A.interact(box.entityId); await sleep(600);
    if (!ok(`...and out again`, (await has('TestRat', iid)) === 1 && (await figs()) === 0)) break;
    await run('clear TestRat');
  }

  // ---------------------------------------------------------------- an ordinary item: just the item, and a punch says what it always said
  await run('item replace entity TestRat hotbar.3 with minecraft:diamond'); A.slot(3); await sleep(300);
  box = await entOf(A, caseSel); if (box) A.interact(box.entityId); await sleep(600);
  ok('a diamond in the case: shown as itself (no figurine)', (await figs()) === 0 && /diamond/.test(await nbt(itemSel, 'item')) && Math.abs((await scaleOf(itemSel)) - 0.5) < 0.01);
  A.bars.length = 0; if (box) A.attack(box.entityId); await sleep(600);
  ok('...a punch: "Sneak + punch to pick the case up." (nothing to switch)', /Sneak \+ punch to pick the case up/.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 100));
  A.slot(5); await sleep(250); if (box) A.interact(box.entityId); await sleep(500);

  // ---------------------------------------------------------------- a wall case, Apophiss's Oath in it - then the case picked up
  await run(`${O}setblock ${X + 3} ${Y + 2} ${Z + 4} minecraft:stone`);
  await at(X + 0.5, Y + 1, Z + 4.5, -90, 5);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/display_case_gilded'); await run('loot replace entity TestRat hotbar.1 loot bm:items/apo_oath');
  await use(A, 0);
  const wallSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X + 2.75},y=${Y + 2.1},z=${Z + 4.5},distance=..0.6,limit=1]`;
  ok('a wall case hung on the stone', (await cnt(wallSel)) === 1);
  const wbox = await entOf(A, wallSel);
  A.slot(1); await sleep(300); if (wbox) A.interact(wbox.entityId); await sleep(700);
  const wfig = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X + 2.75},y=${Y + 2.1},z=${Z + 4.5},distance=..0.8]`;
  ok('the Oath in it: a little Apophiss (12 parts) in the shallow case', (await cnt(wfig)) === 12, `parts ${await cnt(wfig)}`);
  let zmax = 0; for (let k = 0; k < 12; k++) zmax = Math.max(zmax, Math.abs(+(((await run(`${O}data get entity ${wfig.slice(0, -1)},limit=1,sort=random] transformation.translation[2]`)).match(/(-?[\d.]+)f/) || [0, 9])[1])));
  ok('...no deeper than the glass', zmax < 0.16, `deepest joint ${zmax.toFixed(3)}`);
  // (2.78: a wall case is too shallow for a statue to turn in - sneak + right-click leaves it still, and says so)
  A.bars.length = 0; A.input({ shift: true }); await sleep(300); if (wbox) A.interact(wbox.entityId, true); await sleep(600); A.input({}); await sleep(300);
  ok('sneak + right-click on the wall case: the statue stays still', (await cnt(`${wfig.slice(0, -1)},tag=bm.dcmspin]`)) === 0 && (await cnt(wfig)) === 12,
     `turning ${await cnt(`${wfig.slice(0, -1)},tag=bm.dcmspin]`)}`);
  ok('...and the player is told why', A.bars.some(b => /wall case/.test(b)), A.bars.slice(-2).join(' | '));
  A.input({ shift: true }); await sleep(300); if (wbox) A.interact(wbox.entityId, true); await sleep(600); A.input({}); await sleep(300);   // (spin back off)
  A.input({ shift: true }); await sleep(250); if (wbox) A.attack(wbox.entityId); await sleep(500); A.input({}); await sleep(400);
  ok('sneak + punch: the case comes down, the figurine with it', (await cnt(wallSel)) === 0 && (await cnt(wfig)) === 0 && (await has('TestRat', 'display_case_gilded')) === 1);
  ok('...and the Oath drops out, safe', await wait(2000, async () => (await cnt(`@e[type=minecraft:item,x=${X + 2.75},y=${Y + 2},z=${Z + 4.5},distance=..3,nbt={Item:{components:{"minecraft:custom_data":{bm:"apo_oath"}}}}]`)) === 1 ||
                                                  (await has('TestRat', 'apo_oath')) === 1));
  await sleep(3000);
  ok('no figurine part is left anywhere', (await figs()) === 0);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
