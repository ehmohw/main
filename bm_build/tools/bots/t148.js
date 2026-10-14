// 2.78: every follower dressed, auras, and the tidied Office - as a regular (non-op) player, every step a real packet:
// Tullius's coat (Corsair Crimson) used while he's away ("he'll wear it next time"), then his Doubloon calls him - his rig
// wears it; sneak + use the Doubloon: his menu -> Wardrobe -> the aura row says locked, "His old coat" puts it back; his aura
// item used: his for good, on; the wardrobe switches it off. Pearlman's bow tie (Ruby) on his model; Wilfrey's Gilded Sun shield
// in his free hand. The Fixer's Ledger: the Office, Plan a Heist first, every button the same width; Raid Crew -> Outfits ->
// Pearlman's wardrobe. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const tags = async () => (await run('tag TestRat list'));
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const X = 16540, Y = 100, Z = 16000;
  const TU = '@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_body,limit=1]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  for (const t of ['bm.tupet', 'bm.pmpet', 'bm.wilfrey', 'bm.cecilpet', 'bm.emmapet', 'bm.celipet', 'bm.leopet']) await run(`${O}kill @e[tag=${t}]`);
  await sleep(1500);
  for (const o of ['bm.tucd', 'bm.wlcd', 'bm.costu', 'bm.wutul', 'bm.cospm', 'bm.wupearl', 'bm.coswl', 'bm.wuwil']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('tag TestRat remove bm.auown_tul'); await run('tag TestRat remove bm.au_tul');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const kit = ['tul_coin', 'cos_tul_2', 'cos_aura_tul', 'pearl_card', 'cos_pearl_1', 'wilfrey_locket', 'cos_wil_4', 'fixers_ledger'];
  for (let i = 0; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);

  // ---- Tullius's coat, used while he's away
  A.bars.length = 0; await hold(1); await sleep(500);
  ok('Corsair Crimson used while Tullius is away: it\'s picked (bm.costu 2)', (await score('bm.costu')) === 2, `${await score('bm.costu')}`);
  ok('..."he\'ll wear it next time"', A.bars.some(b => /Tullius isn't with you/.test(b)), A.bars.slice(-1).join(''));
  await use(0); await wait(5000, async () => (await cnt(TU)) === 1); await sleep(2500);
  ok('his Doubloon calls him: his rig wears the coat (tu_body_c2)', /tu_body_c2/.test(await nbt(TU, 'item.components."minecraft:item_model"')), await nbt(TU, 'item.components."minecraft:item_model"'));
  await sleep(4000);                                        // (poses: the arm's own model comes back each time - and the coat with it)
  const arm = await nbt('@e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_armr,limit=1]', 'item.components."minecraft:item_model"');
  ok('...his arm too, pose after pose', /_c2"?$/.test(arm), arm);
  // ---- his wardrobe, from his own menu
  ok('sneak + use the Doubloon: his menu', await sneakMenu(0));
  const w1 = await A.press(/Wardrobe/);
  ok('...Wardrobe: his wardrobe opens', w1 && w1.next && A.buttons().some(b => /Corsair Crimson/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  ok('...the aura row: Drowned Gale - locked', A.buttons().some(b => /Drowned Gale.*locked/.test(b.label)));
  A.chats.length = 0; await A.press(/Drowned Gale/); await sleep(600);
  ok('...pressed while locked: where to find it', A.chats.some(c => /Drowned Gale.*locked.*Tailor/.test(c)), A.chats.slice(-1).join(''));
  await A.press(/His old coat/); await sleep(800);
  ok('"His old coat": back to his own (tu_body)', /"bm:tu_body"/.test(await nbt(TU, 'item.components."minecraft:item_model"')), await nbt(TU, 'item.components."minecraft:item_model"'));
  // ---- his aura
  A.chats.length = 0; await hold(2); await sleep(500);
  ok('the aura used: his for good, and on', /bm\.auown_tul/.test(await tags()) && /bm\.au_tul\b/.test(await tags()), await tags());
  ok('...and everyone hears of it', A.chats.some(c => /awakened Drowned Gale/.test(c)), A.chats.slice(-1).join(''));
  ok('...its item used up', !/cos_aura_tul/.test(await run('data get entity TestRat Inventory')));
  await sneakMenu(0); await A.press(/Wardrobe/);
  ok('...the wardrobe says on', A.buttons().some(b => /Drowned Gale.*on/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Drowned Gale/); await sleep(600);
  ok('...switched off there', !/bm\.au_tul\b/.test(await tags()) && /bm\.auown_tul/.test(await tags()), await tags());
  ok('...the wardrobe says off', A.buttons().some(b => /Drowned Gale.*off/.test(b.label)), A.buttons().map(b => b.label).join(' | '));

  // ---- Pearlman's bow tie
  await use(3); await wait(5000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.pmd]')) >= 1); await sleep(1500);
  await hold(4); await sleep(600);
  const pm = await nbt('@e[type=minecraft:item_display,tag=bm.pmd,limit=1]', 'item.components."minecraft:item_model"');
  ok('Pearlman out, the Ruby bow tie used: his model wears it (pearlman_c1)', /pearlman_c1/.test(pm), pm);
  // ---- Wilfrey's shield (chosen while he rests, worn when he comes)
  await hold(6); await sleep(400);
  await hold(5); await wait(4000, async () => (await cnt('@e[type=minecraft:wither_skeleton,tag=bm.wil_body]')) >= 1); await sleep(1500);
  const sh = await nbt('@e[type=minecraft:wither_skeleton,tag=bm.wil_body,limit=1]', 'equipment.offhand');
  ok('Wilfrey comes bearing the Gilded Sun shield', /shield/.test(sh) && /yellow/.test(sh) && /circle/.test(sh), sh.slice(0, 200));

  // ---- the Office
  A.slot(7); await sleep(300);
  ok('the Ledger: the Office opens', await A.useWait(2500));
  const labels = A.buttons().map(b => b.label);
  ok('...Plan a Heist first, then the crew and the Armory', /Plan a Heist/.test(labels[0]) && /Raid Crew/.test(labels[1]) && /Armory/.test(labels[2]), labels.join(' | '));
  ok('...plain names (no "The Armory")', !labels.some(l => /\bThe (Armory|Gutter Bank|Codex|Crate Desk|Locker Hall)/.test(l)), labels.join(' | '));
  const dj = A.dialogs[A.dialogs.length - 1];
  const widths = [...dj.matchAll(/"width":\s*\{?[^0-9]*(\d+)/g)].map(m => +m[1]);
  ok('...every button the same width', labels.length >= 10 && (dj.match(/172/g) || []).length >= labels.length, `${labels.length} buttons; ${widths.join(',')}`);
  await A.press(/Raid Crew/); await A.press(/Outfits/);
  const pw = await A.press(/Pearlman's wardrobe/);
  ok('Raid Crew -> Outfits -> Pearlman\'s wardrobe', pw && pw.next && A.buttons().some(b => /Ruby/.test(b.label)), A.buttons().map(b => b.label).join(' | '));

  for (const t of ['bm.tupet', 'bm.pmpet', 'bm.wilfrey']) await run(`${O}kill @e[tag=${t}]`);
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pmd]`); await run(`${O}kill @e[type=minecraft:wither_skeleton,tag=bm.wil_body]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
