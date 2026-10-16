// 2.80d: the Trophy Stand - as a regular (non-op) player: set down with a use on the floor, opened and folded with
// right-clicks on it, picked up with sneak + punch. rcon sets the stage only: the record a player would have earned (two raid
// rooms in gold, one of them in netherite too; the Tier I laurel's advancement; the conquest up to the Frost Marksman) and
// an Archmage Trophy in the pocket (carried = earned).
//   Use on the floor: the stand stands there (one model, one click box), and the item is used up.
//   Right-click: your trophies come out - the Broodmother and the Frost Marksman (conquered) and the Archmage (carried) on the top step, the
//     Combination room in NETHERITE (its best metal) and the Gauntlet in gold on the middle step, the Tier I laurel in front;
//     the plaque counts them (bosses 3/7, heist rooms 2/12, laurels 1/6). Right-click again: folded away.
//   Opened, then walked away from (13+ blocks): it folds by itself.
//   A plain punch: told how to pick it up. Sneak + punch: it comes back to you.
//   Madame Velour sells it.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const X = 16800, Y = 100, Z = 16000;
  const STAND = '@e[type=minecraft:interaction,tag=bm.tstand,limit=1]', SHOW = '@e[tag=bm.tsshow]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} minecraft:stone`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 6} ${Z + 6} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  // the record (as the raids and the conquest would have left it)
  await run('scoreboard players set TestRat bm.tsb 0');
  for (let m = 1; m <= 6; m++) await run(`scoreboard players set TestRat bm.tr${m} 0`);
  await run('scoreboard players set TestRat bm.tr3 5'); await run('scoreboard players set TestRat bm.tr6 1');   // rooms 0 (levers) + 2 (lasers) in gold; levers in netherite
  await run('advancement revoke TestRat from bm:story/raid_t1'); await run('advancement grant TestRat only bm:story/raid_t1');
  await run('scoreboard players set TestRat bm.conq 1');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 90 40`); await sleep(1500);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/trophy_hex'); await sleep(1500);     // carried: earned
  await run('clear TestRat *[custom_data~{bm:"trophy_hex"}]');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/trophy_stand');

  // ---- set down: a use, looking at the floor 2 blocks west
  A.slot(0); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(800);
  ok('used on the floor: the Trophy Stand stands there (its model and its click box)', (await cnt('@e[type=minecraft:item_display,tag=bm.tsbase]')) === 1 && (await cnt(STAND)) === 1);
  ok('...and the item is used up', (await has('trophy_stand')) === 0);
  const sp = (await run(`${O}data get entity ${STAND} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  // ---- right-click: open
  let ent = await entOf(STAND);
  ok('the bot sees the stand\'s click box', !!ent);
  A.interact(ent.entityId); await sleep(900);
  const models = [];
  for (const m of (await run(`${O}execute as @e[type=minecraft:item_display,tag=bm.tsshow] run data get entity @s item.components."minecraft:item_model"`)).split(/(?=TestRat|\w+ has the)/)) models.push(m);
  const showModels = async () => { const out = []; const n = await cnt('@e[type=minecraft:item_display,tag=bm.tsshow]');
    for (let i = 0; i < n; i++) out.push((await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.tsshow,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] item`)).slice(0, 10));
    return out; };
  const ms = await run(`${O}data get storage bm:p161 c`);
  ok('right-click: it opens - six trophies come out, and the plaque', (await cnt('@e[type=minecraft:item_display,tag=bm.tsshow]')) === 6 && (await cnt('@e[type=minecraft:text_display,tag=bm.tsshow]')) === 1,
     `${await cnt('@e[type=minecraft:item_display,tag=bm.tsshow]')} models`);
  const modelOf = async (m) => (await cnt(`@e[type=minecraft:item_display,tag=bm.tsshow,nbt={item:{components:{"minecraft:item_model":"bm:${m}"}}}]`)) === 1;
  ok('...the Broodmother and the Frost Marksman (conquered) and the Archmage (carried) on the top step', await modelOf('trophy3d_brood') && await modelOf('trophy3d_frost') && await modelOf('trophy3d_hex'));
  ok('...the Combination room in its best metal - netherite, not gold - and the Gauntlet in gold', await modelOf('trophy3d_levers_6') && !(await modelOf('trophy3d_levers_3')) && await modelOf('trophy3d_lasers_3'));
  ok('...the Tier I laurel in front', await modelOf('laurel_t1'));
  const tx = await run(`${O}data get entity @e[type=minecraft:text_display,tag=bm.tsshow,limit=1] text`);
  ok('...the plaque: bosses 3/7, heist rooms 2/12, laurels 1/6', /Bosses 3\/7/.test(tx) && /Heist rooms 2\/12/.test(tx) && /Laurels 1\/6/.test(tx), tx.slice(0, 200));
  const by = (await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.tsshow,limit=1,nbt={item:{components:{"minecraft:item_model":"bm:trophy3d_brood"}}}] Pos[1]`)).match(/(-?[\d.]+)d/);
  const ly = (await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.tsshow,limit=1,nbt={item:{components:{"minecraft:item_model":"bm:laurel_t1"}}}] Pos[1]`)).match(/(-?[\d.]+)d/);
  ok('...the bosses stand higher than the laurels (the top step and the front one)', by && ly && +by[1] > +ly[1] + 0.5, `${by && by[1]} vs ${ly && ly[1]}`);
  // ---- right-click again: folded away
  A.interact(ent.entityId); await sleep(900);
  ok('right-click again: folded away', (await cnt(SHOW)) === 0);
  // ---- open, then walk away: it folds by itself
  A.interact(ent.entityId); await sleep(900);
  const opened = (await cnt(SHOW)) === 7;
  await A.walkTo(X + 0.5 + 14, Z + 0.5); await sleep(2500);
  ok('opened, then walked away from (14 blocks): it folds by itself', opened && (await cnt(SHOW)) === 0);
  await A.walkTo(X + 0.5, Z + 0.5); await sleep(1500);
  // ---- punches
  ent = await entOf(STAND); A.bars.length = 0;
  A.attack(ent.entityId); await sleep(800);
  ok('a plain punch: it stays, and says how to pick it up', (await cnt(STAND)) === 1 && A.bars.some(b => /Sneak \+ punch/.test(b)), A.bars.slice(-1).join(''));
  A.input({ shift: true }); await sleep(300); A.attack(ent.entityId); await sleep(900); A.input({}); await sleep(1200);
  ok('sneak + punch: the stand is gone, and back in your pack', (await cnt(STAND)) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.tsbase]')) === 0 && (await has('trophy_stand')) === 1);
  // ---- for sale
  const vel = require('fs').readFileSync(__dirname + '/../../out_p2/BlackMarket_DP/data/bm/function/npc/outfitter.mcfunction', 'utf8');
  ok('Madame Velour sells the Trophy Stand', /trophy_stand/.test(vel));

  await run('clear TestRat'); for (let m = 1; m <= 6; m++) await run(`scoreboard players set TestRat bm.tr${m} 0`);
  await run('scoreboard players set TestRat bm.tsb 0'); await run('advancement revoke TestRat only bm:story/raid_t1'); await run('scoreboard players set TestRat bm.conq 0');
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
