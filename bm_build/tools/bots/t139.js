// 2.77c: Apophiss's True Crown, as a regular (non-op) player: worn with a use (swapping with the helmet on), its stats (the
// strongest thing anyone can wear), its passives (no wither, no poison, fire-proof, water-breathing, night sight, Regeneration
// when badly hurt, monsters near weakened, Strength II at night), sneak + a real jump for five lines of fangs (they never came
// before: the shadow-crown's handler ate the jump), the Serpent King's Wrath near death (once, then two minutes), and the
// crown set atop a block with a sneak + use (the very crown, its name kept; it turns), not taken by another player, taken back
// with a sneak + punch, and dropped - not lost - when its block is broken. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)(?:[dfbsL])?\s*$/) || [0, NaN])[1]);
  const attr = async (a) => +(((await run(`attribute TestRat minecraft:${a} get`)).match(/is (-?[\d.]+)/) || [0, NaN])[1]);
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const eff = async (e) => /passed/i.test(await run(`execute if entity @a[name=TestRat,nbt={active_effects:[{id:"minecraft:${e}"}]}]`));
  const effAmp = async (e) => { const m = (await run(`data get entity TestRat active_effects`)).match(new RegExp(`\\{[^{}]*id: "minecraft:${e}"[^{}]*\\}`)); if (!m) return -1; const a = m[0].match(/amplifier: (\d+)b/); return a ? +a[1] : 0; };
  const use = async (C, slot, sneak = false) => { C.slot(slot); await sleep(250); if (sneak) { C.input({ shift: true }); await sleep(200); } C.use(); await sleep(400); C.release(); if (sneak) { C.input({}); await sleep(150); } };
  // (a real jump: up off the ground and back down, a tick a step - the server counts it when we leave the ground going up)
  const jump = async (C, sneak = false) => { C.unstand(); if (sneak) { C.input({ shift: true }); await sleep(150); } const y0 = C.pos.y;
    for (const dy of [0.42, 0.75, 1.0, 1.16, 1.25, 1.17, 1.02, 0.79, 0.49, 0.12]) { C.pos.y = y0 + dy; C.ground(false); await sleep(50); }
    C.pos.y = y0; C.ground(true); await sleep(50); if (sneak) { await sleep(200); C.input({}); } C.stand(); };
  const X = 16160, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('time set 1000');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  for (const o of ['bm.crcd', 'bm.crw']) await run(`scoreboard players set TestRat ${o} 0`);

  // ---------------------------------------------------------------- worn with a use: swapped with the helmet on
  const base = await attr('max_health');             // (the bot's own health, before the crown - other things it has earned may add to it)
  await run('item replace entity TestRat armor.head with minecraft:iron_helmet');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown');
  ok('its lore says how: "Use: wear it. Sneak + use on a block: set it there."', /Sneak \+ use on a block: set it there/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components')));
  await use(A, 0);
  ok('a use puts it on (the crown on the head)', /apo_true_crown/.test(await run('data get entity TestRat equipment.head')));
  ok('...and the iron helmet that was on comes to the hand', /iron_helmet/.test(await run('data get entity TestRat SelectedItem')) || /iron_helmet/.test(await run('data get entity TestRat Inventory[{Slot:0b}]')));
  await run('clear TestRat minecraft:iron_helmet');
  await sleep(1300);
  // (its stats: worn alone, nothing else on)
  const mh = await attr('max_health'), ar = await attr('armor'), tg = await attr('armor_toughness'), ad = await attr('attack_damage'), kb = await attr('knockback_resistance'),
        scl = await attr('scale'), rch = await attr('entity_interaction_range'), spd = await attr('movement_speed');
  ok('worn: a size taller (scale 1.25)', Math.abs(scl - 1.25) < 0.01, `scale ${scl}`);
  ok('...+12 health, +8 armour, +6 toughness', mh === base + 12 && ar === 8 && tg === 6, `health ${base} -> ${mh} armour ${ar} toughness ${tg}`);
  ok('...+8 damage (9), +3 reach (6), hard to knock back (0.5), +10% speed', ad === 9 && Math.abs(rch - 6) < 0.01 && Math.abs(kb - 0.5) < 0.01 && Math.abs(spd - 0.11) < 0.001,
     `damage ${ad} reach ${rch} knockback ${kb} speed ${spd}`);
  // (stronger than anything else anyone can wear: the shadow-crown it outclasses, and the heaviest chestplate there is)
  await run('item replace entity TestRat armor.head with minecraft:air'); await run('loot replace entity TestRat armor.head loot bm:items/apophiss_crown'); await sleep(300);
  const hmh = await attr('max_health'), had = await attr('attack_damage'), har = await attr('armor');
  await run('item replace entity TestRat armor.head with minecraft:air'); await run('loot replace entity TestRat armor.chest loot bm:items/juggernaut_chestplate_3'); await sleep(300);
  const jmh = await attr('max_health'), jad = await attr('attack_damage'), jar = await attr('armor'), jtg = await attr('armor_toughness');
  await run('item replace entity TestRat armor.chest with minecraft:air');
  const score = (d, a, h, t) => d + a + h / 2 + t;
  ok('stronger than the shadow-crown the Hollow King wore', ad > had && mh > hmh && ar > har, `true: dmg ${ad} hp +${mh - base} armour ${ar} / shadow: ${had} +${hmh - base} ${har}`);
  ok('...and than the heaviest chestplate there is (damage + armour + health/2 + toughness)', score(ad - 1, ar, mh - base, tg) > score(jad - 1, jar, jmh - base, jtg) + 5,
     `crown ${score(ad - 1, ar, mh - base, tg)} vs juggernaut ${score(jad - 1, jar, jmh - base, jtg)}`);
  // (back on - with a use again)
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown'); await use(A, 0); await sleep(1300);
  ok('on again with a use (empty head: nothing comes back to the hand)', /apo_true_crown/.test(await run('data get entity TestRat equipment.head')) && (await has('TestRat', 'apo_true_crown')) === 1 &&
     !/apo_true_crown/.test(await run('data get entity TestRat SelectedItem')));

  // ---------------------------------------------------------------- the passives
  ok('worn: fire can\'t touch you, you breathe water, you see in the dark', (await eff('fire_resistance')) && (await eff('water_breathing')) && (await eff('night_vision')));
  await run('effect give TestRat minecraft:wither 20 1'); await run('effect give TestRat minecraft:poison 20 1');
  ok('...wither and poison don\'t take hold (gone within a second)', await wait(2500, async () => !(await eff('wither')) && !(await eff('poison'))));
  const hurtTo = async (hp) => { const h = await num('data get entity TestRat Health'); if (h > hp) await run(`damage TestRat ${(h - hp).toFixed(1)} minecraft:magic`); };
  await run('effect clear TestRat minecraft:regeneration'); await hurtTo(12);
  ok('badly hurt (12 of 34 - under half): Regeneration', await wait(2500, async () => await eff('regeneration')), `health ${await num('data get entity TestRat Health')}`);
  await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(400);
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 4.5} {NoAI:1b,Tags:["bm.t139"],PersistenceRequired:1b}`);
  ok('a monster near (4 blocks) is weakened', await wait(2500, async () => /passed/i.test(await run(`${O}execute if entity @e[type=minecraft:husk,tag=bm.t139,nbt={active_effects:[{id:"minecraft:weakness"}]}]`))));
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t139]`);
  await run('time set 18000'); await run('effect clear TestRat minecraft:strength');
  ok('at night: Strength II and Regeneration', await wait(2500, async () => (await effAmp('strength')) === 1 && (await eff('regeneration'))), `strength ${await effAmp('strength')}`);
  await run('time set 1000'); await run('effect clear TestRat minecraft:strength'); await run('effect clear TestRat minecraft:regeneration');

  // ---------------------------------------------------------------- sneak + a real jump: Serpent's Fangs, five lines
  await run('scoreboard players set TestRat bm.crcd 0'); await run(`${O}kill @e[type=minecraft:evoker_fangs]`);
  let fangs = 0; const jp = jump(A, true);
  for (let k = 0; k < 14; k++) { fangs = Math.max(fangs, await cnt(`@e[type=minecraft:evoker_fangs,x=${X},y=${Y},z=${Z},distance=..24]`)); await sleep(50); }
  await jp;
  ok('sneak + jump: the fangs come - five lines of them (they never came before)', fangs >= 40, `fangs ${fangs}`);
  ok('...and the crown rests 2 seconds', (await sc('TestRat', 'bm.crcd')) > 0 && (await sc('TestRat', 'bm.crcd')) <= 40, `cooldown ${await sc('TestRat', 'bm.crcd')}`);
  await sleep(1500); await run(`${O}kill @e[type=minecraft:evoker_fangs]`);
  await jump(A, false); await sleep(400);
  ok('a jump without sneaking: no fangs', (await cnt('@e[type=minecraft:evoker_fangs]')) === 0);

  // ---------------------------------------------------------------- near death: the Serpent King's Wrath, once
  await run('scoreboard players set TestRat bm.crw 0');            // (an earlier step's low health may have spent it already)
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 3.5} {NoAI:1b,Tags:["bm.t139","bm.seen"],PersistenceRequired:1b,Health:20f}`);
  await run('effect clear TestRat minecraft:resistance'); await run('effect clear TestRat minecraft:absorption');
  await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(300);
  A.bars.length = 0; await hurtTo(8);
  ok('at 8 of 34 health: the Serpent King\'s Wrath', await wait(2000, async () => /Wrath/.test(A.bars.join(' '))), A.bars.slice(-1).join('').slice(0, 120));
  ok('...Resistance III, Absorption III, Regeneration II', (await effAmp('resistance')) === 2 && (await effAmp('absorption')) === 2 && (await effAmp('regeneration')) === 1,
     `res ${await effAmp('resistance')} abs ${await effAmp('absorption')} regen ${await effAmp('regeneration')}`);
  ok('...the monster beside you bitten and withered', /passed/i.test(await run(`${O}execute if entity @e[type=minecraft:husk,tag=bm.t139,nbt={active_effects:[{id:"minecraft:wither"}]}]`)) ||
     !(await cnt('@e[type=minecraft:husk,tag=bm.t139]')));
  ok('...then two minutes before it can come again', (await sc('TestRat', 'bm.crw')) >= 118, `cooldown ${await sc('TestRat', 'bm.crw')}`);
  await run('effect clear TestRat minecraft:resistance'); await run('effect clear TestRat minecraft:absorption'); A.bars.length = 0; await run('damage TestRat 3 minecraft:magic'); await sleep(1200);
  ok('...hurt again at once: no second Wrath', !/Wrath/.test(A.bars.join(' ')) && (await effAmp('resistance')) === -1);
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t139]`); await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('scoreboard players set TestRat bm.crw 0');

  // ---------------------------------------------------------------- set atop a block: sneak + use (the very crown, its name kept)
  await run(`${O}setblock ${X + 0.5} ${Y + 1} ${Z + 2.5} minecraft:polished_deepslate`.replace(/(\d+)\.5/g, '$1'));
  await run('item replace entity TestRat armor.head with minecraft:air');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown');
  await run(`item modify entity TestRat hotbar.0 {type:"minecraft:set_name",target:"custom_name",name:{text:"Hiss's Own",color:"green"}}`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 38);
  A.bars.length = 0; await use(A, 0, true);
  const CD = `@e[type=minecraft:item_display,tag=bm.crd,x=${X + 0.5},y=${Y + 2},z=${Z + 2.5},distance=..0.6,limit=1]`;
  const CX = `@e[type=minecraft:interaction,tag=bm.crst,x=${X + 0.5},y=${Y + 2},z=${Z + 2.5},distance=..0.6,limit=1]`;
  ok('sneak + use on the block: the crown sits on top of it', (await cnt(CD)) === 1 && (await cnt(CX)) === 1, A.bars.slice(-1).join('').slice(0, 120));
  ok('...out of the hand', (await has('TestRat', 'apo_true_crown')) === 0);
  ok('...the very crown (its name kept)', /Hiss's Own/.test(await nbt(CD, 'item')));
  ok('..."gleams where you set it. (Sneak + punch it to take it back.)"', /Sneak \+ punch it to take it back/.test(A.bars.join(' ')));
  const r1 = await num(`${O}data get entity ${CD} Rotation[0]`); const g1 = await sc(CD.replace('limit=1]', 'limit=1]'), 'bm.apt'); await sleep(1500);
  const r2 = await num(`${O}data get entity ${CD} Rotation[0]`); const g2 = await sc(CD, 'bm.apt');
  ok('...it turns slowly, and gleams (its sparkle loop runs)', r1 !== r2 && g2 > g1, `yaw ${r1} -> ${r2}, ticks ${g1} -> ${g2}`);
  // (somebody else can't take it)
  const B = await bot('TestMouse'); await sleep(2500); B.stand(); await run('gamemode survival TestMouse'); await run('effect give TestMouse minecraft:resistance 600 4 true');
  await run(`${O}tp TestMouse ${X + 2.5} ${Y + 1} ${Z + 2.5} 90 20`); await wait(2000, async () => B.pos && Math.abs(B.pos.x - (X + 2.5)) < 0.05, 100); await sleep(500);
  let box = await entOf(B, CX); B.bars.length = 0; B.input({ shift: true }); await sleep(250); if (box) B.attack(box.entityId); await sleep(700); B.input({}); await sleep(200);
  ok('another player\'s sneak + punch: "It isn\'t yours to take." (it stays)', /isn't yours/.test(B.bars.join(' ')) && (await cnt(CD)) === 1 && (await has('TestMouse', 'apo_true_crown')) === 0,
     `box ${box ? 'yes' : 'no'} bars ${B.bars.slice(-1).join('').slice(0, 80)}`);
  B.end(); await sleep(500);
  // (its owner takes it back)
  box = await entOf(A, CX); A.input({ shift: true }); await sleep(250); if (box) A.attack(box.entityId); await sleep(800); A.input({}); await sleep(300);
  ok('its owner\'s sneak + punch: back in the inventory - still "Hiss\'s Own"', await wait(2000, async () => (await has('TestRat', 'apo_true_crown')) === 1) &&
     /Hiss's Own/.test(await run('data get entity TestRat Inventory')), `box ${box ? 'yes' : 'no'}`);
  ok('...nothing left on the block', (await cnt(CD)) === 0 && (await cnt(CX)) === 0);
  // (its block broken: it drops, never lost)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 38);
  await use(A, 0, true); ok('set down again', (await cnt(CD)) === 1);
  await at(X + 6.5, Y + 1, Z + 0.5, 0, 0);
  await run(`${O}setblock ${X} ${Y + 1} ${Z + 2} minecraft:air`);
  ok('its block broken: the crown drops as an item (not lost), the display gone', await wait(2500, async () => (await cnt(CD)) === 0 &&
     /passed/i.test(await run(`${O}execute if entity @e[type=minecraft:item,x=${X + 0.5},y=${Y + 1.5},z=${Z + 2.5},distance=..2,nbt={Item:{components:{"minecraft:custom_data":{bm:"apo_true_crown"}}}}]`))));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();
