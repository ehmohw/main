const { bot, rcon, sleep } = require('./lib');
const X = 12300, Y = 200, Z = 12300; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(800); const B = await bot('PartyPal'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => ((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [])[1];
  await run(`fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} stone`); await run(`fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  for (const n of ['TestRat', 'PartyPal']) { await run(`gamemode survival ${n}`); await run(`effect give ${n} resistance 120 4 true`); await run(`trigger bm.party set 3`).catch(()=>{}); }
  A.cmd('trigger bm.party set 3'); B.cmd('trigger bm.party set 3'); await sleep(500);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`tp PartyPal ${X + 3.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
  A.chats.length = 0; B.chats.length = 0;
  A.cmd('trigger bm.party set 2'); await sleep(800);
  ok('Invite: PartyPal gets an [Accept] invite', B.chats.some(c => /invites you/.test(c)), B.chats.slice(-1)[0]);
  B.cmd('trigger bm.party set 4'); await sleep(800);
  const pa = await sc('TestRat', 'bm.pty'), pb = await sc('PartyPal', 'bm.pty');
  ok('Accepted: both in the same party and its team', pa && pa === pb && /passed/.test(await run(`execute if entity @a[name=PartyPal,team=bm.p${pa}]`)) && /passed/.test(await run(`execute if entity @a[name=TestRat,team=bm.p${pa}]`)), `${pa} ${pb}`);
  await run('effect clear TestRat resistance'); const h0 = (await run('data get entity TestRat Health')).match(/([\d.]+)f/)[1];
  await run('damage TestRat 4 minecraft:player_attack by PartyPal'); await sleep(300);
  const h1 = (await run('data get entity TestRat Health')).match(/([\d.]+)f/)[1];
  ok('No friendly fire between party members', +h1 >= +h0, `${h0} -> ${h1}`);
  await sleep(1200);
  ok('The party health list is filled', +(await sc('PartyPal', `bm.ph${pa}`)) > 0, await sc('PartyPal', `bm.ph${pa}`));
  A.chats.length = 0; A.cmd('trigger bm.party set 6'); await sleep(600);
  ok('Members list (with [Kick] for the leader)', A.chats.filter(c => /❤/.test(c)).length === 2 && A.chats.some(c => /Kick/.test(c)), A.chats.slice(-2).join(' | '));
  // boss scaling: two players near a Voidwalker
  await run('effect give TestRat resistance 120 4 true'); await run('time set night');
  await run(`execute positioned ${X} ${Y + 1} ${Z + 8} run function bm:p54/vwk/summon`); await sleep(6500);
  const mx = await run('attribute @e[type=enderman,tag=bm.vwk,limit=1] minecraft:max_health get');
  ok('A boss with 2 players near grows +50% (Voidwalker 450 -> 675)', /675/.test(mx), mx.slice(-40));
  await run('tp PartyPal ~ ~ ~').catch(() => {}); await run(`tp PartyPal ${X + 60} ${Y + 1} ${Z}`); await sleep(6000);
  const mx2 = await run('attribute @e[type=enderman,tag=bm.vwk,limit=1] minecraft:max_health get');
  ok('...and shrinks back when one leaves', /450/.test(mx2), mx2.slice(-40));
  await run('kill @e[tag=bm.vwk]'); await run('kill @e[tag=bm.vwkmin]'); await run('time set day');
  // leaving dissolves a party of two
  await run(`tp PartyPal ${X + 3.5} ${Y + 1} ${Z + 0.5}`); B.cmd('trigger bm.party set 3'); await sleep(800);
  ok('Leaving: a party of one dissolves (team gone)', !(await sc('TestRat', 'bm.pty')) && !/passed/.test(await run(`execute if entity @a[team=bm.p${pa}]`)), await sc('TestRat', 'bm.pty'));
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();
