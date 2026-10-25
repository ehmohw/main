// 2.94m: EMMA'S EASTER EGGS (phase217), as a regular (non-op) player - Emma and Cecil called with their own items: she hugs him
// (rcon makes the rare roll certain: #hug1): her hug state and pose, both held still, his eyes closed, her line and his; it ends
// and both walk free again, and won't come again for half an hour. KillerWatt called with his Spark while she's out: the jolt,
// her KillerWatt look (her parts swap to emkw_*), in her wardrobe for good - turned off and on again from it (sneak + use her
// ribbon -> Wardrobe -> "KillerWatt look"). Hit six times fast (rcon deals the blows, 0.65 s apart): an angry face, the "Frik you!" bubble
// riding over her head, her line - and the bubble gone a few seconds later. Low on health: she panics (the face and a line).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (who, o) => +(((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const use = async (slot, sneak = false) => {
    await wait(3000, async () => !/has [1-9]/.test(await run('scoreboard players get TestRat bm.gvhc')), 200);
    A.slot(slot); await sleep(300); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.use(); await sleep(400); A.release(); if (sneak) { await sleep(200); A.input({}); } await sleep(1500); };
  const X = 17860, Y = 100, Z = 16040;
  const EM = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', CE = '@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]';
  const model = async (part) => ((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.emp,tag=bm.ep_${part},limit=1] item.components."minecraft:item_model"`)).match(/"([^"]+)"$/) || [0, ''])[1];
  const face = async () => ((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.emp,tag=bm.ep_head,limit=1] item.components."minecraft:custom_model_data".strings[0]`)).match(/"([^"]+)"$/) || [0, ''])[1];
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage: a pad, nobody else about, a clear sky, the look not yet had
  await run('gamemode survival TestRat'); await run('weather clear'); await run('time set 6000');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  for (const t of ['cat,tag=bm.emmapet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.kxpet']) await run(`kill @e[type=minecraft:${t}]`);
  await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(3000);
  for (const o of ['bm.emcd', 'bm.cpcd', 'bm.kxcd']) await run(`scoreboard players set TestRat ${o} 0`);
  for (let i = 0; i < 40; i++) await run(`tag TestRat remove bm.arw${i}`);              // (none of them walking back by himself after a faint)
  await run('tag TestRat remove bm.emkw_u'); await run('tag TestRat remove bm.emkw_o'); await run('tag TestRat remove bm.hush');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(800);
  for (const [i, iid] of ['emma_ribbon', 'cecil_gem', 'kw_spark'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);

  // ================================================================== 1. the hug
  await use(0); await use(1);
  ok('Emma and Cecil called with their own items', await wait(5000, async () => (await cnt(EM)) === 1 && (await cnt(CE)) === 1));
  await run(`${O}tp ${CE} ${X + 2.5} ${Y + 1} ${Z + 2.5}`); await run(`${O}tp ${EM} ${X + 1.5} ${Y + 1} ${Z + 2.0}`);
  await run(`${O}scoreboard players set ${EM} bm.emhc 0`); A.chats.length = 0;
  await run('scoreboard players set #hug1 bm.cfg 1');                                        // (the stage: the rare roll made certain)
  const hugged = await wait(15000, async () => (await sc(EM, 'bm.emhg')) > 0, 200);
  await run('scoreboard players set #hug1 bm.cfg 0');
  ok('idle together: Emma hugs Cecil - her hug state (20)', hugged && (await sc(EM, 'bm.ems')) === 20, `hg ${await sc(EM, 'bm.emhg')} ems ${await sc(EM, 'bm.ems')}`);
  ok('...both held still in it (NoAI), she close in front of him', /1b/.test(await run(`${O}data get entity ${EM} NoAI`)) && /1b/.test(await run(`${O}data get entity ${CE} NoAI`)) &&
     await (async () => {
       const p = async s => ((await run(`${O}data get entity ${s} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/) || []).slice(1).map(Number);
       const a = await p(EM), b = await p(CE); return Math.hypot(a[0] - b[0], a[2] - b[2]) < 0.9; })());
  ok('...her face beams (happy), his eyes closed (blink)', (await face()) === 'happy' &&
     /"blink"/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_eyes,limit=1] item.components."minecraft:custom_model_data"`)), await face());
  ok('...her line and his, in chat', A.chats.some(c => /C'mere, you/.test(c)) && A.chats.some(c => /Just this once/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('...it ends: both free again (no NoAI), back to idle', await wait(8000, async () => (await sc(EM, 'bm.emhg')) === 0 && !/1b/.test(await run(`${O}data get entity ${EM} NoAI`)) &&
     !/1b/.test(await run(`${O}data get entity ${CE} NoAI`)) && (await sc(EM, 'bm.ems')) !== 20));
  ok('...and not again for half an hour', (await sc(EM, 'bm.emhc')) > 1700, `rest ${await sc(EM, 'bm.emhc')}`);

  // ================================================================== 2. her KillerWatt look
  ok('Emma in her own clothes before', (await model('head')) !== 'bm:emkw_head', await model('head'));
  A.chats.length = 0; await use(2);
  ok('KillerWatt called with his Spark while she\'s out: a jolt - "glassy green, eyes aglow"', await wait(5000, async () => A.chats.some(c => /glassy green/.test(c))), A.chats.slice(-3).join(' | ').slice(0, 200));
  ok('...her KillerWatt look on: every part swapped (head, body, arms, legs)', await wait(3000, async () => {
       for (const p of ['head', 'body', 'armr', 'arml', 'legr', 'legl']) if ((await model(p)) !== `bm:emkw_${p}`) return false; return true; }),
     `${await model('head')} ${await model('body')} ${await model('legl')}`);
  ok('...in her wardrobe for good (unlocked, worn)', (await cnt('@a[name=TestRat,tag=bm.emkw_u,tag=bm.emkw_o]')) === 1);
  // (her wardrobe: sneak + use the ribbon while she's out - her menu - Wardrobe)
  await use(0, true); await A.press(/Wardrobe/); await sleep(800);
  const btn = A.buttons().find(b => /KillerWatt look/.test(b.label));
  ok('her wardrobe has the row: "KillerWatt look  on"', btn && /on/.test(btn.label), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  await A.press(/KillerWatt look/); await sleep(900);
  ok('...pressed: off - her own clothes back', (await model('head')) !== 'bm:emkw_head' && (await cnt('@a[name=TestRat,tag=bm.emkw_o]')) === 0, await model('head'));
  await A.press(/KillerWatt look/); await sleep(900);
  ok('...pressed again: on', (await model('head')) === 'bm:emkw_head' && (await model('body')) === 'bm:emkw_body', await model('head'));
  A.cmd('trigger bm.act set 2'); await sleep(400);
  ok('...her faces in his look: the head\'s item swaps its expressions too (custom_model_data on emkw_head)', await wait(8000, async () => /blink|happy|wink/.test(await face()), 200), await face());

  // ================================================================== 3. "Frik you!"
  await run(`${O}scoreboard players set ${EM} bm.emfk 0`); await run(`${O}scoreboard players set ${EM} bm.emhn 0`); A.chats.length = 0;
  let bub = false, rode = false, angry = false;
  for (let i = 0; i < 6 && !bub; i++) {                                                         // (the stage: blows, 0.65 s apart)
    await run(`${O}damage ${EM} 3 minecraft:generic`); await sleep(650);
    if ((await cnt('@e[type=minecraft:text_display,tag=bm.emfrik]')) === 1) {
      bub = /Frik you/.test(await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.emfrik,limit=1] text`));
      rode = /text_display/.test(await run(`${O}data get entity ${EM} Passengers`)); angry = (await face()) === 'angry'; }
  }
  ok('hit again and again, fast: "Frik you!" in a bubble over her head', bub);
  ok('...riding her (a passenger of her host)', rode);
  ok('...her angry face', angry, await face());
  ok('...and her line in chat', A.chats.some(c => /Emma: "Frik you!"/.test(c)), A.chats.slice(-1).join(''));
  ok('...the bubble gone a few seconds later', await wait(6000, async () => (await cnt('@e[type=minecraft:text_display,tag=bm.emfrik]')) === 0));
  A.chats.length = 0;
  for (let i = 0; i < 6; i++) { await run(`${O}damage ${EM} 2 minecraft:generic`); await sleep(650); }
  ok('...and not again straight away (30 seconds)', (await cnt('@e[type=minecraft:text_display,tag=bm.emfrik]')) === 0 && !A.chats.some(c => /Frik/.test(c)));

  // ================================================================== 4. panic at low health
  await run(`${O}scoreboard players set ${EM} bm.empn 0`); await run(`${O}data modify entity ${EM} Health set value 12f`); A.chats.length = 0;
  ok('down to a fifth of her health: she panics - the face and a line', await wait(16000, async () => (await face()) === 'panic' && A.chats.some(c => /\(panicking\)/.test(c)), 250),
     `${await face()} | ${A.chats.slice(-1).join('')}`);
  await run(`${O}data modify entity ${EM} Health set value 60f`);

  // ---------------------------------------------------------------- clean up
  for (const t of ['cat,tag=bm.emmapet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.kxpet']) await run(`kill @e[type=minecraft:${t}]`);
  await run('kill @e[type=minecraft:text_display,tag=bm.emfrik]');
  await sleep(1500); for (let i = 0; i < 40; i++) await run(`tag TestRat remove bm.arw${i}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('tag TestRat remove bm.emkw_u'); await run('tag TestRat remove bm.emkw_o');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
