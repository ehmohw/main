// 2.80c: the diamond and netherite looks - as a regular (non-op) player, every step a real packet (rcon sets the stage: a floor,
// the items, the bank's coins, and the Tailor's counter clicked for the bot - his menu is what a right-click opens):
//   Tullius's Diamond Captain used while he's out: his rig wears it (tu_body_c5); his wardrobe (sneak + use the Doubloon) has the
//     Diamond and the Netherite rows; Netherite Captain is locked until it's his - pressed, it says where it's sold.
//   The Tailor: Tullius's page sells the Netherite Captain for 6,144 coins (the Diamond 4,096, the Gilded 2,560); bought - from the
//     bank - it's in his wardrobe for good; pressed there, his rig wears it (tu_body_c6).
//   Leo's Diamond Champion: his helm turns diamond too (le_head_c5). Wilfrey's Netherite Sun: the black sun shield in his free hand
//     and his armour turned to netherite (only its look).
//   Each look's item says what it is ("Diamond: cut and polished", "Netherite: forged in the deep Nether") and glints.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const X = 16620, Y = 100, Z = 16000;
  const TU = '@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_body,limit=1]';
  const model = async sel => await nbt(sel, 'item.components."minecraft:item_model"');
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  for (const t of ['bm.tupet', 'bm.wilfrey', 'bm.leopet', 'bm.pmpet', 'bm.emmapet', 'bm.cecilpet', 'bm.celipet', 'bm.kxpet', 'bm.dmpet']) await run(`${O}kill @e[tag=${t}]`);
  await sleep(1500);
  for (const o of ['bm.tucd', 'bm.wlcd', 'bm.lecd', 'bm.costu', 'bm.wutul', 'bm.coswl', 'bm.wuwil', 'bm.cosl', 'bm.wuleo']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const kit = ['tul_coin', 'cos_tul_5', 'leo_crest', 'cos_leo_5', 'wilfrey_locket', 'cos_wil_6'];
  for (let i = 0; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  // ---- the items say what they are
  const lore = async slot => await run(`data get entity TestRat Inventory[{Slot:${slot}b}].components`);
  const l1 = await lore(1), l5 = await lore(5);
  ok('the Diamond Captain says what it is: cut and polished, 4,096 coins, and it glints', /Diamond: cut and polished/.test(l1) && /4,096 coins/.test(l1) && /enchantment_glint_override": 1b/.test(l1), l1.slice(0, 160));
  ok('...the Netherite Sun: forged in the deep Nether, 6,144 coins', /Netherite: forged in the deep Nether/.test(l5) && /6,144 coins/.test(l5));

  // ---- Tullius: the Diamond Captain, used while he's out
  await use(0); await wait(5000, async () => (await cnt(TU)) === 1); await sleep(2500);
  await hold(1); await sleep(1200);
  ok('Tullius out, the Diamond Captain used: picked (bm.costu 5)', (await score('bm.costu')) === 5, `${await score('bm.costu')}`);
  ok('...his rig wears it (tu_body_c5)', /tu_body_c5/.test(await model(TU)), await model(TU));
  ok('sneak + use the Doubloon: his menu', await sneakMenu(0));
  const w1 = await A.press(/Wardrobe/);
  const labels = () => A.buttons().map(b => b.label).join(' | ');
  ok('...Wardrobe: the Diamond Captain wearing, the Netherite Captain locked', w1 && A.buttons().some(b => /Diamond Captain.*wearing/.test(b.label)) &&
     A.buttons().some(b => /Netherite Captain.*locked/.test(b.label)), labels());
  A.chats.length = 0; A.bars.length = 0; await A.press(/Netherite Captain/); await sleep(600);
  ok('...pressed while locked: where to find it', [...A.chats, ...A.bars].some(c => /Netherite Captain.*locked.*Tailor/.test(c)), [...A.chats, ...A.bars].slice(-1).join(''));
  // ---- the Tailor (his counter clicked for the bot: what a right-click opens)
  await run('scoreboard players set TestRat bm.gbc 10000');
  for (const i of ['gutter_coin', 'gutter_medallion', 'gutter_trophy']) await run(`clear TestRat *[minecraft:custom_data~{bm:"${i}"}]`);
  const n0 = A.dialogN.length; await run('execute as TestRat at @s run function bm:p103/tl/main'); await wait(3000, async () => A.dialogN.length > n0);
  ok('the Tailor opens', A.buttons().some(b => /Tullius/.test(b.label)), labels());
  await A.press(/^Tullius/);
  ok('...Tullius\'s page: Gilded 2560, Diamond 4096, Netherite 6144 coins', A.buttons().some(b => /Gilded Captain.*2560 coins/.test(b.label)) &&
     A.buttons().some(b => /Diamond Captain.*OWNED/.test(b.label)) && A.buttons().some(b => /Netherite Captain.*6144 coins/.test(b.label)), labels());
  A.chats.length = 0; await A.press(/Netherite Captain/); await sleep(800);
  ok('...bought from the bank: in his wardrobe for good, 6,144 coins gone', ((await score('bm.wutul')) & 64) === 64 && (await score('bm.gbc')) === 10000 - 6144,
     `${await score('bm.wutul')} / ${await score('bm.gbc')}`);
  ok('...and the page says OWNED', A.buttons().some(b => /Netherite Captain.*OWNED/.test(b.label)), labels());
  await sneakMenu(0); await A.press(/Wardrobe/);
  await A.press(/Netherite Captain/); await sleep(1200);
  ok('...worn from his wardrobe: his rig in netherite (tu_body_c6)', /tu_body_c6/.test(await model(TU)), await model(TU));
  await run(`${O}kill @e[tag=bm.tupet]`); await sleep(800);

  // ---- Leo: the Diamond Champion - his helm too
  await use(2); await wait(6000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.lep,tag=bm.lp_head]')) >= 1); await sleep(2000);
  await hold(3); await sleep(1500);
  const lh = await model('@e[type=minecraft:item_display,tag=bm.lep,tag=bm.lp_head,limit=1]');
  ok('Leo out, the Diamond Champion used: his helm turns diamond (le_head_c5)', /le_head_c5/.test(lh), lh);
  const lb = await nbt('@e[type=minecraft:item_display,tag=bm.lep,tag=bm.lp_body,limit=1]', 'item.components."minecraft:custom_model_data"');
  ok('...and his tabard and armour (custom_model_data c5)', /c5/.test(lb), lb);
  await run(`${O}kill @e[tag=bm.leopet]`); await sleep(800);

  // ---- Wilfrey: the Netherite Sun (chosen while he rests, worn when he comes)
  await hold(5); await sleep(400);
  await hold(4); await wait(5000, async () => (await cnt('@e[type=minecraft:wither_skeleton,tag=bm.wil_body]')) >= 1); await sleep(1500);
  const W = '@e[type=minecraft:wither_skeleton,tag=bm.wil_body,limit=1]';
  const sh = await nbt(W, 'equipment.offhand');
  ok('Wilfrey comes bearing the Netherite Sun shield (black, a grey sun, glinting)', /shield/.test(sh) && /black/.test(sh) && /circle/.test(sh) && /glint/.test(sh), sh.slice(0, 220));
  const ch = await nbt(W, 'equipment.chest');
  ok('...his armour turned to netherite (its look only)', /asset_id: "minecraft:netherite"/.test(ch), ch.slice(0, 220));

  await run(`${O}kill @e[tag=bm.wilfrey]`); await run('clear TestRat');
  for (const o of ['bm.costu', 'bm.wutul', 'bm.coswl', 'bm.wuwil', 'bm.cosl', 'bm.wuleo']) await run(`scoreboard players set TestRat ${o} 0`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
