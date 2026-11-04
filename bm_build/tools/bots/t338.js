// 3.0g: ROYAL PEARLS FOR TROPHIES, IN THE BANK, FROM MONSTERS - AND PEARLMAN'S CYCLE (phase199, phase31, phase60), as a regular
// (non-op) player. rcon sets the stage (t162's market, placed if a last run hasn't; a Trophy in the pack; Queen Pearl's honours;
// which of Pearlman's gems TestRat has bought; #pqforce for a sure roll) and checks.
//   PEARLS  the Fence sells 4 Royal Pearls for a Black Market Trophy (a real trade); the Banker's Card's Rat Bank has a Royal
//           Pearls page - "Deposit all" puts them in the account (bm.bk_rp), "Take 1" hands one back; with Queen Pearl honoured
//           to rank III (bm.hn_pearlq 1555) a zombie TestRat strikes down drops him a Royal Pearl (the roll forced), and without
//           the honours none does (forced still).
//   CYCLE   eight of the nine gems bought: Pearlman brings the ninth, visit after visit; two missing: each visit brings one of
//           them and two visits bring both; all nine: still three different gems. The missing gem bought from him (a real
//           trade, 3 Medallions): ticked off in his collection.
//   node t338.js [pearls|cycle]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const num = async (sel, p) => +(((await run(`${O}data get entity ${sel} ${p}`)).match(/(-?[\d.]+)[dfbsL]?$/) || [0, NaN])[1]);
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const offerOf = async (sel, iid) => { for (let i = 0; i < 90; i++) { const r = await run(`${O}data get entity ${sel} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`);
    if (new RegExp(`"${iid}"`).test(r)) return i; if (/Found no elements/.test(r) || /No elements/i.test(r)) break; } return -1; };
  const trade = async (sel, idx) => {
    const eid = await uuidEnt(sel); A.windows.length = 0; A.interact(eid); await sleep(1200);
    const w = A.windows[A.windows.length - 1];
    if (w && idx >= 0) {
      A.write('select_trade', { slot: idx }); await sleep(400);
      A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
      A.close(w.windowId); await sleep(500);
    }
    return !!w; };
  const dlg = () => JSON.stringify(A.dialogN[A.dialogN.length - 1] || {});
  const CX = 24000, CY = 30, CZ = 24000;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');

  if (on('pearls')) {
    // ================================================================== the Fence: 4 Royal Pearls for a Trophy
    await run(`${O}forceload add ${CX} ${CZ} ${CX + 76} ${CZ + 96}`);
    const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
    await sleep(2500);
    if (!(await cnt(MK))) { let pl = ''; for (let i = 0; i < 30; i++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
    await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
    const FENCE = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${CX + 38},y=${CY},z=${CZ + 46},distance=..80,limit=1]`;
    ok('the market has its Fence', await wait(30000, async () => (await cnt(FENCE)) === 1, 1000));
    await run(`${O}execute at ${FENCE} run tp TestRat ^ ^ ^1.5 facing entity ${FENCE} eyes`); await sleep(1500); A.stand();
    let idx = await offerOf(FENCE, 'royal_pearl');
    for (let i = 0; i < 12 && idx < 0; i++) { await sleep(1500); idx = await offerOf(FENCE, 'royal_pearl'); }     // (a Fence from before the build: the market's patch hands him the new stock)
    const price = idx >= 0 ? await num(FENCE, `Offers.Recipes[${idx}].buy.count`) : NaN, n = idx >= 0 ? await num(FENCE, `Offers.Recipes[${idx}].sell.count`) : NaN;
    ok('the Fence sells Royal Pearls: 4 for 1 Black Market Trophy', idx >= 0 && price === 1 && n === 4 &&
       /"trophy"/.test(await run(`${O}data get entity ${FENCE} Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)), `offer ${idx}: ${price} for ${n}`);
    await run('loot replace entity TestRat hotbar.1 loot bm:items/trophy'); A.slot(1); await sleep(300);
    const opened = await trade(FENCE, idx);
    ok('...bought in a real trade: 4 Royal Pearls, the Trophy paid', opened && (await has('royal_pearl')) === 4 && (await has('trophy')) === 0, `pearls ${await has('royal_pearl')} trophies ${await has('trophy')}`);

    // ================================================================== the Rat Bank keeps them
    await run('scoreboard players set TestRat bm.bk_rp 0');
    await run('loot replace entity TestRat hotbar.2 loot bm:items/bankers_card'); A.slot(2); await sleep(400);
    await A.useWait();
    await A.press(/^Currencies/);
    ok('the Banker\'s Card: the Rat Bank - Currencies: a Royal Pearls page', /Rat Bank/.test(dlg()) && A.buttons().some(b => /^Royal Pearls/.test(b.label)), A.buttons().map(b => b.label).join(', ').slice(0, 300));
    let b = await A.press(/^Royal Pearls/);
    ok('...its page: deposit and take out', !!b && b.next && A.buttons().some(x => /Deposit all Royal Pearls/.test(x.label)), A.buttons().map(x => x.label).join(', '));
    await A.press(/Deposit all Royal Pearls/); await sleep(600);
    ok('...Deposit all: the 4 pearls in the account, none on TestRat', (await sc('TestRat', 'bm.bk_rp')) === 4 && (await has('royal_pearl')) === 0,
       `account ${await sc('TestRat', 'bm.bk_rp')} pockets ${await has('royal_pearl')}`);
    await A.press(/^Take 1$/); await sleep(600);
    ok('...Take 1: one back in hand, 3 kept', (await sc('TestRat', 'bm.bk_rp')) === 3 && (await has('royal_pearl')) === 1);

    // ================================================================== Queen Pearl's favour (rank III): monsters drop Royal Pearls
    const X = 17600, Y = 100, Z = 16200;
    await run(`${O}forceload add ${X - 12} ${Z - 12} ${X + 12} ${Z + 12}`); await sleep(1500);
    await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
    await run('clear TestRat'); await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword'); A.slot(0);
    const kill = async () => {
      await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 2.0} {NoAI:1b,Health:1f,Tags:["bm.t338z","bm.seen"],PersistenceRequired:1b}`); await sleep(800);
      const eid = await uuidEnt(`@e[type=minecraft:zombie,tag=bm.t338z,limit=1]`);
      if (eid == null) return false;
      for (let i = 0; i < 4 && (await cnt('@e[type=minecraft:zombie,tag=bm.t338z]')); i++) { A.attack(eid); await sleep(700); }
      return (await cnt('@e[type=minecraft:zombie,tag=bm.t338z]')) === 0;
    };
    await run('scoreboard players set #pqforce bm.cfg 1');
    await run('scoreboard players set TestRat bm.hn_pearlq 1555');
    A.bars.length = 0;
    const k1 = await kill(); await sleep(800);
    ok('Queen Pearl honoured to rank III: a zombie struck down drops TestRat a Royal Pearl', k1 && (await has('royal_pearl')) === 1 && A.bars.some(x => /Queen Pearl's favour/.test(x)),
       `killed ${k1} pearls ${await has('royal_pearl')}`);
    await run('clear TestRat *[minecraft:custom_data~{bm:"royal_pearl"}]');
    await run('scoreboard players set TestRat bm.hn_pearlq 1444');
    const k2 = await kill(); await sleep(800);
    ok('...honoured only to rank II: no pearl (the roll still forced)', k2 && (await has('royal_pearl')) === 0, `killed ${k2} pearls ${await has('royal_pearl')}`);
    await run('scoreboard players set #pqforce bm.cfg 0'); await run('scoreboard players reset TestRat bm.hn_pearlq');
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  }

  if (on('cycle')) {
    // ================================================================== Pearlman's cycle
    const KEYS = ['fire', 'water', 'poison', 'earth', 'electric', 'rock', 'air', 'grass', 'ice'];
    const X = 17700, Y = 100, Z = 16300;
    await run(`${O}forceload add ${X - 12} ${Z - 12} ${X + 12} ${Z + 12}`); await sleep(1500);
    await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:grass_block`); await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
    const PM = `@e[type=minecraft:villager,tag=bm.pearl,x=${X},y=${Y},z=${Z},distance=..10,limit=1]`;
    const own = async (list) => { for (const k of KEYS) await run(`tag TestRat ${list.includes(k) ? 'add' : 'remove'} bm.pmg_${k}`); };
    const visit = async () => {
      await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
      await run(`${O}execute positioned ${X + 2.5} ${Y} ${Z + 2.5} run function bm:p60/pm/spawn`); await sleep(400);
      const out = [];
      for (let i = 0; i < 3; i++) { const m = (await run(`${O}data get entity ${PM} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`)).match(/gem_([a-z]+)/); if (m) out.push(m[1]); }
      return out;
    };
    await run('tag TestRat add bm.pmstat');          // (the statue's already his: buying the ninth only ticks it off)
    await own(KEYS.filter(k => k !== 'ice'));
    const seen = [];
    for (let i = 0; i < 4; i++) seen.push(await visit());
    ok('eight of the nine bought: Pearlman brings the Ice Gem on every visit (4 visits)', seen.every(v => v.length === 3 && v.includes('ice')), seen.map(v => v.join('/')).join('  '));
    await own(KEYS.filter(k => k !== 'ice' && k !== 'grass'));
    const v1 = await visit(), v2 = await visit();
    ok('two missing (Grass, Ice): each visit brings one of them, and two visits bring both', [v1, v2].every(v => v.includes('ice') || v.includes('grass')) &&
       [...v1, ...v2].includes('ice') && [...v1, ...v2].includes('grass'), `${v1.join('/')}  ${v2.join('/')}`);
    await own(KEYS);
    const v3 = await visit();
    ok('all nine already his: still three different gems', v3.length === 3 && new Set(v3).size === 3, v3.join('/'));
    // the missing one, bought for real
    await own(KEYS.filter(k => k !== 'ice'));
    const v4 = await visit();
    const idx = v4.indexOf('ice');
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/medallion'); await run('item modify entity TestRat hotbar.0 {type:"minecraft:set_count",count:3}'); A.slot(0);
    A.chats.length = 0;
    const opened = idx >= 0 && await trade(PM, idx); await sleep(800);
    ok('...the Ice Gem bought from him (3 Medallions, a real trade): ticked off in his collection', opened && (await has('gem_ice')) === 1 && /bm\.pmg_ice/.test(await run('tag TestRat list')),
       `offer ${idx} gem ${await has('gem_ice')}`);
    await run(`${O}kill @e[type=minecraft:villager,tag=bm.pearl]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.pearld]`);
  }

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
