// v2.67c: after the heist - every raider pays their own fee (Tokens pass the coat check); a win pays the fee back and maybe a few
// more (1 at Tier I ... 1-5 at Tier V); the leader is asked (home / a new raid), the crew opts in or out; carrying on unpacks the
// haul (Tokens on you, coins and spoils to the bank, the rest to the locker, then the pack, then the scrap heap); can't pay - home;
// a failed heist asks too; Lucky Raids: 1 in 150 from Tier III, harder, the pool split; raid followers back in 45 s
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16100, Y = 100, Z = 16000;
const BAY = [[-242, 64, -244], [-242, 65, -244], [-242, 64, -243], [-242, 65, -243]];      // locker bay 18's four chests
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2000); const B = await bot('TestMouse'); await sleep(2000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (who, pred) => { const o = await run(`clear ${who} ${pred} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const toks = who => cnt(who, '*[minecraft:custom_data~{bm:"token"}]');
  const hauls = who => cnt(who, '*[minecraft:custom_data~{bm_haul:1b}]');
  const setToks = async (who, n) => { await run(`clear ${who} *[minecraft:custom_data~{bm:"token"}]`); for (let i = 0; i < n; i++) await run(`loot give ${who} loot bm:items/token`); };
  const tags = async who => await run(`data get entity ${who} Tags`);
  const dim = async who => (await run(`data get entity ${who} Dimension`)).replace(/.*data: /, '');
  const act = async (who, code) => { await run(`scoreboard players set ${who} bm.act ${code}`); await sleep(500); };
  const until = async (f, ms = 6000) => { for (let t = 0; t < ms; t += 250) { if (await f()) return true; await sleep(250); } return !!(await f()); };
  const instOf = async who => { const gi = await sc('bm.gvi', who); return `@e[type=marker,tag=bm.gvinst,scores={bm.gvi=${gi}},limit=1]`; };
  const bayCount = async id => { let n = 0; for (const [x, y, z] of BAY) { const o = await run(`execute in bm:gutter run data get block ${x} ${y} ${z} Items`);
    for (const m of o.matchAll(/\{[^{}]*\}/g)) if (m[0].includes(`id: "minecraft:${id}"`)) n += +((m[0].match(/count: (\d+)/) || [0, 1])[1]); } return n; };
  const bayClear = async () => { for (const [x, y, z] of BAY) await run(`execute in bm:gutter run data modify block ${x} ${y} ${z} Items set value []`); };
  const P = (id, n, bm) => `{id:"minecraft:${id}",count:${n}${bm ? `,components:{"minecraft:custom_data":{bm:"${bm}"}}` : ''}}`;
  const crate = items => `minecraft:barrel[minecraft:custom_data={bm_haul:1b},minecraft:container=[${items.map((it, i) => `{slot:${i},item:${it}}`).join(',')}]]`;
  const win = async who => { const gi = await sc('bm.gvi', who);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run function bm:p70/payout`); };
  const fail = async who => { const I = await instOf(who); await run(`execute in bm:gutter as ${I} run function bm:p70/tag_mine`); await run(`execute in bm:gutter as ${I} run function bm:p75/fail`); };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
  for (const p of ['TestRat', 'TestMouse']) {
    await run(`execute in minecraft:overworld run tp ${p} ${X + (p === 'TestRat' ? 0.5 : 2.5)} ${Y + 1} ${Z + 0.5} 0 0`);
    await run(`gamemode survival ${p}`); await run(`clear ${p}`); await run(`effect clear ${p}`);
    await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); await run(`execute as ${p} run function bm:p80/init_me`);
    for (const o of ['bm.crew', 'bm.crewoff', 'bm.fcon', 'bm.gvhc', 'bm.cpcd']) await run(`scoreboard players set ${p} ${o} 0`);
    for (const t of ['bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvin', 'bm.gvwait', 'bm.gvp']) await run(`tag ${p} remove ${t}`);
  }
  await sleep(1200);
  const pid = await sc('bm.pid');
  // TestRat keeps locker bay 18 (emptied); nobody else keeps a bay
  await run('scoreboard players set @e[type=interaction,tag=bm.lkb] bm.lko 0'); await run(`scoreboard players operation @e[type=interaction,tag=bm.lkb18] bm.lko = TestRat bm.pid`); await bayClear();
  // a party: TestRat leads
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestMouse bm.pty = TestRat bm.pid');
  await setToks('TestRat', 20); await setToks('TestMouse', 6);
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  const plan = async (tier, lives = 7613) => {
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };

  // ---- 1. every raider pays their own fee; Tokens pass the coat check
  await plan(1);
  ok('In: the leader and the party member', /bm.gvp/.test(await tags('TestRat')) && /bm.gvp/.test(await tags('TestMouse')));
  ok('Each pays their own fee (Tier I: 2 Tokens) - and keeps the rest on them in the vault', (await toks('TestRat')) === 18 && (await toks('TestMouse')) === 4,
     `${await toks('TestRat')} / ${await toks('TestMouse')}`);
  const ret0 = await run(`data get storage bm:gv ret.p${pid}`);

  // ---- 2. the Fixer's prize: the fee back for sure, and maybe 1 (Tier I) ... 1-5 (Tier V) more
  const sure = { 1: 2, 2: 3, 3: 4, 4: 5, 5: 6 }; let bounds = true, bonus5 = 0, detail = '', seen = {};
  for (let t = 1; t <= 5; t++) {
    let lo = 99, hi = 0;
    for (let i = 0; i < 30; i++) {
      await run(`scoreboard players set #gt bm.rng ${t}`); await run('scoreboard players set #pb bm.rng 0'); await run('scoreboard players set #plu bm.rng 0'); await run('scoreboard players set #th bm.rng 2');
      await run('execute as TestRat at @s run function bm:p75/prize');
      const n = await num('scoreboard players get #ptk bm.rng'); lo = Math.min(lo, n); hi = Math.max(hi, n); if (t === 5 && n > sure[5]) bonus5++;
    }
    detail += `T${t} ${lo}-${hi}  `; if (lo !== sure[t] || hi > sure[t] + t) bounds = false;
  }
  ok('A won heist: the fee back for sure, and never more than the tier in extra (T1 +1 ... T5 +5)', bounds, detail);
  ok('...and now and then a few extra (Tier V: about a third of the time)', bonus5 >= 3 && bonus5 <= 20, `${bonus5} of 30`);
  let luckyOk = true;
  for (let t = 3; t <= 5; t++) { await run(`scoreboard players set #gt bm.rng ${t}`); await run('scoreboard players set #plu bm.rng 1'); await run('execute as TestRat at @s run function bm:p75/prize');
    if ((await num('scoreboard players get #ptk bm.rng')) !== sure[t] + t) luckyOk = false; }
  await run('scoreboard players set #plu bm.rng 0');
  ok('...a Lucky Raid: always the most extra (Tier III +3, IV +4, V +5)', luckyOk);
  let plainOk = true;
  for (let t = 1; t <= 5; t++) { await run('scoreboard players set #th bm.rng 1'); await run(`scoreboard players set #gt bm.rng ${t}`); await run('execute as TestRat at @s run function bm:p75/prize');
    if ((await num('scoreboard players get #ptk bm.rng')) !== sure[t]) plainOk = false; }
  await run('scoreboard players set #th bm.rng 2');
  ok('...a plain or gutter haul still pays the fee back (just no extra)', plainOk);
  await run('execute in bm:gutter run data remove block -200 64 -197 Items'); await run('execute in bm:gutter run data remove block -198 64 -197 Items');

  // ---- 3. won: the leader is asked
  await win('TestRat');
  ok('Won: a few seconds on, the leader is asked - home, or another job', await until(async () => /bm.gvask/.test(await tags('TestRat')), 8000));
  ok('...the member is not (they wait on the leader)', !/bm.gvask/.test(await tags('TestMouse')) && B.chats.some(c => /Waiting on/.test(c)), B.chats.slice(-1)[0]);
  ok('...the choice is in chat too, as buttons', A.chats.some(c => /Back to the Overworld/.test(c) && /Start a new raid/.test(c)));

  // ---- 4. a new raid: TestRat's haul (a known one) is unpacked; the plans open; the member is asked
  await run('clear TestRat *[minecraft:custom_data~{bm_haul:1b}]');
  await run(`give TestRat ${crate([P('paper', 5, 'token'), P('paper', 20, 'gutter_coin'), P('paper', 1, 'gutter_medallion'), P('paper', 3, 'copper_cog'), P('diamond', 2), P('oak_log', 16)])}`);
  await run(`execute in bm:gutter at TestRat align xyz run setblock ~2 ~1 ~ minecraft:barrel{Items:[{Slot:0b,id:"minecraft:emerald",count:3}]}`);
  await run(`execute in bm:gutter at TestRat align xyz positioned ~2.5 ~1.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.haulm","bm.t104h"]}`);
  await run(`scoreboard players operation @e[type=marker,tag=bm.t104h] bm.pid = TestRat bm.pid`);
  const tok0 = await toks('TestRat'), gbc0 = await sc('bm.gbc'), gb10 = await sc('bm.gb1'), tokM0 = await toks('TestMouse'), hM0 = await hauls('TestMouse');
  A.chats.length = 0;
  await act('TestRat', 7721);
  ok('Start a new raid: the haul is unpacked - no crate left, in the pack or set down', (await hauls('TestRat')) === 0 &&
     !/passed/i.test(await run('execute if entity @e[type=marker,tag=bm.t104h]')));
  ok('...its Tokens on you', (await toks('TestRat')) === tok0 + 5, `${tok0} -> ${await toks('TestRat')}`);
  ok('...its coins (and a Gutter Medallion, as 16) into the Gutter Bank', (await sc('bm.gbc')) === gbc0 + 36, `${gbc0} -> ${await sc('bm.gbc')}`);
  ok('...its spoils into the bank as spoils', (await sc('bm.gb1')) === gb10 + 3, `${gb10} -> ${await sc('bm.gb1')}`);
  ok('...everything else into your locker (the crate you set down too)', (await bayCount('diamond')) === 2 && (await bayCount('oak_log')) === 16 && (await bayCount('emerald')) === 3,
     `${await bayCount('diamond')} ${await bayCount('oak_log')} ${await bayCount('emerald')}`);
  ok('...and the Fixer says where it all went', A.chats.some(c => /unpacks your haul/.test(c)) && A.chats.some(c => /Into your locker: 3/.test(c)), A.chats.filter(c => /Into|Tokens on/.test(c)).join(' | '));
  ok('...then the Heist Plans open for the leader', /bm.gvnext/.test(await tags('TestRat')) && (await sc('bm.menu')) === 1100);
  ok('...the member is asked to opt in or out', /bm.gvoffer/.test(await tags('TestMouse')) && B.chats.some(c => /Count me in/.test(c)));
  await act('TestMouse', 7722);
  ok('The member opts in: their haul unpacked too (their fee back on them)', /bm.gvin/.test(await tags('TestMouse')) && A.chats.some(c => /TestMouse is in/.test(c)) &&
     hM0 >= 1 && (await hauls('TestMouse')) === 0 && (await toks('TestMouse')) >= tokM0 + 2, `${hM0} crate(s); ${tokM0} -> ${await toks('TestMouse')}`);
  const gi1 = await sc('bm.gvi'), tR = await toks('TestRat'), tM = await toks('TestMouse');
  await plan(2);
  ok('The new raid: both in a fresh heist (still in the vault)', (await sc('bm.gvi')) !== gi1 && (await sc('bm.gvi', 'TestMouse')) === (await sc('bm.gvi')) &&
     /gutter/.test(await dim('TestRat')) && /bm.gvp/.test(await tags('TestMouse')), `${gi1} -> ${await sc('bm.gvi')} / ${await sc('bm.gvi', 'TestMouse')}`);
  ok('...each paid again from their pocket (Tier II: 3 Tokens)', (await toks('TestRat')) === tR - 3 && (await toks('TestMouse')) === tM - 3, `${tR}->${await toks('TestRat')} / ${tM}->${await toks('TestMouse')}`);
  ok('...the way home is still the Overworld one from before', (await run(`data get storage bm:gv ret.p${pid}`)) === ret0, (await run(`data get storage bm:gv ret.p${pid}`)).slice(-80));
  ok('...the deciding is over (no tags left over)', !/bm.gvnext|bm.gvask/.test(await tags('TestRat')) && !/bm.gvin|bm.gvoffer/.test(await tags('TestMouse')));

  // ---- 5. raid followers: back in 45 seconds - in the vault only
  await run('scoreboard players set TestRat bm.cpcd 300'); await sleep(1600);
  ok('A follower fainting in the vault: back in 45 seconds', (await sc('bm.cpcd')) <= 45, `${await sc('bm.cpcd')}`);

  // ---- 6. Lucky Raids: harder (a guard half again as tough)
  const gi2 = await sc('bm.gvi'); const s2 = gi2 - 1;
  const zs = await num('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr_lobby,scores={bm.gvi=' + gi2 + '},limit=1] Pos[2]');
  const hpOne = async (lucky) => { await run(`scoreboard players set #lu${s2} bm.gvlu ${lucky}`); await run(`scoreboard players set #gi bm.rng ${gi2}`);
    await run('scoreboard players set #gt bm.rng 2'); await run('scoreboard players set #gm bm.rng 0');
    await run(`execute in bm:gutter positioned 3.5 68 ${zs + 2} run function bm:p70/guard`); await sleep(150);
    const o = await run(`execute in bm:gutter as @e[tag=bm.gvg,scores={bm.gvi=${gi2}},sort=nearest,limit=1,x=3.5,y=68,z=${zs + 2}] run attribute @s minecraft:max_health get`);
    const v = +((o.match(/is ([\d.]+)/) || [0, NaN])[1]);
    await run(`execute in bm:gutter run kill @e[tag=bm.gvg,scores={bm.gvi=${gi2}}]`); return v; };
  const hps = async (lucky) => { const out = []; for (let i = 0; i < 11; i++) out.push(await hpOne(lucky));      // (the commonest: a plain guard - an odd one, Tiny or Hulking, is rarer)
    const f = {}; for (const v of out.filter(v => v > 0)) f[v] = (f[v] || 0) + 1; return +Object.entries(f).sort((a, b) => b[1] - a[1])[0][0]; };
  const g0 = await hps(0), g1 = await hps(1);
  ok('A Lucky Raid\'s guards: half again as tough', g0 > 0 && g1 / g0 > 1.4 && g1 / g0 < 1.6, `${g0} -> ${g1}`);
  await run(`scoreboard players set #lu${s2} bm.gvlu 0`);
  const cl = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p70/s0/claim.mcfunction', 'utf8');
  ok('Lucky Raids: 1 in 150, and only from Tier III', /random value 1\.\.150/.test(cl) && /#t bm\.rng matches 3\.\. if score #r bm\.rng matches \.\.1 run scoreboard players set #lu0 bm\.gvlu 1/.test(cl));

  // ---- 7. a Lucky win, two raiders: the pool split, the odd Token to the leader
  await run('scoreboard players set #lpool bm.gvlp 101');
  const I2 = await instOf('TestRat');
  await run(`execute in bm:gutter as ${I2} run scoreboard players set @s bm.gvlu 1`);
  A.chats.length = 0;
  await win('TestRat'); await sleep(800);
  ok('A Lucky win, two raiders, a pool of 101: 50 each', (await num('scoreboard players get #lpe bm.rng')) === 50 && (await num('scoreboard players get #lrm bm.rng')) === 1);
  ok('...and the odd Token to the leader', A.chats.some(c => /odd 1 to the leader, TestRat/.test(c)), A.chats.filter(c => /LUCKY|odd/.test(c)).join(' | '));
  await run(`execute in bm:gutter as ${I2} run scoreboard players set @s bm.gvlu 0`);

  // ---- 8. another job - the member has 3 Tokens (enough to opt in), but the leader picks Tier III (4): left behind, home
  ok('Won again: the leader is asked', await until(async () => /bm.gvask/.test(await tags('TestRat')), 8000));
  const tR8 = await toks('TestRat');
  await run('clear TestMouse *[minecraft:custom_data~{bm_haul:1b}]'); await setToks('TestMouse', 3);
  await act('TestRat', 7721); await act('TestMouse', 7722);
  ok('The leader\'s Lucky haul unpacked: at least the 51 Tokens on him', (await toks('TestRat')) >= tR8 + 51, `${tR8} -> ${await toks('TestRat')}`);
  ok('A member with 3 Tokens may opt in', /bm.gvin/.test(await tags('TestMouse')));
  const tR8b = await toks('TestRat');
  await plan(3);
  ok('...but the plan is Tier III (4 Tokens): left behind - home', !/bm.gvp/.test(await tags('TestMouse')) && /overworld/.test(await dim('TestMouse')), await dim('TestMouse'));
  ok('...the leader goes on alone, 4 Tokens lighter', /bm.gvp/.test(await tags('TestRat')) && /gutter/.test(await dim('TestRat')) && (await toks('TestRat')) === tR8b - 4, `${tR8b} -> ${await toks('TestRat')}`);

  // ---- 9. storage full: the Fixer scraps what won't fit (and banks the Tokens that won't) - with a warning
  await run('clear TestRat');
  for (const [x, y, z] of BAY) await run(`execute in bm:gutter run data modify block ${x} ${y} ${z} Items set value [${[...Array(27).keys()].map(k => `{Slot:${k}b,id:"minecraft:stone",count:1}`).join(',')}]`);
  for (let n = 0; n < 36; n++) await run(`item replace entity TestRat container.${n} with minecraft:cobblestone 1`);
  await run(`item replace entity TestRat weapon.offhand with ${crate([P('paper', 3, 'token'), P('diamond', 2), P('oak_log', 16)])}`);
  const gbc9 = await sc('bm.gbc'); A.chats.length = 0;
  await run('execute as TestRat at @s run function bm:p102/unpack'); await sleep(300);
  ok('Pack and locker full: the Tokens banked at 32 coins, the rest scrapped for coins (diamonds 12 each, a stack of logs 1)', (await sc('bm.gbc')) === gbc9 + 96 + 24 + 1,
     `${gbc9} -> ${await sc('bm.gbc')}`);
  ok('...and a warning: storage full', A.chats.some(c => /locker and your pack are full/.test(c) && /scrapped 2 stack/.test(c)) && A.chats.some(c => /No room for 3 Tokens/.test(c)),
     A.chats.filter(c => /full|room/.test(c)).join(' | '));
  ok('...the crate is gone', (await hauls('TestRat')) === 0);
  await run('clear TestRat'); await bayClear(); await run('loot give TestRat loot bm:items/fixers_ledger');

  // ---- 10. the leader picks a job they can't pay for: the plans come back - and a cheaper one goes ahead
  await fail('TestRat');
  ok('Failed: back in the den, and the leader is asked (no free rebuild)', await until(async () => /bm.gvask/.test(await tags('TestRat')), 9000));
  await setToks('TestRat', 3);
  await act('TestRat', 7721);
  const gi10 = await sc('bm.gvi');
  await plan(5);
  ok('Tier V (6 Tokens) with only 3: refused - the plans come back', /bm.gvnext/.test(await tags('TestRat')) && (await sc('bm.menu')) === 1100 && (await sc('bm.gvi')) === gi10 && (await toks('TestRat')) === 3,
     `${await sc('bm.menu')} ${await toks('TestRat')}`);
  await plan(1);
  ok('...Tier I goes ahead (2 Tokens)', (await sc('bm.gvi')) !== gi10 && (await toks('TestRat')) === 1 && !/bm.gvnext/.test(await tags('TestRat')));

  // ---- 11. the leader can't cover even Tier I: home
  await fail('TestRat');
  await until(async () => /bm.gvask/.test(await tags('TestRat')), 9000);
  await act('TestRat', 7721); await sleep(500);
  ok('A leader without a Tier I fee who presses "new raid": home', /overworld/.test(await dim('TestRat')) && !/bm.gvp|bm.gvask|bm.gvnext/.test(await tags('TestRat')), await dim('TestRat'));
  await sleep(2500);
  ok('...and the Tokens carried in the vault come home in the pack (1)', (await toks('TestRat')) === 1, `${await toks('TestRat')}`);
  await run('scoreboard players set TestRat bm.cpcd 300'); await sleep(1600);
  ok('Outside the vault a faint keeps its 5 minutes', (await sc('bm.cpcd')) > 290, `${await sc('bm.cpcd')}`);
  await run('scoreboard players set TestRat bm.cpcd 0');

  // ---- 12. a member who opts in with no fee on them: home at once; one who opts out: home
  await setToks('TestRat', 20); await setToks('TestMouse', 4);
  await run(`execute in minecraft:overworld run tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
  await plan(1);
  await fail('TestRat'); await until(async () => /bm.gvask/.test(await tags('TestRat')), 9000);
  await setToks('TestMouse', 1); A.chats.length = 0;
  await act('TestRat', 7721); await act('TestMouse', 7722);
  ok('A member opting in without a Tier I fee (1 Token): home at once', /overworld/.test(await dim('TestMouse')) && !/bm.gvp|bm.gvin/.test(await tags('TestMouse')) &&
     A.chats.some(c => /TestMouse can't cover a fee/.test(c)), await dim('TestMouse'));
  await act('TestRat', 7720);
  ok('...and the leader can still call it off: home', /overworld/.test(await dim('TestRat')));
  await setToks('TestMouse', 4);
  await run(`execute in minecraft:overworld run tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
  await plan(1);
  await fail('TestRat'); await until(async () => /bm.gvask/.test(await tags('TestRat')), 9000);
  await act('TestRat', 7721); await act('TestMouse', 7723);
  ok('A member who opts out heads home', /overworld/.test(await dim('TestMouse')) && !/bm.gvp/.test(await tags('TestMouse')));
  await act('TestRat', 7720);

  // ---- 13. a win, and the leader walks out mid-decision: the haul comes home as a crate; the choice passes on
  await setToks('TestMouse', 4);
  await run(`execute in minecraft:overworld run tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
  await plan(1);
  await win('TestRat'); await until(async () => /bm.gvask/.test(await tags('TestRat')), 9000);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(600);
  ok('The leader takes the plate home mid-decision: the choice passes to whoever\'s left', /bm.gvask/.test(await tags('TestMouse')) && !/bm.gvask/.test(await tags('TestRat')),
     `${await tags('TestMouse')}`);
  await sleep(2500);
  ok('...and their haul comes home with them, a crate as ever', (await hauls('TestRat')) >= 1 && /overworld/.test(await dim('TestRat')), `${await hauls('TestRat')}`);
  await act('TestMouse', 7720);
  ok('...the one left can call it a night: home', /overworld/.test(await dim('TestMouse')) && !/bm.gvp/.test(await tags('TestMouse')));
  await run('scoreboard players set @e[type=interaction,tag=bm.lkb18] bm.lko 0');
  for (const p of ['TestRat', 'TestMouse']) { await run(`scoreboard players reset ${p} bm.pty`); await run(`clear ${p}`); }
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });
