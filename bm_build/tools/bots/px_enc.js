// 2.94: meeting an 8-bit follower (phase213/214) - as the player: your own Emma / Leo / Cecil called with her/his own item, a Glitched
// Cartridge used beside them (the 8-bit self tumbles out, the cartridge spent), the 8-bit self right-clicked: its cartridge.
// (2.94l: the title, the PRESS START sign over them and their glow say they're a new follower to recruit; the sign goes when they join.)
module.exports = (orig, item, metTag, cart) => async ({ A, run, ok, wait, O, cnt, has, entOf, use, at, X, Y, Z, ENC, sleep }) => {
  await run(`tag TestRat remove ${metTag}`); await run(`execute as TestRat run function bm:p98/home/${orig}`); await sleep(800);
  await run(`scoreboard players set TestRat bm.${{ emma: 'emcd', leo: 'lecd', cecil: 'cpcd' }[orig]} 0`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run(`loot replace entity TestRat hotbar.7 loot bm:items/${item}`); await run('loot replace entity TestRat hotbar.6 loot bm:items/glitch_cart');
  await use(7); await sleep(2500);
  const host = { emma: 'cat,tag=bm.emmapet', leo: 'wolf,tag=bm.leopet', cecil: 'wolf,tag=bm.cecilpet' }[orig];
  ok(`your own ${orig} called (her/his own item)`, (await cnt(`@e[type=minecraft:${host}]`)) >= 1);
  await run(`${O}tp @e[type=minecraft:${host}] ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await sleep(500);
  A.chats.length = 0; A.titles.length = 0; await use(6); await sleep(1500);
  ok('the Glitched Cartridge used beside them: the 8-bit self tumbles out, the cartridge spent', (await cnt(ENC)) === 1 && (await has('glitch_cart')) === 0 &&
     A.chats.some(c => /tumbles/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  // (2.94l) plainly a new follower to recruit: a title on your screen, a PRESS START sign over them, their model glowing
  const ab = { emma: 'xm', leo: 'xl', cecil: 'xc' }[orig];
  ok('...a title says so ("APPEARED!", "right-click to recruit"), and a line in chat', A.titles.some(t => /APPEARED!/.test(t)) && A.titles.some(t => /recruit/.test(t)) &&
     A.chats.some(c => /new follower/.test(c)), A.titles.join(' | ').slice(0, 160));
  ok('...a "PRESS START - right-click to recruit" sign over them, their model glowing', (await cnt(`@e[type=minecraft:text_display,tag=bm.${ab}encsign]`)) === 1 &&
     /Glowing: 1b/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.${ab}encp,limit=1]`)));
  let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
  A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500);
  ok(`right-clicked: ${cart}`, (await has(cart)) === 1, A.chats.slice(-1).join('').slice(0, 160));
  ok('...and the sign goes with them', await wait(3000, async () => (await cnt(`@e[type=minecraft:text_display,tag=bm.${ab}encsign]`)) === 0));
  await run(`clear TestRat *[minecraft:custom_data~{bm:"${item}"}]`);
};
