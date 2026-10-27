// 2.84c: the armour rebalance's re-sync, the Partner Wheel and the alien gear - as a regular (non-op) player.
//   the re-sync: an old (item version 40) Crimson Revenant Ribcage with a Dread tuning and an auction infusion comes back
//     re-synced - the rebalance's toughness and health on it - and keeps its tuning and its infusion.
//   the Partner Wheel: Emma's Ribbon in the off hand + use the wheel: it goes on. Use the wheel: its page has Call Emma;
//     called, she stays (the ribbon is on the wheel, not in a pocket); Send Emma home; Take the item back gives the ribbon
//     back. On again, called again - and when the wheel is dropped, she goes home.
//   Zorp: his stock has the Xenoplate and the Donadian blades; in hard mode the Vorn Warplate too; a Xenoplate Helm bought
//     through his window.
//   the gear: the Plasma Cutter sets a zombie alight and glowing; full Xenoplate: Jump Boost and the Deflector's shield;
//     full Warplate under a third of your health: the Shockwave hurts a zombie beside you.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)(?!.*\d)/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/.test(await run(c));
  const effects = async () => run('data get entity TestRat active_effects');
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const press = async (re) => { const b = await A.press(re); await sleep(700); return b; };
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const hard0 = await sc('#hard', 'bm.cfg');

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('weather clear');                                   // (rain puts the Plasma Cutter's fire out)
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 4} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await sleep(1200); A.stand();

  // ================================================================== 1. the re-sync keeps a tuning and an infusion
  await run('item replace entity TestRat hotbar.4 with minecraft:netherite_chestplate[custom_data={bm:"crimson_chestplate",bmv:1,bm_tune:{hp:1,n:1},bm_inf:"vitality"},' +
            'attribute_modifiers=[{type:"minecraft:armor",id:"minecraft:armor.chestplate",amount:8.0,operation:"add_value",slot:"chest"},' +
            '{type:"minecraft:max_health",id:"bm:tune_hp_1",amount:1.0,operation:"add_value",slot:"chest"}]]');
  const slot4 = () => run('data get entity TestRat Inventory[{Slot:4b}]');
  ok('An old Crimson Ribcage (tuned, infused) is re-synced', await wait(4000, async () => +((await slot4()).match(/bmv: (\d+)/) || [0, 0])[1] > 1), (await slot4()).slice(0, 160));
  const s4 = await slot4();
  ok('...with the rebalance on it (+1 toughness, +4 health in all)', /bm:rb_tough_chestplate/.test(s4) && /bm:rb_hp_chestplate/.test(s4) && /\+4 Max Health, \+1 Toughness/.test(s4));
  ok('...and its Dread tuning kept (the modifier and the record)', /bm:tune_hp_1/.test(s4) && /bm_tune: \{/.test(s4) && /n: 1/.test(s4));
  ok('...and its infusion kept (the mark and the line)', /bm_inf: "vitality"/.test(s4) && /Infused: Vitality/.test(s4));
  await run('clear TestRat');

  // ================================================================== 2. the Partner Wheel
  await run('scoreboard players set TestRat bm.emcd 0'); await run('scoreboard players set TestRat bm.pw0 0');
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.emmapet] run function bm:p62/emma_go`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); await run('loot replace entity TestRat weapon.offhand loot bm:items/emma_ribbon');
  A.slot(0); await sleep(500);
  await A.useWait(1500);
  ok('Emma\'s Ribbon in the off hand + use the wheel: it goes on', (await has('emma_ribbon')) === 0 && (await sc('TestRat', 'bm.pw0')) === 1, `${await has('emma_ribbon')} ribbons, pw0 ${await sc('TestRat', 'bm.pw0')}`);
  const emma = `@e[type=minecraft:cat,tag=bm.emmapet,x=${X},y=${Y},z=${Z},distance=..20]`;
  await A.useWait(1500);
  ok('Use the wheel: its page offers Call Emma (and only partners on it)', A.buttons().some(b => /Call Emma/.test(b.label)) && !A.buttons().some(b => /Leo|Cecil/.test(b.label)),
     A.buttons().map(b => b.label).join(' | '));
  ok('...beside her name, her summoning item\'s own icon (Emma\'s Ribbon, an inline sprite from the items atlas)',
     /"sprite":\{[^}]*"value":"bm:item\/emma_ribbon"/.test(A.dialogs[A.dialogs.length - 1]) || /bm:item\/emma_ribbon/.test(A.dialogs[A.dialogs.length - 1]), (A.dialogs[A.dialogs.length - 1] || '').slice(0, 200));
  await press(/Call Emma/);
  ok('...Call Emma: she comes', await wait(4000, async () => passes(`${O}execute if entity ${emma}`)));
  await sleep(5000);
  ok('...and stays (the ribbon is on the wheel, not in a pocket)', await passes(`${O}execute if entity ${emma}`));
  // 2.88: the wheel's Menu button opens her own menu (her roles and buffs, her wardrobe) - the ribbon itself is on the wheel
  await A.useWait(1500);
  const mb = await A.press(/Menu/); await sleep(700);
  const ml = A.buttons().map(b => b.label);
  ok('...the wheel\'s Menu: Emma\'s own menu opens (not the wheel\'s page)', !!mb && mb.next && ml.length >= 3 && !ml.some(l => /Take the item back/.test(l)), ml.join(' | ').slice(0, 220));
  // 2.88: the chatter switch, right in her menu and on the wheel - it reads on/off, and the same menu comes back
  const hushed = async () => passes('execute if entity @a[name=TestRat,tag=bm.hush]');
  await run('tag TestRat remove bm.hush');
  const c1 = await A.press(/Chatter: on/); await sleep(700);
  ok('...her menu has the chatter switch: pressed, chatter goes off and her menu comes back reading "off"', !!c1 && c1.next && await hushed() &&
     A.buttons().some(b => /Chatter: off/.test(b.label)) && A.buttons().some(b => /Wardrobe/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  await A.press(/Chatter: off/); await sleep(700);
  ok('...pressed again: chatter back on', !(await hushed()) && A.buttons().some(b => /Chatter: on/.test(b.label)));
  await A.useWait(1500);
  const c2 = await A.press(/Chatter: on/); await sleep(700);
  ok('...and on the wheel too: off, and the wheel comes back reading "off"', !!c2 && c2.next && await hushed() &&
     A.buttons().some(b => /Chatter: off/.test(b.label)) && A.buttons().some(b => /Call Emma|Send Emma home/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  await A.press(/Chatter: off/); await sleep(700);
  A.closeDialog && A.closeDialog(); await sleep(300);
  await A.useWait(1500);
  await press(/Send Emma home/);
  ok('...Send Emma home: she goes', await wait(4000, async () => !(await passes(`${O}execute if entity ${emma}`))));
  await A.useWait(1500);
  await press(/Take the item back/);
  ok('...Take the item back: the ribbon is in hand again, off the wheel', await wait(3000, async () => (await has('emma_ribbon')) === 1) && (await sc('TestRat', 'bm.pw0')) === 0);
  await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.1'); await run('item replace entity TestRat hotbar.1 with minecraft:air');
  await run('clear TestRat *[minecraft:custom_data~{bm:"emma_ribbon"}]'); await run('loot replace entity TestRat weapon.offhand loot bm:items/emma_ribbon');
  await A.useWait(1500); await A.useWait(1500); await press(/Call Emma/);
  ok('On again and called again', (await sc('TestRat', 'bm.pw0')) === 1 && await wait(4000, async () => passes(`${O}execute if entity ${emma}`)));
  A.slot(0); await sleep(300); A.drop(true); await sleep(5500);
  ok('...the wheel dropped: Emma goes home', !(await passes(`${O}execute if entity ${emma}`)));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('scoreboard players set TestRat bm.pw0 0'); await run('data remove storage bm:pw p' + (await sc('TestRat', 'bm.pid'))); await run('clear TestRat');

  // ================================================================== 3. Zorp's stock, and hard mode's
  await run('scoreboard players set #hard bm.cfg 0');
  await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z + 4.5} rotated 180 0 run function bm:npc/alien`);
  const ZORP = `@e[type=minecraft:wandering_trader,tag=bm.npc_alien,x=${X},y=${Y},z=${Z},distance=..10,limit=1]`;
  const sells = async id => passes(`${O}execute if data entity ${ZORP} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${id}"}}}}]`);
  await sleep(2500);
  ok('Zorp\'s stock: the Xenoplate and the Donadian blades', await sells('xenoplate_helmet') && await sells('plasma_cutter') && await sells('phase_saber') && !(await sells('warplate_chestplate')));
  await run('scoreboard players set #hard bm.cfg 1');
  ok('...in hard mode: the Vorn Warplate, the Annihilator and the Graviton Pick too',
     await wait(4000, async () => await sells('warplate_chestplate') && await sells('vorn_annihilator') && await sells('graviton_pick')));
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) if (/"xenoplate_helmet"/.test(await run(`${O}data get entity ${ZORP} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`))) idx = i;
  for (let i = 0; i < 20; i++) await run('loot give TestRat loot bm:items/xenite_green');
  for (let i = 0; i < 8; i++) await run('loot give TestRat loot bm:items/xenite_cyan');
  await sleep(500);
  const zid = await uuidEnt(ZORP);
  A.windows.length = 0; A.interact(zid); await sleep(1200);
  const w = A.windows[A.windows.length - 1];
  if (w) {
    A.write('select_trade', { slot: idx }); await sleep(400);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
    A.close(w.windowId); await sleep(500);
  }
  ok('...a Xenoplate Helm bought through his window (20 green, 8 cyan)', (await has('xenoplate_helmet')) === 1 && (await has('xenite_green')) === 0, `trade ${idx}, ${await has('xenoplate_helmet')}`);
  await run(`${O}kill @e[tag=bm.npc_alien,x=${X},y=${Y},z=${Z},distance=..10]`); await run(`${O}kill @e[tag=bm.alien_sprite,x=${X},y=${Y},z=${Z},distance=..10]`);
  await run(`scoreboard players set #hard bm.cfg ${hard0}`); await run('clear TestRat');

  // ================================================================== 4. the gear
  await run('loot replace entity TestRat hotbar.0 loot bm:items/plasma_cutter'); A.slot(0); await sleep(400);
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 2.5} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.t226"],attributes:[{id:"minecraft:max_health",base:200}],Health:200f}`);
  await sleep(800);
  const zo = '@e[type=minecraft:zombie,tag=bm.t226,limit=1]';
  A.attack(await uuidEnt(zo)); await sleep(500);
  ok('The Plasma Cutter: the zombie burns and glows', (await num(`${O}data get entity ${zo} Fire`)) > 0 && /minecraft:glowing/.test(await run(`${O}data get entity ${zo} active_effects`)),
     `fire ${await num(`${O}data get entity ${zo} Fire`)}`);
  await run('scoreboard players set TestRat bm.xdf 0');
  for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
    await run(`loot replace entity TestRat armor.${s} loot bm:items/xenoplate_${p}`);
  ok('Full Xenoplate: Jump Boost and the Deflector\'s shield', await wait(3000, async () => { const e = await effects(); return /jump_boost/.test(e) && /absorption/.test(e); }));
  await run('effect clear TestRat');
  for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
    await run(`loot replace entity TestRat armor.${s} loot bm:items/warplate_${p}`);
  await run('scoreboard players set TestRat bm.wsw 0');
  await sleep(1500);
  ok('Full Warplate, above half health: Strength and Speed', await wait(3000, async () => { const e = await effects(); return /strength/.test(e) && /speed/.test(e); }));
  await run(`${O}data merge entity ${zo} {Health:200f}`); await run(`${O}tp ${zo} ${X + 0.5} ${Y} ${Z + 2.5}`);
  const hp0 = await num('data get entity TestRat Health'), hmx = await num('attribute TestRat minecraft:max_health get'); await run(`damage TestRat ${Math.max(1, Math.floor(hp0 - hmx / 4))} minecraft:starve`); await sleep(200); const hpw = await num('data get entity TestRat Health');
  ok('...under a third: the Shockwave hurts the zombie beside you', await wait(3000, async () => (await num(`${O}data get entity ${zo} Health`)) <= 194) && (await sc('TestRat', 'bm.wsw')) >= 55,
     `hp ${hp0}/${hmx} -> ${hpw}, zombie ${await num(`${O}data get entity ${zo} Health`)}, rest ${await sc('TestRat', 'bm.wsw')}`);

  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t226]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
