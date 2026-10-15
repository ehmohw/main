// 2.79a: GILDED - as a regular (non-op) player, every step a real packet (rcon sets the stage: coins in the Gutter Bank, the
// Fixer's Lounge, a field, the follower items): the Tailor sells Leo's Golden Champion for 2,560 coins - his page says so, the
// button takes the coins and gives the outfit (and Donado's new Gilded coat is on his page at the same price); the outfit used
// with Leo out - his tabard parts wear it (c4) and gold sparkles reach the client round him; his own clothes back - no
// sparkles. Wilfrey in his Gilded Sun: the sun shield, and his armour turned to gold (golden pieces where he had none); the
// Crimson Cross - his own gear back. Donado's Gilded coat on his rig: torso, arms, legs, head, tail (dnr_*_c5) - not his eyes.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ', G = 'execute in bm:gutter run ';
  const cnt = async (sel, d = O) => { const m = (await run(`${d}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path, d = O) => (await run(`${d}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel, d = O) => { const m = (await run(`${d}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel, d = O) => { const u = await uuidOf(sel, d); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(400); };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const dd = d => d && (d.data || d);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // (the particles that reach the client: what it would draw)
  const parts = []; A.on('world_particles', p => parts.push({ t: Date.now(), p }));
  // (26.3 sends them raw: the particle (type + its data) first, then two flags, then x y z as doubles. The gilded motes are gold
  // dust - its colour 0xFFFFD64C (1.0, 0.84, 0.3) and scale 0.7 - so x sits at byte 11 and z at byte 27.)
  const GOLD = 0xFFFFD64C;
  const gold = e => { const b = e.p.data && Buffer.from(e.p.data.data || e.p.data); return b && b.length >= 35 && b.readUInt32BE(1) === GOLD && Math.abs(b.readFloatBE(5) - 0.7) < 0.01 ? [b.readDoubleBE(11), b.readDoubleBE(27)] : null; };
  const near = (since, pos, r) => parts.filter(e => { if (e.t < since) return false; const g = gold(e); return g && Math.hypot(g[0] - pos[0], g[1] - pos[2]) < r; }).length;
  const epos = async (sel, d = O) => { const m = (await nbt(sel, 'Pos', d)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };

  // ---------------------------------------------------------------- the Tailor (the Lounge's): Leo's Golden Champion, 2,560 coins
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gbc 3000'); await run('scoreboard players set TestRat bm.wuleo 0'); await run('scoreboard players set TestRat bm.cosl 0');
  await run('scoreboard players set TestRat bm.wudon 0'); await run('scoreboard players set TestRat bm.cosdn 0');
  await run('execute as TestRat at @s run function bm:p121/enter'); await sleep(2500);
  const TH = '@e[type=minecraft:interaction,tag=bm.tailhit,x=-321,y=60,z=-257,dx=26,dy=20,dz=26,limit=1]';
  const tp = await epos(TH, G);
  ok('(the Lounge: the Tailor\'s counter)', !!tp, JSON.stringify(tp));
  await run(`${G}tp TestRat ${tp[0]} ${tp[1]} ${tp[2] - 2} 0 0`); await sleep(1200);
  const th = await entOf(TH, G); const n0 = A.dialogN.length; if (th) A.interact(th.entityId); await wait(3000, async () => A.dialogN.length > n0);
  ok('right-clicked, the Tailor: his outfits', A.dialogN.length > n0 && /THE TAILOR/.test(JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).title)));
  let pr = await A.press(/^Leo$/);
  const lp = JSON.stringify(A.dialogN[A.dialogN.length - 1]);
  ok('Leo\'s page: the Golden Champion - 2560 coins', pr && pr.next && A.buttons().some(b => /Golden Champion.*2560 coins/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  pr = await A.press(/Golden Champion/); await sleep(800);
  const wu = await score('bm.wuleo');
  ok('...bought: in Leo\'s wardrobe for good (his 16 bit), 2,560 coins gone from the bank (3000 -> 440)', (Math.floor(wu / 16) % 2) === 1 && (await score('bm.gbc')) === 440, `bank ${await score('bm.gbc')}, wardrobe ${wu}`);
  // (Donado's page: his new Gilded coat at the same price)
  if (th) { const n1 = A.dialogN.length; A.interact(th.entityId); await wait(3000, async () => A.dialogN.length > n1); }
  pr = await A.press(/^Donado$/);
  ok('Donado\'s page: his new Gilded coat - 2560 coins too', pr && A.buttons().some(b => /Gilded.*2560 coins/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  A.write('close_window', { windowId: 0 }); await sleep(300);
  await run(`${G}execute as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~`); await sleep(2500);

  // ---------------------------------------------------------------- Leo in it: gold, and sparkling
  const X = 16760, Y = 100, Z = 16000;
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  for (const t of ['bm.leopet', 'bm.wilfrey', 'bm.donado', 'bm.tupet', 'bm.pmpet']) await run(`${O}kill @e[tag=${t}]`);
  await run(`${O}kill @e[type=minecraft:wither_skeleton,tag=bm.wil_body]`);
  for (const o of ['bm.lecd', 'bm.wlcd', 'bm.coswl', 'bm.wuwil', 'bm.dncd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const kit = ['leo_crest', null, 'wilfrey_locket', 'cos_wil_4', 'cos_wil_1', 'donado_tag', 'cos_don_5'];
  for (let i = 0; i < kit.length; i++) if (kit[i]) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await run('item replace entity TestRat hotbar.1 from entity TestRat inventory.0'); await run(`clear TestRat *[minecraft:custom_data~{bm:"cos_leo_4"}]`);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/cos_leo_4');                 // (the outfit as an item, as a raid or an admin gives it)
  const lore = await run('data get entity TestRat Inventory[{Slot:1b}].components."minecraft:lore"');
  ok('the item says what it is: polished gold that sparkles, the Tailor\'s dearest', /polished gold/.test(lore) && /2,560 coins/.test(lore), lore.replace(/^.*?data: /, '').slice(0, 160));
  await run('scoreboard players set TestRat bm.wuleo 0');                                    // (not in his wardrobe yet: the item puts it there)
  await use(0); await wait(5000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1); await sleep(2000);
  ok('Leo called with his Crest', (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1);
  await sleep(2300); await use(1); await sleep(1200);
  ok('the Golden Champion used: his for good, and on (bm.cosl 4)', (await score('bm.cosl')) === 4 && (await has('cos_leo_4')) === 0, `${await score('bm.cosl')}`);
  const LB = '@e[type=minecraft:item_display,tag=bm.lep,tag=bm.lp_body,limit=1]';
  ok('...his tabard wears it (his body part: the c4 look)', /"c4"/.test(await nbt(LB, 'item.components."minecraft:custom_model_data"')), await nbt(LB, 'item.components."minecraft:custom_model_data"'));
  let lpos = await epos('@e[type=minecraft:wolf,tag=bm.leopet,limit=1]'); let t0 = Date.now(); await sleep(3000);
  const sp1 = near(t0, lpos, 3);
  ok('...and gold sparkles round him reach the client (gold motes)', sp1 >= 6, `${sp1} gold motes in 3 s (${parts.filter(e => e.t >= t0).length} particles in all)`);
  // his own clothes again: no sparkles
  await run('scoreboard players set TestRat bm.cosl 0'); await run('execute as TestRat at @s run function bm:p99/leo_now'); await sleep(800);
  lpos = await epos('@e[type=minecraft:wolf,tag=bm.leopet,limit=1]'); t0 = Date.now(); await sleep(3000);
  ok('in his own clothes: no sparkles', near(t0, lpos, 3) === 0, `${near(t0, lpos, 3)}`);
  await run(`${O}kill @e[tag=bm.leopet]`);

  // ---------------------------------------------------------------- Wilfrey in the Gilded Sun: gold
  await sleep(2300); await hold(3); await sleep(800);                                        // (the Gilded Sun, picked while he rests)
  await hold(2); await wait(5000, async () => (await cnt('@e[type=minecraft:wither_skeleton,tag=bm.wil_body]')) >= 1); await sleep(2000);
  const WB = '@e[type=minecraft:wither_skeleton,tag=bm.wil_body,limit=1]';
  const ch = await nbt(WB, 'equipment.chest'), sh = await nbt(WB, 'equipment.offhand');
  ok('Wilfrey comes in the Gilded Sun: the sun shield, shining', /shield/.test(sh) && /circle/.test(sh) && /glint/.test(sh), sh.slice(0, 160));
  ok('...his armour turned to gold (a golden piece where he had none; gold to look at)', /golden_chestplate/.test(ch) && /asset_id: "minecraft:gold"/.test(ch), ch.slice(0, 200));
  await sleep(2300); await hold(4); await sleep(1500);
  const ch2 = await nbt(WB, 'equipment.chest'), sh2 = await nbt(WB, 'equipment.offhand');
  ok('the Crimson Cross: his own gear back (no gold), a red shield', !/gold/.test(ch2) && /red/.test(sh2), `${ch2.slice(0, 120)} | ${sh2.slice(0, 80)}`);
  await run(`${O}kill @e[tag=bm.wilfrey]`); await run(`${O}kill @e[type=minecraft:wither_skeleton,tag=bm.wil_body]`);

  // ---------------------------------------------------------------- Donado's Gilded coat (his new fifth look)
  await sleep(2300); await use(5); await wait(5000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.donado]')) === 1); await sleep(2000);
  ok('Donado called with his tag (and rigged)', (await cnt('@e[type=minecraft:wolf,tag=bm.donado,tag=bm.rigged]')) === 1);
  await sleep(2300); await use(6); await sleep(1500);
  const part = async t => nbt(`@e[type=minecraft:item_display,tag=${t},limit=1]`, 'item.components."minecraft:item_model"');
  const dt = await part('bm.dnr_torso'), dh = await part('bm.dnr_head'), de = await part('bm.dnr_eyes');
  ok('Donado\'s Gilded coat: his rig wears it (torso and head _c5; his eyes his own)', (await score('bm.cosdn')) === 5 && /dnr_torso_c5/.test(dt) && /dnr_head_\w+_c5/.test(dh) && /"bm:dnr_eyes"/.test(de),
     `cosdn ${await score('bm.cosdn')}, ${dt} ${dh} ${de}`);
  // (back in his own coat: the plain parts)
  await run('scoreboard players set TestRat bm.cosdn 0'); await run('execute as TestRat at @s run function bm:p99/don_now'); await sleep(800);
  ok('...his own coat again: plain parts', /"bm:dnr_torso"/.test(await part('bm.dnr_torso')), await part('bm.dnr_torso'));
  await run(`${O}kill @e[tag=bm.donado]`);
  await run('clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
