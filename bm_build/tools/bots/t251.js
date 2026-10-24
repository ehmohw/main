// 2.91: THE NETHER AND THE END - as a regular (non-op) player, every click and every use a real packet (rcon sets the stage: floors,
// the places built by their admin functions, the items, an event started and its clock run down, a boss struck down).
// THE NETHER: the Ember Rat's Outpost (a rat who stays, Hellstars and Heartstones in his stock); an ERUPTION (the title and bar,
// lava bombs round you - none in the outpost, whose walls lend Fire Resistance - and its end pays Ember Scales and a Hellstar);
// a Hellstar falling during it; one used (Fire Resistance, Strength); nine knotted into an Ember Mantle (sneaking), whose flame
// nova burns the thing that hurt you; a Hellstar and a Heartstone dropped together in the Nether: an Emberheart, eaten (+1 attack).
// The Colossus's Forge: the cold anvil explains itself; refuses an empty hand; a Smouldering Idol wakes the Magma Colossus; he
// falls - the forge burns, the spoils; a worn sword tempered unbreakable (2 Hellstars).
// THE END: the Void Rat's Outpost (Voidstars in stock) and its rift anchor (a fall into the void, caught); a VOID STORM (title,
// the heave of gravity, a rift - through it for a Void Shard; its end pays Void Shards and a Voidstar); a Voidstar's blink; the
// Void Mantle (nine, sneaking) - out of the void, set down where you last stood; a Voidstar and a Heartstone in the End: a
// Voidheart (+1 reach). The Observatory: the Starless Eye taken (once), the telescope (a Voidstar comes down; not twice a day),
// the Voidwalker called (3 Voidstars) and beaten there - the spoils. The three mantles dropped together: the Mantle of Three Skies.
// CHESTS: bastion treasure chests now hold Ember Scales.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const N = 'execute in minecraft:the_nether run ', E = 'execute in minecraft:the_end run ';
  const cnt = async (sel, D = N) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path, D = N) => (await run(`${D}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const effects = async () => await run('data get entity TestRat active_effects');
  const uuidOf = async (sel, D) => { const m = (await run(`${D}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel, D) => { const u = await uuidOf(sel, D); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (D, x, y, z, yaw = 0, pitch = 0) => { await run(`${D}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(3000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); };
  const click = async (sel, D, sneak = false) => { await wait(3000, async () => !!(await entOf(sel, D))); const e = await entOf(sel, D); if (!e) return false;
    if (sneak) { A.input({ shift: true }); await sleep(800); } A.interact(e.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true; };
  const use = async (slot, sneak = false, ms = 400) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(250); } A.use(); await sleep(ms); A.release(); if (sneak) { A.input({}); await sleep(200); } await sleep(300); };
  const give = async (slot, iid, n = 1) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); if (n > 1) await run(`item modify entity TestRat hotbar.${slot} {type:"minecraft:set_count",count:${n}}`); await sleep(300); };
  const said = (re) => A.chats.some(c => re.test(c)) || A.bars.some(c => re.test(c)) || A.titles.some(c => re.test(c));
  const floor = async (D, x, y, z, r, h = 8) => { await run(`${D}fill ${x - r} ${y} ${z - r} ${x + r} ${y} ${z + r} minecraft:netherrack`); await run(`${D}fill ${x - r} ${y + 1} ${z - r} ${x + r} ${y + h} ${z + r} minecraft:air`); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1500 4 true'); await run('effect give TestRat minecraft:saturation 1500 0 true');
  for (const o of ['bm.ehrt', 'bm.vhrt', 'bm.gaze', 'bm.veye', 'bm.mtcd']) await run(`scoreboard players reset TestRat ${o}`);
  await run('attribute TestRat minecraft:attack_damage modifier remove bm:emberheart_attack_damage');
  await run('attribute TestRat minecraft:block_interaction_range modifier remove bm:voidheart_block_interaction_range');
  await run('attribute TestRat minecraft:entity_interaction_range modifier remove bm:voidheart_entity_interaction_range');
  await run('scoreboard players set #eru bm.bm 0'); await run('scoreboard players set #vst bm.bm 0');
  await run('scoreboard players set #erucd bm.bm 99999'); await run('scoreboard players set #vstcd bm.bm 99999');        // (no event of its own accord mid-test)

  // ================================================================ THE NETHER
  const NX = 6000, NY = 70, NZ = 6000;
  await run(`${N}forceload add ${NX - 40} ${NZ - 40} ${NX + 120} ${NZ + 40}`);
  await run(`${N}kill @e[type=!minecraft:player,x=${NX},y=${NY},z=${NZ},distance=..140]`);
  await floor(N, NX, NY - 1, NZ, 30, 16);
  await run(`${N}execute positioned ${NX} ${NY} ${NZ} run function bm:admin/ember_outpost`); await sleep(1500);
  const RAT = `@e[type=minecraft:wandering_trader,tag=bm.orat_ember,x=${NX},y=${NY},z=${NZ},distance=..30,limit=1]`;
  const sells = async (sel, D) => { let out = ''; for (let i = 1; i <= 8; i++) out += await nbt(sel, `Offers.Recipes[-${i}].sell.components."minecraft:custom_data".bm`, D); return out; };
  const stock = await sells(RAT, N);
  ok('the Ember Rat\'s Outpost: its rat stays (no packing up), Hellstars, Heartstones and the Smouldering Idol in his stock',
     (await cnt(`@e[type=minecraft:marker,tag=bm.outpost_ember,x=${NX},y=${NY},z=${NZ},distance=..30]`)) === 1 && /hellstar/.test(stock) && /heartstone/.test(stock) &&
     /sum_colossus/.test(stock) && !/bm.field_rat/.test(await nbt(RAT, 'Tags')), stock.replace(/[^a-z_ ]/g, ' ').replace(/\s+/g, ' ').slice(0, 120));
  // an Eruption
  await at(N, NX + 0.5, NY, NZ + 0.5);
  A.titles.length = 0; await run('function bm:admin/eruption'); await sleep(1500);
  ok('an ERUPTION: the title, its bar', said(/ERUPTION/), A.titles.join(' | '));
  await sleep(5000);
  ok('...inside the outpost: no bombs round you, Fire Resistance from its walls', (await cnt(`@e[type=minecraft:marker,tag=bm.lbomb,x=${NX},y=${NY},z=${NZ},distance=..14]`)) === 0 &&
     /fire_resistance/.test(await effects()));
  await floor(N, NX + 60, NY - 1, NZ, 20, 10);
  await at(N, NX + 60.5, NY, NZ + 0.5);
  ok('...out in the open: lava bombs come down round you (the rings)', await wait(20000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.lbomb,x=${NX + 60},y=${NY},z=${NZ},distance=..16]`)) > 0));
  ok('...a Hellstar falls nearby (glowing where it lands)', await wait(60000, async () => (await cnt(`@e[type=minecraft:item,tag=bm.hstar,x=${NX + 60},y=${NY},z=${NZ},distance=..40]`)) > 0, 500));
  const sc0 = await has('ember_scale'), hs0 = await has('hellstar');
  A.titles.length = 0; await run('scoreboard players set TestRat bm.erus 200'); await run('scoreboard players set #eru bm.bm 2'); await sleep(3500);   // (the stage: the four minutes ridden out - 2.94k needs half of it)
  ok('the Eruption ends: you rode it out - Ember Scales and a Hellstar', said(/Eruption ends/) && (await has('ember_scale')) >= sc0 + 4 && (await has('hellstar')) === hs0 + 1,
     `scales +${(await has('ember_scale')) - sc0}`);
  await run(`${N}kill @e[type=minecraft:item,x=${NX + 60},y=${NY},z=${NZ},distance=..40]`); await run(`${N}kill @e[type=minecraft:magma_cube,tag=bm.erumob]`);
  await run('scoreboard players set #erucd bm.bm 99999');
  // a Hellstar used; nine knotted; the Ember Mantle's nova
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 1500 4 true'); await run('effect give TestRat minecraft:saturation 1500 0 true');
  await give(0, 'hellstar', 10);
  await use(0);
  ok('a Hellstar used: Fire Resistance and Strength (one spent)', /fire_resistance/.test(await effects()) && /strength/.test(await effects()) && (await has('hellstar')) === 9);
  await use(0, true);
  ok('sneak + use with nine: the Ember Mantle', (await has('ember_mantle')) === 1 && (await has('hellstar')) === 0);
  await at(N, NX + 60.5, NY, NZ + 0.5); await sleep(3500);
  await run(`${N}summon minecraft:zombie ${NX + 62.5} ${NY} ${NZ + 0.5} {Tags:["bm.t251z"],NoAI:1b,PersistenceRequired:1b}`); await sleep(500);
  const zh0 = +((await nbt('@e[tag=bm.t251z,limit=1]', 'Health')).match(/[\d.]+/) || [0])[0];
  await run(`${N}execute as TestRat run damage @s 1 minecraft:mob_attack by @e[tag=bm.t251z,limit=1]`); await sleep(600);
  const zh1 = +((await nbt('@e[tag=bm.t251z,limit=1]', 'Health')).match(/[\d.]+/) || [0])[0];
  if (!(zh1 < zh0)) console.log('  (nova: ' + [await effects(), await run('scoreboard players get TestRat bm.mtcd'), await run('time query gametime'),
                                   await run('advancement test TestRat bm:p200/hurt'), await run('data get entity TestRat Health'),
                                   await run(`execute as @e[tag=bm.t251z] run data get entity @s Pos`)].join(' | ') + ')');
  ok('...hurt, carrying it: a flame nova - the zombie beside you burned', zh1 < zh0 && +((await nbt('@e[tag=bm.t251z,limit=1]', 'Fire')).match(/-?\d+/) || [0])[0] > 0, `${zh0} -> ${zh1}`);
  await run(`${N}kill @e[tag=bm.t251z]`);
  // the Emberheart, forged on the ground in the Nether
  await give(1, 'hellstar'); await give(2, 'heartstone');
  await at(N, NX + 60.5, NY, NZ + 0.5, 0, 70);
  A.slot(1); await sleep(250); A.drop(); await sleep(300); A.slot(2); await sleep(250); A.drop(); await sleep(500);
  ok('a Hellstar and a Heartstone dropped together in the Nether: an Emberheart forged on the ground',
     await wait(12000, async () => (await cnt(`@e[type=minecraft:item,x=${NX + 60},y=${NY},z=${NZ},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"emberheart"}}}}]`)) === 1));
  await wait(5000, async () => (await has('emberheart')) === 1);
  for (let s = 0; s < 9; s++) { if (/emberheart/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}]`))) { await use(s, false, 2200); break; } }
  ok('...eaten: +1 attack damage, for good', (await score('bm.ehrt')) === 1 && /1\.0|1d/.test(await run('attribute TestRat minecraft:attack_damage modifier value get bm:emberheart_attack_damage')));

  // ---- the Colossus's Forge
  const FX = NX + 60, FY0 = NY, FZ = NZ + 0;
  await run(`${N}kill @e[type=!minecraft:player,x=${FX},y=${FY0},z=${FZ},distance=..40]`);
  await run(`${N}execute positioned ${FX} ${FY0} ${FZ} run function bm:admin/colossus_forge`); await sleep(1500);
  const ANV = `@e[type=minecraft:interaction,tag=bm.fanvil,x=${FX},y=${FY0},z=${FZ},distance=..40,limit=1]`;
  ok('the Colossus\'s Forge is built: its Great Anvil (a click-box)', (await cnt(ANV)) === 1);
  const ap = (await nbt(ANV, 'Pos')).match(/(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d/);
  await at(N, +ap[1], +ap[2] + 0.2, +ap[3] - 2.2, 0, 20);
  A.chats.length = 0; await click(ANV, N);
  ok('the cold anvil: how to wake him', said(/is cold/) && said(/Smouldering Idol/));
  await run('clear TestRat'); A.slot(0); await sleep(200);
  A.bars.length = 0; await click(ANV, N, true);
  ok('...sneak + right-click empty-handed: it wants an Idol (or 32 scales)', said(/wants a Smouldering Idol/));
  await give(0, 'sum_colossus'); A.slot(0); await sleep(200);
  A.titles.length = 0; await click(ANV, N, true); await sleep(1500);
  ok('...with a Smouldering Idol in hand: the Magma Colossus rises in the Forge Heart (the Idol spent)', (await cnt(`@e[type=minecraft:magma_cube,tag=bm.mcol,x=${FX},y=${FY0},z=${FZ},distance=..60]`)) >= 1 &&
     (await has('sum_colossus')) === 0 && said(/forge stirs/));
  const hsF = await has('hellstar');
  await sleep(4500); await run(`${N}kill @e[type=minecraft:magma_cube,tag=bm.mcol]`); await sleep(500); await run(`${N}kill @e[type=minecraft:magma_cube,x=${FX},y=${FY0},z=${FZ},distance=..60]`);
  ok('he falls at his forge: the forge burns again, the spoils (Hellstars, a Heartstone)', await wait(5000, async () => (await score('bm.fst', `@e[type=minecraft:marker,tag=bm.forge,limit=1]`)) === 1) &&
     (await has('hellstar')) >= hsF + 2 && (await has('heartstone')) >= 1);
  await run('item replace entity TestRat hotbar.8 with minecraft:iron_sword[minecraft:damage=100]'); A.slot(8); await sleep(300);
  A.bars.length = 0; await click(ANV, N); await sleep(300);
  ok('a worn sword at the lit anvil (2 Hellstars on you): tempered - unbreakable', /passed/i.test(await run('execute if items entity TestRat weapon.mainhand minecraft:iron_sword[minecraft:unbreakable]')) &&
     said(/never break/), A.bars.slice(-1).join(''));

  // ================================================================ THE END
  const EX = 3000, EY = 70, EZ = 3000;
  await run(`${E}forceload add ${EX - 40} ${EZ - 40} ${EX + 120} ${EZ + 40}`);
  await run(`${E}kill @e[type=!minecraft:player,x=${EX},y=${EY},z=${EZ},distance=..140]`);
  await run(`${E}execute positioned ${EX} ${EY} ${EZ} run function bm:admin/void_outpost`); await sleep(1500);
  const VRAT = `@e[type=minecraft:wandering_trader,tag=bm.orat_void,x=${EX},y=${EY},z=${EZ},distance=..30,limit=1]`;
  const vstock = await sells(VRAT, E);
  ok('the Void Rat\'s Outpost: its rat stays, Voidstars and the Starless Eye in his stock', /voidstar/.test(vstock) && /sum_voidwalker/.test(vstock));
  await run('clear TestRat');
  await at(E, EX + 0.5, EY, EZ + 0.5);
  await at(E, EX + 20.5, -10, EZ + 0.5);
  ok('a fall into the void near it: the rift anchor catches you, back at the outpost', await wait(4000, async () => A.pos && A.pos.y > EY - 5 && Math.abs(A.pos.x - EX) < 4), A.pos ? `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)}` : '');
  // a Void Storm (out on a platform of its own)
  const SX0 = EX + 60;
  await run(`${E}fill ${SX0 - 14} ${EY - 1} ${EZ - 14} ${SX0 + 14} ${EY - 1} ${EZ + 14} minecraft:end_stone`);
  await at(E, SX0 + 0.5, EY, EZ + 0.5);
  A.titles.length = 0; await run('function bm:admin/voidstorm'); await sleep(1500);
  ok('a VOID STORM: the title', said(/VOID STORM/), A.titles.join(' | '));
  await run('scoreboard players set #vst bm.bm 22');
  ok('...gravity heaves (you\'re lifted, then let down slowly)', await wait(6000, async () => { const e = await effects(); return /levitation/.test(e) && /slow_falling/.test(e); }));
  await at(E, SX0 + 0.5, EY, EZ + 0.5);
  await run('scoreboard players set #vst bm.bm 200');
  let riftSeen = false, through = false;
  for (let k = 0; k < 3 && !through; k++) {
    await at(E, SX0 + 0.5, EY, EZ + 0.5);
    if (!(await wait(45000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.vrift,x=${SX0},y=${EY},z=${EZ},distance=..20]`, E)) > 0, 500))) continue;
    riftSeen = true;
    const rp = (await nbt(`@e[type=minecraft:marker,tag=bm.vrift,x=${SX0},y=${EY},z=${EZ},distance=..20,limit=1]`, 'Pos', E)).match(/(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d/);
    const vs0 = await has('void_shard');
    if (rp) await run(`${E}tp TestRat ${rp[1]} ${rp[2]} ${rp[3]}`);
    through = (await wait(3000, async () => (await has('void_shard')) >= vs0 + 1)) && /slow_falling/.test(await effects());
  }
  ok('...a rift tears open near you', riftSeen);
  ok('...stepped through it: a Void Shard, and a long fall (slow)', through);
  await at(E, SX0 + 0.5, EY, EZ + 0.5);
  await run(`${E}kill @e[type=minecraft:endermite,tag=bm.riftmite]`);
  await run('scoreboard players set TestRat bm.vsts 200');                 // (the stage: through the storm - 2.94k needs half of it)
  A.titles.length = 0; await run('scoreboard players set #vst bm.bm 2'); await sleep(3500);
  ok('the storm passes: Void Shards and a Voidstar', said(/Void Storm passes/) && (await has('voidstar')) >= 1);
  await run('scoreboard players set #vstcd bm.bm 99999');
  // the Voidstar's blink; the Void Mantle
  await run(`${E}kill @e[type=minecraft:item,x=${SX0},y=${EY},z=${EZ},distance=..30]`);
  await run('clear TestRat'); await give(0, 'voidstar', 10);
  await at(E, SX0 - 10.5, EY, EZ + 0.5, -90, 0);
  const bx0 = A.pos.x;
  await use(0);
  ok('a Voidstar used: a Void Blink - you\'re carried along where you look', await wait(2000, async () => A.pos.x > bx0 + 5) && (await has('voidstar')) === 9, `x ${bx0.toFixed(1)} -> ${A.pos.x.toFixed(1)}`);
  await use(0, true);
  ok('sneak + use with nine: the Void Mantle', (await has('void_mantle')) === 1);
  await at(E, SX0 + 3.5, EY, EZ + 3.5); await sleep(2500);
  await at(E, SX0 + 40.5, -20, EZ + 0.5);
  ok('...out of the End with it: the void gives you back - set down where you last stood', await wait(4000, async () => A.pos && A.pos.y >= EY - 1 && Math.abs(A.pos.x - (SX0 + 3.5)) < 2),
     A.pos ? `${A.pos.x.toFixed(1)} ${A.pos.y.toFixed(1)}` : '');
  // the Voidheart
  await give(1, 'voidstar'); await give(2, 'heartstone');
  await at(E, SX0 + 0.5, EY, EZ + 0.5, 0, 70);
  A.slot(1); await sleep(250); A.drop(); await sleep(300); A.slot(2); await sleep(250); A.drop(); await sleep(500);
  ok('a Voidstar and a Heartstone dropped together in the End: a Voidheart', await wait(12000, async () => (await cnt(`@e[type=minecraft:item,x=${SX0},y=${EY},z=${EZ},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"voidheart"}}}}]`, E)) === 1));
  await wait(5000, async () => (await has('voidheart')) === 1);
  for (let s = 0; s < 9; s++) { if (/voidheart/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}]`))) { await use(s, false, 2200); break; } }
  ok('...eaten: +1 reach, for good', (await score('bm.vhrt')) === 1 && /1\.0|1d/.test(await run('attribute TestRat minecraft:block_interaction_range modifier value get bm:voidheart_block_interaction_range')));

  // ---- the Observatory
  const OX = EX + 100;
  await run(`${E}execute positioned ${OX} ${EY} ${EZ} run function bm:admin/observatory`); await sleep(1500);
  const EYE = `@e[type=minecraft:interaction,tag=bm.veyebox,x=${OX},y=${EY},z=${EZ},distance=..30,limit=1]`;
  const SCOPE = `@e[type=minecraft:interaction,tag=bm.vscopebox,x=${OX},y=${EY},z=${EZ},distance=..30,limit=1]`;
  ok('the Voidwalker\'s Observatory, adrift: its pedestal (the Starless Eye on it) and its telescope', (await cnt(EYE, E)) === 1 && (await cnt(SCOPE, E)) === 1 &&
     (await cnt(`@e[type=minecraft:item_display,tag=bm.veyed,x=${OX},y=${EY},z=${EZ},distance=..30]`, E)) === 1);
  const ep = (await nbt(EYE, 'Pos', E)).match(/(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d/);
  await run('clear TestRat');
  await at(E, +ep[1] + 2.5, +ep[2] - 1, +ep[3], 90, 25);
  A.chats.length = 0; await click(EYE, E);
  ok('the pedestal: you take the Starless Eye', (await has('sum_voidwalker')) === 1 && said(/Starless Eye/));
  A.chats.length = 0; await click(EYE, E);
  ok('...again: no second Eye (that one\'s for the next stargazer)', (await has('sum_voidwalker')) === 1 && said(/next stargazer/));
  const sp = (await nbt(SCOPE, 'Pos', E)).match(/(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d/);
  await at(E, +sp[1] - 1.8, +sp[2], +sp[3], -90, 10);
  const vg0 = await has('voidstar');
  A.chats.length = 0; await click(SCOPE, E); await sleep(1500);
  ok('the telescope: a Voidstar comes down beside you (and into your hand)', said(/star breaks loose/) &&
     ((await cnt(`@e[type=minecraft:item,tag=bm.vstar,x=${OX},y=${EY},z=${EZ},distance=..20]`, E)) >= 1 || (await has('voidstar')) > vg0));
  A.bars.length = 0; await click(SCOPE, E);
  ok('...not twice in a day', said(/Come back tomorrow/));
  await run(`${E}kill @e[type=minecraft:item,x=${OX},y=${EY},z=${EZ},distance=..30]`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"voidstar"}]'); await give(0, 'voidstar', 3);
  await at(E, +ep[1] + 2.5, +ep[2] - 1, +ep[3], 90, 25);
  A.titles.length = 0; A.bars.length = 0; await click(EYE, E, true); await sleep(1500);
  ok('sneak + right-click the pedestal with 3 Voidstars: the Voidwalker comes to his observatory', await wait(15000, async () => (await cnt(`@e[type=minecraft:enderman,tag=bm.vwk,x=${OX},y=${EY},z=${EZ},distance=..200]`, E)) === 1) &&
     (await has('voidstar')) === 0);
  await sleep(4500); await run(`${E}kill @e[type=minecraft:enderman,tag=bm.vwk]`);
  ok('...beaten there: Voidstars and a Heartstone', await wait(5000, async () => (await has('voidstar')) >= 2 && (await has('heartstone')) >= 1));
  await run(`${E}kill @e[type=minecraft:endermite,x=${OX},y=${EY},z=${EZ},distance=..60]`); await run(`${E}kill @e[type=minecraft:enderman,x=${OX},y=${EY},z=${EZ},distance=..60]`);

  // ---- the Mantle of Three Skies
  await run('clear TestRat'); await give(0, 'star_cloak'); await give(1, 'ember_mantle'); await give(2, 'void_mantle');
  await at(E, SX0 + 0.5, EY, EZ + 0.5, 0, 70);
  for (const s of [0, 1, 2]) { A.slot(s); await sleep(250); A.drop(); await sleep(300); }
  ok('the Star Cloak, the Ember Mantle and the Void Mantle dropped together: the Mantle of Three Skies',
     await wait(12000, async () => (await cnt(`@e[type=minecraft:item,x=${SX0},y=${EY},z=${EZ},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"three_skies_mantle"}}}}]`, E)) === 1));

  // ================================================================ chests: bastion treasure with Ember Scales
  await run('clear TestRat');
  const CX0 = NX + 4;
  await at(N, CX0 + 0.5, NY, NZ + 3.5, 0, 50);
  let found = 0;
  for (let k = 0; k < 5; k++) {
    const sc = await has('ember_scale');
    await run(`${N}setblock ${CX0} ${NY} ${NZ + 5} minecraft:chest{LootTable:"minecraft:chests/bastion_treasure"}`); await sleep(300);
    A.useOn(CX0, NY, NZ + 5, 2); await sleep(900);
    for (const w of A.windows.splice(0)) A.close(w.windowId);
    if ((await has('ember_scale')) > sc) found++;
    await run(`${N}setblock ${CX0} ${NY} ${NZ + 5} minecraft:air`);
  }
  ok('bastion treasure chests opened (five): Ember Scales among the loot', found >= 1, `${found}/5 had scales`);

  // ---- tidy up
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('attribute TestRat minecraft:attack_damage modifier remove bm:emberheart_attack_damage');
  await run('attribute TestRat minecraft:block_interaction_range modifier remove bm:voidheart_block_interaction_range');
  await run('attribute TestRat minecraft:entity_interaction_range modifier remove bm:voidheart_entity_interaction_range');
  for (const o of ['bm.ehrt', 'bm.vhrt']) await run(`scoreboard players reset TestRat ${o}`);
  await run(`${N}kill @e[type=!minecraft:player,x=${NX},y=${NY},z=${NZ},distance=..140]`); await run(`${E}kill @e[type=!minecraft:player,x=${EX},y=${EY},z=${EZ},distance=..140]`);
  await run('scoreboard players set #erucd bm.bm 0'); await run('scoreboard players set #vstcd bm.bm 0');
  await run('execute in minecraft:overworld run tp TestRat 0 120 0');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
