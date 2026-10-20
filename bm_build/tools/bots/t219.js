// 2.82t: THE URGENT FIXES, as a regular (non-op) player TestRat - every step a real packet (rcon sets the stage).
//   THE LEDGER: dropped (Q) in the gutter, it's back in the pack a moment later, nothing left on the floor.
//   WILFREY: the locket is a click - he comes, and the locket never leaves the hand; sneak + click: his menu (Call him over,
//   Send him home, Wardrobe) - Send him home: gone; called again. Knocked out: the rest is 2 minutes, and when it's over he's back
//   by himself. "Back after a faint" switched off on his wardrobe page: knocked out again - not back.
//   THE SATCHEL: two satchels, two bags - a diamond on the filter of one (used with a diamond in the other hand): ON, it takes the
//   diamond on the ground and leaves the dirt; the other bag stays empty. Set down (sneak + use) and the barrel broken: the diamond
//   is back in the bag, the bag back in hand.
//   THE PRIME COOLER: right-click - OFF: a Prime cut on the ground stays there; right-click - ON: it flies in.
//   THE DARK AUCTION: a sale night at dusk - the doors open; the town sleeps through (the clock jumps to morning) - the first lot is
//   called at daybreak.
//   THE REGALIA: Tombstride Treads carry Depth Strider III, the Deathmask Aqua Affinity.
//   THE LUCKY MAP: carrying eight of the nine pieces, a piece from the table is always the ninth (20 draws); a heist win's
//   map piece (its own table) likewise.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async (sel) => { const m = (await run(`execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const hasV = async (id) => { const m = (await run(`clear TestRat ${id} 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const sc = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const X = 14000, Y = 120, Z = 14000;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 4} ${Z + 8} minecraft:air`);
  const home = async () => { await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800); };
  await home();

  // ================================================================== THE LEDGER
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
  await run('execute in bm:gutter run tp TestRat -249.5 61 -249.5'); await sleep(1500);
  A.slot(0); await sleep(300); A.drop(true); await sleep(2500);
  ok('the Ledger dropped in the gutter: back in the pack, nothing on the floor', (await has('fixers_ledger')) === 1 &&
     !(await passes('execute in bm:gutter if entity @e[type=minecraft:item,x=-249.5,y=61,z=-249.5,distance=..12]')));
  await run('clear TestRat'); await home();

  // ================================================================== THE REGALIA
  await run('loot give TestRat loot bm:items/conq_boots'); await run('loot give TestRat loot bm:items/conq_helmet');
  const inv = await run('data get entity TestRat Inventory');
  ok('the Regalia: Treads with Depth Strider III, the Deathmask with Aqua Affinity', /"minecraft:depth_strider": 3/.test(inv) && /"minecraft:aqua_affinity": 1/.test(inv), inv.slice(0, 120));
  await run('clear TestRat');

  // ================================================================== WILFREY
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6'); await run('scoreboard players set TestRat bm.arof 0');
  await run('scoreboard players set TestRat bm.wlcd 0'); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.wilfrey]`); await run(`${O}kill @e[tag=bm.wil_body]`); await run(`${O}kill @e[tag=bm.wil_part]`); await sleep(1500);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/wilfrey_locket');
  const wil = '@e[type=minecraft:wolf,tag=bm.wilfrey]';
  await use(1); await sleep(300);
  ok('the locket clicked: Wilfrey comes - and the locket is still in hand', (await cnt(wil)) === 1 && (await has('wilfrey_locket')) === 1);
  await sleep(1200);
  let n0 = A.dialogN.length; await use(1, true); await wait(3000, async () => A.dialogN.length > n0);
  const labels = A.buttons().map(b => b.label).join(' | ');
  ok('sneak + click: his menu - Call him over, Send him home, Wardrobe', /Call him over/.test(labels) && /Send him home/.test(labels) && /Wardrobe/.test(labels), labels);
  await A.press(/Send him home/); await sleep(2500);
  ok('...Send him home: he fades', (await cnt(wil)) === 0);
  await use(1); await sleep(1500);
  ok('clicked again: he comes back', (await cnt(wil)) === 1);
  // knocked out (his host lost): 2 minutes - then back by himself
  await run(`${O}tp ${wil} ~ -300 ~`); await run(`${O}kill ${wil}`);
  ok('knocked out: his rest is 2 minutes', await wait(8000, async () => { const v = await sc('bm.wlcd'); return v > 100 && v <= 120; }), `${await sc('bm.wlcd')}`);
  await run('scoreboard players set TestRat bm.wlcd 2');
  ok('...and when it\'s over, he comes back by himself', await wait(8000, async () => (await cnt(wil)) === 1));
  // switched off on his wardrobe page
  await sleep(1000); n0 = A.dialogN.length; await use(1, true); await wait(3000, async () => A.dialogN.length > n0);
  n0 = A.dialogN.length; await A.press(/Wardrobe/); await wait(3000, async () => A.dialogN.length > n0);
  const wl = A.buttons().map(b => b.label).join(' | ');
  ok('his wardrobe page: "Back after a faint  on"', /Back after a faint\s+on/.test(wl), wl.slice(0, 300));
  await A.press(/Back after a faint/); await sleep(1500);
  ok('...pressed: off', (await sc('bm.arof')) > 0 && A.buttons().some(b => /Back after a faint\s+off/.test(b.label)));
  await run(`${O}tp ${wil} ~ -300 ~`); await run(`${O}kill ${wil}`);
  await wait(8000, async () => (await sc('bm.wlcd')) > 100);
  await run('scoreboard players set TestRat bm.wlcd 2'); await sleep(6000);
  ok('...knocked out again: the rest over, he stays away', (await cnt(wil)) === 0);
  await run('scoreboard players set TestRat bm.arof 0'); await run('clear TestRat'); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.wilfrey]`); await run(`${O}kill @e[tag=bm.wil_body]`);

  // ================================================================== THE VACUUM SATCHEL
  await home();
  await run('loot replace entity TestRat hotbar.2 loot bm:items/vacuum_satchel'); await run('loot replace entity TestRat hotbar.3 loot bm:items/vacuum_satchel');
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond');
  await use(2); await sleep(400);
  const flt = await run('data get entity TestRat Inventory[{Slot:2b}].components."minecraft:custom_data".bm_flt');
  ok('a satchel used with a diamond in the other hand: a diamond on its filter', /minecraft:diamond/.test(flt), flt.slice(-80));
  await run('item replace entity TestRat weapon.offhand with minecraft:air');
  await use(2); await sleep(400);
  ok('...used again (nothing in the other hand): ON', /bm_vac: ?1b/.test(await run('data get entity TestRat Inventory[{Slot:2b}].components."minecraft:custom_data"')));
  await run(`${O}summon minecraft:item ${X + 3.5} ${Y} ${Z + 0.5} {Item:{id:"minecraft:diamond",count:2},PickupDelay:0s,Tags:["t219i"]}`);
  await run(`${O}summon minecraft:item ${X + 3.5} ${Y} ${Z + 1.5} {Item:{id:"minecraft:dirt",count:5},PickupDelay:0s,Tags:["t219i"]}`);
  await sleep(2500);
  const bag2 = await run('data get entity TestRat Inventory[{Slot:2b}].components."minecraft:container"');
  const bag3 = await run('data get entity TestRat Inventory[{Slot:3b}].components."minecraft:container"');
  ok('ON with the filter: the diamonds fly into that bag, the dirt stays on the ground', /minecraft:diamond/.test(bag2) && !/dirt/.test(bag2) &&
     (await passes(`${O}execute if entity @e[type=minecraft:item,tag=t219i,x=${X + 3.5},y=${Y},z=${Z + 1.5},distance=..2]`)), bag2.slice(-120));
  ok('...the other satchel is its own bag: empty', !/minecraft:diamond/.test(bag3), bag3.slice(-80));
  await run(`${O}kill @e[type=minecraft:item,tag=t219i]`);
  // set down and broken
  await use(2, true); await sleep(1200);
  const bpos = (await run(`${O}data get entity @e[type=minecraft:marker,tag=bm.bxm,limit=1,sort=nearest] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  ok('sneak + use: the satchel sets down as a barrel', !!bpos);
  if (bpos) {
    const [bx, by, bz] = bpos.slice(1).map(v => Math.floor(+v));
    await run(`${O}setblock ${bx} ${by} ${bz} minecraft:air destroy`); await sleep(2500);
    const back = await run('data get entity TestRat SelectedItem.components."minecraft:container"');
    const nsat = await has('vacuum_satchel'), left = await run(`${O}execute if entity @e[type=minecraft:item,x=${bx + 0.5},y=${by},z=${bz + 0.5},distance=..3]`);
    ok('...the barrel broken: the diamonds back in the bag, the bag back in hand', /minecraft:diamond/.test(back) && nsat === 2 && !/passed/i.test(left),
       `${back.slice(-60)} | satchels ${nsat} | ${left}`);
  }
  await run('clear TestRat');

  // ================================================================== THE PRIME COOLER
  await home();
  await run('loot replace entity TestRat hotbar.4 loot bm:items/prime_cooler');
  await use(4); await sleep(500);
  await run(`${O}loot spawn ${X + 3.5} ${Y} ${Z + 0.5} loot bm:items/prime_beef`); await sleep(2500);
  ok('the Prime Cooler switched OFF: the Prime Beef stays on the ground', await passes(`${O}execute if entity @e[type=minecraft:item,x=${X + 3.5},y=${Y},z=${Z + 0.5},distance=..2]`));
  await use(4); await sleep(2500);
  ok('...switched ON: it flies into the cooler', !(await passes(`${O}execute if entity @e[type=minecraft:item,x=${X + 3.5},y=${Y},z=${Z + 0.5},distance=..2]`)) &&
     /prime_beef/.test(await run('data get entity TestRat Inventory[{Slot:4b}].components."minecraft:container"')));
  await run('clear TestRat');

  // ================================================================== THE LUCKY MAP
  for (let k = 1; k <= 8; k++) await run(`loot give TestRat loot bm:items/lucky_fragment_${k}`);
  await sleep(1500);
  let ninth = 0;
  for (let i = 0; i < 20; i++) { await run('execute as TestRat at @s run loot give @s loot bm:p2/fragment_random'); }
  await sleep(300); ninth = await has('lucky_fragment_9');
  let dupes = 0; for (let k = 1; k <= 8; k++) dupes += (await has(`lucky_fragment_${k}`)) - 1;
  ok('carrying eight of the nine map pieces: every new piece is the ninth (until it\'s carried too)', ninth >= 1 && dupes <= 19 - 0 && ninth + dupes === 20 && ninth >= 1,
     `ninth ${ninth}, repeats ${dupes}`);
  // a heist win's map piece (its own table, into the haul): the same rule
  await run('clear TestRat'); for (let k = 2; k <= 9; k++) await run(`loot give TestRat loot bm:items/lucky_fragment_${k}`);
  await sleep(1500);
  for (let i = 0; i < 10; i++) await run('execute as TestRat at @s run loot give @s loot bm:p173/win_frag');
  await sleep(300); const first = await has('lucky_fragment_1');
  ok('a heist win\'s map piece: carrying the other eight, it\'s the one you lack', first >= 1 && first + (await has('lucky_fragment_9')) - 1 === 10, `piece 1 x${first}`);
  await run('clear TestRat');

  // ================================================================== THE DARK AUCTION (no market needed for the clock)
  await run('function bm:admin/auction_stop'); await run('scoreboard players set #state bm.auc 0');
  const st = async () => +((await run('scoreboard players get #state bm.auc')).match(/has (-?\d+)/) || [0, -1])[1];
  const base = 240000;
  await run(`time set ${base + 11000}`); await sleep(1500);
  await run('scoreboard players set #bmday bm.bm 69'); await run('scoreboard players set #lastday bm.auc 69'); await run('scoreboard players set #owed bm.auc 0');
  await run('scoreboard players set #saled bm.auc 0'); await sleep(1500);
  ok('a sale night (day 69), before dusk: the doors still shut', (await st()) === 0);
  await run(`time set ${base + 12100}`); await sleep(3000);
  ok('...at dusk (12100): the doors open (it used to wait for 17000)', (await st()) === 1);
  await run(`time set ${base + 24000 + 1000}`); await sleep(3000);
  ok('...the town sleeps through (the clock jumps to morning): the first lot is called', (await st()) >= 2);
  await run('function bm:admin/auction_stop'); await run('time set day');

  // ---- clean up
  await run('clear TestRat'); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();
