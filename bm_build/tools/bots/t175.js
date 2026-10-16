// 2.80a: the Gutter Bank a page per currency - as a regular (non-op) player, every button pressed as the client got it
// (rcon only sets the stage: an account with spoils, coins and Medallions in it, a Ledger in the pack).
// The Ledger -> Gutter Bank: every currency on its own button with its balance. Copper Cogs: Take 1, Take 10, Take all;
// Deposit 1, Deposit 10, Deposit all - each one exactly, back on the same page with the numbers right. Gutter Coins: takes
// come from loose coins only (a Medallion is never melted down); Medallions: one at a time, worth 16 each in the account.
// "Deposit everything" still takes the lot. A button from an old page can't act on another currency.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  // (every button is a command, and the server kicks a client for more than ~10 in a burst (disconnect.spam): one a second)
  const press = async (re) => { const b = await A.press(re); await sleep(1000); return b; };
  const labels = () => A.buttons().map(b => b.label.replace(/[^\x20-\x7e]/g, '').trim());
  const O = 'execute in minecraft:overworld run ';
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage: a platform, a Ledger, an account: 25 cogs, 3 Medallions + 40 loose coins (bm.gbc 88), nothing on hand
  await run(`${O}forceload add 13290 13290 13310 13310`); await run(`${O}fill 13295 120 13295 13305 120 13305 minecraft:stone`);
  await run(`${O}tp TestRat 13300.5 121 13300.5 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await sleep(1500); A.stand();
  for (const [o, v] of [['bm.gb1', 25], ['bm.gbm', 3], ['bm.gbt', 0], ['bm.gbc', 88]]) await run(`scoreboard players set TestRat ${o} ${v}`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); A.slot(0); await sleep(500);
  const office = async () => { A.slot(0); await sleep(250); await A.useWait(); };
  await office(); await press(/Gutter Bank/);
  const acct = labels();
  ok('the account: a button per currency, each with its balance', acct.some(l => /^Copper Cogs\s+25$/.test(l)) && acct.some(l => /^Gutter Medallions\s+3$/.test(l)) &&
     acct.some(l => /^Gutter Coins\s+40$/.test(l)) && acct.some(l => /Deposit everything/.test(l)), acct.join(' | '));
  await press(/^Copper Cogs/);
  ok('Copper Cogs: its own page - Deposit 1 / 10 / all, Take 1 / 10 / all', ['Deposit 1', 'Deposit 10', 'Deposit all', 'Take 1', 'Take 10', 'Take all'].every(w => labels().some(l => l.startsWith(w))), labels().join(' | '));
  const step = async (re, cogs, bank, what) => { await press(re); await sleep(400);
    ok(what, (await has('copper_cog')) === cogs && (await sc('TestRat', 'bm.gb1')) === bank && labels().some(l => l.startsWith('Take 1')),
       `on you ${await has('copper_cog')} (want ${cogs}), account ${await sc('TestRat', 'bm.gb1')} (want ${bank})`); };
  await step(/Take 1$/, 1, 24, 'Take 1: one cog in hand, 24 left - and back on the cog page');
  await step(/Take 10$/, 11, 14, 'Take 10: ten more');
  await step(/Deposit 1$/, 10, 15, 'Deposit 1: one back in');
  await step(/Deposit 10$/, 0, 25, 'Deposit 10: ten back in');
  await step(/Take all/, 25, 0, 'Take all: all 25');
  await step(/Take 1$/, 25, 0, 'Take 1 with none in the account: nothing happens');
  await step(/Deposit all/, 0, 25, 'Deposit all: every one you carry');
  // coins: loose only
  await press(/Your account/); await press(/^Gutter Coins/);
  await press(/Take all/); await sleep(400);
  ok('Gutter Coins, Take all: the 40 loose coins - the 3 Medallions stay whole in the account', (await has('gutter_coin')) === 40 && (await sc('TestRat', 'bm.gbm')) === 3 && (await sc('TestRat', 'bm.gbc')) === 48,
     `coins ${await has('gutter_coin')}, medallions ${await sc('TestRat', 'bm.gbm')}, worth ${await sc('TestRat', 'bm.gbc')}`);
  await press(/Take 10$/); await sleep(400);
  ok('...Take 10 now: none loose - nothing taken, no Medallion broken', (await has('gutter_coin')) === 40 && (await sc('TestRat', 'bm.gbm')) === 3);
  await press(/Deposit 10$/); await sleep(400);
  ok('...Deposit 10: ten in', (await has('gutter_coin')) === 30 && (await sc('TestRat', 'bm.gbc')) === 58);
  // Medallions
  await press(/Your account/); await press(/^Gutter Medallions/);
  await press(/Take 1$/); await sleep(400);
  ok('Gutter Medallions, Take 1: one Medallion, the account 16 coins lighter', (await has('gutter_medallion')) === 1 && (await sc('TestRat', 'bm.gbm')) === 2 && (await sc('TestRat', 'bm.gbc')) === 42,
     `medallions on you ${await has('gutter_medallion')}, in account ${await sc('TestRat', 'bm.gbm')}, worth ${await sc('TestRat', 'bm.gbc')}`);
  await press(/Deposit all/); await sleep(400);
  ok('...Deposit all: back as a Medallion', (await has('gutter_medallion')) === 0 && (await sc('TestRat', 'bm.gbm')) === 3 && (await sc('TestRat', 'bm.gbc')) === 58);
  // Deposit everything still takes the lot
  await press(/Your account/); await press(/Deposit everything/); await sleep(400);
  ok('Deposit everything: the 30 coins in too', (await has('gutter_coin')) === 0 && (await sc('TestRat', 'bm.gbc')) === 88);
  // an action with no currency page open: stale, nothing moves
  await run('scoreboard players set TestRat bm.menu 7802'); A.cmd('trigger bm.act set 7983'); await sleep(600);
  ok('a Take button with no currency page open: nothing moves', (await has('copper_cog')) === 0 && (await sc('TestRat', 'bm.gb1')) === 25);
  await run('clear TestRat'); await run(`${O}forceload remove 13290 13290 13310 13310`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
