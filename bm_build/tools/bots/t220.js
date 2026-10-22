// 2.83: THE LESS URGENT LIST, part one, as a regular (non-op) player TestRat - every step a real packet (rcon sets the stage).
//   THE BANKER'S CARD: its Exchange page swaps 5 Tokens for a Medallion and back (the account, no fee); Auto-deposit switched on
//   from its menu sweeps Medallions from the pockets into the account and leaves 8 of 20 Tokens on hand; taking 1 out rests it.
//   THE COLLECTORS: Dennis's Ore Magnet switched on (right-click) pulls raw iron lying 5 blocks off into the pack; Pistachio's
//   Spirit Jar, rotten flesh; switched off, the iron stays put; a full pack says so.
//   A FLOOR DISPLAY CASE set down is solid (a barrier in its block); picked up (sneak + punch), the barrier is gone.
//   THE TROPHY STAND set down faces you (its model turned half round).
//   (set-ups run as functions, checked by what they leave) A heist's Blood Moon Guard: diamond, a Sharpness III diamond axe, half
//   again the tier's health; Celi's encounter on a thin snow layer stands on the ground; a held Seawatch Fort opens again for a
//   player without Leo's crest.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async (sel) => { const m = (await run(`execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const hasV = async (id) => { const m = (await run(`clear TestRat ${id} 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const sc = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const X = 14100, Y = 120, Z = 14100;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 5} ${Z + 8} minecraft:air`);
  const home = async (pitch = 0) => { await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 ${pitch}`); await sleep(800); };
  await home();

  // ================================================================== THE BANKER'S CARD
  for (const o of ['bm.bk_tok', 'bm.bk_med', 'bm.bkac', 'bm.bkag']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.bk_tok 10');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bankers_card'); await sleep(300);
  A.slot(0); await sleep(250); let d = await A.useWait(2500); if (!d) { await use(0); await sleep(800); }
  ok('the card opens the Rat Bank: an Exchange button and Auto-deposit (off)', A.buttons().some(b => /Exchange/.test(b.label)) && A.buttons().some(b => /Auto-deposit: off/.test(b.label)),
     A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  await A.press(/^Exchange/);
  ok('the Exchange page: 10 Tokens in the account', A.buttons().some(b => /5 Tokens.*1 Medallion/.test(b.label)));
  await A.press(/5 Tokens.*1 Medallion/); await sleep(300);
  ok('5 Tokens -> 1 Medallion (account 5 / 1)', (await sc('bm.bk_tok')) === 5 && (await sc('bm.bk_med')) === 1, `${await sc('bm.bk_tok')} / ${await sc('bm.bk_med')}`);
  await A.press(/1 Medallion.*5 Tokens/); await sleep(300);
  ok('...and back, no fee (account 10 / 0)', (await sc('bm.bk_tok')) === 10 && (await sc('bm.bk_med')) === 0, `${await sc('bm.bk_tok')} / ${await sc('bm.bk_med')}`);
  await A.press(/1 Medallion.*5 Tokens/); await sleep(300);
  ok('...with no Medallion in the account, nothing changes', (await sc('bm.bk_tok')) === 10);
  await A.press(/Your account/);
  await A.press(/Auto-deposit/);
  ok('Auto-deposit: ON', (await sc('bm.bkac')) === 1 && A.buttons().some(b => /Auto-deposit: ON/.test(b.label)));
  await run('loot give TestRat loot bm:items/medallion'); await run('loot give TestRat loot bm:items/medallion');
  for (let i = 0; i < 20; i++) await run('loot give TestRat loot bm:items/token');
  await wait(3000, async () => (await has('medallion')) === 0);
  ok('...the Medallions in the pocket go into the account', (await has('medallion')) === 0 && (await sc('bm.bk_med')) === 2, `${await has('medallion')} on, ${await sc('bm.bk_med')} banked`);
  ok('...20 Tokens: 12 banked, 8 kept for a fee', (await has('token')) === 8 && (await sc('bm.bk_tok')) === 22, `${await has('token')} on, ${await sc('bm.bk_tok')} banked`);
  await run('execute as TestRat at @s run function bm:p31/bank/open'); await sleep(800);
  await A.press(/Medallions/); await A.press(/Take 1/); await sleep(2200);
  ok('taking a Medallion out: it stays in the pocket (auto-deposit rests)', (await has('medallion')) === 1 && (await sc('bm.bkag')) > 0, `${await has('medallion')} ${await sc('bm.bkag')}`);
  await run('scoreboard players set TestRat bm.bkac 0'); await run('clear TestRat');

  // ================================================================== THE COLLECTORS (2.88: satchels - what they gather goes into them, not the pack)
  await home();
  const inside = async (slot) => await run(`data get entity TestRat Inventory[{Slot:${slot}b}].components."minecraft:container"`);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/ore_magnet'); await sleep(300);
  await run(`${O}summon minecraft:item ${X + 5.5} ${Y} ${Z + 0.5} {Item:{id:"minecraft:raw_iron",count:3},Tags:["bm.t220i"]}`);
  await wait(3000, async () => /raw_iron/.test(await inside(1)));
  ok("Dennis's Ore Magnet carried: the raw iron 5 blocks off goes into the magnet", /raw_iron/.test(await inside(1)) && (await hasV('minecraft:raw_iron')) === 0, (await inside(1)).slice(-120));
  await run(`${O}summon minecraft:item ${X + 5.5} ${Y} ${Z + 0.5} {Item:{id:"minecraft:rotten_flesh",count:2},Tags:["bm.t220i"]}`); await sleep(1500);
  ok('...but not rotten flesh (not its kind) - it stays on the ground', !/rotten_flesh/.test(await inside(1)) && (await hasV('minecraft:rotten_flesh')) === 0 &&
     (await cnt(`@e[type=minecraft:item,x=${X + 5.5},y=${Y},z=${Z + 0.5},distance=..2]`)) >= 1);
  await run('loot replace entity TestRat hotbar.2 loot bm:items/spirit_jar');
  await wait(3000, async () => /rotten_flesh/.test(await inside(2)));
  ok("Pistachio's Spirit Jar carried: the rotten flesh floats into the jar, not the pack", /rotten_flesh/.test(await inside(2)) && (await hasV('minecraft:rotten_flesh')) === 0);
  // right-click: it unfolds into a barrel with what it gathered; walked away from, it packs up and keeps it
  // (right-clicked, it sets a barrel down on the ground in front of you; you open that like any barrel)
  A.windows.length = 0; await use(1); await sleep(900);
  const unfolded = await wait(2000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.bx_orecol]`)) === 1);
  const bp = (await run(`${O}data get entity @e[type=minecraft:marker,tag=bm.bx_orecol,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (bp) { A.useOn(Math.floor(+bp[1]), Math.floor(+bp[2]), Math.floor(+bp[3]), 1); await sleep(900); }
  const bw = A.windows[A.windows.length - 1];
  ok('the magnet right-clicked: it unfolds into a barrel in front of you - opened, a container window', unfolded && !!bw, bw ? JSON.stringify(bw).slice(0, 120) : `no window (unfolded ${unfolded})`);
  if (bw) A.close(bw.windowId); await sleep(400);
  await run(`${O}tp TestRat ${X - 7.5} ${Y} ${Z + 0.5} 0 0`); await sleep(3000);
  ok('...walked away from: packed up, the raw iron still inside', (await cnt('@e[type=minecraft:marker,tag=bm.bx_orecol]')) === 0 && /raw_iron/.test(await inside(1)), (await inside(1)).slice(-120));
  // (a full magnet)
  const full = Array.from({ length: 27 }, (_, i) => `{slot:${i},item:{id:"minecraft:stone",count:64}}`).join(',');
  await run(`item modify entity TestRat hotbar.1 {function:"minecraft:set_components",components:{"minecraft:container":[${full}]}}`); await run('scoreboard players set TestRat bm.vfcd 0');
  A.bars.length = 0;
  await run(`${O}summon minecraft:item ${X - 3.5} ${Y} ${Z + 0.5} {Item:{id:"minecraft:raw_gold",count:1},Tags:["bm.t220i"]}`);
  await wait(7000, async () => A.bars.some(b => /is full/.test(b)));
  ok('a full magnet: "Your Ore Magnet is full"', A.bars.some(b => /Ore Magnet is full/.test(b)), A.bars.slice(-2).join(' | '));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..30]`); await run('clear TestRat');

  // ================================================================== A FLOOR DISPLAY CASE, solid
  await home(60);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/display_case_oak'); await sleep(300);
  await use(0); await sleep(600);
  const box = await run(`${O}execute as @e[type=minecraft:interaction,tag=bm.dchit,x=${X},y=${Y},z=${Z},distance=..4,limit=1] at @s run data get entity @s Pos`);
  const m = box.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/);
  ok('a case set down on the floor', !!m, box.slice(0, 120));
  if (m) {
    const bx = Math.floor(+m[1]), by = Math.floor(+m[2]), bz = Math.floor(+m[3]);
    ok('...and its block is solid: a barrier', await passes(`${O}execute if block ${bx} ${by} ${bz} minecraft:barrier`));
    ok('...its click box a hair over a block (1.02)', /1\.02/.test(await run(`${O}data get entity @e[type=minecraft:interaction,tag=bm.dchit,x=${X},y=${Y},z=${Z},distance=..4,limit=1] width`)));
    const near = Object.values(A.ents).filter(e => Math.abs(e.x - +m[1]) < 0.3 && Math.abs(e.z - +m[3]) < 0.3 && Math.abs(e.y - +m[2]) < 0.6);
    const eid = near.length > 0;
    A.input({ shift: true }); await sleep(250); for (const e of near) { A.attack(e.entityId); await sleep(150); } await sleep(400); A.input({}); await sleep(600);
    ok('sneak + punch: the case comes back to the pack, the barrier goes', (await has('display_case_oak')) === 1 && await passes(`${O}execute if block ${bx} ${by} ${bz} minecraft:air`),
       `case ${await has('display_case_oak')} eid ${!!eid}`);
  }
  await run('clear TestRat');

  // ================================================================== THE TROPHY STAND faces you
  await home(50);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/trophy_stand'); await sleep(300);
  await use(0); await sleep(800);
  const lr = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.tsbase,x=${X},y=${Y},z=${Z},distance=..6,limit=1] transformation.left_rotation`);
  ok('the Trophy Stand set down: turned half round to face you', /\[0\.0f, 1\.0f, 0\.0f, 0\.0f\]/.test(lr), lr.slice(-60));
  await run(`${O}kill @e[tag=bm.tsd,x=${X},y=${Y},z=${Z},distance=..6]`); await run(`${O}kill @e[type=minecraft:interaction,tag=bm.tstand,x=${X},y=${Y},z=${Z},distance=..6]`);

  // ================================================================== (set-ups) a Blood Moon guard; Celi on snow; a fort opening again
  await run('scoreboard players set #gn bm.rng 1'); await run('scoreboard players set #gt bm.rng 5'); await run('scoreboard players set #gi bm.rng 0');
  await run(`${O}summon minecraft:vindicator ${X + 3.5} ${Y} ${Z + 3.5} {Tags:["bm.t220g"],NoAI:1b,PersistenceRequired:1b}`);
  await run(`${O}execute as @e[type=minecraft:vindicator,tag=bm.t220g,limit=1] at @s run function bm:p70/guard_set1`);
  const gd = await run(`${O}data get entity @e[type=minecraft:vindicator,tag=bm.t220g,limit=1]`);
  const gh = await run(`${O}attribute @e[type=minecraft:vindicator,tag=bm.t220g,limit=1] minecraft:max_health base get`);
  ok("a heist's Blood Moon Guard: diamond armour, a Sharpness III diamond axe, not the netherite brute",
     /Blood Moon Guard/.test(gd) && /diamond_axe/.test(gd) && /diamond_chestplate/.test(gd) && !/netherite/.test(gd));
  // (a guard's own health scales with the run - crew, modifiers - and any guard may roll an odd affix (Tiny, Ironclad...)
  //  afterwards, so the Blood Moon's "half again" is checked on its own: a guard of 80 becomes 120)
  const num = t => +((t.match(/([\d.]+)\s*$/) || [])[1]);
  await run(`${O}kill @e[type=minecraft:vindicator,tag=bm.t220g]`);
  await run(`${O}summon minecraft:vindicator ${X + 3.5} ${Y} ${Z + 3.5} {Tags:["bm.t220g"],NoAI:1b,PersistenceRequired:1b,attributes:[{id:"minecraft:max_health",base:80d}],Health:80f}`);
  await run(`${O}execute as @e[type=minecraft:vindicator,tag=bm.t220g,limit=1] at @s run function bm:p174/gv_blood`);
  const bh = num(await run(`${O}attribute @e[type=minecraft:vindicator,tag=bm.t220g,limit=1] minecraft:max_health base get`));
  ok('...its health half again (a guard of 80: 120)', bh === 120, `${bh}`);
  await run(`${O}kill @e[type=minecraft:vindicator,tag=bm.t220g]`);
  await run(`${O}fill ${X - 3} ${Y} ${Z - 3} ${X - 1} ${Y} ${Z - 1} minecraft:snow[layers=1]`); await run(`${O}fill ${X - 3} ${Y - 1} ${Z - 3} ${X - 1} ${Y - 1} ${Z - 1} minecraft:snow_block`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.ceenc]`);
  await run(`${O}execute positioned ${X - 1.5} ${Y} ${Z - 1.5} run function bm:p66/enc/place2`); await sleep(300);
  const cy = (await run(`${O}data get entity @e[type=minecraft:interaction,tag=bm.ceenc,limit=1,sort=nearest] Pos[1]`)).match(/([\d.]+)d/);
  ok('Celi on a thin snow layer stands on the ground, not a block above it', cy && Math.abs(+cy[1] - Y) < 0.2, cy ? cy[1] : 'none');
  await run(`${O}execute as @e[type=minecraft:interaction,tag=bm.ceenc] at @s run function bm:p66/enc/gone`); await run(`${O}kill @e[tag=bm.ceencp]`);
  await run(`${O}summon minecraft:marker ${X + 2.5} ${Y} ${Z - 2.5} {Tags:["bm.lefort","bm.ledone","bm.t220f"]}`);
  await wait(4000, async () => !(await passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.t220f,tag=bm.ledone]`)));
  ok("a held fort opens again for a player without Leo's crest", !(await passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.t220f,tag=bm.ledone]`)));
  await run(`${O}execute as @e[type=minecraft:interaction,tag=bm.leenc,x=${X},y=${Y},z=${Z},distance=..12] at @s run function bm:p96/enc/gone`);
  await run(`${O}kill @e[type=minecraft:marker,tag=bm.t220f]`);

  // ================================================================== THE VAULT HALL: a gallery all the way round; a guard under the floor comes home
  // (a Tier IV vault placed far out in the gutter - the room is the stage, its own init builds the gallery, the leash runs by itself)
  const GU = 'execute in bm:gutter run ', VX = 9000, VY = 100, VZ = 9000;
  await run(`${GU}forceload add ${VX - 8} ${VZ - 8} ${VX + 44} ${VZ + 32}`); await sleep(2500);
  await run(`${GU}kill @e[x=${VX},y=${VY - 8},z=${VZ},dx=40,dy=30,dz=26,type=!player]`);
  await run(`${GU}place template bm:gv_vault_t4 ${VX} ${VY} ${VZ}`); await sleep(500);
  const VM = `@e[type=minecraft:marker,tag=bm.gvr_vault,x=${VX},y=${VY},z=${VZ},dx=40,dy=20,dz=26,limit=1]`;
  await run(`${GU}execute as ${VM} at @s run function bm:p173/perch_vault`);
  const ring = [[1, 12], [23, 12], [12, 1], [12, 23], [2, 2], [22, 22], [1, 2], [2, 1]];
  let solid = 0; for (const [x, z] of ring) solid += await passes(`${GU}execute unless block ${VX + x} ${VY + 9} ${VZ + z} minecraft:air`);
  ok('the vault hall\'s gallery runs round all four walls (ends and corners too)', solid === ring.length, `${solid}/${ring.length}`);
  ok('...its ladders reach the gallery', await passes(`${GU}execute if block ${VX + 3} ${VY + 9} ${VZ + 1} minecraft:ladder`) && await passes(`${GU}execute if block ${VX + 21} ${VY + 9} ${VZ + 23} minecraft:ladder`));
  await run(`${GU}summon minecraft:vindicator ${VX + 8.5} ${VY + 4} ${VZ + 8.5} {Tags:["bm.gvg","bm.t220v"],NoAI:1b,PersistenceRequired:1b,Invulnerable:1b}`);
  await wait(3000, async () => passes(`${GU}execute if entity @e[type=minecraft:vindicator,tag=bm.t220v,tag=bm.gvlsh]`));
  await run(`${GU}tp @e[type=minecraft:vindicator,tag=bm.t220v] ${VX + 8.5} ${VY + 1} ${VZ + 8.5}`);
  await run(`${GU}setblock ${VX + 8} ${VY + 1} ${VZ + 8} minecraft:air`); await run(`${GU}setblock ${VX + 8} ${VY + 2} ${VZ + 8} minecraft:air`);
  const cameBack = await wait(4000, async () => passes(`${GU}execute if entity @e[type=minecraft:vindicator,tag=bm.t220v,x=${VX},y=${VY + 3.6},z=${VZ},dx=37,dy=10,dz=25]`));
  ok('a guard sunk under the hall\'s floor is sent back up into the room', cameBack);
  await run(`${GU}kill @e[x=${VX},y=${VY - 8},z=${VZ},dx=40,dy=30,dz=26,type=!player]`);
  await run(`${GU}fill ${VX} ${VY} ${VZ} ${VX + 36} ${VY + 15} ${VZ + 24} minecraft:air`);

  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log(e); process.exit(1); });
