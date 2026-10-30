// 2.94r: THE FOLLOWER GALLERY (phase220), as a regular (non-op) player - off the Partner Wheel's page (the buttons as sent):
//   the wheel's page has a Gallery button; pressed: the list - "Met: N of <the roster>", a met follower by name (#01 Emma), one not met
//     as "???" (its name nowhere on the page), with a hint on hover;
//   meeting one (holding their item) adds them: the count one up, their name now shown;
//   View in 3D, #01-#08: eight figures (their parts, and eight labels) in an arc in front of you; Emma's (met) lit, an unmet
//     one's dark (a silhouette) under "???"; they turn (a turntable); another page: the first page goes; a minute on: all gone;
//   "« Partner Wheel": the wheel's page again. (rcon sets the stage: which followers are met, an empty field.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); };
  const X = 17900, Y = 100, Z = 16080;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run('kill @e[tag=bm.galx]');
  // (the stage: met Emma and Cecil only - the rest not)
  // (3.0d: every met/ advancement in the built pack, so newer followers met by earlier tests don't count)
  const MET = require('fs').readdirSync(require('path').join(__dirname, '../../out_p2/BlackMarket_DP/data/bm/advancement/met')).filter(f => f.endsWith('.json')).map(f => f.slice(0, -5));
  for (const k of MET) await run(`advancement revoke TestRat only bm:met/${k}`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  await run('loot replace entity TestRat hotbar.1 loot bm:items/emma_ribbon'); await run('loot replace entity TestRat hotbar.2 loot bm:items/cecil_gem'); await sleep(1500);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.pw0 1');            // (Emma on the wheel: its page has partners)
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); await sleep(800);

  const flat = c => c == null ? '' : typeof c === 'string' ? c : Array.isArray(c) ? c.map(flat).join('') : (c.text || '') + flat(c.extra);   // (a component, as read)
  const page = () => { const d = (A.dialogN[A.dialogN.length - 1] || {}).data || {}; return flat(d.title) + ' | ' + [].concat(d.body || []).map(b => flat(b.contents)).join(' | '); };
  const hints = () => JSON.stringify(A.dialogN[A.dialogN.length - 1] || '');
  // ---- the wheel's page -> the Gallery
  let n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0);
  ok('the wheel\'s page has a Gallery button', A.buttons().some(b => /Gallery/.test(JSON.stringify(b))));
  await A.press(/Gallery/); await sleep(600);
  const g1 = page();
  ok('pressed: the Follower Gallery - "Met: 2 of N"', /Follower Gallery/.test(g1) && /Met: 2 of \d+/.test(g1), g1.slice(0, 300));
  ok('...#01 Emma and #04 Cecil by name (met)', /#01 Emma/.test(g1) && /#04 Cecil/.test(g1));
  ok('...#06 not met: "???" (not "#06 Leo"), his hint there to hover', /#06 \?\?\?/.test(g1) && !/#06 Leo/.test(g1) && /little stone fort/.test(hints()));
  // ---- meeting one: Leo's crest held
  await run('loot replace entity TestRat hotbar.3 loot bm:items/leo_crest'); await sleep(1200); await run('item replace entity TestRat hotbar.3 with minecraft:air');
  A.cmd('trigger bm.act set 2'); await sleep(400);
  n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0); await A.press(/Gallery/); await sleep(600);
  const g2 = page();
  ok('Leo\'s crest held (met): "Met: 3 of N", #06 Leo by name', /Met: 3 of \d+/.test(g2) && /#06 Leo/.test(g2), g2.slice(0, 200));

  // ---- View in 3D, #01-#08
  await A.press(/#01-#08/); await sleep(1500);
  const labels = await cnt(`@e[type=minecraft:text_display,tag=bm.galx,x=${X},y=${Y},z=${Z},distance=..12]`);
  const parts = await cnt(`@e[type=minecraft:item_display,tag=bm.galsp,x=${X},y=${Y},z=${Z},distance=..12]`);
  ok('View in 3D #01-#08: eight labels, and the figures\' parts, in front of you', labels === 8 && parts > 40, `labels ${labels}, parts ${parts}`);
  const front = await cnt(`@e[type=minecraft:text_display,tag=bm.galx,x=${X - 5},y=${Y - 1},z=${Z},dx=10,dy=5,dz=8]`);   // (facing south: z+)
  ok('...in an arc in front (facing south: all of them south of you, 3-5 blocks out)', front === 8 &&
     (await cnt(`@e[type=minecraft:text_display,tag=bm.galx,x=${X},y=${Y + 1},z=${Z},distance=..3]`)) === 0, `${front}`);
  const tx = await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.galx,limit=1,sort=nearest,x=${X - 2.4},y=${Y + 2},z=${Z + 4}] text`);
  const all = []; for (let i = 0; i < 8; i++) all.push(await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.galx,limit=1,sort=nearest,x=${X + 0.5 + 4.6 * Math.sin(-(i - 3.5) * 20 * Math.PI / 180)},y=${Y + 2},z=${Z + 0.5 + 4.6 * Math.cos((i - 3.5) * 20 * Math.PI / 180)}] text`));
  ok('...labelled: "#01 Emma" (met), "#02 ???" (Celi, not met), "#06 Leo" (met now)', all.some(t => /#01 /.test(t) && /Emma/.test(t)) && all.some(t => /#02 /.test(t) && /\?\?\?/.test(t)) &&
     all.some(t => /#06 /.test(t) && /Leo/.test(t)) && !all.some(t => /Celi/.test(t)), all.map(t => (t.match(/"#\d+ "|text: "[^"]*"/g) || []).join('')).join(' | ').slice(0, 300));
  const lit = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.galsp,limit=1,sort=nearest,x=${X + 0.5 + 4.6 * Math.sin(-(0 - 3.5) * 20 * Math.PI / 180)},y=${Y + 1},z=${Z + 0.5 + 4.6 * Math.cos((0 - 3.5) * 20 * Math.PI / 180)}] brightness`);
  const dark = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.galsp,limit=1,sort=nearest,x=${X + 0.5 + 4.6 * Math.sin(-(1 - 3.5) * 20 * Math.PI / 180)},y=${Y + 1},z=${Z + 0.5 + 4.6 * Math.cos((1 - 3.5) * 20 * Math.PI / 180)}] brightness`);
  ok('...Emma\'s figure lit, Celi\'s a dark silhouette', /block: 13/.test(lit) && /block: 0/.test(dark), `${lit} | ${dark}`);
  const r0 = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.galsp,limit=1,sort=nearest,x=${X},y=${Y + 1},z=${Z + 4}] Rotation[0]`);
  await sleep(2100);
  const r1 = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.galsp,limit=1,sort=nearest,x=${X},y=${Y + 1},z=${Z + 4}] Rotation[0]`);
  ok('...on a turntable (it turns)', r0 !== r1, `${r0} -> ${r1}`);
  // ---- another page: the first goes
  n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0); await A.press(/Gallery/); await sleep(600);
  await A.press(/#09-#16/); await sleep(1500);
  const p2 = []; for (let i = 0; i < 8; i++) p2.push(await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.galx,limit=1,sort=nearest,x=${X + 0.5 + 4.6 * Math.sin(-(i - 3.5) * 20 * Math.PI / 180)},y=${Y + 2},z=${Z + 0.5 + 4.6 * Math.cos((i - 3.5) * 20 * Math.PI / 180)}] text`));
  ok('another page, #09-#16: the first page gone, eight new labels', (await cnt('@e[type=minecraft:text_display,tag=bm.galx]')) === 8 && p2.some(t => /#09 /.test(t)) && !p2.some(t => /#01 /.test(t)));
  // ---- back to the wheel
  n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0); await A.press(/Gallery/); await sleep(600);
  await A.press(/Partner Wheel/); await sleep(600);
  ok('"« Partner Wheel": the wheel\'s page again', A.buttons().some(b => /Gallery/.test(JSON.stringify(b))) && /Call|Send/.test(page()));
  // ---- a minute on: gone
  await run('scoreboard players set @e[tag=bm.galx] bm.galt 2');
  ok('a minute on, the page is gone', await wait(4000, async () => (await cnt('@e[tag=bm.galx]')) === 0));

  // ---- clean up
  A.cmd('trigger bm.act set 2'); await run('kill @e[tag=bm.galx]'); await run('scoreboard players set TestRat bm.pw0 0'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
