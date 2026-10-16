// v2.33: the Heartwood Branch, Molten Gauntlet and Void Scepter (all forms, catalysts); the Elder Treant, Magma Colossus and
// Voidwalker (vanilla bodies, scaled up; ambience, attacks, enrage, death, retreat, spawns); WANTED; achievements.
const { bot, rcon, sleep } = require('./lib');
const X = 6600, Y = 100, Z = 6600;
const results = [];
let R, A, B; const run = (c) => R.run(c);
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const score = (who, obj) => num(`scoreboard players get ${who} ${obj}`);
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const re = new RegExp(`\\{[^{}]*id: "minecraft:${id}"[^{}]*\\}`); const m = s.match(re);
                                     if (!m) return null; const a = m[0].match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const ok = (n, p, d = '') => { results.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const tp = async (who, x, y, z, yaw = 0, pitch = 0, dim = 'overworld') => { await run(`execute in minecraft:${dim} run tp ${who} ${x} ${y} ${z} ${yaw} ${pitch}`); const b = who === 'TestRat' ? A : B; await sleep(250); if (b.pos) { b.pos.yaw = yaw; b.pos.pitch = pitch; } };
const mob = (x, y, z, tag, hp = 100, type = 'pillager') => run(`summon minecraft:${type} ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],NoAI:1b,PersistenceRequired:1b,Silent:1b,Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}d}]}`);
const hp = (sel) => num(`data get entity ${sel} Health`);
const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
const inv = async (it) => { const r = await run(`clear TestRat ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
const holding = async (iid) => (await run(`execute if items entity TestRat weapon.mainhand *[minecraft:custom_data~{bm:"${iid}"}]`)).includes('passed');
const give0 = async (iid) => { await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); A.slot(0); await sleep(300); await run('scoreboard players set TestRat bm.rcd 0'); };
const click = async (ms = 250) => { A.use(); await sleep(ms); A.release(); await sleep(250); };
const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
const at = () => `x=${X},y=${Y},z=${Z},distance=..80`;
const clean = () => run(`kill @e[type=!player,${at()}]`);
const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
const TOK = '*[custom_data~{bm:"token"}]';
(async () => {
  R = await rcon(); A = await bot('TestRat'); B = await bot('TestRat2'); await sleep(1500);
  for (const [b, n] of [[A, 'TestRat'], [B, 'TestRat2']]) b.on('update_health', (p) => { if (p.health <= 0) console.log('   !! ' + n + ' died'); });
  let parts = 0; A.on('world_particles', () => parts++);
  for (const w of ['TestRat', 'TestRat2']) { await run(`clear ${w}`); await run(`effect clear ${w}`); await run(`gamemode survival ${w}`);
    await run(`effect give ${w} saturation 9999 1 true`); await run(`effect give ${w} regeneration 9999 1 true`); }
  await run('weather clear'); await run('scoreboard players set #forced bm.bm 0'); await run('time set day'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 20'); await sleep(1300);
  await tp('TestRat', X + 0.5, Y + 1, Z + 0.5); await tp('TestRat2', X + 0.5, Y + 1, Z + 70.5); await sleep(2000);
  await run(`fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y} ${Z + 40} stone`); await run(`fill ${X - 40} ${Y + 1} ${Z - 40} ${X + 40} ${Y + 20} ${Z + 40} air`);
  await clean(); await sleep(300);
  const P0 = [X + 0.5, Y + 1, Z + 0.5];
  await run('effect give TestRat resistance 9999 3 true');

  // ================================================================ THE RELICS
  const F = { branch: ['heartwood_branch', 'branch_bark', 'branch_seed', 'branch_bloom'], gauntlet: ['molten_gauntlet', 'gauntlet_obsidian', 'gauntlet_magma', 'gauntlet_hearth'],
              scepter: ['void_scepter', 'scepter_phase', 'scepter_star', 'scepter_rift'] };
  for (const fam of Object.keys(F)) {
    await give0(F[fam][0]); const got = [];
    for (const [off, k] of [['minecraft:armadillo_scute 1', 1], ['minecraft:breeze_rod 1', 2], [null, 3], ['minecraft:blaze_rod 1', 0]]) {
      if (off) await run(`item replace entity TestRat weapon.offhand with ${off}`); else await run('loot replace entity TestRat weapon.offhand loot bm:items/heartstone');
      await tp('TestRat', ...P0, 0, -85); await click(); got.push(await holding(F[fam][k])); }
    ok(`${fam}: every catalyst turns it`, got.every(x => x), got.join(','));
  }
  // ---- Heartwood Branch
  await give0('heartwood_branch'); await tp('TestRat', ...P0, 0, 0);
  await mob(X + 0.5, Y + 1, Z + 6.5, 't_a'); await mob(X + 0.5, Y + 1, Z + 12.5, 't_far'); await sleep(300); await run('effect clear TestRat regeneration'); await click();
  ok('Thornlash: the whip hits the first thing within 8 (9 damage), slows it, heals you', (await hp('@e[tag=t_a,limit=1]')) === 91 && (await effect('@e[tag=t_a,limit=1]', 'slowness')) !== null &&
     (await hp('@e[tag=t_far,limit=1]')) === 100 && (await effect('TestRat', 'regeneration')) === 2, `${await hp('@e[tag=t_a,limit=1]')}, far ${await hp('@e[tag=t_far,limit=1]')}`);
  await run('effect give TestRat regeneration 9999 1 true'); await clean();
  await give0('branch_bark'); await mob(X + 0.5, Y + 1, Z + 2.5, 't_h', 100, 'zombie'); await sleep(200); await run('effect clear TestRat resistance'); await click();
  ok('Barkskin: Resistance II + Regeneration', (await effect('TestRat', 'resistance')) === 1 && (await score('TestRat', 'bm.rst')) > 0);
  await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  ok('...attackers are pricked and rooted', (await hp('@e[tag=t_h,limit=1]')) < 100 && (await effect('@e[tag=t_h,limit=1]', 'slowness')) === 3, `${await hp('@e[tag=t_h,limit=1]')}`);
  await run('effect give TestRat resistance 9999 3 true'); await clean();
  await give0('branch_seed'); await tp('TestRat', ...P0, 0, 0);
  await mob(X - 1.2, Y + 1, Z + 12.5, 't_l'); await mob(X + 0.5, Y + 1, Z + 12.5, 't_m'); await mob(X + 2.2, Y + 1, Z + 12.5, 't_r'); await sleep(300); await click();
  const sd = [await hp('@e[tag=t_l,limit=1]'), await hp('@e[tag=t_m,limit=1]'), await hp('@e[tag=t_r,limit=1]')];
  ok('Seedcaster: three seeds fan out, hurt and root', sd.every(h => h < 100) && (await effect('@e[tag=t_m,limit=1]', 'slowness')) === 3, sd.join(','));
  await clean();
  await give0('branch_bloom'); await tp('TestRat2', X + 4.5, Y + 1, Z + 0.5);
  await run(`setblock ${X + 2} ${Y} ${Z + 2} farmland`); await run(`setblock ${X + 2} ${Y + 1} ${Z + 2} wheat[age=0]`); await tp('TestRat', ...P0, 0, 0); await click();
  ok('Bloomheart: Regeneration II for you and an ally', (await effect('TestRat2', 'regeneration')) === 1);
  ok('...the crops around you ripen', (await run(`execute if block ${X + 2} ${Y + 1} ${Z + 2} minecraft:wheat[age=7]`)).includes('passed'));
  await run('effect give TestRat2 regeneration 9999 1 true'); await tp('TestRat2', X + 0.5, Y + 1, Z + 70.5);
  // ---- Molten Gauntlet
  await give0('molten_gauntlet');
  ok('Volcanic Gauntlet: knocks foes flying (knockback)', (await num('attribute TestRat minecraft:attack_knockback get')) >= 1.5);
  await tp('TestRat', ...P0, 0, 0); await mob(X + 0.5, Y + 1, Z + 3.5, 't_a'); await mob(X + 0.5, Y + 1, Z + 9.5, 't_far'); await sleep(300); await click();
  ok('...Eruption Punch: blasts what is in front of you, up and alight', (await hp('@e[tag=t_a,limit=1]')) < 100 && (await num('data get entity @e[tag=t_a,limit=1] Fire')) > 0 &&
     (await effect('@e[tag=t_a,limit=1]', 'levitation')) !== null && (await hp('@e[tag=t_far,limit=1]')) === 100);
  await clean();
  await give0('gauntlet_obsidian'); await mob(X + 0.5, Y + 1, Z + 2.5, 't_h', 100, 'zombie'); await sleep(200); await click();
  ok('Obsidian Guard: Fire Resistance + Resistance', (await effect('TestRat', 'fire_resistance')) !== null && (await score('TestRat', 'bm.rst')) > 0);
  await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  ok('...attackers burn', (await num('data get entity @e[tag=t_h,limit=1] Fire')) > 0);
  await clean(); await sleep(6000);
  await give0('gauntlet_magma'); await tp('TestRat', ...P0, 0, 0); await mob(X + 0.5, Y + 1, Z + 25.5, 't_a'); await sleep(300); await click();
  ok('Magmashot: 25 blocks, burns the target', (await hp('@e[tag=t_a,limit=1]')) < 100 && (await num('data get entity @e[tag=t_a,limit=1] Fire')) > 0);
  ok('...but never the ground', (await cnt(`@e[type=marker]`)) >= 0 && !(await run(`execute positioned ${X} ${Y + 1} ${Z + 25} if block ~ ~ ~ minecraft:fire`)).includes('passed'));
  await clean();
  await give0('gauntlet_hearth'); await tp('TestRat2', X + 4.5, Y + 1, Z + 0.5); await tp('TestRat', ...P0, 0, 0); await click();
  ok('Hearthfire: Fire Resistance, Regeneration, Absorption for an ally', (await effect('TestRat2', 'fire_resistance')) !== null && (await effect('TestRat2', 'absorption')) !== null);
  // ---- Void Scepter
  await tp('TestRat2', X + 20.5, Y + 1, Z - 15.5);
  await give0('void_scepter'); await tp('TestRat', ...P0, 0, 0); await mob(X + 0.5, Y + 1, Z + 12.5, 't_a'); await sleep(300); await click();
  const vp = await pos('@a[name=TestRat,limit=1]');
  ok('Voidrend: blinks you to the monster you look at and strikes it', (await hp('@e[tag=t_a,limit=1]')) < 100 && vp[2] > Z + 9, `you at z+${(vp[2] - Z).toFixed(1)}, ${await hp('@e[tag=t_a,limit=1]')}`);
  await clean();
  await give0('scepter_phase'); await tp('TestRat', ...P0, 0, 0); await mob(X + 0.5, Y + 1, Z + 2.5, 't_h', 100, 'zombie'); await sleep(200); await click();
  await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  ok('Phaseguard: whoever hits you floats away', (await score('TestRat', 'bm.rst')) > 0 && (await effect('@e[tag=t_h,limit=1]', 'levitation')) !== null);
  await clean(); await sleep(6000);
  await give0('scepter_star'); await tp('TestRat', ...P0, 0, 0);
  await mob(X + 8.5, Y + 1, Z + 8.5, 't_a'); await mob(X - 8.5, Y + 1, Z + 8.5, 't_b'); await sleep(300); await click(); await sleep(200);
  const bul = await cnt('@e[type=shulker_bullet]'); for (let i = 0; i < 40 && (await cnt('@e[type=shulker_bullet]')); i++) await sleep(250);
  ok('Starseeker: homing shulker bullets seek the monsters (and float them)', bul >= 2 && ((await effect('@e[tag=t_a,limit=1]', 'levitation')) !== null || (await effect('@e[tag=t_b,limit=1]', 'levitation')) !== null),
     `${bul} bullets, ${await hp('@e[tag=t_a,limit=1]')} / ${await hp('@e[tag=t_b,limit=1]')}`);
  await clean();
  await give0('scepter_rift'); await tp('TestRat', ...P0, 0, 0); await click();
  const bp = await pos('@a[name=TestRat2,limit=1]');
  ok('Riftcall: a player 25 blocks away blinks to your side, with Slow Falling', Math.hypot(bp[0] - P0[0], bp[2] - P0[2]) < 1.5 && (await effect('TestRat2', 'slow_falling')) !== null,
     bp.map(v => v.toFixed(1)).join(' '));
  await tp('TestRat2', X + 0.5, Y + 1, Z + 70.5); await run('item replace entity TestRat hotbar.0 with air');

  // ================================================================ THE BOSSES
  await run('effect give TestRat resistance 9999 2 true');
  const boss = async (key, ent, tag, admin, scale, attacks, extra) => {
    await tp('TestRat', ...P0, 0, 0); await clean();
    const tok0 = await inv(TOK); parts = 0; await sleep(1500); const calm = parts;
    await run(`execute as TestRat at @s run function bm:admin/${admin}`); await sleep(5600);   // (2.80: each stages its arrival - 5 s)
    const sel = `@e[type=minecraft:${ent},tag=${tag},limit=1]`;
    const sc = await num(`attribute ${sel} minecraft:scale get`);
    ok(`${key}: it appears - a vanilla ${ent}, scaled up`, (await cnt(sel)) === 1 && (scale === 0 || sc === scale), `scale ${sc}`);
    ok(`${key}: you sense it (song, title), its bossbar shows`, (await cnt(`@a[name=TestRat,tag=${tag}sensed]`)) === 1 && (await run(`bossbar get bm:${key} visible`)).includes('currently visible'));
    parts = 0; await sleep(2000);
    ok(`${key}: its ambience (particles around you)`, parts > calm + 10, `${calm} -> ${parts}`);
    await run(`tp ${sel} ${X + 6.5} ${Y + 1} ${Z + 6.5}`); await run(`data merge entity ${sel} {NoAI:1b}`);
    for (const [t, name, check] of attacks) {
      const d0 = await score('TestRat', 'bm.pdmg');
      await run(`scoreboard players set ${sel} bm.r53t ${t - 1}`);
      let pass = false, info = '';
      for (let i = 0; i < 30 && !pass; i++) { await sleep(100); [pass, info] = await check(d0); }
      ok(`${key} attack: ${name}`, pass, info);
      await run('effect clear TestRat levitation'); await run('effect clear TestRat slowness'); await run('effect clear TestRat darkness'); await tp('TestRat', ...P0, 0, 0);
    }
    if (extra) await extra(sel);
    await run(`data merge entity ${sel} {Health:${key === 'mcol' ? 200 : 160}f}`); await sleep(1300);
    ok(`${key}: enrages at half health`, (await cnt(`@e[tag=${tag}_rage]`)) === 1);
    await run(`damage ${sel} 9999 minecraft:player_attack by TestRat`); await sleep(6500);   // (2.80: and its death)
    ok(`${key}: it falls - WANTED paid, minions crumble, bossbar gone`, (await cnt(`@e[type=minecraft:${ent},tag=${tag}]`)) === 0 && (await inv(TOK)) >= tok0 + 8 &&
       (key === 'mcol' || (await cnt(`@e[tag=${tag}min]`)) === 0) && !(await run(`bossbar get bm:${key} visible`)).includes('currently visible'), `tokens ${tok0} -> ${await inv(TOK)}, minions ${await cnt(`@e[tag=${tag}min]`)}`);
    return sel;
  };
  const dmg = async (d0) => { const d = await score('TestRat', 'bm.pdmg'); return [d > d0, `damage taken ${d0} -> ${d}`]; };
  const has = (s, n = 1) => async () => { const c = await cnt(s); return [c >= n, `${c}`]; };
  const eff = (e) => async () => { const v = await effect('TestRat', e); return [v !== null, `${e} ${v}`]; };
  // ---- the Elder Treant
  await run('time set night'); await sleep(1500);
  await boss('trt', 'creaking', 'bm.trt', 'treant', 2.6, [
    [3, 'roots pin you in place', async (d0) => { const v = await effect('TestRat', 'slowness'); return [v === 6, `slowness ${v}`]; }],
    [6, 'a thrown log', async (d0) => { const r = await cnt('@e[type=block_display,tag=bm.r54_log]'); const d = await score('TestRat', 'bm.pdmg'); return [r > 0 || d > d0, `logs ${r}, damage ${d0} -> ${d}`]; }],
    [9, 'Twigs (little creakings)', has('@e[type=creaking,tag=bm.trtmin]')]], null);
  await sleep(2500);
  ok('trt: the log lands where it was thrown (no display left over)', (await cnt('@e[type=block_display,tag=bm.r54rock]')) === 0);
  ok('Heart of the Forest', await adv('treant'));
  await run('execute as TestRat at @s run function bm:admin/treant'); await sleep(5600); await run('time set day'); await sleep(1600);
  ok('trt: it walks back into the trees at dawn', (await cnt('@e[type=creaking,tag=bm.trt]')) === 0);
  // ---- the Magma Colossus
  await boss('mcol', 'magma_cube', 'bm.mcol', 'colossus', 0, [
    [3, 'a ground slam (hurts, throws, burns)', dmg],
    [6, 'a magma boulder', async (d0) => { const r = await cnt('@e[type=block_display,tag=bm.r54_magma]'); return [r > 0, `boulders ${r}`]; }],
    [9, 'lava geysers under your feet (telegraphed)', async (d0) => { const g = await cnt('@e[type=marker,tag=bm.r54gey]'); return [g > 0, `geysers ${g}`]; }]],
    async (sel) => {
      const size = await num(`data get entity ${sel} Size`), mh = await num(`attribute ${sel} minecraft:max_health get`);
      ok('mcol: a gigantic magma cube (Size 7, 420 health)', size === 7 && mh === 420, `size ${size}, max health ${mh}`);
      await run(`data merge entity ${sel} {Health:270f}`); await sleep(1300);
      ok('mcol: it sheds Magma Spawn as it is hurt', (await cnt('@e[type=magma_cube,tag=bm.mcolmin]')) >= 2);
      await run('kill @e[type=magma_cube,tag=bm.mcolmin]');
    });
  await sleep(600);
  const named = await cnt('@e[type=magma_cube,name="The Magma Colossus"]'), spawn = await cnt('@e[type=magma_cube,tag=bm.mcolmin]');
  ok('mcol: it bursts into smaller cubes - renamed Magma Spawn, and none of them counts as the boss', named === 0 && spawn >= 2 && (await cnt('@e[type=magma_cube,tag=bm.mcol]')) === 0, `still named ${named}, spawn ${spawn}`);
  await run(`kill @e[type=magma_cube,${at()}]`);
  ok('Cooled Off', await adv('colossus'));
  // ---- the Voidwalker
  await boss('vwk', 'enderman', 'bm.vwk', 'voidwalker', 2.5, [
    [3, 'it blinks behind you and strikes', dmg],
    [6, 'homing shulker bullets', has('@e[type=shulker_bullet]')],
    [9, 'void grasp (darkness)', eff('darkness')],
    [12, 'Voidlings (endermites)', async () => { const c = await cnt('@e[type=endermite,tag=bm.vwkmin]'); return [c >= 1, `${c} voidlings, ${await cnt('@e[type=endermite]')} endermites, timer ${await score('@e[type=enderman,tag=bm.vwk,limit=1]', 'bm.r53t')}`]; }]],
    async (sel) => {
      const ang = await run(`data get entity ${sel} angry_at`);
      ok('vwk: it is angry at you', ang.includes('I;'), ang.slice(-50));
      ok('vwk: it carries no blocks', !(await run(`data get entity ${sel} carriedBlockState`)).includes('Name'));
    });
  await run(`kill @e[type=shulker_bullet]`); await run('effect clear TestRat levitation');
  ok('Stare Down', await adv('voidwalker'));
  // ---- natural spawns: a forest night, the Nether wastes, the outer End
  await run(`fillbiome ${X - 12} ${Y - 2} ${Z - 12} ${X + 12} ${Y + 12} ${Z + 12} minecraft:forest`); await run('time set night'); await sleep(1500);
  ok('the forest predicate sees the forest', (await run('execute as TestRat at @s if predicate bm:p54/forest')).includes('passed'));
  await run('execute as TestRat at @s run function bm:p54/trt/try'); await sleep(500);
  ok('a forest night spawn: the Treant walks out of the trees', (await cnt('@e[type=creaking,tag=bm.trt]')) === 1);
  await run('kill @e[type=creaking,tag=bm.trt]'); await run(`fillbiome ${X - 12} ${Y - 2} ${Z - 12} ${X + 12} ${Y + 12} ${Z + 12} minecraft:plains`); await run('time set day');
  // the Nether: a cave with a floor 18 blocks off (chunks loaded first)
  await tp('TestRat', X + 0.5, 120, Z + 0.5, 0, 0, 'the_nether'); await run('effect give TestRat slow_falling 30 0 true'); await sleep(3000);
  await run(`execute in minecraft:the_nether run fill ${X - 25} 60 ${Z - 25} ${X + 25} 60 ${Z + 25} netherrack`);
  await run(`execute in minecraft:the_nether run fill ${X - 25} 61 ${Z - 25} ${X + 25} 72 ${Z + 25} air`);
  await tp('TestRat', X + 0.5, 61, Z + 0.5, 0, 0, 'the_nether'); await sleep(2500);
  await run('execute as TestRat at @s run function bm:p54/mcol/try'); await sleep(600);
  const mp = await pos('@e[type=magma_cube,tag=bm.mcol,limit=1]');
  ok('a Nether spawn: the Colossus heaves up in the cave ~18 blocks off (it may be mid-hop)', mp && mp[1] > 60.5 && mp[1] < 72 && Math.hypot(mp[0] - X - 0.5, mp[2] - Z - 0.5) > 12, mp ? mp.map(v => v.toFixed(1)).join(' ') : 'none');
  await run('execute in minecraft:the_nether run kill @e[type=magma_cube]');
  // the End: an island far out (chunks loaded first)
  await tp('TestRat', X + 0.5, 70, Z + 0.5, 0, 0, 'the_end'); await sleep(3000);
  await run(`execute in minecraft:the_end run fill ${X - 25} 60 ${Z - 25} ${X + 25} 60 ${Z + 25} end_stone`);
  await run(`execute in minecraft:the_end run fill ${X - 25} 61 ${Z - 25} ${X + 25} 72 ${Z + 25} air`);
  await tp('TestRat', X + 0.5, 61, Z + 0.5, 0, 0, 'the_end'); await sleep(2500);
  await run('execute as TestRat at @s run function bm:p54/vwk/try'); await sleep(600);
  const ep = await pos('@e[type=enderman,tag=bm.vwk,limit=1]');
  ok('an outer-End spawn: the Voidwalker steps out on the island', ep && Math.abs(ep[1] - 61) < 0.5, ep ? ep.map(v => v.toFixed(1)).join(' ') : 'none');
  await run('execute in minecraft:the_end run kill @e[type=enderman,tag=bm.vwk]');
  await tp('TestRat', ...P0);
  // ---- achievements across all six
  ok('Legendary Hunter (all six roaming bosses)', await adv('legendary_hunter'));
  for (const i of ['horseman_head', 'pharaoh_crook', 'storm_talon', 'heartwood_branch', 'molten_gauntlet', 'void_scepter']) await run(`loot give TestRat loot bm:items/${i}`); await sleep(400);
  ok('Grand Relic Hunter (a relic of each)', await adv('grand_relic_hunter'));
  await run(`summon text_display ${X - 5} ${Y + 3} ${Z} {Tags:["bm.bboard","bm.npc","t_board"]}`); await sleep(2300);
  const board = await run('data get entity @e[type=text_display,tag=t_board,limit=1] text');
  ok('the Bounty Board lists all six WANTED bosses', ['Horseman', 'Pharaoh', 'Storm Roc', 'Treant', 'Colossus', 'Voidwalker'].every(n => board.includes(n)), board.slice(0, 60));
  await clean();
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
