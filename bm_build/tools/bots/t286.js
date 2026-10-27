// 2.94z: FOLLOWERS LIT BY THE WORLD, as a regular (non-op) player - each called with their own item, one at a time: the Chef,
// King Omega, Ashur, the Neighbor, Pistachio, Cecil and the Arachno-Lantern. No part of them keeps a fixed brightness (they were as
// bright at midnight as at noon) - but Cecil's eyes, and the Lantern's lit pumpkin head. And a part from before (rcon: its old
// fixed brightness put back, as a world from 2.94y has it) loses it within a couple of seconds.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const X = 18300, Y = 100, Z = 16480;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('tag TestRat add bm.lnmet');
  for (const o of ['bm.kkcd', 'bm.omcd', 'bm.ascd', 'bm.nbcd', 'bm.picd', 'bm.cecd', 'bm.lncd']) await run(`scoreboard players set TestRat ${o} 0`);
  // [name, item, host tag, part tag, the parts allowed their own light, home]
  const K = [['the Chef', 'chef_ladle', 'bm.kkpet', 'bm.kkp', [], 'p186/home'], ['King Omega', 'om_monocle', 'bm.ompet', 'bm.omp', [], 'p170/home'],
             ['Ashur', 'ashur_cinder', 'bm.aspet', 'bm.asp', [], 'p185/home'], ['the Neighbor', 'neighbor_baton', 'bm.nbpet', 'bm.nbp', [], 'p187/home'],
             ['Pistachio', 'pi_cloche', 'bm.pipet', 'bm.pip', [], 'p163/pi/home'], ['Cecil', 'cecil_gem', 'bm.cecilpet', 'bm.cpet', ['bm.cp_eyes'], 'p98/home/cecil'],
             ['the Arachno-Lantern', 'ln_gourd', 'bm.lnpet', 'bm.lnp', ['bm.lnp_head'], 'p194/home']];
  for (const [nm, iid, host, part, keep, home] of K) {
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.slot(0); await sleep(300); A.use(); await sleep(400); A.release();
    if (!ok(`${nm} called`, await wait(6000, async () => (await cnt(`@e[tag=${host}]`)) >= 1))) continue;
    await sleep(3000);                                                     // (a second or two: any part from before has had its pass)
    const lit = (await cnt(`@e[type=minecraft:item_display,tag=${part},nbt={brightness:{}}${keep.map(k => ',tag=!' + k).join('')}]`));
    const all = await cnt(`@e[type=minecraft:item_display,tag=${part}]`);
    const own = keep.length ? await cnt(`@e[type=minecraft:item_display,tag=${part},nbt={brightness:{}},tag=${keep[0]}]`) : 0;
    ok(`...lit by the world: none of ${nm}'s ${all} parts holds a fixed brightness` + (keep.length ? ` (but ${keep[0].replace('bm.', '')}, its own light)` : ''),
       all > 0 && lit === 0 && (!keep.length || own >= 1), `${lit} still lit; own light ${own}`);
    if (nm === 'the Chef') {                                               // (a part from before: its old brightness back)
      await run(`${O}execute as @e[type=minecraft:item_display,tag=bm.kkp] run data merge entity @s {brightness:{block:13,sky:13}}`);
      await run(`${O}tag @e[type=minecraft:item_display,tag=bm.kkp] remove bm.rplit`);
      ok('...a part from before (its old fixed brightness, as a 2.94y world has it) loses it within a couple of seconds',
         await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.kkp,nbt={brightness:{}}]')) === 0));
    }
    await run(`${O}execute as TestRat at @s run function bm:${home}`); await wait(5000, async () => (await cnt(`@e[tag=${host}]`)) === 0); await sleep(500);
  }
  await run('tag TestRat remove bm.lnmet'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
