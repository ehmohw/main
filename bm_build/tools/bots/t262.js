// 2.94: THE 8-BIT SERPENT KING (phase215), as a regular (non-op) player - a conqueror on Apophiss's seal in the Hollow throne room
// with 8-Bit Emma, Leo and Cecil, called with their own cartridges: the seal glitches and he rears up (a husk host, a flat two-sided (2.94c: not billboarded)
// sprite, a boss bar, the title); his blows land on you; brought low (rcon sets his health), the bot's own blows finish him -
// his death plays, he shatters, and the 8-Bit Crown is yours (and the advancement); worn on your head with a right-click.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const run = c => R.run(c); const res = [];
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = 'execute in bm:hollow_throne run ';
  const cnt = async (sel) => { const m = (await run(`${H}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${H}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${H}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); };
  const SEAL = [1084.5, 103, 1083.5];
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('tag TestRat remove bm.pxcrown');
  await run('advancement revoke TestRat only bm:story/px_crown');
  for (const t of ['bm.xmpet', 'bm.xlpet', 'bm.xcpet', 'bm.emmapet', 'bm.leopet', 'bm.cecilpet']) await run(`kill @e[tag=${t}]`);
  await run(`${H}kill @e[type=minecraft:husk,tag=bm.pxapo]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.pxa_spr]`);
  await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`);
  await sleep(2500);                                                     // (2.94c: a killed follower's faint lands a few ticks on - then its cooldown is cleared)
  for (const o of ['bm.xmcd', 'bm.xlcd', 'bm.xccd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true');
  await run('effect give TestRat minecraft:resistance 900 2 true');
  await run(`${H}tp TestRat ${SEAL[0]} ${SEAL[1]} ${SEAL[2]} -90 0`); await sleep(3000); A.stand();
  await run(`${H}scoreboard players set @e[type=minecraft:marker,tag=bm.apseal] bm.apt 0`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/cart_emma'); await run('loot replace entity TestRat hotbar.1 loot bm:items/cart_leo');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/cart_cecil');
  A.chats.length = 0;
  const came = [];
  for (const [k, t] of [[0, 'bm.xmpet'], [1, 'bm.xlpet'], [2, 'bm.xcpet']]) { await use(k); came.push(await wait(3500, async () => (await cnt(`@e[type=minecraft:wolf,tag=${t}]`)) === 1)); await sleep(2200); }
  ok('8-Bit Emma, Leo and Cecil answer their cartridges in the Hollow (one by one)', came.every(Boolean), JSON.stringify(came));
  const BOSS = '@e[type=minecraft:husk,tag=bm.pxapo,limit=1]';
  ok('all three on the seal: it glitches - the 8-Bit Serpent King rears up (host and sprite)', await wait(6000, async () => (await cnt(BOSS)) === 1 &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.pxa_spr]')) === 1) && A.chats.some(c => /glitches/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  ok('...his sprite turned as he is (flat, not billboarded) and plays his frames', /fixed/.test(await nbt('@e[type=minecraft:item_display,tag=bm.pxa_spr,limit=1]', 'billboard')) &&
     await (async () => { await sleep(300); const a = +((await nbt('@e[type=minecraft:item_display,tag=bm.pxa_spr,limit=1]', 'Rotation[0]')).match(/(-?[\d.]+)/) || [0, 999])[1];
       const b = +((await nbt('@e[type=minecraft:husk,tag=bm.pxapo,limit=1]', 'Rotation[0]')).match(/(-?[\d.]+)/) || [0, -999])[1]; return Math.abs(((a - b) % 360 + 540) % 360 - 180) < 30; })() &&
     /strings/.test(await nbt('@e[type=minecraft:item_display,tag=bm.pxa_spr,limit=1]', 'item.components')));
  ok('...and a boss bar shows him to you', /TestRat/.test(await run('bossbar get bm:pxapo players')), await run('bossbar get bm:pxapo players'));
  const php = async () => +(((await nbt('@a[name=TestRat,limit=1]', 'Health')).match(/([\d.]+)/) || [0, 0])[1]);
  await run('effect give TestRat minecraft:instant_health 1 20 true'); await sleep(800);
  const seen = new Set();
  ok('his blows land on you (bite, black fire, tail slam)', await wait(30000, async () => { seen.add(await run(`${H}scoreboard players get ${BOSS} bm.pxas`)); return (await php()) < 195; }, 400),
     `health ${await php()}; states ${[...seen].map(x => (x.match(/has (\d+)/) || [0, '?'])[1]).join(',')}`);
  await run('effect give TestRat minecraft:instant_health 1 20 true');
  // (brought low for the test: his last few hits are the bot's own)
  await run(`${H}data modify entity ${BOSS} Health set value 8f`);
  await run('loot replace entity TestRat hotbar.4 loot minecraft:netherite_sword'); A.slot(4); await sleep(300);
  for (let i = 0; i < 20 && (await cnt(BOSS)); i++) {
    const p = (await nbt(BOSS, 'Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (p) await run(`${H}tp TestRat ${+p[1] + 1.5} ${+p[2]} ${p[3]} 90 10`);
    const e = await entOf(BOSS); if (e) A.attack(e.entityId); await sleep(700);
  }
  ok('the bot\'s own blows finish him', (await cnt(BOSS)) === 0);
  ok('...his death plays (the sprite stays a moment, dying)', await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.pxa_dying]')) === 1));
  ok('...he shatters, and the 8-Bit Crown is yours (and the advancement)', await wait(8000, async () => (await has('px_crown')) === 1) &&
     (await cnt('@a[name=TestRat,advancements={bm:story/px_crown=true}]')) === 1);
  await run('clear TestRat minecraft:netherite_sword'); await run('clear TestRat *[minecraft:custom_data~{bm:"px_crown"}]');
  await run('loot replace entity TestRat hotbar.5 loot bm:items/px_crown'); await use(5); await sleep(600);
  ok('the crown right-clicked: worn on your head', /px_crown/.test(await nbt('@a[name=TestRat,limit=1]', 'equipment.head')));
  ok('...and with an 8-bit follower out: Luck', await wait(3000, async () => /luck/.test(await nbt('@a[name=TestRat,limit=1]', 'active_effects'))));
  for (const t of ['bm.xmpet', 'bm.xlpet', 'bm.xcpet']) await run(`kill @e[tag=${t}]`);
  await run('attribute TestRat minecraft:max_health base set 20'); await run('clear TestRat'); await run('effect clear TestRat');
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
