// 3.0g: THE DREAD BOSSES AND THE DREAD SOVEREIGN, HARDER (hitcap.py, phase197, phase238) and THE CUTSCENES IN THE LIGHT (phase176's
// p176/nodark), as a regular (non-op) player. rcon sets the stage (a floor, a boss risen, the Undercrown's progress, a boss's health at
// a threshold, the player's gear and effects) and reads health and tags; the bot plays: it strikes with the final boss's own sword,
// stands in the bosses' reach, breaks the Dread Anchors with its blows and watches the Sovereign's coming.
//   dread    the Malevolent Snowbeast: one blow of the Sovereign's Edge with Strength C takes no more than 25 off it (THE HIT CAP); in full
//            netherite with Protection IV and no Resistance, its blows still land heavy (one hit of 4.5+: DREAD, past armour and its
//            enchantments - the old freeze came through at a third)
//   sov      the Dread Sovereign: its coming with a Dread mob beside you and Darkness on you - cleared at once, none laid on you while the
//            camera holds (bm.nodark), the Dread's darkness back once it lets go; THE DREAD WARD at half its first pool (Invulnerable,
//            four Dread Anchors, its title): your blows do nothing to it; each anchor broken with 4 blows; all four: the ward down,
//            it reels, no Resistance; then one Strength C blow of the Edge takes 25 at most; its blows through Protection IV
//            netherite (one hit of 6+); its first entrance (the turn) watched with the Dread beside you: no Darkness
//   node t341.js [dread|sov]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const OX = 2560, OZ = -2560;
const N = 'execute in minecraft:the_nether run ', O = 'execute in minecraft:overworld run ';
const CAP = 25;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (D, who, o) => +((await run(`${D}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (D, sel) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const hpOf = async (D, sel) => +(((await run(`${D}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
  const hp = () => hpOf('', '@a[name=TestRat,limit=1]');
  const fx = async () => await run('data get entity TestRat active_effects');
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (D, sel) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (D, sel) => { const u = await uuidOf(D, sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  // (the final boss's sword, and Strength C: a blow of hundreds - what the cap is for)
  const edge = async () => { await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/sov_edge'); A.slot(0);
    await run('effect give TestRat minecraft:strength 120 100 true'); await sleep(1400); };
  const strike = async (D, sel) => { const e = await entOf(D, sel); if (!e) return null; const h0 = await hpOf(D, sel); A.attack(e.entityId); await sleep(250);
    const h1 = await hpOf(D, sel); return h0 - h1; };
  // (full netherite, Protection IV, no Resistance - and room to be hurt: 200 health)
  const plate = async () => { for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
    await run(`item replace entity TestRat armor.${s} with minecraft:netherite_${p}[enchantments={"minecraft:protection":4}]`);
    await run('effect clear TestRat minecraft:resistance'); await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true'); };
  // (the heaviest single drop in the player's health over ms, polled - one blow at a time)
  const heaviest = async (ms, between) => { let last = await hp(), big = 0; const t0 = Date.now();
    while (Date.now() - t0 < ms) { if (between) await between(); await sleep(100); const h = await hp(); if (h < last) big = Math.max(big, last - h); last = h;
      if (h < 60) { await run('effect give TestRat minecraft:instant_health 1 20 true'); await sleep(100); last = await hp(); } } return big; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('scoreboard players set #hard bm.cfg 1'); await run('clear TestRat'); await run('difficulty normal');
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');

  if (on('dread')) {
    const X = 18600, Y = 100, Z = 16200;
    await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`); await sleep(2000);
    await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y + 20} ${Z + 20} minecraft:air`); await run(`${O}fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`);
    await at(O, X + 0.5, Y, Z - 6.5, 0, 0);
    await run(`${O}execute as @e[tag=bm.db_snow] at @s run function bm:p197/snow/sink`);
    await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z - 5.5} rotated 0 0 run function bm:p197/snow/rise`);
    const B = `@e[tag=bm.db_snow,x=${X},y=${Y},z=${Z},distance=..30,limit=1]`;
    ok('the Snowbeast rises (and is under the hit cap: bm.hcap, 25)', await wait(4000, async () => (await cnt(O, B)) === 1) && /bm\.hcap/.test(await run(`${O}tag ${B} list`)) && (await sc(O, B, 'bm.hcc')) === CAP * 10);
    ok('...and wakes (no longer invulnerable)', await wait(8000, async () => !/1b/.test(await run(`${O}data get entity ${B} Invulnerable`))));
    await edge();
    const bp = await pos(O, B); await at(O, bp[0], bp[1], bp[2] - 2.6, 0, 20);
    const d1 = await strike(O, B);
    ok(`one blow of the Sovereign's Edge with Strength C takes at most ${CAP}`, d1 > 0 && d1 <= CAP + 0.5, `took ${d1}`);
    await sleep(800);
    const d2 = await strike(O, B);
    ok('...and the next the same (a cap, not a wall)', d2 > 0 && d2 <= CAP + 0.5, `took ${d2}`);
    await run('effect clear TestRat minecraft:strength'); await run('clear TestRat');
    await plate(); await run('effect give TestRat minecraft:regeneration infinite 1 true');
    const big = await heaviest(25000, async () => { const p = await pos(O, B); if (p) await run(`${O}tp TestRat ${p[0] + 2} ${p[1]} ${p[2] - 2}`); });
    ok('in Protection IV netherite, no Resistance: its blows still land heavy (one of 4.5+ - Dread, past armour and enchantments)', big >= 4.5, `heaviest ${big.toFixed(2)}`);
    await run(`${O}execute as @e[tag=bm.db_snow] at @s run function bm:p197/snow/sink`);
    await run('attribute TestRat minecraft:max_health base set 20'); await run('clear TestRat'); await run('effect clear TestRat');
    await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  }

  if (on('sov')) {
    await run('tag TestRat add bm.lkpass');
    const ME = '@e[type=minecraft:husk,tag=bm.usov,limit=1]';
    const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
    await run(`${N}tp TestRat ${OX - 40} 100 ${OZ - 40}`); await run(`${N}setblock ${OX - 40} 98 ${OZ - 40} minecraft:obsidian`);
    const UVER = +require('fs').readFileSync(require('path').join(__dirname, '..', '..', 'phase237.py'), 'utf8').match(/^UVER = (\d+)/m)[1];
    if ((await sc(N, '#uver', 'bm.p2')) !== UVER) await run('function bm:admin/under/place');
    ok('the stage: the Undercrown placed', await wait(900000, async () => (await sc(N, '#uver', 'bm.p2')) === UVER, 2000));
    await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`); await sleep(4000);
    ok('...its markers loaded', await wait(90000, async () => (await cnt(N, DG)) === 1, 1000));
    const hub = await pos(N, DG); if (hub) { await at(N, hub[0], hub[1] + 1, hub[2]); await sleep(3000); }
    await run(`${N}scoreboard players set ${DG} bm.pz 17`);
    for (const t of ['bm.dfin', 'bm.svfirst', 'bm.svdone']) await run(`tag TestRat remove ${t}`);
    await run('scoreboard players set #ufell bm.p2 0'); await run('scoreboard players set #dfell bm.cfg 0'); await run('scoreboard players set #ucol bm.p2 0');
    ok('the Sovereign kneels on its throne, dormant', await wait(15000, async () => (await cnt(N, '@e[type=minecraft:husk,tag=bm.usov,tag=bm.svdorm]')) === 1));
    const ar = await pos(N, '@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_under,limit=1]');
    // (a Dread mob at the edge of the hall, beside where TestRat will stand; Darkness on TestRat already)
    const sp = [ar[0] + 2, ar[1], ar[2] + 12];
    await run(`${N}kill @e[tag=bm.t341d]`);
    await run(`${N}summon minecraft:zombie ${sp[0]} ${sp[1]} ${sp[2]} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,Tags:["bm.t341d","bm.seen","bm.dgmob","bm.udread"]}`);
    await run(`${N}execute as @e[type=minecraft:zombie,tag=bm.t341d] run function bm:p176/mk/zombie`);
    await at(N, ar[0] + 0.5, ar[1], ar[2] + 22.5, 180, 0);
    await run('effect give TestRat minecraft:darkness 60 0'); await run('effect give TestRat minecraft:blindness 60 0');
    A.titles.length = 0;
    await at(N, ar[0] + 0.5, ar[1], ar[2] + 10.5, 180, 0);
    ok('crossing the hall: it wakes - the coming (the camera holds you)', await wait(4000, async () => (await cnt(N, '@e[tag=bm.usov,tag=bm.svintro]')) === 1));
    await sleep(600);
    let dark = 0, samples = 0, held = 0;
    await wait(15000, async () => { const f = await fx(); samples++; if (/darkness|blindness/.test(f)) dark++; if (/bm\.nodark/.test(await run('tag TestRat list'))) held++;
      return (await cnt(N, '@e[tag=bm.usov,tag=bm.svintro]')) === 0; }, 300);
    ok('...with a Dread beside you: never Darkness or Blindness while it plays (and you were held: bm.nodark)', dark <= 1 && held >= samples - 1 && samples > 10, `${dark} of ${samples} dark, held ${held}`);
    ok('the coming over: it fights (phase I)', await wait(10000, async () => (await cnt(N, `@e[tag=bm.usov,tag=bm.svlive,scores={bm.svph=1}]`)) === 1));
    ok('...let go, the Dread beside you darkens you again', await wait(6000, async () => /darkness/.test(await fx())), await fx());
    await run(`${N}kill @e[tag=bm.t341d]`); await run('effect clear TestRat minecraft:darkness');
    ok('...and the Sovereign is under the hit cap (25 for one fighter)', (await sc(N, ME, 'bm.hcc')) === CAP * 10 && /bm\.hcap/.test(await run(`${N}tag ${ME} list`)));
    // (its Wellsprings put out: they'd mend it while we read its health)
    await run(`${N}execute as @e[type=minecraft:marker,tag=bm.uwell,tag=bm.svlit] at @s run function bm:p238/w/out`);

    // ---- THE DREAD WARD: at half its first pool
    const pool = await sc(N, ME, 'bm.svhp');
    await run(`${N}data modify entity ${ME} Health set value ${Math.floor(pool / 2) + 100 - 5}f`);
    ok('half its first pool: THE DREAD WARD (bm.svshd, Invulnerable)', await wait(3000, async () => /bm\.svshd/.test(await run(`${N}tag ${ME} list`))) &&
       /1b/.test(await run(`${N}data get entity ${ME} Invulnerable`)));
    ok('...four Dread Anchors rise round the hall', (await cnt(N, '@e[type=minecraft:interaction,tag=bm.svanci]')) === 4);
    ok('..."ITS WARD IS UP - BREAK THE FOUR DREAD ANCHORS"', await wait(2000, async () => A.titles.some(t => /WARD IS UP/.test(t))), A.titles.slice(-2).join(' / '));
    await run(`${N}kill @e[tag=bm.svk]`);
    await edge();
    let mp = await pos(N, ME); await at(N, mp[0], mp[1], mp[2] + 3, 180, 20);
    const dw = await strike(N, ME);
    ok('...your blow (the Edge, Strength C) does nothing to it', dw !== null && Math.abs(dw) < 0.5, `took ${dw}`);
    await run('effect clear TestRat minecraft:strength');
    for (let i = 0; i < 4; i++) {
      const sel = '@e[type=minecraft:interaction,tag=bm.svanci,limit=1]';
      const ap = await pos(N, sel); if (!ap) break;
      await at(N, ap[0] + 1.6, ap[1], ap[2], 90, 20);
      const e = await entOf(N, sel); const n0 = await cnt(N, '@e[type=minecraft:interaction,tag=bm.svanci]');
      for (let k = 0; k < 4 && e; k++) { A.attack(e.entityId); await sleep(700); }
      ok(`...anchor ${i + 1}: four blows break it`, await wait(2000, async () => (await cnt(N, '@e[type=minecraft:interaction,tag=bm.svanci]')) === n0 - 1), `${await cnt(N, '@e[type=minecraft:interaction,tag=bm.svanci]')} left`);
      await run(`${N}kill @e[tag=bm.svk]`);
    }
    ok('all four broken: the ward is down (not Invulnerable), it reels, no Resistance', await wait(2000, async () => !/bm\.svshd/.test(await run(`${N}tag ${ME} list`))) &&
       !/1b/.test(await run(`${N}data get entity ${ME} Invulnerable`)) && (await sc(N, ME, 'bm.svz')) < 0 && !/resistance/.test(await run(`${N}data get entity ${ME} active_effects`)));

    // ---- THE HIT CAP, and its blows through Protection IV
    await edge();
    mp = await pos(N, ME); await at(N, mp[0], mp[1], mp[2] + 3, 180, 20);
    const ds = await strike(N, ME);
    ok(`one blow of the Edge with Strength C takes at most ${CAP} off it`, ds > 0 && ds <= CAP + 0.5, `took ${ds}`);
    await run('effect clear TestRat minecraft:strength'); await run('clear TestRat');
    await run(`${N}data modify entity ${ME} Health set value ${Math.floor(pool / 2) + 100 - 30}f`);
    await plate(); await run('effect give TestRat minecraft:regeneration infinite 1 true');
    const big = await heaviest(30000, async () => { await run(`${N}kill @e[tag=bm.svk]`); await run(`${N}kill @e[type=minecraft:husk,tag=bm.svm]`);
      const p = await pos(N, ME); if (p) await run(`${N}execute positioned ${p[0]} ${p[1]} ${p[2]} rotated as ${ME} run tp TestRat ^ ^ ^4 facing ${p[0]} ${p[1] + 4} ${p[2]}`); });
    ok('in Protection IV netherite, no Resistance: its blows land heavy (one of 6+ - Dread)', big >= 6, `heaviest ${big.toFixed(2)}`);
    await run('attribute TestRat minecraft:max_health base set 20'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('clear TestRat');
    await run('effect give TestRat minecraft:resistance infinite 4 true');

    // ---- its first entrance (the turn), watched with the Dread beside you
    await run(`${N}summon minecraft:zombie ${sp[0]} ${sp[1]} ${sp[2]} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Invulnerable:1b,Tags:["bm.t341d","bm.seen","bm.dgmob","bm.udread"]}`);
    await run(`${N}execute as @e[type=minecraft:zombie,tag=bm.t341d] run function bm:p176/mk/zombie`);
    await at(N, sp[0] - 1.5, sp[1], sp[2] + 1, 180, 0);
    await run('effect give TestRat minecraft:darkness 60 0');
    await run(`${N}data modify entity ${ME} Health set value 100f`);
    ok('its first pool spent: its entrance (the turn) begins', await wait(4000, async () => /bm\.svturn/.test(await run(`${N}tag ${ME} list`))));
    dark = 0; samples = 0;
    await wait(9000, async () => { samples++; if (/darkness|blindness/.test(await fx())) dark++; return false; }, 300);
    ok('...watched with a Dread beside you: no Darkness while it plays', dark <= 1 && samples > 10, `${dark} of ${samples} dark`);

    await run(`${N}kill @e[tag=bm.t341d]`);
    await run(`${N}execute as ${ME} at @s run function bm:p238/abandon`);
    await run('scoreboard players set #ufell bm.p2 0');
    await run('tag TestRat remove bm.lkpass');
  }

  await run('attribute TestRat minecraft:max_health base set 20'); await run('clear TestRat'); await run('effect clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
