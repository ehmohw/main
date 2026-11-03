// 3.0g: PEARLMAN THE FOLLOWER, A RIG AT THE TRADER'S SIZE (pearlman_art, phase128), AND HIS JOKE FORMS, as a regular (non-op) player:
// his Business Card used as an item (call, sneak + use for his menu, its Wardrobe pressed), his cat right-clicked holding an
// Ethereal Gem or a Wraithfire Heart; rcon sets the stage (a floor, the trader beside him, a pool, a NoAI husk) and reads NBT.
//   size    called: his rig (7 parts, bm.pmd + bm.pmp_<part>) - each part's display at the trader's own scale (0.76), not 0.55
//   anim    standing about: idle (bm.pms 0), the summon's tip of the hat first (7); led off at a run he waddles/runs (1 / 2) and
//           his body's pose changes as he goes (its left_rotation tick to tick); right-clicked empty-handed he sits (4, his sit
//           pose); in water he swims (10)
//   forms   right-click him holding an Ethereal Gem: kept (one gone from your hand), bm.pmef 11, his parts in their '_e' models
//           ("Gem Appraiser of the Cosmos"); his wardrobe's "Joke form" row turns it off (1: his own models) and on again; a
//           husk near: his Cosmic Appraisal strikes it; the Wraithfire Heart given: the gem back in your pocket, bm.pmef 12, '_w';
//           "Give back the gem / heart": the heart back, bm.pmef 0, his own models
//   node t352.js [size|anim|forms]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const O = 'execute in minecraft:overworld run ';
const X = 21520, Y = 100, Z = 16400;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (cmd) => +(((await run(cmd)).match(/(-?[\d.]+)[a-z]?$/) || [0, NaN])[1]);
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const CAT = '@e[type=minecraft:cat,tag=bm.pmpet,limit=1]';
  const part = (p) => `@e[type=minecraft:item_display,tag=bm.pmp_${p},limit=1]`;
  const model = async (p = 'body') => ((await run(`${O}data get entity ${part(p)} item.components."minecraft:item_model"`)).match(/"([^"]+)"/) || [0, ''])[1];
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release();
    if (sneak) { A.input({}); await sleep(150); } };
  const click = async () => { const e = await entOf(CAT); if (!e) return false; A.interact(e.entityId); await sleep(700); return true; };
  const at = async (x, z) => { await run(`${O}tp TestRat ${x} ${Y} ${z} 0 0`); await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.3 && Math.abs(A.pos.z - z) < 0.3, 100); A.stand(); await sleep(300); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 30} ${Z - 30} ${X + 30} ${Z + 30}`); await sleep(1500);
  await run(`${O}fill ${X - 24} ${Y - 1} ${Z - 6} ${X + 24} ${Y - 1} ${Z + 6} minecraft:stone`); await run(`${O}fill ${X - 24} ${Y} ${Z - 6} ${X + 24} ${Y + 8} ${Z + 6} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..32]`);
  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/go`); await sleep(500);
  await run('scoreboard players set TestRat bm.pmef 0'); await run('scoreboard players set TestRat bm.pmsea 1');      // (his own colours: no season)
  await at(X + 0.5, Z + 0.5);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/pearl_card'); await sleep(600);
  await use(0);
  ok('His Business Card: Pearlman out', await wait(5000, async () => (await cnt(CAT)) === 1));
  await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.pmd]')) >= 7);

  if (on('size')) {
    const n = await cnt(`@e[type=minecraft:item_display,tag=bm.pmd,x=${X},y=${Y},z=${Z},distance=..10]`);
    const parts = ['body', 'head', 'hat', 'armr', 'arml', 'legr', 'legl'];
    let all = true; for (const p of parts) if ((await cnt(part(p))) !== 1) all = false;
    ok('his rig: seven parts, one of each (body, head, hat, two flippers, two feet)', n === 7 && all, `displays ${n}`);
    await run(`${O}execute positioned ${X + 3.5} ${Y} ${Z + 0.5} run function bm:p60/pm/spawn`); await sleep(1500);
    const trader = await num(`${O}data get entity @e[type=minecraft:item_display,tag=bm.pearld,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] transformation.scale[0]`);
    const mine = await num(`${O}data get entity ${part('body')} transformation.scale[0]`);
    ok('...at the trader\'s own size (a part\'s scale = the trader\'s display\'s, 0.76 - not 0.55)', Math.abs(trader - mine) < 0.01 && mine > 0.7, `trader ${trader}, Pearlman ${mine}`);
    await run(`${O}execute as @e[type=minecraft:villager,tag=bm.pearl,x=${X},y=${Y},z=${Z},distance=..10] at @s run function bm:p60/pm/leave`); await sleep(500);
    await run(`${O}kill @e[tag=bm.pearl,x=${X},y=${Y},z=${Z},distance=..10]`); await run(`${O}kill @e[tag=bm.pearld,x=${X},y=${Y},z=${Z},distance=..10]`);
  }

  if (on('anim')) {
    await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/go`); await sleep(800);
    await use(0); await wait(5000, async () => (await cnt(CAT)) === 1);
    ok('called: he tips his hat (state 7)', await wait(2000, async () => (await sc(CAT, 'bm.pms')) === 7, 100));
    ok('...then stands about (idle, state 0)', await wait(5000, async () => (await sc(CAT, 'bm.pms')) === 0, 200));
    // (led off: you run, he follows - a waddle or a run, his body's pose changing as he goes)
    const seen = new Set(); const rots = new Set();
    for (let i = 0; i < 24; i++) {
      await run(`${O}tp TestRat ${X + 0.5 + (i % 2 ? -14 : 14)} ${Y} ${Z + 0.5}`); A.stand();
      for (let k = 0; k < 6; k++) { seen.add(await sc(CAT, 'bm.pms')); rots.add(await run(`${O}data get entity ${part('body')} transformation.left_rotation`)); await sleep(150); }
      if (seen.has(1) && seen.has(2) && rots.size > 4) break;
    }
    ok('led off: he walks (state 1) or runs (state 2)', seen.has(1) || seen.has(2), `states ${[...seen].join(',')}`);
    ok('...his body\'s pose changes as he goes (its turn, sampled, several different)', rots.size >= 3, `${rots.size} different`);
    await at(X + 0.5, Z + 0.5); await run(`${O}tp ${CAT} ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(1500);
    await click();
    ok('right-clicked empty-handed: he sits (state 4)', await wait(3000, async () => (await sc(CAT, 'bm.pms')) === 4), `sitting ${await run(`${O}data get entity ${CAT} Sitting`)}`);
    await sleep(1500);
    const sitY = await num(`${O}data get entity ${part('body')} transformation.translation[1]`);
    ok('...down on his tail (the body lowered in its sit pose)', sitY < -0.03, `body translation y ${sitY}`);
    await click(); await sleep(500);
    await run(`${O}fill ${X + 6} ${Y - 2} ${Z - 2} ${X + 10} ${Y} ${Z + 2} minecraft:water`);
    await run(`${O}tp ${CAT} ${X + 8.5} ${Y - 1} ${Z + 0.5}`);
    ok('in water: he swims (state 10)', await wait(3000, async () => { await run(`${O}tp ${CAT} ${X + 8.5} ${Y - 1} ${Z + 0.5}`); return (await sc(CAT, 'bm.pms')) === 10; }, 200));
    await run(`${O}fill ${X + 6} ${Y - 2} ${Z - 2} ${X + 10} ${Y} ${Z + 2} minecraft:stone`); await run(`${O}fill ${X + 6} ${Y} ${Z - 2} ${X + 10} ${Y} ${Z + 2} minecraft:air`);
    await run(`${O}tp ${CAT} ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(800);
  }

  if (on('forms')) {
    await at(X + 0.5, Z + 0.5); await run(`${O}tp ${CAT} ${X + 2.5} ${Y} ${Z + 0.5}`); await sleep(1000);
    await run('loot replace entity TestRat hotbar.1 loot bm:items/ethereal_gem'); await run('loot replace entity TestRat hotbar.2 loot bm:items/wraithfire_heart');
    A.slot(1); await sleep(400); await click(); await sleep(800);
    ok('right-clicked holding an Ethereal Gem: he keeps it (gone from your hand), bm.pmef 11', (await sc('TestRat', 'bm.pmef')) === 11 && (await has('ethereal_gem')) === 0,
       `pmef ${await sc('TestRat', 'bm.pmef')} gems ${await has('ethereal_gem')}`);
    ok('...GEM APPRAISER OF THE COSMOS: his parts in their Ethereal models', await wait(2000, async () => /pmr_body_e$/.test(await model()) && /pmr_hat_e$/.test(await model('hat'))), await model());
    ok('...and he didn\'t sit down for it', !/1b/.test(await run(`${O}data get entity ${CAT} Sitting`)));
    // (his wardrobe: sneak + use the card -> Wardrobe -> Joke form)
    await sleep(2300); let n0 = A.dialogN.length; await use(0, true); await wait(3000, async () => A.dialogN.length > n0);
    n0 = A.dialogN.length; await A.press(/Wardrobe/); await wait(3000, async () => A.dialogN.length > n0);
    ok('his wardrobe lists the row: "Joke form  Cosmic: on"', A.buttons().some(b => /Joke form.*Cosmic: on/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
    n0 = A.dialogN.length; await A.press(/Joke form/); await wait(3000, async () => A.dialogN.length > n0);
    ok('...pressed: off - his own models (bm.pmef 1)', (await sc('TestRat', 'bm.pmef')) === 1 && await wait(2000, async () => /pmr_body$/.test(await model())), await model());
    await sleep(1200); n0 = A.dialogN.length; await A.press(/Joke form/); await wait(3000, async () => A.dialogN.length > n0);
    ok('...pressed again: on (bm.pmef 11, the Ethereal models)', (await sc('TestRat', 'bm.pmef')) === 11 && await wait(2000, async () => /pmr_body_e$/.test(await model())), await model());
    A.cmd('trigger bm.act set 2'); await sleep(500);
    // (a husk near: COSMIC APPRAISAL)
    await run(`${O}summon minecraft:husk ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["t352","bm.seen"],NoAI:1b,PersistenceRequired:1b,Health:100f,attributes:[{id:"minecraft:max_health",base:100d}]}`);
    const h0 = 100; let h1 = 100;
    await wait(9000, async () => { h1 = await num(`${O}data get entity @e[type=minecraft:husk,tag=t352,limit=1] Health`); return h1 <= h0 - 15; }, 300);
    ok('a husk near: his Cosmic Appraisal strikes it (18)', h1 <= h0 - 15, `husk ${h1}`);
    await run(`${O}kill @e[type=minecraft:husk,tag=t352]`);
    // (the heart: the Soul Broker - and the gem comes back)
    A.slot(2); await sleep(400); await click(); await sleep(800);
    ok('the Wraithfire Heart handed over: bm.pmef 12, SOUL BROKER models - and the gem back in your pocket',
       (await sc('TestRat', 'bm.pmef')) === 12 && (await has('ethereal_gem')) === 1 && await wait(2000, async () => /pmr_body_w$/.test(await model())),
       `pmef ${await sc('TestRat', 'bm.pmef')} gems ${await has('ethereal_gem')} model ${await model()}`);
    await sleep(2300); n0 = A.dialogN.length; await use(0, true); await wait(3000, async () => A.dialogN.length > n0);
    n0 = A.dialogN.length; await A.press(/Wardrobe/); await wait(3000, async () => A.dialogN.length > n0);
    n0 = A.dialogN.length; await A.press(/Give back the gem/); await wait(3000, async () => A.dialogN.length > n0);
    ok('"Give back the gem / heart": the heart back, bm.pmef 0, his own models', (await sc('TestRat', 'bm.pmef')) === 0 && (await has('wraithfire_heart')) === 1 &&
       await wait(2000, async () => /pmr_body$/.test(await model())), `pmef ${await sc('TestRat', 'bm.pmef')} hearts ${await has('wraithfire_heart')} model ${await model()}`);
    A.cmd('trigger bm.act set 2'); await sleep(500);
  }

  await run(`${O}execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/go`); await run('scoreboard players set TestRat bm.pmsea 0');
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
