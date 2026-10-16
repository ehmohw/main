// 2.75c: invisible armour, Pearlman's bell, builders' crates, the Netherite Laurel, one set of gems per world, hand-run tier
// spawns, Vorn red shards, the haul order, Cecil's beam, graveyards in the land
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'); const OUT = BMB + 'out_p2/BlackMarket_DP/data/bm/';
const F = p => fs.readFileSync(OUT + 'function/' + p + '.mcfunction', 'utf8');
const res = []; const ONLY = process.argv[2] ? new RegExp(process.argv[2]) : null; const want = k => !ONLY || ONLY.test(k);
const X = 19000, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async sel => /passed/i.test(await run(`execute if entity ${sel}`));
  const cnt = async sel => { const o = await run(`execute if entity ${sel}`); return /passed/.test(o) ? +((o.match(/Count: (\d+)/) || [0, 1])[1]) : 0; };
  const A = await bot('TestRat'); await sleep(2500);
  const field = async () => {
    await run(`execute in minecraft:overworld run forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
    await run(`execute in minecraft:overworld run fill ${X - 30} ${Y - 1} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:grass_block`);
    await run(`execute in minecraft:overworld run fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 20} ${Z + 30} minecraft:air`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('weather clear'); await run('time set day');
    await sleep(800);
  };
  await run('gamerule doMobSpawning false');

  if (want('ghost')) {
    await field();
    // (2.76: only the pack's own gear vanishes - vanilla armour stays in sight)
    await run('item replace entity TestRat armor.chest with minecraft:iron_chestplate[minecraft:enchantments={"minecraft:protection":2}]');
    await run('loot replace entity TestRat armor.head loot bm:items/thiefs_cowl');
    await run('loot replace entity TestRat armor.feet loot bm:items/smugglers_boots');
    const cowl0 = await run('data get entity TestRat equipment.head.components');
    const boot0 = await run('data get entity TestRat equipment.feet.components');
    await run('effect give TestRat minecraft:invisibility 3 0 true'); await sleep(400);
    const ch = await run('data get entity TestRat equipment.chest.components');
    const hd = await run('data get entity TestRat equipment.head.components');
    ok('Invisible: a vanilla chestplate stays in sight (only its enchantments)', !/bm:none|bmg/.test(ch) && /protection/.test(ch), ch.slice(0, 160));
    ok('Invisible: the Thief\'s Cowl (a Black Market piece) points at the empty model', /asset_id: "bm:none"/.test(hd) && /thiefs_cowl/.test(hd), hd.slice(0, 160));
    const bt = await run('data get entity TestRat equipment.feet.components');
    ok('Invisible: the Smuggler\'s Boots too (their own data kept)', /bm:none/.test(bt) && /smugglers_boots/.test(bt), bt.slice(0, 160));
    // put a new piece on while invisible: hidden as well
    await run('loot replace entity TestRat armor.legs loot bm:items/crimson_leggings'); await sleep(300);
    ok('A Black Market piece put on while invisible is hidden at once', /bm:none/.test(await run('data get entity TestRat equipment.legs.components')));
    await run('effect clear TestRat minecraft:invisibility'); await sleep(400);
    const ch2 = await run('data get entity TestRat equipment.chest');
    ok('Visible again: the vanilla chestplate is exactly as it was (only its enchantments)', !/bm:none|bmg|equippable|custom_data/.test(ch2) && /protection/.test(ch2), ch2.slice(0, 200));
    const hd2 = await run('data get entity TestRat equipment.head.components');
    ok('Visible again: the Cowl\'s own data is back, the marks gone', !/bmg|bm:none/.test(hd2) && hd2.replace(/^.*?: /, '') === cowl0.replace(/^.*?: /, ''), hd2.slice(0, 120));
    const bt2 = await run('data get entity TestRat equipment.feet.components');
    ok('Visible again: leggings and boots back as they were', !/bmg|bm:none/.test(await run('data get entity TestRat equipment.legs')) && bt2.replace(/^.*?: /, '') === boot0.replace(/^.*?: /, ''), bt2.slice(0, 120));
    // a hidden piece taken off into the pack: put back as it lands
    await run('loot replace entity TestRat armor.chest loot bm:items/crimson_chestplate');
    await run('effect give TestRat minecraft:invisibility 5 0 true'); await sleep(400);
    ok('(a Black Market chestplate, hidden)', /bm:none/.test(await run('data get entity TestRat equipment.chest.components')));
    await run('item replace entity TestRat container.5 from entity TestRat armor.chest'); await run('item replace entity TestRat armor.chest with minecraft:air'); await sleep(400);
    ok('Hidden chestplate moved into the pack: put back there', !/bmg|bm:none/.test(await run('data get entity TestRat Inventory[{Slot:5b}]')), (await run('data get entity TestRat Inventory[{Slot:5b}]')).slice(0, 160));
    // dropped while hidden: put back on the ground
    await run(`summon minecraft:item ${X + 3} ${Y} ${Z} {Tags:["t126i"],PickupDelay:200s,Item:{id:"minecraft:iron_helmet",count:1,components:{"minecraft:equippable":{slot:"head",asset_id:"bm:none"},"minecraft:custom_data":{bmg:1b,bmgeq:{slot:"head",asset_id:"minecraft:iron",equip_sound:"minecraft:item.armor.equip_iron"}}}}}`);
    await sleep(1600);
    ok('A hidden piece on the ground is put back within a second', !/bmg|bm:none|components/.test(await run('data get entity @e[type=item,tag=t126i,limit=1] Item')), (await run('data get entity @e[type=item,tag=t126i,limit=1] Item')).slice(0, 160));
    await run('kill @e[type=item,tag=t126i]'); await run('effect clear TestRat'); await run('clear TestRat');
  }

  if (want('bell')) {
    await field();
    await run('kill @e[type=villager,tag=bm.pearl]'); await run('kill @e[type=item_display,tag=bm.pearld]');
    await run('loot give TestRat loot bm:items/pearl_bell'); await run('loot give TestRat loot bm:items/pearl_bell');
    await run('execute as TestRat at @s run function bm:p126/bell/ring'); await sleep(500);
    ok('Ringing the bell brings Pearlman', await has('@e[type=villager,tag=bm.pearl]'));
    const left = await run('clear TestRat *[minecraft:custom_data~{bm:"pearl_bell"}] 0');
    ok('... and uses up one bell', /Found 1 /i.test(left), left);
    await run('execute as TestRat at @s run function bm:p126/bell/ring'); await sleep(300);
    ok('Rung again while he\'s out: nothing, and the bell is kept', (await cnt('@e[type=villager,tag=bm.pearl]')) === 1 && /Found 1 /i.test(await run('clear TestRat *[minecraft:custom_data~{bm:"pearl_bell"}] 0')));
    await run('kill @e[type=villager,tag=bm.pearl]'); await run('kill @e[type=item_display,tag=bm.pearld]'); await run('clear TestRat');
    ok('5% a won heist, any tier: the bell is among the raid finds (before the haul is packed)', /p126\/bell\/find/.test(F('p105/finds')) && /matches \.\.5 run function bm:p126\/bell\/find/.test(F('p105/finds')));
  }

  if (want('haul')) {
    const h = F('p70/haul').split('\n');
    const pk = h.indexOf('function bm:p74/haul_pack');
    ok('The Big Score and the Skiff part go in before the haul is packed', h.findIndex(l => l.includes('p124/big_score')) < pk && h.findIndex(l => l.includes('p120/skiff')) < pk && pk > 0);
  }

  if (want('crate')) {
    await field();
    for (const [c, kind] of [['crate_stone', /stone|brick|deepslate|tuff|andesite|diorite|granite|calcite|sandstone|blackstone/], ['crate_wood', /_log|_stem/]]) {
      await run('clear TestRat'); await run(`loot give TestRat loot bm:p105/${c}`); await sleep(200);
      let stacks = 0, all = true;
      for (let i = 0; i < 12; i++) { const s = await run(`data get entity TestRat Inventory[${i}]`); if (/count: 64/.test(s)) { stacks++; if (!kind.test(s)) all = false; } }
      ok(`${c}: nine full stacks, all of its kind`, stacks === 9 && all, `${stacks} stacks`);
    }
    const desk = F('p105/desk/buy');
    ok('The Crate Desk sells both (6 and 8 coins)', /8506 run scoreboard players set #need bm.rng 6/.test(desk) && /8507 run scoreboard players set #need bm.rng 8/.test(desk));
    await run('clear TestRat');
  }

  if (want('laurel')) {
    await field();
    await run('loot give TestRat loot bm:items/laurel_t5');
    ok('Tier V laurel: the Netherite Laurel', /Netherite Laurel/.test(await run('data get entity TestRat Inventory[0].components."minecraft:item_name"')));
    await run('clear TestRat');
    await run('give TestRat minecraft:totem_of_undying[minecraft:custom_data={bm:"laurel_t5",bmv:33},minecraft:item_name="Ember Laurel"]'); await sleep(1600);
    ok('An old Ember Laurel is renamed by itself', /Netherite Laurel/.test(await run('data get entity TestRat Inventory[0].components."minecraft:item_name"')), await run('data get entity TestRat Inventory[0].components."minecraft:item_name"'));
    await run('clear TestRat');
  }

  if (want('gem')) {
    await field();
    await run('scoreboard players set TestRat bm.kxel 5'); await run('scoreboard players set TestRat bm.cpel 3');
    await run('scoreboard players set TestRat bm.kxell 0'); await run('scoreboard players set TestRat bm.cpell 0'); await sleep(200);
    await run('effect give TestRat minecraft:slow_falling 10 0 true');
    await run('tag TestRat add bm.gvok'); await run('execute in bm:gutter run tp TestRat -230.5 90 -230.5'); await sleep(300);
    ok('Into the heist lobby: his overworld gems stay behind', (await sc('TestRat', 'bm.kxel')) === 0 && (await sc('TestRat', 'bm.cpel')) === 0, `kxel ${await sc('TestRat', 'bm.kxel')} cpel ${await sc('TestRat', 'bm.cpel')}`);
    await run('scoreboard players set TestRat bm.kxel 10'); await run('scoreboard players set TestRat bm.cpel 10');      // the Ethereal form, given in the lobby
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(300);
    ok('Back in the overworld: his own gems again, not the lobby\'s Ethereal', (await sc('TestRat', 'bm.kxel')) === 5 && (await sc('TestRat', 'bm.cpel')) === 3, `kxel ${await sc('TestRat', 'bm.kxel')} cpel ${await sc('TestRat', 'bm.cpel')}`);
    await run('tag TestRat add bm.gvok'); await run('execute in bm:gutter run tp TestRat -230.5 90 -230.5'); await sleep(300);
    ok('In the lobby again: the lobby\'s Ethereal is waiting there', (await sc('TestRat', 'bm.kxel')) === 10 && (await sc('TestRat', 'bm.cpel')) === 10);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(300);
    for (const o of ['bm.kxel', 'bm.cpel', 'bm.kxell', 'bm.cpell', 'bm.kxelo', 'bm.cpelo']) await run(`scoreboard players set TestRat ${o} 0`);
  }

  if (want('elite')) {
    await field();
    await run('tag TestRat remove bm.elite'); await run(`kill @e[type=zombie,distance=..20,x=${X},y=${Y},z=${Z}]`);
    await run('execute as TestRat at @s run function bm:mobs/elite/zombie'); await run('execute as TestRat at @s run function bm:mobs/champion/skeleton'); await sleep(300);
    ok('Run by hand: an Elite Zombie and a Champion Skeleton appear in front of you', await has(`@e[type=zombie,tag=bm.elite,x=${X},y=${Y},z=${Z},distance=..6]`) && await has(`@e[type=skeleton,tag=bm.champion,x=${X},y=${Y},z=${Z},distance=..6]`));
    const ta = await run('tag TestRat list');
    ok('... and you stay yourself (no elite tags or effects)', !/bm\.elite|bm\.champion|bm\.tiered/.test(ta) && !/strength/.test(await run('data get entity TestRat active_effects')), ta);
    await run(`kill @e[type=zombie,x=${X},y=${Y},z=${Z},distance=..10]`); await run(`kill @e[type=skeleton,x=${X},y=${Y},z=${Z},distance=..10]`); await run('effect clear TestRat');
  }

  if (want('vorn')) {
    await field();
    let red = 0, each = true;
    for (let i = 0; i < 6; i++) {
      await run(`execute positioned ${X + 4} ${Y} ${Z} run function bm:p32/spawn/trooper`); await sleep(100);
      await run(`damage @e[type=husk,tag=bm.vtroop,limit=1,sort=nearest,x=${X + 4},y=${Y},z=${Z}] 500 minecraft:player_attack by TestRat`); await sleep(400);
      const o = await run(`execute store result score #t126 bm.rng run data get entity @e[type=item,limit=1,sort=nearest,x=${X + 4},y=${Y},z=${Z},nbt={Item:{components:{"minecraft:custom_data":{bm:"xenite_red"}}}}] Item.count`);
      const n = +((o.match(/(\d+)\s*$/) || [0, 0])[1]); if (!(n >= 1 && n <= 2)) each = false; red += n;
      await run(`kill @e[type=item,x=${X + 4},y=${Y},z=${Z},distance=..12]`);
    }
    ok('Every Vorn Trooper drops 1-2 Red Xenite', each, `${red} over 6`);
    const surge = F('p32/inv/surge');
    ok('Invasion nights: a roll a second at 1 in 5, up to 8 Vorn about', /random value 1\.\.5/.test(surge) && /matches 8\.\. run return 0/.test(surge));
  }

  if (want('cecil')) {
    const b = F('p46/pet/bolt/fire');
    ok('Cecil\'s bolt is drawn from his staff to the foe (and stops there)', /positioned ~ ~1\.45 ~ facing entity @e\[tag=bm\.cptgt,limit=1\] eyes/.test(b) && /distance=\.\.1\.6/.test(F('p126/cbeam/fire_s')));
  }

  if (want('gy')) {
    const GX = +(process.env.GX || 41200), GZ = +(process.env.GZ || 41200);
    await run(`execute in minecraft:overworld run forceload add ${GX - 96} ${GZ - 96} ${GX + 96} ${GZ + 96}`); await sleep(6000);
    const pl = await run(`execute in minecraft:overworld run place structure bm:graveyard ${GX} 0 ${GZ}`);
    ok('A new graveyard places (yard + crypt pieces)', /Generated/.test(pl), pl);
    await run(`execute in minecraft:overworld run tp TestRat ${GX} 200 ${GZ}`); await run('effect give TestRat minecraft:slow_falling 60 0 true'); await sleep(2500);
    const ctrl = `@e[type=marker,tag=bm.crypt_ctrl,tag=bm.gy2,x=${GX},y=0,z=${GZ},distance=..200]`;
    ok('Its crypt hangs under it (controller marker, new-graveyard tag)', await has(ctrl));
    const cp = (await run(`data get entity ${ctrl.replace(']', ',limit=1]')} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (cp) await run(`execute in minecraft:overworld run tp TestRat ${cp[1]} ${+cp[2] + 40} ${cp[3]}`);
    let done = false; for (let i = 0; i < 30 && !done; i++) { await sleep(1000); done = await has(ctrl.replace(']', ',tag=bm.gyskd]')); }
    ok('The land round it is graded once (the skirt finished)', done);
    console.log('ctrl', cp && cp.slice(1).join(' '));
    await run('effect clear TestRat'); await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`);
  }

  await run('tag @a remove bm.gvok');   // (the operator's pass that staged the vault)

  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
