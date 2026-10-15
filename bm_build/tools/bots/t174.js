// 2.80: Apophiss revised - as a regular (non-op) player, every step a real packet (rcon sets the stage: the den, the boss, the
// gear in the pack, a husk to strike, which attack the boss picks next).
//   boss  - the Serpent King: 1024 health, harder blows; his Judgement ("Kneel."): a ring burns under every player's feet - stand
//           in it and it hits through the Hollow King's Regalia AND Resistance (armour-, enchantment- and resistance-bypassing);
//           walk out of it in time and nothing hits you.
//   mace  - the Serpent King's Mace: F turns it to its next form (sneak + F: back), seven forms round (sword, axe, mace, pickaxe,
//           shovel, hoe, trident), Wind Burst III on the mace; each form's own bite (sword: poison; shovel: lift; hoe: heals you), the
//           Wither on all; the Wrath (use) on a cooldown; the pickaxe gives Haste.
//   crown - the True Crown worn with a use counts as the Regalia's helm (with the other three pieces the set wakes); its enchantments.
//   bond  - Apophiss called with his Oath: the Crown raises Resistance and Regeneration to II, the Mace Strength to II (the Regalia gives I).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
const ONLY = process.argv[2];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const passes = async c => /passed/i.test(await run(c));
  const num = async (c) => { const o = await run(c); const m = o.match(/has (-?\d+) \[/) || o.match(/(-?\d+(?:\.\d+)?)[a-z]?\s*$/i); return m ? +m[1] : NaN; };
  const H = 'execute in bm:hollow_throne run ', O = 'execute in minecraft:overworld run ';
  const B = '@e[type=minecraft:husk,tag=bm.apboss,limit=1]';
  const uuidOf = async (sel, dim = O) => { const m = (await run(`${dim}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel, dim = O) => { const u = await uuidOf(sel, dim); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const hand = async (iid, slot = 'weapon.mainhand') => passes(`execute if items entity TestRat ${slot} *[minecraft:custom_data~{bm:"${iid}"}]`);
  // (26.3 leaves an effect's amplifier out when it's 0: present with no amplifier is level I)
  const effAmp = async (eff) => { const o = await run(`data get entity TestRat active_effects[{id:"minecraft:${eff}"}]`); if (!/data: \{/.test(o)) return -1; const m = o.match(/amplifier: (-?\d+)b/); return m ? +m[1] : 0; };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('time set 1000');
  await run('kill @e[type=minecraft:wolf,tag=bm.appet]');
  await run('scoreboard objectives add bm.dt174 minecraft.custom:minecraft.damage_taken');
  const regalia = async (helm = true) => {
    if (helm) await run('loot replace entity TestRat armor.head loot bm:items/conq_helmet');
    await run('loot replace entity TestRat armor.chest loot bm:items/conq_chestplate'); await run('loot replace entity TestRat armor.legs loot bm:items/conq_leggings');
    await run('loot replace entity TestRat armor.feet loot bm:items/conq_boots');
  };

  // ================================================================== boss: the Serpent King
  if (!ONLY || ONLY === 'boss') {
    await run('attribute TestRat minecraft:max_health base set 60'); await run('effect give TestRat minecraft:instant_health 1 20 true');
    await run('scoreboard players set TestRat bm.conq 6');
    await run('execute as TestRat run function bm:admin/apophiss_den'); await run('scoreboard players set #apwake bm.p2 0'); await sleep(1500); A.stand();
    await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`); await run(`${H}kill @e[type=minecraft:interaction,tag=bm.bhit_ap]`);
    await run(`${H}tp TestRat 1076.5 5 1075.5 180 0`); await sleep(1000); A.stand();        // (the den's floor is y4: you walk at y5)
    await regalia(); await run('effect give TestRat minecraft:resistance 900 0 true');     // (full Regalia and a potion's Resistance: what tanked him before)
    await run('execute as TestRat at @s run function bm:admin/apophiss');
    const up = await wait(40000, async () => (await num(`${H}scoreboard players get ${B} bm.apph`)) === 1 && (await num(`${H}scoreboard players get ${B} bm.apatk`)) !== 9, 500);
    ok('Apophiss rises (phase I)', up);
    const mh = await num(`${H}attribute ${B} minecraft:max_health get`), hp = await num(`${H}data get entity ${B} Health`);
    const ad = await num(`${H}attribute ${B} minecraft:attack_damage base get`), ar = await num(`${H}attribute ${B} minecraft:armor base get`);
    ok('...1024 health, and all of it', mh === 1024 && hp >= 1000, `${hp} of ${mh}`);
    ok('...harder blows and a thicker hide (attack 12, armour 18)', ad === 12 && ar === 18, `attack ${ad}, armour ${ar}`);
    // a clear field: his court sent off, the bot 10 blocks from him
    const JM = '@e[type=minecraft:marker,tag=bm.apjm1]';
    const judge = async (dodge) => {
      await run(`${H}kill @e[type=#bm:hostile,tag=!bm.apboss,x=1076,y=5,z=1076,distance=..40]`);
      const bp = (await run(`${H}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
      const px = +bp[1] + 0.5, pz = +bp[3] + 10.5;
      await run(`${H}tp TestRat ${px} ${+bp[2]} ${pz} 180 0`); await run('effect give TestRat minecraft:instant_health 1 20 true'); await run('effect clear TestRat minecraft:wither');
      await sleep(1200); A.stand();
      await wait(15000, async () => (await num(`${H}scoreboard players get ${B} bm.apatk`)) === 0, 250);   // (between his attacks)
      A.bars.length = 0;
      await run(`${H}execute as ${B} at @s run function bm:p131/b/start {a:8}`);      // (the stage: Judgement is what he picks next)
      const marked = await wait(4000, async () => passes(`${H}execute if entity ${JM}`), 50);
      await run('scoreboard players set TestRat bm.dt174 0');
      if (marked && dodge) { await A.walkTo(px, pz - 4.5, 0.27); }        // (a sprint out of the ring, back the way it came over the open floor: 5.4 blocks a second)
      await wait(4000, async () => !(await passes(`${H}execute if entity ${JM}`)), 50); await sleep(150);
      return { marked, dt: await num('scoreboard players get TestRat bm.dt174'), bar: A.bars.join(' / ') };
    };
    const j1 = await judge(false);
    ok('his Judgement: a ring burns under you ("GET OUT OF THE RING!")', j1.marked && /GET OUT OF THE RING/.test(j1.bar), j1.bar.slice(0, 120));
    ok('...stand in it: 16 through the Regalia AND Resistance (not cut by armour, enchantments or potions)', j1.dt >= 150, `damage taken x10: ${j1.dt}`);
    const j2 = await judge(true);
    ok('...walk out of the ring in time: nothing hits you', j2.marked && j2.dt === 0, `damage taken x10: ${j2.dt}`);
    await run(`${H}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${H}kill @e[type=minecraft:item_display,tag=bm.apb]`); await run(`${H}kill @e[type=minecraft:interaction,tag=bm.bhit_ap]`);
    await run(`${H}kill ${JM}`); await run(`${H}kill @e[type=#bm:hostile,x=1076,y=5,z=1076,distance=..60]`);
    await run('attribute TestRat minecraft:max_health base set 20'); await run('clear TestRat'); await run('effect clear TestRat');
  }

  // ================================================================== mace / crown / bond: out in the world
  const X = 13200, Y = 121, Z = 13200;
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  await run(`${O}fill ${X - 6} ${Y - 1} ${Z - 6} ${X + 6} ${Y - 1} ${Z + 6} minecraft:stone`); await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y + 4} ${Z + 6} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(2000); A.stand();
  if (!ONLY || ONLY === 'mace') {
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_mace'); A.slot(0); await sleep(600);
    const ench = async () => (await run('data get entity TestRat Inventory[{Slot:0b}].components."minecraft:enchantments"')).replace(/.*data: /, '');
    ok('the Serpent King\'s Mace: Wind Burst III (with Density, Breach and Smite)', /wind_burst": 3/.test(await ench()) && /density/.test(await ench()), await ench());
    const F = async (sneak = false) => { if (sneak) { A.input({ shift: true }); await sleep(250); } A.swap(); await sleep(700); if (sneak) { A.input({}); await sleep(200); } };
    await F(); ok('F: its next form - the pickaxe (the offhand left empty)', (await hand('apo_mace_pickaxe')) && !(await passes('execute if items entity TestRat weapon.offhand *')));
    await sleep(1500); ok('...held, the pickaxe gives Haste II', (await effAmp('haste')) === 1, `haste ${await effAmp('haste')}`);
    await F(true); ok('sneak + F: back - the mace', await hand('apo_mace'));
    const seen = ['mace']; const order = ['axe', 'sword', 'trident', 'hoe', 'shovel', 'pickaxe', 'mace'];
    let round = true;
    for (const k of order) { await F(true); const id = k === 'mace' ? 'apo_mace' : `apo_mace_${k}`; if (!(await hand(id))) { round = false; break; } seen.push(k); }
    ok('...and on round all seven (axe, sword, trident, hoe, shovel, pickaxe, mace)', round, seen.join(' > '));
    // each form's own bite on a husk
    const husk = async () => {
      await run(`${O}kill @e[type=minecraft:husk,tag=bm.t174m]`);
      await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 2.5} {Tags:["bm.t174m","bm.seen"],NoAI:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:max_health",base:200.0d}],Health:200f}`);
      await sleep(700); return entOf('@e[type=minecraft:husk,tag=bm.t174m,limit=1]');
    };
    const hEff = async (eff) => /\{/.test(await run(`${O}data get entity @e[type=minecraft:husk,tag=bm.t174m,limit=1] active_effects[{id:"minecraft:${eff}"}]`));
    const strike = async (form) => {
      await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${form === 'mace' ? 'apo_mace' : 'apo_mace_' + form}`); A.slot(0);
      await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('effect clear TestRat');
      const h = await husk(); await sleep(1300); if (h) A.attack(h.entityId); await sleep(600); return !!h;
    };
    ok('the sword\'s bite: Poison - and the Wither, as every form', (await strike('sword')) && (await hEff('poison')) && (await hEff('wither')));
    ok('the shovel\'s: it lifts them (Levitation)', (await strike('shovel')) && (await hEff('levitation')) && (await hEff('wither')));
    ok('the hoe\'s: it heals you (Regeneration III)', (await strike('hoe')) && (await effAmp('regeneration')) === 2 && (await hEff('wither')), `regen ${await effAmp('regeneration')}`);
    // the Wrath: use
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_mace'); A.slot(0); await run('scoreboard players set TestRat bm.amq 0');
    const h = await husk(); const hp0 = await num(`${O}data get entity @e[type=minecraft:husk,tag=bm.t174m,limit=1] Health`);
    await sleep(800); A.use(); await sleep(350); A.release(); await sleep(2500);
    const hp1 = await num(`${O}data get entity @e[type=minecraft:husk,tag=bm.t174m,limit=1] Health`), q = await num('scoreboard players get TestRat bm.amq');
    ok('the Wrath (use): the husk struck, the mace on its cooldown (12 s by day)', !!h && hp1 < hp0 && q > 150 && q <= 240, `husk ${hp0} -> ${hp1}, cooldown ${q}`);
    A.bars.length = 0; A.use(); await sleep(350); A.release(); await sleep(600);
    ok('...used again too soon: not yet', (await num('scoreboard players get TestRat bm.amq')) < q && A.bars.some(b => /Wrath|again|ready|s\b/i.test(b)), A.bars.slice(-1).join(''));
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t174m]`);
  }
  if (!ONLY || ONLY === 'crown') {
    await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 10 true'); await sleep(300); await run('effect clear TestRat');
    await regalia(false);                                        // (at full health: the Crown's own Wrath near death stays out of it)
    await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown'); A.slot(0); await sleep(500);
    A.use(); await sleep(350); A.release(); await sleep(800);
    ok('the True Crown worn with a use', await hand('apo_true_crown', 'armor.head'));
    const en = (await run('data get entity TestRat equipment.head.components."minecraft:enchantments"')).replace(/.*data: /, '');
    ok('...Protection X, Thorns III, Respiration V (as the Regalia\'s helm)', /protection": 10/.test(en) && /thorns": 3/.test(en) && /respiration": 5/.test(en), en);
    ok('...with the Regalia\'s other three pieces: the set wakes (the Crown is its helm)', await wait(3000, async () => /bm\.rgon/.test(await run('tag TestRat list')), 250));
    await sleep(1500);
    ok('...no Apophiss at your side: only the Regalia\'s own Resistance I (not II)', (await effAmp('resistance')) < 1, `resistance ${await effAmp('resistance')}`);
    // the bond: his Oath used
    await run('scoreboard players set TestRat bm.apcd 0');                                      // (no faint cooldown left from a last run)
    await run('loot replace entity TestRat hotbar.1 loot bm:items/apo_oath'); A.slot(1); await sleep(400);
    A.bars.length = 0; A.use(); await sleep(350); A.release();
    const came = await wait(6000, async () => passes(`${O}execute if entity @e[type=minecraft:wolf,tag=bm.appet,x=${X},y=${Y},z=${Z},distance=..20]`), 300);
    ok('his Oath used: Apophiss comes', came, A.bars.slice(-1).join(''));
    ok('...the Crown with him at your side: Resistance II and Regeneration II (past the Regalia\'s own)', await wait(3000, async () => (await effAmp('resistance')) >= 1 && (await effAmp('regeneration')) >= 1, 250),
       `resistance ${await effAmp('resistance')}, regeneration ${await effAmp('regeneration')}`);
    await run('item replace entity TestRat hotbar.2 with minecraft:air'); await run('loot replace entity TestRat hotbar.2 loot bm:items/apo_mace'); A.slot(2);
    ok('...the Mace with him at your side: Strength II', await wait(3000, async () => (await effAmp('strength')) >= 1, 250), `strength ${await effAmp('strength')}`);
    await run('kill @e[type=minecraft:wolf,tag=bm.appet]'); await sleep(300); await run('scoreboard players set TestRat bm.apcd 0');
  }
  await run('scoreboard objectives remove bm.dt174'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
