// 2.80: MENUS - as regular players (rcon sets the stage: what's in the pockets and the accounts, a cleared tier):
// THE RAT BANK opened with the Banker's Card: the account page lists every currency with its balance; a currency's own page
// shows its icon, what's in the account and what's on you; Deposit all and Take 10 work and come back to that page; « back
// to the account; "Deposit everything" banks every currency at once. THE ARMORY (from the Ledger): one short card per
// kit; a kit's page lists its ranks - the owned ones ticked, the next one marked - and Rank up buys it and comes back to the
// page. THE PARTY'S MEMBERS as a dialog: both names with their health and the leader starred; only the leader gets Kick, and
// it kicks. SERVER SETTINGS as a dialog for an operator: a setting's button shows its state and flips it (and a regular
// player can't open it).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const held = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const txt = (c) => JSON.stringify(c.dialogN[c.dialogN.length - 1] || {});
  const btn = (c, re) => c.buttons().find(b => re.test(b.label));
  const press = async (c, re) => { const b = btn(c, re); if (!b) return false; const n = c.dialogN.length; c.cmd(b.command.slice(1)); return wait(2500, async () => c.dialogN.length > n); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance 300 4 true'); await run('effect give TestRat minecraft:slow_falling 300 0 true');

  // ================================================================== the Rat Bank
  await run('loot replace entity TestRat hotbar.1 loot bm:items/bankers_card');
  for (let k = 0; k < 7; k++) await run('loot give TestRat loot bm:items/token');
  for (let k = 0; k < 3; k++) await run('loot give TestRat loot bm:items/blood_crystal');
  await run('scoreboard players set TestRat bm.bk_tok 2'); await run('scoreboard players set TestRat bm.bk_bld 0');
  A.slot(1); await sleep(300); await A.useWait();
  const cur = A.buttons().filter(b => /\s\d+$/.test(b.label));
  ok('The Banker\'s Card opens the account page: every currency on one button with its balance (11)', cur.length === 11 && !!btn(A, /^Tokens\s+2$/) && !!btn(A, /^Blood Crystals\s+0$/) &&
     !!btn(A, /Deposit everything/), A.buttons().map(b => b.label).join(' | ').slice(0, 220));
  await press(A, /^Tokens\s/);
  ok('...Tokens: its own page - the icon, 2 in the account, 7 on you', /Tokens/.test(txt(A)) && /minecraft:item/.test(txt(A)) && /In your account/.test(txt(A)) &&
     /"2"/.test(txt(A)) && /"7"/.test(txt(A)) && !!btn(A, /Deposit all Tokens\s+\(7\)/) && !!btn(A, /^Take all\s+\(2\)/), A.buttons().map(b => b.label).join(' | '));
  await press(A, /Deposit all Tokens/);
  ok('...Deposit all: 9 in the account, none on you - and back on the Tokens page, saying 9', (await sc('TestRat', 'bm.bk_tok')) === 9 && (await held('token')) === 0 &&
     /"9"/.test(txt(A)) && !!btn(A, /^Take all\s+\(9\)/));
  await press(A, /^Take 10$/);
  ok('...Take 10 hands out what there is (9) - the page says 0', (await sc('TestRat', 'bm.bk_tok')) === 0 && (await held('token')) === 9 && !!btn(A, /^Take all\s+\(0\)/));
  await press(A, /Your account/);
  ok('...« back to the account page', !!btn(A, /Deposit everything/) && !!btn(A, /^Tokens\s+0$/));
  await press(A, /Deposit everything/);
  ok('"Deposit everything" banks every currency on you at once (9 Tokens, 3 Blood Crystals)', (await sc('TestRat', 'bm.bk_tok')) === 9 && (await sc('TestRat', 'bm.bk_bld')) === 3 &&
     (await held('token')) === 0 && (await held('blood_crystal')) === 0 && !!btn(A, /^Tokens\s+9$/));

  // ================================================================== the Armory
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gvcl 62'); await run('scoreboard players set TestRat bm.kr1 1');
  await run('scoreboard players set TestRat bm.gbc 100'); await run('scoreboard players set TestRat bm.gb1 10');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); A.slot(0); await sleep(300); await A.useWait();
  await press(A, /Armory/);
  const kits = A.buttons().filter(b => /›$/.test(b.label));
  ok('The Armory: a short card per kit, each kit a button to its own page (4)', kits.length === 4 && !/next: /.test(txt(A)), kits.map(b => b.label).join(' | '));
  const kit1 = kits[0] ? kits[0].label.replace(/\s*›$/, '') : '?';
  await press(A, new RegExp('^' + kit1));
  const t = txt(A);
  ok(`...the ${kit1} kit's page: every rank listed, rank I ticked, rank II marked next`, /KIT/.test(t) && /✔ I /.test(t) && /➜ II /.test(t) && /VI /.test(t) && !!btn(A, /Rank up/) && !!btn(A, /« Armory/));
  A.titles.length = 0;
  await press(A, /Rank up/);
  ok('...Rank up buys rank II (32 coins, 10 spoil) and comes back to the page - II ticked, III next', (await sc('TestRat', 'bm.kr1')) === 2 && (await sc('TestRat', 'bm.gbc')) === 68 &&
     /✔ II /.test(txt(A)) && /➜ III /.test(txt(A)), `rank ${await sc('TestRat', 'bm.kr1')} coins ${await sc('TestRat', 'bm.gbc')}`);
  await press(A, /« Armory/);
  ok('...« back to the Armory', A.buttons().filter(b => /›$/.test(b.label)).length === 4);
  await run('scoreboard players set TestRat bm.kr1 1');

  // ================================================================== the party's members
  const B = await bot('PartyPal'); await sleep(2500); B.stand();
  await run('execute in minecraft:overworld run tp PartyPal 13002.5 120 13000.5'); await run('gamemode survival PartyPal');
  await run('effect give PartyPal minecraft:resistance 300 4 true'); await run('effect give PartyPal minecraft:slow_falling 300 0 true'); await sleep(500);
  A.cmd('trigger bm.party set 3'); B.cmd('trigger bm.party set 3'); await sleep(600);           // (out of any old party first)
  A.cmd('trigger bm.party set 2'); await sleep(700); B.cmd('trigger bm.party set 4'); await sleep(900);
  ok('PartyPal accepts TestRat\'s invite: one party', (await sc('TestRat', 'bm.pty')) > 0 && (await sc('TestRat', 'bm.pty')) === (await sc('PartyPal', 'bm.pty')));
  let n0 = A.dialogN.length; A.cmd('trigger bm.party set 6'); await wait(2500, async () => A.dialogN.length > n0);
  ok('The party\'s members, as a dialog: both names, their health, the leader starred', /TestRat/.test(txt(A)) && /PartyPal/.test(txt(A)) && /★/.test(txt(A)) && /❤/.test(txt(A)) &&
     /2 of 6/.test(txt(A)), txt(A).slice(0, 200));
  ok('...the leader gets a Kick button for the other (not for themself)', !!btn(A, /Kick PartyPal/) && !btn(A, /Kick TestRat/));
  n0 = B.dialogN.length; B.cmd('trigger bm.party set 6'); await wait(2500, async () => B.dialogN.length > n0);
  ok('...a member sees the same list, with no Kick buttons', /TestRat/.test(txt(B)) && /PartyPal/.test(txt(B)) && !btn(B, /Kick/) && !!btn(B, /« Party/));
  await press(A, /Kick PartyPal/);
  ok('...the leader\'s Kick: PartyPal is out of the party', await wait(2500, async () => !((await sc('PartyPal', 'bm.pty')) > 0)), `PartyPal ${await sc('PartyPal', 'bm.pty')}`);

  // ================================================================== server settings (an operator's dialog)
  B.chats.length = 0; n0 = B.dialogN.length; B.cmd('function bm:admin/settings'); await sleep(1200);
  ok('A regular player can\'t open the server settings', B.dialogN.length === n0 && /unknown|incomplete/i.test(B.chats.join(' ')), B.chats.join(' | ').slice(0, 120));
  await run('op TestRat'); await sleep(800);
  const br0 = await sc('#breaker', 'bm.cfg');
  n0 = A.dialogN.length; A.cmd('function bm:admin/settings'); await wait(2500, async () => A.dialogN.length > n0);
  const want = br0 === 1 ? 'On' : 'Off', flip = br0 === 1 ? 'Off' : 'On';
  ok('An operator\'s server settings: a dialog, each setting showing its state on its button', /SERVER SETTINGS/.test(txt(A)) && !!btn(A, new RegExp('^Block Breaker: ' + want + '$')) &&
     !!btn(A, /^Tullius needs Leo: (On|Off)$/) && A.buttons().filter(b => /^Blood Moon: /.test(b.label)).length === 6, A.buttons().map(b => b.label).join(' | ').slice(0, 220));
  await press(A, /^Block Breaker:/);
  ok('...its button flips it - the dialog comes back showing the new state', (await sc('#breaker', 'bm.cfg')) === (br0 === 1 ? 0 : 1) && !!btn(A, new RegExp('^Block Breaker: ' + flip + '$')));
  await press(A, /^Block Breaker:/);
  await run('deop TestRat');
  ok('...and back (setting restored)', (await sc('#breaker', 'bm.cfg')) === br0);

  await run('clear TestRat'); await run('scoreboard players set TestRat bm.bk_tok 0'); await run('scoreboard players set TestRat bm.bk_bld 0');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); B.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
