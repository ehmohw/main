// 2.82d: THE CRIMSON WAR HORN AND THE VORN FLEET BEACON - as a regular (non-op) player TestRat, every step a real packet (rcon
// sets the stage: a field, the Blood Moon, whether the fleet has noticed the world (#vornmet), a Zorp to trade with).
//   THE HORN: the Bloodbroker sells it for 13 Blood Crystals. Blown with no Blood Moon: silent, kept. On a Blood Moon, under the
//   open sky: the Monstrosity (and its Herald) rise ten blocks ahead, the horn spent; blown again while it's out: refused.
//   THE BEACON: before the fleet has noticed the world - Zorp doesn't sell it, and switched on it's dead air (kept). Once a Vorn
//   has fallen aboard a Dreadnought: Zorp's stock shows it (24 Green + 4 Red Xenite); switched on, an Invasion Night tonight,
//   the beacon spent; again: the Vorn are already coming.
//   THE FINDS: a won heist (any tier, every raider) rolls 5% for the Crimson Effigy, 5% for the beacon (only once the fleet has
//   noticed the world), and a Blood Moon heist 5% for the horn.
const fs = require('fs');
const { bot, rcon, sleep } = require('./lib_resp');
const OUT = (process.env.BM_OUT || __dirname + '/../../out_p2') + '/BlackMarket_DP/data/bm/function/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const ecnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const cnt = async (id) => { const o = await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const score = async (h) => +((await run(`scoreboard players get ${h} bm.bm`)).match(/has (-?\d+)/) || [0, 0])[1];
  const bars = () => A.bars.map(b => JSON.stringify(b)).join(' ');
  const X = 28000, Y = 100, Z = 28000;
  const MON = '@e[type=minecraft:ravager,tag=bm.monstrosity]';

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 16} ${Y - 1} ${Z - 16} ${X + 16} ${Y - 1} ${Z + 16} minecraft:grass_block`);
  for (let y = Y; y < Y + 24; y += 8) await run(`${O}fill ${X - 16} ${y} ${Z - 16} ${X + 16} ${y + 7} ${Z + 16} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  const use = async (slot) => { A.slot(slot); await sleep(250); A.bars.length = 0; A.chats.length = 0; A.use(); await sleep(400); A.release(); await sleep(900); };

  // ---- the horn at the Bloodbroker
  const blood = fs.readFileSync(OUT + 'npc/blood.mcfunction', 'utf8');
  const hb = blood.slice(blood.lastIndexOf('{buy:', blood.indexOf('bm:"sum_monstrosity"')), blood.indexOf('bm:"sum_monstrosity"'));
  ok('the Bloodbroker sells the Crimson War Horn for 13 Blood Crystals', /count:13,[^]*bm:"blood_crystal"/.test(hb), hb.slice(0, 80));

  // ---- the horn: no Blood Moon, then a Blood Moon
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day');
  await run(`${O}tp ${MON} ~ -400 ~`); await run(`${O}kill ${MON}`); await run(`${O}kill @e[type=minecraft:pillager,tag=bm.herald]`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/sum_monstrosity');
  await use(0);
  ok('blown with no Blood Moon: silent - and the horn is kept', /wait for a Blood Moon/.test(bars()) && (await cnt('sum_monstrosity')) === 1 && (await ecnt(MON)) === 0, bars().slice(0, 200));
  await run('function bm:admin/blood_moon');
  await wait(15000, async () => (await score('#active')) === 1, 500);
  await use(0);
  ok('on a Blood Moon, under the open sky: the Monstrosity rises ahead - the horn spent', await wait(3000, async () => (await ecnt(MON)) === 1) && (await cnt('sum_monstrosity')) === 0,
     A.chats.slice(-1).join(''));
  const mz = +(((await run(`${O}data get entity ${MON.replace(']', ',limit=1]')} Pos[2]`)).match(/(-?[\d.]+)d/) || [0, 0])[1]);
  ok('...about ten blocks ahead of TestRat (south)', mz - Z > 6 && mz - Z < 14, `${(mz - Z).toFixed(1)}`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/sum_monstrosity'); await use(0);
  ok('...blown again while it\'s out: refused, the horn kept', /already abroad/.test(bars()) && (await cnt('sum_monstrosity')) === 1);
  await run(`${O}tp ${MON} ~ -400 ~`); await run(`${O}kill ${MON}`); await run(`${O}tp @e[type=minecraft:pillager,tag=bm.herald] ~ -400 ~`);
  await run('scoreboard players set #forced bm.bm 0'); await run('function bm:bloodmoon/end'); await run('time set day'); await run('clear TestRat');

  // ---- the beacon, and Zorp
  const vm0 = await score('#vornmet');
  const ZORP = `@e[type=minecraft:wandering_trader,tag=bm.npc_alien,x=${X},y=${Y},z=${Z},distance=..12,limit=1]`;
  await run(`${O}kill @e[tag=bm.npc_alien,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}execute positioned ${X + 4.5} ${Y} ${Z + 0.5} run function bm:npc/alien`);
  const sells = async (id) => (await passes(`${O}execute if data entity ${ZORP} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${id}"}}}}]`)) ? 1 : 0;   // (the whole list overflows rcon)
  await run('scoreboard players set #vornmet bm.bm 0'); await sleep(2500);
  ok('before the fleet has noticed the world: Zorp doesn\'t sell the Vorn Fleet Beacon', (await ecnt(ZORP)) === 1 && (await sells('vorn_beacon')) === 0 && (await sells('rocket_boots')) === 1);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/vorn_beacon'); await run('scoreboard players set #ivn bm.bm 0');
  await use(1);
  ok('...switched on, it\'s dead air - and the beacon is kept', /fleet hasn't noticed/.test(bars()) && (await cnt('vorn_beacon')) === 1 && (await score('#ivn')) === 0, bars().slice(0, 200));
  await run('scoreboard players set #vornmet bm.bm 1');
  ok('once a Vorn has fallen aboard a Dreadnought: Zorp\'s stock shows the beacon', await wait(3000, async () => (await sells('vorn_beacon')) === 1));
  await use(1);
  ok('...switched on: an Invasion Night tonight, the beacon spent', (await score('#ivn')) === 1 && (await score('#iday')) === (await score('#day')) && (await cnt('vorn_beacon')) === 0 &&
     A.chats.some(c => /Vorn are coming tonight/.test(c)), A.chats.slice(-1).join(''));
  await run('loot replace entity TestRat hotbar.1 loot bm:items/vorn_beacon'); await use(1);
  ok('...switched on again: the Vorn are already coming (kept)', /already coming tonight/.test(bars()) && (await cnt('vorn_beacon')) === 1);

  // ---- the finds
  const finds = fs.readFileSync(OUT + 'p105/finds.mcfunction', 'utf8');
  ok('a won heist (any tier) rolls 5% for the Crimson Effigy, 5% for the beacon only once the fleet has noticed the world, and a Blood Moon heist 5% for the horn',
     /matches \.\.5 run function bm:p148\/find\/effigy/.test(finds) && /#vornmet bm\.bm matches 1 if score #r bm\.rng matches \.\.5 run function bm:p148\/find\/beacon/.test(finds) &&
     /#gn bm\.rng matches 1 if score #r bm\.rng matches \.\.5 run function bm:p148\/find\/horn/.test(finds));

  // ---- clean up
  await run(`scoreboard players set #vornmet bm.bm ${vm0}`); await run('scoreboard players set #ivn bm.bm 0');
  await run(`${O}kill @e[tag=bm.npc_alien,x=${X},y=${Y},z=${Z},distance=..12]`); await run(`${O}kill @e[tag=bm.alien_sprite,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
