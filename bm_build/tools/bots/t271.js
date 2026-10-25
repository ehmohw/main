// 2.94o: THE RAID REWARD OVERHAUL (phase218), as a regular (non-op) player TestRat - Tier V heists planned through the Ledger
// (rcon sets the stage: Tokens, the Ledger, the bad-luck count, what the Codex has seen - and pays the heist out at its vault,
// as t104 does, in place of playing seven rooms).
//   twenty dry Tier IV-V wins behind you: the next win's mythic is certain - and the one of its pair you haven't found (the
//     Counterfeiter's Press found: Tier V's own, the Phoenix Plume); the count starts again; the day's first Tier V win marked.
//   another win: the count goes on (or starts again, on a mythic), "Mythic luck" said; the day's first win already claimed.
//   no duplicates: every aura owned but one - the find is that one; Tier V's gear, the Cutlass had - the Scepter.
//   the Office -> the Codex -> RAID ODDS: the table, your count, today's Tier V bonus.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found |data: )(-?\d+)/) || [0, -1])[1]);
  const sc = async o => num(`scoreboard players get TestRat ${o}`);
  const G = 'execute in bm:gutter run ';
  const HA = '-200 64 -197', HB = '-198 64 -197';
  const barrels = async () => (await run(`${G}data get block ${HA} Items`)) + (await run(`${G}data get block ${HB} Items`));
  const clearBarrels = async () => { await run(`${G}data modify block ${HA} Items set value []`); await run(`${G}data modify block ${HB} Items set value []`); };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  for (const f of ['plan_anywhere', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);
  await run('execute in minecraft:overworld run forceload add 12996 12996 13004 13004');
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone');

  // ---- a Tier V heist, planned through the Ledger (the buttons as sent), paid out at its vault
  const unask = async () => { for (const t of ['bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvin', 'bm.gvwait', 'bm.gvp', 'bm.gvwaitd', 'bm.gvpre', 'bm.exon', 'bm.exask']) await run(`tag TestRat remove ${t}`); };   // (the leader's choice after a win: done with)
  const heist = async () => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await unask();
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true');
    await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    for (let k = 0; k < 24; k++) await run('loot give TestRat loot bm:items/token');
    await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 0');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await sleep(2000);
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(900);
    A.cmd('trigger bm.act set 7605'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    const inH = await wait(40000, async () => /passed/.test(await run('execute if entity @a[name=TestRat,tag=bm.gvp]')), 500); await sleep(2500);
    const gi = await sc('bm.gvi');
    const tier = await num(`${G}scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${gi}},limit=1] bm.gvt`);
    return { inH, gi, tier };
  };
  const win = async gi => {
    await clearBarrels(); A.chats.length = 0;
    await run(`${G}execute as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`${G}execute as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run function bm:p70/payout`); await sleep(2500);
  };
  const day = await num('scoreboard players get #day bm.bm');

  // ================================================================== 1. twenty dry wins: the next mythic is certain
  await run('scoreboard players set TestRat bm.mpity 20'); await run('scoreboard players set TestRat bm.t5day -1');
  await run('scoreboard players set TestRat bm.cx_f_counterfeiters_press 1'); await run('scoreboard players set TestRat bm.cx_f_phoenix_plume 0');
  let h = await heist();
  ok('A Tier V heist planned through the Ledger', h.inH && h.gi > 0, `in ${h.inH} gvi ${h.gi} tier ${h.tier}`);
  await win(h.gi);
  ok('won with 20 dry Tier IV-V wins behind: a mythic for certain - the one not found yet (Tier V\'s own Phoenix Plume, the Press found)',
     A.chats.some(c => /found a mythical Phoenix Plume/.test(c)) && (await sc('bm.cx_f_phoenix_plume')) === 1, A.chats.filter(c => /mythical|legendary|Rare find/.test(c)).join(' | ').slice(0, 220));
  ok('...the bad-luck count starts again (0), and says nothing', (await sc('bm.mpity')) === 0 && !A.chats.some(c => /Mythic luck/.test(c)), `${await sc('bm.mpity')}`);
  ok('...the day\'s first Tier V win claimed (a mythic is legendary-or-better: nothing added)', (await sc('bm.t5day')) === day && A.chats.some(c => /first Tier V win today/.test(c)),
     A.chats.filter(c => /Tier V win/.test(c)).join(' | '));

  // ================================================================== 2. another win: the count goes on, said at the end
  await run('scoreboard players set TestRat bm.mpity 3');
  h = await heist(); await win(h.gi);
  const p2 = await sc('bm.mpity'), myth2 = A.chats.some(c => /found a mythical/.test(c));
  ok('another Tier V win without a mythic: the count goes on (3 -> 4), "Mythic luck: 4/20" said (or a mythic, and it starts again)',
     myth2 ? p2 === 0 : (p2 === 4 && A.chats.some(c => /Mythic luck: 4\/20/.test(c))), `count ${p2}, mythic ${myth2} | ${A.chats.filter(c => /Mythic luck/.test(c)).join('')}`);
  ok('...and no second "first Tier V win today"', !A.chats.some(c => /first Tier V win today/.test(c)));

  // ================================================================== 3. no duplicates (an aura; the tier's gear)
  // (the stage: every aura owned but Leo's; the Cutlass had from a heist - the finds' own pickers, as a won heist calls them)
  const auras = (await run('tag TestRat list')).match(/bm\.auown_\w+/g) || [];
  for (const w of ['emma', 'celi', 'zib', 'cecil', 'kw', 'demo', 'apo', 'tul', 'frog', 'don', 'pearl', 'fishy', 'wil', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor',
                   'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones', 'capshun', 'pxcecil', 'pxleo', 'pxemma', 'sky']) await run(`tag TestRat add bm.auown_${w}`);
  await run('tag TestRat remove bm.auown_leo');
  let leo = 0;
  for (let i = 0; i < 4; i++) { await clearBarrels(); await run(`${G}execute as TestRat run function bm:p138/find`);
    if (/cos_aura_leo/.test(await barrels()) && !/cos_aura_(?!leo)/.test(await barrels())) leo++; }
  ok('no duplicates: every aura owned but Leo\'s - each aura find is Leo\'s (4 of 4)', leo === 4, `${leo}`);
  for (const t of ((await run('tag TestRat list')).match(/bm\.auown_\w+/g) || [])) await run(`tag TestRat remove ${t}`);
  for (const t of auras) await run(`tag TestRat add ${t}`);                                 // (as they were)
  await run('scoreboard players set TestRat bm.rg_gutter_cutlass 1'); await run('scoreboard players set TestRat bm.rg_treasurers_scepter 0');
  await clearBarrels(); await run(`${G}scoreboard players set #gt bm.rng 5`); await run(`${G}execute as TestRat run function bm:p105/find_gear5`);
  const b = await barrels();
  ok('...Tier V\'s gear with the Cutlass had: the Treasurer\'s Scepter', /treasurers_scepter/.test(b) && !/gutter_cutlass/.test(b), b.slice(0, 160));
  await clearBarrels();

  // ================================================================== 4. RAID ODDS, off the Codex
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await unask(); A.cmd('trigger bm.act set 2'); await sleep(500);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('scoreboard players set TestRat bm.mpity 7');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await sleep(1500);
  A.dialogN.length = 0; A.slot(7); await sleep(300); await A.useWait(); await sleep(800);
  await A.press(/Codex/); await sleep(800); await A.press(/Raid Odds/); await sleep(900);
  const dl = JSON.stringify(A.dialogN[A.dialogN.length - 1] || '');
  ok('the Office -> the Codex -> RAID ODDS: the table (Tier V\'s mythic 7%), your count (7/20), today\'s bonus (claimed)',
     /RAID ODDS/.test(dl) && /MYTHIC/.test(dl) && /7%/.test(dl) && /7\/20|"7"[^]*\/20/.test(dl) && /claimed/.test(dl), dl.slice(0, 300));

  // ---------------------------------------------------------------- clean up
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('scoreboard players set TestRat bm.mpity 0');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('execute in minecraft:overworld run forceload remove 12996 12996 13004 13004');
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
