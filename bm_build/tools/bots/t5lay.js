const { bot, rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const run = c => R.run(c);
  const A = await bot('TestRat'); await sleep(2000);
  const num = async c => +(((await run(c)).match(/(?:Count: |has |data: |Found )(-?\d+)/) || [0, -1])[1]);
  const cnt = async sel => +(((await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/) || [0, 0])[1]);
  const KINDS = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters', 'ambush', 'pit'];
  const fights = ['guards', 'ambush', 'pit'];
  let allok = true;
  for (let run_ = 0; run_ < 3; run_++) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('function bm:admin/plan_anywhere'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await sleep(1200);
    await run('clear TestRat'); for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token'); await run('loot give TestRat loot bm:items/fixers_ledger');
    await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7605'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(7000);
    const gi = await num('scoreboard players get TestRat bm.gvi');
    const order = [];
    for (let q = 1; q <= 9; q++) for (const k of KINDS) if ((await cnt(`@e[type=minecraft:marker,tag=bm.gvr_${k},scores={bm.gvq=${q},bm.gvi=${gi}}]`)) >= 1) order.push(`${q}:${k}`);
    const bad = order.filter(o => { const [q, k] = o.split(':'); return (+q % 2 === 0) !== fights.includes(k); });
    console.log(`T5 run ${run_ + 1}:`, order.join(' '), bad.length ? 'BAD ' + bad.join(',') : 'ok');
    if (bad.length) allok = false;
    if (run_ === 2) {
      // resupply on another job: mess up the supplies, win, go again
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(800);
      await run('clear TestRat *[minecraft:custom_data~{bm:"paperweight"}]'); await run('give TestRat minecraft:cooked_beef[minecraft:custom_data={bm_kit:1b}] 5');
      await run('execute as TestRat run function bm:p80/kit/give_1_1');
      await run('clear TestRat minecraft:cooked_beef[minecraft:custom_data~{bm_kit:1b}] 30');
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run function bm:p70/payout'); await sleep(3000);
      console.log('before: paperweights', await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"paperweight"}] 0'), 'beef', await num('execute store result score #t bm.rng run clear TestRat minecraft:cooked_beef 0'));
      for (let i = 0; i < 10; i++) await run('loot give TestRat loot bm:items/token');
      await run('scoreboard players set TestRat bm.act 7721'); await sleep(800);
      await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
      await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(7000);
      const pw = await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"paperweight"}] 0'), bf = await num('execute store result score #t bm.rng run clear TestRat minecraft:cooked_beef 0');
      console.log((pw === 4 && bf === 32 ? 'PASS' : 'FAIL')   /* 2.74: 4 paperweights, 32 food */ + ' another job: paperweights', pw, 'beef', bf, '| gi', await num('scoreboard players get TestRat bm.gvi'));
    }
  }
  console.log(allok ? 'PASS T5 layouts alternate' : 'FAIL T5 layouts');
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  A.end(); R.end(); process.exit(0); })();
