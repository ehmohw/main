// 2.94u: SIGNATURE MOVES III (phase224), as a regular (non-op) player - each of the other twenty fighters called with their own
// item, monsters set down near (rcon: the stage). For each: the move starts (its timeline, bm.ksw), the ones that close in travel
// in steps (no jump over 3 a sample - two ticks at most), and its blows land (the monster is hurt by 8 or more, less the husk's armour):
//   KillerWatt (Storm Leap), Zib (Orbital Strike), Tullius (Anchor's Away), Fishy (Tidal Bubble - two near), Dennis (Mother Lode
//   Rush), Pistachio (Silver Service), King Omega (Soul Glide), the Chef (Kitchen Fury), the Neighbor (Grand Finale - two near),
//   Queen Ava (Riptide), Queen Pearl (Royal Twirl), Bloo (Savage Leap), the Stalker (Night Hunt), the Arachno-Lantern (Ember
//   Pounce), Bones (Death Roll), Mr. Capshun (Ink Rush), the Sky Buddies (Storm Front), 8-Bit Emma, Leo and Cecil.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1, 4).map(Number) : null; };
  const sc = async (sel, o) => +(((await run(`${O}scoreboard players get ${sel} ${o}`)).match(/has (-?\d+)/) || [0, -1])[1]);
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2000); };
  const X = 18100, Y = 100, Z = 16280;
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
  const husk = async (dx, dz, tag) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","t280","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
  // (a move watched: its positions while bm.ksw is set; started? biggest step, how far it went, where it ended)
  const watch = async (host, ms) => { let last = null, big = 0, far = 0, on = false, p0 = null, end = null; const t0 = Date.now();
    while (Date.now() - t0 < ms) { await sleep(40); const k = await sc(host, 'bm.ksw'); const p = await pos(host); if (!p) continue;
      if (k >= 1) { if (!on) { on = true; p0 = p; last = p; } big = Math.max(big, Math.hypot(p[0] - last[0], p[2] - last[2])); far = Math.max(far, Math.hypot(p[0] - p0[0], p[2] - p0[2])); last = p; end = p; }
      else if (on) break; }
    return { on, big, far, p0, end }; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:invisibility 900 0 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:sandstone`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 8} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  const stage = async (host, dx, dz) => { await run(`${O}tp ${host} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`${O}scoreboard players set ${host} bm.kcd1 0`); };

  // [name, item, host tag, home fn, the monsters (dx, dz), closes in?]
  const K = [['KillerWatt', 'kw_spark', 'bm.kxpet', 'p98/home/killerwatt', [[0, 7]], 1], ['Zib', 'donadian_medal', 'bm.zibpet', 'p98/home/zib', [[6, 6]], 0],
    ['Tullius', 'tul_coin', 'bm.tupet', 'p98/home/tul', [[-7, 0]], 1], ['Fishy', 'fy_bowl', 'bm.fypet', 'p145/home', [[3, 3], [-3, 4]], 0],
    ['Dennis', 'dw_horn', 'bm.dwpet', 'p163/dw/home', [[0, 7]], 1], ['Pistachio', 'pi_cloche', 'bm.pipet', 'p163/pi/home', [[6, 0]], 1],
    ['King Omega', 'om_monocle', 'bm.ompet', 'p170/home', [[0, -7]], 1], ['The Chef', 'chef_ladle', 'bm.kkpet', 'p186/home', [[-6, 0]], 1],
    ['The Neighbor', 'neighbor_baton', 'bm.nbpet', 'p187/home', [[3, 3], [-3, 3]], 0], ['Queen Ava', 'av_locket', 'bm.avpet', 'p189/home', [[0, 7]], 1],
    ['Queen Pearl', 'pq_pearls', 'bm.pqpet', 'p190/home', [[6, 0]], 1], ['Bloo', 'bo_claw', 'bm.bopet', 'p191/home', [[0, 8]], 1],
    ['The Stalker', 'st_hook', 'bm.svpet', 'p193/home', [[-8, 0]], 1], ['The Arachno-Lantern', 'ln_gourd', 'bm.lnpet', 'p194/home', [[0, -7]], 1],
    ['Bones', 'bn_whistle', 'bm.bjpet', 'p196/home', [[7, 0]], 1], ['Mr. Capshun', 'capshun_pencil', 'bm.mzpet', 'p198/home', [[0, 6]], 1],
    ['The Sky Buddies', 'sky_mobile', 'bm.ybpet', 'p211/home', [[6, 6]], 0], ['8-Bit Emma', 'cart_emma', 'bm.xmpet', 'p213e/home', [[0, 6]], 1],
    ['8-Bit Leo', 'cart_leo', 'bm.xlpet', 'p213l/home', [[-6, 0]], 1], ['8-Bit Cecil', 'cart_cecil', 'bm.xcpet', 'p213c/home', [[6, 6]], 0]];
  await run('tag TestRat add bm.lnmet');                // (the Lantern hatched and taken home already: the stage)
  const only = process.argv[2] ? new RegExp(process.argv[2], 'i') : null;
  for (const [name, iid, tag, home, foes, moves] of K) {
    if (only && !only.test(name)) continue;
    const H = `@e[type=minecraft:wolf,tag=${tag},limit=1]`;
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.chats.length = 0; await use(0); if (!ok(`${name} called`, await wait(6000, async () => (await cnt(H)) === 1), A.chats.slice(-2).join(' | ').slice(0, 200))) continue;
    await sleep(1500); await run(`${O}scoreboard players set ${H} bm.kcd1 999`);
    let w, hs;
    for (let tr = 0; tr < 3; tr++) {        // (its own moves may get in first: a try or two more)
      await run(`${O}kill @e[tag=t280]`); await run(`${O}scoreboard players set ${H} bm.kcd1 999`); await sleep(1500);
      await stage(H);
      for (const [i, [dx, dz]] of foes.entries()) await husk(dx, dz, 'tz' + i);
      w = await watch(H, 7000); await sleep(500);
      hs = []; for (let i = 0; i < foes.length; i++) hs.push(await hp('tz' + i));
      if (w.on && (!moves || (w.far > 2.5 && w.big <= 3)) && hs.every(h => h >= 0 && h <= 192)) break;
      console.log(`   (try ${tr + 1}: ${JSON.stringify(w)} ${hs})`);
    }
    ok(`${name}: the move plays${moves ? ', across the gap in steps (no jump over 3 a sample - two ticks)' : ''}`, w.on && (!moves || (w.far > 2.5 && w.big <= 3)), JSON.stringify(w));
    ok(`...its blows land (each monster hurt 8 or more)`, hs.every(h => h >= 0 && h <= 192), hs.join(','));
    await run(`${O}kill @e[tag=t280]`); await run(`${O}execute as TestRat at @s run function bm:${home}`); await sleep(1000);
  }

  await run('tag TestRat remove bm.lnmet'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
