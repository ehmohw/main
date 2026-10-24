// 2.93: CHAMPIONS OF THE TIDE - as a regular (non-op) player: Queen Ava and Leo called with their own things, Leo one rank
// short (rcon sets the rank); his page at the Tide Font asks his last tribute and an Elemental Gem; Honour III (Might V) bought with the
// dialog's own button - Leo is a Champion (the title, the advancement, the Champion's Ribbon, his new blow named); on his host the
// champion's toughness; his medal and regalia on his own bones, keeping to them as he follows; his aura; KNIGHT'S OATH on a
// monster near him, then its rest; four Blood Moon blows and three Dread pulses, and he stands; the Ribbon (used): medal,
// regalia and aura each switched off and on; sent home and called again - what was off stays off.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const tagged = async (t) => (await run('tag TestRat list')).includes(t);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const click = async (sel, sneak = false) => { await wait(3000, async () => !!(await entOf(sel))); const e = await entOf(sel); if (!e) return false;
    if (sneak) { A.input({ shift: true }); await sleep(800); } A.interact(e.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true; };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(400); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(200); } await sleep(300); };
  const give = async (slot, iid, n = 1) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); if (n > 1) await run(`item modify entity TestRat hotbar.${slot} {type:"minecraft:set_count",count:${n}}`); await sleep(300); };
  const said = (re) => A.chats.some(c => re.test(c)) || A.bars.some(c => re.test(c)) || A.titles.some(c => re.test(c));
  const screen = () => A.dialogN.length ? JSON.stringify(A.dialogN[A.dialogN.length - 1]) : '';
  const CD = { emma: 'bm.emcd', ava: 'bm.avcd', pearlq: 'bm.pqcd', bones: 'bm.bjcd', apo: 'bm.apcd', leo: 'bm.lecd' };
  const home = async (w) => { await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');   // (whose followers)
    await run(`execute as TestRat run function bm:p98/home/${w}`).catch(() => {}); await sleep(600); await run(`scoreboard players reset TestRat ${CD[w]}`); };
  const X = 26000, Y = 31, Z = 26000;
  const CORE = `@e[type=minecraft:marker,tag=bm.kingdom,x=${X},y=${Y},z=${Z},distance=..60,limit=1]`;
  const BOX = (t) => `@e[type=minecraft:interaction,tag=${t},x=${X},y=${Y},z=${Z},distance=..70,limit=1]`;
  const cx = X + 0.5, cy = Y + 4, cz = Z + 6.5;
  const pet = (tag) => `@e[tag=${tag},tag=!bm.ffpet,x=${X},y=${Y},z=${Z},distance=..60,limit=1]`;


  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1500 4 true'); await run('effect give TestRat minecraft:saturation 1500 0 true');
  for (const t of ['bm.chmp_leo', 'bm.chrib', 'bm.nomd_leo', 'bm.norg_leo', 'bm.noau_leo']) await run(`tag TestRat remove ${t}`);
  for (const o of ['bm.hn_leo', 'bm.hn_ava', 'bm.fret']) await run(`scoreboard players reset TestRat ${o}`);
  await run('advancement revoke TestRat only bm:story/champion_tide');
  await run('scoreboard players set #hard bm.cfg 1');
  for (const w of ['ava', 'leo']) await home(w);
  await run(`${O}tp TestRat ${X + 200} 120 ${Z}`); await sleep(1500);
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..90]`);
  for (let z = Z - 46; z <= Z + 46; z += 8) {
    await run(`${O}fill ${X - 46} ${Y - 5} ${z} ${X + 46} ${Y - 1} ${Math.min(z + 7, Z + 46)} minecraft:sand`);
    await run(`${O}fill ${X - 46} ${Y} ${z} ${X + 46} ${Y + 31} ${Math.min(z + 7, Z + 46)} minecraft:water`);
  }
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/kingdom`); await sleep(2500);
  await run(`scoreboard players set ${CORE} bm.kbr -1`);

  // ---- Queen Ava and Leo at the Font; Leo one rank short of every honour's height
  await at(cx, cy, cz + 1, 0, 10);
  await give(0, 'av_locket'); await give(1, 'leo_crest'); await sleep(1000);
  await use(0); await sleep(2500); await use(1); await sleep(2500);
  ok('Queen Ava and Leo called with their own things', (await cnt(pet('bm.avpet'))) === 1 && (await cnt(pet('bm.leopet'))) === 1);
  await run('scoreboard players set TestRat bm.hn_leo 1444');
  await give(5, 'royal_pearl', 28); await give(6, 'dread_token', 3); await give(7, 'gem_fire');
  await run('item replace entity TestRat hotbar.8 with minecraft:heart_of_the_sea 1');
  A.chats.length = 0; A.titles.length = 0; A.dialogN.length = 0; await click(BOX('bm.kfont')); await sleep(1200);
  await A.press(/Leo/);
  ok("Leo's page: Honour +1 (2.94: the last of three ranks) asks his last tribute (a Heart of the Sea) and an Elemental Gem", /heart of the sea/i.test(screen()) && /Elemental Gem/.test(screen()), screen().slice(0, 400));
  await A.press(/Honour \+1/); await sleep(1500);
  ok('Honour III bought (Might V with it): Leo is a CHAMPION OF THE TIDE (the title), the advancement, the Champion\'s Ribbon', (await score('bm.hn_leo')) === 1555 && said(/Champion of the Tide/) &&
     /true|done/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/champion_tide=true}]').then(r => /passed|count: 1/i.test(r) ? 'true' : 'no')) &&
     (await has('champion_ribbon')) === 1, `hn ${await score('bm.hn_leo')} | ${A.titles.join(' | ')}`);
  ok("...his new blow named: Knight's Oath", said(/Knight's Oath/));
  const LEO = pet('bm.leopet');
  ok("...on Leo (within a second): the champion's toughness (+4) and +20 health", await wait(4000, async () =>
     / 4(\.0)?\b/.test(await run(`${O}attribute ${LEO} minecraft:armor_toughness modifier value get bm:champion`)) &&
     / 20(\.0)?\b/.test(await run(`${O}attribute ${LEO} minecraft:max_health modifier value get bm:champion`))));
  const P = (part) => `@e[type=minecraft:item_display,tag=bm.chp_leo,tag=bm.chq_${part},x=${X},y=${Y},z=${Z},distance=..60]`;
  ok('...his medal on his chest, his regalia on his own bones: pauldrons and a cape, and (2.93b) a crystal on his helm - no crown over it', await wait(4000, async () =>
     (await cnt(P('medal'))) === 1 && (await cnt(P('body'))) === 1 && (await cnt(P('head'))) === 1),
     `medal ${await cnt(P('medal'))} body ${await cnt(P('body'))} head ${await cnt(P('head'))} | ${await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.chp_leo,tag=bm.chq_head,limit=1] item.components`)}`);
  await sleep(1500);
  const onBone = async (part, bone) => /passed|count: 1/i.test(await run(`${O}execute as ${P(part)} at @s if entity @e[type=minecraft:item_display,tag=${bone},distance=..0.2]`));
  ok('...each piece rides its bone: the medal and the mantle on his body', await onBone('medal', 'bm.lp_body') && await onBone('body', 'bm.lp_body'));
  // they keep up as he walks: take him a few blocks off and look again
  await at(cx + 6, cy, cz + 1, 0, 10); await sleep(3500);
  ok('...and keep to them as he follows you', await onBone('body', 'bm.lp_body') && await onBone('medal', 'bm.lp_body'));
  ok('...his aura', /bm\.chau/.test(await run(`${O}data get entity ${LEO} Tags`)));
  // the blow: a monster near him
  await run(`${O}execute at TestRat run summon minecraft:zombie ~2 ~ ~ {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t253z"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  const Z0 = `@e[type=minecraft:zombie,tag=bm.t253z,limit=1]`;
  await run(`${O}tp ${LEO} TestRat`);                          // (staging: he climbs about the castle - bring him beside you)
  A.bars.length = 0;
  const cds = [];
  const fired = await wait(17000, async () => { const c = await score('bm.chcd', LEO); cds.push(c); return c >= 14 && said(/Knight's Oath/); });   // (it may be resting from a raider)
  const zh = +((await run(`${O}data get entity ${Z0} Health`)).match(/(-?[\d.]+)f/) || [0, 300])[1];
  ok("KNIGHT'S OATH: a monster near him - it's struck (10, Might V: 17.5), you're named in the oath", fired && zh <= 290, `zombie ${zh} leo@ ${(await run(`${O}data get entity ${LEO} Pos`)).slice(-60)} z@ ${(await run(`${O}data get entity ${Z0} Pos`)).slice(-60)} me@ ${(await run(`data get entity TestRat Pos`)).slice(-60)} hostile ${await run(`${O}execute as ${LEO} at @s if entity @e[type=minecraft:zombie,distance=..6]`)} near ${await run(`${O}execute as ${LEO} at @s if entity @e[type=#bm:hostile,distance=..6]`)} sec ${await run(`${O}execute as ${LEO} at @s run function bm:p205/sec/leo`)} cd2 ${await score('bm.chcd', LEO)} cd ${[...new Set(cds)].join(',')} bars ${A.bars.slice(-3).join(' / ')} tags ${await run(`${O}data get entity ${LEO} Tags`)}`);
  ok('...then it rests (15 s)', fired);
  await run(`${O}kill ${Z0}`);
  // tough enough: Blood Moon blows and Dread blows (Pulse and Mark go through armour)
  for (let i = 0; i < 4; i++) { await run(`${O}damage ${LEO} 13 minecraft:mob_attack`); await sleep(600); }
  for (let i = 0; i < 3; i++) { await run(`${O}damage ${LEO} 9 minecraft:magic`); await sleep(600); }
  const hp = +((await run(`${O}data get entity ${LEO} Health`)).match(/(-?[\d.]+)f/) || [0, 0])[1];
  ok('a Champion takes four Blood Moon blows (13 each) and three Dread pulses (9, through armour) - and still stands', (await cnt(LEO)) === 1 && hp > 0, `health ${hp}`);
  await run(`${O}data modify entity ${LEO} Health set value 1024f`);

  // ---- the Champion's Ribbon: medal, regalia, aura - each on or off
  await give(3, 'champion_ribbon');                // (his crest stays in your pockets: put it away and he goes home)
  A.dialogN.length = 0; await use(3); await sleep(1000);
  ok("THE CHAMPION'S RIBBON (used): Leo, his medal, regalia and aura - all ON", /CHAMPION'S RIBBON/.test(screen()) && /Leo/.test(screen()) && (screen().match(/ON/g) || []).length >= 3, screen().slice(0, 400));
  await A.press(/Medal/); await sleep(1200);
  ok('...Medal OFF: gone from his chest at once (the regalia stays)', (await cnt(P('medal'))) === 0 && (await cnt(P('body'))) === 1 && await tagged('bm.nomd_leo') && /OFF/.test(screen()),
     `medal ${await cnt(P('medal'))} head ${await cnt(P('head'))} tag ${await tagged('bm.nomd_leo')} | ${A.buttons().map(b => b.label).join(', ')}`);
  await A.press(/Regalia/); await sleep(1200);
  ok('...Regalia OFF: the pauldrons, cape and the helm crystal gone', (await cnt(P('body'))) === 0 && (await cnt(P('head'))) === 0);
  await A.press(/Aura/);
  ok('...Aura OFF', await wait(3000, async () => !/bm\.chau/.test(await run(`${O}data get entity ${LEO} Tags`))));
  await A.press(/Medal/);
  ok('...Medal ON again: back on his chest within a second', await wait(3000, async () => (await cnt(P('medal'))) === 1) && (await cnt(P('body'))) === 0);
  // across a recall: what's off stays off
  await home('leo');
  ok('Leo sent home: his pieces go with him', await wait(3000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.chp_leo]`)) === 0));
  await give(1, 'leo_crest'); await use(1); await sleep(3500);
  ok('...called again: the medal back on him, the regalia still off (as you left it)', await wait(4000, async () => (await cnt(P('medal'))) === 1) && (await cnt(P('body'))) === 0);
  for (const nm of ['Regalia', 'Aura']) { A.dialogN.length = 0; await use(3); await sleep(800); await A.press(new RegExp(nm)); await sleep(800); }
  ok('...regalia and aura on again', await wait(4000, async () => (await cnt(P('body'))) === 1 && (await cnt(P('head'))) === 1));

  for (const w of ['ava', 'leo']) await home(w);
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.chp]`);
  for (const t of ['bm.chmp_leo', 'bm.chrib', 'bm.nomd_leo', 'bm.norg_leo', 'bm.noau_leo']) await run(`tag TestRat remove ${t}`);
  await run('scoreboard players reset TestRat bm.hn_leo'); await run('scoreboard players reset TestRat bm.hn_ava');
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
