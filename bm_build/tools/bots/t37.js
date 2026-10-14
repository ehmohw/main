// v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks,
// relic scrapping -> Essences, Essence infusion (netherite only) and Resonance (AoE + aura).
const { bot, rcon, sleep } = require('./lib');
const X = 7000, Y = 100, Z = 7000;
const results = [];
let R, A; const run = (c) => R.run(c);
const num = async (c) => { const s = await run(c); const m = s.match(/(-?\d+(?:\.\d+)?)[dfbsL]?\s*$/) || s.match(/has (-?\d+)/); return m ? parseFloat(m[1]) : NaN; };
const effect = async (who, id) => { const s = await run(`data get entity ${who} active_effects`); const re = new RegExp(`\\{[^{}]*id: "minecraft:${id}"[^{}]*\\}`); const m = s.match(re);
                                     if (!m) return null; const a = m[0].match(/amplifier: (-?\d+)b/); return a ? ((+a[1]) + 256) % 256 : 0; };
const ok = (n, p, d = '') => { results.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
const inv = async (it) => { const r = await run(`clear TestRat ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
const hand = async (path = '') => run(`data get entity TestRat SelectedItem${path}`);
const cd = async () => (await run('data get entity TestRat SelectedItem.components."minecraft:custom_data"'));
const mob = (x, y, z, tag, hp = 100, type = 'pillager', ai = false) => run(`summon minecraft:${type} ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],${ai ? '' : 'NoAI:1b,'}PersistenceRequired:1b,Silent:1b,Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}d}]}`);
const hp = (sel) => num(`data get entity ${sel} Health`);
const hold = async (it) => { await run(`item replace entity TestRat hotbar.0 with ${it}`); A.slot(0); await sleep(250); };
const off = async (it) => { await run(`item replace entity TestRat weapon.offhand with ${it}`); await sleep(100); };
const offL = async (iid, n = 1) => { await run(`loot replace entity TestRat weapon.offhand loot bm:items/${iid}`); if (n > 1) await run(`item modify entity TestRat weapon.offhand {type:"minecraft:set_count",count:${n}}`); await sleep(100); };
const altar = async () => { await run('execute as TestRat at @s run function bm:p24/altar/use'); await sleep(150); };
const infuse = async () => { await run('execute as TestRat at @s run function bm:p24/altar/infuse'); await sleep(150); };
const SH = (c, n = 1) => `minecraft:totem_of_undying[minecraft:custom_data={bm:"xenite_${c}"}] ${n}`;
const shard = async (c, n = 1) => { await run(`loot replace entity TestRat weapon.offhand loot bm:items/xenite_${c}`); await run(`item modify entity TestRat weapon.offhand {type:"minecraft:set_count",count:${n}}`); await sleep(100); };
const attr = (a) => num(`attribute TestRat minecraft:${a} get`);
const last = () => A.bars.slice(-1)[0] || '';
(async () => {
  R = await rcon(); A = await bot('TestRat'); await sleep(1500);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat saturation 9999 1 true');
  await run('time set day'); await run('weather clear'); await sleep(800);
  const home = async () => { await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300); };
  await home(); await sleep(2000); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  const ids = () => Object.values(A.ents).filter(e => Math.abs(e.x - (X + 0.5)) < 0.2 && Math.abs(e.z - (Z + 2.2)) < 0.2).pop()?.entityId;
  const weapon = async (b, c) => { await hold('minecraft:netherite_sword'); await offL('essence_' + b); await infuse(); await shard(c); await altar(); return (await cd()).includes(`bm_res: "${b}"`); };
  const chest = async (b, c) => { await hold('minecraft:netherite_chestplate'); await offL('essence_' + b); await infuse(); await shard(c); await altar();
    const r = (await cd()).includes(`bm_res: "${b}"`); await run('item replace entity TestRat armor.chest from entity TestRat weapon.mainhand'); await run('item replace entity TestRat hotbar.0 with air'); return r; };
  const hits = async (n, cond) => { for (let i = 0; i < n; i++) { await home(); A.attack(ids()); await sleep(950); if (await cond()) return true; } return false; };
  // Roc + violet: bolts on hit, Stormcall to two more foes
  ok("Roc's Essence + violet: Stormcall resonance", await weapon('roc', 'violet'));
  await mob(X + 0.5, Y + 1, Z + 2.2, 't_a', 500); await mob(X + 3.5, Y + 1, Z + 3.5, 't_b', 200); await mob(X - 2.5, Y + 1, Z + 4.5, 't_c', 200); await sleep(400);
  ok('...hits call bolts that leap to the other foes', await hits(16, async () => (await hp('@e[tag=t_b,limit=1]')) < 200 || (await hp('@e[tag=t_c,limit=1]')) < 200),
     `${await hp('@e[tag=t_b,limit=1]')} / ${await hp('@e[tag=t_c,limit=1]')}`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  // Pharaoh + cyan: Sunburst
  ok("Pharaoh's Essence + cyan: Sunburst resonance", await weapon('pharaoh', 'cyan'));
  await mob(X + 0.5, Y + 1, Z + 2.2, 't_a', 500); await mob(X + 2.5, Y + 1, Z + 3.2, 't_b', 200); await sleep(400);
  ok('...hits blaze with light round the target', await hits(16, async () => (await hp('@e[tag=t_b,limit=1]')) < 200), `${await hp('@e[tag=t_b,limit=1]')}`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('item replace entity TestRat hotbar.0 with air');
  // Treant + green: regeneration; Thornmail
  ok("Treant's Essence + green: Thornmail resonance", await chest('treant', 'green'));
  await run('effect clear TestRat'); let rg = false; for (let i = 0; i < 16 && !rg; i++) { await sleep(500); rg = (await effect('TestRat', 'regeneration')) !== null; }
  ok('...slow, steady regeneration', rg);
  await mob(X + 0.5, Y + 1, Z + 1.8, 't_h', 100, 'zombie'); await sleep(1200); await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  ok('...whoever hits you is torn and rooted', (await hp('@e[tag=t_h,limit=1]')) < 100 && (await effect('@e[tag=t_h,limit=1]', 'slowness')) === 3);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('item replace entity TestRat armor.chest with air');
  // Voidwalker + cyan: Void Shroud (blink + foes float)
  ok("Voidwalker's Essence + cyan: Void Shroud resonance", await chest('voidwalker', 'cyan'));
  await home(); await mob(X + 0.5, Y + 1, Z + 1.8, 't_h', 100, 'zombie'); await mob(X + 2.5, Y + 1, Z + 0.5, 't_b', 100, 'zombie'); await sleep(1200);
  await run('damage TestRat 2 minecraft:mob_attack by @e[tag=t_h,limit=1]'); await sleep(300);
  const p = (await run('data get entity TestRat Pos'));
  ok('...when hit you blink away and the foes near you float', (await effect('@e[tag=t_b,limit=1]', 'levitation')) !== null && !p.includes(`${Z + 0.5}d]`), p.slice(-50));
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat');
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
