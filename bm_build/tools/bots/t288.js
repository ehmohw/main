// 2.95b: THE ONES WHO SHINE, as a regular (non-op) player - each called with their own item: KillerWatt (his Spark) and the Sky
// Buddies (the Sky Mobile) are lit through and through, day or night; Cecil is lit by the world in his robes (his eyes aside), and
// handed an Ethereal Gem or a Wraithfire Heart (real right-clicks) shines through and through - and back in his robes (sneak +
// right-click empty-handed), lit by the world again. Emma, charged with a monster near (rcon: her charge, a still husk), takes her
// Ethereal Form and shines - and keeps shining. A Sky Buddy part from 2.94z (rcon: its light taken, as that pass left it) shines again.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`));
  const X = 18300, Y = 100, Z = 16520;
  const uuidOf = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  const clickPet = async (sel, shift = false) => {
    await run(`${O}tp ${sel} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(900);
    const u = await uuidOf(sel); const e = Object.values(A.ents).find(e => e.objectUUID === u); if (!e) return false;
    if (shift) { A.input({ shift: true }); await sleep(250); }
    A.interact(e.entityId, shift); await sleep(700); if (shift) { A.input({}); await sleep(200); } return true; };
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  for (const o of ['bm.kxcd', 'bm.ybcd', 'bm.cpcd', 'bm.emcd']) await run(`scoreboard players set TestRat ${o} 0`);
  const call = async (iid, host) => { await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.slot(0); await sleep(300); A.use(); await sleep(400); A.release(); return wait(6000, async () => (await cnt(`@e[tag=${host}]`)) >= 1); };
  const lit = async (sel) => [await cnt(`@e[type=minecraft:item_display,${sel},nbt={brightness:{block:15}}]`), await cnt(`@e[type=minecraft:item_display,${sel}]`)];
  // ---- KillerWatt, the Sky Buddies
  for (const [nm, iid, host, part, home] of [['KillerWatt', 'kw_spark', 'bm.kxpet', 'tag=bm.kxp,tag=!bm.kxp_boss', 'p98/home/killerwatt'], ['the Sky Buddies', 'sky_mobile', 'bm.ybpet', 'tag=bm.ybp', 'p98/home/sky']]) {
    if (!ok(`${nm} called with their own item`, await call(iid, host))) continue;
    await sleep(2500); const [l, a] = await lit(part);
    ok(`...${nm} shine through and through: ${l} of ${a} parts lit`, a > 0 && l === a);
    if (nm === 'the Sky Buddies') {
      await run(`${O}execute as @e[type=minecraft:item_display,tag=bm.ybp] run data remove entity @s brightness`); await run(`${O}tag @e[type=minecraft:item_display,tag=bm.ybp] add bm.rplit`);
      ok('...a Sky Buddy part from 2.94z (its light taken) shines again within a couple of seconds', await wait(3000, async () => { const [l2, a2] = await lit(part); return a2 > 0 && l2 === a2; }));
    }
    await run(`${O}execute as TestRat at @s run function bm:${home}`); await wait(5000, async () => (await cnt(`@e[tag=${host}]`)) === 0);
  }
  // ---- Cecil: his robes, the Ethereal Gem, the Wraithfire Heart, his robes again
  const CS = '@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]';
  await run('scoreboard players set TestRat bm.cpel 0');
  if (ok('Cecil called with his gem', await call('cecil_gem', 'bm.cecilpet'))) {
    await sleep(2500);
    const body = 'tag=bm.cpet,tag=!bm.cp_eyes';
    let [l, a] = await lit(body); ok(`...in his robes, lit by the world: ${l} of ${a} parts lit (his eyes aside)`, a > 0 && l === 0);
    for (const [gem, el, nm] of [['ethereal_gem', 10, 'an Ethereal Gem: his Ethereal Form'], ['wraithfire_heart', 11, 'a Wraithfire Heart: his Wraithfire Form']]) {
      await run('item replace entity TestRat hotbar.1 with minecraft:air'); await run(`loot replace entity TestRat hotbar.1 loot bm:items/${gem}`); A.slot(1); await sleep(400);
      await run('scoreboard players set TestRat bm.cpck 0'); await clickPet(CS); await sleep(3000); [l, a] = await lit(body);
      ok(`...handed ${nm} - he shines through and through (${l} of ${a}), and still does a couple of seconds on`, (await sc('TestRat', 'bm.cpel')) === el && a > 0 && l === a, `cpel ${await sc('TestRat', 'bm.cpel')}`);
    }
    await run('item replace entity TestRat hotbar.1 with minecraft:air'); await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]'); A.slot(4); await sleep(1700); await run('scoreboard players set TestRat bm.cpck 0');
    await clickPet(CS, true); await sleep(2500); [l, a] = await lit(body);
    ok(`...sneak + right-click empty-handed: back in his robes, lit by the world again (${l} of ${a} lit)`, (await sc('TestRat', 'bm.cpel')) === 0 && a > 0 && l === 0, `cpel ${await sc('TestRat', 'bm.cpel')}`);
    await run(`${O}execute as TestRat at @s run function bm:p98/home/cecil`); await wait(5000, async () => (await cnt('@e[tag=bm.cecilpet]')) === 0);
  }
  // ---- Emma: charged, a monster near - her Ethereal Form
  await run('tag TestRat add bm.emmet');
  if (ok('Emma called with her ribbon', await call('emma_ribbon', 'bm.emmapet'))) {
    await sleep(2000);
    await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] run scoreboard players set @s bm.emc 100`); await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] run scoreboard players set @s bm.eme 0`);
    await run(`${O}summon minecraft:husk ${X + 4.5} ${Y + 1} ${Z + 4.5} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.t288foe"]}`);
    const up = await wait(5000, async () => (await sc('@e[type=minecraft:cat,tag=bm.emmapet,limit=1]', 'bm.eme')) > 0);
    await run(`${O}kill @e[tag=bm.t288foe]`); await sleep(3000);
    const [l, a] = await lit('tag=bm.emp,tag=!bm.emfade');
    ok(`...charged with a monster near, she takes her Ethereal Form - and shines (${l} of ${a} parts lit, three seconds on)`, up && a > 0 && l === a);
    await run(`${O}execute as TestRat at @s run function bm:p98/home/emma`);
  }
  await run(`${O}kill @e[tag=bm.t288foe]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
