// 2.82c: KING OMEGA'S TITHE, THE BLOOD MOON'S BOSSES THAT VANISHED, THE TAILOR'S NAMES, THE PALACE DOOR, THE FENCE'S BACK ROOM -
// as a regular (non-op) player TestRat, every step a real packet (rcon sets the stage: blood mobs and a Blood Moon, where a boss
// rises, which followers TestRat has met; the Tailor's counter is "clicked" for the bot - what a right-click opens).
//   THE TAILOR: met only Cecil - his main page lists Cecil (and the display cases, the auras), no follower TestRat hasn't met;
//   the auras page shows Cecil's aura only; a page code for an unmet follower (Emma's) sends you back to the main page.
//   THE TITHE: King Omega called with his Monocle (a real use). A Blood Moon zombie killed with Omega out drops three times its
//   currency - every kill at least 6 Tokens and 3 Blood Crystals (alone, 2-4 and 1-3); sent home, a kill pays as before.
//   A regular mob killed with Omega out: 1 in 100 drops a Token, a Blood Crystal, a Lucky Token or a Green Xenite (400 kills:
//   a handful); without him, never.
//   THE BLOOD MOON'S BOSSES: an Arachno-Lantern and a Monstrosity rising from a monster's spawn 120 blocks from TestRat are still
//   there five seconds on (the far-despawn took anything past 100 at once); with nobody within 160, they go.
//   THE PALACE DOOR: a palace built here - its arch is cut to the doors (2 wide, 2 high, a lintel); an old palace's 4 x 4 arch is
//   filled in once it's loaded.
//   THE FENCE: his Associate shelf sells 2 Ominous Trial Keys now (the Banker's Card is over his counter).
const fs = require('fs');
const { bot, rcon, sleep } = require('./lib_resp');
const OUT = (process.env.BM_OUT || __dirname + '/../../out_p2') + '/BlackMarket_DP/data/bm/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const ecnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const cnt = async (id) => { const o = await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const X = 27000, Y = 100, Z = 27000;
  const ground = async (id) => {        // (how many of a currency lie on the ground here, every stack counted)
    const near = `x=${X},y=${Y},z=${Z},distance=..10`;
    await run(`${O}execute as @e[type=minecraft:item,${near}] if items entity @s contents *[minecraft:custom_data~{bm:"${id}"}] run tag @s add t206c`);
    await run(`${O}execute as @e[type=minecraft:item,tag=t206c] store result score @s bm.rng run data get entity @s Item.count`);
    await run('scoreboard players set #t206 bm.rng 0'); await run(`${O}scoreboard players operation #t206 bm.rng += @e[type=minecraft:item,tag=t206c] bm.rng`);
    await run(`${O}tag @e[type=minecraft:item,tag=t206c] remove t206c`);
    return +((await run('scoreboard players get #t206 bm.rng')).match(/has (-?\d+)/) || [0, 0])[1]; };
  const labels = () => A.buttons().map(b => b.label).join(' | ').slice(0, 400);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 16} ${Y - 1} ${Z - 16} ${X + 16} ${Y - 1} ${Z + 16} minecraft:stone`);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y + 8} ${Z + 16} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');

  // ---- the Tailor: only who you've met
  const MET = ['emma', 'leo', 'omega', 'pistachio', 'fishy', 'apo', 'tul', 'demo', 'killerwatt', 'celi', 'zib', 'escort', 'frog', 'donado', 'dennis', 'pearl', 'wil', 'cecil'];
  const had = {};
  for (const k of MET) { had[k] = await passes(`execute if entity @a[name=TestRat,advancements={bm:met/${k}=true}]`); await run(`advancement revoke TestRat only bm:met/${k}`); }
  await run('advancement grant TestRat only bm:met/cecil');
  const UNMET = /Emma|Leo|King Omega|Pistachio|Fishy|Apophiss|Tullius|Democratus|KillerWatt|Celi|Zib|Frog|Donado|Dennis|Pearlman|Wilfrey/;
  let n0 = A.dialogN.length; await run('execute as TestRat at @s run function bm:p103/tl/main'); await wait(3000, async () => A.dialogN.length > n0);
  const main = A.buttons().map(b => b.label);
  ok('the Tailor, met only Cecil: Cecil, the display cases and the auras - and no follower TestRat hasn\'t met',
     main.some(l => /^Cecil/.test(l)) && main.some(l => /Display cases/.test(l)) && main.some(l => /Auras/.test(l)) && !main.some(l => UNMET.test(l)), labels());
  const au = await A.press(/Auras/); await sleep(400);
  const al = A.buttons().map(b => b.label);
  ok('...his auras page: Cecil\'s aura (with its price), nobody else\'s', !!au && al.some(l => /Cecil/.test(l) && /coins|OWNED/.test(l)) && !al.some(l => UNMET.test(l)), labels());
  await A.press(/The Tailor/); await sleep(400);
  const cec = await A.press(/^Cecil/); await sleep(400);
  ok('...and Cecil\'s own page opens from the button', !!cec && A.buttons().some(b => /« The Tailor/.test(b.label)), labels());
  await A.press(/The Tailor/); await sleep(400);
  n0 = A.dialogN.length; A.cmd('trigger bm.act set 7741'); await wait(2500, async () => A.dialogN.length > n0);     // (Emma's page, by its code)
  ok('...a page code for someone unmet (Emma\'s) only brings back the main page', A.buttons().some(b => /Display cases/.test(b.label)) && !A.buttons().some(b => /Emma/.test(b.label)), labels());
  A.cmd('trigger bm.act set 2'); await sleep(300);

  // ---- King Omega, called with his Monocle
  await run('scoreboard players set TestRat bm.omcd 0');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/om_monocle'); A.slot(0); await sleep(300);
  A.use(); await sleep(400); A.release();
  const OM = '@e[type=minecraft:wolf,tag=bm.ompet,limit=1]';
  ok('King Omega, called with his Monocle', await wait(5000, async () => (await ecnt(OM)) === 1));
  ok('...and with him out, TestRat carries his tithe (bm.omact)', await wait(3000, async () => passes('execute if entity @a[name=TestRat,tag=bm.omact]')));

  // ---- a Blood Moon zombie, killed by TestRat's own blow
  const ZS = '@e[type=minecraft:zombie,tag=t206z,limit=1]';
  const killBlood = async () => {
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
    for (const c of ['token', 'blood_crystal', 'medallion']) await run(`clear TestRat *[minecraft:custom_data~{bm:"${c}"}]`);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 3.2} {Tags:["t206z","bm.seen"],NoAI:1b}`);
    await run(`${O}execute as ${ZS} at @s run function bm:mobs/blood/zombie`);
    await run(`${O}data merge entity ${ZS} {Health:1f,NoAI:1b}`);
    let e = null; await wait(3000, async () => !!(e = await entOf(ZS)), 200); if (!e) return 'not seen';
    await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
    await run('item replace entity TestRat hotbar.1 with minecraft:iron_sword'); A.slot(1); await sleep(900);   // (a sword, the swing recharged: a fist does next to nothing)
    for (let i = 0; i < 12 && (await ecnt(ZS)) > 0; i++) { A.attack(e.entityId); await sleep(750); }      // (swing till it drops, the blade recharged each time)
    if (!(await wait(2000, async () => (await ecnt(ZS)) === 0))) return 'not killed';
    await sleep(800);                                                                // (its drops on the ground, out of TestRat's reach)
    return { tok: await ground('token'), cry: await ground('blood_crystal') };
  };
  const withO = []; for (let i = 0; i < 4; i++) withO.push(await killBlood());
  ok('with Omega out: every Blood Moon kill pays three times - at least 6 Tokens and 3 Blood Crystals each',
     withO.every(r => r && r.tok !== undefined && r.tok >= 6 && r.cry >= 3 && r.tok <= 12 && r.cry <= 9), JSON.stringify(withO));

  // ---- a regular mob: 1 in 100
  const TITHE = ['token', 'blood_crystal', 'lucky_token', 'xenite_green'];
  const regular = async (n) => {
    for (const c of TITHE) await run(`clear TestRat *[minecraft:custom_data~{bm:"${c}"}]`);
    A.bars.length = 0;
    let got = 0;
    for (let i = 0; i < n; i++) {
      await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 1.5} {Tags:["t206r","bm.seen"],NoAI:1b,Silent:1b,DeathLootTable:"minecraft:empty"}`);
      await run(`${O}damage @e[type=minecraft:zombie,tag=t206r,limit=1] 100 minecraft:player_attack by TestRat`);    // (staging: the blow is TestRat's)
      if (i % 50 === 49) { await sleep(1200); for (const c of TITHE) got += await cnt(c); for (const c of TITHE) await run(`clear TestRat *[minecraft:custom_data~{bm:"${c}"}]`); }
    }
    await sleep(1200); for (const c of TITHE) got += await cnt(c);
    return got;
  };
  const r1 = await regular(400);
  ok('with Omega out: 400 regular zombies killed - a handful paid his tithe (a Token, a Blood Crystal, a Lucky Token or Green Xenite)',
     r1 >= 1 && r1 <= 16 && A.bars.some(b => /tithe/i.test(JSON.stringify(b))), `${r1} tithes`);

  // ---- sent home: as before
  await run(`${O}kill ${OM}`);
  ok('...Omega gone, the tithe is gone with him', await wait(3000, async () => !(await passes('execute if entity @a[name=TestRat,tag=bm.omact]'))));
  const without = []; for (let i = 0; i < 3; i++) without.push(await killBlood());
  ok('without him: a Blood Moon kill pays as before (2-4 Tokens, 1-3 Blood Crystals)', without.every(r => r && r.tok !== undefined && r.tok >= 2 && r.tok <= 4 && r.cry >= 1 && r.cry <= 3), JSON.stringify(without));
  const r0 = await regular(200);
  ok('...and 200 regular zombies pay no tithe at all', r0 === 0, `${r0}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat');

  // ---- the Blood Moon's bosses, risen 120 blocks off
  const BX = X + 120;
  await run(`${O}forceload add ${BX - 16} ${Z - 16} ${BX + 16} ${Z + 16}`);
  await run(`${O}fill ${BX - 12} ${Y - 1} ${Z - 12} ${BX + 12} ${Y - 1} ${Z + 12} minecraft:grass_block`);
  for (let y = Y; y < Y + 40; y += 8) await run(`${O}fill ${BX - 12} ${y} ${Z - 12} ${BX + 12} ${y + 7} ${Z + 12} minecraft:air`);
  await run('function bm:admin/blood_moon');
  await wait(15000, async () => /has 1/.test(await run('scoreboard players get #active bm.bm')), 500);
  const LAN = '@e[type=minecraft:giant,tag=bm.salboss]', MON = '@e[type=minecraft:ravager,tag=bm.monstrosity]';
  await run(`${O}execute as ${LAN} at @s run function bm:p82/leave`); await run(`${O}tp ${MON} ~ -400 ~`); await run(`${O}kill ${MON}`);
  await run(`${O}summon minecraft:zombie ${BX + 0.5} ${Y} ${Z + 0.5} {Tags:["t206l","bm.seen"]}`);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=t206l,limit=1] at @s run function bm:p82/spawn`);
  await run(`${O}summon minecraft:zombie ${BX + 6.5} ${Y} ${Z + 6.5} {Tags:["t206m","bm.seen"]}`);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=t206m,limit=1] at @s run function bm:monst/spawn`);
  await sleep(5000);
  ok('an Arachno-Lantern risen from a spawn 120 blocks off is still there five seconds on (it "died" on the spot)', (await ecnt(LAN)) === 1);
  ok('...and so is a Monstrosity (none ever lived to be seen)', (await ecnt(MON)) === 1);
  await run(`${O}tp TestRat ${X - 60.5} ${Y} ${Z + 0.5}`);                         // (now nobody's within 160)
  ok('...with nobody within 160 blocks, they go', await wait(4000, async () => (await ecnt(LAN)) === 0 && (await ecnt(MON)) === 0));
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`);
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day');
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.salp]`);

  // ---- the palace door
  const PX = X - 200;
  await run(`${O}forceload add ${PX - 56} ${Z - 48} ${PX + 40} ${Z + 48}`); await sleep(3000);
  await run(`${O}fill ${PX - 47} ${Y - 1} ${Z - 2} ${PX - 43} ${Y - 1} ${Z + 2} minecraft:stone`);
  await run(`${O}tp TestRat ${PX - 44.5} ${Y} ${Z + 0.5}`); await sleep(1500);      // (a palace rises only with someone within 112)
  await run(`${O}kill @e[type=minecraft:marker,tag=bm.ompal,x=${PX - 40},y=0,z=${Z - 48},dx=80,dy=320,dz=96]`);
  await run(`${O}execute positioned ${PX} ${Y} ${Z} run function bm:admin/omega_palace`);
  const PM = `@e[type=minecraft:marker,tag=bm.ompal,x=${PX - 40},y=0,z=${Z - 48},dx=80,dy=320,dz=96,limit=1]`;
  ok('a palace built here', await wait(15000, async () => (await ecnt(PM)) === 1, 500));
  const pos = (await run(`${O}data get entity ${PM} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [mx, my, mz] = pos ? [+pos[1], +pos[2], +pos[3]] : [0, 0, 0];
  const TY = 12, CX = 32.5, CY = 6, CZ = 28.5;                                       // (palace.py: TY, CENTER)
  const P = (x, y, z) => `${Math.floor(mx + x - CX + 0.5)} ${Math.round(my + y - CY)} ${Math.floor(mz + z - CZ + 0.5)}`;
  const blk = async (x, y, z, b) => passes(`${O}execute if block ${P(x, y, z)} ${b}`);
  const fitted = async () => (await blk(32, TY + 1, 44, 'minecraft:spruce_door')) && (await blk(33, TY + 2, 44, 'minecraft:spruce_door')) &&
    (await blk(31, TY + 1, 44, 'minecraft:spruce_planks')) && (await blk(34, TY + 2, 44, 'minecraft:spruce_planks')) &&
    (await blk(32, TY + 3, 44, 'minecraft:stripped_spruce_log')) && !(await blk(31, TY + 1, 45, 'minecraft:air')) && !(await blk(32, TY + 3, 45, 'minecraft:air')) &&
    (await blk(32, TY + 1, 45, 'minecraft:air'));
  ok('...its great door fits its arch: two wide, two high, a lintel over it (the arch was 4 x 4 round the doors)', await fitted());
  for (const z of [44, 45]) for (const x of [31, 34]) await run(`${O}fill ${P(x, TY + 1, z)} ${P(x, TY + 4, z)} minecraft:air`);    // (the stage: an old palace's arch)
  await run(`${O}fill ${P(32, TY + 3, 44)} ${P(33, TY + 4, 45)} minecraft:air`); await run(`${O}tag ${PM} remove bm.omdoor2`);
  ok('...an old palace\'s 4 x 4 arch is filled in round its doors once it\'s loaded', await wait(4000, async () => fitted()));

  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`);

  // ---- the Fence's back room
  const dlg = JSON.stringify(JSON.parse(fs.readFileSync(OUT + 'dialog/p28/back_fence_2.json', 'utf8')));
  ok('the Fence\'s Associate shelf: 2 Ominous Trial Keys (the Banker\'s Card is over his counter now)', /2 Ominous Trial Keys/.test(dlg) && !/Banker/.test(dlg));

  // ---- clean up
  for (const k of MET) await run(`advancement ${had[k] ? 'grant' : 'revoke'} TestRat only bm:met/${k}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`);
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
