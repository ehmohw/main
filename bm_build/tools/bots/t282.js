// 2.94u: THE ATTACK KIT, the rest (atk.biters, phase224), as a regular (non-op) player:
//   the Frog with Mustache, Donado, Wilfrey (they fight with their own bite): you strike a monster once and step back; they take it
//   on, and their bites land with the kit's impact (its hit sound, heard by your client - none of yours: you've stopped swinging);
//   Leo's Guard: you hurt (rcon: the stage) with a monster near and Leo 8 off - he dashes to you in steps (no jump over 2.5 a
//   sample, once a blink to your side), shield up, and ends at your side.
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
  const X = 18180, Y = 100, Z = 16360;
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
  const husk = async (dx, dz, tag) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","t282","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
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

  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  // (the client hears sounds by their registry number: learn the impact's)
  A.sounds.length = 0; await run('execute as TestRat at @s run playsound minecraft:entity.player.attack.strong neutral TestRat ~ ~ ~ 0.1 1'); await sleep(800);
  const STRONG = (A.sounds[0] || {}).name || 'attack.strong'; console.log('   (the impact sound is ' + STRONG + ')');
  const CDS = ['bm.dncd', 'bm.fgcd', 'bm.wlcd', 'bm.lecd'];
  for (const o of CDS) await run(`scoreboard players set TestRat ${o} 0`);
  const only = process.argv[2] ? new RegExp(process.argv[2], 'i') : null;
  const K = [['the Frog with Mustache', 'frog_signet', 'bm.frogpet', 'p138/home/frog'], ['Donado', 'donado_tag', 'bm.donado', 'p138/home/don'], ['Wilfrey', 'wilfrey_locket', 'bm.wilfrey', 'p138/home/wil']];
  for (const [name, iid, tag, home] of K) {
    if (only && !only.test(name)) continue;
    const H = `@e[type=minecraft:wolf,tag=${tag},limit=1]`;
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.chats.length = 0; await use(0); if (!ok(`${name} called`, await wait(6000, async () => (await cnt(H)) === 1), A.chats.slice(-2).join(' | ').slice(0, 200))) continue;
    await sleep(1500); await stage(H);
    await husk(0, 2, 'tz0'); await sleep(800);
    const u = await uuidOf('@e[tag=tz0,limit=1]'); const ent = Object.values(A.ents).find(e => e.objectUUID === u);
    if (!ok('(the bot sees the monster)', !!ent)) continue;
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 20`); await sleep(400);
    A.attack(ent.entityId); await sleep(1500);
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z - 5.5} 0 20`);                    // (you step back: from here it's theirs)
    A.sounds.length = 0; const h0 = 197;   // (full, less your one punch)
    await wait(12000, async () => A.sounds.some(s => s.name === STRONG), 200);
    ok(`${name} takes it on: the bites land with the kit's impact (heard)`, A.sounds.some(s => s.name === STRONG) && (await hp('tz0')) < h0, `${h0} -> ${await hp('tz0')} ${[...new Set(A.sounds.map(s => s.name))].join(',').slice(0, 160)}`);
    await run(`${O}kill @e[tag=t282]`); await run(`${O}execute as TestRat at @s run function bm:${home}`); await sleep(1000);
  }
  // ---- Leo's Guard
  if (!only || only.test('Leo')) {
    const LEO = '@e[type=minecraft:wolf,tag=bm.leopet,limit=1]';
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/leo_crest'); await sleep(400);
    await use(0); ok('Leo called', await wait(6000, async () => (await cnt(LEO)) === 1)); await sleep(1500);
    await run(`${O}scoreboard players set ${LEO} bm.kcd1 99999`); await run(`${O}scoreboard players set ${LEO} bm.leg 0`);
    const at = await pos('TestRat');
    for (let i = 0; i < 5; i++) { await run(`${O}tp ${LEO} ${at[0] + 8} ${at[1]} ${at[2]}`); await run(`${O}data merge entity ${LEO} {Sitting:0b}`); await sleep(500);
      const q = await pos(LEO); if (q && Math.hypot(q[0] - at[0], q[2] - at[2]) >= 6) break; }
    await run(`${O}summon minecraft:husk ${at[0] - 3} ${at[1]} ${at[2] - 5} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["tz1","t282","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(800); await run('damage TestRat 12.5 minecraft:generic'); await sleep(100);
    console.log('   (your health: ' + (await run('data get entity TestRat Health')).replace(/.*: /, '') + '; his guard cooldown ' + (await sc(LEO, 'bm.leg')) + ', distance ' + JSON.stringify(await pos(LEO)) + ' you ' + JSON.stringify(at) + ')');
    const me = await pos('TestRat'); let last = await pos(LEO), big = 0, far = 0, close = 99; const p0 = last; const t0 = Date.now(); let guarded = false;
    while (Date.now() - t0 < 6000) { await sleep(40); const p = await pos(LEO); if (!p || !last) continue; big = Math.max(big, Math.hypot(p[0] - last[0], p[2] - last[2])); far = Math.max(far, Math.hypot(p[0] - p0[0], p[2] - p0[2])); last = p; close = Math.min(close, Math.hypot(p[0] - me[0], p[2] - me[2]));
      if (!guarded && /has [1-9]/.test(await run(`${O}scoreboard players get ${LEO} bm.leg`))) guarded = true; }
    await run('effect give TestRat minecraft:instant_health 1 3 true'); await run('effect give TestRat minecraft:resistance 900 4 true');
    ok('LEO\'S GUARD: you hurt, a monster near - he guards you', guarded);
    ok('...dashing to your side in steps (no blink)', far > 4 && big <= 2.5, JSON.stringify({ big, far }));
    ok('...and he comes right to your side', close <= 3, `${close}`);
    await run(`${O}kill @e[tag=t282]`); await run(`${O}execute as TestRat at @s run function bm:p98/home/leo`);
  }
  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
