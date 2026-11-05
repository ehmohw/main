// 3.1: THE GUIDE (phase276, guide_art.py) as a regular (non-op) player - the Handbook's "Guide ›" page: Guide on (its parts appear by
// him, at its hover height, one guide only), each of the four forms in turn (Wisp 5 parts, Rainbow Butterfly 4, Suitcase 5 - on the
// ground, Little Handbook 5: their own guiw_/guib_/guis_/guik_ models, the old form gone); right-clicked (its click box): the happy
// twirl and the Handbook's own front page; a hit on it does nothing; he walks 10 blocks away and it follows; Guide off: gone. The Handbook
// on the Partner Wheel: off hand (F) + the wheel used - it goes on; the wheel's menu opens it and its Guide page; taken back once.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const X = 20840, Y = 180, Z = 16040;
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 32} ${Z + 16}`);
  await run(`fill ${X - 6} ${Y - 1} ${Z - 6} ${X + 20} ${Y - 1} ${Z + 6} minecraft:smooth_stone`);
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 20} ${Y + 4} ${Z + 6} minecraft:air`);
  await run('kill @e[tag=bm.gdx]'); await run('kill @e[type=minecraft:marker,tag=bm.gd]');
  await run('scoreboard players set TestRat bm.gdon 0').catch(() => {});
  const A = await bot('TestRat'); await sleep(2500);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1200); A.stand(); await sleep(300);
  { const _p = A.press.bind(A); A.press = async (re, ms) => { await sleep(600); return _p(re, ms); }; }
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('scoreboard players set TestRat bm.gdon 0'); await run('scoreboard players set TestRat bm.gdf 0');
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/bm_handbook'); A.slot(0); await sleep(300);
  const openB = async () => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length; A.use(); await sleep(350); A.release();
    await wait(2500, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const count = async (sel) => +(((await run(`execute as TestRat at @s if entity ${sel}`)).match(/count: (\d+)/) || [0, 0])[1]);
  const parts = (d = 4) => count(`@e[type=minecraft:item_display,tag=bm.gdp,distance=..${d}]`);
  const model = async (p) => ((await run(`data get entity @e[type=minecraft:item_display,tag=bm.gdp,tag=bm.gdk_${p},limit=1] item.components."minecraft:item_model"`)).match(/"bm:([a-z_]+)"/) || [0, ''])[1];
  const num = async (sel, path) => +(((await run(`data get entity ${sel} ${path}`)).match(/: (-?[\d.]+)/) || [0, NaN])[1]);
  const ppos = async () => [await num('TestRat', 'Pos[0]'), await num('TestRat', 'Pos[1]'), await num('TestRat', 'Pos[2]')];
  const anchor = '@e[type=minecraft:marker,tag=bm.gd,limit=1]';

  ok('the Handbook: its front page has "Guide"', await openB() && A.buttons().some(b => /Guide/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  const pg = await A.press(/Guide ›/);
  ok('...Guide › opens its page: Guide: off, the four forms', pg && pg.next && A.buttons().some(b => /^Guide: off/.test(b.label)) &&
     ['Wisp', 'Rainbow Butterfly', 'Suitcase', 'Little Handbook'].every(n => A.buttons().some(b => b.label.includes(n))), A.buttons().map(b => b.label).join(' | '));
  await A.press(/^Guide:/);
  ok('Guide: on - the page says so', A.buttons().some(b => /^Guide: on/.test(b.label)));
  ok('...the Wisp appears by him: its 5 parts, wisp models', await wait(3000, async () => (await parts()) === 5) && (await model('body')) === 'guiw_body', `${await parts()} parts, ${await model('body')}`);
  await sleep(800);
  const [, py] = await ppos(); const ay = await num(anchor, 'Pos[1]');
  ok('...floating at its hover height (about 1.3 over his feet)', Math.abs(ay - py - 1.3) < 0.35, `dy ${(ay - py).toFixed(2)}`);
  ok('...one guide only', (await count('@e[type=minecraft:marker,tag=bm.gd]')) === 1);
  for (const [name, pre, n, ground] of [['Rainbow Butterfly', 'guib_', 4, false], ['Suitcase', 'guis_', 5, true], ['Little Handbook', 'guik_', 5, false]]) {
    await A.press(new RegExp(name));
    const got = await wait(3000, async () => (await parts()) === n && (await model('body')) === pre + 'body');
    await sleep(600);
    const dy = (await num(anchor, 'Pos[1]')) - (await ppos())[1];
    ok(`form: ${name} - ${n} parts, ${pre} models, the old form gone, one guide`, got && (await count('@e[type=minecraft:item_display,tag=bm.gdp]')) === n &&
       (await count('@e[type=minecraft:marker,tag=bm.gd]')) === 1 && A.buttons().some(b => b.label.includes('●') && b.label.includes(name)), `${await parts()} parts, ${await model('body')}`);
    ok(`...${ground ? 'on the ground beside him' : 'floating'}`, ground ? Math.abs(dy) < 0.3 : dy > 0.9, `dy ${dy.toFixed(2)}`);
  }
  // right-click it: its click box (an interaction, the newest one in view near him)
  await sleep(500);
  const [px, , pz] = await ppos();
  const boxes = Object.values(A.ents).filter(e => e.type === 70 && Math.hypot(e.x - px, e.z - pz) < 3).sort((a, b) => b.entityId - a.entityId);
  ok('its click box is in view', boxes.length > 0, `${boxes.length}`);
  if (boxes.length) {
    const n0 = A.dialogN.length; A.interact(boxes[0].entityId);
    let face = '';
    const happy = await wait(900, async () => { const m = await model('cover'); if (/xhappy/.test(m)) face = m;
      return /has 2 /.test(await run(`scoreboard players get ${anchor} bm.gdst`)) && !!face; }, 40);
    const opened = await wait(2500, async () => A.dialogN.length > n0);
    ok('right-clicked: a happy twirl, and the Handbook opens (its front page)', happy && opened && A.buttons().some(b => /Followers/.test(b.label)) && A.buttons().some(b => /Guide/.test(b.label)));
    ok('...its face goes happy (guik_cover_xhappy)', face === 'guik_cover_xhappy', face);
    A.attack(boxes[0].entityId); await sleep(600);
    ok('a hit on it does nothing: still there, the hit cleared', (await count('@e[type=minecraft:marker,tag=bm.gd]')) === 1 &&
       !/attack/.test(await run('data get entity @e[type=minecraft:interaction,tag=bm.gdh,limit=1]')));
  }
  // he walks away: it follows
  let moving = false;
  const walk = A.walkTo(px + 10, pz, 0.2);
  for (let i = 0; i < 12; i++) { await sleep(150); if (/has 1 /.test(await run(`scoreboard players get ${anchor} bm.gdst`))) moving = true; }
  await walk; await sleep(1500);
  ok('he walks 10 blocks: it follows (its move cycle while it does) and catches up', moving && (await count('@e[type=minecraft:marker,tag=bm.gd,distance=..2.5]')) === 1 &&
     (await parts(3)) === 5, `moving ${moving}, near ${await count('@e[type=minecraft:marker,tag=bm.gd,distance=..2.5]')}`);
  // Guide off
  ok('the Handbook again, Guide ›', await openB() && !!(await A.press(/Guide ›/)));
  await A.press(/^Guide:/);
  ok('Guide: off - the page says so, and it is gone', A.buttons().some(b => /^Guide: off/.test(b.label)) &&
     await wait(2500, async () => (await count('@e[type=minecraft:item_display,tag=bm.gdp]')) === 0 && (await count('@e[type=minecraft:marker,tag=bm.gd]')) === 0));
  await sleep(1500);
  ok('...and stays gone', (await count('@e[tag=bm.gdx]')) === 0);
  // THE HANDBOOK ON THE PARTNER WHEEL: in the off hand (F), the wheel used - it goes on; the wheel opens it, its Guide ›; taken back once
  await run('scoreboard players set TestRat bm.pwhb 0'); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bm_handbook'); await run('loot replace entity TestRat hotbar.1 loot bm:items/partner_wheel');
  const hbN = async () => +(((await run('clear TestRat *[minecraft:custom_data~{bm:"bm_handbook"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
  A.slot(0); await sleep(300); A.swap(); await sleep(500);
  ok('the Handbook in his off hand (F)', /bm_handbook/.test(await run('data get entity TestRat equipment.offhand')));
  A.slot(1); await sleep(300); A.chats.length = 0; await run('scoreboard players set TestRat bm.gvhc 0'); A.use(); await sleep(350); A.release(); await sleep(800);
  ok('...the wheel used: it goes on the wheel (off his hands, the flag set, he is told)', (await hbN()) === 0 && /has 1 /.test(await run('scoreboard players get TestRat bm.pwhb')) &&
     A.chats.some(c => /Partner Wheel/.test(c)), A.chats.slice(-1).join(''));
  await sleep(1200);
  ok('...carrying the wheel counts as carrying it (bm.pw_hb)', /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.pw_hb]')));
  ok('the wheel: Black Market Handbook, Guide ›, Take the Handbook back', await openB() && ['Black Market Handbook', 'Guide', 'Take the Handbook back'].every(n => A.buttons().some(b => b.label.includes(n))),
     A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  const hbp = await A.press(/Black Market Handbook/);
  ok('...its Handbook button opens the Handbook (its front page)', hbp && hbp.next && A.buttons().some(b => /Followers/.test(b.label)));
  await openB(); const gdp = await A.press(/Guide ›/);
  ok('...its Guide › opens the guide page', gdp && gdp.next && A.buttons().some(b => /^Guide: /.test(b.label)));
  await openB(); await A.press(/Take the Handbook back/); await sleep(800);
  ok('...Take the Handbook back: the Handbook is his again, the flag off', (await hbN()) === 1 && /has 0 /.test(await run('scoreboard players get TestRat bm.pwhb')), `${await hbN()} handbooks`);
  A.cmd('trigger bm.act set 7009'); await sleep(800);
  ok('...and only once (the button pressed again: still one)', (await hbN()) === 1);
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
