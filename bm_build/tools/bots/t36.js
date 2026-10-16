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
// (a real hit: the essences' "when hit" effects need a mob's own swing - /damage by a mob never fires them)
const hitBy = async (x, y, z, tag) => { const h0 = A.health;
  await run(`summon minecraft:husk ${x} ${y} ${z} {Tags:["bm.seen","${tag}"],PersistenceRequired:1b,Silent:1b,Health:100f,attributes:[{id:"minecraft:max_health",base:100d}]}`);
  for (let i = 0; i < 40 && !(A.health < h0); i++) await sleep(150);
  await run(`data merge entity @e[tag=${tag},limit=1] {NoAI:1b}`); await sleep(300); };
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
  A.on('update_health', (p) => { if (p.health <= 0) console.log('   !! died'); });
  let parts = 0; A.on('world_particles', () => parts++);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat saturation 9999 1 true');
  await run('time set day'); await run('weather clear'); await sleep(1000);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} stone`); await run(`fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 12} ${Z + 20} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);

  // ---- capacity by material
  await hold('minecraft:wooden_sword'); await shard('green'); await altar();
  ok('wood takes no sockets', !(await cd()).includes('bm_sn') && last().includes('flimsy'), last());
  await hold('minecraft:iron_sword'); const base = await attr('attack_damage'); await shard('green', 2); await altar();
  ok('iron: one socket (+1.5 Attack Damage)', (await cd()).includes('bm_s1: "green"') && Math.abs((await attr('attack_damage')) - base - 1.5) < 0.01, `${base} -> ${await attr('attack_damage')}`);
  await altar(); ok('...and only one', !(await cd()).includes('bm_s2') && last().includes('full'), last());
  await hold('minecraft:golden_sword'); const gb = await attr('attack_damage'); await shard('green'); await altar();
  ok('gold: its shard counts double (+3)', Math.abs((await attr('attack_damage')) - gb - 3) < 0.01 && (await hand('.components."minecraft:lore"')).includes('gilded'));
  // ---- vanilla only
  await run('loot replace entity TestRat hotbar.0 loot bm:items/thirsting_blade'); A.slot(0); await sleep(200); await shard('green'); await altar();
  ok('Black Market goods are refused', !(await cd()).includes('bm_sn') && last().includes('honest vanilla'), last());
  await hold('minecraft:netherite_sword[minecraft:custom_data={bm_from:1b}]'); await shard('green'); await altar();
  ok('vanilla gear bought from a trader is refused too', !(await cd()).includes('bm_sn') && last().includes('earn it'), last());
  // ---- diamond: two sockets and a combo (green + red = Bloodlust)
  await hold('minecraft:diamond_sword'); const mh0 = await attr('max_health'); await shard('green'); await altar(); await shard('red'); await altar();
  const c1 = await cd();
  ok('diamond: two sockets; green + red combine into Bloodlust', c1.includes('bm_s1: "green"') && c1.includes('bm_s2: "red"') && c1.includes('bm_cmb: "gr"'), c1.slice(-120));
  await shard('cyan'); await altar(); ok('...and no third', last().includes('full'));
  ok('red Xenite socket: Vitality (+2 max health while held)', (await attr('max_health')) === mh0 + 2, `${await attr('max_health')}`);
  await run('damage TestRat 8 minecraft:generic'); await sleep(300); const hb = A.health;
  await mob(X + 0.5, Y + 1, Z + 3.5, 't_k', 2); await sleep(200); await run('damage @e[tag=t_k,limit=1] 50 minecraft:player_attack by TestRat'); await sleep(400);
  ok('Bloodlust: a kill heals you', A.health > hb + 2, `${hb} -> ${A.health}`);
  // ---- Second Wind (violet + red) on a worn diamond chestplate
  await hold('minecraft:diamond_chestplate'); await shard('violet'); await altar(); await shard('red'); await altar();
  ok('violet + red: Second Wind', (await cd()).includes('bm_cmb: "vr"'));
  await run('item replace entity TestRat armor.chest from entity TestRat weapon.mainhand'); await run('item replace entity TestRat hotbar.0 with air');
  await run('effect clear TestRat'); await sleep(300); await run(`damage TestRat ${Math.ceil(A.health) - 4} minecraft:generic`); await sleep(1500);
  ok('...below 3 hearts: Regeneration II and Speed, then a recharge', (await effect('TestRat', 'regeneration')) === 1 && (await num('scoreboard players get TestRat bm.r55cd')) > 50,
     `regen ${await effect('TestRat', 'regeneration')}`);
  await run('effect give TestRat instant_health 1 4 true'); await run('item replace entity TestRat armor.chest with air');
  // ---- red size cycle (sneak + right-click with a red shard)
  await hold('minecraft:iron_helmet'); await shard('red'); await altar(); await shard('red'); await infuse();
  ok('a red socket\'s size cycles: GROWTH', (await cd()).includes('bm_red: "grow"'));
  await shard('red'); await infuse(); ok('...SHRINK', (await cd()).includes('bm_red: "shrink"'));
  await shard('red'); await infuse(); ok('...off', (await cd()).includes('bm_red: "off"'));
  // ---- netherite: two sockets + a Masterwork
  await hold('minecraft:netherite_sword'); await shard('green'); await altar(); await shard('cyan'); await altar();
  ok('netherite: two sockets, green + cyan = Precision', (await cd()).includes('bm_cmb: "gc"'));
  const as0 = await attr('attack_speed'); await shard('violet', 4); await altar();
  ok('Masterwork needs a Medallion', !(await cd()).includes('bm_mw') && last().includes('Medallion'), last());
  await run('loot give TestRat loot bm:items/medallion'); await shard('violet', 4); await altar();
  ok('Masterwork (4 violet + a Medallion): Relentless, +0.4 attack speed', (await cd()).includes('bm_mw: "relentless"') && Math.abs((await attr('attack_speed')) - as0 - 0.4) < 0.01 &&
     (await inv('*[custom_data~{bm:"medallion"}]')) === 0 && (await num('data get entity TestRat equipment.offhand.count')) !== 4, `${as0} -> ${await attr('attack_speed')}`);
  await shard('green', 4); await run('loot give TestRat loot bm:items/medallion'); await altar(); ok('...one Masterwork per item', last().includes('full'));
  await run('clear TestRat *[custom_data~{bm:"medallion"}]');
  // ---- scrap a relic: Tokens, Medallions and its Essence
  await run(`setblock ${X + 5} ${Y + 1} ${Z} minecraft:barrel`); await run(`summon marker ${X + 5.5} ${Y + 1} ${Z + 0.5} {Tags:["bm.rs","bm.rs_scrap_bin"]}`);
  await run(`item replace block ${X + 5} ${Y + 1} ${Z} container.0 with minecraft:stone`);
  await run(`loot replace block ${X + 5} ${Y + 1} ${Z} container.0 loot bm:items/pharaoh_crook`); await sleep(2200);
  const bin = await run(`data get block ${X + 5} ${Y + 1} ${Z} Items`);
  ok('the Scrap Bin takes a spare relic: 10 Tokens, 2 Medallions and its Essence', bin.includes('essence_pharaoh') && /bm: "token"/.test(bin) && /bm: "medallion"/.test(bin) && !bin.includes('pharaoh_crook'), bin.slice(0, 160));
  await run(`setblock ${X + 5} ${Y + 1} ${Z} air`); await run('kill @e[tag=bm.rs_scrap_bin]');
  // ---- Essences: netherite only, right kind only
  await hold('minecraft:diamond_sword'); await offL('essence_horseman'); await infuse();
  ok('an Essence only takes to netherite', !(await cd()).includes('bm_ess'), last());
  await hold('minecraft:netherite_sword'); await offL('essence_treant'); await infuse();
  ok('...of the right kind (a chestplate essence refuses a sword)', !(await cd()).includes('bm_ess'), last());
  await hold('minecraft:netherite_sword'); await offL('essence_horseman'); await infuse();
  ok("Horseman's Essence: infused into a netherite sword", (await cd()).includes('bm_ess: "horseman"') && (await hand('.components."minecraft:enchantments"')).includes('ess_horseman'));
  await mob(X + 0.5, Y + 1, Z + 2.2, 't_a', 200); await sleep(400);
  const ids = () => Object.values(A.ents).filter(e => Math.abs(e.x - (X + 0.5)) < 0.2 && Math.abs(e.z - (Z + 2.2)) < 0.2).pop()?.entityId;
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300); A.attack(ids()); await sleep(500);
  ok('...its hits set the target alight', (await num('data get entity @e[tag=t_a,limit=1] Fire')) > 0, `Fire ${await num('data get entity @e[tag=t_a,limit=1] Fire')}`);
  // resonance: + a green socket
  await shard('green'); await altar();
  ok('RESONANCE: the essence + a green socket awaken Hellfire', (await cd()).includes('bm_res: "horseman"') && (await hand('.components."minecraft:enchantments"')).includes('res_horseman'));
  await mob(X + 1.8, Y + 1, Z + 2.2, 't_b', 200); await sleep(400);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300); let burst = false; for (let i = 0; i < 14 && !burst; i++) { A.attack(ids()); await sleep(900); burst = (await hp('@e[tag=t_b,limit=1]')) < 200; }
  ok('...hits sometimes burst into flame round the target (hits the foe beside it)', burst, `${await hp('@e[tag=t_b,limit=1]')}`);
  parts = 0; await sleep(1500);
  ok('...and it glows with its aura while held', parts > 5, `${parts} particle packets`);
  await run(`kill @e[tag=t_a]`); await run(`kill @e[tag=t_b]`);
  // ---- chest essences: Colossus (attackers burn), and Pharaoh's daylight damage
  await hold('minecraft:netherite_chestplate'); await offL('essence_colossus'); await infuse(); await shard('red'); await altar();
  ok("Colossus's Essence + red: Magma Aura resonance on a chestplate", (await cd()).includes('bm_res: "colossus"'));
  await run('item replace entity TestRat armor.chest from entity TestRat weapon.mainhand'); await run('item replace entity TestRat hotbar.0 with air');
  await hitBy(X + 0.5, Y + 1, Z + 1.8, 't_h');
  ok('...whoever hits you burns', (await num('data get entity @e[tag=t_h,limit=1] Fire')) > 0, `Fire ${await num('data get entity @e[tag=t_h,limit=1] Fire')}, wearing ${(await run('data get entity TestRat equipment.chest.components."minecraft:enchantments"')).slice(-60)}`);
  let aura = false; for (let i = 0; i < 12 && !aura; i++) { await sleep(500); aura = (await hp('@e[tag=t_h,limit=1]')) < 100; }
  ok('...and the Magma Aura burns what stands close', aura, `${await hp('@e[tag=t_h,limit=1]')}`);
  await run('kill @e[tag=t_h]'); await run('item replace entity TestRat armor.chest with air');
  await hold('minecraft:netherite_sword'); await offL('essence_pharaoh'); await infuse(); await mob(X + 0.5, Y + 1, Z + 2.2, 't_a', 200); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
  A.attack(ids()); await sleep(400); const day = 200 - await hp('@e[tag=t_a,limit=1]');
  ok("Pharaoh's Essence: +3 damage in daylight (8 + 3)", day >= 10.9, `${day} damage`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat');
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });
