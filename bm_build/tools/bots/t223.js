// 2.84a: HARD MODE, as a regular (non-op) player. (The test server keeps it off - #hardoff 1 - since TestRat has beaten the
// Hollow King; this test lets it wake, and puts it back to sleep at the end.)
//   the waking: TestRat (best-ever conquest 6) online - a HARD MODE title, darkness, Blood Moons every 15 days.
//   the night's monsters: a pen of plain zombies rolls again - some Elite/Champion/Dread, most of the rest with Strength and
//     Resistance (a few at II).
//   a Dread zombie (rcon sets it down, NoAI so it stays put): its name, health, tag, its eldritch armour (the Visage helm, the void-plate); in netherite plate the player stands
//     still beside it and takes a Pulse or a Mark straight through the armour; next time the player walks off the moment
//     the ring appears - and it misses.
//   the player kills it (hits from the bot): bm.dkill and the world's count go up; it drops a Champion's Tokens.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)(?!.*\d)/); return m ? +m[1] : NaN; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const cnt = async sel => +(((await run(`execute store result score #t bm.rng if entity ${sel}`)) && (await run('scoreboard players get #t bm.rng'))).match(/has (\d+)/) || [0, 0])[1];
  const hp = async () => num('data get entity TestRat Health');
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const conq0 = await sc('TestRat', 'bm.conqb'), per0 = await sc('#bmper', 'bm.cfg');
  await run('scoreboard players set #hardoff bm.cfg 1'); await run('scoreboard players set #hard bm.cfg 0');
  const A = await bot('TestRat'); await sleep(2500);
  const titles = []; A.on('set_title_text', p => titles.push(JSON.stringify(p)));
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  // ---- the stage: a stone pen, the player in it, daylight and peace for the spawn rolls
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 5} ${Z + 12} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.conqb 6'); await sleep(1000); A.stand();

  // ================================================================== 1. the waking
  titles.length = 0; A.chats.length = 0;
  await run('scoreboard players set #hardoff bm.cfg 0');
  ok('Someone who has beaten the Hollow King is online: hard mode wakes', await wait(4000, async () => (await sc('#hard', 'bm.cfg')) === 1));
  ok('...a HARD MODE title on screen', await wait(3000, async () => titles.some(t => /HARD MODE/.test(t))), titles.slice(-1).join(''));
  ok('...and a moment of darkness', /darkness/.test(await run('data get entity TestRat active_effects')));
  ok('...Blood Moons every 15 days now', (await sc('#bmper', 'bm.cfg')) === 15, `${await sc('#bmper', 'bm.cfg')}`);
  ok('...the word: what has changed (Dread monsters, the Blood Moon every 15 days, Vesper\'s shop)', await wait(6000, async () => A.chats.some(c => /power behind his throne/.test(c)) &&
     A.chats.some(c => /DREAD monsters stalk/.test(c)) && A.chats.some(c => /Blood Moon rises every 15 days/.test(c)) && A.chats.some(c => /Vesper, the Dread Broker, has opened a shop in Night Alley/.test(c))),
     A.chats.slice(-9).join(' | ').slice(0, 400));

  // ================================================================== 2. the night's monsters roll again
  await run(`${O}kill @e[type=minecraft:zombie,distance=..30,x=${X},y=${Y},z=${Z}]`);
  // (a roofed stone box, walled off from the player - the roll skips NoAI mobs, so these are ordinary zombies)
  await run(`${O}fill ${X - 10} ${Y - 1} ${Z + 2} ${X + 10} ${Y + 3} ${Z + 12} minecraft:stone hollow`);
  for (let i = 0; i < 60; i++) await run(`${O}summon minecraft:zombie ${X - 8 + (i % 8) * 2} ${Y} ${Z + 4 + Math.floor(i / 8)} {PersistenceRequired:1b}`);
  await sleep(2500);
  const box = `x=${X - 10},y=${Y - 1},z=${Z + 2},dx=20,dy=4,dz=10`;
  const all = await cnt(`@e[type=minecraft:zombie,${box}]`);
  const tiered = await cnt(`@e[type=minecraft:zombie,${box},tag=bm.tiered]`);
  const buffed = await cnt(`@e[type=minecraft:zombie,${box},tag=!bm.tiered,nbt={active_effects:[{id:"minecraft:resistance"}]}]`);
  const plain = await cnt(`@e[type=minecraft:zombie,${box},tag=!bm.tiered,nbt=!{active_effects:[{id:"minecraft:resistance"}]}]`);
  ok('60 plain zombies: every one rolled (all seen)', all >= 58 && (await cnt(`@e[type=minecraft:zombie,${box},tag=bm.seen]`)) >= all - 1, `${all}`);
  ok('...some came out Elite, Champion or Dread', tiered >= 3, `${tiered} tiered`);
  ok('...most of the rest with Strength and Resistance', buffed > plain, `${buffed} buffed, ${plain} plain`);
  await run(`${O}kill @e[type=minecraft:zombie,${box}]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}fill ${X - 10} ${Y} ${Z + 2} ${X + 10} ${Y + 3} ${Z + 12} minecraft:air`);

  // ================================================================== 3. a Dread zombie
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z - 2.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.t223"]}`);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t223] run function bm:p176/mk/zombie`);
  const D = '@e[type=minecraft:zombie,tag=bm.t223,limit=1]';
  ok('A Dread zombie: named "Dread", tagged, 100 health', /Dread/.test(await run(`data get entity ${D} CustomName`)) && /bm\.dread/.test(await run(`data get entity ${D} Tags`)) &&
     (await num(`attribute ${D} minecraft:max_health get`)) === 100, await run(`data get entity ${D} CustomName`));
  { const eq = await run(`data get entity ${D} equipment`);
    ok('...in its own eldritch armour: the Dread Visage (a 3D helm) and the void-plate (bm:dread) - and never dropped',
       /item_model":\s*"bm:dread_helm"|item_model:\s*"bm:dread_helm"/.test(eq) && (eq.match(/asset_id:\s*"bm:dread"|asset_id":\s*"bm:dread"/g) || []).length === 3 &&
       !/trim/.test(eq) && /drop_chances/.test(await run(`data get entity ${D}`)) , eq.slice(0, 300)); }
  // full netherite on the player - the Dread's gathering goes straight through it
  for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
    await run(`item replace entity TestRat armor.${s} with minecraft:netherite_${p}[enchantments={"minecraft:protection":4}]`);
  await run('effect give TestRat minecraft:instant_health 1 5 true'); await sleep(800);
  const h0 = await hp();
  await run(`scoreboard players set ${D} bm.drcd 1`);
  ok('Beside it, it gathers itself (a ring or a mark appears)', await wait(4000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.drm]')) > 0));
  const isMark = (await cnt('@e[type=minecraft:marker,tag=bm.drmark]')) > 0;
  let h1 = h0; for (let t = 0; t < 14; t++) { h1 = Math.min(h1, await hp()); await sleep(180); }
  ok(`...standing still in netherite: the ${isMark ? 'Mark' : 'Pulse'} lands straight through the armour (${isMark ? 9 : 7} damage)`, h0 - h1 >= (isMark ? 8 : 6), `${h0} -> ${h1}`);
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true'); await sleep(1500);
  // and again - this time the player walks away from it the moment it begins
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(500);
  const h2 = await hp();
  await run(`scoreboard players set ${D} bm.drcd 1`);
  await wait(4000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.drm]')) > 0, 100);
  await A.walkTo(X + 0.5, Z + 7.5, 0.4);
  await sleep(2500);
  const h3 = await hp();
  ok('...walk off the moment it starts: it misses', h3 >= h2 - 0.5 && (await cnt('@e[type=minecraft:marker,tag=bm.drm]')) === 0, `${h2} -> ${h3}`);

  // ================================================================== 4. killed by the player
  const dk0 = (await sc('TestRat', 'bm.dkill')) || 0, w0 = await sc('#dk', 'bm.cfg');
  await run(`data merge entity ${D} {Health:1f}`); await run(`effect clear ${D}`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 0.5} 180 0`); await sleep(800);
  A.slot(0); await sleep(300); await run('item replace entity TestRat weapon.mainhand with minecraft:netherite_sword'); await sleep(400);
  const eidOf = async sel => { const m = (await run(`data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const de = await eidOf(D);
  for (let i = 0; i < 6 && (await cnt('@e[type=minecraft:zombie,tag=bm.t223]')) > 0; i++) { A.attack(de); await sleep(700); }
  ok('The player kills it: it falls', (await cnt('@e[type=minecraft:zombie,tag=bm.t223]')) === 0, `eid ${de}, health ${await run(`data get entity ${D} Health`)}`);
  ok('...counted: bm.dkill +1, the world\'s count +1', (await sc('TestRat', 'bm.dkill')) === dk0 + 1 && (await sc('#dk', 'bm.cfg')) === w0 + 1,
     `${dk0} -> ${await sc('TestRat', 'bm.dkill')}, ${w0} -> ${await sc('#dk', 'bm.cfg')}`);
  // (the player stands right by it, so the drop goes straight into the pack - counted there, and any left on the ground)
  const toks = async () => { const r = await run(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6] if items entity @s contents *[minecraft:custom_data~{bm:"token"}] run data get entity @s Item.count`);
    const m = (await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0')).match(/Found (\d+)/);
    return (r.match(/data: (\d+)/g) || []).reduce((a, x) => a + +x.match(/\d+/)[0], 0) + (m ? +m[1] : 0); };
  ok('...it drops a Champion\'s Tokens (3 or more)', await wait(3000, async () => (await toks()) >= 3), `${await toks()}`);

  // ================================================================== 5. the operator's switch
  await run('function bm:admin/set/hard_0'); await sleep(1500);
  ok('admin/settings Off: hard mode sleeps, and stays asleep with a conqueror online', (await sc('#hard', 'bm.cfg')) === 0 && (await sc('#hardoff', 'bm.cfg')) === 1);

  await run(`scoreboard players set TestRat bm.conqb ${conq0}`); await run(`scoreboard players set #bmper bm.cfg ${per0}`);
  await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
