// 2.80h: the prize roll, Haul Crates and the win streak - as a regular (non-op) player. rcon sets the stage: a Tier I heist
// of Lever Rooms, the guardian put down once you've walked into the vault, a sword found in the vault (a second Haul).
//   Step onto the strongbox ring: the payout - and the prize roll comes up one at a time: THE HAUL (tier, shares, coins),
//   then the Tokens, a second and more apart. The card says HEIST WON; your streak is one.
//   "Start a new raid": the Fixer unpacks - the sword goes into ONE sealed Haul Crate (in your pack: no locker claimed),
//   labelled with the tier; no loose sword. Plan, pay, win again: WIN STREAK x2 on the screen and on the card.
//   Home: the streak ends. Set the crate down: it's a Haul (minded, opens), the sword inside.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async (t) => new RegExp(`"${t.replace('.', '\\.')}"`).test(await run('data get entity TestRat Tags'));
  const G = 'execute in bm:gutter run ';
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  for (const f of ['prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);
  await run('scoreboard players set TestRat bm.gstk 0');
  const seen = []; let nT = 0; const tick = setInterval(() => { while (nT < A.titles.length) seen.push([A.titles[nT++], Date.now()]); }, 50);
  const titleAt = re => (seen.find(([t]) => re.test(t)) || [0, 0])[1];

  // ---- a won heist: the guardian down (the stage), then the strongbox ring - stepped on
  const winHeist = async () => {
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
    const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
    await run(`execute in bm:gutter as ${V} at @s run tp TestRat ${rel(6, 4, 12)} -90 0`);
    await wait(12000, async () => (await cnt(B)) === 1 && !/bm\.cfrz/.test(await run(`${G}data get entity ${B} Tags`)));
    await run(`${G}data modify entity ${B} DeathLootTable set value "minecraft:empty"`); await run(`${G}kill ${B}`);
    await wait(12000, async () => (await num(`${G}scoreboard players get ${V} bm.gvs`)) === 2);
    const vp = (await run(`${G}data get entity ${V} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    const px = Math.floor(+vp[1]) + 16, pz = Math.floor(+vp[3]) - 3;
    await run(`execute in bm:gutter as ${V} at @s run tp TestRat ${rel(24, 4, 9)} -90 0`); await sleep(600);
    seen.length = 0; A.chats.length = 0;
    await A.walkTo(px + 0.5, pz + 0.5); await sleep(300);
    return wait(5000, async () => has('bm.rv') || seen.some(([t]) => /THE HAUL/.test(t)));
  };
  await heist('levers', 'a', 1); await begin(); await sleep(1500);
  await run('clear TestRat *[minecraft:custom_data~{bm_haul:2b}]');
  ok('stepped onto the strongbox ring: the payout', await winHeist());
  await wait(9000, async () => titleAt(/Tokens/) > 0);
  const tH = titleAt(/THE HAUL/), tT = titleAt(/Tokens/);
  ok('the prize roll: THE HAUL first (tier, shares, coins)...', tH > 0 && seen.some(([t]) => /Tier 1 - \d+ shares, \d+ coins/.test(t)), seen.map(s => s[0]).join(' | ').slice(0, 200));
  ok('...then the Tokens, a beat later (one at a time)', tT > tH && tT - tH >= 1000, `${tT - tH} ms`);
  const resOf = async () => { await run('execute as TestRat run function bm:p103/res_load'); return run('data get storage bm:ui res.r_res'); };
  ok('the card: HEIST WON; your streak is one', /HEIST WON/.test(await resOf()) && (await sc('bm.gstk')) === 1, `streak ${await sc('bm.gstk')}`);

  // ---- carry on: what's left sealed in one Haul Crate
  await run('give TestRat minecraft:barrel[minecraft:custom_data={bm_haul:1b},minecraft:container=[{slot:0,item:{id:"minecraft:diamond_sword",count:1}}]]');   // (the stage: a sword found)
  await wait(6000, async () => has('bm.gvask'));
  A.chats.length = 0; A.cmd('trigger bm.act set 7721'); await sleep(1200);
  const CR = 'Inventory[{components:{"minecraft:custom_data":{bm_haul:2b}}}].components';     // (asked piece by piece: rcon cuts a long reply short)
  const cname = await run(`data get entity TestRat ${CR}."minecraft:custom_name".text`);
  const csword = await run(`data get entity TestRat ${CR}."minecraft:container"[{item:{id:"minecraft:diamond_sword"}}].item.id`);
  const clore = await run(`data get entity TestRat ${CR}."minecraft:lore"[1].text`);
  ok('"Start a new raid": the sword is sealed in one Haul Crate, in your pack', /Haul Crate/.test(cname) && /diamond_sword/.test(csword), `${cname.slice(-40)} | ${csword.slice(-40)}`);
  ok('...labelled with the tier and what\'s inside', /A Tier I haul: \d+ stack/.test(clore), clore.slice(-60));
  ok('...and no loose sword in your pack', !/Found [1-9]/.test(await run('clear TestRat minecraft:diamond_sword 0')));
  ok('...the Fixer says so', A.chats.some(c => /Sealed in 1 Haul Crate/.test(c)), A.chats.filter(c => /Haul|Sealed|unpacks/.test(c)).join(' | ').slice(0, 200));

  // ---- the next job, won: the streak grows
  A.cmd('trigger bm.act set 7601'); await sleep(800); A.cmd('trigger bm.act set 7613'); await sleep(5000);
  const GI2 = await num('scoreboard players get TestRat bm.gvi');
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI2}},limit=1] at @s run tp TestRat ~ ~ ~`);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI2}},limit=1] at @s run setblock ${rel(23, 5, 15)} minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
  await sleep(1500);
  ok('the next job planned and under way (Tokens from the last one paid the fee)', await has('bm.gvp'), `gvi ${GI2}`);
  ok('...won again', await winHeist());
  ok('...the roll shows WIN STREAK x2', await wait(14000, async () => seen.some(([t]) => /WIN STREAK x2/.test(t))), seen.map(s => s[0]).join(' | ').slice(0, 300));
  ok('...and so does the card', /win streak x2/.test(await resOf()) && (await sc('bm.gstk')) === 2);

  // ---- home: the streak ends; the crate set down is a Haul
  await wait(6000, async () => has('bm.gvask'));
  A.cmd('trigger bm.act set 7720');
  await wait(9000, async () => /overworld/.test(await run('data get entity TestRat Dimension'))); await sleep(2000);
  ok('home: the streak ends', (await sc('bm.gstk')) === 0, `streak ${await sc('bm.gstk')}`);
  const pos = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [x, y, z] = [Math.floor(+pos[1]), Math.floor(+pos[2]), Math.floor(+pos[3])];
  await run(`fill ${x - 3} ${y - 1} ${z - 3} ${x + 3} ${y - 1} ${z + 3} minecraft:stone`); await run(`fill ${x - 3} ${y} ${z - 3} ${x + 3} ${y + 3} ${z + 3} minecraft:air`);
  await run(`tp TestRat ${x + 0.5} ${y} ${z + 0.5} 0 45`); await sleep(800);
  const cs = (await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:2b}}}].Slot')).match(/(-?\d+)b?\s*$/);
  let slot = cs ? +cs[1] : -1;
  if (slot > 8) { await run(`item replace entity TestRat hotbar.0 from entity TestRat container.${slot}`); await run(`item replace entity TestRat container.${slot} with minecraft:air`); slot = 0; }
  A.slot(Math.max(0, slot)); await sleep(300);
  A.useOn(x, y - 1, z + 1, 1); await sleep(1500);
  const blk = await run(`data get block ${x} ${y} ${z + 1} Items[{id:"minecraft:diamond_sword"}].id`);
  ok('set down: the crate is a Haul - minded, and the sword inside', /diamond_sword/.test(blk) && (await num(`execute in minecraft:overworld store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.haulm,x=${x + 0.5},y=${y + 0.5},z=${z + 1.5},distance=..1]`)) === 1,
     blk.slice(0, 160));
  await run(`execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=bm.haulm,x=${x + 0.5},y=${y + 0.5},z=${z + 1.5},distance=..1]`); await run(`setblock ${x} ${y} ${z + 1} minecraft:air`);

  clearInterval(tick);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gstk 0');
  for (const f of ['prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'rooms_any', 'variant_random', 'plan_safe']) await run(`function bm:admin/${f}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
