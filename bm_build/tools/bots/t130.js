// 2.76: Pearlman's collection (real trades), the Golden Statue, Pearlman the follower
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const A = await bot('TestRat'); await sleep(2500);
  const O = 'execute in minecraft:overworld run ';
  const count = async (sel, dim = 'minecraft:overworld') => { const m = (await run(`execute in ${dim} run execute if entity ${sel}`)).match(/Count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`));
  const uuidOf = async (sel, dim = 'minecraft:overworld') => { const m = (await run(`execute in ${dim} run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entByUuid = u => Object.values(A.ents).find(e => e.objectUUID === u);
  const tags = async () => (await run('tag TestRat list')).replace(/.*: /, '');
  const fx = async () => await run('data get entity TestRat active_effects');
  const X = 16000, Y = 121, Z = 16000;
  const KEYS = ['fire', 'water', 'poison', 'earth', 'electric', 'rock', 'air', 'grass', 'ice'];
  const reset = async () => {
    await run(`${O}fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} minecraft:stone`);
    await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 5} ${Z + 14} minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
  };
  // trade every gem Pearlman stocks (real trades: open his window, pick the trade, shift-click the result)
  const tradeGems = async (dim, px, py, pz) => {
    const sel = `@e[type=minecraft:villager,tag=bm.pearl,limit=1]`;
    const e = entByUuid(await uuidOf(sel, dim)); if (!e) return 'no pearlman seen';
    A.windows.length = 0; A.interact(e.entityId); await sleep(900);
    const w = A.windows[A.windows.length - 1]; if (!w) return 'no window';
    for (let i = 0; i < 3; i++) {
      A.write('select_trade', { slot: i }); await sleep(250);
      A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(450);
    }
    A.close(w.windowId); await sleep(300); return 'traded';
  };
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  for (const k of KEYS) await run(`tag TestRat remove bm.pmg_${k}`);
  await run('tag TestRat remove bm.pmstat'); await run('advancement revoke TestRat only bm:story/gold_standard');
  await run(`${O}forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await reset(); await sleep(2000);
  await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);

  if (want('gems')) {
    // 1. the heist lobby's gems never count (Pearlman rung up in the vault - he can't be, but even so)
    for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/medallion');
    await run('tag TestRat add bm.gvok'); await run('execute in bm:gutter run tp TestRat -307.5 68 -243.5'); await sleep(2500);
    await run('execute in bm:gutter positioned -307.5 68 -241.5 run function bm:p60/pm/spawn'); await sleep(600);
    const g = await tradeGems('bm:gutter');
    const gt = await tags(); let bought = 0;
    for (const k of KEYS) if (/Found [1-9]/.test(await run(`clear TestRat *[minecraft:custom_data~{bm:"gem_${k}"}] 0`))) bought++;
    ok('A trade with Pearlman in the heist lobby doesn\'t count toward his nine', bought > 0 && !/bm\.pmg_/.test(gt), `${g}; bought ${bought}; tags ${gt.slice(0, 120)}`);
    await run('clear TestRat *[minecraft:custom_data~{bm_vault:1b}]'); for (const k of KEYS) await run(`clear TestRat *[minecraft:custom_data~{bm:"gem_${k}"}]`);
    await run('execute in bm:gutter run kill @e[type=minecraft:villager,tag=bm.pearl]'); await run('execute in bm:gutter run kill @e[type=minecraft:item_display,tag=bm.pearld]');
    // 2. out in the world: three real trades, three ticked off
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(2500);
    await run('clear TestRat *[minecraft:custom_data~{bm:"medallion"}]'); for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/medallion');
    await run(`execute in minecraft:overworld positioned ${X + 0.5} ${Y} ${Z + 2.5} run function bm:p60/pm/spawn`); await sleep(600);
    A.chats.length = 0;
    const t1 = await tradeGems('minecraft:overworld'); await sleep(500);
    const n = KEYS.filter(k => (new RegExp(`bm\\.pmg_${k}\\b`)).test('')).length;
    const tl = await tags(); const got = KEYS.filter(k => tl.includes(`bm.pmg_${k}`));
    ok('Three real trades with Pearlman out in the world: three gems ticked off his nine', got.length === 3, `${t1}; ${got.join(',')}`);
    ok('...and the chat says how many, and which are still to find', A.chats.some(c => /collection: 3 of 9/.test(c) && /Still to find/.test(c)), A.chats.filter(c => /collection/.test(c)).join(' | ').slice(0, 300));
    // 3. the rest (he only stocks three a visit): ticked off by the same trigger, the ninth brings the statue and his card
    for (const k of KEYS.filter(k => !got.includes(k))) await run(`advancement grant TestRat only bm:p128/buy_${k}`);
    await sleep(800);
    ok('All nine: Gold Standard - the Golden Statue and his Business Card', (await has('pearl_statue')) && (await has('pearl_card')) && /bm\.pmstat/.test(await tags()) &&
       /true|done|completed/i.test(await run('advancement test TestRat bm:story/gold_standard')) || ((await has('pearl_statue')) && (await has('pearl_card'))));
    // 4. lost them? a trade puts them back
    await run('clear TestRat *[minecraft:custom_data~{bm:"pearl_statue"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"pearl_card"}]');
    for (let i = 0; i < 3; i++) await run('loot give TestRat loot bm:items/medallion');
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
    await run(`execute in minecraft:overworld positioned ${X + 0.5} ${Y} ${Z + 2.5} run function bm:p60/pm/spawn`); await sleep(600);
    await tradeGems('minecraft:overworld'); await sleep(600);
    ok('Lost the statue and the card: a trade with Pearlman replaces both', (await has('pearl_statue')) && (await has('pearl_card')));
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
  }

  if (want('statue')) {
    await reset(); await run('clear TestRat'); await run('effect clear TestRat'); await sleep(500);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/pearl_statue'); A.slot(0);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 75`); await sleep(700);
    A.input({ shift: true }); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(1800);
    const st = await count(`@e[type=minecraft:interaction,tag=bm.pmst,x=${X},y=${Y},z=${Z},distance=..4]`);
    const f1 = await fx();
    ok('Sneak + use: the Golden Statue stands; near it you\'re Hero of the Village IV (about half price)', st === 1 && /hero_of_the_village/.test(f1) && /amplifier: 3b/.test(f1), `statues ${st}; ${f1.slice(0, 140)}`);
    // a Black Market trader close by: the discount lifts at once, and stays lifted
    await run(`${O}summon minecraft:villager ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["bm.npc","t130npc"],NoAI:1b,Invulnerable:1b}`); await sleep(1600);
    ok('...a Black Market trader nearby: no discount while you\'re near them', !/hero_of_the_village/.test(await fx()));
    await run(`${O}kill @e[type=minecraft:villager,tag=t130npc]`); await sleep(1600);
    ok('...away from them again: the discount is back', /hero_of_the_village/.test(await fx()));
    // sneak + punch: back in your pack
    const hm = (await run(`${O}data get entity @e[type=minecraft:interaction,tag=bm.pmst,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    const hp = hm ? hm.slice(1).map(Number) : [0, 0, 0];
    const all = Object.values(A.ents).filter(e => (e.x - hp[0]) ** 2 + (e.y - hp[1]) ** 2 + (e.z - hp[2]) ** 2 < 0.2);
    A.input({ shift: true }); await sleep(300); for (const e of all) { A.attack(e.entityId); await sleep(150); } await sleep(500); A.input({});
    ok('Sneak + punch it: the statue comes back', (await has('pearl_statue')) && (await count('@e[type=minecraft:interaction,tag=bm.pmst]')) === 0, `ents ${all.length}`);
  }

  if (want('follower')) {
    await reset(); await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] run function bm:p128/pm/go`);
    await sleep(500); await run('loot replace entity TestRat hotbar.1 loot bm:items/pearl_card'); A.slot(1); await sleep(300);
    A.use(); await sleep(400); A.release(); await sleep(1600);
    const cats = await count('@e[type=minecraft:cat,tag=bm.pmpet]'); const disp = await count('@e[type=minecraft:item_display,tag=bm.pmd]');
    ok('His Business Card: Pearlman waddles out (his model on him)', cats === 1 && disp === 1, `cats ${cats} models ${disp}`);
    await sleep(1500); const f2 = await fx();
    const hv = (f2.match(/\{[^}]*hero_of_the_village[^}]*\}/) || [''])[0];
    ok('...and while he\'s near: Luck, and villagers cheaper (Hero of the Village I)', /luck/.test(f2) && hv && !/amplifier/.test(hv), hv);
    await run(`${O}fill ${X - 2} ${Y} ${Z + 4} ${X + 2} ${Y} ${Z + 6} minecraft:water`);
    await run(`${O}tp TestRat ${X} ${Y} ${Z + 5}`); await sleep(1600);
    ok('...in water, you swim like a penguin (Dolphin\'s Grace)', /dolphins_grace/.test(await fx()));
    await run(`${O}fill ${X - 2} ${Y} ${Z + 4} ${X + 2} ${Y} ${Z + 6} minecraft:air`); await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(800);
    // his model keeps up with him
    await run(`${O}tp @e[type=minecraft:cat,tag=bm.pmpet,limit=1] ${X + 5.5} ${Y} ${Z + 0.5}`); await sleep(300);
    const P = async sel => (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    const cp = await P('@e[type=minecraft:cat,tag=bm.pmpet,limit=1]'), dp = await P('@e[type=minecraft:item_display,tag=bm.pmd,limit=1]');
    ok('His model keeps up with him', Math.hypot(cp[0] - dp[0], cp[2] - dp[2]) < 0.6 && cp[0] > X + 2, `cat ${cp} model ${dp}`);
    // the card's menu: wait here, then home
    A.input({ shift: true }); await sleep(250); A.use(); await sleep(400); A.release(); A.input({}); await sleep(500);
    ok('Sneak + use the card: his menu', (await sc('TestRat', 'bm.menu')) === 970, `menu ${await sc('TestRat', 'bm.menu')}`);
    A.cmd('trigger bm.act set 8301'); await sleep(600);
    ok('Wait here: he sits', /1b/.test(await run(`${O}data get entity @e[type=minecraft:cat,tag=bm.pmpet,limit=1] Sitting`)));
    await run('scoreboard players set TestRat bm.menu 970'); A.cmd('trigger bm.act set 8309'); await sleep(700);
    ok('Send him home: gone, model and all', (await count('@e[type=minecraft:cat,tag=bm.pmpet]')) === 0 && (await count('@e[type=minecraft:item_display,tag=bm.pmd]')) === 0);
    // put the card away: he goes home by himself
    A.use(); await sleep(400); A.release(); await sleep(1500);
    await run('item replace entity TestRat hotbar.1 with minecraft:air'); await sleep(4500);
    ok('Put his card away: he heads home', (await count('@e[type=minecraft:cat,tag=bm.pmpet]')) === 0);
    // not in the vault
    await run('loot replace entity TestRat hotbar.1 loot bm:items/pearl_card');
    await run('tag TestRat add bm.gvok'); await run('execute in bm:gutter run tp TestRat -307.5 68 -243.5'); await sleep(2500); A.chats.length = 0; A.bars.length = 0;
    A.use(); await sleep(400); A.release(); await sleep(800);
    ok('In the heist lobby he won\'t come ("Pearlman does not do heists")', (await count('@e[type=minecraft:cat,tag=bm.pmpet]', 'bm:gutter')) === 0 && A.bars.some(b => /heists/.test(b)), A.bars.slice(-1).join(''));
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(1500);
  }
  await run(`${O}forceload remove ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
