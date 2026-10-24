// 2.83a: THE DARK AUCTION ON A SALE NIGHT, as a regular (non-op) player TestRat who stays up all night in the auction hall.
//   The stage (rcon): the test market's hall loaded, the day set to a sale night, the player keyed (tier 2), the clock just
//   before dusk. From there the clock runs by itself (time is only nudged forward within the same night, never past a day):
//   the gate sign says TONIGHT; at dusk the doors open (the chat says so); in the hall the player is handed a bidding paddle
//   and told to take a seat; at midnight the first lot is called - the bossbar shows, a lot goes up on the board.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const st = async () => +((await run('scoreboard players get #state bm.auc')).match(/has (-?\d+)/) || [0, -1])[1];
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };

  // the test market (any market marker the server has) and its auction hall
  const A = await bot('TestRat'); await sleep(2500);
  const bars = []; A.on('boss_bar', (p) => bars.push(p));
  const titles = []; A.on('set_title_text', (p) => titles.push(JSON.stringify(p)));
  await run('function bm:admin/auction_stop'); await run('scoreboard players reset #state bm.auc');   // 2.94b: as a world that never held a sale (no #state at all)
  await run('scoreboard players set TestRat bm.tier 2'); await run('gamemode adventure TestRat');
  const MX = 16938, MZ = 16994;
  await run(`${O}forceload add ${MX - 64} ${MZ - 64} ${MX + 64} ${MZ + 64}`); await sleep(3000);
  const hp = (await run(`${O}execute positioned ${MX} 0 ${MZ} run data get entity @e[type=minecraft:marker,tag=bm.ahall,sort=nearest,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (!ok('the test market has its auction hall', !!hp, hp ? hp[0] : 'none')) { console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(1); }
  const [hx, hy, hz] = [+hp[1], +hp[2], +hp[3]];

  // a sale night: day 69 (a seventh day), not yet held, nothing owed; the clock just before dusk
  const base = 240000;
  await run(`time set ${base + 11800}`); await sleep(1200);
  await run('scoreboard players set #bmday bm.bm 69'); await run('scoreboard players set #lastday bm.auc 69'); await run('scoreboard players set #owed bm.auc 0');
  await run('scoreboard players set #saled bm.auc 0'); await run('scoreboard players set #warnd bm.auc 69');
  await run(`${O}tp TestRat ${hx + 4} ${hy} ${hz} 90 0`); await sleep(2500);
  ok('before dusk, a sale night: the gate sign counts 0 days (tonight)', /has 0 /.test(await run('scoreboard players get #signv bm.auc')), await run('scoreboard players get #signv bm.auc'));
  ok('...and the doors are still shut', (await st()) === 0, `state ${await st()}`);

  // dusk: the clock runs into it by itself
  A.chats.length = 0;
  ok('dusk comes (the clock runs): the doors open', await wait(15000, async () => (await st()) === 1), `state ${await st()}`);
  ok('...the chat says so ("doors are open")', await wait(3000, async () => /doors are open/i.test(A.chats.join(' '))), A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('in the hall: a bidding paddle for the night', await wait(4000, async () => (await has('bidding_paddle')) === 1));

  // the night goes on: nudged to just before midnight (same night), then the clock runs into it
  await run(`time set ${base + 17940}`); bars.length = 0; titles.length = 0;
  ok('midnight (the clock runs into it): the first lot is called', await wait(15000, async () => (await st()) >= 2), `state ${await st()}`);
  ok('...the Dark Auction bossbar shows', await wait(4000, async () => bars.length > 0), `${bars.length} bossbar packets`);
  ok('...and a lot is up (#lotn 1)', /has [1-9]/.test(await run('scoreboard players get #lotn bm.auc')), await run('scoreboard players get #lotn bm.auc'));

  // a world whose Blood Moon comes every 20 days (the settings page allows it): the sign and the doors follow the real moon
  await run('function bm:admin/auction_stop'); await run('scoreboard players set #state bm.auc 0');
  await run('scoreboard players set #bmper bm.cfg 20'); await run(`time set ${base + 24000 + 11000}`); await sleep(1200);
  await run('scoreboard players set #bmday bm.bm 29'); await run('scoreboard players set #lastday bm.auc 29'); await run('scoreboard players set #saled bm.auc 0');
  await sleep(2500);
  ok('a 20-day Blood Moon, day 29 (no moon, no seventh day): the sign does NOT say tonight (it used to: 29 of 30)', !/has 0 /.test(await run('scoreboard players get #signv bm.auc')), await run('scoreboard players get #signv bm.auc'));
  await run('scoreboard players set #bmday bm.bm 39'); await run('scoreboard players set #lastday bm.auc 39'); await sleep(2500);
  ok('...day 39, a Blood Moon night: the sign says tonight', /has 0 /.test(await run('scoreboard players get #signv bm.auc')), await run('scoreboard players get #signv bm.auc'));
  await run(`time set ${base + 24000 + 11900}`);
  ok('...and at dusk the doors open', await wait(15000, async () => (await st()) === 1), `state ${await st()}`);
  await run('scoreboard players set #bmper bm.cfg 30');

  await run('function bm:admin/auction_stop'); await run('time set day'); await run('scoreboard players set TestRat bm.tier 0');
  await run(`${O}forceload remove ${MX - 64} ${MZ - 64} ${MX + 64} ${MZ + 64}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log(e); process.exit(1); });
