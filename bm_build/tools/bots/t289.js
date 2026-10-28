// 2.95c: THE PIERCING BLOW, as a regular (non-op) player - a Champion of the Tide (rcon: the honours' score at rank III, as the Font
// leaves it) called with their own item, beside a still zombie in full diamond (armour 20, toughness 8; 200 health). Within a few
// seconds the Champion vanishes - every part of their model gone - comes back at the zombie, and lands one blow of REND straight
// through the armour: 14 x Might V = 24.5 off its health, armour or no armour. Then they're whole again, free to move.
// King Omega (Ghastly Lunge: out of the ground), Cecil (Shadow Veil), Emma (a cat), KillerWatt, the Frog (no "by" tag of his own).
// (2.95e) not everyone vanishes: Emma (Axe Roll - up in a somersault, the axe slammed down), Bender (Savage Maul - claws, then up on its head, chomping) and Leo (Shield Bash - stunned, then
// the trident three times) go in where you can see them, every part of them in sight, the same 24.5 split over several blows.
// ALL=1: every follower, the same way (Wilfrey's conquests staged by rcon); Bloo, Bones, Democratus, the Chef and Tullius assault too.
// (the Champion's other blow is held off for the test - rcon - so every drop in health is told apart)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (c) => { const o = await run(c); const m = o.match(/has (-?\d+) \[/) || o.match(/(-?[\d.]+)[fd]?$/); return m ? +m[1] : NaN; };
  const X = 18300, Y = 100, Z = 16560;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  const K = [['omega', 'King Omega', 'om_monocle', 'wolf', 'bm.ompet', 'bm.omcd', 'omega'], ['cecil', 'Cecil', 'cecil_gem', 'wolf', 'bm.cecilpet', 'bm.cpcd', 'cecil'],
             ['emma', 'Emma', 'emma_ribbon', 'cat', 'bm.emmapet', 'bm.emcd', 'emma'], ['kw', 'KillerWatt', 'kw_spark', 'wolf', 'bm.kxpet', 'bm.kxcd', 'killerwatt'],
             ['frog', 'the Frog', 'frog_signet', 'wolf', 'bm.frogpet', 'bm.fgcd', 'frog'],
             ['bender', 'Bender', 'bv_ball', 'wolf', 'bm.bvpet', 'bm.bvcd', 'bender'], ['leo', 'Leo', 'leo_crest', 'wolf', 'bm.leopet', 'bm.lecd', 'leo']];
  const ASSAULT = ['emma', 'rufus', 'henry', 'nia', 'bender', 'leo', 'bloo', 'bones', 'demo', 'chef', 'tul'];
  if (process.env.ALL) K.push(
    ['celi', 'celi', 'celi_charm', 'wolf', 'bm.celipet', 'bm.cecd', 'celi'],
    ['zib', 'zib', 'donadian_medal', 'wolf', 'bm.zibpet', 'bm.zbcd', 'zib'],
    ['demo', 'demo', 'demo_seal', 'wolf', 'bm.dmpet', 'bm.dmcd', 'demo'],
    ['apo', 'apo', 'apo_oath', 'wolf', 'bm.appet', 'bm.apcd', 'apo'],
    ['tul', 'tul', 'tul_coin', 'wolf', 'bm.tupet', 'bm.tucd', 'tul'],
    ['don', 'don', 'donado_tag', 'wolf', 'bm.donado', 'bm.dncd', 'donado'],
    ['wil', 'wil', 'wilfrey_locket', 'wolf', 'bm.wilfrey', 'bm.wlcd', null],
    ['fishy', 'fishy', 'fy_bowl', 'wolf', 'bm.fypet', 'bm.fycd', 'fishy'],
    ['dennis', 'dennis', 'dw_horn', 'wolf', 'bm.dwpet', 'bm.dwcd', 'dennis'],
    ['pistachio', 'pistachio', 'pi_cloche', 'wolf', 'bm.pipet', 'bm.picd', 'pistachio'],
    ['ashur', 'ashur', 'ashur_cinder', 'wolf', 'bm.aspet', 'bm.ascd', 'ashur'],
    ['chef', 'chef', 'chef_ladle', 'wolf', 'bm.kkpet', 'bm.kkcd', 'chef'],
    ['neighbor', 'neighbor', 'neighbor_baton', 'wolf', 'bm.nbpet', 'bm.nbcd', 'neighbor'],
    ['ava', 'ava', 'av_locket', 'wolf', 'bm.avpet', 'bm.avcd', 'ava'],
    ['pearlq', 'pearlq', 'pq_pearls', 'wolf', 'bm.pqpet', 'bm.pqcd', 'pearlq'],
    ['bloo', 'bloo', 'bo_claw', 'wolf', 'bm.bopet', 'bm.bocd', 'bloo'],
    ['stalker', 'stalker', 'st_hook', 'wolf', 'bm.svpet', 'bm.svcd', 'stalker'],
    ['lantern', 'lantern', 'ln_gourd', 'wolf', 'bm.lnpet', 'bm.lncd', 'lantern'],
    ['bones', 'bones', 'bn_whistle', 'wolf', 'bm.bjpet', 'bm.bjcd', 'bones'],
    ['capshun', 'capshun', 'capshun_pencil', 'wolf', 'bm.mzpet', 'bm.mzcd', 'capshun'],
    ['pxcecil', 'pxcecil', 'cart_cecil', 'wolf', 'bm.xcpet', 'bm.xccd', 'pxcecil'],
    ['pxleo', 'pxleo', 'cart_leo', 'wolf', 'bm.xlpet', 'bm.xlcd', 'pxleo'],
    ['pxemma', 'pxemma', 'cart_emma', 'wolf', 'bm.xmpet', 'bm.xmcd', 'pxemma'],
    ['sky', 'sky', 'sky_mobile', 'wolf', 'bm.ybpet', 'bm.ybcd', 'sky'],
    ['kettle', 'Kettle', 'kettle_plane', 'wolf', 'bm.ktpet', 'bm.ktcd', 'kettle'],
    ['rufus', 'Rufus Gnaw', 'merc_contract', 'wolf', 'bm.rupet', 'bm.rucd', 'rufus'],
    ['henry', 'Henry', 'henry_tag', 'wolf', 'bm.hypet', 'bm.hycd', 'henry'],
    ['nia', 'Nia', 'nia_bell', 'wolf', 'bm.nipet', 'bm.nicd', 'nia'],
    ['gem', 'The Gem of Creativity', 'creativity_gem', 'wolf', 'bm.cgpet', 'bm.cgcd', 'gem'],
    ['batty', 'Batty', 'gentry_batty', 'wolf', 'bm.ytpet', 'bm.ytcd', 'batty'],
    ['eggbert', 'Eggbert', 'gentry_eggbert', 'wolf', 'bm.ebpet', 'bm.ebcd', 'eggbert'],
    ['count', 'The Count', 'gentry_count', 'wolf', 'bm.knpet', 'bm.kncd', 'count']);
  const after_ = async (w, H) => {
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t289foe]`);
    const home = K.find(k => k[0] === w)[6];
    await run(`${O}execute as TestRat at @s run function bm:p98/home/${home}`); await wait(5000, async () => (await cnt(H)) === 0);
    await run(`scoreboard players reset TestRat bm.hn_${w}`);
  };
  const assault = async (w, nm, H, typ) => {
    let hp = 200, drops = [], seen = 0, hidMax = 0, stun = false, up = 0; const t0 = Date.now();
    while (Date.now() - t0 < 14000) {
      const h = await num(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t289foe,limit=1] Health`);
      const on = (await num(`${O}scoreboard players get ${H} bm.ksw`)) === 3 && (await num(`${O}scoreboard players get ${H} bm.ksg`)) >= 1;
      if (on) seen++;
      if (h < hp - 0.01) { if (seen) drops.push(+(hp - h).toFixed(1)); hp = h; }
      const hid = await cnt('@e[type=minecraft:item_display,tag=bm.prhid]'); if (hid > hidMax) hidMax = hid;
      if (w === 'leo' && /slowness/.test(await run(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t289foe,limit=1] active_effects`))) stun = true;
      if ((w === 'bender' || w === 'emma') && on) { const y = await num(`${O}data get entity ${H} Pos[1]`); if (y > up) up = y; }
      if (seen && !on) { await sleep(400); const h2 = await num(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t289foe,limit=1] Health`); if (h2 < hp - 0.01) drops.push(+(hp - h2).toFixed(1)); break; }
      await sleep(40);
    }
    const sum = drops.reduce((a, b) => a + b, 0);
    ok(`...${nm} doesn't vanish: the move plays out in plain sight, on their own poses (no part of them hidden)`, seen > 0 && hidMax === 0, `move ticks seen ${seen}, parts hidden ${hidMax}`);
    ok(`...two or more blows straight through full diamond, 24.5 in all (14 x Might V, split; with a blow of their own the same moment, more)`, drops.length >= (w === 'emma' ? 1 : 2) && sum > 24 && sum < 42, `drops ${drops.join(', ')} = ${sum.toFixed(1)}`);
    if (w === 'leo') ok('...the shield bash stuns it first (slowed to a standstill, weakened)', stun);
    if (w === 'bender') ok('...and Bender up on its head, chomping', up > Y + 1.9, `highest ${up.toFixed(2)}`);
    if (w === 'emma') ok('...and Emma up in the air for her roll (a block and more) before the slam', up > Y + 2.2, `highest ${up.toFixed(2)}`);
    await sleep(1500);
    ok('...and then back on the ground, free to move (gravity back)', !/NoGravity: 1b/.test(await run(`${O}data get entity ${H} NoGravity`)) && (await num(`${O}scoreboard players get ${H} bm.ksw`)) !== 3,
       `${await run(`${O}data get entity ${H} NoGravity`)}; ksw ${await run(`${O}scoreboard players get ${H} bm.ksw`)}`);
    if (process.env.HOLD) await sleep(+process.env.HOLD); await after_(w, H);
  };
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('tag TestRat add bm.emmet'); await run('tag TestRat add bm.lnmet');
  for (const [w, nm, iid, typ, host, cd, home] of K.filter(k => !process.env.ONLY || process.env.ONLY.split(',').includes(k[0]))) {
    await run(`scoreboard players set TestRat bm.hn_${w} 1555`); await run(`scoreboard players set TestRat ${cd} 0`);
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.slot(0); await sleep(300); A.use(); await sleep(400); A.release();
    const H = `@e[type=minecraft:${typ},tag=${host},limit=1]`;
    if (!ok(`${nm} called with their own item`, await wait(8000, async () => (await cnt(H)) >= 1))) continue;
    if (!ok(`...a Champion (honours at rank III)`, await wait(4000, async () => (await cnt(`@e[type=minecraft:${typ},tag=${host},tag=bm.champ]`)) >= 1))) continue;
    await run(`${O}tp ${H} ${X + 0.5} ${Y + 1} ${Z + 3.5}`);
    await run(`${O}scoreboard players set ${H} bm.chcd 999`); await run(`${O}scoreboard players set ${H} bm.prcd 3`);
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t289foe]`);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y + 1} ${Z + 9.5} {Tags:["bm.t289foe"],NoAI:1b,Silent:1b,PersistenceRequired:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d},{id:"minecraft:armor",base:20d},{id:"minecraft:armor_toughness",base:8d}],equipment:{head:{id:"minecraft:diamond_helmet",count:1},chest:{id:"minecraft:diamond_chestplate",count:1},legs:{id:"minecraft:diamond_leggings",count:1},feet:{id:"minecraft:diamond_boots",count:1}}}`);
    if (ASSAULT.includes(w)) { await assault(w, nm, H, typ); continue; }
    let hp = 200, gone = 0, hidMax = 0, drops = [], after = []; const t0 = Date.now();
    while (Date.now() - t0 < 12000) {
      const h = await num(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t289foe,limit=1] Health`);
      if (h < hp - 0.01) { drops.push(+(hp - h).toFixed(1)); if (hidMax > 0) after.push(+(hp - h).toFixed(1)); hp = h; }
      const hid = await cnt('@e[type=minecraft:item_display,tag=bm.prhid]'); if (hid > hidMax) hidMax = hid;
      const pt = await num(`${O}scoreboard players get ${H} bm.prt`);
      if (pt >= 2) gone++;
      if (gone && pt === 0) { await sleep(300); const h2 = await num(`${O}data get entity @e[type=minecraft:zombie,tag=bm.t289foe,limit=1] Health`); if (h2 < hp - 0.01) after.push(+(hp - h2).toFixed(1)); break; }
      await sleep(40);
    }
    ok(`...${nm} vanishes - ${hidMax} parts of their model gone from sight - and comes back on the zombie`, gone > 0 && hidMax > 0, `move ticks seen ${gone}, parts hidden ${hidMax}`);
    ok(`...one blow straight through full diamond: 24.5 off its health (14 x Might V; with any blow of their own the same moment, more), armour or no armour`, after.some(d => d > 24 && d < 40), `drops ${drops.join(', ')}; from the vanish on: ${after.join(', ')}`);
    await sleep(2000);
    ok(`...and then whole again, free to move: no part left hidden, no longer frozen`,
       (await cnt('@e[type=minecraft:item_display,tag=bm.prhid]')) === 0 && !/NoAI: 1b/.test(await run(`${O}data get entity ${H} NoAI`)) && (await num(`${O}scoreboard players get ${H} bm.prt`)) === 0,
       `hidden ${await cnt('@e[type=minecraft:item_display,tag=bm.prhid]')}; NoAI ${await run(`${O}data get entity ${H} NoAI`)}; prt ${await run(`${O}scoreboard players get ${H} bm.prt`)}`);
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t289foe]`);
    if (home) { await run(`${O}execute as TestRat at @s run function bm:p98/home/${home}`); await wait(5000, async () => (await cnt(H)) === 0); }
    else await run(`${O}tp ${H} ~ -400 ~`);
    await run(`scoreboard players reset TestRat bm.hn_${w}`);
  }
  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
