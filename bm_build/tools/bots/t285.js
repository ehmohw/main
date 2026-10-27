// 2.94z: BENDER'S RAGE, CHOMP BY CHOMP, as a regular (non-op) player - Bender called with his own ball, three monsters set down
// still before him and his rage's charge wound forward (rcon: the stage). Each monster's health watched as he goes: every drop a chomp.
//   No honours: the first in the chain chomped 3 times, each after it once.
//   Fully honoured by Queen Ava (Vitality, Bulwark and Might all V - rcon: the honours' score, as the Font leaves it): 5 on the
//   first, 2 on each after (a Champion of the Tide's own blow, each second, told apart: it isn't a chomp's size).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who) => { const m = (await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const X = 18260, Y = 100, Z = 16440;
  const BV = '@e[type=minecraft:wolf,tag=bm.bvpet,limit=1]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:sandstone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  const hadHn = await score('bm.hn_bender', 'TestRat');
  await run('scoreboard players set TestRat bm.bvcd 0'); await run('tag TestRat add bm.bvmet');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bv_ball');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  A.slot(0); await sleep(300); A.use(); await sleep(400); A.release();
  ok('Bender called with his ball', await wait(6000, async () => (await cnt(BV)) === 1));
  await sleep(1500);

  const chain = async (tagp) => {               // (three still monsters; the rage set off; each one's chomps counted, in the order bitten)
    await run(`${O}tp ${BV} ${X + 0.5} ${Y + 1} ${Z + 3.5}`);
    const tags = [0, 1, 2].map(i => `${tagp}${i}`);
    for (const [i, [dx, dz]] of [[0, 8], [3, 10], [-3, 10]].entries())
      await run(`${O}summon minecraft:zombie ${X + dx + 0.5} ${Y + 1} ${Z + dz + 0.5} {Tags:["${tags[i]}","t285","bm.seen"],PersistenceRequired:1b,Silent:1b,NoAI:1b,` +
                `attributes:[{id:"minecraft:max_health",base:500d},{id:"minecraft:knockback_resistance",base:1d}],Health:500f}`);
    await sleep(500);
    const hp = async (t) => +(((await run(`${O}data get entity @e[tag=${t},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
    const last = {}, n = {}, first = {}, amt = {}; for (const t of tags) { last[t] = await hp(t); n[t] = 0; amt[t] = []; }
    await run(`${O}scoreboard players set ${BV} bm.bvrg 0`);
    const t0 = Date.now(); let k = 0;
    while (Date.now() - t0 < 25000) {
      for (const t of tags) { const h = await hp(t); if (h >= 0 && h < last[t] - 0.01) { n[t]++; amt[t].push(last[t] - h); if (process.env.DBG) console.log('   ', t, 'hp', last[t], '->', h, 'phase', await score('bm.bvrp', BV), 'tick', await score('bm.bvrt', BV), 'state', await score('bm.dqa', BV), 'by', (await run(`${O}execute as @e[tag=${t},limit=1] on attacker run data get entity @s Tags`)).slice(-120)); if (!(t in first)) first[t] = k++; } last[t] = h; }
      if (Date.now() - t0 > 3000 && (await score('bm.bvrp', BV)) === 0) break;
      await sleep(30);
    }
    await run(`${O}kill @e[tag=t285]`); await sleep(500);
    // (a chomp on one monster is always the same blow; a Champion's own blow each second - fully honoured, he is Ava's Champion -
    //  is not his rage's, and isn't counted)
    return tags.filter(t => t in first).sort((a, b) => first[a] - first[b]).map(t => amt[t].filter(d => Math.abs(d - amt[t][0]) < 0.6).length);
  };

  // ---- no honours
  await run('scoreboard players set TestRat bm.hn_bender 0'); await sleep(2200);
  let got = await chain('t285a');
  ok('RAGE, no honours: the first in the chain chomped 3 times, each after it once', JSON.stringify(got) === JSON.stringify([3, 1, 1]), JSON.stringify(got));
  // ---- fully honoured
  await sleep(1000); await run('scoreboard players set TestRat bm.hn_bender 1555');
  ok('(fully honoured: the honours worn - his score 555 and the blessing)', await wait(4000, async () => (await score('bm.hnap', BV)) === 1555));
  got = await chain('t285b');
  ok('RAGE, fully honoured: 5 chomps on the first, 2 on each after', JSON.stringify(got) === JSON.stringify([5, 2, 2]), JSON.stringify(got));

  await run(`scoreboard players set TestRat bm.hn_bender ${hadHn === null ? 0 : hadHn}`);
  await run(`${O}execute as TestRat run function bm:p195/home`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const nn = res.filter(Boolean).length; console.log(`${nn}/${res.length} passed`);
  A.end(); R.end(); process.exit(nn === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
