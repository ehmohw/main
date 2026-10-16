// 2.80e: Apophiss's Unbound Crown - as a regular (non-op) player. rcon sets the stage: a floor, the three pieces, the time,
// a husk or two to burn, an iron chestplate, a bad hurt (down to 6 health).
//   The pieces say where they lead (the True Crown, the Wraithfire Heart, the Deathmask); tossed down together with Q they
//   forge Apophiss's Unbound Crown; walked over: picked up, and the "Unbound" advancement.
//   Right-click: it's worn. By night it is the whole Regalia on its own (the set wakes: its power on you) - and the waking
//   leaves the iron chestplate you wear with it untrimmed.
//   A real jump, then sneak in mid-air: a wingbeat (lifted, then gliding: Slow Falling); a second beat; a third is refused.
//   Soul fire: a fire-immune husk beside you burns. Sneak + jump on the ground: the Fangs - and a husk 7 blocks ahead, out of
//   the aura's reach, is seared. Badly hurt: the Serpent King's Wrath, and three Void Orbs ring you.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 17100, Y = 100, Z = 16000;
  const at = `x=${X},y=${Y},z=${Z},distance=..20`;
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[custom_data~{bm:"${iid}"}] 0`));
  const fx = async (e) => new RegExp(`minecraft:${e}`).test(await run('data get entity TestRat active_effects'));
  const score = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const hp = async (sel) => +((await run(`${O}data get entity ${sel} Health`)).match(/([\d.]+)f/) || [0, -1])[1];
  const lore = async n => await run(`data get entity TestRat Inventory[{Slot:${n}b}].components."minecraft:lore"`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:saturation 900 0 true'); await run('advancement revoke TestRat only bm:story/forge_unbound');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 10} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,${at}]`); await run('time set 1000'); await run('weather clear');
  const stand = async (yaw = 0) => { await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} ${yaw} 0`); await sleep(700); };

  // ---- the forge
  await stand();
  for (const [i, iid] of ['apo_true_crown', 'wraithfire_heart', 'conq_helmet'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  ok('each piece says where it leads (the crown: "...it is unbound"; the heart and the Deathmask: "...they fuse")',
     /it is unbound/.test(await lore(0)) && /True Crown and the Hollow King/.test(await lore(1)) && /True Crown and a Wraithfire Heart/.test(await lore(2)));
  for (let i = 0; i < 3; i++) { A.slot(i); await sleep(200); A.drop(false); await sleep(250); }
  const forged = await wait(9000, async () => (await cnt(`@e[type=minecraft:item,${at},nbt={Item:{components:{"minecraft:custom_data":{bm:"apo_unbound_crown"}}}}]`)) >= 1);
  ok('tossed down together (Q): Apophiss\'s Unbound Crown is forged', forged);
  const p = (await run(`${O}data get entity @e[type=minecraft:item,tag=bm.fgout,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (p) { await sleep(1500); await A.walkTo(+p[1], +p[3]); await sleep(1500); }
  ok('...walked over: picked up', await has('apo_unbound_crown'));
  ok('...the advancement "Unbound"', await wait(3000, async () => (await cnt('@a[name=TestRat,advancements={bm:story/forge_unbound=true}]')) === 1));

  // ---- worn: the whole Regalia, alone (by night); an iron chestplate worn with it stays untrimmed
  await run('clear TestRat'); await stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_unbound_crown'); await run('item replace entity TestRat armor.chest with minecraft:iron_chestplate');
  A.slot(0); await sleep(300); A.use(); await sleep(300); A.release(); await sleep(600);
  ok('right-click: the Unbound Crown is worn', /apo_unbound_crown/.test(await run('data get entity TestRat equipment.head.components."minecraft:custom_data".bm')));
  await run('time set 14000');
  ok('by night, alone, it is the whole Regalia: the set wakes on you', await wait(4000, async () => (await cnt('@a[name=TestRat,tag=bm.rgon]')) === 1 && (await score('bm.rgt')) >= 1),
     `rgt ${await score('bm.rgt')}`);
  ok('...its power: the Regalia\'s damage boost', /bm:rg_power/.test(await run('attribute TestRat minecraft:attack_damage modifier value get bm:rg_power')) ||
     !/No modifier|not have/.test(await run('attribute TestRat minecraft:attack_damage modifier value get bm:rg_power')));
  ok('...and the iron chestplate worn with it is left untrimmed', !/trim/.test(await run('data get entity TestRat equipment.chest.components')));
  await run('time set 1000'); await run('item replace entity TestRat armor.chest with minecraft:air');

  // ---- the wings: a real jump, then sneak in mid-air
  const jumpSneak = async (presses) => { A.unstand(); const y0 = A.pos.y; const path = [0.42, 0.75, 1.0, 1.16, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25];
    const hits = { 4: 1, 7: 2, 10: 3 }; const seen = [];
    for (let k = 0; k < path.length; k++) { A.pos.y = y0 + path[k]; A.ground(false);
      if (hits[k] && hits[k] <= presses) { A.input({ shift: true }); await sleep(100); seen.push([await score('bm.uwn'), await fx('levitation')]); A.input({}); }
      await sleep(80); }
    await sleep(500); const glide = await fx('slow_falling');
    A.pos.y = y0; A.ground(true); A.stand(); return { seen, glide }; };
  await run('effect clear TestRat'); A.bars.length = 0;
  const w = await jumpSneak(3);
  ok('a jump, then sneak in mid-air: a wingbeat lifts you', w.seen[0] && w.seen[0][0] === 1 && w.seen[0][1], JSON.stringify(w.seen));
  ok('...a second beat', w.seen[1] && w.seen[1][0] === 2, JSON.stringify(w.seen));
  ok('...a third is refused - the wings need the ground', w.seen[2] && w.seen[2][0] === 2 && A.bars.some(b => /need the ground/.test(b)), A.bars.slice(-1).join(''));
  ok('...and you glide down (Slow Falling)', w.glide);
  await sleep(600);
  ok('landed: the beats come back', await wait(2000, async () => (await score('bm.uwn')) === 0));

  // ---- soul fire: a fire-immune husk beside you burns
  await stand();
  await run(`${O}summon minecraft:husk ${X + 2.5} ${Y + 1} ${Z + 0.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t186a"],attributes:[{id:"minecraft:max_health",base:200d}],Health:200f,active_effects:[{id:"minecraft:fire_resistance",amplifier:0b,duration:-1}]}`);
  const A0 = `@e[type=minecraft:husk,tag=bm.t186a,${at},limit=1]`;
  ok('soul fire: a fire-immune husk beside you burns', await wait(3500, async () => (await hp(A0)) < 199), `health ${await hp(A0)}`);
  await run(`${O}kill ${A0}`);

  // ---- the Fangs sear: a husk 7 blocks ahead (out of the aura's reach)
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 7.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t186b"],attributes:[{id:"minecraft:max_health",base:200d}],Health:200f}`);
  const B0 = `@e[type=minecraft:husk,tag=bm.t186b,${at},limit=1]`;
  await run('scoreboard players set TestRat bm.crcd 0'); await sleep(1200);
  const h0 = await hp(B0);
  A.unstand(); A.input({ shift: true }); await sleep(150); { const y0 = A.pos.y;
    for (const dy of [0.42, 0.75, 1.0, 1.16, 1.25, 1.17, 1.02, 0.79, 0.49, 0.12]) { A.pos.y = y0 + dy; A.ground(false); await sleep(50); }
    A.pos.y = y0; A.ground(true); } await sleep(300); A.input({}); A.stand(); await sleep(900);
  ok('sneak + jump: the Fangs - and the husk ahead is seared by soul fire', (await hp(B0)) < h0 - 4, `${h0} -> ${await hp(B0)}`);
  await run(`${O}kill ${B0}`);

  // ---- badly hurt: the Wrath, and three Void Orbs ring you
  await run('scoreboard players set TestRat bm.crw 0'); await run('effect clear TestRat');
  { const h = +((await run('data get entity TestRat Health')).match(/([\d.]+)f/) || [0, 30])[1];      // (staged: down to 6 health, past armour)
    await run(`damage TestRat ${Math.max(1, Math.floor(h - 6))} minecraft:out_of_world`); } await sleep(1500);
  ok('badly hurt: the Serpent King\'s Wrath, and three Void Orbs ring you', (await cnt(`@e[type=minecraft:marker,tag=bm.uvo,${at}]`)) === 3,
     `${await cnt(`@e[type=minecraft:marker,tag=bm.uvo,${at}]`)} orbs; Wrath cooldown ${await score('bm.crw')}`);
  ok('...they fade after a few seconds', await wait(8000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.uvo,${at}]`)) === 0));

  await run(`${O}kill @e[type=!minecraft:player,${at}]`); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true');
  await run('scoreboard players set TestRat bm.crw 0');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
