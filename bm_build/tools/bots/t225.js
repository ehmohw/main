// 2.84b: hard mode's Dark Auction lots, hard replays' relics and the community pots - as a regular (non-op) player.
//   the community pots: the Banker's Card -> Community Pots -> the Harvest Guild (rcon fills it to 280 of 300 for the stage);
//     Give 50 takes only the 20 it needs, the pot is full: Luck I for everyone; switching it off takes the Luck away.
//   infusions: Lifesteal on the sword in the off hand (held right-click); a second infusion is refused and returned; with
//     the sword in hand, a kill heals two hearts. Vitality on a chestplate: worn, Regeneration.
//   an artifact (the Drowned Bell): sneak + use on the floor sets it down, punching it picks it back up; the Scrap Bin
//     knows its price.
//   a relic (the Rimeheart): slowness never takes hold.
//   the auction in hard mode: the first lot called is one of its artifacts (rcon stages the sale).
//   a hard replay's buff (a function-level spot check on a zombie): 175% health.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)(?!.*\d)/); return m ? +m[1] : NaN; };
  const effects = async () => run('data get entity TestRat active_effects');
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const press = async (re) => { const b = await A.press(re); await sleep(700); return b; };
  const hold = async (ms) => { A.use(); await sleep(ms); A.release(); await sleep(600); };
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const saved = {}; for (const v of ['pot1', 'potu1', 'poton1']) saved[v] = await sc(`#${v}`, 'bm.cfg');
  saved.hard = await sc('#hard', 'bm.cfg');

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 6} ${Y - 1} ${Z - 6} ${X + 6} ${Y - 1} ${Z + 6} minecraft:stone`);
  await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y + 4} ${Z + 6} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await sleep(1200); A.stand();

  // ================================================================== 1. the community pots
  await run('scoreboard players set #pot1 bm.cfg 280'); await run('scoreboard players set #potu1 bm.cfg 0'); await run('scoreboard players set #poton1 bm.cfg 0');
  await run('scoreboard players set TestRat bm.bk_tok 0');
  for (let i = 0; i < 30; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/bankers_card'); await sleep(400);
  A.slot(7); await sleep(300); await A.useWait(2500);
  ok('The Banker\'s Card: the account page has a Community Pots button', A.buttons().some(b => /Community Pots/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(-200));
  await press(/Community Pots/);
  ok('...the pots page lists the Harvest Guild at 280/300', A.buttons().some(b => /Harvest Guild\s+280\/300/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  await press(/Harvest Guild/);
  await press(/Give 50/);
  ok('Give 50 takes only the 20 it needs: the pot is full and unlocked', (await sc('#pot1', 'bm.cfg')) === 300 && (await sc('#potu1', 'bm.cfg')) === 1 && (await has('token')) === 10,
     `pot ${await sc('#pot1', 'bm.cfg')}, unlocked ${await sc('#potu1', 'bm.cfg')}, ${await has('token')} tokens left`);
  ok('...the world hears of it', A.chats.some(c => /Harvest Guild is full/.test(c)));
  ok('...Luck I for everyone', await wait(3000, async () => /minecraft:luck/.test(await effects())));
  await press(/Switch it on \/ off/);
  ok('Switched off: the Luck goes', (await sc('#poton1', 'bm.cfg')) === 0 && await wait(5000, async () => !/minecraft:luck/.test(await effects())), `${await sc('#poton1', 'bm.cfg')}`);
  A.cmd('trigger bm.act set 2'); await sleep(400);

  // ================================================================== 2. infusions
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/inf_lifesteal');
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_sword'); A.slot(0); await sleep(400);
  await hold(1600);
  const off = await run('data get entity TestRat equipment.offhand');
  ok('Infusion of Lifesteal on the sword in the off hand: marked and described', /bm_inf: "lifesteal"/.test(off) && /Infused: Lifesteal/.test(off) && (await has('inf_lifesteal')) === 0, off.slice(0, 200));
  await run('loot replace entity TestRat hotbar.0 loot bm:items/inf_frenzy'); await sleep(300);
  await hold(1600);
  ok('...a second infusion on it is refused and handed back', (await has('inf_frenzy')) === 1 && /bm_inf: "lifesteal"/.test(await run('data get entity TestRat equipment.offhand')));
  await run('clear TestRat *[minecraft:custom_data~{bm:"inf_frenzy"}]'); await sleep(200);
  A.swap(); await sleep(500);                                       // (F: the sword to the main hand)
  ok('...swapped into the main hand', /bm_inf: "lifesteal"/.test(await run('data get entity TestRat SelectedItem')));
  await run('damage TestRat 10 minecraft:generic'); await sleep(600);
  const h0 = await num('data get entity TestRat Health');
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 2.5} {NoAI:1b,Silent:1b,Health:1f,PersistenceRequired:1b,Tags:["bm.seen","bm.t225"]}`); await sleep(800);
  const zid = await uuidEnt('@e[type=minecraft:zombie,tag=bm.t225,limit=1]');
  A.attack(zid); await sleep(900);
  const h1 = await num('data get entity TestRat Health');
  ok('...a kill with it heals two hearts', !(await run(`${O}execute if entity @e[type=minecraft:zombie,tag=bm.t225]`)).match(/passed/) && h1 - h0 >= 3, `${h0} -> ${h1}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/inf_vitality');
  await run('item replace entity TestRat weapon.offhand with minecraft:iron_chestplate'); A.slot(0); await sleep(400);
  await hold(1600);
  await run('item replace entity TestRat armor.chest from entity TestRat weapon.offhand'); await run('item replace entity TestRat weapon.offhand with minecraft:air');
  ok('Vitality on a chestplate, worn: Regeneration', await wait(3000, async () => /minecraft:regeneration/.test(await effects())), (await effects()).slice(0, 160));
  await run('clear TestRat'); await run('effect clear TestRat');

  // ================================================================== 3. an artifact
  await run('loot replace entity TestRat hotbar.1 loot bm:items/art_bell'); A.slot(1);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await sleep(1200); A.stand();
  A.input({ shift: true }); await sleep(400); A.use(); await sleep(300); A.release(); await sleep(700); A.input({}); await sleep(300);
  const placed = async () => /passed/.test(await run(`${O}execute if entity @e[type=minecraft:item_display,tag=bm.art2d,x=${X},y=${Y},z=${Z},distance=..5]`));
  ok('The Drowned Bell, sneak + use on the floor: set down on display', await placed() && (await has('art_bell')) === 0);
  const bid = await uuidEnt(`@e[type=minecraft:interaction,tag=bm.art2,x=${X},y=${Y},z=${Z},distance=..5,limit=1]`);
  A.attack(bid); await sleep(900);
  ok('...punched: picked back up', !(await placed()) && (await has('art_bell')) === 1);
  ok('...and the Scrap Bin knows its price (Medallions)', /medallion/.test(await run('data get storage bm:scrap table.art_bell')));
  await run('clear TestRat');

  // ================================================================== 4. a relic
  await run('loot give TestRat loot bm:items/relic_frost'); await run('effect give TestRat minecraft:slowness 30 1');
  ok('The Rimeheart in the pack: slowness never takes hold', await wait(3000, async () => !/minecraft:slowness/.test(await effects())));
  await run('clear TestRat');

  // ================================================================== 5. the auction, hard mode: an artifact is the first lot
  await run('function bm:p30/abort'); await run('scoreboard players set #hard bm.cfg 1'); await run('scoreboard players set #saled bm.auc -1');
  await run('function bm:admin/auction_now'); await sleep(1500);
  const cur = await run('data get storage bm:auction cur.name');
  ok('A hard-mode Dark Auction: its first lot is one of hard mode\'s artifacts', /☠/.test(cur) && /Shard|Star-Chart|Bell|Dread Heart|Ledger|First Black Market Key/.test(cur), cur.slice(-80));
  await run('function bm:p30/abort'); await run(`scoreboard players set #hard bm.cfg ${isNaN(saved.hard) ? 0 : saved.hard}`);

  // ================================================================== 6. a hard replay's buff (function-level spot check)
  await run(`${O}summon minecraft:zombie ${X + 3.5} ${Y} ${Z + 3.5} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.t225b"]}`); await sleep(400);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t225b] at @s run function bm:p178/hr/buff`);
  const mh = await num(`${O}attribute @e[type=minecraft:zombie,tag=bm.t225b,limit=1] minecraft:max_health get`);
  const hh = await num(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t225b,limit=1] Health`);
  ok('A hard replay\'s buff: 175% health, healed to full', mh === 35 && hh === 35, `${mh} / ${hh}`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t225b]`);

  // ---- put things back
  for (const v of ['pot1', 'potu1', 'poton1']) await run(`scoreboard players set #${v} bm.cfg ${isNaN(saved[v]) ? 0 : saved[v]}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
