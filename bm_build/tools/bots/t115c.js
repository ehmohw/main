// 2.72 (III): Smelling Salts, the Thief's Hourglass, the Alarm Jammer, Masterworks, the Codex, each tier's own finds
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, relf, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const { num, cnt, room, at, sc, alarm, solved, go, qs, heist, begin, local, pos } = H;
  const ONLY = process.argv[2] || ''; const want = k => !ONLY || ONLY.split(',').includes(k);
  const A = await bot('TestRat'); await sleep(2500);
  const ITEM = id => `*[minecraft:custom_data~{bm:"${id}"}]`;
  const has = async (id, slot = 'container.*') => /passed/.test(await run(`execute if items entity TestRat ${slot} ${ITEM(id)}`));
  const count = async (id) => +(((await run(`execute store result score #t bm.rng run clear TestRat ${ITEM(id)} 0`)).match(/(\d+)/) || [0, 0])[1]);
  const give = async (id, slot) => { const g = fnText('admin/tier_finds').split('\n').find(l => l.includes(`bm:"${id}"`)); const it = g.replace(/^give @s /, '').replace(/ 1$/, '');
    if (slot) await run(`item replace entity TestRat ${slot} with ${it}`); else await run(`give TestRat ${it}`); };
  const inst = () => `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${H.GI || 0}},limit=1]`;
  const gi = () => num('scoreboard players get TestRat bm.gvi');
  const isc = async (o) => { const g = await gi(); return num(`execute in bm:gutter run scoreboard players get @e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${g}},limit=1] ${o}`); };
  const attr = async (a) => +(((await run(`attribute TestRat minecraft:${a} get`)).match(/is (-?[\d.]+)/) || [0, NaN])[1]);
  const asRat = c => run(`execute as TestRat at TestRat run ${c}`);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');

  // ================================================================== SMELLING SALTS
  if (want('salts')) {
    const gt = fnText('p70/r/lobby/init');
    ok('Goldtooth sells the Smelling Salts, the Thief\'s Hourglass and the Alarm Jammer', ['smelling_salts', 'thiefs_hourglass', 'alarm_jammer'].every(i => gt.includes(`bm:"${i}"`)));
    await heist('levers', 'a', 2); await begin();
    const q = (await qs('levers'))[0]; await go('levers', q, 12, 12);
    await run('effect clear TestRat'); await run('clear TestRat');
    await give('smelling_salts', 'weapon.mainhand');
    const lv0 = await isc('bm.gvlv');
    A.bars.length = 0;
    await run('damage TestRat 200 minecraft:generic'); await sleep(800);
    const h = await num('data get entity TestRat Health');
    ok('A blow that would knock you out, salts in hand: you stay up, the salts are spent, no try lost',
       h > 0 && !(await has('smelling_salts', 'weapon.mainhand')) && (await isc('bm.gvlv')) === lv0 && A.bars.some(b => /whiff of salts/.test(b)), `hp ${h}, tries ${lv0} -> ${await isc('bm.gvlv')}`);
    await sleep(1500); await run('effect clear TestRat');
    await run('damage TestRat 200 minecraft:generic'); await sleep(2500);
    ok('...the same blow without them: knocked out - a try lost', (await isc('bm.gvlv')) === lv0 - 1, `${lv0} -> ${await isc('bm.gvlv')}`);
    await sleep(2000);
    // the void (the Sky Isles): checked by hand
    await heist('isles', 'a', 3); await begin();
    const qi = (await qs('isles'))[0]; await go('isles', qi, 12, 12);
    await run('effect clear TestRat'); await run('clear TestRat');
    await give('smelling_salts', 'weapon.offhand'); await give('smelling_salts');
    const lv1 = await isc('bm.gvlv');
    await at('isles', qi, `tp TestRat ${rel(12, -20, 12)}`);
    await at('isles', qi, 'execute as TestRat at TestRat run function bm:p112/void_ko'); await sleep(500);
    const L = await local('isles', qi);
    ok('Into the Sky Isles\' void, salts in the off hand: back at the door, one vial spent, no try lost',
       (await isc('bm.gvlv')) === lv1 && L && Math.abs(L[0] - 2.5) < 1.5 && Math.abs(L[2] - 12.5) < 1.5 && (await count('smelling_salts')) === 1, JSON.stringify(L));
    ok('...and the salts can\'t leave the vault', fnText('p70/unraid').includes('clear @s *[minecraft:custom_data~{bm_vault:1b}]') && fnText('admin/tier_finds').includes('bm_vault:1b'));
  }

  // ================================================================== THE THIEF'S HOURGLASS
  if (want('hourglass')) {
    await run('function bm:admin/room_gallery'); await heist('guards', 'a', 2); await begin();
    const q = (await qs('gallery'))[0];
    ok('(a heist with the Shooting Gallery)', !!q);
    await run('clear TestRat'); await give('thiefs_hourglass'); await give('thiefs_hourglass');
    await go('gallery', q, 4, 12); await asRat('function bm:p117/hg/use');
    ok('Turned before the clock starts: "no clock running" - the hourglass kept', (await count('thiefs_hourglass')) === 2);
    await go('gallery', q, 12, 12); await sleep(5000);
    const z0 = await sc('gallery', q, 'bm.gvz');
    await asRat('function bm:p117/hg/use');
    const z1 = await sc('gallery', q, 'bm.gvz');
    ok('While the targets pop: 20 seconds more on the clock, one hourglass spent', (await sc('gallery', q, 'bm.gvs')) === 1 && z1 === z0 + 400 && (await count('thiefs_hourglass')) === 1, `${z0} -> ${z1}`);
    await asRat('function bm:p117/hg/use');
    ok('...a second turn in the same room: refused, the hourglass kept', (await sc('gallery', q, 'bm.gvz')) === z1 && (await count('thiefs_hourglass')) === 1);
  }

  // ================================================================== THE ALARM JAMMER
  if (want('jammer')) {
    await heist('levers', 'a', 2); await begin();
    await run('clear TestRat'); await give('alarm_jammer'); await give('alarm_jammer');
    const g = await gi(); const I = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${g}},limit=1]`;
    const ring = () => run(`execute in bm:gutter as ${I} at @s run function bm:p70/alarm`);
    await run('scoreboard players set #add bm.rng 10'); const a0 = await alarm(); await ring(); const a1 = await alarm();
    await asRat('function bm:p117/jam/use');
    const j = await isc('bm.gvjam');
    await run('scoreboard players set #add bm.rng 10'); await ring(); const a2 = await alarm();
    ok('Jammer on: 30 seconds on the clock, and a mistake raises no alarm', a1 > a0 && j > 500 && a2 === a1 && (await count('alarm_jammer')) === 1, `${a0}->${a1}, jam ${j}, ${a2}`);
    await asRat('function bm:p117/jam/use');
    ok('...a second jammer while one hums: refused, kept', (await count('alarm_jammer')) === 1);
    await run(`execute in bm:gutter run scoreboard players set ${I} bm.gvjam 3`); await sleep(600);
    await run('scoreboard players set #add bm.rng 10'); await ring(); const a3 = await alarm();
    ok('...when it splutters out, the alarm works again', (await isc('bm.gvjam')) === 0 && a3 > a2, `${a2} -> ${a3}`);
  }

  // ================================================================== MASTERWORKS
  if (want('mw')) {
    await asRat('function bm:admin/masterworks_reset'); await run('clear TestRat');
    for (const [r, id, sel] of [[1, 'kokiri_sword', 'sharpness'], [2, 'pirate_cutlass', 'fire_aspect'], [3, 'fairy_bow', 'flame'], [4, 'staff_of_sparks', null]]) {
      await run('clear TestRat'); await run(`scoreboard players set TestRat bm.kr${r} 1`);
      await asRat(`function bm:p72/kit/give_${r}`);
      const plain = await has(id) && !/passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}",bm_mw:1b}]`));
      await run(`scoreboard players set TestRat bm.mw${r} 1`); await run('clear TestRat');
      await asRat(`function bm:p72/kit/give_${r}`);
      const mwd = /passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}",bm_mw:1b}]`));
      const named = /passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}",bm_mw:1b},minecraft:enchantment_glint_override=true]`));
      const ench = !sel || /passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}"},minecraft:enchantments~[{enchantments:"minecraft:${sel}"}]]`));
      ok(`Masterwork ${r} (${id}): the plain kit weapon until earned; earned - the kit's own weapon comes gilded and better`, plain && mwd && named && ench);
    }
    // what a Masterwork does in the hand
    await run('clear TestRat'); await run('scoreboard players set TestRat bm.kr1 1'); await asRat('function bm:p72/kit/give_1');
    for (let i = 0; i < 9; i++) await run(`execute if items entity TestRat hotbar.${i} ${ITEM('kokiri_sword')} run item replace entity TestRat weapon.mainhand from entity TestRat hotbar.${i}`);
    await run('item replace entity TestRat armor.chest with minecraft:air'); await run('item replace entity TestRat armor.head with minecraft:air'); await run('item replace entity TestRat armor.legs with minecraft:air'); await run('item replace entity TestRat armor.feet with minecraft:air');
    await run('item replace entity TestRat weapon.offhand with minecraft:air'); await sleep(300);
    ok('...the Tank\'s Kokiri Sword · Masterwork in hand: +4 armour', (await attr('armor')) === 4, `${await attr('armor')}`);
    // earning one: a Tier IV+ win with the kit
    await asRat('function bm:admin/masterworks_reset'); await run('scoreboard players set TestRat bm.gvrole 3'); await run('scoreboard players set #gt bm.rng 4');
    await asRat('function bm:p117/mw/earn');
    ok('A Tier IV win as Ranged: the Fairy Bow\'s Masterwork earned (and in the Codex)', (await num('scoreboard players get TestRat bm.mw3')) === 1 && (await num('scoreboard players get TestRat bm.cx_m3')) === 1 &&
       (await num('scoreboard players get TestRat bm.mw1')) !== 1);
    ok('...earned only at Tier IV and V (the haul checks the tier)', fnText('p70/haul').includes('execute if score #gt bm.rng matches 4.. run function bm:p117/mw/earn'));
    // the Lifebinder: the crew near the Support takes less harm
    await heist('levers', 'a', 2); await begin(); await run('effect clear TestRat'); await run('clear TestRat');
    await run('scoreboard players set TestRat bm.mw4 1'); await run('scoreboard players set TestRat bm.kr4 1'); await asRat('function bm:p72/kit/give_4');
    for (let i = 0; i < 9; i++) await run(`execute if items entity TestRat hotbar.${i} ${ITEM('staff_of_sparks')} run item replace entity TestRat weapon.mainhand from entity TestRat hotbar.${i}`);
    await sleep(1500);
    ok('...the Support\'s Staff of Sparks · Masterwork in hand: Resistance for the crew near it', /resistance/.test(await run('data get entity TestRat active_effects')));
    await asRat('function bm:admin/masterworks_reset');
  }

  // ================================================================== THE CODEX
  if (want('codex')) {
    await asRat('function bm:admin/codex_reset');
    ok('The Office has a Codex button (also on a heist, Leave still last)', fnText('p80/office_dlg').includes('"Codex"') && fnText('p104/office_dlg').includes('"Codex"') &&
       fnText('p104/office_dlg').lastIndexOf('Leave the heist') > fnText('p104/office_dlg').lastIndexOf('"Codex"'));
    await heist('library', 'a', 2); await begin();
    const q = (await qs('library'))[0];
    ok('Not yet near the Library: not in the Codex', (await num('scoreboard players get TestRat bm.cx_r_library')) !== 1);
    await go('library', q, 4, 12); await sleep(800);
    ok('...walk in: The Library is written into the Codex', (await num('scoreboard players get TestRat bm.cx_r_library')) === 1);
    // a cursed room beaten: the curse goes in
    await run('function bm:admin/curse_frost'); await heist('levers', 'a', 2); await begin();
    const ql = (await qs('levers'))[0]; await go('levers', ql, 12, 12); await sleep(300);
    await at('levers', ql, 'function bm:p70/solved'); await sleep(300);
    ok('A Frost-cursed room beaten: FROST goes into the Codex', (await num('scoreboard players get TestRat bm.cx_c2')) === 1);
    await run('function bm:admin/curse_never');
    // the pages
    await run('scoreboard players set TestRat bm.menu 7800');
    const o1 = await asRat('function bm:p117/cx/menu');
    const sv = async k => +(((await run(`data get storage bm:ui ${k}`)).match(/contents: (-?\d+)/) || [0, -1])[1]);
    const n1 = await sv('cx.n1'), n3 = await sv('cx.n3');
    const o2 = await asRat('function bm:p117/cx/page1');
    const e = await run('data get storage bm:ui cxp');
    ok('The Codex page opens (Rooms 1+, Curses 1) and the Rooms page lists the Library by name, the rest as ???',
       !/rror|Unknown/.test(o1 + o2) && n1 >= 1 && n3 === 1 && /The Library/.test(e) && /\?\?\?/.test(e), `${n1} ${n3}`);
    // a full page pays, once
    const t0 = await count('token');
    await run('execute as TestRat at TestRat run function bm:admin/codex_fill'); await sleep(300);
    const t1 = await count('token');
    ok('Every page filled: each section pays once (8 Tokens for the two room pages, a Medallion, a Trophy, a Medallion)',
       t1 - t0 === 8 && [1, 2, 3, 4, 5].every(() => true) && (await num('scoreboard players get TestRat bm.cxr4')) === 1 && (await count('trophy')) >= 1 && (await count('medallion')) >= 2, `${t0} -> ${t1}`);
    await run('execute as TestRat at TestRat run function bm:admin/codex_fill'); await sleep(300);
    ok('...filling again pays nothing more', (await count('token')) === t1);
    await asRat('function bm:admin/codex_reset');
  }

  // ================================================================== EACH TIER'S OWN FINDS
  if (want('finds')) {
    await run('execute in bm:gutter run setblock -200 64 -197 minecraft:barrel'); await run('execute in bm:gutter run setblock -198 64 -197 minecraft:barrel');
    const inBarrel = async id => +(((await run(`execute in bm:gutter store result score #t bm.rng run data get block -200 64 -197 Items`)).match(/(\d+)/) || [0, 0])[1]) &&
      /passed/.test(await run(`execute in bm:gutter if data block -200 64 -197 Items[{components:{"minecraft:custom_data":{bm:"${id}"}}}]`));
    const T = { 1: ['mudlarks_charm', 'songbird', 'merchants_bell'], 2: ['smugglers_veil', 'firefly_jar', 'tinkers_thimble'], 3: ['duelists_ribbon', 'honeycomb_brooch', 'fizzle_stone'],
                4: ['navigators_astrolabe', 'trial_key_fob', 'wayfarers_lodestar'], 5: ['fletchers_charm', 'gale_locket', 'phoenix_plume'] };
    let allOk = true, miss = [];
    for (const t of [1, 2, 3, 4, 5]) for (const [j, kind] of [[0, 'rare'], [1, 'legend'], [2, 'myth']].values()) {
      await run('execute in bm:gutter run data remove block -200 64 -197 Items');
      await run(`scoreboard players set #gt bm.rng ${t}`); await asRat(`function bm:p117/find/${kind}${t}`);
      if (!(await inBarrel(T[t][j]))) { allOk = false; miss.push(T[t][j]); }
    }
    ok('Each tier\'s rare, legendary and mythical find lands in the haul (15 different things)', allOk && new Set(Object.values(T).flat()).size === 15, miss.join(','));
    // half the time the tier's own
    await run('execute in bm:gutter run data remove block -200 64 -197 Items'); await run('execute in bm:gutter run data remove block -198 64 -197 Items');
    await run('scoreboard players set #gt bm.rng 2');
    for (let i = 0; i < 24; i++) await asRat('function bm:p105/find_rare');
    const nf = +(((await run('execute in bm:gutter store result score #t bm.rng if data block -200 64 -197 Items[{components:{"minecraft:custom_data":{bm:"forgeheart"}}}]')).match(/(\d+)/) || [0, 0])[1]);
    const nc = +(((await run('execute in bm:gutter store result score #t bm.rng if data block -200 64 -197 Items[{components:{"minecraft:custom_data":{bm:"smugglers_veil"}}}]')).match(/(\d+)/) || [0, 0])[1]);
    ok(`A rare find at Tier II, 24 times: ${nf} Forgehearts, ${nc} Smuggler's Veils (about half each)`, nf >= 4 && nc >= 4 && nf + nc === 24);
    // the charms
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('tag TestRat remove bm.gvp'); await run('clear TestRat'); await run('effect clear TestRat');
    await sleep(1500);
    for (const [id, a, v] of [['mudlarks_charm', 'movement_efficiency', 1], ['smugglers_veil', 'waypoint_transmit_range', 0], ['duelists_ribbon', 'sweeping_damage_ratio', 1]]) {
      const b = await attr(a); await give(id, 'weapon.offhand'); await sleep(250); const w = await attr(a);
      await run('item replace entity TestRat weapon.offhand with minecraft:air'); await sleep(200);
      ok(`${id} in the off hand: ${a} ${b} -> ${w}`, Math.abs(w - v) < 0.01 && Math.abs((await attr(a)) - b) < 0.01 && Math.abs(b - v) > 0.01);
    }
    // the looks: each runs while held in the off hand
    for (const id of ['songbird', 'firefly_jar', 'honeycomb_brooch', 'trial_key_fob', 'gale_locket']) {
      await give(id, 'weapon.offhand'); await sleep(400);
      const f = fnText('loop/fast').split('\n').find(l => l.includes(`bm:"${id}"`));
      ok(`${id}: its look plays from the off hand`, !!f && /passed|Count|Running/.test(await run(f.replace(/^execute as @a\[gamemode=!spectator\]/, 'execute as TestRat'))));
      await run('item replace entity TestRat weapon.offhand with minecraft:air');
    }
    // the merchant's bell: natural villagers restock, the market's own traders don't; once a day
    await run('clear TestRat'); await give('merchants_bell');
    const offer = '{VillagerData:{profession:"minecraft:farmer",level:2,type:"minecraft:plains"},Xp:20,Offers:{Recipes:[{buy:{id:"minecraft:emerald",count:1},sell:{id:"minecraft:bread",count:3},uses:12,maxUses:12}]},NoAI:1b,Tags:["bm.t115"]}';
    await run('execute in minecraft:overworld run summon minecraft:villager 13003.5 120 13000.5 {VillagerData:{profession:"minecraft:farmer",level:2,type:"minecraft:plains"},Xp:20,Offers:{Recipes:[{buy:{id:"minecraft:emerald",count:1},sell:{id:"minecraft:bread",count:3},uses:12,maxUses:12}]},NoAI:1b}');
    await run(`execute in minecraft:overworld run summon minecraft:villager 13000.5 120 13003.5 ${offer}`);
    await run('scoreboard players reset TestRat bm.mbd'); await asRat('function bm:p117/bell/use');
    const u1 = await num('execute in minecraft:overworld positioned 13000.5 120 13000.5 run data get entity @e[type=minecraft:villager,tag=!bm.t115,distance=..6,limit=1,sort=nearest] Offers.Recipes[0].uses');
    const u2 = await num('execute in minecraft:overworld run data get entity @e[type=minecraft:villager,tag=bm.t115,limit=1] Offers.Recipes[0].uses');
    ok('Merchant\'s Bell: the village trader restocks; a trader of our own is left alone', u1 <= 0 && u2 === 12, `${u1 < 0 ? 0 : u1} / ${u2} (a restocked offer saves no use count)`);
    await run('execute in minecraft:overworld positioned 13000.5 120 13000.5 as @e[type=minecraft:villager,tag=!bm.t115,distance=..6] run data modify entity @s Offers.Recipes[0].uses set value 9');
    await asRat('function bm:p117/bell/use');
    ok('...rung again the same day: it needs its rest', (await num('execute in minecraft:overworld positioned 13000.5 120 13000.5 run data get entity @e[type=minecraft:villager,tag=!bm.t115,distance=..6,limit=1,sort=nearest] Offers.Recipes[0].uses')) === 9);
    await run('execute in minecraft:overworld positioned 13000.5 120 13000.5 run kill @e[type=minecraft:villager,distance=..8]');
    // the fizzle stone
    await run('clear TestRat'); await run('execute in minecraft:overworld run summon minecraft:creeper 13005.5 120 13000.5 {NoAI:1b,Tags:["bm.t115"]}');
    await sleep(600);
    const r0 = await num('execute in minecraft:overworld run data get entity @e[type=minecraft:creeper,tag=bm.t115,limit=1] ExplosionRadius');
    await give('fizzle_stone'); await sleep(700);
    const r1 = await num('execute in minecraft:overworld run data get entity @e[type=minecraft:creeper,tag=bm.t115,limit=1] ExplosionRadius');
    ok('Fizzle Stone: a creeper near you loses its bang (blast radius 3 -> 0)', r0 === 3 && r1 === 0, `${r0} -> ${r1}`);
    await run('kill @e[type=minecraft:creeper,tag=bm.t115]');
    // the astrolabe
    await run('clear TestRat'); await give('navigators_astrolabe', 'weapon.offhand'); A.bars.length = 0; await sleep(800);
    ok('Navigator\'s Astrolabe: where you are, which way you face and the time, above the hotbar', A.bars.some(b => /⌖\s*13000\s+120\s+13000/.test(b) && /(North|South|East|West)/.test(b) && /☀\s*\d+:\d\d/.test(b)), A.bars.slice(-1)[0]);
    await run('item replace entity TestRat weapon.offhand with minecraft:air');
    // the fletcher's charm
    await give('fletchers_charm', 'weapon.offhand');
    const uu = (await run('data get entity TestRat UUID')).match(/\[I; ?(-?\d+), ?(-?\d+), ?(-?\d+), ?(-?\d+)\]/).slice(1).join(',');
    await run(`execute in minecraft:overworld run summon minecraft:arrow 13004.5 125 13000.5 {Motion:[0.0d,0.0d,1.0d],NoGravity:1b,Owner:[I;${uu}],Tags:["bm.t115a"]}`);
    await run('execute in minecraft:overworld run summon minecraft:arrow 13004.5 125 12996.5 {Motion:[0.0d,0.0d,1.0d],NoGravity:1b,Tags:["bm.t115b"]}');
    await sleep(150);
    const ma = await run('execute in minecraft:overworld run data get entity @e[type=minecraft:arrow,tag=bm.t115a,limit=1] Motion[2]');
    const mb = await run('execute in minecraft:overworld run data get entity @e[type=minecraft:arrow,tag=bm.t115b,limit=1] Motion[2]');
    const za = +((ma.match(/: (-?[\d.]+)/) || [0, 0])[1]), zb = +((mb.match(/: (-?[\d.]+)/) || [0, 0])[1]);
    ok('Fletcher\'s Charm: your arrow flies half again as fast; an arrow that isn\'t yours doesn\'t', za > 1.3 && zb < 1.05 && zb > 0.8, `${za} / ${zb}`);
    await run('kill @e[type=minecraft:arrow,tag=bm.t115a]'); await run('kill @e[type=minecraft:arrow,tag=bm.t115b]');
    await run('item replace entity TestRat weapon.offhand with minecraft:air');
    // the thimble
    await run('clear TestRat'); await run('item replace entity TestRat weapon.mainhand with minecraft:iron_sword[minecraft:damage=200]'); await give('tinkers_thimble');
    await sleep(10500);
    const dmg = await num('data get entity TestRat SelectedItem.components."minecraft:damage"');
    ok('Tinker\'s Thimble: the worn sword in hand mends itself (damage 200 down)', dmg >= 0 && dmg < 200, `${dmg}`);
    // the lodestar
    await run('clear TestRat'); await give('wayfarers_lodestar');
    await run('scoreboard players set #wd bm.rng 1'); await asRat('function bm:p117/star/mark');
    await run('execute in minecraft:overworld run tp TestRat 13020.5 120 13000.5'); await run('execute in minecraft:overworld run fill 13018 119 12998 13022 119 13002 stone');
    await run('scoreboard players reset TestRat bm.wlc'); await asRat('function bm:p117/star/use');
    const p1 = await pos();
    await run('execute in minecraft:overworld run tp TestRat 13020.5 120 13000.5'); await asRat('function bm:p117/star/use');
    const p2 = await pos();
    ok('Wayfarer\'s Lodestar: back to the marked spot; again at once - "still finding its bearings"', p1 && Math.abs(p1[0] - 13000.5) < 0.2 && p2 && Math.abs(p2[0] - 13020.5) < 0.2, `${p1} / ${p2}`);
    // the plume
    await run('clear TestRat'); await run('effect clear TestRat'); await give('phoenix_plume', 'weapon.offhand');
    await run('damage TestRat 200 minecraft:generic'); await sleep(800);
    const hp = await num('data get entity TestRat Health');
    ok('Phoenix Plume: a killing blow - you live, the plume burns down to a quill (10 minutes to go)',
       hp > 0 && (await has('phoenix_ash')) && !(await has('phoenix_plume', 'weapon.offhand')) && (await num('scoreboard players get TestRat bm.phx')) > 590);
    await run('scoreboard players set TestRat bm.phx 1'); await sleep(2500);
    ok('...ten minutes on, it blazes back to life', (await has('phoenix_plume')) && !(await has('phoenix_ash')));
    await run('clear TestRat');
  }

  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
