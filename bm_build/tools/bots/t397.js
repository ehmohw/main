// 3.1a: THE PIERCING BLOW, SEEN - as a regular (non-op) player. Forty followers no longer vanish for it (phase226b): each Champion
// (rcon: honours at rank III) is called with their own item beside a still zombie in full diamond (armour 20, toughness 8; 200
// health), and their Rank III move must play out ON SCREEN:
//   - no part of the model is ever hidden (no item display tagged bm.prhid, the vanish's mark, at any sample);
//   - the host never jumps: its step between samples, per game tick, stays under 1.5 blocks (an eased dash, never a teleport);
//   - the damage lands: 24.5 in all (14 of rend x Might V), straight through the armour, over the move's blows.
// Plus one KEEP follower (Cecil) who still vanishes, as before (his Shadow Veil: parts hidden, then one blow of 24.5).
// ONLY=celi,zib picks; the default is all forty and Cecil. (The Champion's other blow and their own signature are held off by rcon.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (c) => { const o = await run(c); const m = o.match(/has (-?\d+) \[/) || o.match(/(-?[\d.]+)[fd]?$/); return m ? +m[1] : NaN; };
  const pos = async (H) => { const o = await run(`${O}data get entity ${H} Pos`); const m = o.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const gt = async () => { const m = (await run('time query gametime')).match(/(\d+)/); return m ? +m[1] : NaN; };
  const X = 18300, Y = 100, Z = 16620;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  // [key, name, item, host tag, cooldown, home (p98/home/...)]
  const K = [['celi', 'Celi', 'celi_charm', 'bm.celipet', 'bm.cecd', 'celi'], ['zib', 'Zib', 'donadian_medal', 'bm.zibpet', 'bm.zbcd', 'zib'],
    ['kw', 'KillerWatt', 'kw_spark', 'bm.kxpet', 'bm.kxcd', 'killerwatt'], ['apo', 'Apophiss', 'apo_oath', 'bm.appet', 'bm.apcd', 'apo'],
    ['frog', 'the Frog', 'frog_signet', 'bm.frogpet', 'bm.fgcd', 'frog'], ['don', 'Donado', 'donado_tag', 'bm.donado', 'bm.dncd', 'donado'],
    ['fishy', 'Fishy', 'fy_bowl', 'bm.fypet', 'bm.fycd', 'fishy'], ['dennis', 'Dennis', 'dw_horn', 'bm.dwpet', 'bm.dwcd', 'dennis'],
    ['ashur', 'Ashur', 'ashur_cinder', 'bm.aspet', 'bm.ascd', 'ashur'], ['neighbor', 'the Neighbor', 'neighbor_baton', 'bm.nbpet', 'bm.nbcd', 'neighbor'],
    ['ava', 'Queen Ava', 'av_locket', 'bm.avpet', 'bm.avcd', 'ava'], ['pearlq', 'Queen Pearl', 'pq_pearls', 'bm.pqpet', 'bm.pqcd', 'pearlq'],
    ['lantern', 'the Arachno-Lantern', 'ln_gourd', 'bm.lnpet', 'bm.lncd', 'lantern'], ['capshun', 'Mr. Capshun', 'capshun_pencil', 'bm.mzpet', 'bm.mzcd', 'capshun'],
    ['sky', 'the Sky Buddies', 'sky_mobile', 'bm.ybpet', 'bm.ybcd', 'sky'], ['pxcecil', '8-Bit Cecil', 'cart_cecil', 'bm.xcpet', 'bm.xccd', 'pxcecil'],
    ['pxleo', '8-Bit Leo', 'cart_leo', 'bm.xlpet', 'bm.xlcd', 'pxleo'], ['pxemma', '8-Bit Emma', 'cart_emma', 'bm.xmpet', 'bm.xmcd', 'pxemma'],
    ['kettle', 'Kettle', 'kettle_plane', 'bm.ktpet', 'bm.ktcd', 'kettle'], ['gem', 'the Gem', 'creativity_gem', 'bm.cgpet', 'bm.cgcd', 'gem'],
    ['batty', 'Batty', 'gentry_batty', 'bm.ytpet', 'bm.ytcd', 'batty'], ['eggbert', 'Eggbert', 'gentry_eggbert', 'bm.ebpet', 'bm.ebcd', 'eggbert'],
    ['count', 'the Count', 'gentry_count', 'bm.knpet', 'bm.kncd', 'count'], ['dragon', 'the Doodle Mob', 'doodle_drawing', 'bm.ddpet', 'bm.ddcd', 'dragon'],
    ['eraser', 'the Eraser', 'eraser_crumb', 'bm.ezpet', 'bm.ezcd', 'eraser'], ['cursor', 'the Cursor', 'cursor_mouse', 'bm.uxpet', 'bm.uxcd', 'cursor'],
    ['inkblot', 'the Ink Blot', 'ink_pot', 'bm.ibpet', 'bm.ibcd', 'inkblot'], ['speech', 'the Speech Bubble', 'caption_card', 'bm.wbpet', 'bm.wbcd', 'speech'],
    ['lightbringer', 'the Lightbringer', 'herald_feather', 'bm.lhpet', 'bm.lhcd', 'lightbringer'], ['dryad', 'the Pale Dryad', 'dryad_cap', 'bm.pypet', 'bm.pycd', 'dryad'],
    ['sovereign', 'the Bound Sovereign', 'sov_eye', 'bm.xvpet', 'bm.xvcd', 'sovereign'], ['vexis', 'Vexis', 'vexis_link', 'bm.xbpet', 'bm.xbcd', 'vexis'],
    ['keeper', 'the Keeper of Bonds', 'bond_thread', 'bm.tkpet', 'bm.tkcd', 'keeper'], ['ratking', 'the Rat King', 'royal_marker', 'bm.rwpet', 'bm.rwcd', 'ratking'],
    ['cake', 'the Cake', 'cake_candle', 'bm.czpet', 'bm.czcd', 'cake'], ['sapling', 'the Sapling', 'golden_pip', 'bm.sxpet', 'bm.sxcd', 'sapling'],
    ['spawner', 'the Spawner', 'pilot_light', 'bm.nxpet', 'bm.nxcd', 'spawner'], ['cairn', 'the Cairn', 'waystone_heart', 'bm.axpet', 'bm.axcd', 'cairn'],
    ['knight', 'the Hollow Statue Knight', 'knight_token', 'bm.hxpet', 'bm.hxcd', 'knight'], ['mimic', 'the Mimic', 'mimic_key', 'bm.mxpet', 'bm.mxcd', 'mimic'],
    ['cecil', 'Cecil (KEEP)', 'cecil_gem', 'bm.cecilpet', 'bm.cpcd', 'cecil']];
  const FOE = '@e[type=minecraft:zombie,tag=bm.t397foe,limit=1]';
  const home = async (h, H) => {
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t397foe]`);
    await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');
    await run(`${O}execute as TestRat at @s run function bm:p98/home/${h}`); await wait(5000, async () => (await cnt(H)) === 0);
  };
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('tag TestRat add bm.emmet'); await run('tag TestRat add bm.lnmet');
  const only = process.env.ONLY ? process.env.ONLY.split(',') : null;
  for (const [w, nm, iid, host, cd, h] of K.filter(k => !only || only.includes(k[0]))) {
    await run(`scoreboard players set TestRat bm.hn_${w} 1555`); await run(`scoreboard players set TestRat ${cd} 0`);
    await wait(4000, async () => !((await num('scoreboard players get TestRat bm.gvhc')) > 0), 300);      // (the items' shared debounce)
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.slot(0); await sleep(300); A.use(); await sleep(400); A.release();
    const H = `@e[type=minecraft:wolf,tag=${host},limit=1]`;
    if (!ok(`${nm} called with their own item`, await wait(8000, async () => (await cnt(H)) >= 1))) { await run(`scoreboard players reset TestRat bm.hn_${w}`); continue; }
    if (!ok(`...a Champion (honours at rank III)`, await wait(4000, async () => (await cnt(`@e[type=minecraft:wolf,tag=${host},tag=bm.champ]`)) >= 1))) { await home(h, H); continue; }
    await run(`${O}tp ${H} ${X + 0.5} ${Y + 1} ${Z + 3.5}`);
    await run(`${O}scoreboard players set ${H} bm.chcd 999`); await run(`${O}scoreboard players set ${H} bm.kcd1 999`); await run(`${O}scoreboard players set ${H} bm.kcd2 999`);
    await run(`${O}scoreboard players set ${H} bm.prcd 2`);
    await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t397foe]`);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y + 1} ${Z + 9.5} {Tags:["bm.t397foe","bm.seen"],NoAI:1b,Silent:1b,PersistenceRequired:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d},{id:"minecraft:armor",base:20d},{id:"minecraft:armor_toughness",base:8d}],equipment:{head:{id:"minecraft:diamond_helmet",count:1},chest:{id:"minecraft:diamond_chestplate",count:1},legs:{id:"minecraft:diamond_leggings",count:1},feet:{id:"minecraft:diamond_boots",count:1}}}`);
    if (w === 'cecil') {                                         // KEEP: he still vanishes
      let hp = 200, gone = 0, hidMax = 0, after = []; const t0 = Date.now();
      while (Date.now() - t0 < 12000) {
        const hh = await num(`${O}data get entity ${FOE} Health`);
        if (hh < hp - 0.01) { if (hidMax > 0) after.push(+(hp - hh).toFixed(2)); hp = hh; }
        const hid = await cnt('@e[type=minecraft:item_display,tag=bm.prhid]'); if (hid > hidMax) hidMax = hid;
        const pt = await num(`${O}scoreboard players get ${H} bm.prt`); if (pt >= 2) gone++;
        if (gone && pt === 0) break;
        await sleep(40);
      }
      ok(`...${nm} still vanishes (${hidMax} parts hidden) and strikes out of his shadows: 24.5 straight through`, hidMax > 0 && after.some(d => d > 24 && d < 40), `parts hidden ${hidMax}; drops ${after.join(', ')}`);
      await sleep(1500); ok('...and whole again after', (await cnt('@e[type=minecraft:item_display,tag=bm.prhid]')) === 0);
      await home(h, H); await run(`scoreboard players reset TestRat bm.hn_${w}`); continue;
    }
    let hp = 200, drops = [], seen = 0, hidMax = 0, jump = 0, last = null; const t0 = Date.now();
    while (Date.now() - t0 < 15000) {
      const hh = await num(`${O}data get entity ${FOE} Health`);
      const on = (await num(`${O}scoreboard players get ${H} bm.ksw`)) === 3 && (await num(`${O}scoreboard players get ${H} bm.ksg`)) >= 1;
      if (on) {
        seen++;
        // (the Pos and the game time are two rcon replies, maybe a tick apart: bracket the Pos with the time read before and after it,
        //  and divide by the most ticks there can have been between two Pos reads - else two dash steps can count as one tick)
        const tb = await gt(), p = await pos(H), ta = await gt();
        if (p && last) { const d = Math.hypot(p[0] - last.p[0], p[1] - last.p[1], p[2] - last.p[2]) / Math.max(1, ta - last.tb); if (d > jump) jump = d; }
        last = p ? { p, tb } : last;
      }
      if (hh < hp - 0.01) { if (seen) drops.push(+(hp - hh).toFixed(2)); hp = hh; }
      const hid = await cnt('@e[type=minecraft:item_display,tag=bm.prhid]'); if (hid > hidMax) hidMax = hid;
      if (seen && !on) { await sleep(400); const h2 = await num(`${O}data get entity ${FOE} Health`); if (h2 < hp - 0.01) drops.push(+(hp - h2).toFixed(2)); break; }
      await sleep(30);
    }
    const sum = drops.reduce((a, b) => a + b, 0);
    ok(`...${nm}'s Piercing Blow plays out in sight: never a part hidden`, seen > 0 && hidMax === 0, `move samples ${seen}, parts hidden ${hidMax}`);
    ok('...no jump: the host moves at most ~1.5 blocks a tick (eased, never a teleport)', seen > 0 && jump <= 1.6, `fastest ${jump.toFixed(2)} blocks/tick`);
    ok('...the damage lands: 24.5 straight through full diamond (14 x Might V, split over its blows)', drops.length >= 1 && sum > 24 && sum < 42, `drops ${drops.join(', ')} = ${sum.toFixed(2)}`);
    await home(h, H); await run(`scoreboard players reset TestRat bm.hn_${w}`);
  }
  await run('clear TestRat'); await run('effect clear TestRat');
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
